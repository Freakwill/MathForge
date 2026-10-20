"""New synthetic demonstration workspaces; never copies an existing research atlas."""
from pathlib import Path
import json

ASSETS = Path(__file__).with_name('assets')

def initialize(path):
    root = Path(path).resolve()
    root.mkdir(parents=True, exist_ok=False)
    seed = json.loads((ASSETS / 'synthetic_seed.json').read_text(encoding='utf-8'))
    for rel, value in seed.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('x', encoding='utf-8', newline='\n') as f:
            if rel.endswith('.jsonl'):
                for row in value: f.write(json.dumps(row, ensure_ascii=False) + '\n')
            else: json.dump(value, f, indent=2)
    for p in (ASSETS / 'schemas').glob('*.json'):
        target = root / 'schemas' / p.name
        target.parent.mkdir(exist_ok=True)
        with target.open('xb') as f: f.write(p.read_bytes())
    return root
