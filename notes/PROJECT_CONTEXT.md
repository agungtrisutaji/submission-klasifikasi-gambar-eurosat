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
| Modelling | Done | Baseline CNN dan MobileNetV2 transfer learning |
| Evaluation | Done | Test accuracy run lokal: 0.9148 |
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

Model kandidat dipilih berdasarkan validation accuracy, bukan test accuracy.

Model terbaik pada run lokal:

```text
mobilenetv2_transfer_learning
```

## Evaluation

Ringkasan run lokal:

```text
best training accuracy: 0.8855
best validation accuracy: 0.9178
test accuracy: 0.9148
test loss: 0.2519
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

TFJS export membutuhkan package `tensorflowjs`, tetapi package tersebut tidak ditambahkan ke `requirements.txt` karena file tersebut tidak boleh diubah. Pada run lokal, TFJS berhasil dibuat sebagai graph model dari SavedModel inference-only sementara dengan output signature 10 kelas.
