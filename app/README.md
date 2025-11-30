# RAG Car Diagnostic Dashboard

A Flask-based web application for car diagnostic knowledge base management with RAG (Retrieval Augmented Generation) capabilities.

## Project Structure

```
app/
├── Dockerfile                 # Docker configuration (for entire app)
├── requirements.txt          # Python dependencies (for entire app)
├── README.md                 # Project documentation
│
├── backend/                  # Backend application code
│   ├── app.py               # Main Flask application
│   └── system-prompt.txt    # System prompt configuration
│
└── frontend/                 # Frontend assets
    ├── templates/           # HTML templates
    │   ├── base.html       # Base template with gauges and layout
    │   ├── index.html      # Main page (ask questions, upload docs)
    │   └── about.html      # About page
    └── static/             # Static assets
        └── css/
            └── main.css    # Main stylesheet

```

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd app
```

### 2. Configure environment variables

Copy the example environment file and update with your AWS credentials:

```bash
cp .env.example .env
```

Then edit `.env` with your actual values:
- `KB_ID` - Your AWS Bedrock Knowledge Base ID
- `DS_ID` - Your AWS Bedrock Data Source ID
- `S3_BUCKET` - Your S3 bucket name
- `REGION` - AWS region (default: us-east-1)

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Locally (from app directory):

```bash
python backend/app.py
```

The application will start on `http://localhost:8000`

### Using Docker:

```bash
docker build -t rag-app .
docker run -p 8000:8000 rag-app
```

## Features

- **Ask Questions**: Query the knowledge base and get answers
- **Upload Documents**: Upload .txt files to organize knowledge base folders
- **Refresh KB**: Trigger knowledge base ingestion after uploads
- **Animated Gauges**: Car-themed dashboard with animated gauge decorations

## Tech Stack

- **Backend**: Python, Flask, AWS Bedrock, AWS S3
- **Frontend**: HTML, CSS, JavaScript
- **Cloud**: AWS Bedrock Knowledge Base
