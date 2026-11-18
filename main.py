#!/usr/bin/env python3
"""Entry point for the news-image-20261118 bounty.

The finished image (entry.png, composed by compose.py from the six
panel illustrations) already sits next to this file. This program just
copies it, byte for byte, into the output directory the grader names
in MAKEFUN_OUTPUT_DIR (default /output), so both runs produce
identical bytes.
"""

import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    # Copy via a temp file so a partial write never lands at the target.
    tmp = dest + ".tmp"
    shutil.copyfile(SOURCE, tmp)
    os.replace(tmp, dest)
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
