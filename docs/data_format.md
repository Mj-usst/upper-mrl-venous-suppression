# Data format

LympClear uses nnU-Net v2 data conventions.

## Folder structure

```text
nnUNet_raw/
└── Dataset038_finetune127/
    ├── dataset.json
    ├── imagesTr/
    │   ├── case001_0000.nii.gz
    │   └── case002_0000.nii.gz
    ├── labelsTr/
    │   ├── case001.nii.gz
    │   └── case002.nii.gz
    └── imagesTs/
        └── case101_0000.nii.gz
```

## Channel naming

This release assumes a single image channel:

```json
{
  "channel_names": {"0": "postcontrast_T1w_MRL"},
  "labels": {"background": 0, "vein": 1},
  "file_ending": ".nii.gz"
}
```

## Phase handling

The manuscript reports that training used all dynamic phases per patient and the primary learning-curve evaluation was performed on phase 6. To avoid leakage, all phases from the same patient should remain in the same partition.

## Privacy

Do not commit raw DICOM files, real NIfTI files, manual masks, or patient-level CSV metadata.
