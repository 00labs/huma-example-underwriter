import fastapi
from fastapi.middleware import cors

from underwriter.api import instrumentation, views

instrumentation.instrument()
app = fastapi.FastAPI()


# for javascript to call the endpoints
origins = ["*"]
app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(views.router)


@app.get("/health")
def health() -> str:
    return "ok"
