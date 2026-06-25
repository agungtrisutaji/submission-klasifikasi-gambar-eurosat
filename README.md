# Open Images IT Asset Classification

Repository ini berisi submission Dicoding **Proyek Klasifikasi Gambar** untuk klasifikasi aset IT menggunakan **Open Images V7 detection crops**.

Notebook utama:

```text
klasifikasi-gambar-it-assets.ipynb
```

Branch revisi ini dibuat dari baseline aman:

```text
experiment/open-images-it-assets
15ff878f4e8d4cd737e4710f069f5593914e7912
```

## Dataset

Dataset berasal dari Open Images V7 label type `detections`. Gambar diperoleh menggunakan script Python di folder `src/`, lalu bounding box objek target di-crop menjadi gambar klasifikasi single-object.

Kelas final diatur di:

```text
configs/openimages_it_assets_classes.json
```

Folder sumber gambar lokal:

```text
dataset/raw/<class_name>/
```

Notebook tidak mengunduh ulang Open Images. Notebook memulai dari satu folder sumber `dataset/raw/<class_name>/`, kemudian membuat split manual reviewer-visible ke:

```text
dataset/submission_split/train/<class_name>/
dataset/submission_split/validation/<class_name>/
dataset/submission_split/test/<class_name>/
```

Rasio split: train 80%, validation 10%, test 10%, seed `42`. Jika metadata `source_image_id` dan `file_hash` tersedia, notebook memakai group split untuk mengurangi risiko leakage dan memeriksa duplicate hash antar split.

## Dataset Acquisition Scripts

Script Open Images yang harus ikut submission ZIP:

```text
src/build_openimages_subset.py
src/audit_openimages_subset.py
src/split_openimages_subset.py
src/audit_openimages_split.py
configs/openimages_it_assets_classes.json
notes/DATASET_ACQUISITION.md
notes/DATASET_LICENSE.md
```

Dataset besar, cache, virtual environment, checkpoint, dan folder `.git` tidak perlu ikut ZIP.

## Model Final

Model final pada notebook revisi adalah satu model:

```text
tf.keras.Sequential
```

Model ini memiliki layer eksplisit di luar backbone:

```text
explicit_conv2d_requirement
explicit_pooling_requirement
```

Model final dilatih dengan `model.fit()` dan callback:

```text
ModelCheckpoint
EarlyStopping
ReduceLROnPlateau
```

Monitor callback memakai validation metric, bukan test metric. Test set hanya dipakai untuk evaluasi final dan inference proof.

## Evaluasi

Notebook menghitung metrik langsung dengan:

```python
train_loss, train_accuracy = model.evaluate(train_eval_ds, verbose=1)
val_loss, val_accuracy = model.evaluate(validation_ds, verbose=1)
test_loss, test_accuracy = model.evaluate(test_ds, verbose=1)
```

Classification report dan confusion matrix dibuat langsung dari:

```python
y_prob = model.predict(test_ds, verbose=1)
```

File JSON/CSV di `outputs/evaluation/` hanya hasil simpan setelah evaluasi langsung selesai, bukan sumber utama metrik.

Current local sequential output sebelum packaging final:

| Metric | Value |
| --- | ---: |
| Train accuracy | 0.9293 |
| Validation accuracy | 0.9275 |
| Test accuracy | 0.9439 |

Target minimal Dicoding 85% terpenuhi pada run-all terbaru. Target bintang 5 95% untuk test accuracy belum aman, sehingga tuning lanjutan perlu dilakukan memakai validation set, bukan test set.

Split terbaru dari notebook:

| Split | Total |
| --- | ---: |
| Train | 11,998 |
| Validation | 1,504 |
| Test | 1,498 |

## Export

Notebook mengekspor model yang sama dengan model final yang dilatih dan dievaluasi:

```text
saved_model/it_asset_classifier/
tflite/it_asset_classifier.tflite
tflite/label.txt
tfjs/it_asset_classifier/model.json
tfjs/it_asset_classifier/group*.bin
tfjs/it_asset_classifier/label.txt
label.txt
```

Notebook juga memvalidasi:

- SavedModel bisa diload;
- TFLite interpreter bisa allocate tensors dan menghasilkan output shape sesuai jumlah kelas;
- TFJS `model.json` dan shard `.bin` tersedia;
- `label.txt`, `tflite/label.txt`, dan `tfjs/it_asset_classifier/label.txt` konsisten.

## Cara Menjalankan

Direkomendasikan memakai environment TensorFlow yang sama dengan notebook final. Di workspace ini, run TensorFlow dilakukan lewat WSL.

```bash
pip install -r requirements.txt
jupyter notebook klasifikasi-gambar-it-assets.ipynb
```

Audit setelah run-all:

```bash
python .agents/skills/dicoding_local_workspace_skills/workspace-scripts/audit_notebook.py klasifikasi-gambar-it-assets.ipynb
python .agents/skills/dicoding_local_workspace_skills/workspace-scripts/validate_tf_exports.py .
```

Run-all notebook dan export validator sudah valid pada revisi ini. ZIP final belum dibuat.
