#!/usr/bin/env python
from __future__ import annotations

import argparse
import re
from pathlib import Path

SUSPICIOUS_PATTERNS = {
    # Known internal storage roots and concrete local paths. Generic /path/to examples are not flagged.
    "absolute_linux_data_path": re.compile(r"/data/local_|/mnt/pacs|/home/[^\s]+/PACS", re.I),
    "windows_drive_path": re.compile(r"[A-Z]:\\\\[^\s]+"),
    # Flag concrete private DICOM routing tokens rather than the generic word PACS.
    "dicom_private_tokens": re.compile(r"\b(AE_TITLE\s*=|AETITLE\s*=|DICOM_NODE\s*=|SeriesInstanceUID\s*=|StudyInstanceUID\s*=)\b", re.I),
    "ip_address": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    # Flag explicit patient-name fields; patient_id is allowed in templates but real values should be deidentified.
    "possible_patient_name": re.compile(r"\b(patient[_-]?name\s*=|PatientName\s*=|姓名[:：=])", re.I),
}

SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".zip", ".pth", ".nii", ".gz", ".dcm", ".pyc"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}
SKIP_FILES = {"13_redact_and_check_repo.py"}


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        if path.is_file() and not any(str(path).endswith(s) for s in SKIP_SUFFIXES):
            yield path


def main():
    p = argparse.ArgumentParser(description="Scan repository text files for potentially sensitive strings.")
    p.add_argument("--repo-root", default=".")
    args = p.parse_args()
    root = Path(args.repo_root)

    findings = []
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for name, pattern in SUSPICIOUS_PATTERNS.items():
            for m in pattern.finditer(text):
                findings.append((str(path), name, m.group(0)[:120]))

    if findings:
        print("Potential sensitive strings found:")
        for f in findings:
            print("  ", f)
        raise SystemExit(1)
    print("No obvious sensitive strings found in text files.")


if __name__ == "__main__":
    main()
