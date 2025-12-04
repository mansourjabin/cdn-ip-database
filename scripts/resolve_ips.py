import json
import os
from typing import Any, Dict, List

from scripts.providers.aws import parse_aws_ip_ranges_json
from scripts.utils.http import fetch, get_session
from scripts.utils.ip import (
    extract_ips_from_text,
    is_ip_or_cidr,
    normalize_dedupe_sort,
)


def _extract_ips_from_json_like(obj: Any) -> List[str]:
    collected: List[str] = []
    stack = [obj]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)
        elif isinstance(current, str):
            if is_ip_or_cidr(current):
                collected.append(current)
    return collected


def resolve_for_provider(session, provider_obj: Dict[str, Any]) -> List[str]:
    urls: List[str] = provider_obj.get("urls", []) or []
    static_ips: List[str] = provider_obj.get("static_ips", []) or []

    resolved: List[str] = []
    for url in urls:
        try:
            resp = fetch(session, url)
            content_type = resp.headers.get("Content-Type", "").lower()

            # Prefer JSON path for known AWS CloudFront service
            if "ip-ranges.amazonaws.com" in url or (
                "application/json" in content_type and "ip-ranges" in url
            ):
                try:
                    data = resp.json()
                    resolved.extend(parse_aws_ip_ranges_json(data))
                    continue
                except Exception:
                    pass

            # Generic JSON parsing
            if "application/json" in content_type or url.endswith(".json"):
                try:
                    data = resp.json()
                    resolved.extend(_extract_ips_from_json_like(data))
                    continue
                except Exception:
                    # fall back to text scan
                    pass

            # Text lists
            resolved.extend(extract_ips_from_text(resp.text))
        except Exception:
            # Skip on failure; keep going for other URLs
            continue

    # Merge with static IPs
    resolved.extend(static_ips)
    return normalize_dedupe_sort(resolved)


def main() -> None:
    # Locate sources.json
    source_candidates = [
        os.path.join("data", "sources.json"),
        "sources.json",
    ]
    sources_file = None
    for p in source_candidates:
        if os.path.exists(p):
            sources_file = p
            break
    if not sources_file:
        raise FileNotFoundError("sources.json not found in data/ or project root")

    with open(sources_file, "r", encoding="utf-8") as f:
        providers: List[Dict[str, Any]] = json.load(f)

    session = get_session()

    output: Dict[str, Dict[str, List[str]]] = {}
    all_ips: List[str] = []
    
    for p in providers:
        name = p.get("provider", "")
        if not name:
            continue
        asns = p.get("asns", []) or []
        ips = resolve_for_provider(session, p)
        output[name] = {
            "asns": list(asns),
            "ips": list(ips),
        }
        all_ips.extend(ips)

    # Ensure output directory exists and write original JSON file
    out_candidates = [
        os.path.join("data", "resolved_ips.json"),
        "resolved_ips.json",
    ]
    out_path = out_candidates[0]
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    # Always write to ensure mtime updates (even if content is same)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    # Remove duplicates and sort
    unique_ips = normalize_dedupe_sort(all_ips)

    # Write to cdn.lst file in the same directory as resolved_ips.json
    cdn_lst_path = os.path.join(os.path.dirname(out_path), "cdn.lst")
    with open(cdn_lst_path, "w", encoding="utf-8") as f:
        for ip in unique_ips:
            f.write(ip + "\n")

    print(f"Successfully processed {len(providers)} providers")
    print(f"Generated {out_path} with structured data")
    print(f"Generated {cdn_lst_path} with {len(unique_ips)} unique IP addresses (IPv4 and IPv6)")


if __name__ == "__main__":
    main()