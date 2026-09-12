from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, time, date
from typing import Optional
from repositories.metrics_repository import MetricsRepository

class MetricsService:

    @staticmethod
    async def get_admin_metrics(
        session: AsyncSession,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> dict:
        start_dt = datetime.combine(start_date, time.min) if start_date else None
        end_dt = datetime.combine(end_date, time.max) if end_date else None

        data = await MetricsRepository.get_dashboard_summary(session, start_dt, end_dt)
        
        return {
            "period": {
                "start_date": start_date.isoformat() if start_date else "Last 30 days (Default)",
                "end_date": end_date.isoformat() if end_date else "Now (Default)"
            },
            "sales_summary": data["summary"],
            "top_products": data["top_products"]
        }