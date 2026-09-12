from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime, date
from typing import Optional

class MetricsRepository:

    @staticmethod
    async def get_dashboard_summary(
        session: AsyncSession,
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None
    ) -> dict:
        """
        Executa as duas consultas principais de métricas para o painel administrativo.
        """
        
        # Query 1: Resumo de Vendas e Faturamento
        query_summary = text("""
            SELECT 
                COUNT(id) AS total_orders,
                COALESCE(SUM(total_amount), 0.00) AS total_revenue,
                COALESCE(AVG(total_amount), 0.00) AS average_ticket
            FROM delivery.orders
            WHERE status IN ('COMPLETED', 'OUT_FOR_DELIVERY', 'APPROVED')
              AND created_at >= COALESCE(:start_datetime, (CURRENT_DATE - INTERVAL '30 days')::timestamp)
              AND created_at <= COALESCE(:end_datetime, CURRENT_TIMESTAMP);
        """)

        # Query 2: Top Produtos Mais Vendidos
        query_top_products = text("""
            SELECT 
                p.name AS product_name,
                p.category,
                p.volume,
                SUM(oi.quantity) AS total_quantity_sold,
                SUM(oi.quantity * oi.unit_price) AS total_revenue_generated
            FROM delivery.order_items oi
            JOIN delivery.orders o ON oi.order_id = o.id
            JOIN delivery.products p ON oi.product_id = p.id
            WHERE o.status IN ('COMPLETED', 'OUT_FOR_DELIVERY', 'APPROVED')
              AND o.created_at >= COALESCE(:start_datetime, (CURRENT_DATE - INTERVAL '30 days')::timestamp)
              AND o.created_at <= COALESCE(:end_datetime, CURRENT_TIMESTAMP)
            GROUP BY p.name, p.category, p.volume
            ORDER BY total_quantity_sold DESC
            LIMIT 7;
        """)

        params = {
            "start_datetime": start_datetime,
            "end_datetime": end_datetime
        }

        # Executando Resumo
        summary_result = await session.execute(query_summary, params)
        summary_row = summary_result.mappings().first()

        # Executando Top Produtos
        products_result = await session.execute(query_top_products, params)
        top_products = [dict(row) for row in products_result.mappings().all()]

        return {
            "summary": {
                "total_orders": summary_row["total_orders"] if summary_row else 0,
                "total_revenue": float(summary_row["total_revenue"]) if summary_row else 0.0,
                "average_ticket": float(summary_row["average_ticket"]) if summary_row else 0.0
            },
            "top_products": top_products
        }