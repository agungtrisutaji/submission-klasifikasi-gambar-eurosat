# Dataset Rework Decision

Tanggal: 2026-06-18

## Keputusan

Submission tetap memakai **EuroSAT RGB**.

Alasan teknis:

- EuroSAT RGB sudah memenuhi kriteria wajib dataset: 27.000 gambar, 10 kelas, bukan Rock Paper Scissors, bukan X-Ray, dan dapat direproduksi melalui TensorFlow Datasets.
- Pipeline dataset, audit split, training, evaluasi, inference, dan export model sudah lengkap.
- Fine-tuning MobileNetV2 menaikkan performa dibanding transfer learning frozen, tetapi run penuh final masih berada sedikit di bawah saran bintang 5 95% pada test accuracy.
- EuroSAT RGB memiliki resolusi asli seragam `64x64x3`, sehingga saran resolusi asli tidak seragam tidak diklaim terpenuhi.
- Mengganti dataset pada tahap akhir berisiko membuat submission kurang reproducible jika tidak diaudit dan dijalankan ulang penuh dari awal.

## Ringkasan Kandidat Dataset Alternatif

| Dataset | Sumber | Jumlah gambar | Kelas | Resolusi asli | Risiko |
| --- | --- | ---: | ---: | --- | --- |
| Intel Image Classification | Kaggle | sekitar 25.000 | 6 | umumnya 150x150 | Perlu Kaggle workflow; akurasi 95% tidak pasti untuk scene classification. |
| Food-101 | ETH/TFDS/Hugging Face | 101.000 | 101 | gambar di-rescale max side 512 | Dataset besar dan menantang; target 95% tidak realistis untuk submission cepat. |
| PlantVillage | TFDS/GitHub | sekitar 54.000 | 38 | banyak varian dataset memakai citra daun terkontrol | Lebih mudah, tetapi perlu migrasi notebook penuh dan audit lisensi/source secara rapi. |

## Dampak ke Submission

EuroSAT tetap dipilih karena saat ini submission sudah rapi, reproducible, bebas data leakage, dan memenuhi seluruh kriteria wajib. Risiko bintang 5 yang masih tersisa dicatat secara jujur di `FINAL_AUDIT.md` dan `MODEL_SUMMARY.md`.
