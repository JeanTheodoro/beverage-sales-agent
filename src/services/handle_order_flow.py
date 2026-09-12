import logging
from typing import Any, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from services.order_service import OrderService
from services.session_service import SessionService

logger = logging.getLogger(__name__)


class HandleOrderFlow:

    @staticmethod
    def _format_cart_summary(items: List[Dict[str, Any]]) -> tuple[str, float]:
        """Gera o texto do resumo dos itens e calcula o subtotal."""
        if not items:
            return "Seu carrinho está vazio.", 0.0

        lines = []
        total = 0.0
        for item in items:
            name = item.get("product_name", "Produto")
            volume = item.get("volume")
            vol_str = f" ({volume})" if volume else ""
            qty = item.get("quantity", 1)
            unit_price = item.get("unit_price", 0.0)
            subtotal = qty * unit_price
            total += subtotal

            lines.append(f"• {qty}x {name}{vol_str} - R$ {subtotal:.2f}")

        cart_text = "\n".join(lines)
        return cart_text, total

    @staticmethod
    async def handle(
        session: AsyncSession, customer_phone: str, nlu_result: Any
    ) -> str:
        """Gerencia o fluxo do pedido acumulando dados na sessão turno a turno."""

        # 1. Extrai dados da mensagem atual vindos do NLU
        raw_items = getattr(nlu_result, "items", []) or []
        raw_removals = getattr(nlu_result, "items_to_remove", []) or []

        new_items = [
            {
                "product_id": getattr(item, "product_id", None),
                "product_name": getattr(
                    item, "product_name", getattr(item, "product", "")
                ),
                "quantity": getattr(item, "quantity", 1),
                "unit_price": getattr(item, "unit_price", 0.0),
                "volume": getattr(item, "volume", None),
            }
            for item in raw_items
        ]

        items_to_remove = [
            {
                "product_id": getattr(item, "product_id", None),
                "product_name": getattr(
                    item, "product_name", getattr(item, "product", "")
                ),
                "quantity": getattr(item, "quantity", 0),
            }
            for item in raw_removals
        ]

        customer_name = getattr(nlu_result, "customer_name", None)
        address = getattr(nlu_result, "address", None)
        payment_method = getattr(nlu_result, "payment_method", None)
        cash_received = getattr(nlu_result, "cash_received", None)

        # 2. Atualiza a sessão no Redis
        session_data = await SessionService.update_session(
            session=session,
            customer_phone=customer_phone,
            customer_name=customer_name,
            address=address,
            payment_method=payment_method,
            cash_received=cash_received,
            items=new_items if new_items else None,
            items_to_remove=items_to_remove if items_to_remove else None,
        )

        # 3. Recupera o estado consolidado
        accumulated_items = session_data.get("items", [])
        accumulated_address = session_data.get("address")
        accumulated_payment = session_data.get("payment_method")
        accumulated_name = session_data.get("customer_name")
        accumulated_cash = session_data.get("cash_received")

        # Se não há itens e o usuário não enviou novos itens, solicita a escolha do produto
        if not accumulated_items:
            return (
                "Seu carrinho está vazio! O que gostaria de pedir hoje? "
                "Temos cervejas, refrigerantes, águas e petiscos."
            )

        # Formata o carrinho parcial
        cart_summary_str, subtotal = HandleOrderFlow._format_cart_summary(
            accumulated_items
        )

        # 4. Verifica quais dados cadastrais ainda faltam
        missing_info = []
        if not accumulated_name:
            missing_info.append("*nome*")
        if not accumulated_address:
            missing_info.append("*endereço completo* de entrega")
        if not accumulated_payment:
            missing_info.append(
                "*forma de pagamento* (pix, dinheiro ou cartão)"
            )

        # 5. Se ainda faltam dados cadastrais, solicita ao cliente mostrando o resumo atual
        if missing_info:
            response_lines = ["Anotado! Confira seu pedido até agora:\n"]
            response_lines.append(cart_summary_str)
            response_lines.append(f"\n*Total parcial: R$ {subtotal:.2f}*")

            # Mostra o que já foi preenchido de cadastro
            if accumulated_name:
                response_lines.append(f"👤 *Nome:* {accumulated_name}")
            if accumulated_address:
                response_lines.append(f"📍 *Endereço:* {accumulated_address}")

            if len(missing_info) == 3:
                response_lines.append(
                    "\nDeseja adicionar mais algum item ou podemos finalizar? "
                    "Se quiser finalizar, me informe por favor seu *nome*, *endereço completo* e *forma de pagamento*."
                )
            else:
                missing_str = ", ".join(missing_info)
                response_lines.append(
                    f"\nPerfeito! Para finalizarmos, me informe por favor: o {missing_str}."
                )

            return "\n".join(response_lines)

        # 6. Se TUDO estiver preenchido (Itens + Nome + Endereço + Pagamento), cria o pedido
        try:
            order = await OrderService.create_new_order(
                session=session,
                customer_name=accumulated_name,
                customer_phone=customer_phone,
                address=accumulated_address,
                payment_method=accumulated_payment,
                cash_received=accumulated_cash,
                items=accumulated_items,
            )

            # Limpa a sessão no Redis após criar o pedido com sucesso
            await SessionService.clear_session(session, customer_phone)

            pix_info = ""
            if accumulated_payment.lower() == "pix":
                pix_info = (
                    "\n\nNosso Pix para pagamento é: *jaum1236@delivery.com*\n"
                    "Assim que fizer o pagamento, envie o comprovante por aqui!"
                )

            return (
                f"Pedido #{order['id']} criado com sucesso para *{accumulated_name}*! "
                f"O total é R$ {order['total_amount']:.2f} (inclusa taxa de entrega)."
                f"{pix_info}\n\nObrigado pela preferência no Bar do Jaum! 🍻"
            )

        except ValueError as e:
            logger.error(
                f"Erro de validação ao criar pedido para {customer_phone}: {e}"
            )
            return f"Ops! Não foi possível concluir o pedido: {e}"
        except Exception as e:
            logger.error(
                f"Erro inesperado ao criar pedido para {customer_phone}: {e}"
            )
            return "Ops! Ocorreu um erro interno ao processar seu pedido. Por favor, tente novamente em alguns instantes."
