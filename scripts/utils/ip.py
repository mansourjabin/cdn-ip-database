import ipaddress
from typing import Iterable, List


def is_ip_or_cidr(value: str) -> bool:
    try:
        ipaddress.ip_network(value, strict=False)
        return True
    except ValueError:
        return False


def normalize_dedupe_sort(items: Iterable[str]) -> List[str]:
    seen = set()
    out = []
    for item in items:
        if not item:
            continue
        candidate = item.strip()
        if candidate and candidate not in seen:
            seen.add(candidate)
            out.append(candidate)
    out.sort(key=lambda s: (":" in s, s))  # IPv4 first, then IPv6, lexicographic
    return out


def extract_ips_from_text(text: str) -> List[str]:
    ips = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Some providers include inline comments after space
        token = line.split()[0]
        if is_ip_or_cidr(token):
            ips.append(token)
    return ips
