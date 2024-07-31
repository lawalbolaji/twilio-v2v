from fastapi import FastAPI
import uvicorn

from .config.config import Settings
from .routers import voice

app = FastAPI()
app.include_router(voice.router)

settings = Settings()


@app.get("/healthcheck")
async def healthcheck():
    """healthcheck"""
    return str("ok")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(settings.PORT))
