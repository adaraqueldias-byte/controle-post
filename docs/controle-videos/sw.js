// Service Worker — busca sempre a versão nova quando tem internet
const CACHE = 'controle-videos-v2';
const ARQUIVOS = ['./', './index.html', './manifest.json'];

// Não chama self.skipWaiting() aqui: numa ATUALIZAÇÃO (já existe um SW
// controlando a página), isso faria a página trocar de versão na hora,
// sem dar tempo do aviso "Nova versão disponível" aparecer na tela.
// A troca só acontece quando o index.html manda a mensagem 'skipWaiting'
// (depois de mostrar o aviso). Numa instalação NOVA (primeira vez do app
// no aparelho) isso não atrasa nada: sem SW anterior controlando a
// página, o navegador ativa este sozinho, sem precisar de skipWaiting.
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ARQUIVOS)));
});

self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

// Rede primeiro: se tem internet, sempre pega a versão atualizada.
// Sem internet, usa o que estiver guardado (funciona offline).
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request)
      .then(resp => {
        const copia = resp.clone();
        caches.open(CACHE).then(c => c.put(e.request, copia)).catch(()=>{});
        return resp;
      })
      .catch(() => caches.match(e.request))
  );
});
