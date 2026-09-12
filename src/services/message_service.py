import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.message_repository import MessageRepository

logger = logging.getLogger(__name__)

class MessageService:

    @staticmethod
    async def save_message(session: AsyncSession, customer_phone: str, sender: str, message: str, order_id: Optional[str] = None) -> None:
        """Regra de negócio para salvar uma mensagem."""
        try:
            if not customer_phone or not message:
                logger.warning("Tentativa de salvar mensagem sem telefone ou conteúdo.")
                return
                
            await MessageRepository.create(session, customer_phone, sender, message, order_id)
        except Exception as e:
            await session.rollback()
            logger.error(f"Erro ao salvar mensagem no histórico: {str(e)}", exc_info=True)

    @staticmethod
    async def get_customer_history(session: AsyncSession, customer_phone: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Regra de negócio para recuperar o histórico do cliente."""
        return await MessageRepository.get_by_phone(session, customer_phone, limit)
