# Google Colab Run Guide - IT Assets

Use `klasifikasi-gambar-it-assets.ipynb` in Google Colab with GPU runtime.

## Required Colab Setup

1. Upload or mount the full project folder containing:
   - `configs/openimages_it_assets_classes.json`
   - `dataset/raw/`
   - `dataset/metadata/openimages_crop_metadata.csv`
   - `klasifikasi-gambar-it-assets.ipynb`
2. In Colab, choose `Runtime > Change runtime type > T4 GPU`.
3. Run the notebook from the first cell.

The notebook stops early if Colab GPU is not active.

## What Is Now In The Notebook

- Source data process from `src/build_openimages_subset.py`.
- Crop metadata audit process from `src/audit_openimages_subset.py`.
- Manual grouped split process from `src/split_openimages_subset.py`.
- Split audit process from `src/audit_openimages_split.py`.
- Final `tf.keras.Sequential` model with explicit `Conv2D` and pooling.
- Direct `model.fit`, `model.evaluate(test_ds)`, classification report, plots, export, export validation, and inference proof.

## Colab Notes

- The notebook does not redownload Open Images by default; it uses existing `dataset/raw` and crop metadata.
- Checkpoints save weights only to avoid full-model save hangs during training.
- Full SavedModel, TFLite, and TFJS exports are created after final evaluation.
