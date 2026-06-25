# Render Deployment Checks

Check in this order:

1. Service type: Web Service for Flask/FastAPI apps.
2. Build command, for example `pip install -r requirements.txt`.
3. Start command, for example `gunicorn app:app` for Flask.
4. Python version and required system packages.
5. Environment variables in Render dashboard.
6. Port binding; app must listen on Render-provided `PORT` when required.

If local Flask uses `flask run`, explain that production normally needs Gunicorn.
