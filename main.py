# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services import process_business_requirement

app = FastAPI(
    title="Biz Chatbot API",
    description="An API to convert natural language business requirements into structured JSON.",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRequest(BaseModel):
    requirement: str

@app.post("/generate-post/", tags=['Biz post'])
def generate_business_post(request: UserRequest):
    try:
        structured_data = process_business_requirement(request.requirement)
        return structured_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bizzap Chatbot API"}

