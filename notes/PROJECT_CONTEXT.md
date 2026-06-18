# Project Context

## Project

Dicoding Submission: Proyek Klasifikasi Gambar

Course: Belajar Fundamental Deep Learning

Dataset final: EuroSAT RGB

Notebook utama:

```text
klasifikasi-gambar-eurosat.ipynb
```

## Status Saat Ini

Project sudah melewati tahap dataset preparation, modelling, training, evaluasi awal, dan export utama.

| Area | Status | Catatan |
| --- | --- | --- |
| Dataset selected | Done | EuroSAT RGB |
| Dataset loaded/downloaded | Done | TFDS `eurosat/rgb` dengan mirror Zenodo bila URL bawaan bermasalah |
| Metadata validated | Done | 27.000 gambar, 10 kelas, RGB 64x64x3 |
| Train/validation/test split | Done | Stratified per kelas, 80/10/10, seed 42 |
| Dataset audit | Done | Tidak ada corrupt image atau duplicate cross-split pada run lokal |
| Modelling | Done | Baseline CNN, MobileNetV2 transfer learning, dan MobileNetV2 fine-tuning |
| Evaluation | Done | Test accuracy run penuh final: 0.9448 |
| Export | Done | SavedModel, TFLite, dan TFJS berhasil dibuat dan divalidasi |

## Dataset Preparation

Struktur dataset lokal yang dibuat notebook:

```text
dataset/
├── raw/
├── train/
├── validation/
└── test/
```

Split:

```text
train: 21.600 images
validation: 2.700 images
test: 2.700 images
seed: 42
method: stratified per class
```

Audit output:

```text
outputs/dataset_audit/dataset_split_summary.csv
outputs/dataset_audit/dataset_audit_summary.json
```

## Model

Model yang dibandingkan:

1. Baseline CNN.
2. MobileNetV2 transfer learning dengan base model frozen.
3. MobileNetV2 fine-tuning dari checkpoint transfer learning terbaik.

Model kandidat dipilih berdasarkan validation accuracy, bukan test accuracy.

Model terbaik pada run penuh final:

```text
mobilenetv2_finetuned
```

## Evaluation

Ringkasan run penuh final:

```text
train accuracy checkpoint: 0.9562
validation accuracy checkpoint: 0.9396
test accuracy: 0.9448
test loss: 0.1753
test samples: 2.700
```

Test set hanya digunakan pada bagian evaluasi akhir dan sample inference.

## Export

Export yang tervalidasi:

```text
saved_model/eurosat_classifier/
tflite/eurosat_classifier.tflite
tflite/label.txt
tfjs/eurosat_classifier/model.json
tfjs/eurosat_classifier/group1-shard*.bin
tfjs/eurosat_classifier/label.txt
```

TFJS export membutuhkan package `tensorflowjs`, tetapi package tersebut tidak dimasukkan langsung ke `requirements.txt` karena resolver pip menarik `tensorflow-decision-forests` yang bentrok pada Windows/Python 3.12. Pada run lokal, TFJS berhasil dibuat sebagai graph model dari SavedModel inference-only sementara dengan output signature 10 kelas.
