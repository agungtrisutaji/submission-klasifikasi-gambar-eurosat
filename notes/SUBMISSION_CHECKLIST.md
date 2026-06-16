# Submission Checklist

## Struktur File

- [x] `README.md` menjelaskan tujuan, dataset, split, metode, hasil, export, dan cara menjalankan notebook.
- [x] `requirements.txt` tetap tidak diubah.
- [x] Notebook utama tetap `klasifikasi-gambar-eurosat.ipynb`.
- [x] Path notebook relatif terhadap root repository.
- [x] Dataset besar tidak masuk git.
- [x] Folder output run tidak masuk git.

## Dataset

- [x] Dataset EuroSAT RGB digunakan.
- [x] Dataset dimuat melalui TensorFlow Datasets.
- [x] Total gambar divalidasi: 27.000.
- [x] Jumlah kelas divalidasi: 10.
- [x] Nama kelas diambil dari metadata TFDS.
- [x] Split train/validation/test dibuat 80/10/10.
- [x] Split dibuat stratified per kelas.
- [x] Seed reproducibility: 42.
- [x] Distribusi data sebelum dan sesudah split diaudit.
- [x] Corrupt image dicek.
- [x] Duplicate image dicek.
- [x] Duplicate antar split dicek.

## Modelling

- [x] Preprocessing gambar tersedia.
- [x] Data augmentation hanya digunakan pada training flow.
- [x] Baseline CNN tersedia.
- [x] Improved model berbasis MobileNetV2 transfer learning tersedia.
- [x] Callback EarlyStopping tersedia.
- [x] Callback ModelCheckpoint tersedia.
- [x] Callback ReduceLROnPlateau tersedia.
- [x] Training accuracy/loss dan validation accuracy/loss dicatat.

## Evaluation

- [x] Model dipilih berdasarkan validation set.
- [x] Test set tidak dipakai untuk training/tuning.
- [x] Test accuracy dihitung.
- [x] Test loss dihitung.
- [x] Confusion matrix dibuat.
- [x] Classification report dibuat.
- [x] Sample inference dibuat.
- [x] Kesimpulan performa model tersedia di notebook.

## Export

- [x] SavedModel berhasil dibuat.
- [x] SavedModel berhasil diload ulang untuk validasi prediksi.
- [x] TFLite berhasil dibuat.
- [x] TFLite berhasil diload dengan interpreter untuk validasi prediksi.
- [ ] TFJS berhasil dibuat.

Catatan TFJS: cell export TFJS tersedia, tetapi run lokal terakhir melewati export TFJS karena paket `tensorflowjs` tidak tersedia dan `requirements.txt` tidak boleh diubah.

## Sebelum ZIP

- [ ] Jalankan notebook dari atas ke bawah di environment final.
- [ ] Jika format TFJS wajib, install `tensorflowjs` di environment eksekusi lalu jalankan ulang cell **Konversi Model**.
- [ ] Pastikan folder model export yang diwajibkan Dicoding ikut masuk ZIP.
- [ ] Jangan masukkan `.venv/`, `dataset/`, `tfds_data/`, atau `outputs/` bila tidak diminta.
- [ ] Jangan membuat ZIP di dalam ZIP.
