from fastapi import HTTPException, status


class ClientError(HTTPException):
    status_code: int = status.HTTP_400_BAD_REQUEST
