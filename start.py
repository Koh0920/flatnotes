"""Entrypoint for the flatnotes ato capsule.

Adds the uv-managed venv site-packages to sys.path, then launches the
flatnotes FastAPI app via uvicorn.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Force CWD to the capsule source dir so flatnotes' relative-path checks
# (e.g. `os.path.exists(FLATNOTES_PATH)`) resolve consistently regardless
# of how ato launches us.
os.chdir(HERE)

VENV_SITE_PACKAGES = HERE / ".venv" / "lib" / "python3.11" / "site-packages"
if VENV_SITE_PACKAGES.exists() and str(VENV_SITE_PACKAGES) not in sys.path:
    sys.path.insert(0, str(VENV_SITE_PACKAGES))


def main() -> None:
    # flatnotes refuses to start if FLATNOTES_PATH does not already exist.
    data_dir = HERE / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    # Pin FLATNOTES_PATH to an absolute path so flatnotes' internal
    # `os.path.exists(self.storage_path)` check passes even if our
    # process CWD ends up somewhere else than `source/`.
    os.environ["FLATNOTES_PATH"] = str(data_dir)

    # flatnotes' FastAPI app lives under server/main.py
    server_dir = HERE / "server"
    if str(server_dir) not in sys.path:
        sys.path.insert(0, str(server_dir))

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8082,
        access_log=False,
    )


if __name__ == "__main__":
    main()
