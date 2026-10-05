from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity

from src.preprocessing import preprocess_ticket


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "models"

TFIDF_PATH = MODEL_DIR / "similarity_tfidf.joblib"
MATRIX_PATH = MODEL_DIR / "similarity_tfidf_matrix.npz"
METADATA_PATH = MODEL_DIR / "similarity_ticket_metadata.csv"


similarity_tfidf = joblib.load(TFIDF_PATH)
similarity_matrix = load_npz(MATRIX_PATH)
ticket_metadata = pd.read_csv(METADATA_PATH)


def find_similar_tickets(
    subject: str = "",
    body: str = "",
    top_k: int = 5
) -> list:
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    top_k = min(top_k, len(ticket_metadata))

    cleaned_text = preprocess_ticket(subject, body)

    ticket_vector = similarity_tfidf.transform([cleaned_text])

    similarity_scores = cosine_similarity(
        ticket_vector,
        similarity_matrix
    )[0]

    top_indices = np.argsort(similarity_scores)[-top_k:][::-1]

    results = []

    for index in top_indices:
        ticket = ticket_metadata.iloc[index]

        results.append({
            "ticket_index": int(index),
            "similarity_score": round(
                float(similarity_scores[index]),
                4
            ),
            "subject": ticket.get("subject", ""),
            "body": ticket.get("body", ""),
            "queue": ticket.get("queue", ""),
            "priority": ticket.get("priority", ""),
            "type": ticket.get("type", "")
        })

    return results