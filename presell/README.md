# Criador de Presell

App pessoal que monta **páginas de presell** (pré-venda) para marketing de afiliados e
as publica num **link grátis**, sem você precisar contratar domínio nem hospedagem.
Roda 100% no navegador, sem servidor.

É a mesma ideia de apps pagos tipo o "Presell Pro" — a diferença é que aqui as páginas
ficam hospedadas de graça no **GitHub Pages** deste próprio repositório.

> Este app é totalmente **independente** dos outros projetos do repositório
> (`index.html`, `docs/`, `minerador/`, `novo/`, `series-video/`). Nada ali é alterado
> nem compartilhado com este app.

## Como usar

1. Abra `index.html` no navegador (de preferência **Chrome**, no computador ou Android).
2. **Seção 1 — Dados da oferta:** preencha o produto, a chamada, os benefícios, o
   depoimento, o preço e principalmente o **link de afiliado** (o botão leva pra lá).
   A imagem, se você anexar, fica embutida na página — não precisa hospedar em lugar
   nenhum.
3. **Seção 2 — Modelo:** escolha o estilo do texto (notícia, história, review ou alerta).
   O app escreve o texto sozinho, de graça.
4. **Seção 3 — IA (opcional):** se quiser um texto mais elaborado, cole uma chave da
   OpenAI e clique em "Reescrever com IA". Sem chave, o app funciona normalmente.
5. **Seção 4 — Prévia:** clique em "Gerar / atualizar prévia" pra ver a página pronta.
6. **Seção 5 — Publicar:**
   - **Publicar no meu link grátis:** precisa configurar uma vez o **token do GitHub**
     (botão "⚙️ Configurar token"). Ao publicar, o app cria a página em
     `docs/presell/paginas/<endereço>.html` e te dá o link público. O link fica no ar
     em 1–2 minutos (tempo do GitHub Pages atualizar).
   - **Baixar HTML:** alternativa sem token — baixa o arquivo `.html` pronto pra você
     hospedar onde quiser (ou mandar por onde preferir).
7. **Seção 6 — Minhas páginas:** lista tudo que você já publicou, com abrir, copiar link
   e excluir.

## O link grátis (como funciona)

A pasta `docs/` deste repositório é publicada automaticamente pelo **GitHub Pages**.
Quando você publica uma presell, o app grava o arquivo em `docs/presell/paginas/` e ele
passa a ficar acessível em:

```
https://adaraqueldias-byte.github.io/controle-post/presell/paginas/SEU-ENDERECO.html
```

Sem custo de hospedagem e sem domínio próprio. Se um dia você quiser um domínio bonito,
dá pra apontar um domínio pro GitHub Pages — mas não é obrigatório.

## O token do GitHub (uma vez só)

Para publicar, o app precisa de um **token pessoal** com permissão de escrita:

1. No GitHub: **Settings → Developer settings → Personal access tokens →
   Fine-grained tokens → Generate new token**.
2. Dê acesso ao repositório `controle-post` com permissão **Contents: Read and write**.
3. Copie o token (começa com `github_pat_`) e cole no app pelo botão "⚙️ Configurar token".

O token fica guardado **só no seu aparelho** (localStorage). É o mesmo esquema que o app
principal já usa pra "Salvar na nuvem".

## Sobre a chave da OpenAI (opcional)

A chave de API é diferente da assinatura do ChatGPT Plus — é uma conta separada, cobrada
por uso (pré-pago). Crie em https://platform.openai.com/api-keys. Cada página reescrita
custa centavos de dólar. **Sem a chave, o app funciona 100%** usando os modelos de texto
embutidos.

## Limitações conhecidas

- **Publicar** exige o token do GitHub. Sem ele, use "Baixar HTML".
- O link novo pode levar 1–2 minutos pra ficar no ar (build do GitHub Pages).
- As páginas geradas são estáticas: o botão leva ao seu link de afiliado, mas o app não
  faz rastreamento de cliques nem integra com pixel/analytics (dá pra colar o código do
  pixel manualmente no HTML depois, se quiser).
- Use com responsabilidade: escreva promessas honestas e respeite as regras da
  plataforma de afiliados e da rede de anúncios.
