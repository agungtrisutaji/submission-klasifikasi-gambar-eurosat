# Project Context

## Project

Dicoding Submission: Proyek Klasifikasi Gambar

Course: Belajar Fundamental Deep Learning

Branch eksperimen:

```text
experiment/open-images-it-assets
```

Dataset final branch ini:

```text
Open Images V7 IT Asset Subset
```

Notebook utama:

```text
klasifikasi-gambar-it-assets.ipynb
```

## Status Saat Ini

Project sudah melewati dataset preparation, split audit, modelling, training, evaluasi final, inference proof, dan export utama.

| Area | Status | Catatan |
| --- | --- | --- |
| Dataset selected | Done | Open Images V7 IT Asset Subset |
| Dataset loaded/downloaded | Done | via FiftyOne Open Images V7 detections |
| Crop dataset built | Done | 15.000 crop, 5 kelas |
| Train/validation/test split | Done | group split by `source_image_id`, seed 42 |
| Dataset audit | Done | leakage antar split 0, corrupt image 0 |
| Modelling | Done | baseline Sequential CNN dan final transfer-learning ensemble |
| Evaluation | Done | train 0.9973, validation 0.9554, test 0.9579 |
| Export | Done | SavedModel, TFLite, dan TFJS dibuat dan divalidasi |

## Dataset Preparation

Struktur dataset lokal:

```text
dataset/
├── raw/
├── train/
├── validation/
└── test/
```

Split:

```text
train: 12002 crops
validation: 1502 crops
test: 1496 crops
seed: 42
method: grouped by source_image_id
```

Audit output:

```text
outputs/dataset_audit/openimages_split_audit.json
outputs/dataset_audit/openimages_split_summary.csv
```

## Model

Model final:

```text
EfficientNetV2B1 + EfficientNetV2B2 + EfficientNetV2B3 + ConvNeXtTiny
```

Model kandidat dipilih berdasarkan validation accuracy, bukan test accuracy.

## Evaluation

Ringkasan run final:

```text
train accuracy: 0.9973
validation accuracy: 0.9554
test accuracy: 0.9579
```

Test set hanya digunakan pada evaluasi akhir dan sample inference.

## Export

Export yang tervalidasi:

```text
saved_model/it_asset_classifier/
tflite/it_asset_classifier.tflite
tfjs/it_asset_classifier/
```

Risiko utama saat ini adalah ukuran export ensemble yang besar.
