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

# ---------------------------
# API: list folders from S3 prefix
# ---------------------------
@app.get("/folders")
def list_folders():
    resp = s3.list_objects_v2(Bucket=S3_BUCKET, Delimiter="/")
    prefixes = [p["Prefix"] for p in resp.get("CommonPrefixes", [])]
    return jsonify({"folders": prefixes})

# ---------------------------
# API: upload file to selected folder
# ---------------------------
@app.post("/upload")
def upload():
    folder = request.form.get("folder", "").strip()
    if folder and not folder.endswith("/"):
        folder += "/"

    if "files" not in request.files:
        return jsonify({"error": "missing files"}), 400

    uploaded = []
    for f in request.files.getlist("files"):
        if f.filename.lower().endswith(".txt"):
            key = f"{folder}{f.filename}"
            s3.upload_fileobj(f, S3_BUCKET, key, ExtraArgs={"ContentType": "text/plain"})
            uploaded.append(key)

    job = agent_client.start_ingestion_job(
        knowledgeBaseId=KB_ID,
        dataSourceId=DS_ID
    )

    return jsonify({"uploaded": uploaded})

# ---------------------------
# API: ask KB
# ---------------------------
@app.post("/ask")
def ask():
    data = request.get_json()
    question = (data.get("question") or "").strip()

    resp = agent_runtime.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KB_ID,
                "modelArn": f"arn:aws:bedrock:{REGION}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
            }
        }
    )

    return jsonify({"answer": resp["output"]["text"]})

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
