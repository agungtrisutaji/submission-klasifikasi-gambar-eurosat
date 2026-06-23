# Open Images IT Asset Classification

Submission Dicoding **Belajar Fundamental Deep Learning** untuk klasifikasi gambar aset IT berbasis **Open Images V7 IT Asset Subset**.

Notebook utama:

```text
klasifikasi-gambar-it-assets.ipynb
```

## Status Final

Notebook sudah dijalankan ulang secara lokal dengan TensorFlow GPU di WSL2. Guard `REQUIRE_GPU=1` aktif, sehingga notebook berhenti jika TensorFlow tidak mendeteksi GPU.

| Item | Hasil |
| --- | ---: |
| TensorFlow runtime | 2.21.0 |
| GPU runtime | `/physical_device:GPU:0` |
| Total gambar sumber | 15.000 |
| Jumlah kelas | 5 |
| Split | train/validation/test = 12.000/1.500/1.500 |
| Corrupt image | 0 |
| Cross-split duplicate hash | 0 |
| Train accuracy | 0.9532 |
| Validation accuracy | 0.9427 |
| Test accuracy | 0.9160 |
| Minimum Dicoding 85% | Terpenuhi |

Target internal 95% belum tercapai oleh model final Sequential ini, sehingga README tidak mengklaim 95%. Hasil yang dipakai adalah evaluasi langsung dari `model.evaluate(test_ds)`.

## Dataset

Dataset dibuat dari Open Images V7 detection crops untuk 5 kelas:

| Label | Jumlah crop |
| --- | ---: |
| `camera` | 3.000 |
| `computer_keyboard` | 3.000 |
| `computer_monitor` | 3.000 |
| `laptop` | 3.000 |
| `mobile_phone` | 3.000 |

Sumber tunggal data adalah:

```text
dataset/raw/<class_name>/
dataset/metadata/openimages_crop_metadata.csv
configs/openimages_it_assets_classes.json
```

Notebook memuat ulang proses data yang sebelumnya berada di `src/`:

```text
src/build_openimages_subset.py
src/audit_openimages_subset.py
src/split_openimages_subset.py
src/audit_openimages_split.py
```

Split manual dibuat dari metadata sumber tunggal dengan seed `42`, rasio 80/10/10, grouping `source_image_id`, dan guard `file_hash` untuk mencegah duplikat lintas split.

## Model

Model final adalah `tf.keras.Sequential` yang benar-benar dilatih dengan `model.fit`.

Arsitektur ringkas:

```text
Input 160x160x3
EfficientNetV2B0 feature extractor
Conv2D eksplisit
MaxPooling2D eksplisit
GlobalAveragePooling2D
Dense head
Softmax 5 kelas
```

Data augmentation hanya dipakai saat training. Untuk evaluasi dan export, notebook membuat clone `float32` tanpa layer augmentation agar SavedModel, TFLite, dan TFJS berasal dari model evaluasi yang sama dan bisa divalidasi ulang.

## Output Evaluasi

File hasil evaluasi final:

```text
outputs/evaluation/sequential_direct_eval.json
outputs/evaluation/sequential_classification_report.csv
outputs/evaluation/sequential_confusion_matrix.csv
outputs/evaluation/sequential_accuracy_plot.png
outputs/evaluation/sequential_loss_plot.png
outputs/evaluation/sample_inference.csv
outputs/evaluation/sample_inference.png
```

## Export Model

Export final:

```text
saved_model/it_asset_classifier/
tflite/it_asset_classifier.tflite
tfjs/it_asset_classifier/
label.txt
tflite/label.txt
tfjs/it_asset_classifier/label.txt
```

Validasi export:

| Export | Status |
| --- | --- |
| SavedModel | exported_and_validated |
| TFLite | exported_and_validated |
| TFJS | exported_and_validated |

## Menjalankan Notebook

Untuk lokal Windows, TensorFlow GPU native Windows tidak tersedia pada TensorFlow modern. Jalankan notebook di WSL2 atau Google Colab GPU.

Contoh environment lokal yang dipakai untuk run final:

```bash
export REQUIRE_GPU=1
export REUSE_EXISTING_WEIGHTS=1
export REUSE_EXISTING_SPLIT=1
```

Di Google Colab, aktifkan runtime GPU terlebih dahulu, lalu jalankan notebook dari atas. Jika dataset dan checkpoint belum tersedia, notebook akan membuat split dan training penuh dari awal.

## Submission

Folder dan ZIP submission final:

```text
submission_it_assets/
submission_it_assets.zip
```

Dataset/cache besar tidak dimasukkan ke Git. Artefak besar untuk submission disimpan di folder/ZIP lokal.
