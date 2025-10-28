import json
import sys
from jsonschema import validate, Draft202012Validator

SCHEMA_PATH = 'schema/sources.schema.json'
SOURCES_PATH_CANDIDATES = [
    'data/sources.json',
    'sources.json',
]

def load_sources_path() -> str:
    for p in SOURCES_PATH_CANDIDATES:
        try:
            with open(p, 'r', encoding='utf-8'):
                return p
        except FileNotFoundError:
            continue
    raise FileNotFoundError('sources.json not found in expected locations')


def main() -> int:
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    sources_path = load_sources_path()
    with open(sources_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    Draft202012Validator.check_schema(schema)
    validate(instance=data, schema=schema)
    print(f"Validation OK: {sources_path}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
