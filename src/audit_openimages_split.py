"""Audit local train/validation/test splits for Open Images IT asset crops."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SPLITS = ["train", "validation", "test"]
EXPECTED_TOTAL_CROPS = 10000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit Open Images IT asset train/validation/test split."
    )
    parser.add_argument(
        "--split-metadata-path",
        type=Path,
        default=Path("dataset") / "metadata" / "openimages_split_metadata.csv",
    )
    parser.add_argument(
        "--class-config",
        type=Path,
        default=Path("configs") / "openimages_it_assets_classes.json",
    )
    parser.add_argument(
        "--audit-json",
        type=Path,
        default=Path("outputs") / "dataset_audit" / "openimages_split_audit.json",
    )
    parser.add_argument(
        "--split-summary-csv",
        type=Path,
        default=Path("outputs") / "dataset_audit" / "openimages_split_summary.csv",
    )
    return parser.parse_args()


def import_pillow() -> tuple[Any, Any]:
    try:
        from PIL import Image, UnidentifiedImageError
    except ImportError as error:
        raise SystemExit(
            "Pillow is required. Install dependencies with: pip install -r requirements.txt"
        ) from error
    return Image, UnidentifiedImageError


def validate_local_label(local_label: str) -> None:
    if not re.fullmatch(r"[a-z0-9][a-z0-9_]*", local_label):
        raise ValueError(
            "Invalid local_label. Use lowercase letters, numbers, and underscores "
            f"only, starting with a letter or number: {local_label!r}"
        )


def load_expected_labels(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Class config not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    class_items = config.get("classes")
    if not isinstance(class_items, list):
        raise ValueError("Class config field 'classes' must be a list.")

    labels: list[str] = []
    seen_openimages_labels: set[str] = set()
    seen_local_labels: set[str] = set()
    for index, item in enumerate(class_items):
        if not isinstance(item, dict):
            raise ValueError(f"Class config item #{index + 1} must be an object.")
        openimages_label = item.get("openimages_label")
        local_label = item.get("local_label")
        if not isinstance(openimages_label, str) or not openimages_label.strip():
            raise ValueError(
                f"Class config item #{index + 1} must include openimages_label."
            )
        if not isinstance(local_label, str) or not local_label.strip():
            raise ValueError(f"Class config item #{index + 1} must include local_label.")
        openimages_label = openimages_label.strip()
        local_label = local_label.strip()
        validate_local_label(local_label)
        if openimages_label in seen_openimages_labels:
            raise ValueError(f"Duplicate openimages_label: {openimages_label}")
        if local_label in seen_local_labels:
            raise ValueError(f"Duplicate local_label: {local_label}")
        seen_openimages_labels.add(openimages_label)
        seen_local_labels.add(local_label)
        labels.append(local_label)

    if not labels:
        raise ValueError("Class config must contain at least one class.")
    return labels


def read_split_metadata(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Split metadata not found: {path}")
    with path.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    if not rows:
        raise ValueError(f"Split metadata is empty: {path}")

    required_columns = {
        "source_image_id",
        "source_split",
        "local_label",
        "crop_width",
        "crop_height",
        "crop_path",
        "file_hash",
        "local_split",
        "split_crop_path",
    }
    missing_columns = sorted(required_columns - set(rows[0].keys()))
    if missing_columns:
        raise ValueError(f"Split metadata missing required columns: {missing_columns}")
    return rows


def validate_image(path: Path) -> tuple[bool, str | None]:
    Image, UnidentifiedImageError = import_pillow()
    try:
        image = Image.open(path)
        image.load()
        return True, None
    except (OSError, UnidentifiedImageError) as error:
        return False, str(error)


def write_split_summary(
    path: Path,
    rows: list[dict[str, str]],
    expected_labels: list[str],
) -> list[dict[str, Any]]:
    path.parent.mkdir(parents=True, exist_ok=True)
    total = len(rows)
    summary_rows: list[dict[str, Any]] = []
    split_counts = Counter(row["local_split"] for row in rows)
    split_class_counts = Counter(
        (row["local_split"], row["local_label"]) for row in rows
    )
    source_counts_by_split: dict[str, set[str]] = defaultdict(set)
    resolution_counts_by_split: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        split_name = row["local_split"]
        source_counts_by_split[split_name].add(row["source_image_id"])
        resolution_counts_by_split[split_name].add(
            f"{row.get('crop_width')}x{row.get('crop_height')}"
        )

    fieldnames = [
        "split",
        *expected_labels,
        "total",
        "ratio",
        "source_image_id_count",
        "unique_crop_resolutions",
    ]
    for split_name in SPLITS:
        summary_row: dict[str, Any] = {"split": split_name}
        for local_label in expected_labels:
            summary_row[local_label] = split_class_counts[(split_name, local_label)]
        summary_row["total"] = split_counts[split_name]
        summary_row["ratio"] = round(split_counts[split_name] / total, 6) if total else 0
        summary_row["source_image_id_count"] = len(source_counts_by_split[split_name])
        summary_row["unique_crop_resolutions"] = len(resolution_counts_by_split[split_name])
        summary_rows.append(summary_row)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    return summary_rows


def build_audit(rows: list[dict[str, str]], expected_labels: list[str]) -> dict[str, Any]:
    total_crop = len(rows)
    split_counts = Counter(row["local_split"] for row in rows)
    split_class_counts = Counter(
        (row["local_split"], row["local_label"]) for row in rows
    )
    source_ids_by_split: dict[str, set[str]] = defaultdict(set)
    splits_by_source_id: dict[str, set[str]] = defaultdict(set)
    hash_rows_by_split: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    splits_by_hash: dict[str, set[str]] = defaultdict(set)
    resolutions_total: set[str] = set()
    resolutions_by_split: dict[str, set[str]] = defaultdict(set)

    crop_path_missing = []
    split_crop_path_missing = []
    corrupt_images = []

    for row in rows:
        split_name = row["local_split"]
        source_id = row["source_image_id"]
        file_hash = row["file_hash"]
        resolution = f"{row.get('crop_width')}x{row.get('crop_height')}"

        source_ids_by_split[split_name].add(source_id)
        splits_by_source_id[source_id].add(split_name)
        hash_rows_by_split[(split_name, file_hash)].append(row)
        splits_by_hash[file_hash].add(split_name)
        resolutions_total.add(resolution)
        resolutions_by_split[split_name].add(resolution)

        crop_path = Path(row["crop_path"])
        split_crop_path = Path(row["split_crop_path"])
        if not crop_path.is_file():
            crop_path_missing.append(row["crop_path"])
        if not split_crop_path.is_file():
            split_crop_path_missing.append(row["split_crop_path"])
        else:
            is_valid, error = validate_image(split_crop_path)
            if not is_valid:
                corrupt_images.append(
                    {"split_crop_path": row["split_crop_path"], "error": error}
                )

    source_leakage = {
        source_id: sorted(splits)
        for source_id, splits in splits_by_source_id.items()
        if len(splits) > 1
    }
    duplicate_hash_within_split = {
        f"{split_name}:{file_hash}": [
            row["split_crop_path"] for row in duplicate_rows[:10]
        ]
        for (split_name, file_hash), duplicate_rows in hash_rows_by_split.items()
        if len(duplicate_rows) > 1
    }
    duplicate_hash_across_split = {
        file_hash: sorted(splits)
        for file_hash, splits in splits_by_hash.items()
        if len(splits) > 1
    }

    all_classes_in_all_splits = all(
        split_class_counts[(split_name, local_label)] > 0
        for split_name in SPLITS
        for local_label in expected_labels
    )
    expected_split_dirs_exist = all(
        split_counts[split_name] > 0 for split_name in SPLITS
    )

    blockers = []
    warnings = []
    if total_crop != EXPECTED_TOTAL_CROPS:
        blockers.append(
            f"Expected {EXPECTED_TOTAL_CROPS} total crops, found {total_crop}."
        )
    if not all_classes_in_all_splits:
        blockers.append("One or more active classes are missing from a split.")
    if not expected_split_dirs_exist:
        blockers.append("One or more local splits are empty.")
    if source_leakage:
        blockers.append("source_image_id leakage across local splits was found.")
    if duplicate_hash_across_split:
        blockers.append("Duplicate file_hash values across local splits were found.")
    if corrupt_images:
        blockers.append("Corrupt split crop files were found.")
    if split_crop_path_missing:
        blockers.append("Missing split crop files were found.")
    if split_counts["validation"] == 0:
        blockers.append("Validation set is empty.")
    if split_counts["test"] == 0:
        blockers.append("Test set is empty.")
    if crop_path_missing:
        warnings.append("Original crop_path files are missing.")
    if duplicate_hash_within_split:
        warnings.append("Duplicate file_hash values within a split were found.")

    ready_for_modelling = not blockers

    return {
        "total_crop": total_crop,
        "expected_labels": expected_labels,
        "crop_count_per_split": dict(split_counts),
        "crop_count_per_split_per_class": {
            split_name: {
                local_label: split_class_counts[(split_name, local_label)]
                for local_label in expected_labels
            }
            for split_name in SPLITS
        },
        "source_image_id_count_per_split": {
            split_name: len(source_ids_by_split[split_name])
            for split_name in SPLITS
        },
        "all_classes_in_all_splits": all_classes_in_all_splits,
        "duplicate_file_hash_within_split_count": len(duplicate_hash_within_split),
        "duplicate_file_hash_within_split_sample": dict(
            list(duplicate_hash_within_split.items())[:20]
        ),
        "duplicate_file_hash_across_split_count": len(duplicate_hash_across_split),
        "duplicate_file_hash_across_split_sample": dict(
            list(duplicate_hash_across_split.items())[:20]
        ),
        "source_image_id_leakage_across_split_count": len(source_leakage),
        "source_image_id_leakage_across_split_sample": dict(
            list(source_leakage.items())[:20]
        ),
        "crop_path_missing_count": len(crop_path_missing),
        "crop_path_missing_sample": crop_path_missing[:20],
        "split_crop_path_missing_count": len(split_crop_path_missing),
        "split_crop_path_missing_sample": split_crop_path_missing[:20],
        "corrupt_image_count": len(corrupt_images),
        "corrupt_images_sample": corrupt_images[:20],
        "unique_crop_resolutions_total": len(resolutions_total),
        "unique_crop_resolutions_per_split": {
            split_name: len(resolutions_by_split[split_name])
            for split_name in SPLITS
        },
        "actual_split_ratios": {
            split_name: round(split_counts[split_name] / total_crop, 6)
            if total_crop
            else 0
            for split_name in SPLITS
        },
        "blockers": blockers,
        "warnings": warnings,
        "ready_for_modelling": ready_for_modelling,
    }


def main() -> None:
    args = parse_args()
    expected_labels = load_expected_labels(args.class_config)
    rows = read_split_metadata(args.split_metadata_path)
    invalid_splits = sorted({row["local_split"] for row in rows} - set(SPLITS))
    if invalid_splits:
        raise ValueError(f"Invalid local_split values: {invalid_splits}")

    summary_rows = write_split_summary(args.split_summary_csv, rows, expected_labels)
    audit = build_audit(rows, expected_labels)
    audit["split_summary_csv"] = args.split_summary_csv.as_posix()
    audit["split_summary"] = summary_rows

    args.audit_json.parent.mkdir(parents=True, exist_ok=True)
    with args.audit_json.open("w", encoding="utf-8") as file:
        json.dump(audit, file, indent=2)

    print("Open Images IT asset split audit complete.")
    print(f"Audit JSON: {args.audit_json}")
    print(f"Split summary CSV: {args.split_summary_csv}")
    print(f"Total crops: {audit['total_crop']}")
    print(f"Ready for modelling: {audit['ready_for_modelling']}")
    if audit["blockers"]:
        print("Blockers:")
        for blocker in audit["blockers"]:
            print(f"- {blocker}")


if __name__ == "__main__":
    main()
