# Submission Checklist

Current branch summary for `experiment/open-images-it-assets`.

Detailed version: `notes/SUBMISSION_CHECKLIST_IT_ASSETS.md`.

## Dataset

- [x] Dataset minimal 10.000 gambar/crop.
- [x] Dataset memiliki 5 kelas.
- [x] Resolusi crop asli tidak seragam.
- [x] Metadata crop tersimpan.
- [x] Split train/validation/test dibuat.
- [x] Split memakai seed `42`.
- [x] Source image leakage antar split 0.
- [x] Duplicate hash antar split 0.
- [x] Corrupt image count 0.
- [x] Dataset/cache besar tidak masuk git.

## Model dan Evaluasi

- [x] Baseline Sequential CNN tersedia di notebook.
- [x] Transfer learning dipakai untuk model final.
- [x] Data augmentation hanya untuk training.
- [x] Callback digunakan.
- [x] Model selection memakai validation set.
- [x] Test set tidak dipakai untuk tuning.
- [x] Train accuracy lebih dari 95%.
- [x] Validation accuracy lebih dari 95%.
- [x] Test accuracy lebih dari 95%.
- [x] Confusion matrix tersedia.
- [x] Classification report tersedia.
- [x] Inference proof tersedia.

## Export

- [x] SavedModel diexport dan divalidasi.
- [x] TFLite diexport dan divalidasi.
- [x] TFJS diexport dan divalidasi.
- [x] Label files sinkron.

## Remaining Risk

- [ ] Ukuran export ensemble perlu dicek sebelum final ZIP/push.
- [ ] Jika GitHub menolak file besar, gunakan Git LFS atau model lebih kecil.
