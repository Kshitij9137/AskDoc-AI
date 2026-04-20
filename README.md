# AskDocs AI

AskDocs AI is a Django-based document question-answering web application. It lets users register, upload PDF documents, extract and chunk content, generate embeddings, build a FAISS search index, and ask natural language questions against their uploaded documents.

## Features

- User registration and JWT-based authentication
- PDF upload with automatic text extraction
- Document chunking and embedding generation
- Semantic search using FAISS
- Reranking with `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Answer generation using `google/flan-t5-large`
- Query history storage with source references
- Simple frontend served from `static/frontend`
- Admin user list and profile endpoint

## Architecture

- `askdocs_backend/`
  - Django project configuration and URL routing
- `users/`
  - Custom user model (`CustomUser`) with role support
  - Authentication and profile APIs
- `documents/`
  - Document upload, extraction, chunking, embedding, and FAISS index management
- `qa_engine/`
  - Question-answering pipeline
  - Search, reranking, generation, and history APIs
- `static/frontend/`
  - HTML/CSS/JS frontend pages for login, registration, and app UI

## Key implementation details

### Document processing
- `documents/processor.py`
  - Extracts text from PDFs using `pdfplumber`
  - Splits documents into chunks using smart paragraph and sentence boundaries
  - Generates embeddings and rebuilds FAISS index

### Embeddings
- `documents/embedder.py`
  - Uses `sentence-transformers` model `all-MiniLM-L6-v2`
- `documents/faiss_store.py`
  - Stores FAISS index in `faiss_index/index.faiss`
  - Stores chunk mapping in `faiss_index/chunk_map.json`

### Question answering
- `qa_engine/searcher.py`
  - Converts user questions to embeddings
  - Performs FAISS similarity search
- `qa_engine/pipeline.py`
  - Filters chunks, reranks them, builds context, and saves query history
- `qa_engine/llm.py`
  - Uses `google/flan-t5-large` to generate answers

## API Endpoints

### Auth
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/token/refresh/`
- `GET /api/auth/profile/`
- `GET /api/auth/admin/users/`

### Documents
- `POST /api/documents/upload/`
- `GET /api/documents/`
- `GET /api/documents/<pk>/`
- `GET /api/documents/<pk>/text/`
- `GET /api/documents/<pk>/chunks/`

### QA
- `POST /api/qa/ask/`
- `GET /api/qa/history/`
- `DELETE /api/qa/history/clear/`

### Frontend
- `/login`
- `/register`
- `/app`

## Setup

```bash
git clone https://github.com/<your-user>/AskDoc-AI.git
cd AskDoc-AI

python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt
