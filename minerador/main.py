"""Ponto de entrada do robô minerador.

Uso:
    python main.py            -> minera agora e sai
    python main.py --postar   -> posta no Telegram os produtos ainda não postados
    python main.py --tudo     -> minera E depois posta no Telegram
    python main.py --agendar  -> fica rodando e minera+posta todo dia no horário
    python main.py --exportar -> só regenera o JSON a partir do banco
"""
import sys
import time

import schedule

from minerador.robo import minerar
from minerador.exportador import exportar_json
from minerador.telegram import TelegramPostador
from minerador import config


def postar() -> None:
    TelegramPostador().postar_novos()


def minerar_e_postar() -> None:
    minerar()
    postar()


def modo_agendado() -> None:
    print(f"Robô agendado para rodar todo dia às {config.HORARIO_DIARIO}.")
    print("Rodando uma primeira vez agora...")
    minerar_e_postar()

    schedule.every().day.at(config.HORARIO_DIARIO).do(minerar_e_postar)
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
    elif "--postar" in args:
        postar()
    elif "--tudo" in args:
        minerar_e_postar()
    else:
        minerar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")
