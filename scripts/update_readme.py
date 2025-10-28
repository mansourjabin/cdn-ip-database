import json
import os
import re
from datetime import datetime, timezone

BEGIN_MARKER = "<!-- BEGIN PROVIDER_TABLE -->"
END_MARKER = "<!-- END PROVIDER_TABLE -->"
LAST_BEGIN = "<!-- BEGIN_LAST_UPDATED -->"
LAST_END = "<!-- END_LAST_UPDATED -->"


def generate_table(providers):
    table = "| Provider | IP Source(s) | ASN | Note |\n"
    table += "|----------|--------------|-----|------|\n"
    for p in providers:
        provider = p.get('provider', '')
        urls = p.get('urls', [])
        asns = p.get('asns', [])
        static_ips = p.get('static_ips', [])
        note = p.get('note', '')
        
        source_info = []
        if urls:
            source_info.extend([f'[{url.split("//")[-1]}]({url})' for url in urls])
        if static_ips:
            source_info.extend(static_ips)
            
        source_text = '<br>'.join(source_info)
        asn_list = ', '.join(asns)
        
        table += f"| {provider} | {source_text} | {asn_list} | {note} |\n"
    return table


def update_readme(sources_path, readme_path):
    with open(sources_path, 'r', encoding='utf-8') as f:
        providers = json.load(f)
    
    table = generate_table(providers)
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Compute last updated timestamp (prefer resolved_ips.json mtime, fallback to now)
    last_updated = None
    mtime_candidates = [
        'data/resolved_ips.json',
        'resolved_ips.json',
    ]
    for path in mtime_candidates:
        if os.path.exists(path):
            try:
                ts = os.path.getmtime(path)
                last_updated = datetime.fromtimestamp(ts, tz=timezone.utc)
                break
            except OSError:
                continue
    if last_updated is None:
        last_updated = datetime.now(tz=timezone.utc)
    last_updated_str = last_updated.strftime('%Y-%m-%d %H:%M UTC')

    # Replace ALL instances of last updated markers across README
    pattern = re.compile(r"<!--\s*BEGIN_LAST_UPDATED\s*-->.*?<!--\s*END_LAST_UPDATED\s*-->", re.DOTALL)
    content = re.sub(pattern, f"{LAST_BEGIN}{last_updated_str}{LAST_END}", content)

    # Prefer marker-based replacement
    if BEGIN_MARKER in content and END_MARKER in content:
        start = content.index(BEGIN_MARKER) + len(BEGIN_MARKER)
        end = content.index(END_MARKER, start)
        new_content = content[:start] + "\n\n" + table + "\n\n" + content[end:]
    else:
        # Fallback: find Provider List section and wrap table with markers
        start_marker = "## Provider List"
        end_marker = "\n## "
        start_index = content.find(start_marker)
        if start_index == -1:
            print("Provider list section not found in README.")
            return
        # Search for the end marker after the start marker
        after = content.find(end_marker, start_index + len(start_marker))
        before_section = content[:start_index]
        header = start_marker + "\n\n" + BEGIN_MARKER
        body = "\n\n" + table + "\n\n" + END_MARKER + "\n"
        after_section = content[after:] if after != -1 else ""
        new_content = before_section + header + body + after_section

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


if __name__ == "__main__":
    # Prefer data/ then fallback to root
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

    readme_file = 'README.md'
    update_readme(sources_file, readme_file)
