import json

BEGIN_MARKER = "<!-- BEGIN PROVIDER_TABLE -->"
END_MARKER = "<!-- END PROVIDER_TABLE -->"


def generate_table(providers):
    table = "| Provider | IP Source(s) | ASN |\n"
    table += "|----------|--------------|-----|\n"
    for p in providers:
        provider = p.get('provider', '')
        urls = p.get('urls', [])
        asns = p.get('asns', [])
        static_ips = p.get('static_ips', [])
        
        source_info = []
        if urls:
            source_info.extend([f'[{url.split("//")[-1]}]({url})' for url in urls])
        if static_ips:
            source_info.extend(static_ips)
            
        source_text = '<br>'.join(source_info)
        asn_list = ', '.join(asns)
        
        table += f"| {provider} | {source_text} | {asn_list} |\n"
    return table


def update_readme(sources_path, readme_path):
    with open(sources_path, 'r', encoding='utf-8') as f:
        providers = json.load(f)
    
    table = generate_table(providers)
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

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
