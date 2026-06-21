# Final ZIP Audit - Open Images IT Assets

| Area | Status | Catatan |
|---|---|---|
| Notebook .ipynb ada | OK | `klasifikasi-gambar-it-assets.ipynb` tersedia. |
| Notebook sudah dijalankan | OK | Semua code cell menyimpan output. |
| Tidak ada output error notebook | OK | Audit notebook tidak menemukan output bertipe `error`. |
| Identitas notebook | WARN | `Nama`, `Email`, dan `ID Dicoding` masih placeholder dan harus diisi manual sebelum submit. |
| requirements.txt ada | OK | `requirements.txt` tersedia dan memuat dependency utama. |
| SavedModel ada | OK | `saved_model/it_asset_classifier/saved_model.pb` dan `variables/` tersedia. |
| TFLite ada | OK | `tflite/it_asset_classifier.tflite` tersedia. |
| TFJS ada | OK | `tfjs/it_asset_classifier/model.json`, shard `.bin`, dan `label.txt` tersedia. |
| Label konsisten | OK | `label.txt`, `tflite/label.txt`, dan `tfjs/it_asset_classifier/label.txt` sama. |
| README ada | OK | `README.md` tersedia. |
| Notes audit ada | OK | Notes dataset/model/final audit tersedia di folder final. |
| Tidak ada dataset/cache/venv/output | OK | Folder final tidak berisi `dataset/`, cache Open Images, `.venv/`, `outputs/`, atau `checkpoints/`. |
| Tidak ada ZIP/RAR di dalam ZIP | OK | Folder final tidak berisi archive nested. |
| Ukuran ZIP dicek | OK | Folder final sekitar 1.136 GB sebelum ZIP; ukuran ZIP dicek setelah kompresi. |
| Risiko reject | WARN | Risiko utama adalah identitas notebook yang masih placeholder dan ukuran ZIP yang besar karena SavedModel, TFLite, dan TFJS ensemble. |

## Validation Summary

- Dataset final: Open Images V7 IT Asset Subset.
- Total crop valid: 15.000.
- Classes: `camera`, `computer_keyboard`, `computer_monitor`, `laptop`, `mobile_phone`.
- Train accuracy: 0.9973.
- Validation accuracy: 0.9554.
- Test accuracy: 0.9579.
- SavedModel status: exported and structurally validated.
- TFLite status: exported and structurally validated.
- TFJS status: exported and structurally validated.
- Final ZIP folder: `submission_it_assets/`.
- Final ZIP file: `submission_it_assets.zip`.

## Remaining Risk

The final archive is expected to be large because it includes all required export formats for a four-backbone ensemble. If the Dicoding upload portal rejects the file size, the next practical options are model distillation, single-backbone retraining, or a smaller export strategy.

Before submitting, replace the notebook placeholders for `Nama`, `Email`, and `ID Dicoding` with the real Dicoding identity.
