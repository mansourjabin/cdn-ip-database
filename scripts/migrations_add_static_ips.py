import json
from pathlib import Path

SOURCES_PATH = Path('cdn-ip-database/sources.json')

def main():
    data = json.loads(SOURCES_PATH.read_text(encoding='utf-8'))
    changed = False
    for entry in data:
        if 'static_ips' not in entry:
            entry['static_ips'] = []
            changed = True
        # Ensure expected keys exist
        if 'urls' not in entry:
            entry['urls'] = []
            changed = True
        if 'asns' not in entry:
            entry['asns'] = []
            changed = True
    if changed:
        SOURCES_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False), encoding='utf-8')
        print('sources.json updated: static_ips ensured for all providers')
    else:
        print('No changes needed')

if __name__ == '__main__':
    main()
