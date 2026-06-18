"""Audit the exploratory Open Images V7 IT asset crop subset.

The audit reads dataset/metadata/openimages_crop_metadata.csv, validates crop
files, summarizes class counts and resolution diversity, and writes JSON/CSV
artifacts under outputs/dataset_audit/.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TARGET_LOCAL_LABELS = [
    "laptop",
    "computer_keyboard",
    "computer_mouse",
    "mobile_phone",
    "printer",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit an exploratory Open Images V7 IT asset crop subset."
    )
    parser.add_argument(
        "--class-config",
        type=Path,
        default=None,
        help=(
            "Optional JSON class config. When provided, expected labels are read "
            "from the 'classes' field instead of the built-in fallback labels."
        ),
    )
    parser.add_argument(
        "--metadata-path",
        type=Path,
        default=Path("dataset") / "metadata" / "openimages_crop_metadata.csv",
        help="Metadata CSV created by build_openimages_subset.py.",
    )
    parser.add_argument(
        "--audit-json",
        type=Path,
        default=Path("outputs")
        / "dataset_audit"
        / "openimages_subset_audit.json",
        help="Output audit JSON path.",
    )
    parser.add_argument(
        "--resolution-summary-csv",
        type=Path,
        default=Path("outputs")
        / "dataset_audit"
        / "openimages_resolution_summary.csv",
        help="Output resolution summary CSV path.",
    )
    parser.add_argument(
        "--min-crops-per-class",
        type=int,
        default=100,
        help="Minimum crop count per class for exploratory acceptance.",
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


def load_expected_labels(class_config_path: Path | None) -> list[str]:
    if class_config_path is None:
        return TARGET_LOCAL_LABELS.copy()

    if not class_config_path.exists():
        raise FileNotFoundError(f"Class config not found: {class_config_path}")

    with class_config_path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    class_items = config.get("classes")
    if not isinstance(class_items, list):
        raise ValueError("Class config field 'classes' must be a list.")

    expected_labels: list[str] = []
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
        expected_labels.append(local_label)

    if not expected_labels:
        raise ValueError("Class config must contain at least one class.")

    return expected_labels


def read_metadata(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {path}. Run src/build_openimages_subset.py first."
        )

    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def parse_int(value: str, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def numeric_summary(values: list[int]) -> dict[str, float | int | None]:
    if not values:
        return {
            "min": None,
            "max": None,
            "mean": None,
            "median": None,
        }

    return {
        "min": min(values),
        "max": max(values),
        "mean": round(statistics.fmean(values), 4),
        "median": statistics.median(values),
    }


def validate_crop(path: Path) -> tuple[bool, str | None, tuple[int, int] | None]:
    Image, UnidentifiedImageError = import_pillow()
    try:
        image = Image.open(path)
        image.load()
        return True, None, image.size
    except (OSError, UnidentifiedImageError) as error:
        return False, str(error), None


def summarize_resolutions(
    rows: list[dict[str, str]], expected_labels: list[str]
) -> list[dict[str, Any]]:
    summary_rows: list[dict[str, Any]] = []
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["local_label"]].append(row)

    for local_label in expected_labels:
        class_rows = grouped.get(local_label, [])
        crop_widths = [parse_int(row.get("crop_width", "")) for row in class_rows]
        crop_heights = [parse_int(row.get("crop_height", "")) for row in class_rows]
        source_widths = [parse_int(row.get("source_width", "")) for row in class_rows]
        source_heights = [parse_int(row.get("source_height", "")) for row in class_rows]
        resolutions = {
            (parse_int(row.get("crop_width", "")), parse_int(row.get("crop_height", "")))
            for row in class_rows
        }

        crop_width_summary = numeric_summary(crop_widths)
        crop_height_summary = numeric_summary(crop_heights)
        source_width_summary = numeric_summary(source_widths)
        source_height_summary = numeric_summary(source_heights)

        summary_rows.append(
            {
                "local_label": local_label,
                "crop_count": len(class_rows),
                "unique_crop_resolutions": len(resolutions),
                "crop_width_min": crop_width_summary["min"],
                "crop_width_max": crop_width_summary["max"],
                "crop_width_mean": crop_width_summary["mean"],
                "crop_width_median": crop_width_summary["median"],
                "crop_height_min": crop_height_summary["min"],
                "crop_height_max": crop_height_summary["max"],
                "crop_height_mean": crop_height_summary["mean"],
                "crop_height_median": crop_height_summary["median"],
                "source_width_min": source_width_summary["min"],
                "source_width_max": source_width_summary["max"],
                "source_width_mean": source_width_summary["mean"],
                "source_width_median": source_width_summary["median"],
                "source_height_min": source_height_summary["min"],
                "source_height_max": source_height_summary["max"],
                "source_height_mean": source_height_summary["mean"],
                "source_height_median": source_height_summary["median"],
            }
        )

    return summary_rows


def write_resolution_summary(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "local_label",
        "crop_count",
        "unique_crop_resolutions",
        "crop_width_min",
        "crop_width_max",
        "crop_width_mean",
        "crop_width_median",
        "crop_height_min",
        "crop_height_max",
        "crop_height_mean",
        "crop_height_median",
        "source_width_min",
        "source_width_max",
        "source_width_mean",
        "source_width_median",
        "source_height_min",
        "source_height_max",
        "source_height_mean",
        "source_height_median",
    ]
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_audit(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
    expected_labels: list[str],
) -> dict[str, Any]:
    class_counts = Counter(row["local_label"] for row in rows)
    crop_resolution_counter = Counter(
        f"{parse_int(row.get('crop_width', ''))}x{parse_int(row.get('crop_height', ''))}"
        for row in rows
    )
    file_hash_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    source_split_groups: dict[str, set[str]] = defaultdict(set)

    corrupt_images = []
    size_mismatches = []

    for row in rows:
        crop_path = Path(row["crop_path"])
        is_valid, error, actual_size = validate_crop(crop_path)
        if not is_valid:
            corrupt_images.append({"crop_path": row["crop_path"], "error": error})
            continue

        expected_size = (
            parse_int(row.get("crop_width", "")),
            parse_int(row.get("crop_height", "")),
        )
        if actual_size != expected_size:
            size_mismatches.append(
                {
                    "crop_path": row["crop_path"],
                    "expected_size": expected_size,
                    "actual_size": actual_size,
                }
            )

        file_hash_groups[row["file_hash"]].append(row)
        source_split_groups[row["source_image_id"]].add(row["source_split"])

    duplicate_hash_groups = {
        file_hash: group for file_hash, group in file_hash_groups.items() if len(group) > 1
    }
    duplicate_across_classes = {
        file_hash: sorted({row["local_label"] for row in group})
        for file_hash, group in duplicate_hash_groups.items()
        if len({row["local_label"] for row in group}) > 1
    }
    source_ids_in_multiple_source_splits = {
        source_image_id: sorted(source_splits)
        for source_image_id, source_splits in source_split_groups.items()
        if len(source_splits) > 1
    }

    unique_crop_resolutions = len(crop_resolution_counter)
    all_target_classes_present = all(
        class_counts.get(local_label, 0) > 0 for local_label in expected_labels
    )
    classes_meet_exploration_minimum = all(
        class_counts.get(local_label, 0) >= args.min_crops_per_class
        for local_label in expected_labels
    )
    resolution_non_uniform = unique_crop_resolutions > 1

    blockers = []
    warnings = []
    if not all_target_classes_present:
        blockers.append("One or more target classes have zero crops.")
    if not classes_meet_exploration_minimum:
        blockers.append(
            f"One or more classes have fewer than {args.min_crops_per_class} crops."
        )
    if corrupt_images:
        blockers.append("Corrupt crop files were found.")
    if not resolution_non_uniform:
        blockers.append("Crop resolutions are still uniform.")
    if source_ids_in_multiple_source_splits:
        blockers.append("The same source_image_id appears in multiple source splits.")
    if size_mismatches:
        warnings.append("Some crop metadata sizes differ from actual image sizes.")
    if duplicate_hash_groups:
        warnings.append("Duplicate crop hashes were found and should be reviewed.")
    if duplicate_across_classes:
        warnings.append("Duplicate crop hashes across classes were found.")

    return {
        "metadata_path": args.metadata_path.as_posix(),
        "total_crop_rows": len(rows),
        "target_classes": expected_labels,
        "class_counts": dict(class_counts),
        "unique_crop_resolutions": unique_crop_resolutions,
        "top_crop_resolutions": dict(crop_resolution_counter.most_common(20)),
        "corrupt_image_count": len(corrupt_images),
        "corrupt_images": corrupt_images[:50],
        "size_mismatch_count": len(size_mismatches),
        "size_mismatches": size_mismatches[:50],
        "duplicate_hash_group_count": len(duplicate_hash_groups),
        "duplicate_crop_count": sum(len(group) for group in duplicate_hash_groups.values()),
        "duplicate_hashes_sample": {
            file_hash: [
                {
                    "local_label": row["local_label"],
                    "crop_path": row["crop_path"],
                    "source_image_id": row["source_image_id"],
                }
                for row in group[:10]
            ]
            for file_hash, group in list(duplicate_hash_groups.items())[:20]
        },
        "duplicate_across_classes_group_count": len(duplicate_across_classes),
        "duplicate_across_classes_sample": dict(
            list(duplicate_across_classes.items())[:20]
        ),
        "source_ids_in_multiple_source_splits_count": len(
            source_ids_in_multiple_source_splits
        ),
        "source_ids_in_multiple_source_splits_sample": dict(
            list(source_ids_in_multiple_source_splits.items())[:20]
        ),
        "local_split_created": False,
        "cross_local_split_leakage_checked": False,
        "is_crop_resolution_non_uniform": resolution_non_uniform,
        "classes_meet_exploration_minimum": classes_meet_exploration_minimum,
        "ready_for_full_scale_dataset_build": not blockers,
        "blockers": blockers,
        "warnings": warnings,
        "recommendation": (
            "Dataset exploration is ready to continue to full-scale build."
            if not blockers
            else "Fix blockers before full-scale dataset build."
        ),
    }


def main() -> None:
    args = parse_args()
    expected_labels = load_expected_labels(args.class_config)
    rows = read_metadata(args.metadata_path)

    resolution_rows = summarize_resolutions(rows, expected_labels)
    write_resolution_summary(args.resolution_summary_csv, resolution_rows)

    audit = build_audit(rows, args, expected_labels)
    args.audit_json.parent.mkdir(parents=True, exist_ok=True)
    with args.audit_json.open("w", encoding="utf-8") as file:
        json.dump(audit, file, indent=2)

    print("Open Images IT asset exploratory subset audit complete.")
    print(f"Audit JSON: {args.audit_json}")
    print(f"Resolution summary CSV: {args.resolution_summary_csv}")
    print(f"Total crops: {audit['total_crop_rows']}")
    print(f"Ready for full scale: {audit['ready_for_full_scale_dataset_build']}")
    if audit["blockers"]:
        print("Blockers:")
        for blocker in audit["blockers"]:
            print(f"- {blocker}")


if __name__ == "__main__":
    main()
