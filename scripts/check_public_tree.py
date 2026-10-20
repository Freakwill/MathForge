"""Check static distribution scope. Runtime reports/venvs and fresh VCS metadata are excluded."""
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
IGNORE={'reports','.git','__pycache__','build','dist','.venv'}
patterns={
 'private_key':rb'-----BEGIN (?:OPENSSH |RSA |EC |DSA )?PRIVATE KEY-----',
 'provider_token':rb'(?:sk-proj-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})',
 'personal_windows_path':rb'(?i)[A-Z]:[/\\]Users[/\\][A-Za-z0-9_.-]+',
 'personal_unix_path':rb'/(?:home|Users)/[A-Za-z0-9_.-]+/',
}
files=[];findings=[]
if (ROOT/'.git').exists():
    names=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode('utf-8').split('\0')
    files=[ROOT/p for p in names if p]
else:
    files=[p for p in ROOT.rglob('*') if p.is_file() and not set(p.relative_to(ROOT).parts)&IGNORE and not any(x.endswith('.egg-info') for x in p.parts)]
for p in files:
    rel=p.relative_to(ROOT).as_posix()
    if p.suffix in {'.pdf','.sqlite3','.olean','.dll','.exe','.pyd'} or any(x in rel.split('/') for x in ['private_audit','node_modules','MathForge_Manuscripts']):findings.append((rel,'forbidden distribution asset'))
    if p.name.startswith('.env') or p.name in ['id_rsa','id_ed25519']:findings.append((rel,'credential-like filename'))
    raw=p.read_bytes()
    for name,pattern in patterns.items():
        if re.search(pattern,raw):findings.append((rel,name))
if findings:
    for p,kind in findings:print(p,kind)
    raise SystemExit(1)
print('PASS: static candidate scope,',len(files),'files; no high-confidence secret/path signatures')
