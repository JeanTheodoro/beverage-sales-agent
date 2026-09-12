import logging
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.nlu import ClassificationResult, Intent
from services.order_service import OrderService
from services.product_service import ProductService
from services.session_service import SessionService

logger = logging.getLogger(__name__)

# Intenções reconhecidas pela LLM que sinalizam intenção de avanço/envio de dados
ADVANCE_INTENTS = {
    Intent.FINALIZE_ORDER.value,
    Intent.ORDER_CONFIRMATION.value,
    Intent.NEGATIVE.value,
    Intent.PROVIDE_ADDRESS.value,
    Intent.PROVIDE_NAME.value,
    Intent.PAYMENT.value,
    Intent.AFFIRMATIVE.value,
}


class HandleOrderFlow:

    @staticmethod
    async def handle(
        session: AsyncSession,
        customer_phone: str,
        nlu_result: ClassificationResult,
        user_raw_text: str = "",
    ) -> str:
        """
        Gerencia o fluxo conversacional do pedido acoplando intenções do NLU,
        acumulando estado da sessão no banco/Redis e validando pendências até a efetivação.
        """

        intent_value = (
            nlu_result.intent.value
            if isinstance(nlu_result.intent, Intent)
            else str(nlu_result.intent)
        )

        # 0. Tratamento de cancelamento total do pedido
        if intent_value == Intent.ORDER_CANCELLATION.value:
            await SessionService.clear_session(session, customer_phone)
            return (
                "Seu pedido e os dados em andamento foram cancelados. "
                "Se precisar de algo mais, é só me chamar!"
            )

        # 1. Recupera o estado atual da sessão
        current_session = await SessionService.get_session(session, customer_phone)
        existing_items = current_session.get("items", [])

        # 2. Processa novos itens trazidos pela NLU
        new_items = []
        remove_items = []
        unrecognized_products = []  # Guarda produtos não encontrados no banco para informar o cliente

        if nlu_result.items:
            for item in nlu_result.items:
                product_db = await ProductService.validate_product_exists(
                    session, item.product, item.volume
                )

                # Se o produto NÃO existe no banco de dados, busca sugestões no catálogo
                if not product_db:
                    similar_products = await ProductService.search_catalog(session, item.product)
                    unrecognized_products.append({
                        "requested_term": item.product,
                        "suggestions": similar_products
                    })
                    continue

                raw_price = product_db.get("price", 0.0) if product_db else 0.0
                unit_price = float(raw_price) if raw_price is not None else 0.0

                vol_suffix = f" ({product_db['volume']})" if product_db and product_db.get("volume") else ""
                prod_name = f"{product_db['name']}{vol_suffix}" if product_db else item.product

                item_data = {
                    "product": prod_name,          # Esperado pelo OrderService
                    "product_name": prod_name,     # Usado no resumo do carrinho
                    "quantity": int(item.quantity),
                    "unit_price": unit_price,
                }

                if product_db and product_db.get("id"):
                    item_data["product_id"] = product_db["id"]

                if intent_value == Intent.REMOVE_FROM_CART.value:
                    remove_items.append(item_data)
                else:
                    new_items.append(item_data)

        # Se houver algum produto não reconhecido no banco, informa as opções disponíveis
        if unrecognized_products:
            msg_parts = []
            for unrec in unrecognized_products:
                term = unrec["requested_term"]
                suggestions = unrec["suggestions"]

                if suggestions:
                    options_list = [
                        f"- {p['name']} ({p.get('volume', 'N/I')}) - R$ {float(p['price']):.2f}"
                        for p in suggestions
                    ]
                    options_str = "\n".join(options_list)
                    msg_parts.append(
                        f"Poxa, não encontrei '{term}' no nosso cardápio. Temos estas opções disponíveis:\n{options_str}"
                    )
                else:
                    msg_parts.append(f"Poxa, no momento não temos '{term}' em nosso estoque.")

            summary_prefix = ""
            if existing_items or new_items:
                # Salva os itens válidos que foram informados até o momento
                if new_items:
                    existing_items = HandleOrderFlow._merge_items(existing_items, new_items)
                    await SessionService.update_session(
                        session=session,
                        customer_phone=customer_phone,
                        updates={"items": existing_items},
                    )
                summary_prefix = f"{HandleOrderFlow._build_items_summary(existing_items)}\n\n"

            joined_msg_parts = "\n\n".join(msg_parts)
            return f"{summary_prefix}{joined_msg_parts}\n\nQual dessas opções você prefere?"

        # 3. Mescla os novos itens com os itens que já estavam no carrinho
        updated_items = list(existing_items)

        # Trata remoções
        if remove_items:
            for r_item in remove_items:
                r_id = r_item.get("product_id")
                r_name = (r_item.get("product") or r_item.get("product_name") or "").strip().lower()

                filtered_items = []
                for i in updated_items:
                    i_id = i.get("product_id")
                    i_name = (i.get("product") or i.get("product_name") or "").strip().lower()

                    is_match = False
                    if r_id and i_id and r_id == i_id:
                        is_match = True
                    elif r_name and i_name and (r_name == i_name or r_name in i_name or i_name in r_name):
                        is_match = True

                    if not is_match:
                        filtered_items.append(i)

                updated_items = filtered_items

        # Trata adições / atualizações de quantidade
        if new_items:
            updated_items = HandleOrderFlow._merge_items(updated_items, new_items)

        # 4. Monta o payload de atualização de sessão mantendo valores existentes
        session_updates = {
            "items": updated_items,
        }

        if nlu_result.customer_name:
            session_updates["customer_name"] = nlu_result.customer_name
        if nlu_result.address:
            session_updates["address"] = nlu_result.address
        if nlu_result.payment_method:
            session_updates["payment_method"] = nlu_result.payment_method
        if nlu_result.cash_received is not None:
            session_updates["cash_received"] = float(nlu_result.cash_received)

        session_data = await SessionService.update_session(
            session=session,
            customer_phone=customer_phone,
            updates=session_updates,
        )

        accumulated_items = session_data.get("items", [])
        accumulated_address = session_data.get("address")
        accumulated_payment = session_data.get("payment_method")
        accumulated_name = session_data.get("customer_name")
        accumulated_cash = session_data.get("cash_received")

        # Se o carrinho estiver vazio
        if not accumulated_items:
            return "Seu carrinho está vazio! O que você gostaria de pedir hoje?"

        # 5. Verificação de intenção de avanço
        wants_to_advance = (
            intent_value in ADVANCE_INTENTS
            or bool(nlu_result.address or nlu_result.payment_method or nlu_result.customer_name)
        )

        # ETAPA A: Cliente alterou produtos e NÃO solicitou avanço
        if (new_items or remove_items) and not wants_to_advance:
            summary_text = HandleOrderFlow._build_items_summary(accumulated_items)
            return (
                f"{summary_text}\n\n"
                f"Deseja adicionar mais algum item ao seu pedido ou podemos avançar?"
            )

        # ETAPA B: Cliente confirmou avanço, mas faltam dados obrigatórios (Nome, Endereço ou Pagamento)
        missing_info = []
        if not accumulated_name:
            missing_info.append("seu *nome*")
        if not accumulated_address:
            missing_info.append("o *endereço completo* de entrega")
        if not accumulated_payment:
            missing_info.append("a *forma de pagamento* (pix, dinheiro ou cartão)")

        if missing_info:
            if len(missing_info) == 1:
                missing_str = missing_info[0]
            else:
                missing_str = ", ".join(missing_info[:-1]) + " e " + missing_info[-1]

            summary_text = HandleOrderFlow._build_items_summary(accumulated_items)

            saved_details = []
            if accumulated_name:
                saved_details.append(f"👤 *Nome:* {accumulated_name}")
            if accumulated_address:
                saved_details.append(f"📍 *Endereço:* {accumulated_address}")
            if accumulated_payment:
                payment_text = f"💳 *Pagamento:* {accumulated_payment.upper()}"
                if accumulated_payment.lower() in ["cash", "dinheiro"] and accumulated_cash:
                    payment_text += f" (Troco para R$ {accumulated_cash:.2f})"
                saved_details.append(payment_text)

            details_str = ("\n" + "\n".join(saved_details)) if saved_details else ""

            return (
                f"{summary_text}{details_str}\n\n"
                f"Perfeito! Para finalizarmos, me informe por favor: {missing_str}."
            )

        # ETAPA C: Todas as informações preenchidas -> Criação do Pedido
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

            await SessionService.clear_session(session, customer_phone)
            total_amount = float(order.get("total_amount", 0.0))

            if accumulated_payment and accumulated_payment.lower() == "pix":
                return (
                    f"Pedido #{order['id']} criado com sucesso para *{accumulated_name}*! O total é R$ {total_amount:.2f} "
                    f"(inclusa taxa de entrega).\n\n"
                    f"Nosso Pix para pagamento é: *jaum1236@delivery.com*\n"
                    f"Assim que fizer o pagamento, envie o comprovante por aqui para aprovarmos o seu pedido, meu amigo!"
                )

            return (
                f"Pedido #{order['id']} criado com sucesso para *{accumulated_name}*! O total é R$ {total_amount:.2f} "
                f"(inclusa taxa de entrega). Seu pedido foi enviado para aprovação e logo entraremos em contato, amigo!"
            )
        except Exception as e:
            logger.error(f"ERRO AO CRIAR PEDIDO NO ORDER SERVICE: {str(e)}", exc_info=True)
            return "Ops! Não foi possível concluir o seu pedido no momento. Por favor, tente novamente em alguns instantes."

    @staticmethod
    def _merge_items(existing_items: List[dict], new_items: List[dict]) -> List[dict]:
        """Auxiliar para mesclar e incrementar quantidades de itens no carrinho."""
        updated_items = list(existing_items)
        for n_item in new_items:
            found = False
            n_id = n_item.get("product_id")
            n_name = (n_item.get("product") or n_item.get("product_name") or "").strip().lower()

            for item in updated_items:
                item_id = item.get("product_id")
                item_name = (item.get("product") or item.get("product_name") or "").strip().lower()

                is_same_product = False
                if n_id and item_id and n_id == item_id:
                    is_same_product = True
                elif n_name and item_name and n_name == item_name:
                    is_same_product = True
                elif n_name and item_name and (n_name in item_name or item_name in n_name):
                    is_same_product = True

                if is_same_product:
                    item["quantity"] += n_item["quantity"]
                    if item.get("unit_price", 0.0) == 0.0 and n_item.get("unit_price", 0.0) > 0:
                        item["unit_price"] = n_item["unit_price"]
                        item["product"] = n_item["product"]
                        item["product_name"] = n_item["product_name"]

                    if not item.get("product_id") and n_id:
                        item["product_id"] = n_id

                    found = True
                    break

            if not found:
                updated_items.append(n_item)
        return updated_items

    @staticmethod
    def _build_items_summary(items: List[dict]) -> str:
        """Gera o resumo formatado do carrinho com subtotais calculados em código."""
        formatted_items = []
        total_items_price = 0.0

        for item in items:
            qty = int(item.get("quantity", 1))
            price = float(item.get("unit_price", 0.0))
            item_name = item.get("product_name") or item.get("product", "Produto")

            subtotal = qty * price
            total_items_price += subtotal

            if price > 0:
                formatted_items.append(f"• {qty}x {item_name} - R$ {subtotal:.2f}")
            else:
                formatted_items.append(f"• {qty}x {item_name}")

        items_str = "\n".join(formatted_items)
        return f"Anotado! Confira seu pedido até agora:\n\n{items_str}\n\n*Total parcial: R$ {total_items_price:.2f}*"
