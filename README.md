
# Smart Feedback App

## Phase 1 (Backend Setup with FastAPI)

## Objective

Build a simple backend API using Python (FastAPI) and verify it locally before moving to Docker and AWS.

---

# Step 1: Project Setup

Create project structure:

```bash
mkdir feedback-app
cd feedback-app
mkdir backend
cd backend
````

---

# Step 2: Install Required System Packages (IMPORTANT)

On Ubuntu/WSL, install:

```bash
sudo apt update
sudo apt install python3-pip python3.12-venv
```

Why:

* python3-pip → install Python packages
* python3.12-venv → create virtual environments

---

# Step 3: Create Virtual Environment (MANDATORY)

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

You should see:

```bash
(venv) username@system:...
```

Why we use venv:

* Avoid breaking system Python
* Isolate project dependencies
* Follow real DevOps best practices

---

# Step 4: Create Backend Files

## main.py

```python
from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI()

feedback_list = []

class Feedback(BaseModel):
    name: str
    message: str

@app.get("/")
def root():
    return {"message": "Feedback API running"}

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
```

---

## requirements.txt

```txt
fastapi
uvicorn
```

---

# Step 5: Install Dependencies

Make sure venv is activated:

```bash
pip install -r requirements.txt
```

---

# Step 6: Run the Application

```bash
uvicorn main:app --reload
```

---

# Step 7: Verify in Browser

Open:

* [http://127.0.0.1:8000](http://127.0.0.1:8000)
* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

# Step 8: Test API (Swagger UI)

## POST /feedback

```json
{
  "name": "Test User",
  "message": "Hello DevOps!"
}
```

## GET /feedback

Expected output:

```json
[
  {
    "id": "...",
    "name": "Test User",
    "message": "Hello DevOps!"
  }
]
```

---

# Final Checkpoint

Ensure:

* Application runs successfully
* Swagger UI (/docs) works
* POST API stores data
* GET API retrieves data
* No errors in terminal

---

# Important Notes

Do NOT run:

```bash
pip install --break-system-packages
```

Do NOT install packages globally

Always use virtual environment

---

# Key Learning

* FastAPI helps quickly build APIs
* Virtual environments isolate dependencies
* Always validate application locally before moving to Docker

---

# Outcome

You now have a working backend API ready to be:

* Containerized using Docker (next phase)

---

# Phase 2 (Dockerizing Backend)

## Objective

Containerize the FastAPI backend so it can run consistently across environments and be deployed to cloud/Kubernetes.

---

# Prerequisites

Ensure Phase 1 is complete:

* Backend working locally
* Virtual environment used (for local dev only)
* APIs tested successfully

---

# Project Structure

```bash
feedback-app/
 └── backend/
      ├── venv/
      ├── main.py
      ├── requirements.txt
      ├── .gitignore
```

---

# Step 1: Create Dockerfile

```bash
touch Dockerfile
```

## Dockerfile content:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

---

# Step 2: Create .dockerignore

```bash
touch .dockerignore
```

```dockerignore
venv/
__pycache__/
*.pyc
```

---

# Step 3: Build Docker Image

```bash
docker build -t feedback-app .
```

---

# Step 4: Run Container

```bash
docker run -p 8000:80 feedback-app
```

---

# Step 5: Verify Application

* [http://localhost:8000](http://localhost:8000)
* [http://localhost:8000/docs](http://localhost:8000/docs)

---

# Step 6: Test API Again

* POST /feedback
* GET /feedback

---

# Key Learning

* Docker packages app + dependencies together
* Eliminates “works on my machine” problem
* Foundation for CI/CD and Kubernetes

---

# Outcome

You now have a containerized backend ready for:

* Amazon ECR
* Amazon EKS
* CI/CD pipelines

---

# Phase 3 (Push Docker Image to AWS ECR)

## Objective

Push Docker image to AWS ECR.

---

# Steps

```bash
aws configure
aws ecr create-repository --repository-name feedback-app
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag feedback-app:latest <repository-uri>:latest
docker push <repository-uri>:latest
```

---

# Key Learning

* ECR is AWS Docker registry
* Required for Kubernetes deployments

---

# Phase 4 (Deploy to AWS EKS)

## Steps

```bash
eksctl create cluster --name feedback-cluster --region us-east-1
aws eks --region us-east-1 update-kubeconfig --name feedback-cluster
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

# Observability, Self-Healing & Scaling

## Self-Healing

```bash
kubectl delete pod <pod-name>
```

## Scaling

```bash
kubectl scale deployment feedback-app --replicas=4
```

---

# Key Concepts

* Self-healing systems
* Horizontal scaling
* Declarative infrastructure
* Kubernetes controllers

---

# Outcome

You now understand how Kubernetes:

* Recovers from failures
* Scales applications
* Maintains system stability

```

---

