# Project Type Signals

Use multiple signals before deciding.

- Next.js: `package.json` has `next`, `app/`, `pages/`, or scripts like `next dev`.
- Vite/React: `package.json` has `vite`, `src/main.jsx`, `src/main.tsx`, or `index.html` plus Vite scripts.
- Streamlit: `streamlit_app.py`, `app.py` importing `streamlit`, or `requirements.txt` containing `streamlit`.
- Flask: `app.py` importing `flask`, `requirements.txt` containing `Flask`, or `wsgi.py`.
- Generic Python: `.py` files plus requirements or pyproject, no web framework signal.
- Static HTML: `index.html` with no package or Python dependency files.

When mixed signals exist, prefer the explicit script in README or `package.json`.
