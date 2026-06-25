#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

SECRET_PATTERNS = [
    ('openai', re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b')),
    ('anthropic', re.compile(r'\bsk-ant-[A-Za-z0-9_-]{20,}\b')),
    ('generic_assignment', re.compile(r'(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*[\"\']?([A-Za-z0-9_./+=-]{16,})')),
]
SKIP_DIRS = {'.git', 'node_modules', '.next', 'dist', 'build', 'coverage', 'test-results', 'playwright-report', '__pycache__'}
TEXT_EXTS = {'.js','.jsx','.ts','.tsx','.py','.env','.local','.json','.md','.txt','.toml','.yaml','.yml','.html','.css','.mjs','.cjs'}


def mask(value):
    if not value:
        return '[REDACTED]'
    if len(value) <= 8:
        return '[REDACTED]'
    return value[:4] + '...' + value[-4:]


def should_scan(path):
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.name.startswith('.env'):
        return True
    return path.suffix in TEXT_EXTS


def scan(root):
    root = Path(root)
    findings = []
    gitignore = root / '.gitignore'
    gitignore_text = gitignore.read_text(errors='ignore') if gitignore.exists() else ''
    env_files = [p for p in root.glob('.env*') if p.is_file() and p.name != '.env.example']
    if env_files and '.env' not in gitignore_text:
        findings.append({'severity':'high','type':'env-not-ignored','file':'.gitignore','line':0,'match':'[policy]','message':'Env files exist but .gitignore does not clearly ignore .env files.'})
    for path in root.rglob('*'):
        if not path.is_file() or not should_scan(path):
            continue
        try:
            text = path.read_text(errors='ignore')
        except Exception:
            continue
        rel = str(path.relative_to(root))
        for idx, line in enumerate(text.splitlines(), 1):
            for kind, rx in SECRET_PATTERNS:
                for m in rx.finditer(line):
                    raw = m.group(2) if kind == 'generic_assignment' and m.lastindex else m.group(0)
                    severity = 'high'
                    if 'example' in rel.lower() or 'sample' in line.lower() or 'your_' in line.lower():
                        severity = 'low'
                    client_risk = any(part in rel for part in ['components/', 'public/', 'static/', 'src/app/']) or 'NEXT_PUBLIC_' in line
                    findings.append({'severity':severity,'type':kind,'file':rel,'line':idx,'match':mask(raw),'client_risk':client_risk,'message':'Possible secret-like value found; full value is masked.'})
    return {'root': str(root), 'finding_count': len(findings), 'findings': findings}


def main():
    ap = argparse.ArgumentParser(description='Scan a project for likely API key exposure without printing full secrets.')
    ap.add_argument('--path', default='.')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    data = scan(args.path)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"findings: {data['finding_count']}")
        for f in data['findings']:
            print(f"{f['severity']} {f['file']}:{f['line']} {f['type']} {f['match']}")

if __name__ == '__main__':
    main()
