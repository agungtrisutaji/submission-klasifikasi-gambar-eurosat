## Dataset

Dataset yang digunakan adalah EuroSAT RGB, berisi 27.000 citra satelit Sentinel-2 RGB dengan 10 kelas.

Sumber:
- TensorFlow Datasets: eurosat/rgb
- GitHub resmi EuroSAT: phelber/eurosat

Struktur dataset:
- train: 80%
- validation: 10%
- test: 10%

Catatan:
Dataset dibagi secara stratified per kelas menggunakan random seed 42.
Test set tidak digunakan untuk training maupun tuning.
