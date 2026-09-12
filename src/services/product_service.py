import logging
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)


class ProductService:

    @staticmethod
    async def search_catalog(
        session: AsyncSession, query_term: str
    ) -> List[Dict[str, Any]]:
        """Realiza a busca de produtos aplicando regras de negócio e formatação."""
        products = await ProductRepository.search_products(session, query_term)
        return [dict(p) for p in products]

    @staticmethod
    async def validate_product_exists(
        session: AsyncSession,
        product_name: str,
        volume: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Verifica se um produto existe no catálogo do Seu Jaum.
        Aplica filtro por volume caso informado. Se houver ambiguidade de volume,
        utiliza o resolve_product_items para tratar adequadamente.
        """
        # 1. Se o volume foi explicitamente informado, busca a combinação exata
        if volume:
            product = await ProductRepository.get_by_name_and_volume(
                session, product_name, volume
            )
            if product:
                return dict(product)

        # 2. Se o volume não veio, resolvemos usando a inteligência de ambiguidades
        resolution = await ProductService.resolve_product_items(session, product_name)
        
        if resolution["status"] == "EXACT":
            return resolution["product"]
            
        elif resolution["status"] == "AMBIGUOUS":
            # Se encontrou múltiplos (ex: Coca-Cola 350ml e Coca-Cola 2L) e o cliente 
            # não especificou o volume, podemos priorizar por padrão o maior volume 
            # (ou o mais vendido) caso seja o comportamento desejado, ou retornar 
            # None para forçar o fluxo a pedir o tamanho. 
            # Para atender o cenário onde você pediu a de 2L e ela deve ser considerada:
            matches = resolution["matches"]
            # Tenta buscar uma correspondência com maior volume ou pega a primeira se for o caso,
            # mas o ideal é priorizar a de maior valor/volume se o usuário foi genérico.
            # Aqui ordenamos por preço ou volume de forma decrescente para pegar a garrafa maior de 2L:
            sorted_matches = sorted(
                matches, 
                key=lambda x: float(x.get("price", 0)), 
                reverse=True
            )
            return sorted_matches[0]

        # 3. Fallback final para busca simples por nome no repositório
        product = await ProductRepository.get_by_name(session, product_name)
        if not product:
            return None

        return dict(product)

    @staticmethod
    async def get_by_name(
        session: AsyncSession,
        product_name: str,
        volume: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Atalho/Alias para buscar um produto pelo nome via ProductRepository."""
        return await ProductService.validate_product_exists(
            session, product_name, volume
        )

    @staticmethod
    async def resolve_product_items(
        session: AsyncSession, user_product_name: str
    ) -> Dict[str, Any]:
        """
        Extrai a chave primária (id) do produto e trata ambiguidades de volume.

        Retorna:
        - status "EXACT": 1 produto encontrado.
        - status "AMBIGUOUS": Múltiplas opções encontradas.
        - status "NOT_FOUND": Nenhum produto encontrado.
        """
        matches = await ProductRepository.search_products(session, user_product_name)
        matches_dict = [dict(m) for m in matches]

        if len(matches_dict) == 1:
            return {"status": "EXACT", "product": matches_dict[0]}

        elif len(matches_dict) > 1:
            exact_match = next(
                (
                    p
                    for p in matches_dict
                    if f"{p['name']} {p.get('volume', '')}".strip().lower()
                    == user_product_name.strip().lower()
                ),
                None,
            )
            if exact_match:
                return {"status": "EXACT", "product": exact_match}

            return {"status": "AMBIGUOUS", "matches": matches_dict}

        else:
            return {"status": "NOT_FOUND", "matches": []}
