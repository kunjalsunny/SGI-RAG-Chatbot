# SGI-RAG-Chatbot

A lightweight **Retrieval-Augmented Generation (RAG)** chatbot:

- **Retriever:** AWS **Amazon Bedrock Knowledge Bases** (vector search via `Retrieve`)
- **Generator:** **OpenAI Chat Completions**
- **Backend:** **FastAPI** (REST API)
- **UI:** **Streamlit** chat interface + source display



## What this Project does

This project answers questions by **retrieving relevant chunks** from an AWS Bedrock Knowledge Base and then **augmenting** the LLM prompt with those chunks before generating the final answer.

### End-to-end RAG flow

1. User asks a question in **Streamlit UI**
2. UI calls `POST /v1/chat` on the **FastAPI backend**
3. Backend retrieves top-k relevant chunks from **Bedrock Knowledge Base**
4. **Augmentation happens here:** backend injects retrieved chunks into the prompt as `Context: ... [1] ... [2] ...`
5. Backend calls **OpenAI** to generate an answer grounded in the context
6. Backend returns `answer` + `sources`
7. UI displays the answer and expandable sources

> Note: This repo uses Bedrock Knowledge Base only for **retrieval**.
> Generation is done by **OpenAI** (not Bedrock `RetrieveAndGenerate`).

---

## Tech stack

- FastAPI + Uvicorn (API)
- Streamlit (UI)
- boto3 (AWS Bedrock Knowledge Bases retrieval)
- OpenAI SDK (generation)
- Pydantic / pydantic-settings (config)
- python-dotenv (local env loading)

---

## Project structure

```text
.
├── backend/
│   └── app/
│       ├── main.py                  # FastAPI app + routers
│       ├── core/
│       │   └── settings.py           # Env config (pydantic-settings)
│       ├── api/
│       │   └── routes/
│       │       ├── health.py         # GET /health
│       │       └── chat.py           # POST /v1/chat (RAG endpoint)
│       └── rag/
│           ├── kb_client.py          # Bedrock KB retrieval client (boto3)
│           └── openai_client.py      # OpenAI chat completion wrapper
├── ui/
│   └── streamlit.py                 # Streamlit chat UI
├── docker/
│   └── docker-compose.yml           # Runs backend container
├── Dockerfile                       # Builds backend container (uvicorn)
├── requirements.txt                 # Dependencies
├── template.py                      # Scaffold generator
└── README.md
```
---


## Environment variables

Create a `.env` file in the repo root (it’s gitignored).

```
env
# AWS
AWS_DEFAULT_REGION=YOUR_AWS_DEFAULT_REGION
BEDROCK_KNOWLEDGE_BASE_ID=YOUR_KB_ID_HERE
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY

# OpenAI
OPENAI_API_KEY=YOUR_OPENAI_KEY
OPENAI_MODEL=gpt-4.1

# App
DEFAULT_TOP_K=4
```


Run the backend (Docker)
```
cd docker
docker compose up --build

```

Backend runs at:
```
http://localhost:8000
```

Run the UI (Streamlit)
```
pip install -r requirements.txt
streamlit run ui/streamlit.py
```


### **Knowledge Base creation (AWS) — with Vector Store**

This repo assumes you already created an **Amazon Bedrock Knowledge Base** and you provide:
```
BEDROCK_KNOWLEDGE_BASE_ID
```

Bedrock Knowledge Bases ingestion pipeline (high level):

Takes documents from a data source (commonly S3)
Chunks content
Creates embeddings (e.g., Titan Text Embeddings)
Writes embeddings to a vector store
Later, your app calls Retrieve to fetch top-k chunks for a user query

### **A) Enable model access in Bedrock**

You must have access to an **embedding model** to ingest (vectorize) documents.  
Common choice:

Amazon Titan Text Embeddings (e.g., Titan Text Embeddings V2)

### **B) Choose a vector store option **

Bedrock Knowledge Bases supports multiple vector store choices, including:

1. Quick create (Bedrock creates and configures the store for you):
2. Amazon S3 Vectors (vector bucket + vector index)
3. Amazon OpenSearch Serverless (vector search collection + index)
4. Amazon Aurora PostgreSQL Serverless (pgvector-backed)
5. Amazon Neptune Analytics (graph + RAG)

Bring your own vector store (you provide connection details):

Here an existing AWS store was created (e.g., an existing S3 vector bucket/index or OpenSearch)

**Recommendation for simple/low-ops setup:**  
Start with **Quick create S3 Vectors** or **Quick create OpenSearch Serverless**.

---

### **Step 1 — Prepare your documents in S3 (data source)**

1. Create an **S3 bucket** (or reuse an existing one)  
2. Upload your documents under a prefix, for example:

```bash
s3://<your-bucket>/rag_docs/
```

### ** Step 2 — Create the Knowledge Base (Console path) **

In AWS Console:
Open Amazon Bedrock → Knowledge bases
Click Create knowledge base → choose Create with vector store
Set:

- Name / description
- IAM service role (let Bedrock create one, or provide your own)

Choose Data source:
- Amazon S3
- Provide the S3 URI/prefix where docs are stored

Choose Embeddings model (for ingestion)

### ** Choose Vector database: **
**Option A — Quick create: S3 Vectors**
Select Amazon S3 Vectors

Choose Quick create

Bedrock creates:

- an S3 vector bucket
- a vector index
- field mappings + metadata plumbing

**Option B — Quick create: OpenSearch Serverless(Keep an eye on utilization it is costly)**

Select Amazon OpenSearch Serverless

Choose Quick create

Bedrock creates:

- vector search collection
- index and required fields

**Option C — Quick create: Aurora PostgreSQL Serverless**

Select Amazon Aurora PostgreSQL Serverless

Choose Quick create

- Bedrock provisions the DB + stores vectors in PostgreSQL (pgvector)

**Option D — Use a vector store you created (BYO)**

Choose “Use a vector store you have created”

Provide required details depending on store type, such as:

- endpoint / ARN
- index name
- vector field name
- metadata field name
- credentials (if needed via Secrets Manager)
- Review → Create knowledge base

### ** Step 3 — Ingest / Sync documents **

After KB is created:
- Open the knowledge base
- Go to Data sources
- Click Sync / Start ingestion
- Wait until ingestion status is Completed
- Whenever documents change, run Sync again.

### ** Step 4 — Test retrieval (sanity check) **

In the Bedrock console:

Use the KB “Test” or “Query” functionality
OR in your app:

Start the backend and query  ```/v1/chat```