# Final Audit

Tanggal audit: 2026-06-18

## Ringkasan

Repository sudah memiliki notebook utama, dataset lokal hasil preparation, checkpoint training, evaluasi akhir, dan export model lengkap. Notebook sudah dijalankan ulang dengan kernel `.venv` Python 3.12, lalu export SavedModel, TFLite, dan TFJS divalidasi terhadap file aktual di workspace.

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

1. TFJS pre-built export sempat tidak ada di folder `tfjs/eurosat_classifier/`.
2. Output notebook sempat menyimpan status TFJS `failed` akibat stub `tensorflow_decision_forests` tanpa `__spec__`.
3. `requirements.txt` tetap tidak boleh dipakai untuk menambahkan `tensorflowjs` karena resolver pip dapat menarik dependency yang konflik pada Windows/Python 3.12.

## Validasi yang Dilakukan

- Tidak ada output error tersimpan di notebook.
- `requirements.txt` tidak diubah pada validasi akhir ini.
- Dependency PyTorch CUDA di `requirements.txt` sengaja tetap dipertahankan sesuai kondisi proyek.
- Angka evaluasi dokumentasi sudah disinkronkan dengan output notebook terbaru.
- Output notebook sudah dibersihkan dari path lokal pribadi dan warning yang tidak relevan.
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
- `tfjs/eurosat_classifier/label.txt` sama persis dengan `tflite/label.txt`.

## Hasil Evaluasi Lokal

| Metrik | Nilai |
| --- | ---: |
| Model terpilih | `mobilenetv2_transfer_learning` |
| Best training accuracy | 0.8855 |
| Best validation accuracy | 0.9178 |
| Test accuracy | 0.9196 |
| Test loss | 0.2490 |
| Test samples | 2.700 |

## Status Export

| Format | Status | Lokasi |
| --- | --- | --- |
| SavedModel | Berhasil | `saved_model/eurosat_classifier/` |
| TFLite | Berhasil | `tflite/eurosat_classifier.tflite` |
| Label TFLite | Berhasil | `tflite/label.txt` |
| TFJS | Berhasil | `tfjs/eurosat_classifier/` |

## Kesimpulan Audit

Repository sudah siap untuk submission dari sisi export model utama: notebook memiliki alur lengkap, dokumentasi menjelaskan dataset sampai export, hasil evaluasi final tersedia, output notebook sudah dibersihkan, dan export SavedModel/TFLite/TFJS sudah ada. Risiko utama yang tersisa adalah dependency runtime TFJS tidak masuk langsung ke `requirements.txt` karena resolver pip menarik `tensorflow-decision-forests` yang bentrok pada Windows/Python 3.12.
