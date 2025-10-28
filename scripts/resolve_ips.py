import json
import os
import sys
from typing import Dict, List

# Ensure project root is on sys.path for local imports
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.utils.http import get_session, fetch
from scripts.utils.ip import is_ip_or_cidr, extract_ips_from_text, normalize_dedupe_sort
from scripts.providers.aws import parse_aws_ip_ranges_json


def resolve_ips(sources_path: str) -> Dict[str, Dict[str, List[str]]]:
    with open(sources_path, 'r', encoding='utf-8') as f:
        sources = json.load(f)

    session = get_session()

    resolved_data: Dict[str, Dict[str, List[str]]] = {}
    for source in sources:
        provider = source['provider']
        resolved_data[provider] = {
            'ips': list(source.get('static_ips', [])),
            'asns': list(source.get('asns', [])),
        }

        for url in source.get('urls', []):
            try:
                resp = fetch(session, url)
                ct = (resp.headers.get('Content-Type') or '').lower()

                if 'json' in ct:
                    data = resp.json()
                    if 'amazonaws.com' in url:
                        ips = parse_aws_ip_ranges_json(data)
                    else:
                        # Generic JSON walker (fallback)
                        ips = [item for item in _find_ips_in_json(data) if is_ip_or_cidr(item)]
                else:
                    ips = extract_ips_from_text(resp.text)

                resolved_data[provider]['ips'].extend(ips)
            except Exception as e:
                print(f"Could not fetch {url} for {provider}: {e}")

        # Deduplicate/sort for determinism
        resolved_data[provider]['ips'] = normalize_dedupe_sort(resolved_data[provider]['ips'])

    # Sort providers deterministically by name
    ordered = {k: resolved_data[k] for k in sorted(resolved_data.keys())}
    return ordered


def _find_ips_in_json(data):
    if isinstance(data, dict):
        for v in data.values():
            yield from _find_ips_in_json(v)
    elif isinstance(data, list):
        for item in data:
            yield from _find_ips_in_json(item)
    elif isinstance(data, str):
        yield data


if __name__ == "__main__":
    # Try data/ then root for sources.json
    candidates = [
        'data/sources.json',
        'sources.json',
    ]
    sources_file = None
    for p in candidates:
        try:
            with open(p, 'r', encoding='utf-8'):
                sources_file = p
                break
        except FileNotFoundError:
            continue
    if not sources_file:
        raise FileNotFoundError('sources.json not found in expected locations')

    resolved_ips_data = resolve_ips(sources_file)
    # Write to data path
    with open('data/resolved_ips.json', 'w', encoding='utf-8') as f:
        json.dump(resolved_ips_data, f, indent=2, sort_keys=True)
