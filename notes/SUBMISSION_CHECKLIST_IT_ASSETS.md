# Submission Checklist - Open Images IT Assets

## Wajib / Basic

- [x] Dataset minimal 1.000 gambar.
- [x] Dataset final 15.000 crop.
- [x] Minimal 3 kelas; dataset final memiliki 5 kelas.
- [x] Ada train/validation/test split.
- [x] Notebook memakai dataset lokal `dataset/train`, `dataset/validation`, dan `dataset/test`.
- [x] Model baseline menggunakan `Sequential`.
- [x] Model baseline menggunakan `Conv2D`.
- [x] Model baseline menggunakan pooling layer.
- [x] Train accuracy lebih dari 85%.
- [x] Test accuracy lebih dari 85%.
- [x] Ada plot accuracy dan loss.
- [x] Ada callback.
- [x] Ada sample inference.
- [x] Export SavedModel.
- [x] Export TFLite.
- [x] Export TFJS.

## Tambahan / Skilled

- [x] Dataset bukan dataset latihan Dicoding.
- [x] Dataset minimal 10.000 gambar/crop.
- [x] Split menjaga `source_image_id` agar tidak bocor antar split.
- [x] Source image leakage antar split 0.
- [x] Duplicate hash antar split 0.
- [x] Corrupt image count 0.
- [x] Metadata crop dan metadata split tersimpan.
- [x] Class names konsisten untuk model, TFLite labels, dan TFJS labels.
- [x] Classification report tersedia.
- [x] Confusion matrix tersedia.

## Advanced / Bintang 5

- [x] Dataset memiliki resolusi asli/crop tidak seragam.
- [x] Train accuracy lebih dari 95%.
- [x] Validation accuracy lebih dari 95%.
- [x] Test accuracy lebih dari 95%.
- [x] Model selection berdasarkan validation set.
- [x] Test set tidak dipakai untuk training, tuning, callback, checkpoint selection, atau model selection.
- [x] SavedModel divalidasi reload/inference.
- [x] TFLite divalidasi dengan interpreter.
- [x] TFJS divalidasi melalui `model.json`, output class, dan label file.

## Risiko Reject

- [ ] Ukuran export final perlu dicek terhadap batas submission/hosting.
- [ ] Jika harus push artefak model ke GitHub, gunakan Git LFS atau model lebih kecil.
- [ ] Duplicate hash within-train berjumlah 2 dapat dibersihkan untuk polishing, meskipun tidak menyebabkan leakage antar split.
- [ ] ZIP final belum dibuat pada tugas ini.

## Bukti yang Harus Disertakan

- [x] `outputs/evaluation/15k_ensemble_eval.json`
- [x] `outputs/evaluation/15k_classification_report.csv`
- [x] `outputs/evaluation/15k_confusion_matrix.csv`
- [x] `outputs/export/it_asset_export_summary.json`
- [x] `notes/MODEL_SUMMARY_IT_ASSETS.md`
- [x] `notes/FINAL_AUDIT_IT_ASSETS.md`

## Final Check Sebelum ZIP

- [ ] Jalankan notebook dari atas ke bawah jika ingin output cell final tersimpan ulang.
- [ ] Pastikan `dataset/`, `openimages_data/`, `fiftyone/`, `outputs/`, `.venv/`, `checkpoints/`, dan archive sementara tidak masuk ZIP.
- [ ] Pastikan export model final yang wajib ada tetap ikut ZIP lokal, meskipun tidak ikut push Git biasa.
- [ ] Pastikan ukuran ZIP masih masuk batas upload Dicoding.
- [ ] Pastikan README tidak lagi membingungkan EuroSAT baseline dengan Open Images final.
