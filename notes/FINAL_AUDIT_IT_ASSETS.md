# Final Audit - Open Images IT Assets

## Audit Summary

| Area | Status | Catatan |
|---|---|---|
| Instruksi wajib | ✅ | Notebook memiliki dataset pipeline, baseline Sequential CNN, Conv2D, pooling layer, training, evaluasi, inference, dan export. |
| Kriteria tambahan | ✅ | Dataset 15.000 crop, 5 kelas, resolusi asli tidak seragam, train/test accuracy lebih dari 95%. |
| Struktur folder | ✅ | Dataset lokal berada di `dataset/`, export di `saved_model/`, `tflite/`, dan `tfjs/`. |
| Notebook/script berjalan | ✅ | Notebook JSON valid; script dataset/audit lolos `py_compile`. |
| Dataset benar | ✅ | Open Images V7 IT Asset Subset, split group by `source_image_id`, leakage antar split 0. |
| Model/evaluasi benar | ✅ | Model final dipilih dari validation set; test set hanya untuk evaluasi final. |
| Screenshot/bukti lengkap | ✅ | Notebook menyiapkan plot history, confusion matrix, classification report, dan sample inference. |
| README lengkap | ✅ | README sudah menjelaskan Open Images sebagai dataset final eksperimen dan EuroSAT sebagai baseline historis. |
| requirements.txt lengkap | ✅ | Dependency utama sudah tersedia; TFJS export sudah tervalidasi di environment lokal. |
| ZIP final benar | ⚠️ | ZIP final belum dibuat pada tugas ini. Ukuran artefak perlu dicek sebelum packaging. |
| Risiko reject | ⚠️ | Risiko utama adalah ukuran export ensemble yang besar, bukan metrik akurasi. Artefak IT Asset tidak dipush via Git biasa karena melewati limit GitHub 100 MB. |

## Dataset Audit

Audit split final menggunakan 15.000 crop Open Images V7 IT Asset Subset.

| Check | Result |
| --- | ---: |
| Total crop | 15.000 |
| Minimum total crop target | 10.000 |
| Crop per class target | 3.000 |
| Source image leakage across split | 0 |
| Duplicate file hash across split | 0 |
| Corrupt image count | 0 |
| Missing crop path count | 0 |
| Missing split crop path count | 0 |
| Unique crop resolutions total | 14.168 |
| Ready for modelling | true |

Split:

| Split | Crop | Ratio |
| --- | ---: | ---: |
| Train | 12.002 | 0.8001 |
| Validation | 1.502 | 0.1001 |
| Test | 1.496 | 0.0997 |

Crop per class:

| Class | Crop |
| --- | ---: |
| laptop | 3.000 |
| computer_keyboard | 3.000 |
| mobile_phone | 3.000 |
| computer_monitor | 3.000 |
| camera | 3.000 |

## Warning Reviewed

Audit menemukan 2 duplicate file hash within split, semuanya berada di split `train`. Tidak ada duplicate hash antar split dan tidak ada leakage `source_image_id` antar split.

Keputusan: warning ini tidak memblokir evaluasi final karena tidak menyentuh validation/test leakage. Untuk final polishing, duplicate within-train dapat dibuang dan split dibangun ulang, tetapi hasil saat ini sudah memenuhi guardrail utama anti-leakage.

## Model Audit

Model final:

```text
EfficientNetV2B1 + EfficientNetV2B2 + EfficientNetV2B3 + ConvNeXtTiny
```

| Metric | Result |
| --- | ---: |
| Train accuracy | 0.9973 |
| Validation accuracy | 0.9554 |
| Test accuracy | 0.9579 |

Model selection dilakukan berdasarkan validation accuracy. Test set hanya digunakan untuk evaluasi akhir.

## Export Audit

| Export | Status |
| --- | --- |
| SavedModel | exported_and_validated |
| TFLite | exported_and_validated |
| TFJS | exported_and_validated |

Export paths:

```text
saved_model/it_asset_classifier/
tflite/it_asset_classifier.tflite
tfjs/it_asset_classifier/
```

## Submission Readiness

Secara metrik dan kelengkapan artefak, eksperimen ini memenuhi target utama:

- dataset lebih dari 10.000 gambar;
- 5 kelas;
- resolusi crop asli tidak seragam;
- train accuracy lebih dari 95%;
- test accuracy lebih dari 95%;
- callback digunakan pada training head;
- inference proof disiapkan di notebook;
- SavedModel, TFLite, dan TFJS tersedia.

Risiko tersisa: ukuran export ensemble sangat besar. Sebelum final ZIP, cek batas ukuran submission dan pertimbangkan model distillation atau single-backbone retraining bila ukuran harus diperkecil. Untuk GitHub, gunakan Git LFS atau biarkan artefak export IT Asset tetap lokal karena `saved_model/it_asset_classifier/variables/variables.data-00000-of-00001` dan `tflite/it_asset_classifier.tflite` melewati limit 100 MB.
