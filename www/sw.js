// Service worker de Medianeras: hace que la app funcione sin conexión.
// IMPORTANTE: cuando cambies archivos de la app (HTML, CSS, JS), subí VERSION
// para que los teléfonos descarguen la versión nueva.

const VERSION = 'v22';
const CACHE_APP = `medianeras-app-${VERSION}`;
const CACHE_DATOS = 'medianeras-datos';
const CACHE_FOTOS = 'medianeras-fotos';
const CACHE_MAPA = 'medianeras-mapa';
const MAX_MOSAICOS = 500;

const APP = [
  './',
  'index.html',
  'manifest.webmanifest',
  'css/estilos.css',
  'js/app.js',
  'js/datos.js',
  'js/filtros.js',
  'js/ui.js',
  'js/exportar.js',
  'js/grafica.js',
  'js/tema.js',
  'js/filas.js',
  'js/lib/zip.js',
  'js/plataforma/almacen.js',
  'js/plataforma/ubicacion.js',
  'js/plataforma/fotos.js',
  'js/plataforma/compartir.js',
  'js/plataforma/preferencias.js',
  'js/vistas/inicio.js',
  'js/vistas/obras.js',
  'js/vistas/perfil.js',
  'js/vistas/mapa.js',
  'js/vistas/obra.js',
  'js/vistas/diario.js',
  'js/vistas/listas.js',
  'js/vistas/nueva-visita.js',
  'fuentes/archivo-latin.woff2',
  'fuentes/plex-mono-400-latin.woff2',
  'fuentes/plex-mono-500-latin.woff2',
  'fuentes/caslon-400-latin.woff2',
  'fuentes/caslon-400i-latin.woff2',
  'vendor/leaflet/leaflet.js',
  'vendor/leaflet/leaflet.css',
  'vendor/leaflet/images/layers.png',
  'vendor/leaflet/images/layers-2x.png',
  'iconos/icono.svg',
  'iconos/icono-192.png',
  'iconos/apple-touch-icon.png',
];

self.addEventListener('install', (evento) => {
  evento.waitUntil(
    caches.open(CACHE_APP)
      .then((cache) => cache.addAll(APP.map((ruta) => new Request(ruta, { cache: 'reload' }))))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener('activate', (evento) => {
  evento.waitUntil(
    caches.keys()
      .then((nombres) => Promise.all(nombres
        .filter((n) => n.startsWith('medianeras-app-') && n !== CACHE_APP)
        .map((n) => caches.delete(n))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (evento) => {
  const { request } = evento;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);

  if (url.hostname === 'tile.openstreetmap.org') {
    evento.respondWith(mosaico(request));
    return;
  }
  if (url.origin !== self.location.origin) return;

  const ruta = url.pathname.slice(new URL(self.registration.scope).pathname.length);
  if (request.mode === 'navigate' && (ruta === '' || ruta === 'index.html')) {
    evento.respondWith(caches.match(new URL('index.html', self.registration.scope)).then((r) => r ?? fetch(request)));
  } else if (ruta.startsWith('data/')) {
    evento.respondWith(primeroRed(request, CACHE_DATOS));
  } else if (ruta.startsWith('img/')) {
    evento.respondWith(guardadoYActualizar(evento, CACHE_FOTOS));
  } else {
    evento.respondWith(primeroCache(request, CACHE_APP));
  }
});

// Datos: lo último si la red responde en menos de 4 s; si no, lo que quedó guardado.
async function primeroRed(request, nombreCache) {
  const cache = await caches.open(nombreCache);
  const red = fetch(request).then((respuesta) => {
    if (respuesta.ok) cache.put(request, respuesta.clone());
    return respuesta;
  });
  const guardada = await cache.match(request, { ignoreSearch: true });
  if (!guardada) return red;
  const espera = new Promise((resolver) => setTimeout(() => resolver(guardada), 4000));
  return Promise.race([red.catch(() => guardada), espera]);
}

// App: lo guardado primero; si no está, se baja y se guarda.
async function primeroCache(request, nombreCache) {
  const cache = await caches.open(nombreCache);
  const guardada = await cache.match(request);
  if (guardada) return guardada;
  const respuesta = await fetch(request);
  if (respuesta.ok) cache.put(request, respuesta.clone());
  return respuesta;
}

// Fotos: se muestra lo guardado al instante y se actualiza en segundo plano
// (por si se reemplazó una foto manteniendo el nombre de archivo).
async function guardadoYActualizar(evento, nombreCache) {
  const cache = await caches.open(nombreCache);
  const guardada = await cache.match(evento.request);
  const red = fetch(evento.request).then(async (respuesta) => {
    if (respuesta.ok) await cache.put(evento.request, respuesta.clone());
    return respuesta;
  });
  if (!guardada) return red;
  evento.waitUntil(red.catch(() => {}));
  return guardada;
}

// Mosaicos del mapa: solo se guardan los que ya se vieron, con un tope
// (la política de OpenStreetMap no permite descargas masivas).
async function mosaico(request) {
  const cache = await caches.open(CACHE_MAPA);
  const guardado = await cache.match(request);
  if (guardado) return guardado;
  const respuesta = await fetch(request);
  if (respuesta.ok) {
    await cache.put(request, respuesta.clone());
    const claves = await cache.keys();
    for (const clave of claves.slice(0, Math.max(0, claves.length - MAX_MOSAICOS))) await cache.delete(clave);
  }
  return respuesta;
}
