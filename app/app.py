import os
import boto3
from flask import Flask, request, jsonify, render_template

# ---------------------------
# Config
# ---------------------------
S3_BUCKET = "aicourse-lesson7-clay227"
SYSTEM_PROMPT_PATH = os.environ.get("SYSTEM_PROMPT_FILE", "system_prompt.txt")

DEFAULT_KB_ID = os.environ.get("KNOWLEDGE_BASE_ID", "")
DEFAULT_DS_ID = os.environ.get("DATA_SOURCE_ID", "")

deb_client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
agent_client = boto3.client("bedrock-agent", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")

app = Flask(__name__)


# ---------------------------
# Load System Prompt
# ---------------------------
def load_system_prompt():
    if not os.path.exists(SYSTEM_PROMPT_PATH):
        return ""
    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


SYSTEM_PROMPT = load_system_prompt()


# ---------------------------
# Helpers
# ---------------------------
def list_prefixes(prefix):
    resp = s3.list_objects_v2(
        Bucket=S3_BUCKET,
        Prefix=prefix,
        Delimiter="/"
    )
    return resp.get("CommonPrefixes", [])


def get_ids(req):
    kb_id = req.args.get("kbId") or DEFAULT_KB_ID
    ds_id = req.args.get("dsId") or DEFAULT_DS_ID

    if not kb_id or not ds_id:
        raise ValueError("kbId and dsId are mandatory (either as query params or ENV).")

    return kb_id, ds_id


# ---------------------------
# Pages
# ---------------------------
@app.get("/")
def home():
    return render_template("index.html")


# ---------------------------
# API: Health
# ---------------------------
@app.get("/health")
def health():
    return jsonify({"status": "ok"})


# ---------------------------
# API: KB Folders
# ---------------------------
@app.get("/kb-folders")
def kb_folders():
    folders = []
    stack = ["KB/"]

    while stack:
        current = stack.pop()
        prefixes = list_prefixes(current)
        for p in prefixes:
            folder = p["Prefix"]
            folders.append(folder)
            stack.append(folder)

    return jsonify({"folders": folders})


# ---------------------------
# API: Upload
# ---------------------------
@app.post("/upload")
def upload():
    try:
        kb_id, ds_id = get_ids(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if "files" not in request.files:
        return jsonify({"error": "Send file(s) under 'files'"}), 400

    rel_path = (request.args.get("path") or "").strip()
    if not rel_path:
        return jsonify({"error": "Provide ?path=<folder>"}), 400

    rel_path = rel_path.lstrip("/")
    files = request.files.getlist("files")
    saved = []

    for f in files:
        if not f.filename:
            continue
        key = f"KB/{rel_path}/{f.filename}"

        s3.upload_fileobj(
            f,
            S3_BUCKET,
            key,
            ExtraArgs={"ContentType": "text/plain"}
        )
        saved.append(key)

    # Check if ingestion is running
    jobs = agent_client.list_ingestion_jobs(
        knowledgeBaseId=kb_id,
        dataSourceId=ds_id
    )

    for job in jobs.get("ingestionJobSummaries", []):
        if job["status"] in ["STARTING", "IN_PROGRESS"]:
            return jsonify({"error": "Ingestion already in progress"}), 409

    # Start ingestion
    job = agent_client.start_ingestion_job(
        knowledgeBaseId=kb_id,
        dataSourceId=ds_id
    )

    return jsonify({
        "saved": saved,
        "count": len(saved),
        "job": job
    })


# ---------------------------
# API: Ingestion Status
# ---------------------------
@app.get("/ingestion-status")
def ingestion_status():
    try:
        kb_id, ds_id = get_ids(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    job_id = request.args.get("jobId")
    if not job_id:
        return jsonify({"error": "Missing jobId"}), 400

    status = agent_client.get_ingestion_job(
        knowledgeBaseId=kb_id,
        dataSourceId=ds_id,
        ingestionJobId=job_id
    )

    return jsonify({"status": status["ingestionJob"]["status"]})


# ---------------------------
# API: Ask KB
# ---------------------------
@app.post("/ask")
def ask():
    try:
        kb_id, ds_id = get_ids(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    data = request.get_json(force=True, silent=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"error": "Provide question"}), 400

    response = deb_client.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": kb_id,
                "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.hiku-3.5"
            }
        },
        promptOverride={
            "system": SYSTEM_PROMPT
        }
    )

    return jsonify({
        "question": question,
        "answer": response["output"]["text"]
    })


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
