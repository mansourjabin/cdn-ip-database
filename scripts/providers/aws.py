from typing import Dict, List

from scripts.utils.ip import is_ip_or_cidr


def parse_aws_ip_ranges_json(data: Dict, service: str = "CLOUDFRONT_ORIGIN_FACING") -> List[str]:
    ips: List[str] = []
    for item in data.get("prefixes", []) or []:
        if item.get("service") == service:
            cidr = item.get("ip_prefix")
            if cidr and is_ip_or_cidr(cidr):
                ips.append(cidr)
    for item in data.get("ipv6_prefixes", []) or []:
        if item.get("service") == service:
            cidr = item.get("ipv6_prefix")
            if cidr and is_ip_or_cidr(cidr):
                ips.append(cidr)
    return ips
