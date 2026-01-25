from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.app.core.settings import settings
from backend.app.rag.kb_client import BedrockKB
from backend.app.rag.openai_client import OpenAITextGen

router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    top_k: int = Field(default=settings.DEFAULT_TOP_K, ge=1, le=20)

@router.post("/v1/chat")
def chat(req: ChatRequest):
    try:
        kb = BedrockKB()
        gen = OpenAITextGen()

        contexts = kb.retrieve(req.message, top_k=req.top_k)
        ctx_block = "\n\n".join(
            [f"[{i+1}] {c.get('metadata',{}).get('source','')}\n{c['text']}"
             for i, c in enumerate(contexts)]
        )

        system = (
            "You are SGI’s internal assistant. Use only the provided context. "
            "If context is insufficient, say so and ask a focused follow-up. "
            "Cite sources like [1], [2]."
        )
        prompt = f"Context:\n{ctx_block}\n\nQuestion:\n{req.message}\n\nAnswer with citations."
        answer = gen.generate(system, prompt)

        return {"answer": answer, "sources": contexts}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
