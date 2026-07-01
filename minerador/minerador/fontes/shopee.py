"""Fonte: Shopee.

Usa a Open API oficial do programa de Afiliados da Shopee (GraphQL).
Esse é o caminho recomendado e estável: você gera um App ID e um App
Secret no painel de afiliados e o robô assina cada requisição.

Painel: https://affiliate.shopee.com.br  ->  Painel do desenvolvedor

Se as credenciais não estiverem preenchidas no .env, a fonte se declara
indisponível e é pulada — o robô continua rodando só com o Mercado Livre.
"""
import hashlib
import json
import time

import requests

from .base import FonteBase
from ..models import Produto
from .. import config


class Shopee(FonteBase):
    nome = "Shopee"
    URL_API = "https://open-api.affiliate.shopee.com.br/graphql"

    # Consulta GraphQL: pede link, imagem, preço, vendas e avaliação.
    QUERY = """
    query Buscar($palavra: String!, $limite: Int!) {
      productOfferV2(keyword: $palavra, limit: $limite, sortType: 2) {
        nodes {
          itemId
          productName
          priceMin
          priceMax
          imageUrl
          offerLink
          sales
          ratingStar
        }
      }
    }
    """

    def __init__(self):
        self.app_id = config.SHOPEE_APP_ID
        self.app_secret = config.SHOPEE_APP_SECRET

    def disponivel(self) -> bool:
        return bool(self.app_id and self.app_secret)

    def _cabecalho(self, corpo: str) -> dict:
        """Monta o header Authorization exigido pela Shopee.

        Assinatura = SHA256(app_id + timestamp + payload + app_secret).
        """
        timestamp = int(time.time())
        base = f"{self.app_id}{timestamp}{corpo}{self.app_secret}"
        assinatura = hashlib.sha256(base.encode("utf-8")).hexdigest()
        return {
            "Content-Type": "application/json",
            "Authorization": (
                f"SHA256 Credential={self.app_id}, "
                f"Timestamp={timestamp}, Signature={assinatura}"
            ),
        }

    def buscar(self, termo: str, limite: int) -> list[Produto]:
        if not self.disponivel():
            return []

        corpo = json.dumps(
            {"query": self.QUERY, "variables": {"palavra": termo, "limite": limite}},
            separators=(",", ":"),
        )
        try:
            resp = requests.post(
                self.URL_API,
                data=corpo,
                headers=self._cabecalho(corpo),
                timeout=20,
            )
            resp.raise_for_status()
            dados = resp.json()
        except (requests.RequestException, ValueError) as erro:
            print(f"  [Shopee] falha ao buscar '{termo}': {erro}")
            return []

        if dados.get("errors"):
            print(f"  [Shopee] a API retornou erro: {dados['errors']}")
            return []

        nodes = (
            dados.get("data", {})
            .get("productOfferV2", {})
            .get("nodes", [])
        )

        produtos: list[Produto] = []
        for item in nodes:
            preco = float(item.get("priceMin") or item.get("priceMax") or 0)
            produtos.append(
                Produto(
                    fonte=self.nome,
                    id_externo=str(item.get("itemId", "")),
                    titulo=item.get("productName", ""),
                    preco=preco,
                    link=item.get("offerLink", ""),
                    foto=item.get("imageUrl", ""),
                    vendas=item.get("sales"),
                    avaliacao=(
                        float(item["ratingStar"]) if item.get("ratingStar") else None
                    ),
                )
            )
        return produtos
