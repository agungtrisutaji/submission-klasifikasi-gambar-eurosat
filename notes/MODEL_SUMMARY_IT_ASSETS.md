# Model Summary - Open Images IT Assets

## Dataset

Model final memakai Open Images V7 IT Asset Subset berbasis crop bounding box.

| Item | Value |
| --- | ---: |
| Total crop source | 15,000 |
| Classes | 5 |
| Crop per class | 3,000 |
| Split ratio | 80/10/10 |
| Seed | 42 |
| Train crop | 11,998 |
| Validation crop | 1,504 |
| Test crop | 1,498 |

Kelas final:

- `camera`
- `computer_keyboard`
- `computer_monitor`
- `laptop`
- `mobile_phone`

Notebook memulai dari `dataset/raw/<class_name>/` dan membangun ulang split manual ke `dataset/submission_split/train|validation|test/<class_name>/`.

## Architecture

Model final reviewer-visible adalah `tf.keras.Sequential`.

Struktur utama:

```text
Input
data_augmentation
EfficientNetV2B0 feature extractor
Conv2D(name="explicit_conv2d_requirement")
MaxPooling2D(name="explicit_pooling_requirement")
GlobalAveragePooling2D
Dropout
Dense
Dropout
Dense softmax
```

Layer `Conv2D` dan pooling eksplisit berada di luar pretrained backbone agar terlihat jelas memenuhi feedback reviewer.

## Training

Model final dilatih dengan `model.fit()` pada notebook utama.

Callback:

- `ModelCheckpoint`
- `EarlyStopping`
- `ReduceLROnPlateau`

Checkpoint dan early stopping memonitor validation metric. Test set tidak dipakai untuk training, tuning, callback, checkpoint selection, atau model selection.

## Direct Evaluation

Notebook menghitung evaluasi langsung dengan:

```python
model.evaluate(train_eval_ds)
model.evaluate(validation_ds)
model.evaluate(test_ds)
```

Current local sequential output sebelum packaging final:

| Metric | Value |
| --- | ---: |
| Train accuracy | 0.9293 |
| Validation accuracy | 0.9275 |
| Test accuracy | 0.9439 |

Target minimal Dicoding 85% terpenuhi. Target bintang 5 95% untuk test accuracy belum aman pada run-all terbaru.

## Report and Export

Classification report dan confusion matrix dibuat langsung dari `model.predict(test_ds)`, kemudian disimpan ke `outputs/evaluation/`.

Export dibuat dari model final yang sama:

```text
saved_model/it_asset_classifier/
tflite/it_asset_classifier.tflite
tfjs/it_asset_classifier/
label.txt
```

Label file root, TFLite, dan TFJS harus konsisten.

Run-all terbaru memvalidasi SavedModel, TFLite, dan TFJS dari model final yang sama.
