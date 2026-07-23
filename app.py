[     UTC     ] Logs for kraivin-dashboard-cpmnvlfyd78y4kyfgryypb.streamlit.app/

────────────────────────────────────────────────────────────────────────────────────────

[08:37:31] 🚀 Starting up repository: 'kraivin-dashboard', branch: 'main', main module: 'app.py'

[08:37:31] 🐙 Cloning repository...

[08:37:32] 🐙 Cloning into '/mount/src/kraivin-dashboard'...

[08:37:32] 🐙 Cloned repository!

[08:37:32] 🐙 Pulling code changes from Github...

[08:37:32] 📦 Processing dependencies...


──────────────────────────────────────── uv ───────────────────────────────────────────


Using uv pip install.

Using Python 3.14.6 environment at /home/adminuser/venv

Resolved 7 packages in 192ms

Prepared 7 packages in 759ms

Installed 7 packages in 83ms

 + [2026-07-23 08:37:33.917156] narwhals==2.24.0

 + numpy==2.5.1

 + packaging==26.2

 + pandas==3.0.5

 + plotly==6.9.0

 + python-dateutil==2.9.0.post0

 + six==1.17.0

Checking if Streamlit is installed

Installing rich for an improved exception logging

Using uv pip install.

Using Python 3.14.6 environment at /home/adminuser/venv

Resolved 4 packages in 116ms

Prepared 4 packages in 101ms

Installed 4 packages in 13ms

 + markdown-it-py==4.2.0

 + mdurl==0.1.2[2026-07-23 08:37:34.630836] 

 + pygments==2.20.0

 + rich==15.0.0


────────────────────────────────────────────────────────────────────────────────────────


[08:37:35] 🐍 Python dependencies were installed from /mount/src/kraivin-dashboard/requirements.txt using uv.

Check if streamlit is installed


──────────────────────────────── Installing Streamlit ──────────────────────────────────


Using uv pip install.

Using Python 3.14.6 environment at /home/adminuser/venv

Resolved 41 packages in 365ms

Prepared 35 packages in 1.05s

Installed 35 packages in 48ms

 + altair==6.2.2

 + anyio==4.14.2

 + attrs==26.1.0

 + blinker==1.9.0

 + certifi==2026.7.22

 + charset-normalizer==3.4.9

 + click==8.4.2

 + gitdb==4.0.12

 + gitpython==3.1.55

 + h11[2026-07-23 08:37:36.650370] ==0.16.0

 + httptools==0.8.0

 + idna==3.18

 + itsdangerous==2.2.0

 + jinja2==3.1.6

 + jsonschema==4.26.0

 + [2026-07-23 08:37:36.651154] jsonschema-specifications==2025.9.1

 + markupsafe==3.0.3

 + pillow==12.3.0

 + protobuf==7.35.1

 + pyarrow==24.0.0

 + pydeck==0.9.3

 + python-multipart==0.0.32

 + referencing==0.37.0

 + requests==2.34.2

 + rpds-py==2026.6.3

 + smmap==5.0.3

 + starlette==1.3.1

 + streamlit==1.60.0

 + tenacity==9.1.4

 + toml==0.10.2

 + typing-extensions==4.16.0

 + urllib3==2.7.0

 + uvicorn==0.51.0

 + watchdog==6.0.0

 + websockets==16.1.1


────────────────────────────────────────────────────────────────────────────────────────


[08:37:37] 📦 Processed dependencies!

2026-07-23 08:37:39.969 Uvicorn server started on :::8501




2026-07-23 08:37:44.930 Script compilation error

Traceback (most recent call last):

  File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 659, in _run_script

    code = self._script_cache.get_bytecode(script_path)

  File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/scriptrunner/script_cache.py", line 72, in get_bytecode

    filebody = magic.add_magic(filebody, script_path)

  File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/scriptrunner/magic.py", line 45, in add_magic

    tree = ast.parse(code, script_path, "exec")

  File "/usr/local/lib/python3.14/ast.py", line 46, in parse

    return compile(source, filename, mode, flags,

                   _feature_version=feature_version, optimize=optimize)

  File "/mount/src/kraivin-dashboard/app.py", line 2

    """

    ^

SyntaxError: unterminated triple-quoted string literal (detected at line 5)

2026-07-23 08:37:44.946 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.

2026-07-23 08:38:21.492 Script compilation error

Traceback (most recent call last):

  File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 659, in _run_script

    code = self._script_cache.get_bytecode(script_path)

  File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/scriptrunner/script_cache.py", line 72, in get_bytecode

    filebody = magic.add_magic(filebody, script_path)

  File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/scriptrunner/magic.py", line 45, in add_magic

    tree = ast.parse(code, script_path, "exec")

  File "/usr/local/lib/python3.14/ast.py", line 46, in parse

    return compile(source, filename, mode, flags,

                   _feature_version=feature_version, optimize=optimize)

  File "/mount/src/kraivin-dashboard/app.py", line 2

    """

    ^

SyntaxError: unterminated triple-quoted string literal (detected at line 5)

2026-07-23 08:38:21.494 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.

[08:39:03] 🐙 Pulling code changes from Github...

[08:39:04] 📦 Processing dependencies...

[08:39:04] 📦 Processed dependencies!

[08:39:06] 🔄 Updated app!
