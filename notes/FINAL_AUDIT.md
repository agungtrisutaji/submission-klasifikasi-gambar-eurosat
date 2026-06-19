# Final Audit

Current branch summary for `experiment/open-images-it-assets`.

Detailed version: `notes/FINAL_AUDIT_IT_ASSETS.md`.

## Dataset Audit

| Check | Result |
| --- | ---: |
| Total crop | 15.000 |
| Minimum total crop target | 10.000 |
| Classes | 5 |
| Crop per class | 3.000 |
| Source image leakage across split | 0 |
| Duplicate file hash across split | 0 |
| Corrupt image count | 0 |
| Unique crop resolutions total | 14.168 |
| Ready for modelling | true |

Split:

| Split | Crop |
| --- | ---: |
| Train | 12.002 |
| Validation | 1.502 |
| Test | 1.496 |

## Model Audit

| Metric | Result |
| --- | ---: |
| Train accuracy | 0.9973 |
| Validation accuracy | 0.9554 |
| Test accuracy | 0.9579 |

Model selection used validation accuracy. Test set was reserved for final evaluation.

## Export Audit

| Export | Status |
| --- | --- |
| SavedModel | exported_and_validated |
| TFLite | exported_and_validated |
| TFJS | exported_and_validated |

## Remaining Risk

Export artifacts are large because the final model is an ensemble. Before final packaging, verify submission size limits and decide whether to keep the ensemble, use Git LFS, or distill/retrain a smaller single-backbone model.
