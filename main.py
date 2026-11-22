#!/usr/bin/env python3
"""THE WORLD TODAY — Saturday 21 November 2026.

Entry program: copies the pre-rendered front page (entry.png, drawn by
render.py from verified 21 November 2026 reporting) to
$MAKEFUN_OUTPUT_DIR/entry.png. Deterministic: the same bytes every run.
"""
import os
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent


def main():
    outdir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    outdir.mkdir(parents=True, exist_ok=True)
    src = BASE / "entry.png"
    dst = outdir / "entry.png"
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
