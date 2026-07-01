# 🤖 Robô Minerador de Produtos — Shopee & Mercado Livre

Projeto **novo e independente**. Robô que garimpa (minera) ofertas da
**Shopee** e do **Mercado Livre** automaticamente, **todos os dias**,
guardando de cada produto o mais importante: **link** (já com a sua tag de
afiliado) e **foto**.

Este é o **módulo minerador** — a base de uma esteira de afiliados. Ele
alimenta com produtos frescos qualquer painel ou automação de postagem que
você conecte depois.

---

## O que ele faz

- 🔎 Busca produtos por **palavras-chave** que você define.
- 🏪 Duas fontes prontas: **Mercado Livre** (API pública) e **Shopee** (API
  oficial de Afiliados).
- 🔗 Guarda **link + foto + preço + desconto + nº de vendas + avaliação**.
- 🗓️ **Atualização diária automática** no horário que você escolher.
- 💾 Salva tudo num banco **SQLite** (histórico) e exporta um **JSON**.
- 🖥️ **Painel visual** (`painel.html`) que mostra os produtos com foto e
  botão "Ver produto".
- ➕ Fácil de **adicionar novas lojas** (Amazon, AliExpress, etc.).

---

## Estrutura de pastas

```
minerador/
├── main.py                 # ponto de entrada (rodar / agendar / exportar)
├── requirements.txt        # dependências
├── .env.example            # modelo de configuração (copie para .env)
├── painel.html             # painel visual dos produtos minerados
├── dados/                  # banco SQLite + JSON gerado (não vai pro Git)
└── minerador/              # o código do robô
    ├── config.py           # lê o .env e centraliza as configurações
    ├── models.py           # o que é um "Produto" (link, foto, preço...)
    ├── robo.py             # roda uma rodada de mineração
    ├── storage.py          # salva/atualiza no SQLite (sem duplicar)
    ├── exportador.py       # gera o dados/produtos.json
    └── fontes/             # uma classe por loja
        ├── base.py         # contrato que toda loja segue
        ├── mercadolivre.py # Mercado Livre (API pública)
        └── shopee.py       # Shopee (API oficial de Afiliados)
```

---

## Como usar

### 1. Instalar as dependências
```bash
cd minerador
pip install -r requirements.txt
```

### 2. Configurar
```bash
cp .env.example .env
```
Abra o `.env` e preencha:
- **PALAVRAS_CHAVE** — os produtos que quer garimpar (ex.: `fone,smartwatch`).
- **HORARIO_DIARIO** — hora da mineração diária (ex.: `08:00`).
- **ML_AFFILIATE_TAG** — sua tag de afiliado do Mercado Livre (opcional).
- **SHOPEE_APP_ID / SHOPEE_APP_SECRET** — credenciais do painel de
  Afiliados da Shopee. Sem elas, a Shopee é pulada e o robô roda só com o
  Mercado Livre.

> A Shopee usa a **Open API de Afiliados** (assinatura SHA256). Gere as
> credenciais em <https://affiliate.shopee.com.br> → Painel do
> desenvolvedor. Esse é o caminho oficial e estável (evita bloqueios de
> scraping).

### 3. Rodar
```bash
python main.py            # minera uma vez agora
python main.py --agendar  # fica rodando e minera todo dia no horário
python main.py --exportar # só regenera o JSON a partir do banco
```

### 4. Ver os produtos
Abra o `painel.html` no navegador (de preferência servindo a pasta:
`python -m http.server` e acesse `painel.html`). Ele lê o
`dados/produtos.json` e mostra tudo com foto, preço, desconto e link.

---

## Deixar rodando 24h num servidor

Para a "atualização diária" acontecer sem você ligar o PC, rode num
servidor. Duas opções comuns:

- **`python main.py --agendar`** dentro de um serviço (systemd, PM2,
  Docker) — o próprio robô cuida do horário.
- **Cron do sistema** chamando `python main.py` uma vez por dia (aí não
  precisa do `--agendar`):
  ```cron
  0 8 * * *  cd /caminho/minerador && /usr/bin/python3 main.py
  ```

---

## Como isso se encaixa numa esteira de afiliados

Este módulo é o **"robô minerador que garimpa ofertas 24h"**. O JSON que
ele gera (`dados/produtos.json`, com link de afiliado + foto de cada
produto) é a matéria-prima para os próximos módulos que você pode plugar:

| Módulo | O que faz | Status |
|--------|-----------|--------|
| **Minerador** | Garimpa ofertas da Shopee/ML com seu link e foto | ✅ este projeto |
| **Cupons** | Aplica cupons válidos no link antes de postar | 🔌 encaixa no `Produto.link` |
| **Postador** | Publica os produtos em grupos (WhatsApp/Telegram) | 🔌 consome o `produtos.json` |
| **Painel** | Tudo num lugar só, rodando no servidor | ✅ `painel.html` (base) |

Cada peça conversa pelo mesmo `produtos.json`, então dá para crescer aos
poucos sem refazer nada.

---

## Aviso legal

Use sempre as **APIs oficiais de afiliados** (como já está configurado).
Respeite os termos de uso e os limites de requisição de cada plataforma.
Fazer scraping direto dos sites pode violar os termos e levar a bloqueios.
