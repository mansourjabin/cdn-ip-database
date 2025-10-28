<div align="center">

# CDN IP Registry

Official IP ranges (IPv4/IPv6) and ASN numbers for CDN providers. Direct, authoritative source URLs for Cloudflare, Akamai, Fastly, AWS CloudFront, Google Cloud, ArvanCloud, and more.

</div>

---

## Data & Automation

- **Data files**
  - **Sources (source of truth)**: [data/sources.json](data/sources.json)
  - **Resolved IPs (auto-generated daily)**: [data/resolved_ips.json](data/resolved_ips.json)
- **Schedule**: Daily at 00:10 UTC (GitHub Actions)
- **Runtime**: Python 3.12, pinned dependencies
- **Releases**: On changes, an automated release is created with `data/resolved_ips.json` attached.
- **Behavior**:
  - Robust HTTP with retries/backoff; failures are logged and skipped (job continues).
  - AWS `ip-ranges.json` is strictly filtered to `service = CLOUDFRONT_ORIGIN_FACING`.
  - Table below is rebuilt from `data/sources.json`.

### Local usage

```bash
# install
pip install -r cdn-ip-database/requirements.txt

# validate sources.json against schema
python cdn-ip-database/scripts/validate_sources.py

# generate resolved IPs → data/resolved_ips.json
python cdn-ip-database/scripts/resolve_ips.py

# rebuild the README provider table from data/sources.json
python cdn-ip-database/scripts/update_readme.py
```

### Extending providers
- Edit `data/sources.json` and add an object with:
  - `provider` (string), `urls` (array), `asns` (array), `static_ips` (array; optional, may be empty)
- The resolver supports text lists and JSON responses. Add provider-specific parsers as needed under `scripts/providers/`.

## Provider List

| Provider | IP Source(s) | ASN |
|----------|--------------|-----|
| Akamai | [techdocs.akamai.com/property-manager/pdfs/akamai_ipv4_CIDRs.txt](https://techdocs.akamai.com/property-manager/pdfs/akamai_ipv4_CIDRs.txt)<br>[techdocs.akamai.com/property-manager/pdfs/akamai_ipv6_CIDRs.txt](https://techdocs.akamai.com/property-manager/pdfs/akamai_ipv6_CIDRs.txt) | AS12222, AS133103, AS16625, AS16702, AS17204, AS18680, AS18717, AS20189, AS20940, AS21342, AS21357, AS21399, AS22207, AS22452, AS23454, AS23455, AS23903, AS24319, AS26008, AS30675, AS31107, AS31108, AS31109, AS31110, AS31377, AS33047, AS33905, AS34164, AS34850, AS35204, AS35993, AS35994, AS36183, AS393560, AS39836, AS43639, AS55409, AS55770, AS63949 |
| ArvanCloud | [www.arvancloud.ir/en/ips.txt](https://www.arvancloud.ir/en/ips.txt) |  |
| BelugaCDN | 45.32.205.194<br>45.32.171.136<br>207.148.103.72<br>45.32.139.246<br>155.138.163.55<br>136.244.96.178<br>149.28.228.141<br>95.179.211.233<br>149.248.35.160<br>155.138.145.126<br>45.32.79.109<br>45.76.135.107<br>139.180.212.85<br>141.164.34.103<br>149.28.189.219<br>149.28.118.26<br>104.207.131.132 |  |
| Bunny |  | AS200325 |
| CacheFly | [cachefly.cachefly.net/ips/cdn.txt](https://cachefly.cachefly.net/ips/cdn.txt) |  |
| CDN77 | [prefixlists.tools.cdn77.com/public_lmax_prefixes.json](https://prefixlists.tools.cdn77.com/public_lmax_prefixes.json) |  |
| CDNetworks |  | AS36408 |
| Cloudflare | [www.cloudflare.com/ips-v4/](https://www.cloudflare.com/ips-v4/)<br>[www.cloudflare.com/ips-v6/](https://www.cloudflare.com/ips-v6/) |  |
| CloudFront | [ip-ranges.amazonaws.com/ip-ranges.json](https://ip-ranges.amazonaws.com/ip-ranges.json) |  |
| DDoS-Guard |  | AS57724 |
| Derak Cloud | [api.derak.cloud/public/ipv4](https://api.derak.cloud/public/ipv4)<br>[api.derak.cloud/public/ipv6](https://api.derak.cloud/public/ipv6) |  |
| Edgecast |  | AS15133 |
| EdgeNext |  | AS139057, AS149981 |
| Edgio |  | AS60261 |
| F5 | [docs.cloud.f5.com/docs-v2/platform/reference/network-cloud-ref](https://docs.cloud.f5.com/docs-v2/platform/reference/network-cloud-ref) |  |
| Fastly | [api.fastly.com/public-ip-list](https://api.fastly.com/public-ip-list) |  |
| Gcore | [api.gcore.com/cdn/public-ip-list](https://api.gcore.com/cdn/public-ip-list) |  |
| Google Cloud | [www.gstatic.com/ipranges/cloud.json](https://www.gstatic.com/ipranges/cloud.json) |  |
| Imperva | [my.imperva.com/api/integration/v1/ips](https://my.imperva.com/api/integration/v1/ips) |  |
| IranServer | [ips.f95.com/ip.txt](https://ips.f95.com/ip.txt) |  |
| Leaseweb | [networksdb.io/ip-addresses-of/leaseweb-cdn-bv](https://networksdb.io/ip-addresses-of/leaseweb-cdn-bv) |  |
| Limelight |  | AS22822 |
| Medianova | [cloud.medianova.com/api/v1/ip/blocks-list](https://cloud.medianova.com/api/v1/ip/blocks-list) |  |
| Microsoft Azure | [www.microsoft.com/en-us/download/details.aspx?id=56519](https://www.microsoft.com/en-us/download/details.aspx?id=56519) |  |
| ParsPack | [parspack.com/cdnips.txt](https://parspack.com/cdnips.txt) |  |
| Qrator |  | AS200449 |
| StackPath |  | AS12989 |
| StormWall |  | AS59796 |
| Sucuri |  | AS30148 |
| X4B |  | AS136165 |
| Alibaba Cloud CDN |  |  |
| Azion |  |  |
| BaishanCloud |  |  |
| ChinaCache (QUANTIL) |  |  |
| Huawei Cloud CDN |  |  |
| KeyCDN |  |  |
| OVHcloud CDN |  |  |
| Tencent Cloud CDN |  |  |
| CDNsun |  |  |

## Contributing

Contributions are welcome. Please open a pull request to add or correct entries.

- Include provider name
- Provide direct official URL(s) for IPv4 and/or IPv6 lists (if any)
- Add ASN(s) if officially documented
- Add a short note for special cases (e.g., “no public list”, “paid API only”)
- If the source is not obviously official, include a reference link to docs

## Keywords

CDN IP ranges, CDN IPv4, CDN IPv6, CDN ASN, Cloudflare IPs, Akamai IPs, Fastly IPs, AWS CloudFront IPs, Google Cloud IP ranges, ArvanCloud IPs, Iran CDNs, public IP lists, allowlist, firewall, DDoS mitigation, network automation

 

 
