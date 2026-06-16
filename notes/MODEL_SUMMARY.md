# Model Summary

## Model yang Dicoba

Notebook membandingkan dua pendekatan:

1. **Baseline CNN**
   - Conv2D + BatchNormalization + ReLU + MaxPooling.
   - Dropout dan GlobalAveragePooling untuk mengurangi overfitting.
   - Normalisasi menggunakan preprocessing MobileNetV2 agar pipeline preprocessing konsisten.

2. **MobileNetV2 Transfer Learning**
   - Base model MobileNetV2 pretrained ImageNet.
   - Base model dibekukan pada training awal.
   - Head klasifikasi disesuaikan untuk 10 kelas EuroSAT RGB.
   - Data augmentation diterapkan melalui layer Keras di dalam model dan hanya aktif pada training.

## Model Terpilih

Model terpilih:

```text
mobilenetv2_transfer_learning
```

Alasan:

- Memiliki best validation accuracy tertinggi dibanding baseline.
- Gap train-validation masih wajar pada run lokal.
- Test accuracy akhir masih konsisten dengan validation accuracy.

## Training Summary

| Model | Best Epoch | Best Train Accuracy | Best Validation Accuracy | Best Validation Loss | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| MobileNetV2 Transfer Learning | 11 | 0.8855 | 0.9178 | 0.2421 | reasonable_fit |
| Baseline CNN | 12 | 0.8701 | 0.8667 | 0.3907 | reasonable_fit |

## Final Evaluation

Evaluasi akhir dilakukan hanya pada test set setelah model dipilih menggunakan validation set.

| Metrik | Nilai |
| --- | ---: |
| Test accuracy | 0.9148 |
| Test loss | 0.2519 |
| Test samples | 2.700 |

## Export Summary

Export yang tervalidasi:

```text
saved_model/eurosat_classifier/
tflite/eurosat_classifier.tflite
tflite/label.txt
```

Validasi prediksi:

- SavedModel prediction shape: `(1, 10)`.
- TFLite prediction shape: `(1, 10)`.
- Jumlah probabilitas prediksi mendekati 1.

## Limitasi

- Base MobileNetV2 belum di-fine-tune.
- TFJS export membutuhkan paket `tensorflowjs`; paket tersebut tidak ditambahkan ke `requirements.txt` karena file tersebut sengaja tidak boleh diubah.
- Model dilatih pada gambar EuroSAT RGB dan belum divalidasi pada citra satelit dari sumber/domain lain.
