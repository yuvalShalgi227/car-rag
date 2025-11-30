import os
from flask import Flask, request, jsonify, render_template
import boto3

# ---------------------------
# Env config
# ---------------------------
REGION = os.environ.get("REGION", "us-east-1")
KB_ID = os.environ.get("KB_ID", "TVUWZMEJQ2")
DS_ID = os.environ.get("DS_ID", "MD435CFF3F")
S3_BUCKET = os.environ.get("S3_BUCKET", "aicourse-lesson7-clay227")

# ---------------------------
# AWS clients
# ---------------------------
s3 = boto3.client("s3", region_name=REGION)
agent_runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)
agent_client = boto3.client("bedrock-agent", region_name=REGION)

# ---------------------------
# Flask
# ---------------------------
app = Flask(__name__)

# ---------------------------
# Page
# ---------------------------
@app.get("/")
def index():
    return render_template("index.html")



@app.post("/ingest")
def ingest():
    job = agent_client.start_ingestion_job(
        knowledgeBaseId=KB_ID,
        dataSourceId=DS_ID
    )
    return jsonify({"jobId": job["ingestionJob"]["ingestionJobId"]})

@app.get("/ingest_status")
def ingest_status():
    job_id = request.args.get("jobId")
    if not job_id:
        return jsonify({"error": "missing jobId"}), 400

    try:
        res = agent_client.get_ingestion_job(
            knowledgeBaseId=KB_ID,
            dataSourceId=DS_ID,
            ingestionJobId=job_id
        )

        print("INGESTION STATUS RAW:", res)

        status = res["ingestionJob"]["status"]
        return jsonify({"status": status})

    except Exception as e:
        print("ERROR IN STATUS CHECK:", str(e))
        return jsonify({"status": "ERROR", "detail": str(e)})

# ---------------------------
# API: upload file to selected folder
# ---------------------------
@app.post("/upload")
def upload():
    folder = request.form.get("folder", "").strip()
    print(f"start upload to folder: {folder}")
    if folder and not folder.endswith("/"):
        folder += "/"

    if "files" not in request.files:
        return jsonify({"error": "missing files"}), 400

    uploaded = []
    for f in request.files.getlist("files"):
        print(f"uploading {f.filename}")
        if f.filename.lower().endswith(".txt"):
            key = f"{folder}{f.filename}"
            s3.upload_fileobj(f, S3_BUCKET, key, ExtraArgs={"ContentType": "text/plain"})
            uploaded.append(key)

    job = agent_client.start_ingestion_job(
        knowledgeBaseId=KB_ID,
        dataSourceId=DS_ID
    )

    return jsonify({"uploaded": uploaded})

@app.get("/folders")
def get_folders():
    prefixes = set()
    all_keys = []

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=S3_BUCKET):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            all_keys.append(key)

    # Build folder structure
    for key in all_keys:
        parts = key.split("/")[:-1]  # remove filename
        for i in range(1, len(parts) + 1):
            prefix = "/".join(parts[:i])
            prefixes.add(prefix)

    folders = sorted(prefixes)
    return jsonify({"folders": folders})

# ---------------------------
# API: ask KB
# ---------------------------
@app.post("/ask")
def ask():
    data = request.get_json()
    question = (data.get("question") or "").strip()

    # Custom system prompt for brief, direct answers
    system_prompt = """Always answer briefly and directly. Do not mention sources, the knowledge base, or how you derived the answer. Just state the fact."""

    resp = agent_runtime.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KB_ID,
                "modelArn": f"arn:aws:bedrock:{REGION}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
                "generationConfiguration": {
                    "promptTemplate": {
                        "textPromptTemplate": f"""{system_prompt}

$search_results$

User question: $query$

Answer:"""
                    }
                }
            }
        }
    )

    return jsonify({"answer": resp["output"]["text"]})

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
