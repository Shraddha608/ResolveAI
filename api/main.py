from fastapi import FastAPI, HTTPException

from api.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ClassificationResponse,
    HealthResponse,
    SimilarityRequest,
    SimilarityResponse,
    TicketRequest,
)

from src.classifier import classify_ticket
from src.routing import create_routing_decision
from src.similarity import find_similar_tickets


APP_TITLE = "ResolveAI — Support Ticket Intelligence API"
APP_DESCRIPTION = """
ResolveAI is an NLP-powered support ticket intelligence system.

The API provides:
- Support queue classification
- Ticket priority prediction
- Historical ticket similarity search
- Automated department routing
"""
APP_VERSION = "1.0.0"


app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)


@app.get(
    "/",
    tags=["System"],
    summary="ResolveAI API information",
)
def root() -> dict:
    return {
        "service": "ResolveAI",
        "description": "AI-powered support ticket intelligence API",
        "version": APP_VERSION,
        "docs": "/docs",
        "health": "/health",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Check API health",
)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="ResolveAI",
        version=APP_VERSION,
    )


@app.post(
    "/predict",
    response_model=ClassificationResponse,
    tags=["Prediction"],
    summary="Predict ticket queue and priority",
)
def predict_ticket(
    ticket: TicketRequest,
) -> ClassificationResponse:
    try:
        result = classify_ticket(
            subject=ticket.subject,
            body=ticket.body,
        )

        return ClassificationResponse(
            queue=result["queue"],
            priority=result["priority"],
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}",
        )


@app.post(
    "/similar",
    response_model=SimilarityResponse,
    tags=["Similarity"],
    summary="Find similar historical tickets",
)
def similar_tickets(
    request: SimilarityRequest,
) -> SimilarityResponse:
    try:
        results = find_similar_tickets(
            subject=request.subject,
            body=request.body,
            top_k=request.top_k,
        )

        return SimilarityResponse(
            similar_tickets=results
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Similarity search failed: {str(error)}",
        )


@app.post(
    "/analyze",
    response_model=AnalyzeResponse,
    tags=["Analysis"],
    summary="Analyze and route a support ticket",
)
def analyze_ticket(
    request: AnalyzeRequest,
) -> AnalyzeResponse:
    try:
        classification = classify_ticket(
            subject=request.subject,
            body=request.body,
        )

        similar_tickets = find_similar_tickets(
            subject=request.subject,
            body=request.body,
            top_k=request.top_k,
        )

        routing = create_routing_decision(classification)

        return AnalyzeResponse(
            ticket=TicketRequest(
                subject=request.subject,
                body=request.body,
            ),
            classification=ClassificationResponse(
                queue=classification["queue"],
                priority=classification["priority"],
            ),
            similar_tickets=similar_tickets,
            routing=routing,
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ticket analysis failed: {str(error)}",
        )