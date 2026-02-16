# TicketMaster — AI-Powered Ticket Assignment System

## Overview

TicketMaster is a production-style AI engineering project that automates IT/support ticket assignment using Retrieval-Augmented Generation (RAG), vector search, and asynchronous processing. It ingests employee skill datasets, builds embeddings, performs semantic retrieval, reranks employees based on structured metadata, and assigns tickets automatically with notifications.

The system combines modern AI tooling (LLM reasoning + vector embeddings) with realistic backend architecture including async workers, distributed services, containerization, and event-driven workflows.

---

## Key Features

- AI-driven automated ticket assignment
- Gemini LLM integration for reasoning, query parsing, and reranking
- MiniLM embeddings (HuggingFace) for semantic retrieval
- Hybrid RAG pipeline with metadata filtering
- Async processing via Celery workers
- CSV ingestion pipeline through object storage
- Automated email notifications
- Redis vector database + metadata store
- Department-aware candidate filtering
- Streamlit UI for interaction and demo
- Fully containerized microservice-style architecture

---

## Architecture

### Core Components

**Frontend (Streamlit)**

- Upload employee datasets
- Submit tickets
- Department dropdown dynamically fetched
- Toast/status feedback for async operations

**FastAPI Backend**

- Ticket submission endpoint
- Dataset upload endpoint
- Department retrieval endpoint
- Triggers Celery async pipelines

**Celery Worker Responsibilities**

- File ingestion from object storage
- Data cleaning/preprocessing
- Embedding generation (MiniLM)
- Vector database storage
- Metadata extraction
- RAG orchestration
- Email notifications

**Vector Database — Redis Vector Search**

- Stores embeddings + structured metadata
- Department pre-filter before semantic search
- HNSW indexing for fast similarity search

**LLM Layer**

- Gemini API for reasoning, reranking, query interpretation

**Message Broker**

- RabbitMQ orchestrates async Celery tasks

**Object Storage**

- LocalStack S3 emulation for development/testing

---

## Tech Stack

- Python 3.12
- FastAPI
- Streamlit
- Celery
- RabbitMQ
- Redis + Redis Vector Search
- HuggingFace MiniLM (Embeddings)
- Gemini API (LLM reasoning)
- LangChain
- Pandas
- Boto3 / LocalStack
- Docker + Docker Compose

---

## Project Structure

```
project-root/
├── api/                # FastAPI backend
├── frontend/           # Streamlit UI
├── worker/             # Celery workers + AI pipeline tasks
├── Dockerfile.client
├── Dockerfile.worker
├── docker-compose.yml
└── requirements.txt
```

---

## Environment Variables

Create a `.env` file and configure the following values:

```
RABBITMQ_USER=RabbitMQ username
RABBITMQ_PASSWORD=RabbitMQ password

CELERY_BROKER_URL=RabbitMQ connection URL for Celery broker
CELERY_BACKEND_URL=Redis URL for Celery result backend

AWS_ENDPOINT_URL=S3/LocalStack endpoint URL
AWS_ACCESS_KEY_ID=AWS or LocalStack access key
AWS_SECRET_ACCESS_KEY=AWS or LocalStack secret key
AWS_REGION_NAME=AWS region
AWS_BUCKET=S3 bucket name used for dataset uploads

REDIS_HOST=Redis database URL for metadata storage
REDIS_VECTOR_URL=Redis database URL used specifically for vector embeddings

SMTP_SERVER=SMTP server host
SMTP_PORT=SMTP server port
SMTP_USERNAME=SMTP email username
SMTP_PASSWORD=SMTP email password/app password

GOOGLE_API_KEY=Gemini API key for LLM reasoning
NOTIFICATION_EMAIL=Default email used for notifications if needed

BACKEND_BASE_URL=FastAPI base URL used by frontend/services
```

Do not commit this file to version control.

---

## Running the Project

### Option 1 — Using Prebuilt Images

```
docker compose up
```

### Option 2 — Build Locally

Uncomment build sections in `docker-compose.yml` and run:

```
docker compose up --build
```

---

## Workflow

### Employee Dataset Upload

1. CSV uploaded via frontend
2. Stored in object storage (LocalStack S3)
3. Celery worker processes dataset
4. MiniLM embeddings generated
5. Metadata extracted
6. Stored in Redis vector database

### Ticket Assignment Pipeline

1. User submits ticket + department
2. Relevant metadata extracted from Redis
3. Query embedded via MiniLM
4. Vector similarity search performed
5. Gemini LLM reranks candidates
6. Best employee assigned
7. Notification email triggered

---

## Why This Project Matters

This project demonstrates realistic AI engineering capabilities:

- Retrieval-Augmented Generation pipeline design
- Vector database usage in production-style flows
- Async distributed architecture
- Containerized microservices deployment
- AI-driven automation workflows
- Practical LLM integration beyond chatbots

It reflects how modern AI backend systems are actually built — not toy demos.

---

## Future Improvements

- Authentication & role-based access
- Kubernetes deployment
- CI/CD automation
- Monitoring/logging stack
- Managed vector DB integration
- Production frontend upgrade
- Full MLOps lifecycle integration

---

## License

MIT License

