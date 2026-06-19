# Model Summary

Current branch summary for `experiment/open-images-it-assets`.

Detailed version: `notes/MODEL_SUMMARY_IT_ASSETS.md`.

## Dataset

| Item | Value |
| --- | ---: |
| Dataset | Open Images V7 IT Asset Subset |
| Total crop | 15.000 |
| Classes | 5 |
| Crop per class | 3.000 |
| Train crop | 12.002 |
| Validation crop | 1.502 |
| Test crop | 1.496 |
| Unique crop resolutions | 14.168 |

## Final Model

```text
EfficientNetV2B1 + EfficientNetV2B2 + EfficientNetV2B3 + ConvNeXtTiny
```

The final exported graph includes horizontal-flip test-time augmentation.

## Final Metrics

| Metric | Value |
| --- | ---: |
| Train accuracy | 0.9973 |
| Validation accuracy | 0.9554 |
| Test accuracy | 0.9579 |

Model selection used validation accuracy. Test accuracy was measured after model selection and was not used for tuning.

## Export Summary

| Format | Location | Status |
| --- | --- | --- |
| SavedModel | `saved_model/it_asset_classifier/` | exported_and_validated |
| TFLite | `tflite/it_asset_classifier.tflite` | exported_and_validated |
| TFJS | `tfjs/it_asset_classifier/` | exported_and_validated |

## Risk

The exported ensemble is large. Check final submission ZIP size before packaging, and use Git LFS or a smaller model if GitHub file limits become blocking.
