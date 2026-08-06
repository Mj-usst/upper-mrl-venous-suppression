# Release checklist

Before making the GitHub repository public, complete the following checks.

## Code consistency

- [ ] `configs/paper_constants.yaml` matches the final manuscript's model-related methods.
- [ ] `configs/release_mapping.yaml` uses `Dataset025_leg`, `Dataset029_upperlimb`, `Dataset033_finetune10`, and `Dataset038_finetune127`.
- [ ] Final model uses `fold_0`.
- [ ] Final model uses `checkpoint_best.pth`.
- [ ] Fine-tuning script uses `nnUNetv2_train ... -pretrained_weights`.
- [ ] Venous suppression is implemented as a `3×3×3` local nonvenous median.
- [ ] The learning-curve CSV matches manuscript Table 2.
- [ ] No reader-study ratings, preference-test results, or reader-study statistical-analysis scripts are included.
- [ ] No Grad-CAM code or derived maps are included.

## Weight release

- [ ] Export lower-extremity pretrained weight: `Dataset025_leg/fold_0/checkpoint_best.pth`.
- [ ] Export final upper-extremity fine-tuned weight: `Dataset038_finetune127/fold_0/checkpoint_best.pth`.
- [ ] Optionally export 10-case fine-tuned weight: `Dataset033_finetune10/fold_0/checkpoint_best.pth`.
- [ ] Upload weight archives through GitHub Releases or Git LFS.
- [ ] Update checksums in `weights/weight_manifest.yaml`.

## Privacy and security

- [ ] No DICOM files.
- [ ] No NIfTI files from real patients.
- [ ] No manual masks from real patients.
- [ ] No PACS IP, AE title, port, username, or password.
- [ ] No patient names or patient IDs.
- [ ] No internal absolute paths from hospital servers or PACS workstations.
- [ ] No reader-study source data or patient-level reader-study tables.
- [ ] Run `python scripts/13_redact_and_check_repo.py --repo-root .`.

## Usability

- [ ] A fresh clone can install the environment.
- [ ] `python -m compileall lympclear scripts` passes.
- [ ] The synthetic example can run.
- [ ] The model card is visible on GitHub.
- [ ] The release tag is created: `v1.0.0`.
