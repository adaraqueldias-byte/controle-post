"""Exporta os produtos do banco para um arquivo JSON.

Esse JSON é o que uma interface (site, app ou planilha) consome para
mostrar os produtos com foto e link. Fica em dados/produtos.json.
"""
import json
from datetime import datetime

from .storage import Banco
from . import config


def exportar_json(caminho: str = config.CAMINHO_JSON) -> str:
    banco = Banco()
    produtos = banco.listar(ordenar_por="atualizado_em")

    saida = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "total": len(produtos),
        "produtos": produtos,
    }
    with open(caminho, "w", encoding="utf-8") as arq:
        json.dump(saida, arq, ensure_ascii=False, indent=2)

    return caminho
