# LQ-RAG Legal AI

> An AI-powered legal question-answering system that combines Retrieval-Augmented Generation (RAG), hybrid search, document analysis, and citation-aware responses for legal information.

## Overview

**LQ-RAG Legal AI** is a full-stack Legal AI application designed to help users ask questions about legal documents and retrieve grounded answers from a legal knowledge base.

The system supports two main workflows:

- **Document-specific Q&A** — upload a legal document and ask questions using only that document as context.
- **General legal Q&A** — ask questions against the indexed legal knowledge base.

The application combines a **Next.js frontend**, **FastAPI backend**, **FAISS vector search**, **MongoDB**, embeddings, reranking, and configurable LLM providers.

> **Important:** This project is intended for informational and educational purposes. It does not provide legal advice or replace a qualified legal professional.

## Key Features

### Authentication

- User registration and login
- JWT-based authentication
- Protected API routes
- Logout and authenticated-session handling

### Legal Document Processing

- Upload legal documents including PDF, DOCX, TXT, RTF, and supported image files
- Text extraction and chunking
- Embedding generation
- Document metadata and legal analysis
- User-scoped uploaded-document retrieval

### RAG Pipeline

- Dense vector retrieval using **FAISS**
- Lexical retrieval
- Hybrid retrieval with reciprocal-rank fusion
- Optional cross-encoder reranking
- Answer generation using configurable LLM providers
- Query rewriting and second-pass retrieval when the initial result is weak
- Citation-aware responses

### Quality & Transparency

- Confidence information
- Source citations and document metadata
- Faithfulness and retrieval evaluation metrics
- Hallucination-risk indicators
- Precision@K and Recall@K
- Citation coverage
- User feedback collection
- Evaluation summary dashboard

### Multilingual Support

The project includes a multilingual retrieval flow with language detection and a translate-for-retrieval approach, allowing supported queries to use an English retrieval path and return the response in the query language.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | Next.js, React, JavaScript, Tailwind CSS |
| Backend | Python, FastAPI |
| Authentication | JWT |
| Database | MongoDB |
| Vector Search | FAISS |
| Retrieval | Dense + lexical hybrid retrieval |
| Reranking | Optional cross-encoder |
| AI / LLM | Configurable provider integrations |
| Package Management | npm, pip |
| API Communication | HTTP / Axios |

## System Architecture

```text
                    ┌──────────────────────────┐
                    │       Next.js UI         │
                    │      React Frontend      │
                    └────────────┬─────────────┘
                                 │
                          HTTP / JWT
                                 │
                    ┌────────────▼─────────────┐
                    │      FastAPI Backend      │
                    ├───────────────────────────┤
                    │ Authentication            │
                    │ Document Upload           │
                    │ Query API                 │
                    │ Feedback & Evaluation     │
                    └────────────┬──────────────┘
                                 │
                ┌────────────────┼─────────────────┐
                │                │                 │
        ┌───────▼──────┐ ┌──────▼───────┐ ┌──────▼──────┐
        │    MongoDB   │ │    FAISS     │ │ LLM /       │
        │ Users, logs, │ │ Vector index │ │ Embeddings  │
        │ feedback     │ │ + metadata   │ │ + reranker  │
        └──────────────┘ └──────────────┘ └─────────────┘
```

## RAG Flow

```text
User Question
      │
      ▼
Query Processing
      │
      ▼
Hybrid Retrieval
(Dense + Lexical)
      │
      ▼
Rank Fusion
      │
      ▼
Optional Reranking
      │
      ▼
Context Selection
      │
      ▼
Draft Answer
      │
      ▼
Faithfulness / Quality Check
      │
      ├── Weak → Query Rewrite + Second Retrieval
      │
      └── Good
           │
           ▼
     Final Answer + Citations
```

## Project Structure

```text
LQ-RAG-Legal-AI/
│
├── backend/
│   ├── auth/                 # Authentication and security
│   ├── data/                 # Legal datasets
│   ├── database/             # MongoDB integration
│   ├── embeddings/           # Embedding generation
│   ├── faiss_index/          # FAISS index and document metadata
│   ├── models/               # Processing and LLM configuration
│   ├── rag/                  # RAG pipeline and retrieval logic
│   ├── routes/               # FastAPI API routes
│   ├── services/             # Application services
│   ├── vectorstore/          # Vector and hybrid search
│   ├── main.py               # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment variable template
│
├── legal-ai-frontend/
│   ├── public/               # Static assets
│   ├── src/app/              # Next.js application pages
│   ├── src/components/       # React components
│   ├── src/lib/              # API client and utilities
│   ├── package.json          # Node dependencies and scripts
│   └── .env.example          # Frontend environment template
│
├── .gitignore
└── README.md
```

## API Overview

Base URL:

```text
http://localhost:8000/api
```

### Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/signup` | Register a user |
| POST | `/auth/login` | Authenticate a user |
| GET | `/auth/me` | Get current user |
| POST | `/auth/change-password` | Change password |
| POST | `/auth/logout` | Logout |

### RAG & Documents

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/query` | Ask a legal question |
| POST | `/upload` | Upload and process documents |
| GET | `/upload/health` | Upload service health |

### Feedback & Evaluation

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/feedback` | Submit feedback |
| GET | `/feedback` | Retrieve feedback |
| GET | `/eval/summary` | Evaluation summary |

### System & Models

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Backend health |
| GET | `/index/status` | FAISS index status |
| POST | `/index/recover` | Index recovery |
| GET | `/models/ollama` | Available Ollama models |
| POST | `/models/select` | Select model |
| GET | `/models/recommendations` | Model recommendations |

## Getting Started

### Prerequisites

Install the following:

- Python 3.11
- Node.js 20+
- npm
- MongoDB (local or MongoDB Atlas)
- Git

Optional:

- Ollama for local LLM inference

### 1. Clone the Repository

```bash
git clone https://github.com/himateja123/LQ-RAG-Legal-AI.git
cd LQ-RAG-Legal-AI
```

### 2. Backend Setup

Open a terminal in the project root:

```bash
cd backend
```

Create a Python virtual environment.

**Windows:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file.

**Windows:**

```powershell
copy .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

Configure the required values in `.env`, such as:

```text
MONGO_URI=...
MONGO_DB_NAME=...
```

Add the required LLM provider configuration based on the provider you intend to use.

Start the backend:

```bash
uvicorn main:app --reload
```

The backend will normally be available at:

```text
http://localhost:8000
```

### 3. Frontend Setup

Open a second terminal:

```bash
cd legal-ai-frontend
npm install
```

Create the local environment file.

**Windows:**

```powershell
copy .env.example .env.local
```

**macOS / Linux:**

```bash
cp .env.example .env.local
```

Configure the frontend API URL and required client-side settings in `.env.local`.

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:3000
```

## Environment Variables

Environment files containing secrets are intentionally excluded from Git.

Use these templates:

- `backend/.env.example`
- `legal-ai-frontend/.env.example`

Typical backend configuration may include:

- MongoDB connection details
- Database name
- LLM provider settings
- Embedding model configuration
- Reranker configuration

**Never commit real API keys, passwords, database credentials, or secret tokens.**

## Development Notes

### Embedding & Reranking

The backend supports configurable embedding and reranking settings, including:

```text
EMBEDDING_MODEL_CANDIDATES
EMBEDDING_TARGET_DIM
ENABLE_CROSS_ENCODER_RERANKER
CROSS_ENCODER_MODEL
```

### Local FAISS Index

The repository includes the generated FAISS index used by the current project version:

```text
backend/faiss_index/index.faiss
backend/faiss_index/documents.pkl
```

If the index needs to be rebuilt, use the project's ingestion/indexing workflow rather than manually editing the generated files.

## Testing

### Python Syntax Check

From the `backend` directory:

```bash
python -m py_compile main.py routes/auth.py routes/query.py routes/upload.py rag/pipeline.py vectorstore/faiss_store.py
```

### Frontend Build

From `legal-ai-frontend`:

```bash
npm run build
```

Run the configured lint command as needed during development.

## Security

- Real `.env` and `.env.local` files are excluded from version control.
- API keys and database credentials should only be stored in local environment files or secure deployment configuration.
- Authentication uses JWT-based access control.
- Uploaded-document retrieval is scoped using retrieval metadata and user context.
- This application provides informational legal assistance and should not be treated as a substitute for professional legal advice.

## Future Enhancements

Potential improvements include:

- Automated evaluation pipelines for RAG releases
- More legal-domain-specific embedding and reranking models
- Improved multilingual retrieval
- Expanded citation verification
- Cloud deployment and CI/CD
- More comprehensive automated tests
- Role-based access control
- Server-side token revocation

## Author

**Himateja Perla**

- GitHub: [@himateja123](https://github.com/himateja123)
- Repository: https://github.com/himateja123/LQ-RAG-Legal-AI

## License

Add an appropriate license before distributing this project as open source.
