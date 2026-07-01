"""Módulo Postador: publica os produtos minerados no Telegram.

Usa a Bot API oficial do Telegram (sendPhoto). Cada produto vira um post
com foto, título, preço, desconto e um botão "🛒 Comprar" que leva para o
seu link de afiliado. Marca no banco o que já foi postado, então nunca
repete o mesmo produto.

Como preparar (uma vez):
  1. No Telegram, fale com @BotFather e crie um bot -> ele te dá o TOKEN.
  2. Crie seu canal/grupo e adicione o bot como administrador.
  3. Descubra o chat_id do canal (ex.: use @userinfobot ou a getUpdates).
  4. Preencha TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no .env (ou nos
     Secrets do GitHub).
"""
import time

import requests

from .storage import Banco
from . import config

API = "https://api.telegram.org/bot{token}/{metodo}"
LIMITE_LEGENDA = 1024  # limite de caracteres da legenda no Telegram


class TelegramPostador:
    def __init__(self):
        self.token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.banco = Banco()

    def disponivel(self) -> bool:
        return bool(self.token and self.chat_id)

    # ---- montagem da mensagem -------------------------------------
    @staticmethod
    def _moeda(valor) -> str:
        try:
            return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (TypeError, ValueError):
            return "R$ --"

    def _legenda(self, p: dict) -> str:
        linhas = [f"🔥 <b>{self._escapar(p.get('titulo', ''))}</b>", ""]

        preco = f"💰 <b>{self._moeda(p.get('preco'))}</b>"
        if p.get("preco_antigo"):
            preco += f"  <s>{self._moeda(p['preco_antigo'])}</s>"
        linhas.append(preco)

        desconto = self._desconto(p)
        if desconto:
            linhas.append(f"🏷️ <b>{desconto}% OFF</b>")

        extras = []
        if p.get("avaliacao"):
            extras.append(f"⭐ {p['avaliacao']}")
        if p.get("vendas"):
            extras.append(f"🛍️ {p['vendas']} vendas")
        if extras:
            linhas.append(" · ".join(extras))

        linhas.append(f"🏪 {p.get('fonte', '')}")
        legenda = "\n".join(linhas)
        return legenda[: LIMITE_LEGENDA - 1]

    @staticmethod
    def _desconto(p: dict) -> int | None:
        antigo, atual = p.get("preco_antigo"), p.get("preco")
        if antigo and atual and antigo > atual:
            return round((1 - atual / antigo) * 100)
        return None

    @staticmethod
    def _escapar(texto: str) -> str:
        # Escapa os caracteres reservados do parse_mode HTML do Telegram.
        return (
            texto.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    def _botao(self, link: str) -> dict:
        return {"inline_keyboard": [[{"text": "🛒 Comprar agora", "url": link}]]}

    # ---- envio ----------------------------------------------------
    def _enviar(self, p: dict) -> bool:
        """Tenta postar com foto; se a foto falhar, cai para texto."""
        legenda = self._legenda(p)
        botao = self._botao(p.get("link", ""))

        try:
            resp = requests.post(
                API.format(token=self.token, metodo="sendPhoto"),
                json={
                    "chat_id": self.chat_id,
                    "photo": p.get("foto"),
                    "caption": legenda,
                    "parse_mode": "HTML",
                    "reply_markup": botao,
                },
                timeout=20,
            )
            if resp.ok and resp.json().get("ok"):
                return True

            # Foto recusada (URL inválida etc.) -> tenta como mensagem de texto.
            resp = requests.post(
                API.format(token=self.token, metodo="sendMessage"),
                json={
                    "chat_id": self.chat_id,
                    "text": f"{legenda}\n\n👉 {p.get('link', '')}",
                    "parse_mode": "HTML",
                    "reply_markup": botao,
                    "disable_web_page_preview": False,
                },
                timeout=20,
            )
            return resp.ok and resp.json().get("ok", False)
        except (requests.RequestException, ValueError) as erro:
            print(f"  [Telegram] falha ao postar '{p.get('titulo', '')}': {erro}")
            return False

    def postar_novos(self, limite: int | None = None) -> dict:
        if not self.disponivel():
            print("Telegram sem credenciais (TELEGRAM_BOT_TOKEN / CHAT_ID). Pulando.")
            return {"postados": 0}

        limite = limite or config.MAX_POSTS_POR_RODADA
        produtos = self.banco.listar_nao_postados(limite)

        if not produtos:
            print("Nenhum produto novo para postar.")
            return {"postados": 0}

        print(f"Postando {len(produtos)} produto(s) no Telegram...")
        postados = 0
        for i, p in enumerate(produtos):
            if self._enviar(p):
                self.banco.marcar_postado(p["chave"])
                postados += 1
                print(f"  ✔ {p.get('titulo', '')[:50]}")
            else:
                print(f"  ✘ falhou: {p.get('titulo', '')[:50]}")

            # Pausa entre posts para não bater no limite do Telegram.
            if i < len(produtos) - 1:
                time.sleep(config.INTERVALO_POSTS)

        print(f"Concluído: {postados} postado(s).")
        return {"postados": postados}
