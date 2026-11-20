#!/usr/bin/env python3
"""news-image-20261120 entry (Python 3.13, standard library only).

The entry image is entry.png beside this file: a newspaper-style front page
drawn programmatically (see draw.py) that sums up world news of Friday
20 November 2026. This program copies it to /output/entry.png (or
$MAKEFUN_OUTPUT_DIR/entry.png outside the grader), byte for byte, so both
graded runs write identical bytes.

Run it:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT, "entry.png")
shutil.copyfile(src, dst)
# Fail loudly rather than submit a truncated copy: the gate reads the
# whole PNG, so a short write must never pass silently.
if os.path.getsize(dst) != os.path.getsize(src):
    raise SystemExit("entry.png copy incomplete")
