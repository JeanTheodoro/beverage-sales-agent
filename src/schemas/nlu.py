from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class Intent(str, Enum):
    GREETING = "greeting"
    PRODUCT_SEARCH = "product_search"
    ADD_TO_CART = "add_to_cart"
    REMOVE_FROM_CART = "remove_from_cart"
    UPDATE_CART = "update_cart"
    PROVIDE_NAME = "provide_name"
    PROVIDE_ADDRESS = "provide_address"
    PAYMENT = "payment"
    ORDER_CONFIRMATION = "order_confirmation"
    ORDER_CANCELLATION = "order_cancellation"
    ORDER_STATUS = "order_status"
    HUMAN_SUPPORT = "human_support"
    OTHER = "other"
    FINALIZE_ORDER = "finalize_order"  # "vamos avançar", "só isso", "fechar pedido", "pode mandar"
    AFFIRMATIVE = "affirmative"        # "sim", "isso mesmo", "com certeza"
    NEGATIVE = "negative"              # "não", "cancela", "nenhum"


class ProductItem(BaseModel):
    product: str = Field(description="Nome ou termo do produto identificado na mensagem")
    quantity: int = Field(default=1, description="Quantidade solicitada ou a ser removida")
    volume: Optional[str] = Field(
        default=None, 
        description="Volume ou tamanho do produto, se especificado (ex: '350ml', '600ml', '2L', 'lata', 'long neck')"
    )

    model_config = {"additionalProperties": False}


class ProductSearchDetail(BaseModel):
    query: Optional[str] = Field(default=None, description="Termo de busca exato (ex: 'Heineken')")
    category: Optional[str] = Field(default=None, description="Categoria do produto (ex: 'cerveja', 'água')")

    model_config = {"additionalProperties": False}


class ClassificationResult(BaseModel):
    intent: Intent = Field(description="Intenção principal identificada no texto do usuário")
    items: List[ProductItem] = Field(
        default_factory=list,
        description="Lista de itens para adicionar, atualizar ou remover do carrinho"
    )
    customer_name: Optional[str] = Field(default=None, description="Nome do cliente se informado")
    address: Optional[str] = Field(default=None, description="Endereço de entrega se informado")
    payment_method: Optional[str] = Field(default=None, description="Forma de pagamento (pix, cartão, dinheiro)")
    cash_received: Optional[float] = Field(default=None, description="Valor em dinheiro fornecido para cálculo de troco")
    product_search: Optional[ProductSearchDetail] = Field(default=None, description="Detalhes de busca no catálogo")

    model_config = {"additionalProperties": False}
