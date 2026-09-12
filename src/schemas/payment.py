from pydantic import BaseModel, Field
from typing import Optional, Literal

class PaymentData(BaseModel):
    payment_method: Optional[Literal["pix", "cash", "card"]] = Field(None, description="Forma de pagamento escolhida")
    cash_received: Optional[float] = Field(None, description="Valor em dinheiro entregue, se aplicável")