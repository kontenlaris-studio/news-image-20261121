#!/usr/bin/env python3
"""Entry point for the "Sum up 21 November's world news in one image"
entry (make.fun bounty news-image-20261121).

The artwork lives beside this file as artwork.png (drawn by
render_artwork.py). This program copies those exact bytes to
entry.png inside the output directory, so every run hands the judge
the identical image: no network, no clock, no randomness.

Locally, MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "artwork.png"


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


MAX_BYTES = 1_048_576  # the gate's 1 MiB cap for the judged image


def main() -> None:
    data = SOURCE.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("artwork.png is not a PNG")
    if len(data) > MAX_BYTES:
        raise SystemExit("artwork.png exceeds the 1 MiB gate cap")
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "entry.png").write_bytes(data)


if __name__ == "__main__":
    main()
