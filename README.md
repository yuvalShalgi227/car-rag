# RAG Car Diagnostic Dashboard

An AI-powered automotive assistant that helps you manage your car and resolve issues using Retrieval-Augmented Generation (RAG) technology powered by AWS Bedrock.

## What is This Project?

This is an **intelligent automotive knowledge base** that uses AI to answer your car-related questions. Think of it as having an expert mechanic available 24/7 to help you with:

- 🚨 **Warning Light Identification** - "What does this dashboard light mean?"
- 🔧 **Maintenance Information** - "What's the correct tire pressure for my car?"
- 📖 **Owner's Manual Queries** - "How do I change the cabin air filter?"
- 📊 **Vehicle Specifications** - "What type of oil does my car need?"
- ⚠️ **Safety Guidance** - Get immediate advice on whether it's safe to drive

The system uses **RAG (Retrieval-Augmented Generation)** to search through automotive manuals, specifications, and warning light databases to provide accurate, fact-based answers instead of guessing or hallucinating information.


### Technology Stack

- **Frontend**: HTML, CSS, JavaScript with animated car dashboard gauges
- **Backend**: Python Flask application
- **AI/ML**: AWS Bedrock
- **Storage**: AWS S3 for document storage
- **Knowledge Base**: AWS Bedrock Knowledge Base with RAG
- **Vector Search**: Open search


## AWS Bedrock Knowledge Base Setup
### How the Knowledge Base Works

1. **Document Ingestion**:
   - Upload documents (.txt files) to S3 bucket
   - Trigger ingestion job in Bedrock Knowledge Base
   - Documents are automatically chunked and embedded into vector representations

2. **Query Processing**:
   - User asks a question through the web interface
   - The question is embedded into a vector
   - Bedrock searches for semantically similar document chunks
   - Retrieved chunks are sent to Claude AI as context
   - Claude generates an answer based on the retrieved information

3. **Answer Generation**:
   - Claude uses the system prompt (in `backend/system-prompt.txt`) to guide response style
   - Answers are concise, factual, and safety-focused
   - No hallucinations - only information from the knowledge base

## Key Features

### 🎯 Accurate Information
- Answers are grounded in actual vehicle documentation
- No guessing or making up information
- Clear indication when information is not available

### 🔒 Safety First
- Priority on safety-critical information (brakes, oil pressure, overheating)
- Clear warnings about when NOT to drive
- Severity and urgency levels for warning lights

### 📚 Comprehensive Coverage
- Owner's manuals from multiple manufacturers
- Technical specifications
- Warning light database with severity levels
- Maintenance schedules and procedures

### 🚀 Easy to Use
- Clean, car-themed dashboard interface
- Simple question-and-answer format
- Upload new documents through the web interface
- Real-time knowledge base updates

## Getting Started

### Prerequisites

- Python 3.12+
- AWS Account with Bedrock access
- AWS S3 bucket
- AWS Bedrock Knowledge Base configured

### Quick Start

1. Navigate to the `app/` folder
2. Follow the setup instructions in `app/README.md`
3. Configure your `.env` file with AWS credentials
4. Run the application

```bash
cd app
python backend/app.py
```

Visit `http://localhost:8000` to start using the dashboard.

## Project Structure

```
rag_project_kb/
├── README.md              # This file - Project overview
├── app/                   # Web application
│   ├── backend/          # Flask backend application
│   ├── frontend/         # HTML/CSS/JS frontend
│   ├── .env.example      # Environment variables template
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Docker configuration
│
└── data/                 # Example S3 structure
    └── KB/              # Knowledge Base content
        ├── manuals/     # Owner's manuals by manufacturer
        ├── specs/       # Vehicle specifications
        └── manufacturers/ # Manufacturer-specific data
```

## Data Folder

The `data/` folder contains an **example of the S3 bucket structure** used by the AWS Bedrock Knowledge Base. This shows how documents should be organized:

```
data/KB/
├── manuals/
│   ├── toyota/
│   │   └── camry_2024.txt
│   └── honda/
│       └── civic_2024.txt
├── specs/
│   ├── toyota/
│   │   └── camry_2024_specs.txt
│   └── honda/
│       └── civic_2024_specs.txt
└── manufacturers/
    └── general_info.txt
```

**Note**: The actual data is stored in AWS S3 and synced to the Bedrock Knowledge Base. The `data/` folder is just a reference structure.



## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built with AWS Bedrock


---

**Need Help?** Check out the `app/README.md` for detailed setup and configuration instructions.
