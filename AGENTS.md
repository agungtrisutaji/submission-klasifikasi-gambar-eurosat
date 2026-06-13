# AGENTS.md

## Project Context

This project is a Dicoding final submission for **Belajar Fundamental Deep Learning**, focused on **image classification** using the **EuroSAT RGB** dataset.

The main notebook is:

```text
klasifikasi-gambar-eurosat.ipynb
```

This notebook is the primary source of truth for the submission. Do not create a replacement notebook unless explicitly requested.

## Main Goal

Build a clean, reproducible, reviewer-friendly image classification submission that:

1. satisfies all mandatory Dicoding criteria;
2. targets 5-star quality;
3. uses a valid image classification dataset;
4. avoids data leakage;
5. includes clear dataset preparation, modelling, training, evaluation, inference, and model export;
6. can be run from top to bottom without errors.

## Final Dataset Decision

The selected dataset is:

```text
EuroSAT RGB
```

Dataset source:

```text
TensorFlow Datasets: eurosat/rgb
Official EuroSAT repository
```

Known dataset characteristics:

```text
Total images: 27,000
Number of classes: 10
Image size: 64x64x3
Initial TFDS split: train only
Task: multi-class image classification
```

Because the original TFDS dataset only provides a train split, this project must create explicit:

```text
train/
validation/
test/
```

using stratified split with seed `42`.

## Important Workflow Rule

Do not start modelling before the dataset stage is complete.

The dataset stage is complete only if:

1. EuroSAT RGB is successfully loaded/downloaded.
2. Total images are validated.
3. Number of classes and class names are validated.
4. Dataset is exported or prepared into a clear folder structure.
5. Stratified train/validation/test split is created.
6. Dataset distribution is audited.
7. Corrupt images are checked.
8. Duplicate images are checked.
9. Cross-split duplicates are checked.
10. Dataset source and license are documented.

## Expected Workspace Structure

Use this structure:

```text
submission-klasifikasi-gambar-eurosat/
├── AGENTS.md
├── README.md
├── requirements.txt
├── .gitignore
├── klasifikasi-gambar-eurosat.ipynb
├── dataset/
│   └── .gitkeep
├── models/
│   └── .gitkeep
├── outputs/
│   ├── dataset_audit/
│   ├── evaluation/
│   └── export/
└── notes/
    ├── PROJECT_CONTEXT.md
    ├── SUBMISSION_CHECKLIST.md
    └── DATASET_DECISION.md
```

## Coding Rules

1. Use relative paths only.
2. Do not use personal local paths such as `C:/Users/...` or `/Users/...`.
3. Use seed `42` for reproducibility.
4. Keep code readable and notebook-friendly.
5. Add markdown explanations before major notebook sections.
6. Do not remove existing template sections unless explicitly requested.
7. Do not hardcode class names if they can be extracted from TFDS metadata.
8. Do not use test data for training, tuning, checkpoint selection, or early stopping.
9. Keep train, validation, and test usage clearly separated.
10. Prefer small, safe changes over large rewrites.

## Notebook Section Order

The notebook should follow this order:

```text
1. Project introduction
2. Import libraries
3. Reproducibility setup
4. Dataset loading
5. Dataset metadata validation
6. Dataset export / preparation
7. Train-validation-test split
8. Dataset audit
9. Image preprocessing pipeline
10. Data augmentation
11. Baseline model
12. Improved model / transfer learning if needed
13. Training with callbacks
14. Training history visualization
15. Final evaluation on test set
16. Confusion matrix and classification report
17. Inference test
18. Model export
19. Export validation
20. Conclusion
```

## Dataset Preparation Requirements

For the dataset stage, implement:

1. Load `eurosat/rgb` from TensorFlow Datasets.
2. Validate metadata:

   * total images;
   * number of classes;
   * class names;
   * split information;
   * image shape;
   * dtype.
3. Export or prepare dataset into:

```text
dataset/raw/<class_name>/
dataset/train/<class_name>/
dataset/validation/<class_name>/
dataset/test/<class_name>/
```

4. Split using 80/10/10 stratified split per class with seed `42`.
5. Save audit outputs to:

```text
outputs/dataset_audit/dataset_split_summary.csv
outputs/dataset_audit/dataset_audit_summary.json
```

6. Audit:

   * class distribution before split;
   * class distribution after split;
   * image format;
   * image mode;
   * image resolution;
   * corrupt files;
   * duplicate files;
   * duplicate files across splits.

## Modelling Rules

Do not implement modelling until the dataset stage is confirmed complete.

When modelling starts:

1. Use TensorFlow/Keras.
2. Start with a clear baseline if needed.
3. Use data augmentation for training data only.
4. Use callbacks:

   * EarlyStopping;
   * ModelCheckpoint;
   * optionally ReduceLROnPlateau.
5. Explain all design choices in markdown.
6. Track accuracy and loss for training and validation.
7. Watch for overfitting and underfitting.

## Evaluation Rules

Evaluation must include:

1. Training and validation accuracy/loss plots.
2. Test set evaluation.
3. Confusion matrix.
4. Classification report.
5. Inference examples with:

   * input image;
   * predicted label;
   * confidence score;
   * true label if available.
6. Explanation of model performance and limitations.

## Export Rules

Export format must follow the official Dicoding submission instruction.

If multiple formats are required, separate the export cells clearly.

After export:

1. Load the exported model again.
2. Run inference using the exported model.
3. Confirm the exported model produces valid predictions.

## Documentation Rules

Update `README.md` with:

1. Project overview.
2. Dataset source and license.
3. Dataset structure.
4. How to run the notebook.
5. Model summary.
6. Evaluation result.
7. Exported model files.
8. Notes for reproducibility.

## What Not To Do

Do not:

1. start modelling before dataset validation is complete;
2. use test data for training or tuning;
3. create unrelated API, Docker, MLflow, CI/CD, monitoring, or deployment files unless the submission explicitly requires them;
4. remove important notebook explanations;
5. hardcode absolute local paths;
6. commit large dataset files unless explicitly needed;
7. create a final ZIP before final audit.
