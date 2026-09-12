import logging
import smtplib
from email.message import EmailMessage
from typing import Optional
from core.config.settings import settings

logger = logging.getLogger(__name__)


class EmailService:
    
    @staticmethod
    def send_human_escalation_alert(
        customer_name: Optional[str],
        customer_phone: str,
        last_message: str,
        order_id: Optional[str] = None
    ) -> bool:
        """
        Envia um e-mail estruturado para a gerência do Bar do Jaum informando a solicitação de atendimento humano.
        """
        EMAIL_ORIGEM = settings.EMAIL_ORIGEM
        SENHA_APP = settings.SENHA_APP
        EMAIL_DESTINO = settings.EMAIL_DESTINO

        msg = EmailMessage()
        msg["Subject"] = f"🚨 ATENDIMENTO HUMANO SOLICITADO - {customer_name or customer_phone}"
        msg["From"] = EMAIL_ORIGEM
        msg["To"] = EMAIL_DESTINO

        corpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
                    <h2 style="color: #d9534f; border-bottom: 2px solid #d9534f; padding-bottom: 10px; margin-top: 0;">
                        🚨 Solicitação de Atendimento Humano
                    </h2>
                    <p>Um cliente acabou de pedir ajuda de um atendente humano no chat do <strong>Bar do Jaum</strong>.</p>
                    
                    <div style="background-color: #fff; padding: 15px; border-radius: 6px; border: 1px solid #e1e1e1; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #333; border-bottom: 1px solid #eee; padding-bottom: 8px;">Detalhes do Contato</h3>
                        <ul style="list-style-type: none; padding: 0; margin: 0;">
                            <li style="padding: 4px 0;"><strong>👤 Nome:</strong> {customer_name or 'Não informado'}</li>
                            <li style="padding: 4px 0;"><strong>📱 Telefone / WhatsApp:</strong> {customer_phone}</li>
                            <li style="padding: 4px 0;"><strong>📦 ID do Pedido:</strong> {order_id or 'Nenhum pedido vinculado'}</li>
                        </ul>
                    </div>

                    <div style="background-color: #fff3cd; padding: 15px; border-radius: 6px; border: 1px solid #ffeeba; margin: 20px 0;">
                        <h4 style="margin-top: 0; color: #856404;">💬 Última Mensagem do Cliente:</h4>
                        <p style="margin: 0; font-style: italic; color: #533f03;">"{last_message}"</p>
                    </div>

                    <p style="font-size: 14px; color: #666; text-align: center; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px;">
                        Sistema Automatizado - Bar do Jaum Delivery 🍻
                    </p>
                </div>
            </body>
        </html>
        """
        
        msg.set_content(
            f"O cliente {customer_name or customer_phone} solicitou atendimento humano.\n"
            f"Telefone: {customer_phone}\n"
            f"Pedido: {order_id or 'Nenhum'}\n"
            f"Mensagem: {last_message}"
        )
        msg.add_alternative(corpo_html, subtype="html")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ORIGEM, SENHA_APP)
                smtp.send_message(msg)
            
            logger.info(f"E-mail de escalação estruturado enviado com sucesso para o cliente {customer_phone}.")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar o e-mail estruturado de alerta: {e}")
            return False

    @staticmethod
    def send_order_status_alert(
        customer_name: Optional[str],
        customer_phone: str,
        order_id: str,
        status_description: str
    ) -> bool:
        """Envia um e-mail limpo para a gerência informando a mudança de status do pedido."""
        EMAIL_ORIGEM = settings.EMAIL_ORIGEM
        SENHA_APP = settings.SENHA_APP
        EMAIL_DESTINO = settings.EMAIL_DESTINO

        msg = EmailMessage()
        msg["Subject"] = f"🍻 STATUS DO PEDIDO #{order_id} - {status_description}"
        msg["From"] = EMAIL_ORIGEM
        msg["To"] = EMAIL_DESTINO

        corpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
                    <h2 style="color: #0275d8; border-bottom: 2px solid #0275d8; padding-bottom: 10px; margin-top: 0;">
                        🍻 Atualização de Pedido - Bar do Jaum
                    </h2>
                    <p>O status de um pedido foi atualizado no sistema.</p>
                    
                    <div style="background-color: #fff; padding: 15px; border-radius: 6px; border: 1px solid #e1e1e1; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #333; border-bottom: 1px solid #eee; padding-bottom: 8px;">Detalhes</h3>
                        <ul style="list-style-type: none; padding: 0; margin: 0;">
                            <li style="padding: 4px 0;"><strong>📦 ID do Pedido:</strong> #{order_id}</li>
                            <li style="padding: 4px 0;"><strong>📌 Novo Status:</strong> {status_description}</li>
                            <li style="padding: 4px 0;"><strong>👤 Cliente:</strong> {customer_name or 'Não informado'}</li>
                            <li style="padding: 4px 0;"><strong>📱 WhatsApp:</strong> {customer_phone}</li>
                        </ul>
                    </div>

                    <p style="font-size: 14px; color: #666; text-align: center; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px;">
                        Sistema Automatizado - Bar do Jaum Delivery 🍻
                    </p>
                </div>
            </body>
        </html>
        """
        
        msg.set_content(f"Pedido #{order_id} atualizado para: {status_description}. Cliente: {customer_name or customer_phone}")
        msg.add_alternative(corpo_html, subtype="html")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ORIGEM, SENHA_APP)
                smtp.send_message(msg)
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar o e-mail de status do pedido: {e}")
            return False

    @staticmethod
    def send_order_notification_email(
        customer_email: str,
        customer_name: Optional[str],
        order_id: str,
        status_type: str,
        total_amount: Optional[float] = None
    ) -> bool:
        EMAIL_ORIGEM = settings.EMAIL_ORIGEM
        SENHA_APP = settings.SENHA_APP

        nome_exibicao = customer_name or "Cliente"
        
        if status_type == "APPROVED":
            assunto = f"🍻 PEDIDO APROVADO - Pedido #{order_id}"
            titulo_box = "PEDIDO APROVADO"
            cor_destaque = "#5cb85c"
            mensagem_principal = f"Recebemos a confirmação do seu pagamento. Seu pedido <strong>#{order_id}</strong> foi aprovado com sucesso e já está sendo preparado, meu amigo!"
        elif status_type == "OUT_FOR_DELIVERY":
            assunto = f"🛵 SEU PEDIDO SAIU PARA A ENTREGA - Pedido #{order_id}"
            titulo_box = "SEU PEDIDO SAIU PARA A ENTREGA"
            cor_destaque = "#f0ad4e"
            mensagem_principal = f"Prepare os copos! O entregador já está a caminho com as suas bebidas do pedido <strong>#{order_id}</strong>. Fique atento para receber!"
        else:
            return False

        msg = EmailMessage()
        msg["Subject"] = assunto
        msg["From"] = EMAIL_ORIGEM
        msg["To"] = customer_email

        corpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9;">
                    <div style="text-align: center; border-bottom: 2px solid {cor_destaque}; padding-bottom: 15px; margin-bottom: 20px;">
                        <h1 style="color: #333; margin: 0; font-size: 24px;">Bar do Jaum 🍻</h1>
                    </div>

                    <h2 style="color: {cor_destaque}; margin-top: 0; text-align: center;">{titulo_box}</h2>
                    
                    <p>Fala aí, <strong>{nome_exibicao}</strong>!</p>
                    
                    <p>{mensagem_principal}</p>
                    
                    <div style="background-color: #fff; padding: 15px; border-radius: 6px; border: 1px solid #e1e1e1; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #333; border-bottom: 1px solid #eee; padding-bottom: 8px;">Resumo do Pedido</h3>
                        <p style="margin: 4px 0;"><strong>🆔 Número do Pedido:</strong> #{order_id}</p>
                        {f'<p style="margin: 4px 0;"><strong>💰 Valor Total:</strong> R$ {total_amount:.2f}</p>' if total_amount else ''}
                    </div>

                    <p style="font-size: 14px; color: #555;">Qualquer dúvida, é só chamar a gente por aqui ou no WhatsApp. Valeu pela preferência!</p>

                    <p style="font-size: 13px; color: #888; text-align: center; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px;">
                        Bar do Jaum Delivery • Todos os direitos reservados.
                    </p>
                </div>
            </body>
        </html>
        """

        msg.set_content(f"Olá {nome_exibicao}, status do seu pedido #{order_id}: {status_type}")
        msg.add_alternative(corpo_html, subtype="html")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ORIGEM, SENHA_APP)
                smtp.send_message(msg)
            
            logger.info(f"E-mail de status ({status_type}) enviado com sucesso para {customer_email}.")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar o e-mail de status do pedido: {e}")
            return False