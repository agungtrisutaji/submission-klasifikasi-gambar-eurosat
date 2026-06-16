# Final Audit

Tanggal audit: 2026-06-16

## Ringkasan

Repository sudah memiliki notebook utama, dataset lokal hasil preparation, checkpoint training, evaluasi akhir, dan export model utama. Audit ini menemukan bahwa README dan dokumentasi pendukung masih minim, serta bagian evaluasi/export/inference di notebook sebelumnya masih kosong. Bagian tersebut sudah dipatch.

## Struktur Repository

File/folder utama:

```text
AGENTS.md
README.md
requirements.txt
.gitignore
klasifikasi-gambar-eurosat.ipynb
dataset/
notes/
outputs/
saved_model/
tfds_data/
tfjs/
tflite/
```

Folder besar yang tidak perlu masuk git:

```text
dataset/
tfds_data/
outputs/
.venv/
```

Folder export model:

```text
saved_model/
tfjs/
tflite/
```

## Masalah yang Ditemukan

1. `README.md` sebelumnya hanya menjelaskan dataset secara singkat.
2. `notes/DATASET_DECISION.md` dan `notes/SUBMISSION_CHECKLIST.md` masih kosong.
3. `notes/PROJECT_CONTEXT.md` masih menyatakan fase project berhenti di dataset preparation, padahal notebook sudah berisi modelling.
4. Cell notebook untuk evaluasi akhir, export model, dan inference masih kosong.
5. Folder `saved_model/`, `tfjs/`, dan `tflite/` sebelumnya hanya berisi `.gitkeep`.
6. TFJS export belum bisa dibuat di environment lokal karena paket `tensorflowjs` tidak tersedia.

## Validasi yang Dilakukan

- Tidak ada output error tersimpan di notebook.
- `requirements.txt` tidak diubah.
- Dataset audit lokal menunjukkan:
  - total raw images: 27.000;
  - train images: 21.600;
  - validation images: 2.700;
  - test images: 2.700;
  - corrupt images: 0;
  - duplicate files within parts: 0;
  - duplicate files across train/validation/test: 0.
- Evaluasi model dari checkpoint berhasil dijalankan.
- SavedModel berhasil dibuat dan diload ulang.
- TFLite berhasil dibuat dan diload dengan interpreter.

## Hasil Evaluasi Lokal

| Metrik | Nilai |
| --- | ---: |
| Model terpilih | `mobilenetv2_transfer_learning` |
| Best training accuracy | 0.8855 |
| Best validation accuracy | 0.9178 |
| Test accuracy | 0.9148 |
| Test loss | 0.2519 |
| Test samples | 2.700 |

## Status Export

| Format | Status | Lokasi |
| --- | --- | --- |
| SavedModel | Berhasil | `saved_model/eurosat_classifier/` |
| TFLite | Berhasil | `tflite/eurosat_classifier.tflite` |
| Label TFLite | Berhasil | `tflite/label.txt` |
| TFJS | Perlu rerun dengan `tensorflowjs` | `tfjs/` |

## Kesimpulan Audit

Repository sudah jauh lebih siap untuk submission: notebook memiliki alur lengkap, dokumentasi menjelaskan dataset sampai export, dan hasil evaluasi final sudah tersedia. Risiko utama yang masih tersisa adalah export TFJS bila format tersebut diwajibkan oleh instruksi submission yang digunakan.
