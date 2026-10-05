QUEUE_TO_DEPARTMENT = {
    "Billing and Payments": "Billing Department",
    "Customer Service": "Customer Service Department",
    "IT Support": "IT Department",
    "Product Support": "Product Support Department",
    "Sales and Pre-Sales": "Sales Department",
    "Returns and Exchanges": "Returns Department",
    "Technical Support": "Technical Support Department",
    "Human Resources": "HR Department",
    "Refunds": "Refunds Department",
    "Other": "General Support Department",
}


PRIORITY_HANDLING = {
    "high": "Urgent",
    "medium": "Standard",
    "low": "Normal",
}


def route_ticket(queue: str, priority: str) -> dict:
    department = QUEUE_TO_DEPARTMENT.get(
        queue,
        "General Support Department"
    )

    handling_level = PRIORITY_HANDLING.get(
        priority.lower(),
        "Standard"
    )

    return {
        "queue": queue,
        "priority": priority,
        "department": department,
        "handling_level": handling_level
    }


def create_routing_decision(classification_result: dict) -> dict:
    queue = classification_result.get("queue", "Other")
    priority = classification_result.get("priority", "medium")

    return route_ticket(
        queue=queue,
        priority=priority
    )