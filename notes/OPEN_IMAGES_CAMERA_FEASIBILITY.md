# Open Images Camera Replacement Feasibility

## Candidate Classes

| Open Images class | Local label |
| --- | --- |
| Laptop | laptop |
| Computer keyboard | computer_keyboard |
| Mobile phone | mobile_phone |
| Computer monitor | computer_monitor |
| Camera | camera |

## Command

```powershell
.\.venv\Scripts\python.exe src\build_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --target-crops-per-class 2000 --max-samples-per-class 5000 --source-splits train --overwrite
.\.venv\Scripts\python.exe src\audit_openimages_subset.py --class-config configs\openimages_it_assets_classes.json --min-crops-per-class 2000
```

## Result

| Class | Target | Actual | Status |
| --- | ---: | ---: | --- |
| laptop | 2000 | 2000 | Pass |
| computer_keyboard | 2000 | 2000 | Pass |
| mobile_phone | 2000 | 2000 | Pass |
| computer_monitor | 2000 | 2000 | Pass |
| camera | 2000 | 2000 | Pass |

Total crops: 10000
Unique crop resolutions: 9617
Corrupt image count: 0
Duplicate hash group count: 0
Duplicate across classes group count: 0
Source IDs in multiple source splits count: 0
Ready for full scale: true

## Blockers

- None.

## Warnings

- None.

## Decision

The Camera replacement combination is feasible for the final dataset build. The next step is creating a local train/validation/test split with group split by `source_image_id`.

Do not start modelling yet. Training should wait until the split script is created, the split is audited, and cross-split leakage is confirmed to be zero.

## Next Action

- Create `src/split_openimages_subset.py` with group split by `source_image_id`.
- Use stratified class distribution targets with seed `42`.
- Ensure all crops from the same `source_image_id` stay in the same local split.
- Audit split distribution, corrupt images, duplicate hashes, and cross-split source leakage before modelling.
