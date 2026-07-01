"""Fonte: Mercado Livre.

Usa a API pública de busca do Mercado Livre, que devolve título, preço,
link (permalink) e foto (thumbnail) de cada produto — exatamente o que
o robô precisa. Não exige credenciais para buscar.

Docs: https://developers.mercadolivre.com.br/
"""
import requests

from .base import FonteBase
from ..models import Produto
from .. import config


class MercadoLivre(FonteBase):
    nome = "Mercado Livre"
    URL_BUSCA = "https://api.mercadolibre.com/sites/MLB/search"  # MLB = Brasil

    # Cabeçalhos de navegador: a API costuma bloquear (403) requisições com
    # User-Agent genérico de robô. Simulando um navegador, o acesso passa.
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    }

    def __init__(self):
        self.tag = config.ML_AFFILIATE_TAG

    def _com_tag(self, link: str) -> str:
        """Anexa a tag de afiliado ao link, se configurada."""
        if not self.tag:
            return link
        sep = "&" if "?" in link else "?"
        return f"{link}{sep}matt_tool={self.tag}"

    def buscar(self, termo: str, limite: int) -> list[Produto]:
        params = {"q": termo, "limit": limite}
        try:
            resp = requests.get(self.URL_BUSCA, params=params, headers=self.HEADERS, timeout=20)
            resp.raise_for_status()
            itens = resp.json().get("results", [])
        except (requests.RequestException, ValueError) as erro:
            print(f"  [Mercado Livre] falha ao buscar '{termo}': {erro}")
            return []

        produtos: list[Produto] = []
        for item in itens:
            # A thumbnail vem em http e baixa resolução; troca por https.
            foto = (item.get("thumbnail") or "").replace("http://", "https://")
            produtos.append(
                Produto(
                    fonte=self.nome,
                    id_externo=str(item.get("id", "")),
                    titulo=item.get("title", ""),
                    preco=float(item.get("price") or 0),
                    preco_antigo=(
                        float(item["original_price"])
                        if item.get("original_price")
                        else None
                    ),
                    link=self._com_tag(item.get("permalink", "")),
                    foto=foto,
                    vendas=item.get("sold_quantity"),
                )
            )
        return produtos
