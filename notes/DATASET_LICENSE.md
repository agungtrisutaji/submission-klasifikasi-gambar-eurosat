# Dataset License Notes

## Sumber dataset

Eksperimen ini direncanakan memakai subset Open Images V7 untuk klasifikasi aset IT.

Sumber resmi:

- Open Images Dataset: https://storage.googleapis.com/openimages/web/index.html
- Open Images V7 download page: https://storage.googleapis.com/openimages/web/download_v7.html
- Open Images V7 description and license notes: https://storage.googleapis.com/openimages/web/factsfigures_v7.html

Subset lokal akan dibuat dari gambar Open Images V7 yang memiliki bounding box untuk kelas target seperti Laptop, Computer keyboard, Computer mouse, Mobile phone, dan Printer.

## Catatan lisensi dan attribution

Berdasarkan dokumentasi resmi Open Images V7:

- anotasi dilisensikan oleh Google LLC dengan lisensi CC BY 4.0;
- gambar terdaftar sebagai CC BY 2.0;
- pengguna tetap perlu memverifikasi status lisensi gambar sesuai kebutuhan karena Open Images tidak memberi jaminan status lisensi untuk setiap gambar.

Konsekuensi untuk project ini:

- catat sumber Open Images V7 pada README dan notebook;
- simpan metadata gambar/crop yang diperlukan untuk attribution bila tersedia;
- pertahankan mapping dari crop lokal ke `image_id` sumber;
- jangan mengklaim kepemilikan gambar;
- gunakan subset untuk kebutuhan pembelajaran/submission secara wajar dan reproducible.

## Kebijakan file besar

Gambar Open Images, crop dataset, cache FiftyOne, dan output eksperimen tidak boleh disimpan di git atau ZIP submission bila ukurannya besar.

Folder yang harus tetap lokal dan di-ignore:

```text
dataset/
openimages_data/
fiftyone/
outputs/
```

File model export hanya boleh dipertahankan di repo bila memang dibutuhkan oleh instruksi submission dan ukurannya masih masuk akal. Untuk branch eksperimen ini, export ulang belum dilakukan pada tahap awal.

## Reproduksi subset

Cara reproduksi subset harus dicatat di notebook dan README sebelum dataset dinyatakan final:

- versi Open Images V7;
- tool download, misalnya FiftyOne;
- versi package utama;
- kelas yang dipakai;
- split sumber yang dipakai;
- parameter download;
- filter bounding box atau kualitas crop;
- seed split lokal, yaitu `42`;
- jumlah crop per kelas;
- lokasi file audit;
- catatan lisensi dan attribution.

Tanpa catatan reproduksi tersebut, subset belum siap dipakai untuk modelling submission.
