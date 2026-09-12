import logging

from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from langfuse import observe, propagate_attributes

from agent.classifier import Classifier
from agent.handlers.handle_order_flow import HandleOrderFlow
from agent.handlers.search_products import SearchProductsHandler
from schemas.nlu import Intent
from services.session_service import SessionService

logger = logging.getLogger("bar_do_jaum")

class SalesAgent:


    @staticmethod
    @observe(name="sales_agent_process_message")
    async def process_message(
        session: AsyncSession,
        message_body: str,
        customer_phone: str,
    ) -> Dict[str, Any]:
        """Processa a mensagem do cliente de ponta a ponta com sub-handlers especializados."""

        # =========================================================
        # LANGFUSE CONTEXT
        # =========================================================

        with propagate_attributes(
            user_id=customer_phone,
            metadata={
                "message_length": len(message_body),
            },
        ):

            # =====================================================
            # 1. RECUPERA OS DADOS DA SESSÃO
            # =====================================================

            session_data = await SessionService.get_session(
                session,
                customer_phone,
            )

            history = session_data.get("history", [])

            session_state = {
                "customer_name": session_data.get("customer_name"),
                "address": session_data.get("address"),
                "payment_method": session_data.get("payment_method"),
                "cash_received": session_data.get("cash_received"),
            }

            # =====================================================
            # 2. CLASSIFICAÇÃO
            # =====================================================

            nlu_result = await Classifier.classify_message(
                raw_message=message_body,
                history=history,
                session_state=session_state,
            )

            intent = nlu_result.intent

            intent_value = (
                intent.value
                if isinstance(intent, Intent)
                else intent
            )

            # =====================================================
            # 3. PREPARA RESPOSTA
            # =====================================================

            response_data = {
                "intent": intent_value,
                "reply_message": "",
                "order_id": None,
            }

            has_active_cart = bool(
                session_data.get("items")
            )

            ORDER_FLOW_INTENTS = {
                Intent.ADD_TO_CART.value,
                Intent.REMOVE_FROM_CART.value,
                Intent.UPDATE_CART.value,
                Intent.ORDER_CANCELLATION.value,
                Intent.PAYMENT.value,
                Intent.PROVIDE_ADDRESS.value,
                Intent.PROVIDE_NAME.value,
                Intent.ORDER_CONFIRMATION.value,
                Intent.FINALIZE_ORDER.value,
                Intent.AFFIRMATIVE.value,
            }

            # =====================================================
            # 4. ROTEAMENTO
            # =====================================================

            if intent_value == Intent.PRODUCT_SEARCH.value:

                response_data["reply_message"] = (
                    await SearchProductsHandler.handle(
                        session,
                        message_body,
                        nlu_result,
                    )
                )

            elif (
                has_active_cart
                or intent_value in ORDER_FLOW_INTENTS
            ):

                response_data["reply_message"] = (
                    await HandleOrderFlow.handle(
                        session,
                        customer_phone,
                        nlu_result,
                    )
                )

            elif intent_value == Intent.GREETING.value:

                response_data["reply_message"] = (
                    "Fala, campeão! Bem-vindo ao Bar do Jaum. "
                    "O que vai ser hoje? "
                    "Manda a braba ou gostaria de ver quais "
                    "produtos temos: cervejas, refrigerantes e água"
                )

            else:

                response_data["reply_message"] = (
                    "Não entendi muito bem. "
                    "Você gostaria de ver o catálogo de bebidas "
                    "ou fazer um pedido?"
                )

            return response_data

