from fastapi import FastAPI

app = FastAPI(title="CV Offer RAG Agent")

@app.get("/")
def root():
    return {"message": "API running"}