# Open Images V7 IT Asset Subset Plan

## Tujuan eksperimen

Branch `experiment/open-images-it-assets` digunakan untuk menguji migrasi dari EuroSAT RGB ke subset Open Images V7 untuk klasifikasi gambar aset IT. Tujuan akhirnya adalah membuat submission Dicoding yang tetap reproducible, bebas data leakage, dan lebih dekat dengan saran bintang 5:

- minimal 10.000 gambar;
- minimal 3 kelas;
- resolusi asli gambar tidak seragam;
- train accuracy minimal 95%;
- test accuracy minimal 95%;
- memakai callback;
- memiliki proof inference;
- export SavedModel, TFLite, dan TFJS.

Tahap awal ini belum melakukan download dataset, training, atau export ulang model.

## Status eksplorasi dataset

Tahap builder eksplorasi sudah disiapkan melalui script lokal:

```text
src/build_openimages_subset.py
src/audit_openimages_subset.py
src/split_openimages_subset.py
src/audit_openimages_split.py
configs/openimages_it_assets_classes.json
```

Scope tahap ini:

- validasi bahwa class name Open Images dapat dipakai oleh FiftyOne;
- download subset kecil Open Images V7 dengan label type `detections`;
- crop bounding box kelas target menjadi dataset klasifikasi awal;
- simpan metadata crop ke `dataset/metadata/openimages_crop_metadata.csv`;
- audit jumlah crop, resolusi crop, corrupt file, duplicate hash, dan potensi duplicate antar kelas;
- belum membuat split final train/validation/test;
- belum training;
- belum export ulang SavedModel, TFLite, atau TFJS.

Full-scale feasibility awal dengan `Laptop`, `Computer keyboard`, `Computer mouse`, `Mobile phone`, dan `Printer` gagal untuk target 2.000 crop per kelas. `computer_mouse` hanya mencapai 724 crop dan `printer` hanya mencapai 262 crop dari source split `train`, sehingga dua kelas tersebut tidak dipakai sebagai kandidat final saat ini. Ringkasan keputusan ada di `notes/OPEN_IMAGES_FULL_SCALE_FEASIBILITY.md`.

Feasibility pengganti dengan `Headphones` juga gagal karena hanya mencapai 1.241 crop dari target 2.000. Ringkasan hasilnya ada di `notes/OPEN_IMAGES_REPLACEMENT_FEASIBILITY.md`. Camera kemudian dipakai sebagai pengganti `Headphones`, dan feasibility Camera sudah lolos: total 10.000 crop, setiap kelas 2.000 crop, resolusi crop tidak seragam, corrupt image 0, duplicate hash group 0, duplicate across classes 0, blockers kosong, dan `ready_for_full_scale_dataset_build = true`. Ringkasan hasilnya ada di `notes/OPEN_IMAGES_CAMERA_FEASIBILITY.md`.

Output eksplorasi berada pada folder yang di-ignore git:

```text
dataset/
openimages_data/
outputs/
```

Cara menjalankan builder eksplorasi:

```powershell
.\.venv\Scripts\python.exe src\build_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --target-crops-per-class 2000 --max-samples-per-class 5000 --source-splits train --overwrite
```

Cara menjalankan audit:

```powershell
.\.venv\Scripts\python.exe src\audit_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --min-crops-per-class 2000
```

Output audit:

```text
outputs/dataset_audit/openimages_subset_audit.json
outputs/dataset_audit/openimages_resolution_summary.csv
```

Camera replacement combination accepted for final dataset preparation. Next step: create train/validation/test split with group split by `source_image_id`. Jangan training, tuning, atau export model sebelum split dan audit split selesai.

Split lokal train/validation/test sudah dibuat dengan group split berdasarkan `source_image_id` dan seed `42`. Hasil audit split ada di `notes/OPEN_IMAGES_SPLIT_AUDIT.md`: total 10.000 crop, train 8.006, validation 994, test 1.000, source image leakage across split 0, duplicate hash across split 0, corrupt image count 0, missing split crop file count 0, dan `ready_for_modelling = true`.

## Rencana migrasi identitas project

Mapping identitas yang dipakai untuk migrasi bertahap:

| Identitas lama | Identitas baru |
| --- | --- |
| `klasifikasi-gambar-eurosat.ipynb` | `klasifikasi-gambar-it-assets.ipynb` |
| `eurosat_classifier` | `it_asset_classifier` |
| EuroSAT RGB | Open Images V7 IT Asset Subset |
| satellite image classification | IT asset image classification |
| `saved_model/eurosat_classifier/` | `saved_model/it_asset_classifier/` |
| `tflite/eurosat_classifier.tflite` | `tflite/it_asset_classifier.tflite` |
| `tfjs/eurosat_classifier/` | `tfjs/it_asset_classifier/` |

Untuk tahap awal, notebook dan export EuroSAT lama tidak dihapus. Notebook baru dibuat sebagai template migrasi, lalu isi notebook akan diganti bertahap setelah dataset subset Open Images selesai diaudit.

## Kandidat kelas

Kelas awal yang sudah diuji:

| Label target | Open Images class |
| --- | --- |
| `laptop` | Laptop |
| `computer_keyboard` | Computer keyboard |
| `computer_mouse` | Computer mouse |
| `mobile_phone` | Mobile phone |
| `printer` | Printer |

Status kelas awal:

| Label target | Status |
| --- | --- |
| `laptop` | Pass feasibility awal |
| `computer_keyboard` | Pass feasibility awal |
| `computer_mouse` | Ditolak sementara, hanya 724 crop dari target 2.000 |
| `mobile_phone` | Pass feasibility awal |
| `printer` | Ditolak sementara, hanya 262 crop dari target 2.000 |

Kelas kandidat berikutnya di `configs/openimages_it_assets_classes.json`:

| Label target | Open Images class |
| --- | --- |
| `laptop` | Laptop |
| `computer_keyboard` | Computer keyboard |
| `mobile_phone` | Mobile phone |
| `computer_monitor` | Computer monitor |
| `camera` | Camera |

Kelas yang ditolak atau ditunda:

| Label target | Status |
| --- | --- |
| `headphones` | Ditolak sementara, hanya 1.241 crop dari target 2.000 |
| `server` | Ditunda, label boxable persis `Server` belum ditemukan di metadata lokal |

Kelas cadangan bila jumlah sample, kualitas crop, atau separabilitas kelas kandidat kurang baik:

| Label target | Open Images class |
| --- | --- |
| `tablet_computer` | Tablet computer |
| `television` | Television |
| `server` | Server |
| `remote_control` | Remote control |

Catatan: `Server` disimpan sebagai kandidat pengganti, tetapi cache class descriptions Open Images lokal di workspace ini belum menunjukkan label boxable persis `Server`. Validasi nama kelas Open Images perlu dilakukan sebelum `server` dipromosikan ke daftar `classes` utama.

Keputusan final kelas harus dibuat setelah audit jumlah bounding box, ukuran objek, variasi resolusi, dan overlap antar kelas.

## Strategi download Open Images V7

Sumber utama dataset adalah Open Images V7 dari Google:

- halaman dataset: https://storage.googleapis.com/openimages/web/index.html
- halaman download V7: https://storage.googleapis.com/openimages/web/download_v7.html
- metadata dan class descriptions tersedia dari halaman download resmi.

Strategi yang disarankan untuk subset:

1. Gunakan FiftyOne Dataset Zoo untuk mengunduh hanya kelas dan split yang dibutuhkan.
2. Ambil label type `detections` agar bounding box tersedia untuk crop objek.
3. Batasi jumlah sample awal per kelas untuk eksplorasi cepat.
4. Simpan data mentah dan cache lokal di folder yang di-ignore git, misalnya `openimages_data/` atau `fiftyone/`.
5. Catat versi library, parameter download, kelas, split, dan jumlah sample aktual di notebook dan README.

Contoh arah perintah awal, belum dijalankan pada tahap ini:

```python
import fiftyone as fo
import fiftyone.zoo as foz

classes = [
    "Laptop",
    "Computer keyboard",
    "Mobile phone",
    "Computer monitor",
    "Camera",
]

fo.config.dataset_zoo_dir = "openimages_data"

dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="train",
    label_types=["detections"],
    classes=classes,
    max_samples=1000,
)
```

Parameter final tidak boleh hanya memakai `max_samples` global bila hasilnya tidak seimbang. Setelah eksplorasi, download harus diarahkan agar setiap kelas memenuhi target minimum dan tetap dapat diaudit.

## Strategi crop bounding box menjadi dataset klasifikasi

Open Images V7 adalah dataset multi-label dan object detection. Untuk submission klasifikasi gambar, subset harus dibuat sebagai crop objek tunggal:

1. Filter detection berdasarkan kelas target.
2. Download gambar sumber yang memiliki bounding box kelas target.
3. Crop area bounding box dari gambar asli.
4. Simpan crop ke `dataset/raw/<class_name>/`.
5. Simpan metadata crop ke CSV/JSON, minimal berisi:
   - `image_id`;
   - split sumber Open Images;
   - label Open Images;
   - label target lokal;
   - bounding box normalized dan pixel;
   - ukuran gambar asli;
   - ukuran crop;
   - path crop relatif;
   - attribution atau metadata lisensi bila tersedia;
   - hash file crop.
6. Hindari crop yang terlalu kecil, terlalu blur, atau terlalu berat occlusion.
7. Jika satu gambar sumber mengandung beberapa kelas target, pastikan semua crop dari gambar sumber yang sama hanya masuk ke satu split lokal.

Crop digunakan sebagai gambar klasifikasi, bukan bounding box task. Notebook harus menjelaskan transformasi ini secara eksplisit agar reviewer memahami asal dataset.

## Target jumlah gambar/crop per kelas

Target awal:

| Kelas | Target minimum crop | Target eksplorasi |
| --- | ---: | ---: |
| Laptop | 2.000 | 2.500-3.000 |
| Computer keyboard | 2.000 | 2.500-3.000 |
| Computer mouse | 2.000 | 2.500-3.000 |
| Mobile phone | 2.000 | 2.500-3.000 |
| Printer | 2.000 | 2.500-3.000 |

Target dataset final minimal 10.000 crop valid. Jika salah satu kelas utama sulit mencapai jumlah atau kualitas memadai, gunakan kelas cadangan dan catat alasan penggantian.

## Audit resolusi asli

Karena target bintang 5 mencakup resolusi asli tidak seragam, audit harus menyimpan distribusi ukuran sebelum resize model:

- ukuran gambar sumber;
- ukuran crop sebelum resize;
- width, height, aspect ratio;
- min, max, mean, median per kelas;
- jumlah resolusi unik per kelas dan total;
- contoh gambar resolusi kecil, sedang, dan besar.

Model boleh menerima resize tetap pada pipeline preprocessing, tetapi dokumentasi harus membedakan resolusi asli/crop dari ukuran input model.

## Split train/validation/test

Split lokal yang dibuat:

```text
dataset/train/<class_name>/
dataset/validation/<class_name>/
dataset/test/<class_name>/
```

Proporsi awal:

| Split | Proporsi |
| --- | ---: |
| Train | 0.8006 |
| Validation | 0.0994 |
| Test | 0.1000 |

Split dibuat dengan seed `42`, stratified mendekati 80/10/10 per kelas, dan group split berdasarkan `source_image_id`. Semua crop dari source image yang sama harus tetap berada dalam satu split lokal.

Command split:

```powershell
.\.venv\Scripts\python.exe src\split_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --metadata-path dataset\metadata\openimages_crop_metadata.csv --raw-dir dataset\raw --split-dir dataset --train-ratio 0.8 --validation-ratio 0.1 --test-ratio 0.1 --seed 42 --overwrite
```

Command audit split:

```powershell
.\.venv\Scripts\python.exe src\audit_openimages_split.py --class-config configs\openimages_it_assets_classes.json
```

## Anti data leakage

Aturan anti leakage:

1. Group split berdasarkan `image_id` sumber, bukan berdasarkan file crop.
2. Semua crop dari satu gambar sumber harus berada di split lokal yang sama.
3. Jangan gunakan test set untuk training, tuning, early stopping, checkpoint selection, atau pemilihan model.
4. Hitung hash crop untuk mendeteksi duplikasi file.
5. Hitung perceptual hash atau minimal hash konten untuk mendeteksi crop identik lintas split.
6. Simpan audit duplicate within split dan cross-split duplicate.
7. Simpan metadata split agar dataset bisa direproduksi.
8. Hindari augmentasi sebelum split. Augmentasi hanya dilakukan di pipeline training.

## Acceptance criteria tahap dataset

Tahap dataset dianggap selesai bila:

- Open Images V7 berhasil diakses dari sumber resmi atau FiftyOne;
- kelas final terdokumentasi;
- minimal 10.000 crop valid tersedia;
- minimal 3 kelas valid tersedia, target awal 5 kelas;
- folder `dataset/raw`, `dataset/train`, `dataset/validation`, dan `dataset/test` terbentuk;
- split stratified 80/10/10 dengan seed `42` tersimpan;
- setiap split memiliki distribusi kelas yang diaudit;
- resolusi asli/crop tidak seragam dan ringkasannya tersimpan;
- corrupt image count bernilai 0 atau semua file corrupt dikeluarkan;
- duplicate within split dan cross-split duplicate diaudit;
- group leakage berdasarkan `image_id` sumber bernilai 0;
- sumber dataset, license note, dan reproduksi subset tercatat di notebook dan README;
- tidak ada dataset besar, cache Open Images, atau output run yang masuk git.

Setelah acceptance criteria dataset terpenuhi, baru lanjut ke modelling.
