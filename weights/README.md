# Model weights

The public release is intended to include:

1. Lower-extremity pretrained model:
   `LympClear_lower_pretrained_Dataset025_leg_fold0_checkpoint_best.zip`
2. Final upper-extremity fine-tuned model:
   `LympClear_upper_finetune127_Dataset038_finetune127_fold0_checkpoint_best.zip`
3. Optional 10-case fine-tuned model for learning-curve reproducibility:
   `LympClear_upper_finetune10_Dataset033_finetune10_fold0_checkpoint_best.zip`

The actual model weights are **not included** in this generated ChatGPT archive because the trained `.pth`/`.zip` files were not uploaded. Export them on the training server:

```bash
python scripts/14_package_weights_for_release.py \
  --nnunet-results "$nnUNet_results" \
  --output-dir weights \
  --include-lower \
  --include-upper-final \
  --include-upper-n10
```

Upload large weight archives through GitHub Releases or Git LFS.
