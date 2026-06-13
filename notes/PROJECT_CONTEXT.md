# PROJECT_CONTEXT.md

## Project

Dicoding Submission: Proyek Klasifikasi Gambar
Course: Belajar Fundamental Deep Learning

## Main Notebook

```text
klasifikasi-gambar-eurosat.ipynb
```

## Current Project Phase

Current phase:

```text
02 - Dataset & Struktur Data
```

The project must not move to modelling until dataset preparation, split, and audit are complete.

## Dataset Decision

Final dataset:

```text
EuroSAT RGB
```

Reason:

1. 27,000 images.
2. 10 classes.
3. Suitable for multi-class image classification.
4. Not a prohibited/simple dataset such as Rock Paper Scissors.
5. Clear source through TensorFlow Datasets and official EuroSAT repository.
6. Reasonable size for Colab/local experimentation.

## Current Dataset Status

| Area                        |  Status | Notes                                         |
| --------------------------- | ------: | --------------------------------------------- |
| Dataset selected            |    Done | EuroSAT RGB                                   |
| Dataset loaded/downloaded   | Not yet | Must be done in notebook                      |
| Metadata validated          | Not yet | Need total images, class names, shape, dtype  |
| Train/validation/test split | Not yet | Use stratified 80/10/10                       |
| Dataset audit               | Not yet | Check distribution, corrupt files, duplicates |
| Ready for modelling         |      No | Dataset stage is not complete                 |

## Dataset Preparation Target

Create this structure:

```text
dataset/
├── raw/
├── train/
├── validation/
└── test/
```

Each split must contain 10 class folders.

## Split Strategy

Use:

```text
train: 80%
validation: 10%
test: 10%
seed: 42
method: stratified per class
```

## Audit Outputs

Save:

```text
outputs/dataset_audit/dataset_split_summary.csv
outputs/dataset_audit/dataset_audit_summary.json
```

## Next Action

Work only on dataset preparation in `klasifikasi-gambar-eurosat.ipynb`.

Do not implement modelling, training, evaluation, inference, or export yet.
