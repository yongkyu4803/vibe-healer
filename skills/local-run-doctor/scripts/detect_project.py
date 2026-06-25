#!/usr/bin/env python3
import argparse, json
from pathlib import Path


def read_text(path):
    try:
        return path.read_text(errors='ignore')
    except Exception:
        return ''


def detect(root):
    root = Path(root)
    indicators = []
    commands = []
    warnings = []
    pjson = root / 'package.json'
    req = root / 'requirements.txt'
    pyproject = root / 'pyproject.toml'
    index_html = root / 'index.html'

    if pjson.exists():
        indicators.append('package.json')
        try:
            data = json.loads(read_text(pjson))
        except Exception:
            data = {}
            warnings.append('package.json could not be parsed')
        deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
        scripts = data.get('scripts', {})
        if 'next' in deps or any('next' in str(v) for v in scripts.values()):
            commands.append('npm run dev')
            return result('nextjs', 0.92, indicators + ['next dependency or script'], commands, warnings)
        if 'vite' in deps or any('vite' in str(v) for v in scripts.values()):
            commands.append('npm run dev')
            return result('vite', 0.88, indicators + ['vite dependency or script'], commands, warnings)
        if scripts.get('dev'):
            commands.append('npm run dev')
            return result('node-app', 0.70, indicators + ['dev script'], commands, warnings)

    req_text = read_text(req).lower() if req.exists() else ''
    py_text = read_text(pyproject).lower() if pyproject.exists() else ''
    app_py = root / 'app.py'
    streamlit_py = root / 'streamlit_app.py'
    if streamlit_py.exists() or 'streamlit' in req_text or 'streamlit' in py_text:
        indicators.append('streamlit signal')
        entry = 'streamlit_app.py' if streamlit_py.exists() else 'app.py'
        commands.append(f'streamlit run {entry}')
        return result('streamlit', 0.88, indicators, commands, warnings)
    if app_py.exists() and ('flask' in read_text(app_py).lower() or 'flask' in req_text or 'flask' in py_text):
        indicators.append('flask signal')
        commands.extend(['python app.py', 'flask --app app run'])
        return result('flask', 0.84, indicators, commands, warnings)
    if req.exists() or pyproject.exists() or list(root.glob('*.py')):
        indicators.append('python files or dependency file')
        commands.append('python main.py')
        warnings.append('No specific web framework detected')
        return result('python', 0.55, indicators, commands, warnings)
    if index_html.exists():
        indicators.append('index.html')
        commands.append('open index.html or run a static server')
        return result('static-html', 0.70, indicators, commands, warnings)
    return result('unknown', 0.10, indicators, commands, ['No known project files found'])


def result(kind, confidence, indicators, commands, warnings):
    return {'project_type': kind, 'confidence': confidence, 'indicators': indicators, 'suggested_commands': commands, 'warnings': warnings}


def main():
    ap = argparse.ArgumentParser(description='Detect beginner project type and local run command.')
    ap.add_argument('--path', default='.')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    data = detect(args.path)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"project_type: {data['project_type']}")
        print(f"confidence: {data['confidence']}")
        for cmd in data['suggested_commands']:
            print(f"command: {cmd}")
        for warning in data['warnings']:
            print(f"warning: {warning}")

if __name__ == '__main__':
    main()
