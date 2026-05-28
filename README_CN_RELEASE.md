# LympClear 开源发布说明（中文）

这个仓库已经按你的论文和你确认的信息重新整理，重点保证以下内容一致：

- `Dataset025_leg`：论文中的下肢 MRL 预训练模型；
- `Dataset029_upperlimb`：上肢 development/full dataset；
- `Dataset033_finetune10`：论文中的 10 例上肢微调模型；
- `Dataset038_finetune127`：最终 127 例上肢微调模型；
- 最终模型使用 `fold_0`；
- 最终 checkpoint 使用 `checkpoint_best.pth`；
- 微调命令使用 `nnUNetv2_train ... -pretrained_weights`；
- 静脉抑制采用 `3×3×3 local non-venous median`；
- GitHub 发布代码，同时发布下肢预训练权重和最终上肢微调权重。

## 你上传 GitHub 前的实际操作

1. 解压本项目。
2. 在真实训练服务器上配置 nnU-Net 环境变量：

```bash
export nnUNet_raw=/your/path/nnUNet_raw
export nnUNet_preprocessed=/your/path/nnUNet_preprocessed
export nnUNet_results=/your/path/nnUNet_results
```

3. 导出权重：

```bash
python scripts/14_package_weights_for_release.py \
  --nnunet-results "$nnUNet_results" \
  --output-dir weights \
  --include-lower \
  --include-upper-final \
  --include-upper-n10
```

4. 做一次敏感信息检查：

```bash
python scripts/13_redact_and_check_repo.py --repo-root .
```

5. 本地跑通 demo 或真实测试病例后再上传 GitHub。

## 重要提醒

这个压缩包没有包含真实模型权重，因为你没有把服务器上的 `checkpoint_best.pth` 或 nnU-Net 导出 zip 上传到当前对话。仓库已经准备好了 `weights/` 目录、manifest 和自动打包脚本。你需要在本地服务器运行脚本导出真实权重后，再放到 GitHub Release 或 Git LFS。

不建议上传：

- 真实 DICOM；
- 真实 NIfTI；
- 真实人工 mask；
- PACS AE title、IP、端口；
- 服务器绝对路径；
- 带患者编号的 CSV；
- 整个 `nnUNet_raw`、`nnUNet_preprocessed`、`nnUNet_results` 工作目录。
