#!/usr/bin/env python3
import json, subprocess, tempfile, os, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
  'local-run-doctor': {'scripts':['detect_project.py'], 'refs':['project-types.md','local-run-troubleshooting.md']},
  'error-doctor': {'scripts':['classify_error.py'], 'refs':['error-patterns-node.md','error-patterns-python.md','error-response-template.md']},
  'deploy-fixer': {'scripts':[], 'refs':['deploy-vercel.md','deploy-render.md','deploy-streamlit.md','deploy-log-patterns.md']},
  'api-key-guardian': {'scripts':['secret_scan.py'], 'refs':['api-key-safety.md','env-file-patterns.md','client-server-boundary.md']},
  'git-savepoint': {'scripts':['git_status_summary.py'], 'refs':['git-savepoint-policy.md','gitignore-common.md']},
  'ui-screenshot-reviewer': {'scripts':[], 'refs':['ui-review-rubric.md','responsive-checklist.md','screenshot-report-template.md']},
}


def fail(msg):
    print(f'FAIL: {msg}')
    sys.exit(1)


def run(cmd, cwd=None, input_text=None):
    p = subprocess.run(cmd, cwd=cwd, input=input_text, text=True, capture_output=True, check=False)
    if p.returncode != 0:
        fail(f"command failed: {' '.join(map(str, cmd))}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return p.stdout


def validate_structure():
    manifest = ROOT / '.codex-plugin' / 'plugin.json'
    if not manifest.exists():
        fail('missing .codex-plugin/plugin.json')
    data = json.loads(manifest.read_text())
    if data.get('name') != 'vibe-healer':
        fail('plugin name must be vibe-healer')
    if data.get('skills') != './skills/':
        fail('plugin skills path must be ./skills/')
    for skill, req in REQUIRED.items():
        base = ROOT / 'skills' / skill
        smd = base / 'SKILL.md'
        if not smd.exists():
            fail(f'missing {skill}/SKILL.md')
        text = smd.read_text()
        bad_markers = ['[' + 'TO' + 'DO', 'TO' + 'DO:']
        if any(marker in text for marker in bad_markers):
            fail(f'placeholder remains in {skill}/SKILL.md')
        if not text.startswith('---'):
            fail(f'{skill}/SKILL.md missing frontmatter')
        m = re.search(r'^name:\s*(\S+)', text, re.M)
        if not m or m.group(1) != skill:
            fail(f'{skill}/SKILL.md name mismatch')
        if not re.search(r'^description:\s*.+', text, re.M):
            fail(f'{skill}/SKILL.md missing description')
        if not (base / 'agents' / 'openai.yaml').exists():
            fail(f'missing agents/openai.yaml for {skill}')
        for ref in req['refs']:
            if not (base / 'references' / ref).exists():
                fail(f'missing reference {skill}/{ref}')
        for script in req['scripts']:
            if not (base / 'scripts' / script).exists():
                fail(f'missing script {skill}/{script}')


def validate_scripts():
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        next_app = t / 'next-app'
        next_app.mkdir()
        (next_app / 'package.json').write_text('{"scripts":{"dev":"next dev"},"dependencies":{"next":"16.0.0"}}')
        out = run([sys.executable, str(ROOT/'skills/local-run-doctor/scripts/detect_project.py'), '--path', str(next_app), '--json'])
        if json.loads(out)['project_type'] != 'nextjs':
            fail('detect_project did not detect nextjs')

        flask = t / 'flask-app'
        flask.mkdir()
        (flask / 'app.py').write_text('from flask import Flask\napp = Flask(__name__)\n')
        (flask / 'requirements.txt').write_text('Flask\n')
        out = run([sys.executable, str(ROOT/'skills/local-run-doctor/scripts/detect_project.py'), '--path', str(flask), '--json'])
        if json.loads(out)['project_type'] != 'flask':
            fail('detect_project did not detect flask')

        log = 'Error: listen EADDRINUSE: address already in use :::3000\n'
        out = run([sys.executable, str(ROOT/'skills/error-doctor/scripts/classify_error.py'), '--json'], input_text=log)
        if json.loads(out)['category'] != 'port-conflict':
            fail('classify_error did not classify port conflict')

        secret_project = t / 'secret-project'
        secret_project.mkdir()
        fake_key = 'sk-' + 'proj-' + 'abcdefghijklmnopqrstuvwxyz123456'
        (secret_project / '.env').write_text('OPENAI_API_KEY=' + fake_key + '\n')
        (secret_project / '.gitignore').write_text('node_modules/\n')
        out = run([sys.executable, str(ROOT/'skills/api-key-guardian/scripts/secret_scan.py'), '--path', str(secret_project), '--json'])
        data = json.loads(out)
        if data['finding_count'] < 1:
            fail('secret_scan did not find fake key')
        if fake_key in out:
            fail('secret_scan printed full secret')

        out = run([sys.executable, str(ROOT/'skills/git-savepoint/scripts/git_status_summary.py'), '--path', str(t), '--json'])
        if json.loads(out)['is_git_repo'] is not False:
            fail('git_status_summary should handle non-git folder')


def main():
    validate_structure()
    validate_scripts()
    print('Vibe Healer validation passed')

if __name__ == '__main__':
    main()
