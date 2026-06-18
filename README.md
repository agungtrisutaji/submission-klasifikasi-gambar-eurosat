# Submission Klasifikasi Gambar EuroSAT

> Branch eksperimen: `experiment/open-images-it-assets`.
>
> Branch ini sedang menyiapkan migrasi aman dari **EuroSAT RGB** ke **Open Images V7 IT Asset Subset**. Notebook EuroSAT lama tetap dipertahankan sebagai baseline stabil, sedangkan template migrasi awal disiapkan di `klasifikasi-gambar-it-assets.ipynb`. Rencana dataset dan catatan lisensi ada di `notes/OPEN_IMAGES_SUBSET_PLAN.md` dan `notes/DATASET_LICENSE.md`.

Repository ini berisi submission Dicoding untuk proyek klasifikasi gambar pada kelas **Belajar Fundamental Deep Learning**. Tujuannya adalah membangun pipeline image classification yang rapi, reproducible, dan mudah diperiksa reviewer dari tahap dataset sampai export model.

## Eksperimen Open Images IT Asset

Branch `experiment/open-images-it-assets` memiliki builder awal untuk membuat subset eksplorasi kecil dari Open Images V7. Tahap ini hanya memvalidasi download, bounding box, crop objek, metadata, dan audit dataset. Belum ada training dan belum ada export ulang model.

Script yang tersedia:

```text
src/build_openimages_subset.py
src/audit_openimages_subset.py
src/split_openimages_subset.py
src/audit_openimages_split.py
configs/openimages_it_assets_classes.json
```

Feasibility awal dengan kelas `Laptop`, `Computer keyboard`, `Computer mouse`, `Mobile phone`, dan `Printer` sudah dijalankan untuk target 2.000 crop per kelas. Hasilnya belum layak untuk dataset final karena `computer_mouse` hanya mencapai 724 crop dan `printer` hanya mencapai 262 crop dari source split `train`. Dua kelas tersebut tidak dipakai sebagai kandidat final saat ini.

Kombinasi kandidat berikutnya disimpan di class config:

| Open Images class | Label lokal |
| --- | --- |
| Laptop | `laptop` |
| Computer keyboard | `computer_keyboard` |
| Mobile phone | `mobile_phone` |
| Computer monitor | `computer_monitor` |
| Camera | `camera` |

Feasibility pengganti dengan `headphones` juga belum layak karena hanya menghasilkan 1.241 crop dari target 2.000. Config kemudian mengganti `headphones` dengan `camera`, dan feasibility Camera sudah lolos: total 10.000 crop, setiap kelas 2.000 crop, resolusi crop tidak seragam, corrupt image 0, duplicate hash group 0, duplicate across classes 0, blockers kosong, dan `ready_for_full_scale_dataset_build = true`.

Camera replacement combination accepted for final dataset preparation. Next step: create train/validation/test split with group split by `source_image_id`. Jangan training, tuning, atau export model sebelum split dan audit split selesai.

Jalankan builder feasibility kandidat baru dari root repository:

```powershell
.\.venv\Scripts\python.exe src\build_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --target-crops-per-class 2000 --max-samples-per-class 5000 --source-splits train --overwrite
```

Output builder:

```text
dataset/raw/<label_local>/
dataset/metadata/openimages_crop_metadata.csv
```

Jalankan audit:

```powershell
.\.venv\Scripts\python.exe src\audit_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --min-crops-per-class 2000
```

Output audit:

```text
outputs/dataset_audit/openimages_subset_audit.json
outputs/dataset_audit/openimages_resolution_summary.csv
```

Split lokal train/validation/test sudah dibuat dengan group split berdasarkan `source_image_id` untuk mencegah leakage. Hasil audit split:

| Split | Total |
| --- | ---: |
| Train | 8.006 |
| Validation | 994 |
| Test | 1.000 |

Source image leakage across split `0`, duplicate hash across split `0`, corrupt image count `0`, missing split crop file count `0`, dan `ready_for_modelling = true`.

Command split:

```powershell
.\.venv\Scripts\python.exe src\split_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --metadata-path dataset\metadata\openimages_crop_metadata.csv --raw-dir dataset\raw --split-dir dataset --train-ratio 0.8 --validation-ratio 0.1 --test-ratio 0.1 --seed 42 --overwrite
```

Command audit split:

```powershell
.\.venv\Scripts\python.exe src\audit_openimages_split.py --class-config configs\openimages_it_assets_classes.json
```

Folder `dataset/`, `openimages_data/`, `fiftyone/`, dan `outputs/` di-ignore oleh git. Modelling boleh mulai setelah audit split ini, dengan catatan test set hanya untuk evaluasi final dan tidak boleh dipakai untuk training, tuning, callback, checkpoint selection, atau model selection.

Notebook utama:

```text
klasifikasi-gambar-eurosat.ipynb
```

## Dataset

Dataset yang digunakan tetap **EuroSAT RGB**, berisi 27.000 citra satelit Sentinel-2 RGB dengan 10 kelas dan resolusi asli 64x64x3.

Sumber dataset:

- TensorFlow Datasets: `eurosat/rgb`
- Repositori resmi EuroSAT: `phelber/eurosat`
- Mirror arsip RGB: Zenodo EuroSAT RGB

TFDS hanya menyediakan split awal `train`, sehingga notebook membuat split eksplisit:

| Split | Jumlah | Proporsi |
| --- | ---: | ---: |
| Train | 21.600 | 80% |
| Validation | 2.700 | 10% |
| Test | 2.700 | 10% |

Split dibuat stratified per kelas dengan random seed `42`. Test set tidak digunakan untuk training, tuning, callback, checkpoint selection, atau pemilihan model.

Catatan bintang 5: EuroSAT memenuhi syarat jumlah gambar, jumlah kelas, dan bukan dataset latihan Dicoding, tetapi resolusi asli dataset ini seragam (`64x64x3`). Karena itu, submission tidak mengklaim memenuhi saran "gambar asli memiliki resolusi tidak seragam". Dataset tidak diganti karena pipeline EuroSAT sudah kuat, reproducible, dan bebas data leakage, meskipun test accuracy run penuh final belum mencapai 95%.

## Ringkasan Metode

Notebook menjalankan alur berikut:

1. Setup seed dan path relatif repository.
2. Load EuroSAT RGB dari TensorFlow Datasets.
3. Validasi metadata dataset: total gambar, jumlah kelas, nama kelas, split awal, shape, dan dtype.
4. Export dataset ke `dataset/raw/<class_name>/`.
5. Membuat split stratified ke `dataset/train/`, `dataset/validation/`, dan `dataset/test/`.
6. Audit dataset untuk distribusi kelas, format, mode, resolusi, file corrupt, duplikasi dalam split, dan duplikasi antar split.
7. Membuat pipeline `tf.data` untuk train, validation, dan test.
8. Menerapkan data augmentation hanya di alur training melalui layer Keras.
9. Melatih baseline CNN Sequential dan MobileNetV2 transfer learning.
10. Memilih model berdasarkan validation accuracy.
11. Melakukan fine-tuning sebagian layer atas MobileNetV2 dengan learning rate kecil.
12. Evaluasi final pada test set.
13. Export model ke SavedModel, TFLite, dan TFJS.

## Hasil Evaluasi

Run lokal terakhir memakai model terbaik berdasarkan validation set:

| Metrik | Nilai |
| --- | ---: |
| Model terpilih | `mobilenetv2_finetuned` |
| Train accuracy checkpoint | 0.9562 |
| Validation accuracy checkpoint | 0.9396 |
| Test accuracy | 0.9448 |
| Test loss | 0.1753 |
| Jumlah sampel test | 2.700 |

Artefak evaluasi dihasilkan ke:

```text
outputs/evaluation/
```

Folder `outputs/` di-ignore oleh git karena berisi artefak hasil run, tetapi file tersebut dapat dibuat ulang dengan menjalankan notebook.

## Export Model

Export yang sudah tervalidasi pada run lokal:

```text
saved_model/eurosat_classifier/
tflite/eurosat_classifier.tflite
tflite/label.txt
tfjs/eurosat_classifier/model.json
tfjs/eurosat_classifier/group1-shard*.bin
tfjs/eurosat_classifier/label.txt
```

Validasi export:

- SavedModel dapat diload ulang dan menghasilkan prediksi shape `(1, 10)`.
- TFLite dapat diload dengan interpreter dan menghasilkan prediksi shape `(1, 10)`.
- TFJS graph model memiliki `model.json`, tiga shard `.bin`, dan output signature 10 kelas.
- `tfjs/eurosat_classifier/label.txt` sama dengan `tflite/label.txt`.
- Jumlah probabilitas prediksi mendekati 1.

Catatan TFJS: `tensorflowjs` tidak dimasukkan langsung ke `requirements.txt` karena pip akan menarik `tensorflow-decision-forests` dan dapat memicu konflik dependency pada Windows/Python 3.12. Jika perlu membuat ulang export TFJS, install converter secara manual dengan dependency resolver dimatikan untuk package `tensorflowjs`:

```bash
python -m pip install tf_keras==2.21.0 tensorflow-hub==0.16.1 jax==0.4.34 jaxlib==0.4.34 "packaging~=23.1" "setuptools<81"
python -m pip install --no-deps tensorflowjs==4.22.0
```

Pada environment lokal Windows/Python 3.12 ini, export TFJS paling stabil dilakukan sebagai TFJS graph model dari SavedModel inference-only sementara. Notebook membuat model inference-only tanpa layer augmentation untuk konversi TFJS, memvalidasi bahwa outputnya identik dengan model asli pada mode inference (`max_delta=0.0`), lalu menghasilkan folder `tfjs/eurosat_classifier/`.

## Cara Menjalankan Notebook

1. Buat dan aktifkan virtual environment.
2. Install dependency dari `requirements.txt`.
3. Jalankan notebook dari root repository.
4. Eksekusi cell dari atas ke bawah.

Contoh:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter notebook klasifikasi-gambar-eurosat.ipynb
```

Eksekusi pertama akan mengunduh EuroSAT RGB dan membuat folder dataset lokal. Dataset dan output run tidak perlu dimasukkan ke git.

## Cara Menjalankan Inference

Jalankan cell bagian **Inference** di notebook setelah bagian evaluasi dan export selesai. Cell tersebut mengambil beberapa gambar dari `dataset/test/`, menampilkan:

- input image;
- true label;
- predicted label;
- confidence score;
- status benar/salah.

Hasil inference disimpan ulang ke:

```text
outputs/evaluation/sample_inference.csv
outputs/evaluation/sample_inference.png
```

## Struktur Repository

```text
submission-klasifikasi-gambar-eurosat/
├── AGENTS.md
├── README.md
├── requirements.txt
├── .gitignore
├── klasifikasi-gambar-eurosat.ipynb
├── dataset/
├── notes/
│   ├── DATASET_DECISION.md
│   ├── FINAL_AUDIT.md
│   ├── MODEL_SUMMARY.md
│   ├── PROJECT_CONTEXT.md
│   └── SUBMISSION_CHECKLIST.md
├── outputs/
├── saved_model/
│   └── eurosat_classifier/
├── tfds_data/
├── tfjs/
│   └── eurosat_classifier/
│       ├── model.json
│       ├── group1-shard*.bin
│       └── label.txt
└── tflite/
    ├── eurosat_classifier.tflite
    └── label.txt
```

## Reproducibility Notes

- Semua path notebook relatif terhadap root repository.
- Random seed utama: `42`.
- Dataset split dibuat stratified per kelas.
- Test set hanya dipakai pada evaluasi final dan sample inference.
- Folder `dataset/`, `tfds_data/`, dan `outputs/` di-ignore karena dapat dibuat ulang dan ukurannya besar.
- `requirements.txt` tidak diubah dalam audit ini.
