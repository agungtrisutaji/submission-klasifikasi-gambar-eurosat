# Dataset Rework Decision

Tanggal: 2026-06-19

## Keputusan

Branch `experiment/open-images-it-assets` memakai **Open Images V7 IT Asset Subset** sebagai dataset final eksperimen.

Keputusan ini menggantikan keputusan lama yang mempertahankan EuroSAT RGB untuk branch stabil. EuroSAT tetap menjadi baseline historis repo utama, tetapi branch eksperimen ini memakai Open Images karena targetnya adalah mengejar saran bintang 5 yang belum terpenuhi oleh EuroSAT, terutama resolusi asli yang tidak seragam dan test accuracy minimal 95%.

## Alasan Teknis

- Dataset final memiliki 15.000 crop valid.
- Ada 5 kelas dengan 3.000 crop per kelas.
- Crop dibuat dari bounding box Open Images V7 detections.
- Resolusi crop asli tidak seragam dengan 14.168 resolusi unik.
- Group split berdasarkan `source_image_id` mencegah leakage antar train/validation/test.
- Audit final menunjukkan corrupt image 0 dan duplicate hash antar split 0.
- Model final mencapai train accuracy 99,73%, validation accuracy 95,54%, dan test accuracy 95,79%.

## Kelas yang Ditolak

| Label lokal | Alasan |
| --- | --- |
| `computer_mouse` | hanya 724 crop valid dari target 2.000 |
| `printer` | hanya 262 crop valid dari target 2.000 |
| `headphones` | hanya 1.241 crop valid dari target 2.000 |

## Dampak ke Submission

Open Images IT Asset Subset dipilih karena branch ini sekarang memenuhi target utama yang belum dicapai EuroSAT pada run sebelumnya. Risiko utama yang tersisa bukan metrik akurasi, tetapi ukuran export model ensemble yang besar.
