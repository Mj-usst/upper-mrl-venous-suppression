#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path

import yaml

DEFAULT_ITEMS = {
    "lower": {
        "dataset_id": 25,
        "dataset_name": "Dataset025_leg",
        "output": "LympClear_lower_pretrained_Dataset025_leg_fold0_checkpoint_best.zip",
        "description": "Lower-extremity source-domain pretrained model",
    },
    "upper_n10": {
        "dataset_id": 33,
        "dataset_name": "Dataset033_finetune10",
        "output": "LympClear_upper_finetune10_Dataset033_finetune10_fold0_checkpoint_best.zip",
        "description": "10-case upper-extremity fine-tuned model",
    },
    "upper_final": {
        "dataset_id": 38,
        "dataset_name": "Dataset038_finetune127",
        "output": "LympClear_upper_finetune127_Dataset038_finetune127_fold0_checkpoint_best.zip",
        "description": "Final 127-case upper-extremity fine-tuned model",
    },
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def export_item(item, out_dir: Path, fold: int, config: str, trainer: str, plans: str, checkpoint: str):
    output_path = out_dir / item["output"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "nnUNetv2_export_model_to_zip",
        "-d", str(item["dataset_id"]),
        "-c", config,
        "-f", str(fold),
        "-tr", trainer,
        "-p", plans,
        "-chk", checkpoint,
        "-o", str(output_path),
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    return output_path


def parse_args():
    p = argparse.ArgumentParser(description="Export manuscript-confirmed nnU-Net weights for public release.")
    p.add_argument("--nnunet-results", default=None, help="Optional; normally use $nnUNet_results")
    p.add_argument("--output-dir", default="weights")
    p.add_argument("--fold", type=int, default=0)
    p.add_argument("--config", default="3d_fullres")
    p.add_argument("--trainer", default="nnUNetTrainer")
    p.add_argument("--plans", default="nnUNetPlans")
    p.add_argument("--checkpoint", default="checkpoint_best.pth")
    p.add_argument("--include-lower", action="store_true")
    p.add_argument("--include-upper-n10", action="store_true")
    p.add_argument("--include-upper-final", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    out_dir = Path(args.output_dir)
    selected = []
    if args.include_lower:
        selected.append("lower")
    if args.include_upper_n10:
        selected.append("upper_n10")
    if args.include_upper_final:
        selected.append("upper_final")
    if not selected:
        selected = ["lower", "upper_final"]

    manifest = {
        "release_version": "v1.0.0",
        "fold": args.fold,
        "checkpoint": args.checkpoint,
        "configuration": args.config,
        "weights": [],
    }
    for key in selected:
        item = DEFAULT_ITEMS[key]
        if args.dry_run:
            print(f"Would export {key}: {item}")
            continue
        path = export_item(item, out_dir, args.fold, args.config, args.trainer, args.plans, args.checkpoint)
        manifest["weights"].append({
            "name": key,
            "dataset_id": item["dataset_id"],
            "dataset_name": item["dataset_name"],
            "description": item["description"],
            "filename": path.name,
            "sha256": sha256_file(path),
        })

    manifest_path = out_dir / "weight_manifest.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    print(f"Wrote {manifest_path}")


if __name__ == "__main__":
    main()
