// Arranque de la app: router por hash, barra de pestañas y service worker.

import { cargarDatos, TIPOS_PERFIL } from './datos.js';
import { FACETAS } from './filtros.js';
import { el, icono, cerrarHoja, liberarUrls, aviso, mensaje } from './ui.js';
import { logo } from './grafica.js';
import { iniciarTema, abrirSelectorTema } from './tema.js';
import { leerPreferencia, guardarPreferencia } from './plataforma/preferencias.js';
import * as inicio from './vistas/inicio.js';
import * as obras from './vistas/obras.js';
import * as perfil from './vistas/perfil.js';
import * as mapa from './vistas/mapa.js';
import * as obra from './vistas/obra.js';
import * as diario from './vistas/diario.js';
import * as listas from './vistas/listas.js';
import * as nuevaVisita from './vistas/nueva-visita.js';

// pestana: qué pestaña queda marcada · atras: muestra el botón Volver (y adónde ir si no hay historial)
// seccion: la palabra que acompaña a la marca en la cabecera · titulo: el título de la pestaña del navegador
const SECCION_PERFIL = { provincia: 'Provincia', ciudad: 'Ciudad', barrio: 'Barrio', arquitecto: 'Arquitecto/a' };
const RUTAS = {
  '': { render: inicio.render, pestana: 'obras', titulo: 'Jagten' },
  obras: { render: obras.render, pestana: 'obras', titulo: 'Obras', seccion: 'Obras', atras: '#/' },
  // Perfiles (#/arquitecto/frank-lloyd-wright) e índices (#/arquitectos)
  ...Object.fromEntries(Object.entries(TIPOS_PERFIL).flatMap(([tipo, def]) => [
    [tipo, { render: perfil.render, pestana: 'obras', seccion: SECCION_PERFIL[tipo] ?? def.singular, atras: '#/' }],
    [def.indice, { render: perfil.renderIndice, pestana: 'obras', titulo: def.plural, seccion: def.plural, atras: '#/' }],
  ])),
  obra: { render: obra.render, pestana: 'obras', seccion: 'Obra', atras: '#/' },
  mapa: { render: mapa.render, pestana: 'mapa', titulo: 'Mapa', seccion: 'Mapa', persistente: true },
  diario: { render: diario.render, pestana: 'diario', titulo: 'Diario', seccion: 'Diario' },
  listas: { render: listas.render, pestana: 'listas', titulo: 'Listas', seccion: 'Listas' },
  lista: { render: listas.renderDetalle, pestana: 'listas', seccion: 'Lista', atras: '#/listas' },
  nueva: { render: nuevaVisita.render, pestana: 'visita', titulo: 'Nueva visita', seccion: 'Visita', atras: '#/' },
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
// En el celular la búsqueda está plegada en la lupa: tocarla la despliega en la misma fila, en
// lugar del título. Con el campo vacío y sin foco, vuelve a plegarse.
const cabecera = document.querySelector('.cabecera');
const plegable = () => matchMedia('(max-width: 599px)').matches;
function desplegar(abierta) {
  cabecera.classList.toggle('buscando', abierta);
  if (abierta) campoBusqueda.focus();
}
campoBusqueda.addEventListener('blur', () => { if (!campoBusqueda.value.trim()) setTimeout(() => desplegar(false), 150); });
document.querySelector('.cabecera-busqueda').addEventListener('submit', (e) => {
  e.preventDefault();
  if (plegable() && !cabecera.classList.contains('buscando')) { desplegar(true); return; }
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

// La cabecera es siempre la de la portada: la marca (lleva al inicio) y la palabra de la sección.
function ponerCabecera(seccion) {
  titulo.classList.add('cabecera-marca');
  titulo.replaceChildren(
    el('a', { class: 'marca-enlace', href: '#/', 'aria-label': 'Jagten: ir al inicio' },
      logo(), el('span', { class: 'marca-texto' }, el('span', { class: 'logo-nombre' }, 'jagten'),
        seccion && el('span', { class: 'cabecera-seccion' }, seccion))),
  );
}

// Las vistas dan el nombre de lo que muestran: va al título de la pestaña del navegador.
function ponerTitulo(texto) {
  document.title = texto === 'Jagten' ? texto : `${texto} · Jagten`;
}


// La primera vez que se entra a la app, la pantalla de carga se queda hasta que el skyline termina
// de construirse (y se recuerda en el teléfono). Las veces siguientes se va apenas cargan los
// datos. Con "reducir movimiento" no hay animación y no se espera.
const primeraVez = leerPreferencia('carga-vista') !== 'si';

function finDelSkyline(carga) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return 0;
  const segundos = (t) => parseFloat(t) * (t.endsWith('ms') ? 0.001 : 1);
  let fin = 0;
  for (const edificio of carga.querySelectorAll('.edificio')) {
    const estilo = getComputedStyle(edificio);
    fin = Math.max(fin, segundos(estilo.animationDelay) + segundos(estilo.animationDuration));
  }
  return fin * 1000 + 400; // un instante quieto antes de irse
}

function quitarCarga() {
  const carga = document.getElementById('carga');
  if (!carga || carga.classList.contains('oculta')) return;
  const ocultar = () => {
    carga.classList.add('oculta');
    setTimeout(() => carga.remove(), 300);
  };
  if (!primeraVez) { ocultar(); return; }
  guardarPreferencia('carga-vista', 'si');
  setTimeout(ocultar, Math.max(0, finDelSkyline(carga) - performance.now()));
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
  ponerCabecera(partes[0] === 'obra' && partes[2] === 'visitas' ? 'Visitas' : ruta?.seccion);
  ponerTitulo(ruta?.titulo ?? 'Jagten');
  // El campo de la cabecera muestra la búsqueda de la grilla; fuera de ella, queda vacío.
  if (clave === 'obras') campoBusqueda.value = params.get('q') ?? '';
  else if (document.activeElement !== campoBusqueda) campoBusqueda.value = '';
  cabecera.classList.toggle('buscando', Boolean(campoBusqueda.value) || document.activeElement === campoBusqueda);

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

// El botón VISITA abre la nueva visita en un panel. En una obra, esa obra viene elegida; en un
// perfil, sus obras aparecen primero.
document.querySelector('.pestanas [data-pestana="visita"]').addEventListener('click', async (e) => {
  e.preventDefault();
  const datos = await cargarDatos().catch(() => null);
  if (!datos) { location.hash = '#/nueva'; return; }
  const { partes } = leerRuta();
  const opciones = { alGuardar: () => mostrar({ recarga: true }) };
  if (partes[0] === 'obra' && datos.porId.has(partes[1])) opciones.obra = partes[1];
  else if (TIPOS_PERFIL[partes[0]]) {
    const valor = datos.slugs[partes[0]]?.get(partes[1] ?? '');
    if (valor) opciones.sugeridas = perfil.obrasDePerfil(datos, partes[0], valor).map((o) => o.id);
  }
  nuevaVisita.abrirNuevaVisita(datos, opciones);
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
    if (habiaControlador) aviso('Hay una versión nueva de Jagten.', { accion: 'Actualizar', alTocar: () => location.reload(), duracion: 0 });
    habiaControlador = true;
  });
  navigator.serviceWorker.register('sw.js').catch((error) => console.warn('No se pudo registrar el service worker', error));
}
