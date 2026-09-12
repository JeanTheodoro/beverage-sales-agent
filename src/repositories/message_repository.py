import logging
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

class MessageRepository:

    @staticmethod
    async def create(session: AsyncSession, customer_phone: str, sender: str, message: str, order_id: Optional[str] = None) -> None:
        """Insere uma nova mensagem no banco de dados."""
        query = text("""
            INSERT INTO delivery.messages (customer_phone, sender, message, order_id)
            VALUES (:customer_phone, :sender, :message, :order_id);
        """)
        await session.execute(query, {
            "customer_phone": customer_phone,
            "sender": sender,
            "message": message,
            "order_id": order_id
        })
        await session.commit()

    @staticmethod
    async def get_by_phone(session: AsyncSession, customer_phone: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Busca o histórico de mensagens filtrando pelo telefone do cliente."""
        query = text("""
            SELECT id, customer_phone, sender, message, order_id,
                   (created_at AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo') AS created_at
            FROM delivery.messages
            WHERE customer_phone = :customer_phone
            ORDER BY created_at ASC
            LIMIT :limit;
        """)
        result = await session.execute(query, {"customer_phone": customer_phone, "limit": limit})
        return [dict(row) for row in result.mappings().all()]
