from pydantic import BaseModel, Field, field_validator


class IncomingMessagePayload(BaseModel):
    phone: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)

    @field_validator("phone", "message")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("O campo não pode estar vazio.")

        return value

class ResponseMessageWebhook(BaseModel):

    status:str
    reply_message: str
