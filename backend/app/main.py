from fastapi import FastAPI

from app.router import api_router

app = FastAPI(
    title="CV Matching API",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "CV Matching API is running"}