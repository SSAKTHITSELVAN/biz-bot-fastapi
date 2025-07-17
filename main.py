# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services import process_business_requirement
from app import gst_scraper

app = FastAPI(
    title="Biz Chatbot API",
    description="An API to convert natural language business requirements into structured JSON.",
    version="1.0.0"
)

app.include_router(router= gst_scraper.router, tags=['GSTIN'])

class UserRequest(BaseModel):
    requirement: str

@app.post("/generate-post/", tags=['Biz post'])
def generate_business_post(request: UserRequest):
    """
    Accepts a user's natural language requirement and returns a structured business post.
    """
    try:
        structured_data = process_business_requirement(request.requirement)
        return structured_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bizzap Chatbot API"}
