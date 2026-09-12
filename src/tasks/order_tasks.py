import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from core.config.celery_app import celery_app
from core.config.settings import settings
from services.email_service import EmailService

logger = logging.getLogger(__name__)

def get_db_connection():
    """Abre uma conexão síncrona com o Supabase usando a URL síncrona do settings."""
    database_url = settings.SUPABASE_DATABASE_URL_NO_ASYNC
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

@celery_app.task(name="tasks.check_orders_status")
def check_orders_status():
    """Varre os pedidos periodicamente e dispara as mensagens e e-mails de alerta."""
    print("[CELERY BEAT] Verificando status dos pedidos no Supabase...")
    logger.info("[CELERY BEAT] Verificando status dos pedidos no Supabase...")
    
    # Usar 'with' garante que a conexão e o cursor fecham sozinhos, 
    # mesmo se ocorrer qualquer erro no meio do caminho.
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                
                # ----------------------------------------------------
                # 1. Regra para pedidos com status 'APPROVED'
                # ----------------------------------------------------
                cursor.execute("""
                    SELECT id, customer_name, customer_phone, payment_method 
                    FROM delivery.orders 
                    WHERE status = 'APPROVED' 
                      AND (approved_notified = FALSE OR approved_notified IS NULL)
                """)
                orders_to_approve = cursor.fetchall()
                print(f"[DEBUG] Pedidos aprovados encontrados: {len(orders_to_approve)}")
                
                for order in orders_to_approve:
                    phone = order["customer_phone"]
                    order_id = order["id"]
                    customer_name = order.get("customer_name")
                    
                    mensagem = f"Compra aprovada! Seu pedido #{order_id} já foi confirmado, meu amigo!"
                    print(f"[WHATSAPP] Enviado para {phone}: {mensagem}")
                    
                    # Tenta enviar o e-mail com tratamento isolado
                    email_enviado_com_sucesso = False
                    try:
                        EmailService.send_order_status_alert(
                            customer_name=customer_name,
                            customer_phone=phone,
                            order_id=str(order_id),
                            status_description="Aprovado / Confirmado"
                        )
                        print(f"[EMAIL] Alerta enviado para a gerência referente ao pedido #{order_id}")
                        email_enviado_com_sucesso = True
                    except Exception as mail_err:
                        logger.error(f"[EMAIL ERROR] Falha crítica ao enviar e-mail do pedido {order_id}: {mail_err}")
                        print(f"[EMAIL ERROR] Falha ao enviar e-mail: {mail_err}")
                    
                    # SÓ atualiza o banco como notificado se o processo ocorreu bem 
                    # (ou ajuste conforme sua regra se quiser marcar mesmo sem e-mail)
                    if email_enviado_com_sucesso:
                        cursor.execute("""
                            UPDATE delivery.orders 
                            SET approved_notified = TRUE, updated_at = CURRENT_TIMESTAMP 
                            WHERE id = %s
                        """, (order_id,))
                        conn.commit()

                # ----------------------------------------------------
                # 2. Regra para status 'OUT_FOR_DELIVERY'
                # ----------------------------------------------------
                cursor.execute("""
                    SELECT id, customer_name, customer_phone 
                    FROM delivery.orders 
                    WHERE status = 'OUT_FOR_DELIVERY' 
                      AND (delivery_notified = FALSE OR delivery_notified IS NULL)
                """)
                orders_out_for_delivery = cursor.fetchall()
                print(f"[DEBUG] Pedidos em entrega encontrados: {len(orders_out_for_delivery)}")
                
                for order in orders_out_for_delivery:
                    phone = order["customer_phone"]
                    order_id = order["id"]
                    customer_name = order.get("customer_name")
                    
                    mensagem = f"Já estamos saindo para entregar suas bebidas do pedido #{order_id}! Fique atento."
                    print(f"[WHATSAPP] Enviado para {phone}: {mensagem}")
                    
                    email_enviado_com_sucesso = False
                    try:
                        EmailService.send_order_status_alert(
                            customer_name=customer_name,
                            customer_phone=phone,
                            order_id=str(order_id),
                            status_description="Saiu para Entrega (Delivery)"
                        )
                        print(f"[EMAIL] Alerta de entrega enviado referente ao pedido #{order_id}")
                        email_enviado_com_sucesso = True
                    except Exception as mail_err:
                        logger.error(f"[EMAIL ERROR] Falha crítica ao enviar e-mail de delivery do pedido {order_id}: {mail_err}")
                        print(f"[EMAIL ERROR] Falha ao enviar e-mail: {mail_err}")
                    
                    if email_enviado_com_sucesso:
                        cursor.execute("""
                            UPDATE delivery.orders 
                            SET delivery_notified = TRUE, updated_at = CURRENT_TIMESTAMP 
                            WHERE id = %s
                        """, (order_id,))
                        conn.commit()

    except Exception as e:
        print(f"[CELERY ERROR] Erro na conexão ou varredura do banco: {e}")
        logger.error(f"[CELERY ERROR] Erro na conexão ou varredura do banco: {e}")