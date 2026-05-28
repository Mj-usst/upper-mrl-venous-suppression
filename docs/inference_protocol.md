# Inference protocol

## 1. Install public model archive

```bash
nnUNetv2_install_pretrained_model_from_zip weights/LympClear_upper_finetune127_Dataset038_finetune127_fold0_checkpoint_best.zip
```

## 2. Predict venous mask

```bash
bash scripts/07_predict_upper_final.sh \
  --input /path/to/imagesTs \
  --output outputs/pred_venous_mask
```

## 3. Generate postprocessed outputs

```bash
python scripts/08_postprocess_suppression_highlighting.py \
  --image /path/to/case_0000.nii.gz \
  --mask outputs/pred_venous_mask/case.nii.gz \
  --out-dir outputs/postprocessed_case \
  --mode both
```

## 4. Create MIP/cine

```bash
python scripts/10_make_mip_cine.py \
  --image outputs/postprocessed_case/suppressed.nii.gz \
  --out-dir outputs/postprocessed_case/mip_cine \
  --axis 0 \
  --make-gif
```
