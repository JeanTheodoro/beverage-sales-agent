from typing import List, Dict, Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class GroupedMessageOrderResponse(BaseModel):
    order_id: str
    customer_phone: str
    messages: List[Dict[str, str]]

class OrderStatusUpdate(BaseModel):
    status: str
