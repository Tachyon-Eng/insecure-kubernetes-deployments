# Code Review Service

A Flask application that accepts pasted source code or ZIP archives and sends the contents to the configured analysis provider.

## Run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` and submit either text or a ZIP archive for review.
