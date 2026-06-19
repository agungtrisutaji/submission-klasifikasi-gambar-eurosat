# Dataset Decision

Dataset final untuk branch eksperimen ini adalah **Open Images V7 IT Asset Subset**.

## Alasan Pemilihan

- Memenuhi konteks image classification multi-class.
- Memiliki lebih dari 10.000 crop valid.
- Memiliki 5 kelas aset IT yang mudah dipahami.
- Resolusi crop asli tidak seragam.
- Sumber dataset publik dan terdokumentasi.
- Bounding box Open Images dapat diubah menjadi crop objek untuk klasifikasi gambar.

## Karakteristik Dataset

| Properti | Nilai |
| --- | --- |
| Total crop | 15.000 |
| Jumlah kelas | 5 |
| Crop per class | 3.000 |
| Source dataset | Open Images V7 |
| Label type | detections |
| Task akhir | Multi-class crop image classification |

Kelas final:

- `camera`
- `computer_keyboard`
- `computer_monitor`
- `laptop`
- `mobile_phone`

## Split yang Digunakan

| Split | Jumlah | Proporsi |
| --- | ---: | ---: |
| Train | 12.002 | 0.8001 |
| Validation | 1.502 | 0.1001 |
| Test | 1.496 | 0.0997 |

Split dilakukan dengan seed `42` dan group split berdasarkan `source_image_id`.

## Data Leakage Control

- Semua crop dari source image yang sama berada di split lokal yang sama.
- Source image leakage antar split bernilai 0.
- Duplicate file hash antar split bernilai 0.
- Test set tidak digunakan untuk training.
- Test set tidak digunakan untuk tuning hyperparameter.
- Test set tidak digunakan untuk callback atau checkpoint selection.
- Model terbaik dipilih berdasarkan validation set.
- Data augmentation hanya diterapkan pada training flow.
