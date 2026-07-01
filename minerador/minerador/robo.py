"""Cérebro do robô: roda uma rodada de mineração.

Percorre todas as fontes disponíveis, busca cada palavra-chave, salva no
banco e exporta o JSON. É isto que o agendador chama uma vez por dia.
"""
from datetime import datetime

from .fontes import FONTES
from .storage import Banco
from .exportador import exportar_json
from . import config


def minerar() -> dict:
    inicio = datetime.now()
    print(f"\n=== Mineração iniciada em {inicio:%d/%m/%Y %H:%M:%S} ===")

    if not config.PALAVRAS_CHAVE:
        print("Nenhuma palavra-chave configurada (veja PALAVRAS_CHAVE no .env).")
        return {"coletados": 0}

    banco = Banco()
    total_coletado = novos = atualizados = 0

    for classe_fonte in FONTES:
        fonte = classe_fonte()
        if not fonte.disponivel():
            print(f"- {fonte.nome}: sem credenciais, pulando.")
            continue

        print(f"- {fonte.nome}:")
        for termo in config.PALAVRAS_CHAVE:
            produtos = fonte.buscar(termo, config.LIMITE_POR_BUSCA)
            n, a = banco.salvar_varios(produtos)
            total_coletado += len(produtos)
            novos += n
            atualizados += a
            print(f"    '{termo}': {len(produtos)} produtos ({n} novos)")

    caminho_json = exportar_json()
    duracao = (datetime.now() - inicio).total_seconds()

    print(
        f"=== Fim: {total_coletado} coletados | {novos} novos | "
        f"{atualizados} atualizados | {duracao:.1f}s ==="
    )
    print(f"JSON exportado em: {caminho_json}")

    return {
        "coletados": total_coletado,
        "novos": novos,
        "atualizados": atualizados,
        "json": caminho_json,
    }
