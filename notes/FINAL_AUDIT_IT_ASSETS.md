# Final Audit - IT Assets

Audit ini berdasarkan run final notebook `klasifikasi-gambar-it-assets.ipynb` pada GPU WSL2.

## Dataset

| Item | Hasil |
| --- | ---: |
| Total source image/crop | 15.000 |
| Kelas | 5 |
| Train | 12.000 |
| Validation | 1.500 |
| Test | 1.500 |
| Duplicate file hash | 2 |
| Cross-split duplicate hash | 0 |
| Corrupt image | 0 |
| Unique crop resolutions | 14.168 |

Split dibuat manual dari sumber tunggal `dataset/raw` dan metadata `dataset/metadata/openimages_crop_metadata.csv`. Proses dari `src/build_openimages_subset.py`, `src/audit_openimages_subset.py`, `src/split_openimages_subset.py`, dan `src/audit_openimages_split.py` sudah diringkas dan dijalankan ulang di notebook.

## Model dan Evaluasi

| Kriteria | Status |
| --- | --- |
| `tf.keras.Sequential` | Terpenuhi |
| Ada `Conv2D` eksplisit | Terpenuhi |
| Ada pooling eksplisit | Terpenuhi |
| Training dengan `model.fit` | Terpenuhi |
| Callback EarlyStopping | Terpenuhi |
| Callback ModelCheckpoint | Terpenuhi untuk clean run; resume lokal tidak overwrite checkpoint |
| Callback ReduceLROnPlateau | Terpenuhi |
| Plot training history | Terpenuhi |
| Evaluasi langsung `model.evaluate(test_ds)` | Terpenuhi |
| Classification report dari `test_ds` | Terpenuhi |
| Confusion matrix dari `test_ds` | Terpenuhi |
| Inference proof | Terpenuhi |

Metrik final:

```json
{
  "train_accuracy": 0.953166663646698,
  "validation_accuracy": 0.9426666498184204,
  "test_accuracy": 0.9160000085830688,
  "minimum_required_accuracy": 0.85,
  "meets_minimum_test_accuracy": true,
  "meets_target_test_accuracy": false
}
```

## Export

| Export | Status |
| --- | --- |
| SavedModel | exported_and_validated |
| TFLite | exported_and_validated |
| TFJS | exported_and_validated |

Export final berasal dari clone `float32` model evaluasi yang sama, tanpa augmentation training-only.
