import os
import shutil
import zipfile
from pathlib import Path

def package_submission():
    root_dir = Path(__file__).resolve().parent.parent
    sub_dir = root_dir / "submission_it_assets"
    zip_path = root_dir / "submission_it_assets.zip"

    print("=== Packaging Submission ===")
    
    # 1. Clean up old packaging
    if sub_dir.exists():
        shutil.rmtree(sub_dir)
    if zip_path.exists():
        zip_path.unlink()
        
    sub_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Files to copy directly
    files_to_copy = [
        "klasifikasi-gambar-it-assets.ipynb",
        "README.md",
        "requirements.txt",
        "label.txt",
        "AGENTS.md"
    ]
    
    for f in files_to_copy:
        src = root_dir / f
        if src.exists():
            shutil.copy2(src, sub_dir / f)
            print(f"Copied file: {f}")
        else:
            print(f"Warning: direct file {f} not found!")

    # 3. Folders to copy
    folders_to_copy = {
        "configs": None, # Copy entire folder
        "notes": None,   # Copy entire folder
        "src": lambda p: "__pycache__" not in p and "package_submission" not in p,
        "saved_model/it_asset_classifier": None,
        "tflite": lambda p: "eurosat" not in p,
        "tfjs/it_asset_classifier": None,
        "outputs/dataset_audit": lambda p: "openimages" not in p and "source_process" not in p,
        "outputs/evaluation": lambda p: p.startswith("sequential_") or p.startswith("sample_")
    }

    for folder, filter_func in folders_to_copy.items():
        src_path = root_dir / folder
        dst_path = sub_dir / folder
        if src_path.exists():
            dst_path.mkdir(parents=True, exist_ok=True)
            for item in src_path.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(src_path)
                    # Apply filter
                    if filter_func and not filter_func(str(rel_path).replace("\\", "/")):
                        continue
                    item_dst = dst_path / rel_path
                    item_dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, item_dst)
            print(f"Copied filtered folder: {folder}")
        else:
            print(f"Warning: folder {folder} not found!")

    # 4. Create ZIP archive
    print("\nCreating ZIP archive...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in sub_dir.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(sub_dir)
                zip_file.write(file_path, arcname=Path("submission_it_assets") / rel_path)
    
    zip_size_mb = zip_path.stat().st_size / 1024 / 1024
    print(f"ZIP Archive created: {zip_path.name} ({zip_size_mb:.2f} MB)")
    
    # 5. Validation Audit
    print("\n=== Validation Audit ===")
    print(f"Check ZIP size: {zip_size_mb:.2f} MB (Target: < 200 MB)")
    assert zip_size_mb < 200, "ZIP size is too large! Check for embedded dataset files."
    
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        namelist = zip_file.namelist()
        
        # Check required files
        required = [
            "submission_it_assets/klasifikasi-gambar-it-assets.ipynb",
            "submission_it_assets/saved_model/it_asset_classifier/saved_model.pb",
            "submission_it_assets/tflite/it_asset_classifier.tflite",
            "submission_it_assets/tfjs/it_asset_classifier/model.json"
        ]
        
        for req in required:
            if req in namelist:
                print(f"  OK: {req} is in ZIP")
            else:
                print(f"  ERROR: {req} is MISSING from ZIP!")
                
        # Check for dataset leak
        dataset_leaked = any("dataset/" in name for name in namelist)
        if dataset_leaked:
            print("  WARNING: Dataset files detected in ZIP! Please clean up.")
        else:
            print("  OK: No dataset files leaked into ZIP.")

if __name__ == "__main__":
    package_submission()
