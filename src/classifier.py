from pathlib import Path

import joblib

from src.preprocessing import preprocess_ticket


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "models"

QUEUE_MODEL_PATH = MODEL_DIR / "queue_model.joblib"
QUEUE_TFIDF_PATH = MODEL_DIR / "queue_tfidf.joblib"

PRIORITY_MODEL_PATH = MODEL_DIR / "priority_model.joblib"
PRIORITY_TFIDF_PATH = MODEL_DIR / "priority_tfidf.joblib"


queue_model = joblib.load(QUEUE_MODEL_PATH)
queue_tfidf = joblib.load(QUEUE_TFIDF_PATH)

priority_model = joblib.load(PRIORITY_MODEL_PATH)
priority_tfidf = joblib.load(PRIORITY_TFIDF_PATH)


def predict_queue(text: str) -> str:
    text_vector = queue_tfidf.transform([text])
    return queue_model.predict(text_vector)[0]


def predict_priority(text: str) -> str:
    text_vector = priority_tfidf.transform([text])
    return priority_model.predict(text_vector)[0]


def classify_ticket(
    subject: str = "",
    body: str = ""
) -> dict:
    cleaned_text = preprocess_ticket(subject, body)

    queue = predict_queue(cleaned_text)
    priority = predict_priority(cleaned_text)

    return {
        "queue": queue,
        "priority": priority
    }