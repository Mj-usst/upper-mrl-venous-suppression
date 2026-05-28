# Synthetic demo case

Run:

```bash
python scripts/12_generate_synthetic_demo.py
python scripts/08_postprocess_suppression_highlighting.py \
  --image examples/synthetic_case/imagesTs/synthetic_upper_mrl_0000.nii.gz \
  --mask examples/synthetic_case/labelsTs/synthetic_upper_mrl.nii.gz \
  --out-dir outputs/synthetic_postprocess \
  --mode both
```

This synthetic demo is not clinical data.
