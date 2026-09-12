from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Optional, Dict, Any, Mapping


class OrderRepository:
    """Repositório assíncrono para operações de pedidos do Bar do Jaum."""

    @staticmethod
    async def get_all_messages_with_orders(
        session: AsyncSession,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Mapping[str, Any]]:
        """Retorna todas as mensagens garantindo que nenhum registro da tabela messages seja ignorado."""
        from datetime import datetime

        query = """
            SELECT 
                m.message,
                m.customer_phone,
                m.sender,
                m.created_at AS message_time,
                o.id AS order_id,
                o.total_amount,
                o.status AS order_status,
                o.created_at AS order_time
            FROM delivery.messages m
            LEFT JOIN LATERAL (
                SELECT id, total_amount, status, created_at
                FROM delivery.orders
                WHERE customer_phone = m.customer_phone
                ORDER BY ABS(EXTRACT(EPOCH FROM (created_at - m.created_at))) ASC
                LIMIT 1
            ) o ON true
            WHERE 1=1
        """

        params = {}

        if start_date:
            query += " AND m.created_at >= :start_date"
            params["start_date"] = datetime.strptime(start_date, "%Y-%m-%d")

        if end_date:
            query += " AND m.created_at <= :end_date"
            params["end_date"] = datetime.strptime(f"{end_date} 23:59:59", "%Y-%m-%d %H:%M:%S")

        query += " ORDER BY m.created_at DESC;"

        result = await session.execute(text(query), params)
        return result.mappings().all()
    

    @staticmethod
    async def create_order_with_items(
        session: AsyncSession,
        order_id: str,
        customer_name: str,
        customer_phone: str,
        address: str,
        delivery_fee: float,
        total_amount: float,
        payment_method: str,
        cash_received: Optional[float],
        items_to_insert: List[Dict[str, Any]]
    ) -> None:
        """Executa a persistência completa do pedido, itens e baixa de estoque de forma transacional."""
        
        # 1. Insere o pedido principal
        await session.execute(
            text("""
                INSERT INTO delivery.orders (
                    id, customer_name, customer_phone, address, delivery_fee, total_amount, 
                    payment_method, cash_received, change_due, status
                ) VALUES (
                    :id, :customer_name, :customer_phone, :address, :delivery_fee, :total_amount, 
                    :payment_method, :cash_received, :change_due, 'PENDING_APPROVAL'
                )
            """),
            {
                "id": order_id,
                "customer_name": customer_name,
                "customer_phone": customer_phone,
                "address": address,
                "delivery_fee": delivery_fee,
                "total_amount": total_amount,
                "payment_method": payment_method,
                "cash_received": cash_received,
                "change_due": None
            }
        )

        # 2. Insere os itens vinculados ao pedido
        for item_data in items_to_insert:
            await session.execute(
                text("""
                    INSERT INTO delivery.order_items (order_id, product_id, quantity, unit_price)
                    VALUES (:order_id, :product_id, :quantity, :unit_price)
                """),
                {
                    "order_id": order_id,
                    "product_id": item_data["product_id"],
                    "quantity": item_data["quantity"],
                    "unit_price": item_data["unit_price"]
                }
            )

        # 3. Dá baixa no estoque dos produtos comprados
        for item_data in items_to_insert:
            await session.execute(
                text("""
                    UPDATE delivery.products 
                    SET stock_quantity = stock_quantity - :qty 
                    WHERE id = :prod_id
                """),
                {
                    "qty": item_data["quantity"],
                    "prod_id": item_data["product_id"]
                }
            )

    @staticmethod
    async def get_all_orders(session: AsyncSession, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        base_query = """
            SELECT 
                o.id, 
                o.customer_name, 
                o.customer_phone, 
                o.address, 
                o.total_amount, 
                o.payment_method, 
                o.cash_received, 
                o.change_due, 
                o.status, 
                (o.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo') AS created_at,
                COALESCE(
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'product_name', p.name,
                            'category', p.category,
                            'volume', p.volume,
                            'quantity', oi.quantity,
                            'unit_price', oi.unit_price,
                            'subtotal', (oi.quantity * oi.unit_price)
                        )
                    ) FILTER (WHERE oi.id IS NOT NULL),
                    '[]'::json
                ) AS items
            FROM delivery.orders o
            LEFT JOIN delivery.order_items oi ON o.id = oi.order_id
            LEFT JOIN delivery.products p ON oi.product_id = p.id
        """

        if status_filter:
            sql = text(f"""
                {base_query}
                WHERE o.status = :status
                GROUP BY 
                    o.id, o.customer_name, o.customer_phone, o.address, 
                    o.total_amount, o.payment_method, o.cash_received, 
                    o.change_due, o.status, o.created_at
                ORDER BY o.created_at DESC;
            """)
            result = await session.execute(sql, {"status": status_filter})
        else:
            sql = text(f"""
                {base_query}
                GROUP BY 
                    o.id, o.customer_name, o.customer_phone, o.address, 
                    o.total_amount, o.payment_method, o.cash_received, 
                    o.change_due, o.status, o.created_at
                ORDER BY o.created_at DESC;
            """)
            result = await session.execute(sql)

        return [dict(row) for row in result.mappings().all()]
    
    @staticmethod
    async def get_order_by_id(session: AsyncSession, order_id: str) -> Optional[Dict[str, Any]]:
        query = text("""
            SELECT id, customer_name, customer_phone, address, delivery_fee, 
                   total_amount, payment_method, cash_received, change_due, status, created_at
            FROM delivery.orders
            WHERE id = :order_id;
        """)
        result = await session.execute(query, {"order_id": order_id})
        row = result.mappings().first()
        return dict(row) if row else None

    @staticmethod
    async def get_order_items(session: AsyncSession, order_id: str) -> List[Dict[str, Any]]:
        query = text("""
            SELECT product_id, quantity, unit_price
            FROM delivery.order_items
            WHERE order_id = :order_id;
        """)
        result = await session.execute(query, {"order_id": order_id})
        return [dict(row) for row in result.mappings().all()]

    @staticmethod
    async def update_order_status(session: AsyncSession, order_id: str, new_status: str) -> Optional[Dict[str, Any]]:
        query = text("""
            UPDATE delivery.orders
            SET status = :status, updated_at = CURRENT_TIMESTAMP
            WHERE id = :order_id
            RETURNING id, status;
        """)
        result = await session.execute(query, {"status": new_status, "order_id": order_id})
        row = result.mappings().first()
        
        if not row:
            return None
            
        # Retorna mapeando o campo 'status' do banco para a chave esperada pelo serviço
        row_dict = dict(row)
        return {
            "id": row_dict["id"],
            "new_status": row_dict["status"]
        }

    @staticmethod
    async def get_grouped_messages_history(
        session: AsyncSession,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Busca o histórico cru e retorna tudo da base, agrupando por pedido ou listando avulsos."""
        from collections import defaultdict

        raw_records = await OrderRepository.get_all_messages_with_orders(
            session=session, 
            start_date=start_date, 
            end_date=end_date, 
        )

        # Usar um dicionário para controlar pedidos unicos e evitar duplicações geradas pelo JOIN
        orders_map = {}
        orphan_messages = []

        for row in raw_records:
            order_id = row.get("order_id")
            customer_phone = row.get("customer_phone")
            sender = row.get("sender")
            message_text = row.get("message")
            message_time = row.get("message_time")

            if not order_id:
                orphan_messages.append({
                    "customer_phone": customer_phone,
                    "sender": sender,
                    "message": message_text,
                    "message_time": message_time
                })
                continue

            # Se o pedido ainda não está no mapa, inicializa
            if order_id not in orders_map:
                orders_map[order_id] = {
                    "customer_phone": customer_phone,
                    "order_status": row.get("order_status"),
                    "total_amount": row.get("total_amount"),
                    "messages": []
                }

            # Evita duplicar a mesma mensagem caso o JOIN traga linhas repetidas
            msg_entry = {
                "sender": sender,
                "message": message_text,
                "message_time": message_time
            }
            if msg_entry not in orders_map[order_id]["messages"]:
                orders_map[order_id]["messages"].append(msg_entry)

        result = []
        
        # Processa os pedidos agrupados
        for order_id, data in orders_map.items():
            sorted_messages = sorted(data["messages"], key=lambda x: x.get("message_time") or "")
            
            # Formato limpo com chave dinâmica correta
            clean_messages = [{m["sender"]: m["message"]} for m in sorted_messages]

            result.append({
                "order_id": order_id,
                "customer_phone": data["customer_phone"],
                "order_status": data["order_status"],
                "total_amount": data["total_amount"],
                "messages": clean_messages
            })

        # Adiciona mensagens órfãs
        if orphan_messages:
            sorted_orphans = sorted(orphan_messages, key=lambda x: x.get("message_time") or "")
            clean_orphans = [{msg["sender"]: msg["message"]} for msg in sorted_orphans]
            
            result.append({
                "order_id": "SEM_PEDIDO_VINCULADO",
                "customer_phone": "Vários",
                "messages": clean_orphans
            })

        return result