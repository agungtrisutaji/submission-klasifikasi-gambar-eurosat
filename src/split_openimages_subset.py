"""Create local train/validation/test splits for Open Images IT asset crops.

The split is driven by metadata, not by scanning dataset/raw folders. This
prevents stale class folders from previous feasibility runs from entering the
local dataset. Source image IDs are treated as groups so every crop from the
same source image stays in exactly one local split.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import re
import shutil
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path
from typing import Any


SPLITS = ["train", "validation", "test"]
EXTRA_COLUMNS = ["local_split", "split_crop_path"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split Open Images IT asset crops with source_image_id grouping."
    )
    parser.add_argument(
        "--metadata-path",
        type=Path,
        default=Path("dataset") / "metadata" / "openimages_crop_metadata.csv",
        help="Input crop metadata CSV from build_openimages_subset.py.",
    )
    parser.add_argument(
        "--class-config",
        type=Path,
        default=Path("configs") / "openimages_it_assets_classes.json",
        help="Class config JSON containing active labels in the 'classes' field.",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("dataset") / "raw",
        help="Raw crop root. Used only to validate crop paths are local to the dataset.",
    )
    parser.add_argument(
        "--split-dir",
        type=Path,
        default=Path("dataset"),
        help="Dataset root where train/validation/test folders are created.",
    )
    parser.add_argument(
        "--split-metadata-path",
        type=Path,
        default=Path("dataset") / "metadata" / "openimages_split_metadata.csv",
        help="Output split metadata CSV path.",
    )
    parser.add_argument("--train-ratio", type=float, default=0.8)
    parser.add_argument("--validation-ratio", type=float, default=0.1)
    parser.add_argument("--test-ratio", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Remove dataset/train, dataset/validation, dataset/test, and split metadata.",
    )
    return parser.parse_args()


def validate_local_label(local_label: str) -> None:
    if not re.fullmatch(r"[a-z0-9][a-z0-9_]*", local_label):
        raise ValueError(
            "Invalid local_label. Use lowercase letters, numbers, and underscores "
            f"only, starting with a letter or number: {local_label!r}"
        )


def load_class_config(path: Path) -> OrderedDict[str, str]:
    if not path.exists():
        raise FileNotFoundError(f"Class config not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    class_items = config.get("classes")
    if not isinstance(class_items, list):
        raise ValueError("Class config field 'classes' must be a list.")

    class_map: OrderedDict[str, str] = OrderedDict()
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
        class_map[openimages_label] = local_label

    if not class_map:
        raise ValueError("Class config must contain at least one class.")

    return class_map


def read_metadata(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Metadata file not found: {path}")

    with path.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError(f"Metadata file is empty: {path}")

    required_columns = {
        "source_image_id",
        "source_split",
        "openimages_label",
        "local_label",
        "crop_path",
        "file_hash",
    }
    missing_columns = sorted(required_columns - set(rows[0].keys()))
    if missing_columns:
        raise ValueError(f"Metadata missing required columns: {missing_columns}")

    return rows


def validate_ratios(args: argparse.Namespace) -> dict[str, float]:
    ratios = {
        "train": args.train_ratio,
        "validation": args.validation_ratio,
        "test": args.test_ratio,
    }
    for split_name, ratio in ratios.items():
        if ratio <= 0:
            raise ValueError(f"{split_name} ratio must be positive: {ratio}")

    total_ratio = sum(ratios.values())
    if abs(total_ratio - 1.0) > 1e-6:
        raise ValueError(f"Split ratios must sum to 1.0, got {total_ratio}")

    return ratios


def prepare_output_dirs(
    split_dir: Path,
    split_metadata_path: Path,
    active_labels: list[str],
    overwrite: bool,
) -> None:
    if overwrite:
        for split_name in SPLITS:
            target_dir = split_dir / split_name
            if target_dir.exists():
                shutil.rmtree(target_dir)
        if split_metadata_path.exists():
            split_metadata_path.unlink()

    split_metadata_path.parent.mkdir(parents=True, exist_ok=True)
    for split_name in SPLITS:
        for local_label in active_labels:
            (split_dir / split_name / local_label).mkdir(parents=True, exist_ok=True)


def filter_and_validate_rows(
    rows: list[dict[str, str]],
    active_labels: list[str],
) -> list[dict[str, str]]:
    active_label_set = set(active_labels)
    active_rows = [row for row in rows if row["local_label"] in active_label_set]
    if not active_rows:
        raise ValueError("No metadata rows matched active labels from class config.")

    counts = Counter(row["local_label"] for row in active_rows)
    missing_labels = [label for label in active_labels if counts[label] == 0]
    if missing_labels:
        raise ValueError(f"Active labels with no metadata rows: {missing_labels}")

    missing_crop_paths = [
        row["crop_path"] for row in active_rows if not Path(row["crop_path"]).is_file()
    ]
    if missing_crop_paths:
        sample = missing_crop_paths[:10]
        raise FileNotFoundError(
            f"{len(missing_crop_paths)} crop_path files are missing. Sample: {sample}"
        )

    source_split_by_id: dict[str, set[str]] = defaultdict(set)
    for row in active_rows:
        source_split_by_id[row["source_image_id"]].add(row["source_split"])
    multi_source_split = {
        source_image_id: sorted(source_splits)
        for source_image_id, source_splits in source_split_by_id.items()
        if len(source_splits) > 1
    }
    if multi_source_split:
        sample = dict(list(multi_source_split.items())[:10])
        raise ValueError(
            "A source_image_id appears in multiple source_split values. "
            f"Sample: {sample}"
        )

    return active_rows


def build_groups(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["source_image_id"]].append(row)
    return dict(groups)


def assign_groups(
    groups: dict[str, list[dict[str, str]]],
    active_labels: list[str],
    ratios: dict[str, float],
    seed: int,
) -> dict[str, str]:
    rng = random.Random(seed)
    class_totals = Counter(row["local_label"] for rows in groups.values() for row in rows)
    targets = {
        split_name: {
            label: class_totals[label] * ratio for label in active_labels
        }
        for split_name, ratio in ratios.items()
    }
    current = {
        split_name: {label: 0 for label in active_labels}
        for split_name in SPLITS
    }
    group_label_counts = {
        source_image_id: Counter(row["local_label"] for row in rows)
        for source_image_id, rows in groups.items()
    }
    groups_by_label: dict[str, list[str]] = defaultdict(list)
    for source_image_id, label_counts in group_label_counts.items():
        for label in label_counts:
            groups_by_label[label].append(source_image_id)

    assignments: dict[str, str] = {}

    def choose_split(label_counts: Counter[str]) -> str:
        best_split = SPLITS[0]
        best_score: tuple[float, float, int] | None = None
        for split_index, split_name in enumerate(SPLITS):
            overfill = 0.0
            remaining_after = 0.0
            for label, count in label_counts.items():
                target = targets[split_name][label]
                after = current[split_name][label] + count
                overfill += max(0.0, after - target)
                remaining_after += target - after
            score = (overfill, -remaining_after, split_index)
            if best_score is None or score < best_score:
                best_score = score
                best_split = split_name
        return best_split

    for label in active_labels:
        source_ids = [source_id for source_id in groups_by_label[label] if source_id not in assignments]
        rng.shuffle(source_ids)
        for source_image_id in source_ids:
            label_counts = group_label_counts[source_image_id]
            split_name = choose_split(label_counts)
            assignments[source_image_id] = split_name
            for current_label, count in label_counts.items():
                current[split_name][current_label] += count

    unassigned = [source_id for source_id in groups if source_id not in assignments]
    rng.shuffle(unassigned)
    for source_image_id in unassigned:
        label_counts = group_label_counts[source_image_id]
        split_name = choose_split(label_counts)
        assignments[source_image_id] = split_name
        for current_label, count in label_counts.items():
            current[split_name][current_label] += count

    return assignments


def copy_crops_and_write_metadata(
    groups: dict[str, list[dict[str, str]]],
    assignments: dict[str, str],
    split_dir: Path,
    split_metadata_path: Path,
    active_labels: list[str],
) -> list[dict[str, str]]:
    split_rows: list[dict[str, str]] = []
    fieldnames: list[str] | None = None

    for source_image_id in sorted(groups):
        split_name = assignments[source_image_id]
        for row in groups[source_image_id]:
            crop_path = Path(row["crop_path"])
            local_label = row["local_label"]
            if local_label not in active_labels:
                continue

            split_crop_path = split_dir / split_name / local_label / crop_path.name
            shutil.copy2(crop_path, split_crop_path)

            split_row = dict(row)
            split_row["local_split"] = split_name
            split_row["split_crop_path"] = split_crop_path.as_posix()
            split_rows.append(split_row)

            if fieldnames is None:
                fieldnames = list(row.keys()) + EXTRA_COLUMNS

    if fieldnames is None:
        raise ValueError("No split rows were produced.")

    with split_metadata_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(split_rows)

    return split_rows


def main() -> None:
    args = parse_args()
    ratios = validate_ratios(args)
    class_map = load_class_config(args.class_config)
    active_labels = list(class_map.values())
    rows = read_metadata(args.metadata_path)
    active_rows = filter_and_validate_rows(rows, active_labels)

    prepare_output_dirs(
        split_dir=args.split_dir,
        split_metadata_path=args.split_metadata_path,
        active_labels=active_labels,
        overwrite=args.overwrite,
    )

    groups = build_groups(active_rows)
    assignments = assign_groups(groups, active_labels, ratios, args.seed)
    split_rows = copy_crops_and_write_metadata(
        groups=groups,
        assignments=assignments,
        split_dir=args.split_dir,
        split_metadata_path=args.split_metadata_path,
        active_labels=active_labels,
    )

    split_counts = Counter(row["local_split"] for row in split_rows)
    class_split_counts = Counter(
        (row["local_split"], row["local_label"]) for row in split_rows
    )

    print("Open Images IT asset split complete.")
    print(f"Split metadata: {args.split_metadata_path}")
    print(f"Total crops: {len(split_rows)}")
    for split_name in SPLITS:
        print(f"- {split_name}: {split_counts[split_name]}")
        for local_label in active_labels:
            print(f"  - {local_label}: {class_split_counts[(split_name, local_label)]}")


if __name__ == "__main__":
    main()
