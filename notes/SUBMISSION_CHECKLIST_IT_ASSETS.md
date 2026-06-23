# Submission Checklist - IT Assets

- [x] Notebook utama memakai `klasifikasi-gambar-it-assets.ipynb`.
- [x] Proses data dari `src/` dimasukkan ke notebook.
- [x] Dataset berasal dari satu sumber, `dataset/raw`.
- [x] Split train/validation/test dibuat manual dengan seed `42`.
- [x] Rasio split final 12.000/1.500/1.500.
- [x] Test set tidak dipakai untuk training, tuning, early stopping, atau checkpoint selection.
- [x] Dataset audit menyimpan ringkasan ke `outputs/dataset_audit/`.
- [x] Model final adalah `tf.keras.Sequential`.
- [x] Model final memiliki `Conv2D` eksplisit.
- [x] Model final memiliki pooling eksplisit.
- [x] Model dilatih dengan `model.fit`.
- [x] Training memakai callback EarlyStopping, ModelCheckpoint, dan ReduceLROnPlateau.
- [x] Plot accuracy/loss dibuat dari history training.
- [x] Evaluasi train/validation/test dihitung langsung dengan `model.evaluate`.
- [x] Classification report dibuat dari prediksi `test_ds`.
- [x] Confusion matrix dibuat dari prediksi `test_ds`.
- [x] Inference proof tersedia.
- [x] SavedModel tervalidasi.
- [x] TFLite tervalidasi.
- [x] TFJS tervalidasi.
- [x] Notebook sudah dijalankan ulang sampai selesai tanpa error output.

Catatan akurasi: test accuracy final `0.9160`, memenuhi minimum 85% tetapi belum mencapai target internal 95%.
