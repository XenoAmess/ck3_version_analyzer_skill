#!/usr/bin/env python3
"""Compatibility entrypoint; the repository-root script is the only implementation."""

from pathlib import Path
import runpy


implementation = Path(__file__).resolve().parents[3] / "ck3_analyzer.py"
if __name__ == "__main__":
    runpy.run_path(str(implementation), run_name="__main__")
else:
    globals().update({
        key: value for key, value in runpy.run_path(str(implementation)).items()
        if not key.startswith("_")
    })
