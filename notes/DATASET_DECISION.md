# Dataset Decision

Dataset final untuk submission ini adalah **EuroSAT RGB**.

## Alasan Pemilihan

- Memenuhi konteks image classification multi-class.
- Memiliki 27.000 gambar, cukup besar untuk submission final.
- Memiliki 10 kelas dengan distribusi yang jelas.
- Bukan dataset sederhana/prohibited seperti Rock Paper Scissors.
- Tersedia melalui TensorFlow Datasets sebagai `eurosat/rgb`.
- Sumber resmi dan referensi dataset mudah dilacak.

## Karakteristik Dataset

| Properti | Nilai |
| --- | --- |
| Total gambar | 27.000 |
| Jumlah kelas | 10 |
| Resolusi asli | 64x64 |
| Channel | RGB |
| TFDS split awal | `train` saja |
| Task | Multi-class image classification |

## Split yang Digunakan

Karena TFDS hanya menyediakan split awal `train`, notebook membuat split eksplisit:

| Split | Jumlah | Proporsi |
| --- | ---: | ---: |
| Train | 21.600 | 80% |
| Validation | 2.700 | 10% |
| Test | 2.700 | 10% |

Split dilakukan stratified per kelas dengan seed `42`.

## Data Leakage Control

- Test set tidak digunakan untuk training.
- Test set tidak digunakan untuk tuning hyperparameter.
- Test set tidak digunakan untuk callback atau checkpoint selection.
- Model terbaik dipilih berdasarkan validation set.
- Data augmentation hanya berada di model training flow dan tidak diterapkan sebagai transformasi permanen ke validation/test data.
