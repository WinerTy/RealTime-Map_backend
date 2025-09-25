from pydantic import BaseModel


class YooKassaPayment(BaseModel):
    shop_id: str
    secret_key: str