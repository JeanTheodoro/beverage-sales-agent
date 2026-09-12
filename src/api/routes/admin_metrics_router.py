from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db  # Ajuste para a sua importação de sessão do banco
from repositories.metrics_repository import MetricsRepository

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

@router.get("/dashbord")
async def get_admin_dashboard(
    start_date: Optional[str] = Query(None, description="Data inicial no formato YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Data final no formato YYYY-MM-DD"),
    session: AsyncSession = Depends(get_db)
):
    """
    Retorna o resumo de métricas e top produtos filtrados por intervalo de datas.
    """
    try:
        start_datetime = None
        end_datetime = None

        # Converte a string YYYY-MM-DD para datetime completo (início do dia)
        if start_date:
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")

        # Converte a string YYYY-MM-DD para o final do dia (23:59:59) para abranger todo o dia final
        if end_date:
            dt_end = datetime.strptime(end_date, "%Y-%m-%d")
            end_datetime = dt_end.replace(hour=23, minute=59, second=59)

        # Chama o repositório passando as datas tratadas
        metrics = await MetricsRepository.get_dashboard_summary(
            session=session,
            start_datetime=start_datetime,
            end_datetime=end_datetime
        )

        return metrics

    except ValueError as ve:
        raise HTTPException(
            status_code=400, 
            detail=f"Formato de data inválido. Utilize YYYY-MM-DD. Erro: {ve}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno ao carregar o dashboard: {str(e)}"
        )
    