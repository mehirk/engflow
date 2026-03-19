from fastapi import FastAPI

app = FastAPI(
    title="EngFlow API",
    description="Developer analytics platform API",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"status": "ok", "message": "EngFlow is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
