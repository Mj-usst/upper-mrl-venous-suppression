# Training protocol

## 1. Pretraining on lower-extremity MRL

Confirmed lower-extremity source-domain model:

```text
Dataset025_leg
fold_0
checkpoint_best.pth
```

## 2. Upper-extremity scratch training

```bash
bash scripts/03_train_scratch.sh --dataset-id 29 --fold 0 --config 3d_fullres
```

## 3. Upper-extremity fine-tuning

Confirmed fine-tuning method:

```bash
nnUNetv2_train TARGET_DATASET_ID 3d_fullres 0 -pretrained_weights PRETRAINED_CHECKPOINT
```

Example final 127-case fine-tuning:

```bash
bash scripts/04_finetune_from_lower_limb.sh \
  --target-dataset-id 38 \
  --fold 0 \
  --config 3d_fullres \
  --pretrained-checkpoint "$nnUNet_results/Dataset025_leg/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_0/checkpoint_best.pth"
```

## 4. Learning-curve models

The manuscript evaluates target-domain labeled sample sizes:

```text
1, 2, 5, 10, 20, 40, 80, 127
```

The confirmed 10-case model is:

```text
Dataset033_finetune10/fold_0/checkpoint_best.pth
```

The confirmed final 127-case model is:

```text
Dataset038_finetune127/fold_0/checkpoint_best.pth
```
