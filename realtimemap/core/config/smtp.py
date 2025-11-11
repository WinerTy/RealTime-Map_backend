from pydantic import BaseModel, EmailStr


class SmtpConfig(BaseModel):
    admin_email: EmailStr
    admin_password: str
    host: str
    port: int