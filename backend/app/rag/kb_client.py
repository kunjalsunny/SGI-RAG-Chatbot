import boto3
from botocore.config import Config
from backend.app.core.settings import settings

class BedrockKB:
    def __init__(self):
        cfg = Config(retries={"max_attempts": 3, "mode": "standard"})
        self.client = boto3.client(
            "bedrock-agent-runtime",
            region_name=settings.AWS_DEFAULT_REGION,
            config=cfg,
        )

    def retrieve(self, query: str, top_k: int) -> list[dict]:
        resp = self.client.retrieve(
            knowledgeBaseId=settings.BEDROCK_KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": query},
            retrievalConfiguration={
                "vectorSearchConfiguration": {"numberOfResults": int(top_k)}
            },
        )

        results = resp.get("retrievalResults") or []
        out = []
        for r in results:
            out.append({
                "text": (r.get("content") or {}).get("text", "") or "",
                "location": r.get("location") or {},
                "metadata": r.get("metadata") or {},
                "score": r.get("score"),
            })
        return out