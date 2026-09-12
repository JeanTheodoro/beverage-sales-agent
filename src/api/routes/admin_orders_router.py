from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any

from core.database import get_db
from services.order_service import OrderService
from schemas.order import GroupedMessageOrderResponse, OrderStatusUpdate

router = APIRouter(prefix="/admin/orders", tags=["Admin Orders"])


@router.get("/", response_model=List[Dict[str, Any]])
async def get_orders(
    status_filter: Optional[str] = Query(None, alias="status"),
    session: AsyncSession = Depends(get_db)
):
    """Lista todos os pedidos para o painel administrativo, com filtro opcional por status."""
    try:
        return await OrderService.list_orders(session, status_filter)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{order_id}/details")
async def get_order_details(
    order_id: str,
    session: AsyncSession = Depends(get_db)
):
    """Retorna os detalhes completos do pedido, seus itens e o histórico de chat."""
    try:
        return await OrderService.get_order_complete_details(session, order_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/{order_id}/status")
async def patch_order_status(
    order_id: str,
    body: OrderStatusUpdate,
    session: AsyncSession = Depends(get_db)
):
    """Atualiza o status de um pedido (ex: aprovar ou marcar como saiu para entrega)."""
    try:
        return await OrderService.change_order_status(session, order_id, body.status)
    except ValueError as e:
        status_code = status.HTTP_400_BAD_REQUEST if "Status inválido" in str(e) else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=str(e))


@router.get("/messages", response_model=List[GroupedMessageOrderResponse])
async def list_all_messages_with_orders(
    start_date: Optional[str] = Query(None, description="Data inicial (ex: 2026-09-01)"),
    end_date: Optional[str] = Query(None, description="Data final (ex: 2026-09-11)"),
    session: AsyncSession = Depends(get_db)
):
    """Retorna todas as mensagens com ou sem pedidos vinculados para exibição na tela com diálogos."""
    try:
        history = await OrderService.fetch_all_messages_with_orders(
            session=session,
            start_date=start_date,
            end_date=end_date
        )
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")
