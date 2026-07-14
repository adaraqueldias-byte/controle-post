# CLAUDE.md

Guidance for AI assistants (Claude Code and others) working in this repository.

## What this repo is

`controle-post` is a personal affiliate-marketing toolkit for a Brazilian
affiliate seller ("afiliada"). It combines two independent-but-connected
pieces:

1. **Controle de Post** — a single-file PWA (`index.html`) that helps the user
   track, day by day, which affiliate products they have posted to which
   channels (WhatsApp, Telegram, Instagram, Facebook, YouTube, TikTok, plus
   store showcases like Shopee Vitrine / Meus Links ML). Runs entirely in the
   browser, stores data in `localStorage`, and can back up to GitHub.
2. **Minerador** (`minerador/`) — a Python robot that mines (garimpa) daily
   offers from **Shopee** and **Mercado Livre** affiliate APIs, stores them in
   SQLite, exports a JSON feed, and auto-posts to Telegram. It runs for free on
   a daily GitHub Actions schedule (no server needed).

The language throughout the code, comments, commit messages, and UI is
**Brazilian Portuguese**. Keep it that way — match the existing language and
tone in any new code, comments, or user-facing strings.

## Repository layout

```
.
├── index.html            # "Controle de Post" PWA — the main app (single file, ~49KB)
├── manifest.json         # PWA manifest for the main app
├── sw.js                 # Service worker for the main app (network-first)
├── icon-192.png          # PWA icons (main app)
├── icon-512.png
├── novo/
│   └── index.html        # "reset" page: clears SW + caches, then redirects to ../ (recovery helper)
├── dados-nuvem/
│   └── backup.json       # Cloud backup of the main app's localStorage (written via GitHub API)
├── docs/                 # "Garimpo" PWA — published via GitHub Pages
│   ├── index.html        #   storefront that reads produtos.json and shows offers
│   ├── produtos.json     #   product feed written by the minerador (committed by CI)
│   ├── manifest.json / sw.js / icon-*.png
├── minerador/            # Python mining robot (see minerador/README.md — very detailed)
│   ├── main.py           #   entry point / CLI
│   ├── requirements.txt  #   requests, schedule, python-dotenv
│   ├── .env.example      #   config template (copy to .env)
│   ├── dados/            #   SQLite DB (produtos.db) — history + "already posted" flags
│   └── minerador/        #   the package
│       ├── config.py     #     loads .env, centralizes all settings & paths
│       ├── models.py     #     Produto dataclass
│       ├── robo.py       #     runs one mining round
│       ├── storage.py    #     SQLite persistence (dedupe by "fonte:id_externo")
│       ├── exportador.py #     writes docs/produtos.json from the DB
│       ├── telegram.py   #     the "Postador": posts products to Telegram
│       └── fontes/       #     one class per store
│           ├── base.py         #   FonteBase abstract contract
│           ├── mercadolivre.py #   Mercado Livre (public API, no creds)
│           └── shopee.py       #   Shopee Affiliate Open API (SHA256-signed GraphQL)
└── .github/workflows/
    └── minerar.yml       # daily cron that mines, posts to Telegram, commits produtos.json + db
```

## Two apps, two audiences — don't confuse them

- **Root `index.html` = "Controle de Post"** (dark purple theme, `#7c3aed`).
  A private posting-tracker for the user. No product data comes from the
  minerador — the user enters products manually and checks off channels.
- **`docs/index.html` = "Garimpo"** (light theme). A public storefront that
  `fetch`es `produtos.json` and renders offers with photo/price/discount/share.
  This is the front-end for the minerador's output.

These share only a repo. Changing one does not affect the other.

## The minerador (Python) — how it works

- **Entry point** is `minerador/main.py`. Run commands from inside `minerador/`:
  ```bash
  cd minerador
  pip install -r requirements.txt
  cp .env.example .env      # then fill in credentials
  python main.py            # mine once, now
  python main.py --postar   # post un-posted products to Telegram
  python main.py --tudo     # mine, then post (this is what CI runs)
  python main.py --agendar  # long-running: mine+post every day at HORARIO_DIARIO
  python main.py --exportar # only regenerate docs/produtos.json from the DB
  ```
- **Config** lives in `minerador/minerador/config.py` and is read from `.env`
  (via `python-dotenv`). All env vars use the `X or default` idiom to survive
  empty strings (common in CI). Key vars: `PALAVRAS_CHAVE`, `LIMITE_POR_BUSCA`,
  `HORARIO_DIARIO`, `ML_AFFILIATE_TAG`, `SHOPEE_APP_ID`/`SHOPEE_APP_SECRET`,
  `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`, `MAX_POSTS_POR_RODADA`,
  `INTERVALO_POSTS`.
- **Paths** are derived in `config.py`: the SQLite DB is `minerador/dados/produtos.db`;
  the JSON feed is written to `docs/produtos.json` at the **repo root** (so
  GitHub Pages serves it). Don't hardcode these elsewhere — import from `config`.
- **Data model**: `models.Produto` (dataclass). Its `chave` property
  (`"{fonte}:{id_externo}"`) is the dedupe key; `desconto` is computed from
  `preco`/`preco_antigo`. Store fields center on `link` (with affiliate tag) and
  `foto` — those are the two most important fields.
- **Storage** (`storage.Banco`): SQLite with `INSERT ... ON CONFLICT(chave) DO
  UPDATE`. It self-migrates the `postado_em` column for old DBs. `postado_em`
  tracks what has already gone to Telegram so nothing is reposted.

### Adding a new store (fonte)

This is the main intended extension point. To add Amazon, AliExpress, etc.:

1. Create `minerador/minerador/fontes/<loja>.py` with a class that subclasses
   `FonteBase` (see `fontes/base.py`).
2. Implement `buscar(self, termo, limite) -> list[Produto]`. It **must catch its
   own network errors and return `[]` on failure** so one broken store never
   kills the whole round.
3. Override `disponivel(self)` to return `False` when credentials are missing
   (see `shopee.py`) — the round will skip it cleanly.
4. Register the class in `fontes/__init__.py`'s `FONTES` list.

No other file needs to change — `robo.minerar()` iterates `FONTES` generically.

## GitHub Actions — the "free server"

`.github/workflows/minerar.yml` runs daily (`cron: "0 11 * * *"` = 08:00
Brasília / UTC-3) and on manual dispatch. It:
1. Installs deps and runs `python main.py --tudo` from `minerador/`.
2. Commits `docs/produtos.json` and `minerador/dados/produtos.db` back to the
   repo with message `"Atualiza produtos minerados [skip ci]"`.

Configure secrets/vars under **Settings → Secrets and variables → Actions**:
- **Variables** (visible): `PALAVRAS_CHAVE`, `LIMITE_POR_BUSCA`, `MAX_POSTS_POR_RODADA`.
- **Secrets** (hidden): `ML_AFFILIATE_TAG`, `SHOPEE_APP_ID`, `SHOPEE_APP_SECRET`,
  `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

The `[skip ci]` tag in the auto-commit prevents infinite CI loops. Note the bulk
of the git history is these automated `"Atualiza produtos minerados [skip ci]"`
commits — that is normal.

## The PWAs (front-end)

- Both `index.html` files are **self-contained**: inline `<style>` and inline
  `<script>`, vanilla JS, no build step, no frameworks, no dependencies.
- **Main app state** is in `localStorage`, keyed `post_YYYY-MM-DD` (an array of
  products per day) plus `relatorios_salvos`, `meta_produtos_loja`, and
  `gh_token`. Photos are base64 data URIs, compressed on upload to fit the
  `localStorage` quota; `liberarEspacoAutomatico` evicts old days when full.
- **Cloud backup**: the main app can push all `post_*` keys + saved reports to
  `dados-nuvem/backup.json` via the GitHub Contents API, using a user-supplied
  `github_pat_` token stored only in `localStorage` (`salvarNaNuvem` /
  `carregarDaNuvem`). There is no server — the browser talks to GitHub directly.
- **Service workers are network-first**: `fetch` from network, fall back to
  cache offline, and cache the fresh copy. When you change `index.html` or
  `docs/index.html`, **bump the `CACHE` constant in the matching `sw.js`**
  (e.g. `controle-post-v17` → `v18`) so clients pick up the new version. The
  main app also auto-reloads on a new SW via `skipWaiting` + `controllerchange`.
- `novo/index.html` is a recovery page: it unregisters SWs, deletes all caches,
  then redirects to `../` (localStorage/products are preserved). Point users
  here if they're stuck on a stale cached version.

### Working conventions for the PWAs

- Keep everything in the single HTML file — do not split into modules or add a
  bundler. That single-file simplicity is intentional (the user deploys by
  committing the file).
- Preserve the Portuguese UI text and the existing visual theme per app.
- Test locally with `python -m http.server` inside the relevant folder and open
  in a browser (there are no automated tests).

## Deployment

- **Garimpo storefront**: GitHub Pages, **Settings → Pages → Deploy from a
  branch → `/docs`**. Publishes at `https://<user>.github.io/controle-post/`.
- **Controle de Post main app**: the user runs it as an installed PWA from
  wherever it is hosted; committing `index.html` updates it.

## Conventions & gotchas

- **Language**: Portuguese everywhere (identifiers, comments, commits, UI).
  Follow suit.
- **No test suite, no linter config** — verify by running the code / opening the
  app. For Python changes, at minimum run the relevant `python main.py ...`
  command and check output.
- **Secrets never in the repo**: `.env` is git-ignored; real credentials live in
  GitHub Secrets or the user's device. `.env.example` is the only template.
  Never commit tokens.
- **Don't hand-edit `docs/produtos.json` or `minerador/dados/produtos.db`** —
  they are generated/committed by the workflow.
- When changing a PWA, remember the service-worker cache bump (above) or users
  will keep seeing the old version.
- The minerador README (`minerador/README.md`) is thorough and user-facing;
  keep it in sync when you change how the robot is configured or run.

## Git / branch workflow

Feature work happens on a dedicated branch (currently
`claude/claude-md-docs-nsd0up`); `main` is the default. Commit with clear
Portuguese messages, push with `git push -u origin <branch>`, and only open a
PR when explicitly asked.
