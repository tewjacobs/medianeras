// Arranque de la app: router por hash, barra de pestañas y service worker.

import { cargarDatos } from './datos.js';
import { el, icono, cerrarHoja, liberarUrls, aviso, mensaje } from './ui.js';
import * as inicio from './vistas/inicio.js';
import * as mapa from './vistas/mapa.js';
import * as obra from './vistas/obra.js';
import * as diario from './vistas/diario.js';
import * as listas from './vistas/listas.js';
import * as nuevaVisita from './vistas/nueva-visita.js';

// pestana: qué pestaña queda marcada · atras: muestra el botón Volver (y adónde ir si no hay historial)
const RUTAS = {
  '': { render: inicio.render, pestana: 'obras', titulo: 'Medianeras' },
  obra: { render: obra.render, pestana: 'obras', atras: '#/' },
  mapa: { render: mapa.render, pestana: 'mapa', titulo: 'Mapa', persistente: true },
  diario: { render: diario.render, pestana: 'diario', titulo: 'Diario' },
  listas: { render: listas.render, pestana: 'listas', titulo: 'Listas' },
  lista: { render: listas.renderDetalle, pestana: 'listas', atras: '#/listas' },
  nueva: { render: nuevaVisita.render, pestana: 'visita', titulo: 'Nueva visita', atras: '#/' },
};

const principal = document.getElementById('principal');
const titulo = document.querySelector('.cabecera-titulo');
const botonAtras = document.querySelector('.cabecera-atras');
const pestanas = document.querySelectorAll('.pestanas a');

const persistentes = new Map();
const scrolls = new Map();
let hashActual = null;
let rutaActual = null;
let navegaciones = 0;
let turno = 0;

for (const nodo of document.querySelectorAll('[data-icono]')) nodo.replaceWith(icono(nodo.dataset.icono));

function leerRuta() {
  const hash = location.hash.replace(/^#\/?/, '');
  const corte = hash.indexOf('?');
  const camino = corte === -1 ? hash : hash.slice(0, corte);
  const query = corte === -1 ? '' : hash.slice(corte + 1);
  const partes = camino.split('/').filter(Boolean).map((p) => {
    try { return decodeURIComponent(p); } catch { return p; }
  });
  return { partes, params: new URLSearchParams(query) };
}

function ponerTitulo(texto) {
  titulo.textContent = texto;
  document.title = texto === 'Medianeras' ? texto : `${texto} · Medianeras`;
}

async function mostrar({ recarga = false } = {}) {
  const miTurno = ++turno;
  if (hashActual !== null && !recarga) scrolls.set(hashActual, window.scrollY);
  hashActual = location.hash || '#/';
  if (!recarga) navegaciones++;

  const { partes, params } = leerRuta();
  const clave = partes[0] ?? '';
  const ruta = RUTAS[clave];
  rutaActual = ruta;

  cerrarHoja({ inmediato: true });
  document.body.dataset.vista = ruta ? clave || 'inicio' : 'error';
  for (const a of pestanas) a.toggleAttribute('aria-current', a.dataset.pestana === ruta?.pestana);
  botonAtras.hidden = !ruta?.atras;
  ponerTitulo(ruta?.titulo ?? 'Medianeras');

  let datos;
  try {
    datos = await cargarDatos();
  } catch (error) {
    console.error(error);
    principal.replaceChildren(mensaje('No se pudieron cargar los datos', error.message,
      el('button', { type: 'button', class: 'boton', onclick: () => mostrar({ recarga: true }) }, 'Reintentar')));
    return;
  }
  if (miTurno !== turno) return;

  // Las vistas comunes se rehacen en cada visita; las persistentes (el mapa) se conservan ocultas.
  for (const hijo of principal.children) hijo.hidden = true;
  principal.querySelector('.vista:not(.vista-persistente)')?.remove();
  liberarUrls();

  let contenedor;
  if (ruta?.persistente) {
    contenedor = persistentes.get(clave);
    if (!contenedor) {
      contenedor = el('section', { class: `vista vista-persistente vista-${clave}` });
      persistentes.set(clave, contenedor);
      principal.append(contenedor);
    }
    contenedor.hidden = false;
  } else {
    contenedor = el('section', { class: `vista vista-${clave || 'inicio'}` });
    principal.append(contenedor);
  }

  const ctx = { datos, partes, params, titulo: ponerTitulo, recargar: () => mostrar({ recarga: true }) };
  try {
    if (!ruta) {
      contenedor.append(mensaje('Página no encontrada', null, el('a', { class: 'boton', href: '#/' }, 'Ir al inicio')));
    } else {
      await ruta.render(contenedor, ctx);
    }
  } catch (error) {
    console.error(error);
    contenedor.replaceChildren(mensaje('Algo salió mal', error.message));
  }
  if (miTurno !== turno || ruta?.persistente) return;
  window.scrollTo(0, recarga ? window.scrollY : ruta?.atras ? 0 : (scrolls.get(hashActual) ?? 0));
}

botonAtras.addEventListener('click', () => {
  if (navegaciones > 1) history.back();
  else location.replace(rutaActual?.atras ?? '#/');
});

// Tocar la pestaña activa vuelve arriba de todo, como en las apps de iOS.
for (const a of pestanas) {
  a.addEventListener('click', (e) => {
    if (a.hasAttribute('aria-current') && location.hash === a.getAttribute('href')) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });
}

window.addEventListener('hashchange', () => mostrar());
mostrar();

// ---- Service worker (solo en la web; dentro de Capacitor no hace falta) ----

const esNativo = window.Capacitor?.isNativePlatform?.() === true;
if ('serviceWorker' in navigator && !esNativo) {
  let habiaControlador = Boolean(navigator.serviceWorker.controller);
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (habiaControlador) aviso('Hay una versión nueva de Medianeras.', { accion: 'Actualizar', alTocar: () => location.reload(), duracion: 0 });
    habiaControlador = true;
  });
  navigator.serviceWorker.register('sw.js').catch((error) => console.warn('No se pudo registrar el service worker', error));
}
