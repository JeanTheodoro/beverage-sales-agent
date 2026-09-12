import logging
from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class ProductRepository:

    @staticmethod
    async def search_products(
        session: AsyncSession,
        query_term: str,
    ) -> List[Dict[str, Any]]:
        """
        Busca produtos por Full-Text Search e ILIKE, considerando apenas produtos com estoque positivo.
        Se o termo de busca for vazio, retorna todo o catálogo disponível em estoque.
        """
        clean_term = query_term.strip().lower()

        if not clean_term:
            return await ProductRepository.get_all_available(session)

        sql = text("""
            SELECT
                id,
                name,
                description,
                price,
                stock_quantity,
                volume,
                category
            FROM delivery.products
            WHERE stock_quantity > 0
              AND (
                to_tsvector(
                    'portuguese',
                    unaccent(
                        coalesce(name, '') || ' ' ||
                        coalesce(description, '') || ' ' ||
                        coalesce(category, '')
                    )
                )
                @@ plainto_tsquery(
                    'portuguese',
                    unaccent(:term)
                )

                OR unaccent(name)
                    ILIKE unaccent(:like_term)

                OR unaccent(description)
                    ILIKE unaccent(:like_term)

                OR unaccent(category)
                    ILIKE unaccent(:like_term)
              )
            ORDER BY name
        """)

        result = await session.execute(
            sql,
            {
                "term": clean_term,
                "like_term": f"%{clean_term}%",
            },
        )

        rows = result.mappings().all()
        return [dict(row) for row in rows]

    @staticmethod
    async def get_all_available(session: AsyncSession) -> List[Dict[str, Any]]:
        """Retorna todos os produtos que possuem estoque maior que zero."""
        sql = text("""
            SELECT
                id,
                name,
                description,
                price,
                stock_quantity,
                volume,
                category
            FROM delivery.products
            WHERE stock_quantity > 0
            ORDER BY name
        """)
        result = await session.execute(sql)
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    @staticmethod
    async def get_by_name(session: AsyncSession, product_name: str) -> Optional[Dict[str, Any]]:
        """Busca um produto no catálogo pelo nome ou variação com volume, de forma flexível."""
        
        clean_name = product_name.split("(")[0].strip()
        
        query = text("""
            SELECT id, name, description, price, stock_quantity, volume, category 
            FROM delivery.products 
            WHERE stock_quantity > 0
              AND unaccent(name) ILIKE unaccent(:search_name)
            ORDER BY 
                CASE WHEN volume ILIKE :full_query THEN 0 ELSE 1 END,
                price ASC
            LIMIT 1
        """)
        
        result = await session.execute(
            query, 
            {
                "search_name": f"%{clean_name}%",
                "full_query": f"%{product_name}%"
            }
        )
        row = result.mappings().first()
        
        return dict(row) if row else None

    @staticmethod
    async def get_by_id(session: AsyncSession, product_id: int) -> Optional[Dict[str, Any]]:
        """Busca um produto diretamente pela chave primária (id)."""
        query = text("""
            SELECT id, name, description, price, stock_quantity, volume, category
            FROM delivery.products
            WHERE id = :product_id
            LIMIT 1
        """)
        result = await session.execute(query, {"product_id": product_id})
        row = result.mappings().first()
        return dict(row) if row else None

    @staticmethod
    async def get_by_name_and_volume(
        session: AsyncSession, name: str, volume: str
    ) -> Optional[Dict[str, Any]]:
        """Busca um produto combinando nome e volume no catálogo."""
        clean_name = name.split("(")[0].strip()

        query = text("""
            SELECT id, name, description, price, stock_quantity, volume, category
            FROM delivery.products
            WHERE stock_quantity > 0
              AND unaccent(name) ILIKE unaccent(:name)
              AND unaccent(volume) ILIKE unaccent(:volume)
            LIMIT 1
        """)

        result = await session.execute(
            query,
            {
                "name": f"%{clean_name}%",
                "volume": f"%{volume}%",
            },
        )
        row = result.mappings().first()
        return dict(row) if row else None
