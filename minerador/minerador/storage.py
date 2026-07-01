"""Armazenamento dos produtos em um banco SQLite.

Guarda o histórico de tudo que foi minerado e evita duplicados usando a
chave "fonte:id_externo". A cada rodada, produtos já existentes têm o
preço atualizado; produtos novos são inseridos.
"""
import sqlite3
from contextlib import closing

from .models import Produto
from . import config


class Banco:
    def __init__(self, caminho: str = config.CAMINHO_BANCO):
        self.caminho = caminho
        self._criar_tabela()

    def _conectar(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.caminho)
        con.row_factory = sqlite3.Row
        return con

    def _criar_tabela(self) -> None:
        with closing(self._conectar()) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS produtos (
                    chave        TEXT PRIMARY KEY,
                    fonte        TEXT NOT NULL,
                    id_externo   TEXT NOT NULL,
                    titulo       TEXT,
                    preco        REAL,
                    preco_antigo REAL,
                    moeda        TEXT,
                    link         TEXT,
                    foto         TEXT,
                    vendas       INTEGER,
                    avaliacao    REAL,
                    coletado_em  TEXT,
                    atualizado_em TEXT
                )
                """
            )
            con.commit()

    def salvar_varios(self, produtos: list[Produto]) -> tuple[int, int]:
        """Insere novos e atualiza existentes.

        Retorna (novos, atualizados).
        """
        novos = atualizados = 0
        with closing(self._conectar()) as con:
            for p in produtos:
                existe = con.execute(
                    "SELECT 1 FROM produtos WHERE chave = ?", (p.chave,)
                ).fetchone()
                con.execute(
                    """
                    INSERT INTO produtos
                        (chave, fonte, id_externo, titulo, preco, preco_antigo,
                         moeda, link, foto, vendas, avaliacao, coletado_em,
                         atualizado_em)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(chave) DO UPDATE SET
                        titulo=excluded.titulo,
                        preco=excluded.preco,
                        preco_antigo=excluded.preco_antigo,
                        link=excluded.link,
                        foto=excluded.foto,
                        vendas=excluded.vendas,
                        avaliacao=excluded.avaliacao,
                        atualizado_em=excluded.atualizado_em
                    """,
                    (
                        p.chave, p.fonte, p.id_externo, p.titulo, p.preco,
                        p.preco_antigo, p.moeda, p.link, p.foto, p.vendas,
                        p.avaliacao, p.coletado_em, p.coletado_em,
                    ),
                )
                if existe:
                    atualizados += 1
                else:
                    novos += 1
            con.commit()
        return novos, atualizados

    def listar(self, ordenar_por: str = "atualizado_em") -> list[dict]:
        colunas_ok = {"atualizado_em", "preco", "vendas", "avaliacao"}
        coluna = ordenar_por if ordenar_por in colunas_ok else "atualizado_em"
        with closing(self._conectar()) as con:
            linhas = con.execute(
                f"SELECT * FROM produtos ORDER BY {coluna} DESC"
            ).fetchall()
        return [dict(l) for l in linhas]
