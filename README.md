# LympClear

**Cross-anatomic Transfer Learning for Venous Postprocessing at Upper-Extremity MR Lymphangiography**

LympClear is an nnU-Net-based research pipeline for venous segmentation and dual-mode postprocessing in dynamic contrast-enhanced upper-extremity MR lymphangiography (MRL). It supports:

1. source-domain lower-extremity MRL pretraining;
2. target-domain upper-extremity MRL fine-tuning;
3. venous-mask inference with 3D nnU-Net;
4. venous suppression using a local nonvenous median replacement;
5. venous highlighting for planning-oriented visualization;
6. MIP/cine generation;
7. Dice evaluation, learning-curve summarization, and reader-study statistics.

This repository was prepared to match the manuscript:

> Cross-anatomic Transfer Learning for Venous Postprocessing at Upper-Extremity MR Lymphangiography

## Paper-consistent study settings

The repository constants are defined in `configs/paper_constants.yaml` and `configs/release_mapping.yaml`.

| Item | Repository value |
|---|---|
| Source-domain lower-extremity pretraining dataset | `Dataset025_leg` |
| Upper-extremity development/full dataset | `Dataset029_upperlimb` |
| 10-case upper-extremity fine-tuned model | `Dataset033_finetune10` |
| Final 127-case upper-extremity fine-tuned model | `Dataset038_finetune127` |
| Final model fold | `fold_0` |
| Final checkpoint | `checkpoint_best.pth` |
| Fine-tuning method | `nnUNetv2_train ... -pretrained_weights` |
| Venous suppression | `3 × 3 × 3` local nonvenous median |
| Public release plan | code + lower-extremity pretrained weight + final upper-extremity weight |

## Repository layout

```text
LympClear/
├── README.md
├── README_CN_RELEASE.md
├── RELEASE_CHECKLIST.md
├── PAPER_CONSISTENCY_AUDIT.md
├── LICENSE
├── CITATION.cff
├── .gitignore
├── .gitattributes
├── environment.yml
├── requirements.txt
├── pyproject.toml
├── configs/
├── docs/
├── examples/
├── lympclear/
├── scripts/
├── tests/
├── weights/
└── results/
```

## Installation

```bash
conda env create -f environment.yml
conda activate lympclear
```

If you install manually:

```bash
pip install nnunetv2 nibabel SimpleITK pydicom numpy pandas scipy scikit-image imageio tqdm statsmodels matplotlib PyYAML
pip install -e .
```

## nnU-Net environment variables

Set the nnU-Net v2 paths before training or inference:

```bash
export nnUNet_raw=/path/to/nnUNet_raw
export nnUNet_preprocessed=/path/to/nnUNet_preprocessed
export nnUNet_results=/path/to/nnUNet_results
```

For Windows PowerShell:

```powershell
$env:nnUNet_raw="<path-to-nnUNet_raw>"
$env:nnUNet_preprocessed="<path-to-nnUNet_preprocessed>"
$env:nnUNet_results="<path-to-nnUNet_results>"
```

## Quick start: inference with the final upper-extremity model

After placing the public final model archive under `weights/`, install it into nnU-Net:

```bash
nnUNetv2_install_pretrained_model_from_zip weights/LympClear_upper_finetune127_fold0_checkpoint_best.zip
```

Run prediction on NIfTI images in nnU-Net format:

```bash
bash scripts/07_predict_upper_final.sh \
  --input /path/to/imagesTs \
  --output outputs/pred_venous_mask
```

Generate venous-suppressed and venous-highlighted outputs:

```bash
python scripts/08_postprocess_suppression_highlighting.py \
  --image /path/to/case_0000.nii.gz \
  --mask outputs/pred_venous_mask/case.nii.gz \
  --out-dir outputs/postprocessed_case \
  --mode both
```

Create MIP/cine visualizations:

```bash
python scripts/10_make_mip_cine.py \
  --image outputs/postprocessed_case/suppressed.nii.gz \
  --out-dir outputs/postprocessed_case/mip_cine \
  --axis 0 \
  --make-gif
```

## Training from scratch

```bash
bash scripts/03_train_scratch.sh --dataset-id 29 --fold 0 --config 3d_fullres
```

## Fine-tuning from the lower-extremity pretrained model

This matches the release confirmation: direct nnU-Net v2 fine-tuning with `-pretrained_weights`.

```bash
bash scripts/04_finetune_from_lower_limb.sh \
  --target-dataset-id 38 \
  --fold 0 \
  --config 3d_fullres \
  --pretrained-checkpoint "$nnUNet_results/Dataset025_leg/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_0/checkpoint_best.pth"
```

## Export model weights for GitHub Release

Because trained model weights were not uploaded to this ChatGPT session, the generated repository contains the weight manifest and export scripts, but not the actual `.pth`/`.zip` weights. On your workstation/server, run:

```bash
python scripts/14_package_weights_for_release.py \
  --nnunet-results "$nnUNet_results" \
  --output-dir weights \
  --include-lower \
  --include-upper-final \
  --include-upper-n10
```

Expected public release files:

```text
weights/LympClear_lower_pretrained_Dataset025_leg_fold0_checkpoint_best.zip
weights/LympClear_upper_finetune10_Dataset033_finetune10_fold0_checkpoint_best.zip
weights/LympClear_upper_finetune127_Dataset038_finetune127_fold0_checkpoint_best.zip
weights/weight_manifest.yaml
```

For GitHub, upload large model archives through **GitHub Releases** or **Git LFS** rather than ordinary commits.

## Data availability

Clinical imaging data and manual masks are not included because they contain sensitive patient-derived medical information and are subject to institutional data-governance restrictions. This repository includes code, configuration templates, aggregate result tables, and synthetic examples only.

## Clinical disclaimer

This software is provided for research use. It is not cleared or approved as a standalone clinical diagnostic, surgical-planning, or treatment-decision tool. Venous-highlighted outputs are intended to support visualization and communication; venous caliber, depth, and patency should be confirmed by clinical assessment such as targeted ultrasonography where applicable.
