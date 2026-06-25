#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path

PATTERNS = [
    ('port-conflict', r'EADDRINUSE|Address already in use|port .* already in use', 'Another process is already using the port.', 'Run the app on another port or identify the process before stopping it.'),
    ('missing-env', r'(Environment Variable|env var|process\.env\.[A-Z0-9_]+|KeyError: [\'\"][A-Z0-9_]+|Missing .*API.*key|not found in environment)', 'A required environment variable is missing.', 'Check `.env.example` and create the missing key in your local env file.'),
    ('missing-package', r"Module not found|Cannot find module|ModuleNotFoundError|No module named|Can't resolve", 'A dependency or import target is missing.', 'Install the missing package or fix the import path after confirming the package name.'),
    ('typescript', r'Type error:|TS\d{4}|TypeScript', 'TypeScript found a source contract problem.', 'Open the file and line shown in the log and fix the type mismatch first.'),
    ('syntax', r'SyntaxError|IndentationError|Unexpected token|Unexpected end of input', 'The source code cannot be parsed.', 'Fix the first syntax line shown in the log before trying other changes.'),
    ('permission', r'Permission denied|EACCES|Operation not permitted', 'The command does not have permission for a file or folder.', 'Check file permissions and avoid using sudo until the path is understood.'),
    ('version-mismatch', r'Unsupported engine|requires Node|node version|Python .* required|not compatible', 'The runtime version is incompatible.', 'Check the required Node or Python version and use a matching runtime.'),
]


def load_text(path):
    if path:
        return Path(path).read_text(errors='ignore')
    return sys.stdin.read()


def first_relevant_line(text, pattern):
    rx = re.compile(pattern, re.I)
    for line in text.splitlines():
        if rx.search(line):
            return line.strip()[:500]
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines[0][:500] if lines else ''


def classify(text):
    for category, pattern, explanation, action in PATTERNS:
        if re.search(pattern, text, re.I):
            return {
                'category': category,
                'root_cause_line': first_relevant_line(text, pattern),
                'beginner_explanation': explanation,
                'first_action': action,
                'verification': 'Run the same command again and confirm this error category no longer appears.'
            }
    return {
        'category': 'unknown',
        'root_cause_line': first_relevant_line(text, r'.+'),
        'beginner_explanation': 'The log does not match a known beginner error pattern yet.',
        'first_action': 'Share the full command you ran and the first 30 lines above the failure.',
        'verification': 'A clearer log should reveal a specific category.'
    }


def main():
    ap = argparse.ArgumentParser(description='Classify common beginner error logs.')
    ap.add_argument('logfile', nargs='?')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    data = classify(load_text(args.logfile))
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for k, v in data.items():
            print(f'{k}: {v}')

if __name__ == '__main__':
    main()
