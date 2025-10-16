from decimal import Decimal
from typing import Annotated, Optional, Dict, Any

from pydantic import BaseModel, Field


class AmountPayment(BaseModel):
    value: Annotated[
        Decimal, Field(max_digits=10, decimal_places=2, description="Summary")
    ]
    currency: Annotated[str, Field("RUB", description="Currency code")]


class ConfirmationPayment(BaseModel):
    type: Annotated[str, Field("redirect", description="Type")]
    return_url: Annotated[
        str, Field("https://www.example.com/return_url", description="Return URL")
    ]


class CreatePayment(BaseModel):
    amount: AmountPayment
    confirmation: ConfirmationPayment
    capture: Annotated[bool, Field(True, description="Capture payment")]
    description: Annotated[str, Field(None, description="Description")]
    metadata: Annotated[Optional[Dict[str, Any]], Field(None, description="Metadata")]
