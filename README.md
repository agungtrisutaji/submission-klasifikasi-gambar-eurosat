# Open Images IT Asset Classification

Branch eksperimen: `experiment/open-images-it-assets`

Repository ini berisi eksperimen migrasi submission Dicoding **Belajar Fundamental Deep Learning** dari baseline EuroSAT RGB ke **Open Images V7 IT Asset Subset**. Target eksperimen adalah submission klasifikasi gambar yang lebih dekat dengan saran bintang 5: dataset minimal 10.000 gambar, resolusi asli tidak seragam, akurasi train/test minimal 95%, callback, proof inference, dan export SavedModel, TFLite, serta TFJS.

Baseline EuroSAT lama tetap dipertahankan di repository sebagai referensi historis. Notebook utama eksperimen Open Images adalah:

```text
klasifikasi-gambar-it-assets.ipynb
```

## Status Final Eksperimen

Dataset Open Images IT Asset sudah dibangun, di-split, diaudit, dilatih, dievaluasi, dan diexport secara lokal.

| Item | Status |
| --- | --- |
| Dataset Open Images V7 crop classification | Selesai |
| Total crop valid | 15.000 |
| Jumlah kelas | 5 |
| Resolusi crop asli tidak seragam | Ya, 14.168 resolusi unik |
| Source image leakage antar split | 0 |
| Duplicate file hash antar split | 0 |
| Corrupt image | 0 |
| Train accuracy | 99,73% |
| Validation accuracy | 95,54% |
| Test accuracy | 95,79% |
| SavedModel export | Valid |
| TFLite export | Valid |
| TFJS export | Valid |

Model final dipilih berdasarkan validation accuracy, bukan test set. Test set hanya dipakai sekali untuk evaluasi final.

## Dataset

Subset dibuat dari **Open Images V7** dengan label type `detections`. Bounding box objek target di-crop menjadi gambar klasifikasi single-object.

Kelas final:

| Open Images class | Label lokal | Crop |
| --- | --- | ---: |
| Camera | `camera` | 3.000 |
| Computer keyboard | `computer_keyboard` | 3.000 |
| Computer monitor | `computer_monitor` | 3.000 |
| Laptop | `laptop` | 3.000 |
| Mobile phone | `mobile_phone` | 3.000 |

Kelas yang ditolak dari kandidat awal:

| Label lokal | Alasan |
| --- | --- |
| `computer_mouse` | hanya 724 crop valid dari target 2.000 |
| `printer` | hanya 262 crop valid dari target 2.000 |
| `headphones` | hanya 1.241 crop valid dari target 2.000 |

Dataset lokal tidak dimasukkan ke git. Folder besar/cache seperti `dataset/`, `openimages_data/`, `fiftyone/`, `tfds_data/`, dan `outputs/` di-ignore.

## Split Dataset

Split dibuat dengan seed `42`, group split berdasarkan `source_image_id`, dan rasio mendekati 80/10/10.

| Split | Total |
| --- | ---: |
| Train | 12.002 |
| Validation | 1.502 |
| Test | 1.496 |

Audit split final:

```text
outputs/dataset_audit/openimages_split_audit.json
outputs/dataset_audit/openimages_split_summary.csv
```

Ringkasan audit terdokumentasi di:

```text
notes/OPEN_IMAGES_SPLIT_AUDIT.md
notes/FINAL_AUDIT_IT_ASSETS.md
```

## Model Final

Model final adalah ensemble TensorFlow/Keras dengan horizontal-flip test-time augmentation di dalam graph export:

```text
EfficientNetV2B1 + EfficientNetV2B2 + EfficientNetV2B3 + ConvNeXtTiny
```

Metrik real dari run lokal:

| Metric | Value |
| --- | ---: |
| Train accuracy | 0.9973 |
| Validation accuracy | 0.9554 |
| Test accuracy | 0.9579 |

File evaluasi:

```text
outputs/evaluation/15k_ensemble_eval.json
outputs/evaluation/15k_classification_report.csv
outputs/evaluation/15k_confusion_matrix.csv
```

## Export Model

Export lokal yang sudah tervalidasi:

```text
saved_model/it_asset_classifier/
tflite/it_asset_classifier.tflite
tfjs/it_asset_classifier/
label.txt
tflite/label.txt
tfjs/it_asset_classifier/label.txt
```

Validasi export:

| Export | Status | Output shape |
| --- | --- | --- |
| SavedModel | exported_and_validated | `[1, 5]` |
| TFLite | exported_and_validated | `[1, 5]` |
| TFJS | exported_and_validated | 5 kelas |

Catatan penting: model ensemble berukuran besar. Artefak export IT Asset sudah tervalidasi secara lokal, tetapi `saved_model/it_asset_classifier/`, `tflite/it_asset_classifier.tflite`, dan `tfjs/it_asset_classifier/` sengaja di-ignore dari Git biasa karena melewati batas file GitHub 100 MB. Untuk submission final, simpan artefak ini di workspace lokal/ZIP submission atau gunakan Git LFS bila memang harus dipush ke GitHub.

## Cara Rebuild Dataset

Jalankan dari root repository:

```powershell
.\.venv\Scripts\python.exe src\build_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --target-crops-per-class 3000 --max-samples-per-class 9000 --source-splits train --overwrite
```

Audit dataset crop:

```powershell
.\.venv\Scripts\python.exe src\audit_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --min-crops-per-class 3000
```

Buat split:

```powershell
.\.venv\Scripts\python.exe src\split_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --metadata-path dataset\metadata\openimages_crop_metadata.csv --raw-dir dataset\raw --split-dir dataset --train-ratio 0.8 --validation-ratio 0.1 --test-ratio 0.1 --seed 42 --overwrite
```

Audit split:

```powershell
.\.venv\Scripts\python.exe src\audit_openimages_split.py --class-config configs\openimages_it_assets_classes.json --split-metadata-path dataset\metadata\openimages_split_metadata.csv --audit-json outputs\dataset_audit\openimages_split_audit.json --split-summary-csv outputs\dataset_audit\openimages_split_summary.csv --min-total-crops 10000 --min-crops-per-class 3000
```

## Cara Menjalankan Notebook

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter notebook klasifikasi-gambar-it-assets.ipynb
```

Notebook berisi alur dataset, modelling, evaluasi, inference proof, dan export. Test set tidak boleh digunakan untuk training, tuning, callback, checkpoint selection, atau model selection.

## Struktur Penting

```text
configs/openimages_it_assets_classes.json
src/build_openimages_subset.py
src/audit_openimages_subset.py
src/split_openimages_subset.py
src/audit_openimages_split.py
klasifikasi-gambar-it-assets.ipynb
notes/
saved_model/it_asset_classifier/
tflite/it_asset_classifier.tflite
tfjs/it_asset_classifier/
```

## Reproducibility Notes

- Seed utama: `42`.
- Semua path notebook dan script relatif terhadap root repository.
- Augmentasi hanya diterapkan pada training pipeline.
- Test set hanya digunakan untuk evaluasi final dan inference proof.
- Dataset dan cache besar tidak dimasukkan ke git.
- Hasil akurasi yang dilaporkan berasal dari output evaluasi real, bukan manipulasi manual.
