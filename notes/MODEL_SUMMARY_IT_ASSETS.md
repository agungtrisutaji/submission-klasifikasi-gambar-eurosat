# Model Summary - IT Assets

Notebook final: `klasifikasi-gambar-it-assets.ipynb`

Runtime final:

- TensorFlow 2.21.0
- GPU terdeteksi: `/physical_device:GPU:0`
- Mixed precision dipakai saat training
- Model evaluasi/export dibuat ulang sebagai clone `float32`

Model final adalah `tf.keras.Sequential`:

```text
Input 160x160x3
EfficientNetV2B0 include_preprocessing=True
Conv2D explicit_conv2d_requirement
MaxPooling2D explicit_pooling_requirement
GlobalAveragePooling2D
Dropout
Dense
Dropout
Dense softmax 5 kelas
```

Data augmentation berada di model training saja. Setelah training/checkpoint dimuat, notebook membuat clone evaluasi/export tanpa augmentation layer agar SavedModel, TFLite, dan TFJS memakai graph inferensi yang sama.

Metrik final dari `model.evaluate`:

| Split | Accuracy | Loss |
| --- | ---: | ---: |
| Train | 0.9532 | 0.1860 |
| Validation | 0.9427 | 0.2678 |
| Test | 0.9160 | 0.4016 |

Status:

- Minimum Dicoding 85%: terpenuhi.
- Target internal 95%: belum terpenuhi oleh model Sequential final.
- Test set tidak dipakai untuk training, tuning, checkpoint selection, atau early stopping.
