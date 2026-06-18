# Open Images Split Audit

## Command

```powershell
.\.venv\Scripts\python.exe src\split_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --metadata-path dataset\metadata\openimages_crop_metadata.csv --raw-dir dataset\raw --split-dir dataset --train-ratio 0.8 --validation-ratio 0.1 --test-ratio 0.1 --seed 42 --overwrite
.\.venv\Scripts\python.exe src\audit_openimages_split.py --class-config configs\openimages_it_assets_classes.json
```

## Result

Total crops: 10000
Train crops: 8006
Validation crops: 994
Test crops: 1000

| Split | laptop | computer_keyboard | mobile_phone | computer_monitor | camera | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| train | 1600 | 1600 | 1598 | 1602 | 1606 | 8006 |
| validation | 200 | 201 | 197 | 199 | 197 | 994 |
| test | 200 | 199 | 205 | 199 | 197 | 1000 |

Actual split ratios:

| Split | Ratio |
| --- | ---: |
| train | 0.8006 |
| validation | 0.0994 |
| test | 0.1000 |

Source image leakage across split: 0
Duplicate hash across split: 0
Corrupt image count: 0
Missing split crop file count: 0
Unique crop resolutions total: 9617
Ready for modelling: true

## Blockers

- None.

## Warnings

- None.

## Decision

Dataset split is accepted for modelling. Training may start after this audit.

The split uses group assignment by `source_image_id`, so all crops from the same source image stay in one local split. Test data must remain reserved for final evaluation only and must not be used for training, tuning, callback decisions, checkpoint selection, or model selection.
