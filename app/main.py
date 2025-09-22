from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="CodeSentinel",
    description="AI-Powered Distributed Code Review Platform",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "name": "CodeSentinel",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}