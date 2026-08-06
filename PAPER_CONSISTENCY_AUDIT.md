# Model-code consistency audit

This file records how the public repository maps to the model-related methods and results in the manuscript.

## Manuscript-to-repository mapping

| Manuscript model item | Repository implementation |
|---|---|
| 1022 lower-extremity MRL cases / 6162 dynamic phases for source-domain pretraining | `configs/paper_constants.yaml` and `configs/release_mapping.yaml` |
| 255 upper-extremity MRL cases / 1581 dynamic phases for adaptation and testing | `configs/paper_constants.yaml` |
| Development set: MC1, 127 patients | `configs/paper_constants.yaml` |
| External test sets: MC2 = 42, MC3 = 51, MC4 = 35 patients | `configs/paper_constants.yaml` and `results/learning_curve_table2.csv` |
| 3D nnU-Net for venous segmentation | `scripts/03_train_scratch.sh`, `scripts/04_finetune_from_lower_limb.sh`, `scripts/07_predict_upper_final.sh` |
| Fine-tuning with target-domain sample sizes 1, 2, 5, 10, 20, 40, 80, 127 | `configs/paper_constants.yaml`, `results/learning_curve_table2.csv` |
| 10-case model | `Dataset033_finetune10`, `weights/weight_manifest.yaml` |
| Final 127-case model | `Dataset038_finetune127`, `weights/weight_manifest.yaml` |
| Final fold and checkpoint | `fold_0`, `checkpoint_best.pth` in `configs/release_mapping.yaml` |
| Direct nnU-Net v2 fine-tuning with `-pretrained_weights` | `scripts/04_finetune_from_lower_limb.sh` |
| Primary evaluation phase: phase 6 | `configs/paper_constants.yaml`; reflected in result table notes |
| Patient-level Dice with bootstrap 95% confidence intervals | `lympclear/metrics/dice.py`, `scripts/09_evaluate_dice.py` |
| Aggregate learning-curve results | `results/learning_curve_table2.csv` and `results/key_results_summary.json` |
| Venous suppression | `lympclear/postprocessing/suppression.py`, `scripts/08_postprocess_suppression_highlighting.py` |
| Venous highlighting | `lympclear/postprocessing/highlighting.py`, `scripts/08_postprocess_suppression_highlighting.py` |
| MIP/cine generation | `lympclear/visualization/mip.py`, `scripts/10_make_mip_cine.py` |
| PACS deployment concept | Documented in `docs/deployment_dicom_workflow.md`; no private PACS endpoint is included |
| Clinical limitations | `docs/model_card.md` and README disclaimer |

## Public release scope

The public repository is limited to model training, transfer learning, inference, segmentation evaluation, aggregate learning-curve results, and image postprocessing.

The following manuscript components are intentionally not included:

- reader-study source data and ratings;
- paired-preference-test results;
- reader-study statistical-analysis code;
- Grad-CAM analysis code and derived maps;
- clinical DICOM/NIfTI data and manual masks;
- patient-level metadata;
- hospital-specific PACS configuration.

Actual trained weights are not currently committed to the repository. The weight-release scripts are included, and the weights must be exported from the original training server before publication through GitHub Releases or Git LFS.

## Release-level verification commands

```bash
python -m compileall lympclear scripts
python scripts/13_redact_and_check_repo.py --repo-root .
python scripts/00_check_environment.py
```
