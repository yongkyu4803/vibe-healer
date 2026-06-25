#!/usr/bin/env python3
import argparse, json, subprocess
from pathlib import Path

SUSPICIOUS = ('.env', 'secret', 'token', 'key', 'credential')
GENERATED = ('node_modules/', '.next/', 'dist/', 'build/', 'coverage/', 'test-results/', 'playwright-report/', '__pycache__/')


def run(cmd, cwd):
    try:
        p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except FileNotFoundError:
        return 127, '', 'command not found'


def summarize(path):
    root = Path(path)
    code, out, err = run(['git','rev-parse','--is-inside-work-tree'], root)
    if code != 0 or out.strip() != 'true':
        return {'is_git_repo': False, 'root': str(root), 'clean': None, 'files': [], 'warnings': ['Not a Git repository']}
    _, branch, _ = run(['git','branch','--show-current'], root)
    _, status, _ = run(['git','status','--short'], root)
    files = []
    warnings = []
    for line in status.splitlines():
        if not line:
            continue
        state = line[:2]
        name = line[3:].strip()
        entry = {'state': state, 'path': name, 'category': 'normal'}
        lower = name.lower()
        if any(s in lower for s in SUSPICIOUS):
            entry['category'] = 'suspicious-secret'
            warnings.append(f'Check possible secret before committing: {name}')
        elif any(lower.startswith(g) or f'/{g}' in lower for g in GENERATED):
            entry['category'] = 'generated-artifact'
            warnings.append(f'Usually do not commit generated artifact: {name}')
        files.append(entry)
    return {'is_git_repo': True, 'root': str(root), 'branch': branch or None, 'clean': not bool(files), 'files': files, 'warnings': warnings}


def main():
    ap = argparse.ArgumentParser(description='Summarize Git state for safe beginner savepoints.')
    ap.add_argument('--path', default='.')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    data = summarize(args.path)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"git_repo: {data['is_git_repo']}")
        print(f"clean: {data['clean']}")
        for f in data.get('files', []):
            print(f"{f['state']} {f['category']} {f['path']}")
        for w in data.get('warnings', []):
            print(f"warning: {w}")

if __name__ == '__main__':
    main()
