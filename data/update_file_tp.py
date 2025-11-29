import os
import json
from pathlib import Path
import boto3


def write_readme(path: Path, text: str):
    (path / "README.txt").write_text(text, encoding="utf-8")


def create_tire_pressure_files(base_path: str):
    base = Path(base_path)
    tire_dir = base / "tire_pressure"
    tire_dir.mkdir(parents=True, exist_ok=True)

    # README
    readme_text = (
        "This folder contains structured tire pressure data for all supported vehicles.\n"
        "The file 'tire_pressures.json' stores all tire pressure values in a single place.\n"
        "Format:\n"
        "{\n"
        "   \"Manufacturer_Model_Year\": {\n"
        "       \"front\": \"XX psi\",\n"
        "       \"rear\": \"YY psi\"\n"
        "   }\n"
        "}\n"
        "LLM Note: This is a high-frequency lookup dataset used for fast tire pressure answers."
    )
    write_readme(tire_dir, readme_text)

    # Example data — you can expand this as needed
    tire_data = {
        "Toyota_Corolla_2018": {
            "front": "33 psi",
            "rear": "32 psi"
        },
        "Mazda_3_2016": {
            "front": "36 psi",
            "rear": "34 psi"
        },
        "Hyundai_i20_2019": {
            "front": "32 psi",
            "rear": "30 psi"
        }
    }

    json_path = tire_dir / "tire_pressures.json"
    json_path.write_text(json.dumps(tire_data, indent=4), encoding="utf-8")

    print("Created tire pressure folder and files.")


def upload_tire_pressure_to_s3(local_folder: str, bucket: str):
    s3_client = boto3.client("s3")

    local_path = Path(local_folder).resolve()
    bucket_prefix = "KB/tire_pressure"

    for root, dirs, files in os.walk(local_path):
        for file in files:
            full_local = Path(root) / file
            relative = full_local.relative_to(local_path)
            s3_key = f"{bucket_prefix}/{relative.as_posix()}"

            s3_client.upload_file(str(full_local), bucket, s3_key)
            print(f"Uploaded: {full_local} → s3://{bucket}/{s3_key}")


# === RUN ===

base_kb = "knowledge_base"
bucket_name = "aicourse-lesson7-clay227"

create_tire_pressure_files(base_kb)
upload_tire_pressure_to_s3(f"{base_kb}/tire_pressure", bucket_name)
