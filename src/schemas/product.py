from pydantic import BaseModel, Field
from typing import Optional


class ProductItem(BaseModel):
    product: str = Field(..., description="Nome do produto mencionado")
    quantity: int = Field(..., gt=0, description="Quantidade solicitada")

class ProductSearch(BaseModel):
    category: Optional[str] = Field(None, description="Categoria ou termo buscado no catálogo")
    product_name: Optional[str] = Field(None, description="Nome específico do produto buscado")