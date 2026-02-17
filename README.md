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

├── backend/
│ └── app/
│ ├── main.py # FastAPI app + routers
│ ├── core/
│ │ └── settings.py # Env config (pydantic-settings)
│ ├── api/
│ │ └── routes/
│ │ ├── health.py # GET /health
│ │ └── chat.py # POST /v1/chat (RAG endpoint)
│ └── rag/
│ ├── kb_client.py # Bedrock KB retrieval client (boto3)
│ └── openai_client.py # OpenAI chat completion wrapper
├── ui/
│ └── streamlit.py # Streamlit chat UI
├── docker/
│ └── docker-compose.yml # Runs backend container
├── Dockerfile # Builds backend container (uvicorn)
├── requirements.txt # Dependencies
├── template.py # Scaffold generator
└── README.md


---

## Environment variables

Create a `.env` file in the repo root (it’s gitignored).

```
env
# AWS
AWS_DEFAULT_REGION=ca-central-1
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
