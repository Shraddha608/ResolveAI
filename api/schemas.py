from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


TicketSubject = Annotated[
    str,
    Field(
        default="",
        max_length=300,
        description="Optional subject or short summary of the support ticket.",
        examples=[
            "Payment charged twice",
            "Unable to reset password",
        ],
    ),
]


TicketBody = Annotated[
    str,
    Field(
        min_length=1,
        max_length=10_000,
        description="Detailed description of the customer's support issue.",
        examples=[
            "I was charged twice for the same transaction. "
            "Please check the duplicate payment."
        ],
    ),
]


TopK = Annotated[
    int,
    Field(
        default=5,
        ge=1,
        le=20,
        description="Number of similar historical tickets to retrieve.",
        examples=[5],
    ),
]


class TicketRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "subject": "Payment charged twice",
                    "body": (
                        "I was charged twice for the same transaction. "
                        "Please check the duplicate payment and refund "
                        "one of the charges."
                    ),
                }
            ]
        },
    )

    subject: TicketSubject
    body: TicketBody

    @field_validator("body")
    @classmethod
    def validate_body(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                "Ticket body cannot be empty or whitespace only."
            )

        return value


class SimilarityRequest(TicketRequest):
    top_k: TopK


class AnalyzeRequest(SimilarityRequest):
    pass


class ClassificationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    queue: Annotated[
        str,
        Field(
            description="Predicted support queue.",
            examples=["Billing and Payments"],
        ),
    ]

    priority: Annotated[
        Literal["high", "medium", "low"],
        Field(
            description="Predicted ticket priority.",
            examples=["high"],
        ),
    ]


class SimilarTicket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_index: Annotated[
        int,
        Field(
            ge=0,
            description="Index of the historical ticket in the similarity index.",
            examples=[1247],
        ),
    ]

    similarity_score: Annotated[
        float,
        Field(
            ge=-1.0,
            le=1.0,
            description="Cosine similarity score between the new ticket and the historical ticket.",
            examples=[0.8421],
        ),
    ]

    subject: Annotated[
        str,
        Field(
            description="Subject of the historical support ticket.",
            examples=["Duplicate payment issue"],
        ),
    ]

    body: Annotated[
        str,
        Field(
            description="Body of the historical support ticket.",
        ),
    ]

    queue: Annotated[
        str,
        Field(
            description="Support queue assigned to the historical ticket.",
            examples=["Billing and Payments"],
        ),
    ]

    priority: Annotated[
        str,
        Field(
            description="Priority assigned to the historical ticket.",
            examples=["medium"],
        ),
    ]

    type: Annotated[
        str,
        Field(
            description="Type of the historical support ticket.",
            examples=["Incident"],
        ),
    ]


class SimilarityResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    similar_tickets: Annotated[
        list[SimilarTicket],
        Field(
            description="Historical support tickets ranked by descending similarity.",
        ),
    ]


class RoutingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    queue: Annotated[
        str,
        Field(
            description="Predicted support queue.",
            examples=["Billing and Payments"],
        ),
    ]

    priority: Annotated[
        Literal["high", "medium", "low"],
        Field(
            description="Predicted ticket priority.",
            examples=["high"],
        ),
    ]

    department: Annotated[
        str,
        Field(
            description="Department to which the ticket should be routed.",
            examples=["Billing Department"],
        ),
    ]

    handling_level: Annotated[
        str,
        Field(
            description="Operational handling level derived from priority.",
            examples=["Urgent"],
        ),
    ]


class AnalyzeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket: Annotated[
        TicketRequest,
        Field(description="Original customer support ticket."),
    ]

    classification: Annotated[
        ClassificationResponse,
        Field(description="Predicted support queue and ticket priority."),
    ]

    similar_tickets: Annotated[
        list[SimilarTicket],
        Field(description="Most similar historical support tickets."),
    ]

    routing: Annotated[
        RoutingResponse,
        Field(
            description="Recommended operational routing based on the predicted queue and priority.",
        ),
    ]


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Annotated[
        Literal["healthy"],
        Field(
            description="Current API service status.",
            examples=["healthy"],
        ),
    ]

    service: Annotated[
        str,
        Field(
            description="Name of the service.",
            examples=["ResolveAI"],
        ),
    ]

    version: Annotated[
        str,
        Field(
            description="Current API version.",
            examples=["1.0.0"],
        ),
    ]