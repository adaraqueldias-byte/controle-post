"""Modelo de dados de um produto minerado."""
from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass
class Produto:
    """Representa um produto encontrado em uma das fontes.

    Os dois campos mais importantes pedidos são o `link` e a `foto`.
    """

    fonte: str          # "Shopee" ou "Mercado Livre"
    id_externo: str     # id do produto na loja de origem (evita duplicados)
    titulo: str
    preco: float
    link: str           # link do produto (com tag de afiliado, se houver)
    foto: str           # URL da imagem do produto
    moeda: str = "BRL"
    preco_antigo: float | None = None
    vendas: int | None = None       # nº de vendas, quando a fonte informa
    avaliacao: float | None = None  # nota média (0 a 5), quando disponível
    coletado_em: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    @property
    def chave(self) -> str:
        """Chave única usada para não duplicar o mesmo produto."""
        return f"{self.fonte}:{self.id_externo}"

    @property
    def desconto(self) -> int | None:
        """Percentual de desconto, se houver preço antigo."""
        if self.preco_antigo and self.preco_antigo > self.preco:
            return round((1 - self.preco / self.preco_antigo) * 100)
        return None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["desconto"] = self.desconto
        return d
