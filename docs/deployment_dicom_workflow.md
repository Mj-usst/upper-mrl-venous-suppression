# DICOM/PACS deployment concept

The manuscript describes a clinical workflow in which MRL DICOM series are transferred to a dedicated AI inference server, processed, and returned to PACS as derived DICOM series with geometry preserved.

This public repository does **not** include hospital-specific PACS settings. Do not publish:

- AE title;
- IP address;
- port;
- username or password;
- routing rules;
- internal server paths.

For a local institutional deployment, implement the following steps under institutional governance:

1. receive DICOM series from scanner/PACS;
2. convert or map the target MRL phase to NIfTI for nnU-Net inference;
3. run venous mask prediction;
4. generate venous-suppressed and venous-highlighted outputs;
5. preserve orientation, spacing, and slice position metadata;
6. export derived series back to PACS with new SeriesInstanceUID;
7. keep the original clinical series unchanged.
