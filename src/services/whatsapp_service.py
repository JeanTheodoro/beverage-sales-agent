import logging
import json

from sqlalchemy.ext.asyncio import AsyncSession
from langfuse import observe, propagate_attributes

from agent.sales_agent import SalesAgent
from services.message_service import MessageService
from schemas.guardrail import GuardrailDecision
from agent.guardrails.input_guardrail import InputGuardrail
from services.escalation_service import EscalationService

logger = logging.getLogger("bar_do_jaum")

class WhatsAppService:


    @staticmethod
    @observe(name="process_incoming_message")
    async def process_incoming_message(
        session: AsyncSession,
        customer_phone: str,
        message_body: str,
    ) -> str:

        try:

            with propagate_attributes(
                user_id=customer_phone,
                tags=["whatsapp", "production"],
            ):

                # ==========================================
                # INPUT GUARDRAIL
                # ==========================================

                guardrail_result = InputGuardrail.check(message_body)

                # ==========================================
                # BLOCK
                # ==========================================

                if guardrail_result.decision == GuardrailDecision.BLOCK:

                    bot_reply = (
                        "Não posso ajudar com esse tipo de solicitação."
                    )

                    logger.warning(
                        json.dumps(
                            {
                                "event": "security_block",
                                "category": "prompt_injection",
                                "customer_phone": customer_phone,
                                "payload": message_body,
                                "reason": guardrail_result.reason,
                            },
                            ensure_ascii=False,
                        )
                    )

                    await MessageService.save_message(
                        session=session,
                        customer_phone=customer_phone,
                        sender="user",
                        message=message_body,
                        order_id=None,
                    )

                    await MessageService.save_message(
                        session=session,
                        customer_phone=customer_phone,
                        sender="bot",
                        message=bot_reply,
                        order_id=None,
                    )

                    return bot_reply

                # ==========================================
                # HUMAN HANDOFF
                # ==========================================

                if guardrail_result.decision == GuardrailDecision.HUMAN:

                    return await EscalationService.handle_human_escalation(
                        session=session,
                        customer_phone=customer_phone,
                        message_body=message_body,
                        customer_name=None, # Opcional: passe o nome caso já o tenha recuperado da sessão
                        order_id=None       # Opcional: passe o ID do pedido atual caso o cliente já possua um aberto
                    )

                # ==========================================
                # SALES AGENT
                # ==========================================

                response_data = await SalesAgent.process_message(
                    session=session,
                    message_body=message_body,
                    customer_phone=customer_phone,
                )

                bot_reply = response_data.get(
                    "reply_message",
                    "Ops, não consegui entender bem. Pode repetir?",
                )

                current_order_id = response_data.get("order_id")

                # ==========================================
                # SAVE USER MESSAGE
                # ==========================================

                await MessageService.save_message(
                    session=session,
                    customer_phone=customer_phone,
                    sender="user",
                    message=message_body,
                    order_id=current_order_id,
                )

                # ==========================================
                # SAVE BOT MESSAGE
                # ==========================================

                await MessageService.save_message(
                    session=session,
                    customer_phone=customer_phone,
                    sender="bot",
                    message=bot_reply,
                    order_id=current_order_id,
                )

                return bot_reply

        except Exception as e:

            logger.error(
                f"[ERROR WHATSAPP SERVICE] "
                f"Erro ao processar mensagem de {customer_phone}: {e}",
                exc_info=True,
            )

            raise e 
