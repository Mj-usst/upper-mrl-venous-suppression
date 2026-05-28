# Model Card: LympClear Upper-Extremity Venous Segmentation Model

## Model name

LympClear upper-extremity venous segmentation model.

## Intended use

This model is intended for research use in venous segmentation and postprocessing of contrast-enhanced upper-extremity MR lymphangiography. The predicted venous mask can be used to generate:

- venous-suppressed images for lymphatic interpretation;
- venous-highlighted images for planning-oriented visualization and communication.

## Out-of-scope use

The model is not intended for standalone diagnosis, treatment selection, autonomous surgical planning, or replacement of radiologist review. Venous-highlighted outputs should not replace targeted ultrasonography or other clinical confirmation of venous caliber, depth, and patency.

## Training summary

- Source-domain pretraining: lower-extremity MR lymphangiography, `Dataset025_leg`.
- Target-domain fine-tuning: upper-extremity MR lymphangiography, including `Dataset033_finetune10` and final `Dataset038_finetune127`.
- Architecture: 3D nnU-Net.
- Final public model: `Dataset038_finetune127`, `fold_0`, `checkpoint_best.pth`.
- Fine-tuning method: `nnUNetv2_train ... -pretrained_weights`.

## Input

- Fat-suppressed 3D T1-weighted postcontrast MR lymphangiography.
- NIfTI format in nnU-Net v2 convention, e.g. `case001_0000.nii.gz`.
- Phase 6 or equivalent late postcontrast phase is recommended for results matching the manuscript's primary evaluation.

## Output

- Binary venous mask with labels: `0 = background`, `1 = vein`.
- Optional venous-suppressed NIfTI image.
- Optional venous-highlighted PNG/MIP visualizations.

## Known limitations

- Residual errors may occur near injection sites.
- Superficial venous clusters may cause over-suppression or residual artifact.
- Severe motion, metal artifact, field inhomogeneity, or unusual acquisition protocols may reduce performance.
- Results may require adaptation before use in other anatomic regions or scanner protocols.

## Ethical and privacy considerations

The public repository does not include patient-level imaging data or masks. Public weights should be released only after institutional approval.
