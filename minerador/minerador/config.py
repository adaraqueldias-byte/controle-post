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

# --- Parâmetros da mineração ---------------------------------------
PALAVRAS_CHAVE = [
    termo.strip()
    for termo in os.getenv("PALAVRAS_CHAVE", "").split(",")
    if termo.strip()
]

LIMITE_POR_BUSCA = int(os.getenv("LIMITE_POR_BUSCA", "20"))
HORARIO_DIARIO = os.getenv("HORARIO_DIARIO", "08:00").strip()

# --- Caminhos ------------------------------------------------------
PASTA_DADOS = os.path.join(RAIZ, "dados")
CAMINHO_BANCO = os.path.join(PASTA_DADOS, "produtos.db")
CAMINHO_JSON = os.path.join(PASTA_DADOS, "produtos.json")

os.makedirs(PASTA_DADOS, exist_ok=True)
