import uuid
from decimal import Decimal
from typing import Optional, Dict, Any

from yookassa import Payment

from .schemas import CreatePayment, AmountPayment, ConfirmationPayment


class YookassaClient:
    def __init__(self):
        pass

    @staticmethod
    def _preparate_data(
        value: Decimal,
        redirect_url: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        valid_data = CreatePayment(
            amount=AmountPayment(value=value),
            confirmation=ConfirmationPayment(return_url=redirect_url),
            description=description,
            metadata=metadata,
        )
        return valid_data

    def create_payment(
        self,
        value: Decimal,
        redirect_url: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        payment_data = self._preparate_data(value, redirect_url, description, metadata)
        payment = Payment.create(
            payment_data.model_dump(exclude_none=True), uuid.uuid4()
        )
        return payment
