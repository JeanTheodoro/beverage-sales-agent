from pydantic import BaseModel, Field
from typing import Optional

class DeliveryData(BaseModel):
    customer_name: Optional[str] = Field(None, description="Nome do cliente informado")
    address: Optional[str] = Field(None, description="Endereço de entrega informado")