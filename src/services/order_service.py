import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List, Optional, Mapping
from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository

class OrderService:
    VALID_STATUSES = ['PENDING_APPROVAL', 'APPROVED', 'OUT_FOR_DELIVERY', 'COMPLETED', 'CANCELLED']

    @staticmethod
    async def create_new_order(
        session: AsyncSession,
        customer_name: str,
        customer_phone: str,
        address: str,
        payment_method: str,
        cash_received: float | None,
        items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Cria um novo pedido com ID hexadecimal, valida estoque e calcula o total."""
        
        # 1. Gera um ID hexadecimal único e curto (ex: 'A3F8B12C')
        order_id = uuid.uuid4().hex[:8].upper()

        total_amount = 0.0
        order_items_to_insert = []

        # 2. Valida estoque e calcula o valor total com base no catálogo de produtos considerando o volume
        for item in items:
            product_name = item.get("product") or item.get("product_name")
            quantity = item["quantity"]
            item_volume = item.get("volume")

            product = None

            # Tenta extrair o volume se ele estiver embutido no nome (ex: "Coca-Cola (2L)")
            if not item_volume and "(" in product_name and ")" in product_name:
                parts = product_name.split("(")
                base_name = parts[0].strip()
                vol = parts[1].replace(")", "").strip()
                product = await ProductRepository.get_by_name_and_volume(session, base_name, vol)
            
            # Se já temos um volume explícito, busca combinando nome e volume
            if not product and item_volume:
                product = await ProductRepository.get_by_name_and_volume(session, product_name, item_volume)

            # Fallback final para busca apenas pelo nome caso nenhum volume tenha sido encontrado
            if not product:
                product = await ProductRepository.get_by_name(session, product_name)

            if not product:
                raise ValueError(f"Produto '{product_name}' não encontrado no catálogo.")
            
            if product["stock_quantity"] < quantity:
                raise ValueError(f"Estoque insuficiente para o produto '{product_name}'. Disponível: {product['stock_quantity']}")

            unit_price = float(product["price"])
            subtotal = unit_price * quantity
            total_amount += subtotal

            order_items_to_insert.append({
                "product_id": product["id"],
                "quantity": quantity,
                "unit_price": unit_price
            })

        # Adiciona taxa de entrega fixa (R$ 5,00)
        delivery_fee = 5.00
        total_amount += delivery_fee

        # 3. Delega a persistência transacional para o Repositório
        await OrderRepository.create_order_with_items(
            session=session,
            order_id=order_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            address=address,
            delivery_fee=delivery_fee,
            total_amount=total_amount,
            payment_method=payment_method,
            cash_received=cash_received,
            items_to_insert=order_items_to_insert
        )

        await session.commit()

        return {
            "id": order_id,
            "total_amount": total_amount
        }

    @staticmethod
    async def list_orders(session: AsyncSession, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        if status_filter and status_filter not in OrderService.VALID_STATUSES:
            raise ValueError(f"Filtro de status inválido. Opções válidas: {OrderService.VALID_STATUSES}")
        return await OrderRepository.get_all_orders(session, status_filter)

    @staticmethod
    async def get_order_complete_details(session: AsyncSession, order_id: str) -> Dict[str, Any]:
        order = await OrderRepository.get_order_by_id(session, order_id)
        if not order:
            raise ValueError("Pedido não encontrado.")

        items = await OrderRepository.get_order_items(session, order_id)
        
        return {
            "order": order,
            "items": items,
            "chat_history": []
        }

    @staticmethod
    async def change_order_status(session: AsyncSession, order_id: str, new_status: str) -> Dict[str, Any]:
        if new_status not in OrderService.VALID_STATUSES:
            raise ValueError(f"Status inválido. Escolha entre: {OrderService.VALID_STATUSES}")

        updated_order = await OrderRepository.update_order_status(session, order_id, new_status)
        if not updated_order:
            raise ValueError("Pedido não encontrado para atualização.")

        await session.commit()
        return {
            "message": "Status atualizado com sucesso",
            "order_id": updated_order["id"],
            "new_status": updated_order["new_status"]
        }

    @staticmethod
    async def fetch_all_messages_with_orders(
        session: AsyncSession,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Mapping[str, Any]]:
        history = await OrderRepository.get_grouped_messages_history(
            session=session,
            start_date=start_date,
            end_date=end_date,
    )
    
        return history
