import json
import logging
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from core.redis import redis_client

logger = logging.getLogger("bar_do_jaum")

SESSION_TTL = 60 * 10  # 10 minutos


class SessionService:

    @staticmethod
    def _get_key(customer_phone: str) -> str:
        return f"session:{customer_phone}"

    @staticmethod
    async def get_session(
        session: AsyncSession, customer_phone: str
    ) -> Dict[str, Any]:
        """Recupera os dados da sessão do Redis."""
        try:
            key = SessionService._get_key(customer_phone)
            data = await redis_client.get(key)
            if data:
                return json.loads(data)
            return {
                "history": [],
                "items": [],
                "customer_name": None,
                "address": None,
                "payment_method": None,
                "cash_received": None,
            }
        except Exception as e:
            logger.error(
                f"[SESSION SERVICE] Erro ao buscar sessão de {customer_phone}: {e}"
            )
            return {
                "history": [],
                "items": [],
                "customer_name": None,
                "address": None,
                "payment_method": None,
                "cash_received": None,
            }

    @staticmethod
    async def save_session(
        session: AsyncSession,
        customer_phone: str,
        session_data: Dict[str, Any],
    ) -> None:
        """Sobrescreve/salva os dados da sessão no Redis com expiração."""
        try:
            key = SessionService._get_key(customer_phone)
            await redis_client.set(
                key, json.dumps(session_data, ensure_ascii=False), ex=SESSION_TTL
            )
        except Exception as e:
            logger.error(
                f"[SESSION SERVICE] Erro ao salvar sessão de {customer_phone}: {e}"
            )

    @staticmethod
    async def update_session(
        session: AsyncSession,
        customer_phone: str,
        updates: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Atualiza a sessão aceitando dicionário e/ou kwargs diretamente."""
        try:
            current_session = await SessionService.get_session(
                session, customer_phone
            )

            # Se um dicionário foi passado no parâmetro updates, mescla
            if updates and isinstance(updates, dict):
                current_session.update(updates)

            # Se argumentos nomeados (ex: customer_name="...") foram passados, mescla
            if kwargs:
                current_session.update(kwargs)

            await SessionService.save_session(
                session, customer_phone, current_session
            )
            return current_session
        except Exception as e:
            logger.error(
                f"[SESSION SERVICE] Erro ao atualizar sessão de {customer_phone}: {e}"
            )
            raise e

    @staticmethod
    async def clear_session(
        session: AsyncSession, customer_phone: str
    ) -> None:
        """Limpa a sessão do cliente (útil após a finalização do pedido)."""
        try:
            key = SessionService._get_key(customer_phone)
            await redis_client.delete(key)
        except Exception as e:
            logger.error(
                f"[SESSION SERVICE] Erro ao limpar sessão de {customer_phone}: {e}"
            )

    @staticmethod
    async def add_message_to_history(
        session: AsyncSession,
        customer_phone: str,
        role: str,
        content: str,
        max_history_length: int = 10,
    ) -> None:
        """Adiciona uma mensagem ao histórico e atualiza o Redis."""
        try:
            session_data = await SessionService.get_session(
                session, customer_phone
            )
            history: List[Dict[str, str]] = session_data.get("history", [])

            history.append({"role": role, "content": content})

            if len(history) > max_history_length:
                history = history[-max_history_length:]

            session_data["history"] = history
            await SessionService.save_session(
                session, customer_phone, session_data
            )
        except Exception as e:
            logger.error(
                f"[SESSION SERVICE] Erro ao adicionar histórico para {customer_phone}: {e}"
            )
