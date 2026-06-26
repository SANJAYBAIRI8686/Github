# 🚀 GitHub Repo Analyzer

> **An AI-powered code intelligence platform that understands GitHub repositories, answers questions about code, detects security issues, generates documentation, and helps developers onboard faster using Retrieval-Augmented Generation (RAG).**

---

## 🌟 Overview

GitHub Repo Analyzer transforms any GitHub repository into an intelligent knowledge base.

Instead of manually browsing hundreds of files, developers can simply ask questions like:

> *"How does authentication work?"*

> *"Where is JWT implemented?"*

> *"What are the project's dependencies?"*

> *"Generate documentation for this repository."*

The application clones a repository, analyzes its source code, creates vector embeddings, and enables natural language conversations with complete source citations.

---

## ✨ Features

### 🤖 AI-Powered Code Understanding

* Chat with any GitHub repository
* Retrieval-Augmented Generation (RAG)
* Semantic code search
* Context-aware answers
* Source citations for every response

---

### 📚 Repository Intelligence

* Automatic repository overview
* Architecture visualization
* Dependency analysis
* Code summarization
* File explanations
* Project onboarding guides

---

### 🔒 Security & Code Quality

* Static bug detection
* Security issue scanning
* Repository health score
* Code quality insights
* Duplicate detection

---

### 📄 Documentation Generation

Generate:

* README
* API documentation
* Architecture summaries
* Developer onboarding guides

---

### ⚡ Developer Experience

* JWT Authentication
* Background processing with Celery
* Repository ingestion pipeline
* Chroma Vector Database
* Streaming AI responses
* Docker support
* REST API
* Modern React frontend

---

# 🏗️ Architecture

```text
                GitHub Repository
                        │
                        ▼
                 Repository Cloner
                        │
                        ▼
                 Source Code Parser
                        │
                        ▼
                Text Chunk Generator
                        │
                        ▼
              OpenAI Embedding Model
                        │
                        ▼
                 Chroma Vector Store
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
 Semantic Search                 AI Chat Engine
        │                               │
        └───────────────┬───────────────┘
                        ▼
                FastAPI REST Backend
                        │
                        ▼
             React + TypeScript Frontend
```

---

# 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Celery
* Redis
* PostgreSQL
* ChromaDB

### AI

* OpenAI
* LangChain
* Retrieval-Augmented Generation (RAG)
* Vector Embeddings

### Frontend

* React
* TypeScript
* Tailwind CSS
* Next.js

### DevOps

* Docker
* Docker Compose
* Alembic
* GitHub Actions (optional)

---

# 📂 Project Structure

```text
app/
 ├── api/
 ├── core/
 ├── db/
 ├── models/
 ├── repositories/
 ├── schemas/
 ├── services/
 ├── tasks/
 └── main.py

frontend/

docker-compose.yml

README.md
```

---

# 🚀 Getting Started

## Clone the Repository

```bash
git clone https://github.com/yourusername/github-repo-analyzer.git

cd github-repo-analyzer
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

```bash
cp .env.example .env
```



It helps others discover the project and motivates future improvements.
