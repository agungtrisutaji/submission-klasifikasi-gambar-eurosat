# Open Images Replacement Class Feasibility

## Candidate Classes

| Open Images class | Local label |
| --- | --- |
| Laptop | laptop |
| Computer keyboard | computer_keyboard |
| Mobile phone | mobile_phone |
| Computer monitor | computer_monitor |
| Headphones | headphones |

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
| headphones | 2000 | 1241 | Fail |

Total crops: 9241
Unique crop resolutions: 8927
Corrupt image count: 0
Duplicate hash group count: 0
Duplicate across classes group count: 0
Ready for full scale: false

## Blockers

- One or more classes have fewer than 2000 crops.

## Warnings

- None.

## Candidate Replacement Check

Counts below were read from the local Open Images train detection metadata:

| Candidate | Train images | Train detections | Note |
| --- | ---: | ---: | --- |
| Camera | 5037 | 6404 | Strong next candidate |
| Television | 2789 | 3789 | Plausible backup |
| Tablet computer | 784 | 975 | Likely too small |
| Remote control | 192 | 236 | Too small |
| Server | 0 | 0 | Exact boxable label not found in local class metadata |

## Decision

The replacement combination with `headphones` is not suitable for the final dataset because `headphones` only produced 1241 valid crops from the Open Images train split. The dataset is clean otherwise: crop resolutions are non-uniform, corrupt image count is zero, duplicate hash groups are zero, duplicate across classes are zero, and no source image appears in multiple source splits.

`headphones` should be replaced before continuing. The config has been updated to use `Camera` as the next active replacement candidate because local train metadata shows enough source images and detections to plausibly reach 2000 valid crops.

## Next Action

- Rerun feasibility with the updated config that replaces `Headphones` with `Camera`.
- Do not train before the new combination reaches `ready_for_full_scale_dataset_build = true`.
- If the `Camera` combination succeeds, the next step is to create `src/split_openimages_subset.py` with group split by `source_image_id`.
- If the `Camera` combination fails, try `Television` next.
