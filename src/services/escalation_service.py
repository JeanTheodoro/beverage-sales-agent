import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from services.email_service import EmailService
from services.message_service import MessageService


logger = logging.getLogger("bar_do_jaum")


class EscalationService:

    @staticmethod
    async def handle_human_escalation(
        session: AsyncSession,
        customer_phone: str,
        message_body: str,
        customer_name: Optional[str] = None,
        order_id: Optional[str] = None
    ) -> str:
        """
        Gerencia o processo de transbordo humano: envia o e-mail de alerta,
        salva as mensagens no histórico do chat e retorna a resposta padrão para o bot.
        """
        bot_reply = (
            "Vou encaminhar você para um atendente humano. "
            "Aguarde um momento!"
        )

        logger.info(
            f"[GUARDRAIL HUMAN] Cliente {customer_phone} solicitou atendimento humano."
        )

        # 1. Dispara o e-mail de alerta para a gerência
        EmailService.send_human_escalation_alert(
            customer_name=customer_name,
            customer_phone=customer_phone,
            last_message=message_body,
            order_id=order_id
        )

        # 2. Salva a mensagem do usuário no banco
        await MessageService.save_message(
            session=session,
            customer_phone=customer_phone,
            sender="user",
            message=message_body,
            order_id=order_id,
        )

        # 3. Salva a resposta do bot no banco
        await MessageService.save_message(
            session=session,
            customer_phone=customer_phone,
            sender="bot",
            message=bot_reply,
            order_id=order_id,
        )

        return bot_reply
