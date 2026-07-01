"""Fontes de mineração (cada loja é uma fonte)."""
from .mercadolivre import MercadoLivre
from .shopee import Shopee

# Lista de fontes que o robô vai percorrer em cada rodada.
FONTES = [MercadoLivre, Shopee]

__all__ = ["MercadoLivre", "Shopee", "FONTES"]
