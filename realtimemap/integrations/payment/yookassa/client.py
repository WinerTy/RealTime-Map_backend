import logging
import uuid
from decimal import Decimal
from typing import Optional, Dict, Any

from yookassa import Payment

from .exception import GatewayException
from .schemas import CreatePayment, AmountPayment, ConfirmationPayment

logger = logging.getLogger(__name__)


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
            amount=AmountPayment(value=value, currency="RUB"),
            confirmation=ConfirmationPayment(return_url=redirect_url, type="redirect"),
            description=description,
            metadata=metadata,
            capture=True,
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

    @staticmethod
    def create_paymentv2(payment_request: CreatePayment):
        try:
            payment = Payment.create(
                payment_request.model_dump(exclude_none=True), uuid.uuid4()
            )
            return payment
        except Exception as e:
            logger.error("Yokassa payment failed", e)
            raise GatewayException
