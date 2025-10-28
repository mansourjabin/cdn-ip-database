import json

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
        
    start_marker = "## Provider List"
    # Find the next section to mark the end of the provider list section
    end_marker = "\n## "
    
    start_index = content.find(start_marker)
    if start_index == -1:
        print("Provider list section not found in README.")
        return
    
    # Search for the end marker after the start marker
    end_index = content.find(end_marker, start_index + len(start_marker))
    
    # Construct the new content
    # Part before the provider list
    before_section = content[:start_index]
    
    # The new provider list section
    provider_section = start_marker + "\n\n" + table + "\n"

    # Part after the provider list (if it exists)
    after_section = ""
    if end_index != -1:
        after_section = content[end_index:]
    
    new_content = before_section + provider_section + after_section

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
