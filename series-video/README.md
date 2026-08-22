# Série de Vídeos IA

App pessoal que transforma um tema em um vídeo vertical curto: gera um roteiro de cenas,
gera uma imagem de IA para cada cena, aplica um efeito de movimento (zoom/pan) e junta
tudo com uma música que você mesma anexa. Roda 100% no navegador, sem servidor.

**Não faz:** narração/voz, geração de música, nem postagem automática no TikTok/YouTube.
O vídeo final é um arquivo `.webm` para você baixar e postar manualmente.

## Como usar

1. Abra `index.html` num navegador (de preferência **Chrome**, no computador ou Android).
2. Cole suas chaves de API na seção 1 e clique em "Salvar chaves".
3. Escreva o tema e escolha o estilo/número de cenas, clique em "Gerar roteiro".
4. Revise/edite os textos das cenas, escolha o provedor de imagem e clique em
   "Gerar todas as imagens".
5. Anexe um arquivo de música sua, ajuste a duração e clique em "Montar vídeo agora".
6. Baixe o `.webm` gerado.

## De onde vêm as chaves de API (e quanto custa)

As chaves de API são **diferentes** das assinaturas ChatGPT Plus ou Claude Pro — são
contas separadas, cobradas por uso (pré-pago):

- **OpenAI** (roteiro de cenas, e imagem alternativa): crie em
  https://platform.openai.com/api-keys — adicione um pequeno crédito (ex.: US$ 5).
- **Flux / Black Forest Labs** (geração de imagem principal, mais realista): crie em
  https://bfl.ai — também com crédito pré-pago.

Custo aproximado por vídeo (6 cenas): roteiro em texto custa centavos de dólar; cada
imagem custa entre US$ 0,04 e US$ 0,08 dependendo do provedor. Um vídeo de 6 cenas fica em
torno de **US$ 0,25 a US$ 0,50**. Confira os preços atuais nos sites de cada provedor —
os valores mudam com o tempo.

## Sobre a música

O app **não** integra com o Spotify nem baixa áudio de nenhum streaming — isso violaria
os termos de uso dessas plataformas e não é tecnicamente viável de forma legal. Você
precisa anexar um arquivo de áudio próprio (`.mp3`, `.wav` etc.) que já tenha os direitos
de usar: banco de músicas royalty-free, trilha licenciada ou gravação própria.

## Limitações conhecidas

- **Navegador:** o alvo é Chrome (desktop ou Android). Safari/iOS tem suporte fraco a
  gravação de vídeo `.webm` no navegador.
- **CORS da Flux:** se o provedor Flux não liberar CORS para o navegador, o app detecta
  isso automaticamente e avisa qual cena precisa ser regerada com o provedor OpenAI
  (que sempre funciona, pois retorna a imagem já embutida na resposta).
- **Chave exposta:** por ser um app 100% no navegador com sua própria chave, **não
  publique este app online com as chaves salvas** — ele é uma ferramenta pessoal, para
  uso só no seu aparelho.
- **Sem postagem automática:** publicar direto no TikTok/YouTube exigiria um servidor e
  aprovação de app nas plataformas — fora do escopo deste projeto pessoal.

## Estrutura de arquivos

Este app é totalmente independente dos outros projetos deste repositório
(`index.html`, `docs/`, `minerador/`, `novo/`) — nada ali foi alterado.
