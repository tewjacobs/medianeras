// Arranque de la app: router por hash, barra de pestañas y service worker.

import { cargarDatos, TIPOS_PERFIL } from './datos.js';
import { FACETAS } from './filtros.js';
import { el, icono, cerrarHoja, liberarUrls, aviso, mensaje } from './ui.js';
import { logo } from './grafica.js';
import { iniciarTema, abrirSelectorTema } from './tema.js';
import * as inicio from './vistas/inicio.js';
import * as obras from './vistas/obras.js';
import * as perfil from './vistas/perfil.js';
import * as mapa from './vistas/mapa.js';
import * as obra from './vistas/obra.js';
import * as diario from './vistas/diario.js';
import * as listas from './vistas/listas.js';
import * as nuevaVisita from './vistas/nueva-visita.js';

// pestana: qué pestaña queda marcada · atras: muestra el botón Volver (y adónde ir si no hay historial)
const RUTAS = {
  '': { render: inicio.render, pestana: 'obras', titulo: 'Medianeras' },
  obras: { render: obras.render, pestana: 'obras', titulo: 'Obras', atras: '#/' },
  // Perfiles (#/arquitecto/frank-lloyd-wright) e índices (#/arquitectos)
  ...Object.fromEntries(Object.entries(TIPOS_PERFIL).flatMap(([tipo, def]) => [
    [tipo, { render: perfil.render, pestana: 'obras', atras: '#/' }],
    [def.indice, { render: perfil.renderIndice, pestana: 'obras', titulo: def.plural, atras: '#/' }],
  ])),
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

iniciarTema();
for (const nodo of document.querySelectorAll('[data-icono]')) nodo.replaceWith(icono(nodo.dataset.icono));
document.querySelector('.cabecera-tema').addEventListener('click', abrirSelectorTema);
// Búsqueda de la cabecera: escribir lleva a la grilla de todas las obras; ahí, cada letra la filtra.
const campoBusqueda = document.querySelector('.cabecera-campo');
const enObras = () => (location.hash.replace(/^#\/?/, '').split(/[/?]/)[0] === 'obras');
function buscar() {
  const q = campoBusqueda.value.trim();
  if (enObras()) window.dispatchEvent(new CustomEvent('medianeras:buscar', { detail: q }));
  else location.hash = q ? `#/obras?${new URLSearchParams({ q })}` : '#/obras';
}
campoBusqueda.addEventListener('input', buscar);
document.querySelector('.cabecera-busqueda').addEventListener('submit', (e) => {
  e.preventDefault();
  if (!campoBusqueda.value.trim() && !enObras()) { campoBusqueda.focus(); return; }
  buscar();
  campoBusqueda.blur(); // cierra el teclado en el iPhone
});

// Los links viejos con filtros en el inicio (#/?pais=Argentina) pasan a la grilla completa.
function redirigirFiltrosViejos({ partes, params }) {
  if (partes.length || ![...FACETAS.map((f) => f.clave), 'q'].some((c) => params.has(c))) return false;
  location.replace(`#/obras?${params}`);
  return true;
}

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
  const esInicio = texto === 'Medianeras';
  titulo.classList.toggle('cabecera-marca', esInicio);
  if (esInicio) titulo.replaceChildren(logo(), el('span', { class: 'logo-nombre' }, texto.toLowerCase()));
  else titulo.textContent = texto;
  document.title = esInicio ? texto : `${texto} · Medianeras`;
}

function quitarCarga() {
  const carga = document.getElementById('carga');
  if (!carga) return;
  carga.classList.add('oculta');
  setTimeout(() => carga.remove(), 300);
}

async function mostrar({ recarga = false } = {}) {
  const miTurno = ++turno;
  if (hashActual !== null && !recarga) scrolls.set(hashActual, window.scrollY);
  hashActual = location.hash || '#/';
  if (!recarga) navegaciones++;

  const leida = leerRuta();
  if (redirigirFiltrosViejos(leida)) return;
  const { partes, params } = leida;
  const clave = partes[0] ?? '';
  const ruta = RUTAS[clave];
  rutaActual = ruta;

  cerrarHoja({ inmediato: true });
  document.body.dataset.vista = ruta ? clave || 'inicio' : 'error';
  for (const a of pestanas) a.toggleAttribute('aria-current', a.dataset.pestana === ruta?.pestana);
  botonAtras.hidden = !ruta?.atras;
  ponerTitulo(ruta?.titulo ?? 'Medianeras');
  // El campo de la cabecera muestra la búsqueda de la grilla; fuera de ella, queda vacío.
  if (clave === 'obras') campoBusqueda.value = params.get('q') ?? '';
  else if (document.activeElement !== campoBusqueda) campoBusqueda.value = '';

  let datos;
  try {
    datos = await cargarDatos();
  } catch (error) {
    quitarCarga();
    console.error(error);
    principal.replaceChildren(mensaje('No se pudieron cargar los datos', error.message,
      el('button', { type: 'button', class: 'boton', onclick: () => mostrar({ recarga: true }) }, 'Reintentar')));
    return;
  }
  quitarCarga();
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
