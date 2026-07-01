"""Configurações centrais do robô minerador.

Lê tudo do arquivo .env (via python-dotenv) e expõe constantes já
prontas para o resto do projeto usar.
"""
import os
from dotenv import load_dotenv

# Raiz do projeto = pasta acima deste pacote (onde ficam .env e dados/).
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(RAIZ, ".env"))

# --- Credenciais ---------------------------------------------------
ML_AFFILIATE_TAG = os.getenv("ML_AFFILIATE_TAG", "").strip()
SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID", "").strip()
SHOPEE_APP_SECRET = os.getenv("SHOPEE_APP_SECRET", "").strip()

# --- Telegram (módulo Postador) ------------------------------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
# Quantos produtos postar por rodada (evita floodar o canal).
MAX_POSTS_POR_RODADA = int(os.getenv("MAX_POSTS_POR_RODADA") or 5)
# Segundos de intervalo entre um post e outro (respeita limites do Telegram).
INTERVALO_POSTS = int(os.getenv("INTERVALO_POSTS") or 3)

# --- Parâmetros da mineração ---------------------------------------
# Se nada for configurado, usa esta lista padrão (facilita o 1º uso).
PALAVRAS_PADRAO = "fone de ouvido,smartwatch,luminária led,organizador de cozinha"

PALAVRAS_CHAVE = [
    termo.strip()
    for termo in (os.getenv("PALAVRAS_CHAVE") or PALAVRAS_PADRAO).split(",")
    if termo.strip()
]

# `or` protege contra variável definida como string vazia (comum no CI).
LIMITE_POR_BUSCA = int(os.getenv("LIMITE_POR_BUSCA") or 20)
HORARIO_DIARIO = (os.getenv("HORARIO_DIARIO") or "08:00").strip()

# --- Caminhos ------------------------------------------------------
PASTA_DADOS = os.path.join(RAIZ, "dados")
CAMINHO_BANCO = os.path.join(PASTA_DADOS, "produtos.db")
CAMINHO_JSON = os.path.join(PASTA_DADOS, "produtos.json")

os.makedirs(PASTA_DADOS, exist_ok=True)
