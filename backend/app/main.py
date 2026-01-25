from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from backend.app.core.settings import settings
from backend.app.api.routes.health import router as health_router
from backend.app.api.routes.chat import router as chat_router

app = FastAPI(title=settings.APP_NAME)

app.include_router(health_router)
app.include_router(chat_router)
