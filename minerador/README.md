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
python main.py --postar   # posta no Telegram os produtos ainda não postados
python main.py --tudo     # minera E depois posta no Telegram
python main.py --agendar  # fica rodando e minera+posta todo dia no horário
python main.py --exportar # só regenera o JSON a partir do banco
```

### 4. Ver os produtos
Abra o `painel.html` no navegador (de preferência servindo a pasta:
`python -m http.server` e acesse `painel.html`). Ele lê o
`dados/produtos.json` e mostra tudo com foto, preço, desconto e link.

---

## Rodar 24h **sem servidor** (GitHub Actions — grátis) ⭐

Você **não precisa de servidor nem deixar o PC ligado**. O próprio GitHub
roda o robô todo dia de graça, usando o arquivo
[`.github/workflows/minerar.yml`](../.github/workflows/minerar.yml).

Como ligar (uma vez só):

1. **Suba o projeto para o GitHub** (este repositório já está lá).
2. No GitHub, vá em **Settings → Secrets and variables → Actions**:
   - Aba **Variables** → crie `PALAVRAS_CHAVE` (ex.: `fone,smartwatch,luminária`)
     e, se quiser, `LIMITE_POR_BUSCA` (ex.: `20`).
   - Aba **Secrets** → crie `SHOPEE_APP_ID`, `SHOPEE_APP_SECRET` e
     `ML_AFFILIATE_TAG` (as credenciais ficam ocultas e seguras).
3. Pronto. Todo dia às **08:00 (horário de Brasília)** o robô minera
   sozinho e **salva o `dados/produtos.json` de volta no repositório**.

> Quer testar na hora? Vá na aba **Actions → Minerar produtos (diário) →
> Run workflow**. Para mudar o horário, edite a linha `cron` do workflow
> (o valor é sempre em **UTC**; 08:00 de Brasília = `0 11 * * *`).

### Alternativa: rodar no seu próprio computador/servidor

Se um dia tiver uma máquina ligada, também dá:

- **`python main.py --agendar`** — o próprio robô cuida do horário; ou
- **Cron do sistema** chamando `python main.py` uma vez por dia.

---

## 📣 Postar automático no Telegram

O módulo Postador (`minerador/telegram.py`) pega os produtos minerados e
publica no seu canal/grupo do Telegram: **foto + título + preço + desconto
+ botão "🛒 Comprar"** com o seu link. Ele marca no banco o que já postou,
então **nunca repete** o mesmo produto.

### Preparar (uma vez)

1. No Telegram, fale com **@BotFather** → `/newbot` → guarde o **token**.
2. Crie seu **canal/grupo** e adicione o bot como **administrador**.
3. Pegue o **chat_id** do canal (ex.: use o **@userinfobot** ou publique
   algo e leia em `https://api.telegram.org/bot<TOKEN>/getUpdates`).
4. Preencha no `.env` (ou nos **Secrets do GitHub**):
   - `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`
   - `MAX_POSTS_POR_RODADA` (quantos posts por rodada, padrão 5)

Pronto. Rodando pelo GitHub Actions, todo dia o robô **minera e posta
sozinho** — de graça, sem servidor. (WhatsApp não entra aqui: exige
conexão sempre ligada e tem alto risco de banimento; o Telegram é o
caminho seguro e automatizável.)

## Como isso se encaixa numa esteira de afiliados

Este módulo é o **"robô minerador que garimpa ofertas 24h"**. O JSON que
ele gera (`dados/produtos.json`, com link de afiliado + foto de cada
produto) é a matéria-prima para os próximos módulos que você pode plugar:

| Módulo | O que faz | Status |
|--------|-----------|--------|
| **Minerador** | Garimpa ofertas da Shopee/ML com seu link e foto | ✅ este projeto |
| **Postador** | Publica os produtos no Telegram (foto + link + botão) | ✅ `telegram.py` |
| **Cupons** | Aplica cupons válidos no link antes de postar | 🔌 encaixa no `Produto.link` |
| **Painel** | Tudo num lugar só, rodando no servidor | ✅ `painel.html` (base) |

Cada peça conversa pelo mesmo `produtos.json`, então dá para crescer aos
poucos sem refazer nada.

---

## Aviso legal

Use sempre as **APIs oficiais de afiliados** (como já está configurado).
Respeite os termos de uso e os limites de requisição de cada plataforma.
Fazer scraping direto dos sites pode violar os termos e levar a bloqueios.
