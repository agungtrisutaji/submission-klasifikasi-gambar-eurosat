# Submission Checklist - Open Images IT Assets

## Wajib / Basic

- [x] Dataset minimal 1,000 gambar.
- [x] Dataset source Open Images V7 tersedia di `dataset/raw/<class_name>/`.
- [x] Minimal 3 kelas; dataset final memiliki 5 kelas.
- [x] Notebook membuat split manual train/validation/test ke `dataset/submission_split/`.
- [x] Notebook load dataset dari hasil split manual dengan `image_dataset_from_directory`.
- [x] Model final menggunakan `tf.keras.Sequential`.
- [x] Model final memiliki `Conv2D` eksplisit bernama `explicit_conv2d_requirement`.
- [x] Model final memiliki pooling eksplisit bernama `explicit_pooling_requirement`.
- [x] Model final memiliki cell `model.fit()`.
- [x] Notebook memiliki plot accuracy/loss dari `history`.
- [x] Notebook memiliki callback `ModelCheckpoint`, `EarlyStopping`, dan `ReduceLROnPlateau`.
- [x] Notebook memiliki sample inference.
- [x] Notebook memiliki cell export SavedModel.
- [x] Notebook memiliki cell export TFLite.
- [x] Notebook memiliki cell export TFJS.
- [x] Notebook run-all terbaru selesai tanpa error.

## Evaluasi Langsung

- [x] Train accuracy dihitung dengan `model.evaluate(train_eval_ds)`.
- [x] Validation accuracy dihitung dengan `model.evaluate(validation_ds)`.
- [x] Test accuracy dihitung dengan `model.evaluate(test_ds)`.
- [x] Classification report dibuat dari `model.predict(test_ds)`.
- [x] Confusion matrix dibuat dari `model.predict(test_ds)`.
- [x] JSON/CSV evaluasi hanya disimpan setelah direct evaluation.

## Dataset Acquisition

- [x] `src/build_openimages_subset.py`
- [x] `src/audit_openimages_subset.py`
- [x] `src/split_openimages_subset.py`
- [x] `src/audit_openimages_split.py`
- [x] `configs/openimages_it_assets_classes.json`
- [x] `notes/DATASET_LICENSE.md`
- [x] `notes/DATASET_ACQUISITION.md`

## Advanced / Bintang 5

- [x] Dataset minimal 10,000 gambar/crop.
- [x] Dataset memiliki 5 kelas.
- [x] Notebook memeriksa corrupt image count.
- [x] Notebook memeriksa duplicate hash antar split.
- [x] Test set tidak dipakai untuk training, tuning, callback, checkpoint selection, atau model selection.
- [ ] Test accuracy direct evaluation >= 95% pada run-all terbaru.
- [x] SavedModel valid pada run-all terbaru.
- [x] TFLite valid pada run-all terbaru.
- [x] TFJS valid pada run-all terbaru.

## Risiko Reject

- [x] Notebook run-all terbaru sudah selesai tanpa error.
- [ ] Target bintang 5 95% untuk test accuracy belum aman pada output sequential lokal terakhir.
- [ ] ZIP final belum dibuat dan belum diaudit.
- [ ] Jangan masukkan dataset/cache/.venv/checkpoint/.git/nested archive ke ZIP.

## Final Check Sebelum ZIP

- [x] Jalankan notebook dari atas ke bawah.
- [x] Jalankan `audit_notebook.py`.
- [x] Jalankan `validate_tf_exports.py`.
- [ ] Hapus helper sementara seperti `tmp_write_it_asset_notebook.py`.
- [ ] Audit isi ZIP sebelum upload.
