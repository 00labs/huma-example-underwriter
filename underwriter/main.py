import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from underwriter.core.views import router as underwriter_router

logger = structlog.get_logger(__name__)

app = FastAPI()


# for javascript to call the endpoints
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(underwriter_router)


@app.get("/health")
def health() -> str:
    return "ok"
