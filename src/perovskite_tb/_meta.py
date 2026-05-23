"""Reproducibility metadata for computed results.

Every result file carries the git commit, timestamp, package version and the
exact numeric inputs, per the project's data-management policy
(docs/data-management.md): "results must always carry execution metadata".
"""

from __future__ import annotations

import datetime as _dt
import platform
import subprocess
from typing import Any


def _git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=5
        )
        if out.returncode == 0:
            commit = out.stdout.strip()
            dirty = subprocess.run(
                ["git", "status", "--porcelain"], capture_output=True, text=True, timeout=5
            ).stdout.strip()
            return commit + ("-dirty" if dirty else "")
    except Exception:
        pass
    return "unknown"


def run_metadata(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a dict of reproducibility metadata."""
    import numpy

    from . import __version__

    try:  # scipy is a declared dependency but not functionally required.
        import scipy
        scipy_ver = scipy.__version__
    except ImportError:
        scipy_ver = "not installed"

    meta = {
        "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "git_commit": _git_commit(),
        "package_version": __version__,
        "python": platform.python_version(),
        "numpy": numpy.__version__,
        "scipy": scipy_ver,
        "platform": platform.platform(),
    }
    if extra:
        meta.update(extra)
    return meta
