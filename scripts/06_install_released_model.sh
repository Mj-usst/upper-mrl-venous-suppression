#!/usr/bin/env bash
set -euo pipefail

MODEL_ZIP="weights/LympClear_upper_finetune127_Dataset038_finetune127_fold0_checkpoint_best.zip"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model-zip) MODEL_ZIP="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ ! -f "$MODEL_ZIP" ]]; then
  echo "Model archive not found: $MODEL_ZIP" >&2
  exit 1
fi

nnUNetv2_install_pretrained_model_from_zip "$MODEL_ZIP"
