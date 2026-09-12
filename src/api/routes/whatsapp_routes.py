import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from services.whatsapp_service import WhatsAppService
from schemas.webhook import IncomingMessagePayload, ResponseMessageWebhook

logger = logging.getLogger("bar_do_jaum")

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp Webhook"])


@router.post("/webhook", response_model=ResponseMessageWebhook)
async def whatsapp_webhook(
    payload: IncomingMessagePayload,
    session: AsyncSession = Depends(get_db),
):
    try:
        reply_message = await WhatsAppService.process_incoming_message(
            session=session,
            customer_phone=payload.phone,
            message_body=payload.message,
        )

        return {
            "status": "success",
            "reply_message": reply_message,
        }

    except Exception as exc:
        logger.error(f"[ERROR WHATSAPP WEBHOOK] {exc}", exc_info=True)

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao processar a mensagem.",
        )
