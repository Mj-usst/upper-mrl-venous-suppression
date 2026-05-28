#!/usr/bin/env python
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Create a clean source archive for release.")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--output", default="LympClear_source_release.zip")
    return p.parse_args()


def main():
    args = parse_args()
    repo = Path(args.repo_root).resolve()
    output = Path(args.output).resolve()
    if output.exists():
        output.unlink()
    shutil.make_archive(str(output.with_suffix("")), "zip", repo)
    print(f"Created {output}")


if __name__ == "__main__":
    main()
