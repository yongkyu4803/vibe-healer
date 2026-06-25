# Local Run Troubleshooting

Common beginner blockers:

- Missing dependencies: install only after identifying the package manager.
- Port in use: suggest a different port or identify the process; do not kill processes without confirmation.
- Missing env vars: ask the user to create `.env.local` from `.env.example`; do not invent real keys.
- Wrong folder: confirm the command is run from the project root.
- Python venv missing: suggest creating or activating a venv before installing packages.

Verification examples:

- Next.js: browser opens at `http://localhost:3000` or selected port.
- Streamlit: browser opens at `http://localhost:8501`.
- Flask: terminal shows serving URL and a browser request returns 200.
