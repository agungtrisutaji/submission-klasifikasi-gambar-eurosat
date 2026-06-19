# Open Images Split Audit

## Command

```powershell
.\.venv\Scripts\python.exe src\split_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --metadata-path dataset\metadata\openimages_crop_metadata.csv --raw-dir dataset\raw --split-dir dataset --train-ratio 0.8 --validation-ratio 0.1 --test-ratio 0.1 --seed 42 --overwrite
.\.venv\Scripts\python.exe src\audit_openimages_split.py --class-config configs\openimages_it_assets_classes.json --split-metadata-path dataset\metadata\openimages_split_metadata.csv --audit-json outputs\dataset_audit\openimages_split_audit.json --split-summary-csv outputs\dataset_audit\openimages_split_summary.csv --min-total-crops 10000 --min-crops-per-class 3000
```

## Result

Total crops: 15000
Train crops: 12002
Validation crops: 1502
Test crops: 1496

| Split | laptop | computer_keyboard | mobile_phone | computer_monitor | camera | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| train | 2399 | 2400 | 2402 | 2401 | 2400 | 12002 |
| validation | 303 | 300 | 299 | 300 | 300 | 1502 |
| test | 298 | 300 | 299 | 299 | 300 | 1496 |

Actual split ratios:

| Split | Ratio |
| --- | ---: |
| train | 0.8001 |
| validation | 0.1001 |
| test | 0.0997 |

Source image leakage across split: 0
Duplicate hash across split: 0
Corrupt image count: 0
Missing split crop file count: 0
Unique crop resolutions total: 14168
Ready for modelling: true

## Blockers

- None.

## Warnings

- Duplicate file hash values within a split were found: 2 groups in train only.

## Decision

Dataset split is accepted for modelling. The split uses group assignment by `source_image_id`, so all crops from the same source image stay in one local split. Test data must remain reserved for final evaluation only and must not be used for training, tuning, callback decisions, checkpoint selection, or model selection.
