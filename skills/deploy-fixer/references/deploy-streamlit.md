# Streamlit Community Cloud Checks

Check in this order:

1. Main file path, often `streamlit_app.py`.
2. `requirements.txt` includes every import.
3. Secrets are configured in Streamlit secrets, not committed to Git.
4. Python version compatibility.
5. App logs for package install errors.

For secrets, suggest `.streamlit/secrets.toml` locally but do not commit real values.
