# Model Summary - Open Images IT Assets

## Dataset

Model final dilatih pada Open Images V7 IT Asset Subset berbasis crop bounding box.

| Item | Value |
| --- | ---: |
| Total crop | 15.000 |
| Classes | 5 |
| Crop per class | 3.000 |
| Train crop | 12.002 |
| Validation crop | 1.502 |
| Test crop | 1.496 |
| Unique crop resolutions | 14.168 |

Kelas final:

- `camera`
- `computer_keyboard`
- `computer_monitor`
- `laptop`
- `mobile_phone`

## Architecture

Notebook tetap menyertakan baseline Sequential CNN dengan `Conv2D`, `MaxPooling2D`, dan `GlobalAveragePooling2D` untuk memenuhi requirement baseline yang mudah dibaca.

Model final yang mencapai target akurasi adalah ensemble:

```text
EfficientNetV2B1 + EfficientNetV2B2 + EfficientNetV2B3 + ConvNeXtTiny
```

Inference final memakai horizontal-flip test-time augmentation. TTA dimasukkan ke graph Keras sebelum export sehingga SavedModel dan TFLite menghasilkan perilaku yang sama dengan evaluasi lokal.

## Selection Rule

Model dipilih berdasarkan validation accuracy tertinggi dari kandidat ensemble 15k. Test set tidak dipakai untuk memilih model.

Top validation candidate:

| Members | Validation accuracy |
| --- | ---: |
| EfficientNetV2B1 + EfficientNetV2B2 + EfficientNetV2B3 + ConvNeXtTiny | 0.9554 |

## Final Metrics

| Metric | Value |
| --- | ---: |
| Train accuracy | 0.9973 |
| Validation accuracy | 0.9554 |
| Test accuracy | 0.9579 |

Semua target accuracy 95% terpenuhi pada run lokal ini.

## Export Validation

| Export | Status | Notes |
| --- | --- | --- |
| SavedModel | exported_and_validated | shape `[1, 5]`, prediction sum `1.0` |
| TFLite | exported_and_validated | shape `[1, 5]`, prediction sum `1.0` |
| TFJS | exported_and_validated | 5 output classes |

Label files match:

```text
label.txt
tflite/label.txt
tfjs/it_asset_classifier/label.txt
```

## Risks

- Artifact export sangat besar karena memakai ensemble empat backbone.
- TFLite dan SavedModel melewati batas ukuran file GitHub normal jika dipush tanpa Git LFS; artefak IT Asset dibiarkan lokal/ignored untuk push biasa.
- TensorFlow native Windows berjalan di CPU pada environment ini. PyTorch CUDA tersedia, tetapi pipeline akhir memakai TensorFlow/Keras untuk kompatibilitas export Dicoding.
