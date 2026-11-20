#!/usr/bin/env python3
"""Entrypoint for the news-image-20261120 make.fun submission.

Copies the pre-rendered poster (entry.png, produced by generate.py) to the
output location the harness requests via MAKEFUN_OUTPUT_DIR, defaulting to
/output/entry.png. Standard library only; the copy is byte-for-byte, so
repeated runs always produce identical output.
"""

import os
import shutil
import sys
from pathlib import Path


def main() -> int:
    source = Path(__file__).resolve().with_name("entry.png")
    dest_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    dest = dest_dir / "entry.png"

    if not source.is_file():
        print(f"missing poster next to entrypoint: {source}", file=sys.stderr)
        return 1

    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    print(f"copied {source} -> {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
