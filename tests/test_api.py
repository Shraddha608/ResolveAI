from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


SAMPLE_TICKET = {
    "subject": "Payment charged twice",
    "body": (
        "I was charged twice for the same transaction. "
        "Please check the duplicate payment."
    ),
}


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "ResolveAI"
    assert data["version"] == "1.0.0"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "ResolveAI"


def test_predict_endpoint():
    response = client.post(
        "/predict",
        json=SAMPLE_TICKET,
    )

    assert response.status_code == 200

    data = response.json()

    assert "queue" in data
    assert "priority" in data

    assert isinstance(data["queue"], str)
    assert data["priority"] in {"high", "medium", "low"}


def test_similarity_endpoint():
    response = client.post(
        "/similar",
        json={
            **SAMPLE_TICKET,
            "top_k": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "similar_tickets" in data
    assert len(data["similar_tickets"]) == 5

    for ticket in data["similar_tickets"]:
        assert "ticket_index" in ticket
        assert "similarity_score" in ticket
        assert "subject" in ticket
        assert "body" in ticket
        assert "queue" in ticket
        assert "priority" in ticket
        assert "type" in ticket

        assert 0 <= ticket["similarity_score"] <= 1


def test_analyze_endpoint():
    response = client.post(
        "/analyze",
        json={
            **SAMPLE_TICKET,
            "top_k": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "ticket" in data
    assert "classification" in data
    assert "similar_tickets" in data
    assert "routing" in data

    assert "queue" in data["classification"]
    assert "priority" in data["classification"]

    assert len(data["similar_tickets"]) == 5

    assert "queue" in data["routing"]
    assert "priority" in data["routing"]
    assert "department" in data["routing"]
    assert "handling_level" in data["routing"]


def test_empty_body_validation():
    response = client.post(
        "/predict",
        json={
            "subject": "Payment issue",
            "body": "",
        },
    )

    assert response.status_code == 422


def test_invalid_top_k():
    response = client.post(
        "/similar",
        json={
            **SAMPLE_TICKET,
            "top_k": 100,
        },
    )

    assert response.status_code == 422


def test_unexpected_field():
    response = client.post(
        "/predict",
        json={
            **SAMPLE_TICKET,
            "queue": "Billing and Payments",
        },
    )

    assert response.status_code == 422


def test_invalid_low_top_k():
    response = client.post(
        "/similar",
        json={
            **SAMPLE_TICKET,
            "top_k": 0,
        },
    )

    assert response.status_code == 422