# Final Audit

Tanggal audit: 2026-06-18

## Ringkasan

Repository sudah memiliki notebook utama, dataset lokal hasil preparation, checkpoint training, evaluasi akhir, dan export model lengkap. Model final memakai EuroSAT RGB dengan MobileNetV2 fine-tuning. Export SavedModel, TFLite, dan TFJS sudah diregenerasi dari checkpoint fine-tuned serta divalidasi terhadap file aktual di workspace.

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
4. EuroSAT RGB memiliki resolusi asli seragam `64x64x3`, sehingga saran bintang 5 tentang resolusi asli tidak seragam tidak diklaim terpenuhi.

## Validasi yang Dilakukan

- Tidak ada output error tersimpan di notebook.
- `requirements.txt` tidak diubah pada validasi akhir ini.
- Dependency PyTorch CUDA di `requirements.txt` sengaja tetap dipertahankan sesuai kondisi proyek.
- Angka evaluasi dokumentasi sudah disinkronkan dengan output notebook terbaru.
- Output notebook sudah dibersihkan dari path lokal pribadi dan warning yang tidak relevan.
- Model fine-tuned dipilih memakai validation accuracy; test set hanya digunakan untuk evaluasi final dan inference proof.
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
| Model terpilih | `mobilenetv2_finetuned` |
| Train accuracy checkpoint | 0.9562 |
| Validation accuracy checkpoint | 0.9396 |
| Test accuracy | 0.9448 |
| Test loss | 0.1753 |
| Test samples | 2.700 |

## Status Export

| Format | Status | Lokasi |
| --- | --- | --- |
| SavedModel | Berhasil | `saved_model/eurosat_classifier/` |
| TFLite | Berhasil | `tflite/eurosat_classifier.tflite` |
| Label TFLite | Berhasil | `tflite/label.txt` |
| TFJS | Berhasil | `tfjs/eurosat_classifier/` |

## Kesimpulan Audit

Repository sudah siap untuk submission dari sisi kriteria wajib: notebook memiliki alur lengkap, dokumentasi menjelaskan dataset sampai export, hasil evaluasi final tersedia, output notebook sudah dibersihkan, dan export SavedModel/TFLite/TFJS sudah ada. Risiko utama untuk bintang 5 adalah test accuracy run penuh final `0.9448`, masih sedikit di bawah saran 95%, serta EuroSAT RGB memiliki resolusi asli seragam.
