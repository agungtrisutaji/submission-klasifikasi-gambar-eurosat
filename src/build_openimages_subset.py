"""Build a small Open Images V7 IT asset classification subset.

This script downloads a small Open Images V7 detection subset with FiftyOne,
crops target object bounding boxes, and writes classification-ready crops to
dataset/raw/<local_label>/ plus metadata CSV.

It is intentionally scoped for exploration. It does not create train,
validation, or test splits and it does not train a model.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any


TARGET_CLASSES = OrderedDict(
    [
        ("Laptop", "laptop"),
        ("Computer keyboard", "computer_keyboard"),
        ("Computer mouse", "computer_mouse"),
        ("Mobile phone", "mobile_phone"),
        ("Printer", "printer"),
    ]
)

METADATA_COLUMNS = [
    "source_image_id",
    "source_split",
    "openimages_label",
    "local_label",
    "bbox_x",
    "bbox_y",
    "bbox_width",
    "bbox_height",
    "source_width",
    "source_height",
    "crop_width",
    "crop_height",
    "crop_path",
    "file_hash",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an exploratory Open Images V7 IT asset crop subset."
    )
    parser.add_argument(
        "--source-splits",
        nargs="+",
        default=["train"],
        choices=["train", "validation", "test"],
        help="Open Images source split(s) to sample from.",
    )
    parser.add_argument(
        "--target-crops-per-class",
        type=int,
        default=150,
        help="Stop after this many valid crops per target class.",
    )
    parser.add_argument(
        "--max-samples-per-class",
        type=int,
        default=500,
        help="Maximum FiftyOne samples to request per class and source split.",
    )
    parser.add_argument(
        "--min-crop-size",
        type=int,
        default=32,
        help="Skip crops whose width or height is smaller than this many pixels.",
    )
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("openimages_data"),
        help="Local FiftyOne/Open Images download directory. This path is ignored by git.",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("dataset") / "raw",
        help="Output directory for class crop folders.",
    )
    parser.add_argument(
        "--metadata-path",
        type=Path,
        default=Path("dataset") / "metadata" / "openimages_crop_metadata.csv",
        help="Output metadata CSV path.",
    )
    parser.add_argument(
        "--dataset-name-prefix",
        default="it-assets-openimages-explore",
        help="Temporary FiftyOne dataset name prefix.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for FiftyOne shuffle.",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=4,
        help="Number of workers for FiftyOne image download.",
    )
    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=95,
        help="JPEG quality for saved crops.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Remove existing crop folders for target labels and rewrite metadata.",
    )
    return parser.parse_args()


def import_fiftyone() -> tuple[Any, Any]:
    try:
        import fiftyone as fo
        import fiftyone.zoo as foz
    except ImportError as error:
        raise SystemExit(
            "FiftyOne is required. Install dependencies with: pip install -r requirements.txt"
        ) from error

    return fo, foz


def import_pillow() -> tuple[Any, Any]:
    try:
        from PIL import Image, UnidentifiedImageError
    except ImportError as error:
        raise SystemExit(
            "Pillow is required. Install dependencies with: pip install -r requirements.txt"
        ) from error

    return Image, UnidentifiedImageError


def sanitize_filename(value: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    return sanitized.strip("._") or "unknown"


def get_sample_field(sample: Any, field_names: list[str]) -> Any | None:
    for field_name in field_names:
        try:
            value = sample[field_name]
        except Exception:
            value = getattr(sample, field_name, None)
        if value not in (None, ""):
            return value
    return None


def get_source_image_id(sample: Any) -> str:
    image_id = get_sample_field(
        sample,
        [
            "open_images_id",
            "openimages_id",
            "OpenImagesID",
            "image_id",
            "ImageID",
        ],
    )
    if image_id:
        return str(image_id)
    return Path(sample.filepath).stem


def get_detections(sample: Any) -> list[Any]:
    detections = get_sample_field(sample, ["detections", "ground_truth"])
    if detections is None:
        return []
    return list(getattr(detections, "detections", []) or [])


def bbox_to_pixels(
    bbox: list[float], image_width: int, image_height: int
) -> tuple[int, int, int, int]:
    x, y, width, height = bbox
    left = round(x * image_width)
    top = round(y * image_height)
    right = round((x + width) * image_width)
    bottom = round((y + height) * image_height)

    left = max(0, min(left, image_width))
    top = max(0, min(top, image_height))
    right = max(0, min(right, image_width))
    bottom = max(0, min(bottom, image_height))

    return left, top, right, bottom


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_output_dirs(args: argparse.Namespace) -> None:
    args.metadata_path.parent.mkdir(parents=True, exist_ok=True)
    args.raw_dir.mkdir(parents=True, exist_ok=True)

    for local_label in TARGET_CLASSES.values():
        label_dir = args.raw_dir / local_label
        if args.overwrite and label_dir.exists():
            for image_path in label_dir.glob("*.jpg"):
                image_path.unlink()
        label_dir.mkdir(parents=True, exist_ok=True)


def load_openimages_subset(
    foz: Any,
    dataset_name: str,
    openimages_label: str,
    source_split: str,
    args: argparse.Namespace,
) -> Any:
    return foz.load_zoo_dataset(
        "open-images-v7",
        split=source_split,
        label_types=["detections"],
        classes=[openimages_label],
        only_matching=True,
        include_id=True,
        max_samples=args.max_samples_per_class,
        shuffle=True,
        seed=args.seed,
        dataset_name=dataset_name,
        num_workers=args.num_workers,
    )


def crop_class_from_dataset(
    dataset: Any,
    openimages_label: str,
    local_label: str,
    source_split: str,
    args: argparse.Namespace,
    existing_rows: list[dict[str, Any]],
    current_count: int,
) -> int:
    Image, UnidentifiedImageError = import_pillow()
    output_dir = args.raw_dir / local_label
    target_count = args.target_crops_per_class

    for sample in dataset:
        if current_count >= target_count:
            break

        try:
            image = Image.open(sample.filepath)
            image.load()
            image = image.convert("RGB")
        except (OSError, UnidentifiedImageError):
            continue

        source_width, source_height = image.size
        source_image_id = sanitize_filename(get_source_image_id(sample))

        for detection_index, detection in enumerate(get_detections(sample)):
            if current_count >= target_count:
                break

            if getattr(detection, "label", None) != openimages_label:
                continue

            bbox = getattr(detection, "bounding_box", None)
            if not bbox or len(bbox) != 4:
                continue

            bbox_x, bbox_y, bbox_width, bbox_height = [float(value) for value in bbox]
            if bbox_width <= 0 or bbox_height <= 0:
                continue

            left, top, right, bottom = bbox_to_pixels(
                [bbox_x, bbox_y, bbox_width, bbox_height],
                source_width,
                source_height,
            )
            crop_width = right - left
            crop_height = bottom - top
            if crop_width < args.min_crop_size or crop_height < args.min_crop_size:
                continue

            crop = image.crop((left, top, right, bottom))
            filename = (
                f"{local_label}_{source_split}_{source_image_id}_"
                f"{current_count + 1:05d}_{detection_index:03d}.jpg"
            )
            crop_path = output_dir / filename

            try:
                crop.save(crop_path, format="JPEG", quality=args.jpeg_quality)
            except OSError:
                continue

            file_hash = sha256_file(crop_path)
            existing_rows.append(
                {
                    "source_image_id": source_image_id,
                    "source_split": source_split,
                    "openimages_label": openimages_label,
                    "local_label": local_label,
                    "bbox_x": bbox_x,
                    "bbox_y": bbox_y,
                    "bbox_width": bbox_width,
                    "bbox_height": bbox_height,
                    "source_width": source_width,
                    "source_height": source_height,
                    "crop_width": crop_width,
                    "crop_height": crop_height,
                    "crop_path": crop_path.as_posix(),
                    "file_hash": file_hash,
                }
            )
            current_count += 1

    return current_count


def write_metadata(metadata_path: Path, rows: list[dict[str, Any]]) -> None:
    with metadata_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=METADATA_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    fo, foz = import_fiftyone()
    args.dataset_dir.mkdir(parents=True, exist_ok=True)
    fo.config.dataset_zoo_dir = str(args.dataset_dir.resolve())
    prepare_output_dirs(args)

    rows: list[dict[str, Any]] = []
    crop_counts = {local_label: 0 for local_label in TARGET_CLASSES.values()}

    for openimages_label, local_label in TARGET_CLASSES.items():
        for source_split in args.source_splits:
            if crop_counts[local_label] >= args.target_crops_per_class:
                break

            dataset_name = (
                f"{args.dataset_name_prefix}-"
                f"{sanitize_filename(source_split)}-"
                f"{sanitize_filename(local_label)}"
            )
            if fo.dataset_exists(dataset_name):
                fo.delete_dataset(dataset_name)

            dataset = load_openimages_subset(
                foz=foz,
                dataset_name=dataset_name,
                openimages_label=openimages_label,
                source_split=source_split,
                args=args,
            )

            crop_counts[local_label] = crop_class_from_dataset(
                dataset=dataset,
                openimages_label=openimages_label,
                local_label=local_label,
                source_split=source_split,
                args=args,
                existing_rows=rows,
                current_count=crop_counts[local_label],
            )

    write_metadata(args.metadata_path, rows)

    print("Open Images IT asset exploratory subset build complete.")
    print(f"Metadata: {args.metadata_path}")
    print(f"Total crops: {len(rows)}")
    for local_label, count in crop_counts.items():
        print(f"- {local_label}: {count}")
    print("No train/validation/test split was created in this stage.")


if __name__ == "__main__":
    main()
