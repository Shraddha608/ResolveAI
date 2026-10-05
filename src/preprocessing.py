import re


def clean_text(text: str) -> str:
    if text is None:
        return ""

    text = str(text).lower()

    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def combine_ticket_text(subject: str = "", body: str = "") -> str:
    subject = "" if subject is None else str(subject)
    body = "" if body is None else str(body)

    combined_text = subject.strip() + " " + body.strip()

    return combined_text.strip()


def preprocess_ticket(
    subject: str = "",
    body: str = ""
) -> str:
    combined_text = combine_ticket_text(subject, body)
    cleaned_text = clean_text(combined_text)

    return cleaned_text