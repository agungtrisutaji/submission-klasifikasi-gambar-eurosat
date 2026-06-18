# Model Summary

## Model yang Dicoba

Notebook membandingkan tiga pendekatan:

1. **Baseline CNN**
   - Conv2D + BatchNormalization + ReLU + MaxPooling.
   - Dropout dan GlobalAveragePooling untuk mengurangi overfitting.
   - Normalisasi menggunakan preprocessing MobileNetV2 agar pipeline preprocessing konsisten.

2. **MobileNetV2 Transfer Learning**
   - Base model MobileNetV2 pretrained ImageNet.
   - Base model dibekukan pada training awal.
   - Head klasifikasi disesuaikan untuk 10 kelas EuroSAT RGB.
   - Data augmentation diterapkan melalui layer Keras di dalam model dan hanya aktif pada training.

3. **MobileNetV2 Fine-tuning**
   - Melanjutkan checkpoint transfer learning terbaik.
   - Sebagian layer atas MobileNetV2 dibuka dengan learning rate kecil `1e-5`.
   - BatchNormalization pada base model tetap dibekukan agar training stabil.
   - Callback tetap memakai validation set; test set hanya dipakai setelah checkpoint final dipilih.

## Model Terpilih

Model terpilih:

```text
mobilenetv2_finetuned
```

Alasan:

- Memiliki best validation accuracy tertinggi dibanding baseline dan transfer learning frozen.
- Gap train-validation masih wajar pada run lokal.
- Test accuracy akhir meningkat dibanding transfer learning frozen tanpa memakai test set untuk training atau tuning.

## Training Summary

| Model | Best Epoch | Best Train Accuracy | Best Validation Accuracy | Best Validation Loss | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| MobileNetV2 Fine-tuning | 7 | 0.9329 | 0.9396 | 0.1769 | reasonable_fit |
| MobileNetV2 Transfer Learning | 14 | 0.8884 | 0.9178 | 0.2362 | reasonable_fit |
| Baseline CNN | 11 | 0.8817 | 0.8989 | 0.2969 | reasonable_fit |

## Final Evaluation

Evaluasi akhir dilakukan hanya pada test set setelah model dipilih menggunakan validation set.

| Metrik | Nilai |
| --- | ---: |
| Train accuracy checkpoint | 0.9562 |
| Validation accuracy checkpoint | 0.9396 |
| Test accuracy | 0.9448 |
| Test loss | 0.1753 |
| Test samples | 2.700 |

## Export Summary

Export yang tervalidasi:

```text
saved_model/eurosat_classifier/
tflite/eurosat_classifier.tflite
tflite/label.txt
tfjs/eurosat_classifier/model.json
tfjs/eurosat_classifier/group1-shard*.bin
tfjs/eurosat_classifier/label.txt
```

Validasi prediksi:

- SavedModel prediction shape: `(1, 10)`.
- TFLite prediction shape: `(1, 10)`.
- TFJS output classes: `10`.
- TFJS inference source model max delta terhadap model asli pada mode inference: `0.0`.
- Jumlah probabilitas prediksi mendekati 1.

## Limitasi

- EuroSAT RGB memiliki resolusi asli seragam `64x64x3`, sehingga saran dataset dengan resolusi asli tidak seragam tidak diklaim terpenuhi.
- Target saran bintang 5 `>=95%` untuk test accuracy belum tercapai pada run penuh final; hasil final jujur adalah `0.9448`.
- TFJS export membutuhkan paket `tensorflowjs`; package ini tidak dimasukkan langsung ke `requirements.txt` karena resolver pip menarik `tensorflow-decision-forests` yang bentrok pada Windows/Python 3.12. Torch tetap dipertahankan di `requirements.txt`.
- Model dilatih pada gambar EuroSAT RGB dan belum divalidasi pada citra satelit dari sumber/domain lain.
