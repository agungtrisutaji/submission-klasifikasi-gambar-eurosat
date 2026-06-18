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

Kelas utama:

| Label target | Open Images class |
| --- | --- |
| `laptop` | Laptop |
| `computer_keyboard` | Computer keyboard |
| `computer_mouse` | Computer mouse |
| `mobile_phone` | Mobile phone |
| `printer` | Printer |

Kelas cadangan bila jumlah sample, kualitas crop, atau separabilitas kelas utama kurang baik:

| Label target | Open Images class |
| --- | --- |
| `tablet_computer` | Tablet computer |
| `computer_monitor` | Computer monitor |
| `headphones` | Headphones |
| `camera` | Camera |

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
import fiftyone.zoo as foz

classes = [
    "Laptop",
    "Computer keyboard",
    "Computer mouse",
    "Mobile phone",
    "Printer",
]

dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="train",
    label_types=["detections"],
    classes=classes,
    max_samples=1000,
    dataset_dir="openimages_data",
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

Split lokal yang direncanakan:

```text
dataset/train/<class_name>/
dataset/validation/<class_name>/
dataset/test/<class_name>/
```

Proporsi awal:

| Split | Proporsi |
| --- | ---: |
| Train | 80% |
| Validation | 10% |
| Test | 10% |

Split dibuat stratified per kelas dengan seed `42`. Jika memakai split bawaan Open Images sebagai sumber, tetap buat split lokal eksplisit untuk submission dan dokumentasikan mapping-nya.

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
