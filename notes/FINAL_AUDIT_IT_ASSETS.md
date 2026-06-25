# Final Audit - Open Images IT Assets

## Audit Summary

| Area | Status | Catatan |
|---|---:|---|
| Instruksi wajib | OK | Notebook run-all terbaru menampilkan source data, split manual, Sequential final, training, evaluasi langsung, report, export, dan inference. |
| Kriteria tambahan | WARNING | Dataset 15,000 crop dan 5 kelas tersedia. Target minimal 85% tercapai; target bintang 5 95% untuk test accuracy belum aman. |
| Struktur folder | OK | Script Open Images, config, notebook, notes, dan export path tersedia di workspace. |
| Notebook/script berjalan | OK | `audit_notebook.py` menemukan 0 unrun cell, 0 output error, dan 0 warning. |
| Dataset benar | OK | Dataset berasal dari Open Images V7 detection crops dan notebook memulai dari `dataset/raw/<class_name>/`. |
| Model/evaluasi benar | OK | Notebook memakai final `tf.keras.Sequential` dengan Conv2D/pooling eksplisit dan evaluasi langsung dari `model.evaluate(...)`. |
| README lengkap | OK | README menjelaskan acquisition, split manual, model final, evaluasi langsung, export, dan guardrail ZIP. |
| requirements.txt lengkap | OK | Run-all dilakukan di WSL Python 3.12, TensorFlow 2.19.0, GPU terdeteksi. |
| ZIP final benar | WARNING | ZIP belum boleh dibuat sebelum notebook run-all dan export validator valid. |
| Risiko reject | WARNING | Risiko utama: ZIP belum dibuat/audit, helper sementara harus dihapus, dan test accuracy sequential belum mencapai 95%. |

## Reviewer Feedback Mapping

| Feedback | Status | Evidence |
| --- | ---: | --- |
| Split train/validation/test terlihat di notebook | Prepared | Notebook membuat `dataset/submission_split/...` dari `dataset/raw/...` dengan seed 42. |
| Script Open Images ikut submission | Prepared | Script ada di `src/` dan dicatat di `notes/DATASET_ACQUISITION.md`. |
| Model final `tf.keras.Sequential` | Prepared | Cell model membuat `model = tf.keras.Sequential(...)`. |
| Conv2D eksplisit | Prepared | Layer bernama `explicit_conv2d_requirement`. |
| Pooling eksplisit | Prepared | Layer bernama `explicit_pooling_requirement`. |
| `model.fit()` dijalankan | OK | Notebook run-all terbaru memiliki output training. |
| Test accuracy dari `model.evaluate(test_ds)` | OK | Test accuracy terbaru 0.9439. |
| Tidak memakai JSON/CSV lama sebagai sumber metrik | Prepared | JSON/CSV hanya disimpan setelah evaluasi langsung. |
| Report dari `test_ds` langsung | OK | Cell report memakai `model.predict(test_ds)` dan notebook sudah run-all. |
| Export dari model yang sama | OK | Export summary terbaru valid untuk SavedModel, TFLite, dan TFJS. |

## Current Known Sequential Output

Output lokal sequential dari run-all terbaru:

| Metric | Value |
| --- | ---: |
| Train accuracy | 0.9293 |
| Validation accuracy | 0.9275 |
| Test accuracy | 0.9439 |

Keputusan: cukup untuk target minimal Dicoding 85%, belum aman untuk target bintang 5 95%.

## Dataset Audit

| Check | Result |
| --- | ---: |
| Total source images | 15,000 |
| Train images | 11,998 |
| Validation images | 1,504 |
| Test images | 1,498 |
| Corrupt image count | 0 |
| Cross-split duplicate hash count | 0 |
| Source image leakage across split | 0 |
| Unique resolutions | 14,168 |
| Ready for modelling | true |

## Export Audit

`validate_tf_exports.py .` result: OK.

| Export | Status |
| --- | --- |
| SavedModel | exported_and_validated |
| TFLite | exported_and_validated |
| TFJS | exported_and_validated |
| Label consistency | true |

## Before ZIP

Wajib jalankan:

```bash
python .agents/skills/dicoding_local_workspace_skills/workspace-scripts/audit_notebook.py klasifikasi-gambar-it-assets.ipynb
python .agents/skills/dicoding_local_workspace_skills/workspace-scripts/validate_tf_exports.py .
```

ZIP final boleh menjadi langkah berikutnya, tetapi harus dibuat dan diaudit terpisah agar folder besar/cache tidak ikut masuk.
