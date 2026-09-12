from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from services.product_service import ProductService


class SearchProductsHandler:
    @staticmethod
    async def handle(session: AsyncSession, raw_message: str, nlu_result: Any) -> str:
        """Gerencia buscas e listagens de produtos no catálogo extraindo termos ou categorias priorizadas pela LLM."""
        query_term = None

        if nlu_result.product_search:
            if nlu_result.product_search.query:
                query_term = nlu_result.product_search.query
            elif nlu_result.product_search.category:
                query_term = nlu_result.product_search.category

        # Se a LLM não extraiu nem termo nem categoria, buscamos todo o catálogo disponível em estoque
        if not query_term:
            products = await ProductService.search_catalog(session, "")
        else:
            products = await ProductService.search_catalog(session, query_term)

            # Fallback caso a busca específica não retorne nada: exibe todo o catálogo disponível para o cliente não ficar travado
            if not products:
                products = await ProductService.search_catalog(session, "")

        if not products:
            return "Poxa, no momento estamos com o estoque vazio ou em manutenção. Tente chamar mais tarde!"

        # ==========================================================
        # TRATAMENTO DE AMBIGUIDADE DE VOLUMES (EX: COCA-COLA)
        # ==========================================================
        # Se o usuário buscou um termo genérico (ex: "coca-cola") e a busca retornou
        # múltiplos produtos com o mesmo nome base mas volumes diferentes, listamos
        # explicitamente as opções para o cliente escolher o tamanho correto.
        if query_term:
            normalized_query = query_term.strip().lower()
            matching_products = [
                p for p in products 
                if normalized_query in p['name'].lower()
            ]
            
            if len(matching_products) > 1:
                options_str = "\n".join(
                    [f"- {p['name']} ({p.get('volume', 'N/I')}) - R$ {float(p['price']):.2f}" for p in matching_products]
                )
                return f"Encontrei algumas opções para '{query_term}'. Qual o tamanho você prefere?\n{options_str}"

        # Conversão explícita para float() para evitar erros de formatação com tipo Decimal vindo do banco
        product_list_str = "\n".join(
            [f"- {p['name']} ({p.get('volume', 'N/I')}) - R$ {float(p['price']):.2f}" for p in products]
        )
        return f"Aqui estão os produtos disponíveis no Bar do Jaum:\n{product_list_str}\n\nO que vai ser hoje?"
    