import boto3
import os
from pathlib import Path

def upload_folder_to_s3(local_folder: str, bucket_name: str, s3_prefix: str):
    """
    Uploads an entire folder (with subdirectories) to an S3 bucket.
    Preserves the folder structure under the given S3 prefix.
    """

    s3_client = boto3.client("s3")
    local_folder_path = Path(local_folder).resolve()

    for root, dirs, files in os.walk(local_folder_path):
        for file in files:
            full_local_path = Path(root) / file

            # Compute the S3 path while preserving folder structure
            relative_path = full_local_path.relative_to(local_folder_path)
            s3_path = f"{s3_prefix}/{relative_path.as_posix()}"

            s3_client.upload_file(str(full_local_path), bucket_name, s3_path)

            print(f"Uploaded: {full_local_path} → s3://{bucket_name}/{s3_path}")


# === Usage ===
local_kb_folder = "knowledge_base"
bucket_name = "aicourse-lesson7-clay227"
s3_prefix = "KB"

upload_folder_to_s3(local_kb_folder, bucket_name, s3_prefix)
