# ResolveAI — AI-Powered Support Ticket Intelligence System

ResolveAI is an NLP-powered support ticket intelligence system that analyzes customer support tickets and automatically predicts their support queue, priority, similar historical tickets, and recommended routing department.

The project combines machine learning, NLP, similarity search, REST API development, and Docker-based deployment into an end-to-end application.

---

## Features

- Support ticket queue classification
- Ticket priority prediction
- Historical ticket similarity search
- Automated department routing
- REST API using FastAPI
- Input validation using Pydantic
- Dockerized deployment
- Automated API testing using Pytest

---

## System Workflow

```text
Customer Support Ticket
          |
          v
   Text Preprocessing
          |
          v
      TF-IDF
          |
     +----+----+
     |         |
     v         v
Queue Model  Priority Model
     |         |
     +----+----+
          |
          v
   Classification
          |
          +------------------+
          |                  |
          v                  v
 Similarity Search       Routing Logic
          |                  |
          v                  v
 Historical Tickets      Department
                          + Handling Level