# Dataset Acquisition - Open Images IT Assets

Dataset submission ini berasal dari **Open Images V7 detection crops**.

Gambar Open Images diperoleh menggunakan script Python yang disertakan pada folder `src/`. Notebook ini tidak mengunduh ulang gambar, tetapi memulai dari satu folder sumber `dataset/raw/<class_name>/` lalu melakukan pembagian manual menjadi train, validation, dan test agar proses split dapat diverifikasi langsung oleh reviewer.

## Source

- Dataset: Open Images V7
- Label type: detections
- Task: multi-class image classification dari crop bounding box
- Local source folder: `dataset/raw/<class_name>/`

## Class Configuration

Konfigurasi kelas ada di:

```text
configs/openimages_it_assets_classes.json
```

Kelas final:

- `camera`
- `computer_keyboard`
- `computer_monitor`
- `laptop`
- `mobile_phone`

## Acquisition Scripts

Script yang dipakai untuk membangun dan mengaudit dataset:

```text
src/build_openimages_subset.py
src/audit_openimages_subset.py
src/split_openimages_subset.py
src/audit_openimages_split.py
```

`src/build_openimages_subset.py` mengambil Open Images detection data dan membuat crop objek ke `dataset/raw/<class_name>/`.

Notebook utama tidak wajib mengunduh ulang gambar dari Open Images. Untuk reviewer, proses penting yang ditampilkan langsung di notebook adalah split manual dari `dataset/raw/<class_name>/` ke:

```text
dataset/submission_split/train/<class_name>/
dataset/submission_split/validation/<class_name>/
dataset/submission_split/test/<class_name>/
```

## Notebook Evidence

Notebook menampilkan:

- total gambar sumber;
- jumlah kelas;
- jumlah gambar per kelas sebelum split;
- jumlah gambar train/validation/test;
- jumlah gambar per kelas di setiap split;
- corrupt image count;
- duplicate hash antar split;
- contoh gambar;
- load dataset dari folder hasil split.

## ZIP Notes

Script dan dokumentasi dataset harus ikut dalam ZIP submission:

```text
src/build_openimages_subset.py
src/audit_openimages_subset.py
src/split_openimages_subset.py
src/audit_openimages_split.py
configs/openimages_it_assets_classes.json
notes/DATASET_ACQUISITION.md
notes/DATASET_LICENSE.md
```

Folder besar/cache seperti `dataset/`, `openimages_data/`, `.venv/`, checkpoint training, dan `.git/` tidak perlu ikut ZIP.
