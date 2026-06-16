# Final Audit

Tanggal audit: 2026-06-16

## Ringkasan

Repository sudah memiliki notebook utama, dataset lokal hasil preparation, checkpoint training, evaluasi akhir, dan export model lengkap. Audit ini menemukan bahwa README dan dokumentasi pendukung masih minim, bagian evaluasi/export/inference di notebook sebelumnya masih kosong, dan TFJS belum tersedia. Bagian tersebut sudah dipatch.

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
6. TFJS export awalnya belum bisa dibuat di environment lokal karena paket `tensorflowjs` belum tersedia.

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
- TFJS berhasil dibuat ke `tfjs/eurosat_classifier/`.
- TFJS `model.json` valid JSON.
- TFJS shard `group1-shard*.bin` tersedia.
- TFJS `label.txt` sama dengan `tflite/label.txt`.
- TFJS output signature menunjukkan 10 kelas.

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
| TFJS | Berhasil | `tfjs/eurosat_classifier/` |

## Kesimpulan Audit

Repository sudah siap untuk submission dari sisi export model utama: notebook memiliki alur lengkap, dokumentasi menjelaskan dataset sampai export, hasil evaluasi final tersedia, dan export SavedModel/TFLite/TFJS sudah ada. Risiko utama yang tersisa adalah dependency runtime TFJS tidak masuk langsung ke `requirements.txt` karena resolver pip menarik `tensorflow-decision-forests` yang bentrok pada Windows/Python 3.12.
