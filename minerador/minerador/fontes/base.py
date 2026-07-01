"""Contrato base que toda fonte de mineração precisa seguir."""
from abc import ABC, abstractmethod

from ..models import Produto


class FonteBase(ABC):
    """Classe base para uma loja mineradora.

    Para adicionar uma loja nova (ex.: Amazon, AliExpress), basta criar
    uma classe que herde desta e implemente `buscar`.
    """

    nome: str = "Fonte genérica"

    @abstractmethod
    def buscar(self, termo: str, limite: int) -> list[Produto]:
        """Busca produtos por um termo e devolve uma lista de Produto.

        Deve tratar os próprios erros de rede e devolver [] em caso de
        falha, para que uma fonte quebrada não derrube a rodada inteira.
        """
        raise NotImplementedError

    def disponivel(self) -> bool:
        """Indica se a fonte está pronta para uso (ex.: tem credenciais)."""
        return True
