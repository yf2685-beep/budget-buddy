# Recreate Budget Buddy workflow

Captured from the actual Flask UI using fictional spending records and an isolated in-memory MongoDB substitute. The recorded expense changes the displayed total from 365.00 to 377.50; no personal or team financial data is used.

Run from the repository root in a separate Python 3.11+ environment:

~~~bash
python -m venv .venv-demo
source .venv-demo/bin/activate
python -m pip install -r scripts/demo-requirements.txt
python -m playwright install chromium
python scripts/capture_demo.py
~~~

Output: docs/media/budget-workflow.gif. On Windows, activate with .venv-demo/Scripts/activate.

The capture script starts a temporary local server on an available loopback port, seeds fictional records, exercises the real routes/UI, and shuts down afterwards. The database is mongomock, not a running MongoDB server. Environment-file loading is disabled, and database settings are overridden for the capture process. Do not run this by importing it into a production process.

The GIF adds a title, step captions and click highlights around real screenshots. Typing is shown in sampled steps and waits are shortened or held for readability. The original application templates and business logic are used without visual replacements. Its public CDN scripts may need network access. The --browser option selects a browser executable explicitly.

Team/source attribution remains in the main README and original project files. The demo adds presentation assets, not new product functionality.
