# 🏗️ AI Project Architect

An AI-powered software architecture generator that transforms a simple project idea into a complete production-ready technical blueprint using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and structured output generation.

The application generates software architecture, technology recommendations, APIs, database design, roadmap, risks, folder structure, and architecture diagrams automatically.

---

## ✨ Features

- 🤖 AI-powered software architecture generation
- 📚 Retrieval-Augmented Generation (RAG)
- 🧠 Structured JSON generation using Pydantic
- 🏗️ Automatic architecture pattern recommendation
- 📊 Interactive Mermaid architecture diagrams
- 🛠️ Technology stack recommendations
- 🗄️ Database schema generation
- 🔌 REST API design
- 📁 Project folder structure generation
- 🗺️ Development roadmap
- ⚠️ Risk analysis and mitigation strategies
- 🚀 Future feature recommendations
- 📥 Export blueprint as Markdown

---

## 🖥️ Demo

### Input

The user provides:

- Project Idea
- Project Type
- Target Users
- Project Constraints

### Output

The system generates:

- Project Overview
- Functional Requirements
- Non-functional Requirements
- Software Architecture
- Architecture Diagram
- Components
- Technology Stack
- Database Design
- REST APIs
- Folder Structure
- Development Roadmap
- Risks
- Future Enhancements

---

## 🏛️ System Architecture

```
User
   │
   ▼
Streamlit UI
   │
   ▼
Retriever (RAG)
   │
   ▼
Knowledge Base
   │
   ▼
Groq Llama 3.3 70B
   │
   ▼
Structured Output (Pydantic)
   │
   ▼
Blueprint Generator
   │
   ▼
Markdown Export
```

---

## 🧰 Tech Stack

### Frontend

- Streamlit

### AI

- Groq API
- Llama 3.3 70B Versatile
- LangChain

### Retrieval

- LangChain Retriever
- FAISS Vector Database
- RAG Pipeline

### Validation

- Pydantic

### Visualization

- Mermaid.js (rendered via mermaid.ink)

### Environment

- Python
- dotenv

---

## 📂 Project Structure

```
AI_Project_Architect/
│
├── data/
│   └── knowledge_base/        # Source docs used to build the RAG index
│       ├── docker/
│       ├── faiss/
│       ├── fastapi/
│       ├── langchain/
│       ├── postgresql/
│       └── streamlit/
│
├── models/
│   └── schemas.py              # Pydantic schema for the generated blueprint
│
├── rag/
│   ├── __init__.py
│   ├── embeddings.py            # Embedding model setup
│   ├── ingest.py                # Builds/refreshes the vector index
│   ├── loader.py                # Loads documents from data/knowledge_base
│   ├── retrieve.py              # Retrieval logic used by app.py
│   └── splitter.py              # Text chunking
│
├── utils/
│   └── markdown_export.py      # Converts a blueprint into a downloadable .md
│
├── vector_db/                   # Persisted FAISS index (generated, not hand-edited)
│
├── app.py                       # Streamlit app entry point
├── requirements.txt
├── .env                          # Local secrets (not committed)
└── .gitignore
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI_Project_Architect.git
```

Navigate to the project

```bash
cd AI_Project_Architect
```

Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_api_key
```

Build the vector index (first run only, if `vector_db/` is empty)

```bash
python -m rag.ingest
```

Run the application

```bash
streamlit run app.py
```

---

## ☁️ Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select this repo/branch, and set the main file to `app.py`.
4. Under **Advanced settings → Secrets**, add:
   ```
   GROQ_API_KEY = "your_api_key"
   ```
5. Deploy. Streamlit Cloud installs `requirements.txt` and launches the app automatically.

> `vector_db/` must either be committed to the repo (if small) or rebuilt on startup via `rag/ingest.py`, since Streamlit Cloud won't have your local FAISS index otherwise.

---

## 🧠 How It Works

1. User enters a software project idea.
2. Relevant documentation is retrieved using RAG.
3. Retrieved context is injected into the system prompt.
4. Groq Llama 3.3 generates a structured software blueprint.
5. Pydantic validates the generated output.
6. Streamlit renders the architecture visually.
7. The blueprint can be exported as Markdown.

---

## 📊 Example Output

The generated blueprint includes:

- ✅ Project Overview
- ✅ Functional Requirements
- ✅ Non-functional Requirements
- ✅ Architecture Pattern
- ✅ Mermaid Architecture Diagram
- ✅ Technology Stack
- ✅ Components
- ✅ Database Design
- ✅ REST APIs
- ✅ Folder Structure
- ✅ Development Roadmap
- ✅ Risk Assessment
- ✅ Future Enhancements

---

## 🎯 Use Cases

- Software Architecture Design
- AI Solution Planning
- Graduation Projects
- Startup MVP Planning
- Technical Documentation
- System Design Interviews
- AI Project Scaffolding

---


## 📄 License

This project is licensed under the MIT License.
