# Open Images Full Scale Feasibility

## Tujuan

Menguji apakah kombinasi kelas awal Open Images V7 IT Asset dapat mencapai target minimal 10.000 crop dengan distribusi seimbang untuk submission Dicoding.

## Command

```powershell
.\.venv\Scripts\python.exe src\build_openimages_subset.py --target-crops-per-class 2000 --max-samples-per-class 5000 --source-splits train --overwrite
.\.venv\Scripts\python.exe src\audit_openimages_subset.py --min-crops-per-class 2000
```

## Result

| Class | Target | Actual | Status |
| --- | ---: | ---: | --- |
| laptop | 2000 | 2000 | Pass |
| computer_keyboard | 2000 | 2000 | Pass |
| computer_mouse | 2000 | 724 | Fail |
| mobile_phone | 2000 | 2000 | Pass |
| printer | 2000 | 262 | Fail |

Total crops: 6986
Ready for full scale: False

## Decision

The initial 5-class combination is not suitable for the final dataset because `computer_mouse` and `printer` cannot reach the target minimum of 2000 valid crops from the current Open Images train source split.

## Next Action

Replace `computer_mouse` and `printer` with candidate classes that have enough valid bounding box crops and are visually separable from existing classes.

Recommended candidate classes:

- Computer monitor
- Headphones
- Tablet computer
- Camera
- Television
- Server
- Remote control

Note: `Server` is listed as a candidate requested for follow-up, but the local Open Images class descriptions cached in this workspace did not show an exact `Server` boxable label during this pass. Verify the exact Open Images class name before promoting it into the active `classes` list.

Do not start modelling until a replacement class combination reaches:

- total crop count >= 10.000;
- each selected class >= 2.000 crop;
- crop resolutions are non-uniform;
- corrupt images are zero or removed;
- duplicate/cross-class duplicate issues are reviewed;
- `ready_for_full_scale_dataset_build` is True.
