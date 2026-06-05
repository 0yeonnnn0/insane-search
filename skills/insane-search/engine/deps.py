"""Small dependency bootstrap helpers for the insane-search engine.

The original skill promises zero-config first use. Keep that promise in a
contained helper instead of scattering ad-hoc pip calls through the engine.

Set INSANE_SEARCH_NO_AUTO_INSTALL=1 to disable runtime installs.
"""
from __future__ import annotations

import importlib
import os
import subprocess
import sys
from typing import Optional


def import_or_install(module: str, package: Optional[str] = None):
    """Import `module`, optionally installing `package` first if missing.

    Returns the imported module, or raises the original/final ImportError when
    auto-install is disabled or pip installation fails.
    """
    try:
        return importlib.import_module(module)
    except ImportError as first_error:
        if os.environ.get("INSANE_SEARCH_NO_AUTO_INSTALL") in {"1", "true", "TRUE", "yes"}:
            raise first_error

        pkg = package or module
        attempts = [
            [sys.executable, "-m", "pip", "install", "--user", "-q", pkg],
            # Debian/Raspberry Pi OS may enforce PEP 668 even for --user installs.
            # This mirrors the original skill's documented zero-config behavior;
            # users can disable it with INSANE_SEARCH_NO_AUTO_INSTALL=1.
            [sys.executable, "-m", "pip", "install", "--user", "--break-system-packages", "-q", pkg],
        ]
        last_error: Exception | None = None
        for cmd in attempts:
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                break
            except Exception as install_error:
                last_error = install_error
        else:
            raise ImportError(f"{module} not installed and auto-install failed: {last_error}") from first_error

        return importlib.import_module(module)
