from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI()

# Temporary in-memory storage (we will replace with DynamoDB later)
feedback_list = []

class Feedback(BaseModel):
    name: str
    message: str

@app.get("/")
def root():
    return {"message": "Feedback API running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/feedback")
def submit_feedback(feedback: Feedback):
    item = {
        "id": str(uuid.uuid4()),
        "name": feedback.name,
        "message": feedback.message
    }
    feedback_list.append(item)
    return {"status": "success", "data": item}

@app.get("/feedback")
def get_feedback():
    return feedback_list