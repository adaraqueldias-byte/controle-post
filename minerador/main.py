"""Ponto de entrada do robô minerador.

Uso:
    python main.py            -> roda uma mineração agora e sai
    python main.py --agendar  -> fica rodando e minera todo dia no horário
    python main.py --exportar -> só regenera o JSON a partir do banco
"""
import sys
import time

import schedule

from minerador.robo import minerar
from minerador.exportador import exportar_json
from minerador import config


def modo_agendado() -> None:
    print(f"Robô agendado para minerar todo dia às {config.HORARIO_DIARIO}.")
    print("Rodando uma primeira vez agora...")
    minerar()

    schedule.every().day.at(config.HORARIO_DIARIO).do(minerar)
    print("Aguardando o próximo horário. (Ctrl+C para sair.)")
    while True:
        schedule.run_pending()
        time.sleep(30)


def main() -> None:
    args = sys.argv[1:]

    if "--agendar" in args:
        modo_agendado()
    elif "--exportar" in args:
        caminho = exportar_json()
        print(f"JSON exportado em: {caminho}")
    else:
        minerar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")
