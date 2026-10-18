// Mapa mundial con Leaflet + OpenStreetMap. Se crea una sola vez y se conserva
// al cambiar de pestaña, para no perder la posición.

import { el, icono, flecha, abrirHoja, cerrarHoja, imagenObra, filaObra, lineaAutoria, rutaObra, aviso } from '../ui.js';
import { tieneCoordenadas, distanciaKm, formatoDistancia, lugarCorto, colorMarco, COLORES_MARCO } from '../datos.js';
import { obtenerUbicacion } from '../plataforma/ubicacion.js';

// Vista inicial: zona norte de Buenos Aires (entre Belgrano y Vicente López).
const VISTA_INICIAL = { centro: [-34.543, -58.472], zoom: 13 };
const CERCANAS = 10;

let mapa = null;
let obras = [];
let posicion = null;
let capaPosicion = null;

export function render(contenedor, { datos, params, titulo }) {
  titulo('Mapa');
  if (!window.L) {
    contenedor.replaceChildren(el('div', { class: 'mensaje' }, el('h2', {}, 'No se pudo cargar el mapa'), el('p', { class: 'tenue' }, 'Revisá la conexión y recargá la página.')));
    return;
  }
  if (!mapa) iniciar(contenedor, datos);
  else requestAnimationFrame(() => mapa.invalidateSize());

  const obra = datos.porId.get(params.get('obra'));
  if (obra && tieneCoordenadas(obra)) enfocar(obra);
}

function iniciar(contenedor, datos) {
  const lienzo = el('div', { class: 'mapa' });
  const botonCerca = el('button', { type: 'button', class: 'boton boton-flotante boton-cerca', onclick: cercaMio }, icono('ubicacion'), 'Cerca mío');
  const botonInicio = el('button', {
    type: 'button', class: 'boton-icono boton-flotante boton-inicio', 'aria-label': 'Volver a la vista inicial', title: 'Volver a la vista inicial',
    onclick: () => mapa.flyTo(VISTA_INICIAL.centro, VISTA_INICIAL.zoom),
  }, icono('inicio'));
  contenedor.append(lienzo, botonInicio, botonCerca);

  obras = datos.obras.filter(tieneCoordenadas);
  const sinCoordenadas = datos.obras.length - obras.length;
  if (sinCoordenadas > 0) {
    contenedor.append(el('p', { class: 'mapa-nota' }, sinCoordenadas === 1 ? '1 obra sin coordenadas no aparece' : `${sinCoordenadas} obras sin coordenadas no aparecen`));
  }

  mapa = L.map(lienzo, { zoomControl: false, worldCopyJump: true, minZoom: 2 }).setView(VISTA_INICIAL.centro, VISTA_INICIAL.zoom);
  L.control.zoom({ position: 'topright', zoomInTitle: 'Acercar', zoomOutTitle: 'Alejar' }).addTo(mapa);
  mapa.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    crossOrigin: true, // permite que el service worker guarde los mosaicos ya vistos
    attribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">colaboradores de OpenStreetMap</a>',
  }).addTo(mapa);

  // Cada marcador lleva el color del marco de su obra.
  const marcadores = new Map(COLORES_MARCO.map((c) => [c, L.divIcon({ className: `marcador marco-${c}`, html: '<span></span>', iconSize: [40, 40] })]));
  for (const obra of obras) {
    L.marker([obra.ubicacion.lat, obra.ubicacion.lng], { icon: marcadores.get(colorMarco(obra)), title: obra.nombre, alt: obra.nombre })
      .on('click', () => mostrarObra(obra))
      .addTo(mapa);
  }
  requestAnimationFrame(() => mapa.invalidateSize());
}

function distancia(obra) {
  return posicion ? distanciaKm(posicion, obra.ubicacion) : null;
}

function enfocar(obra) {
  mapa.setView([obra.ubicacion.lat, obra.ubicacion.lng], Math.max(mapa.getZoom(), 16));
  mostrarObra(obra);
}

function mostrarObra(obra) {
  const km = distancia(obra);
  abrirHoja({
    titulo: obra.nombre,
    contenido: el('a', { class: 'hoja-obra', href: rutaObra(obra.id) },
      el('div', { class: 'hoja-obra-foto' }, imagenObra(obra)),
      el('p', {}, lineaAutoria(obra)),
      el('p', { class: 'tenue' }, [lugarCorto(obra), km !== null && `a ${formatoDistancia(km)}`].filter(Boolean).join(' · ')),
    ),
    pie: [
      el('a', {
        class: 'boton', target: '_blank', rel: 'noopener',
        href: `https://maps.apple.com/?daddr=${obra.ubicacion.lat},${obra.ubicacion.lng}&q=${encodeURIComponent(obra.nombre)}`,
      }, flecha('paralela'), 'Cómo llegar'),
      el('a', { class: 'boton boton-primario', href: rutaObra(obra.id) }, 'Ver ficha'),
    ],
  });
}

async function cercaMio(evento) {
  const boton = evento.currentTarget;
  boton.disabled = true;
  boton.lastChild.textContent = 'Buscando…';
  try {
    posicion = await obtenerUbicacion();
  } catch (error) {
    aviso(error.message, { duracion: 7000 });
    return;
  } finally {
    boton.disabled = false;
    boton.lastChild.textContent = 'Cerca mío';
  }

  const punto = [posicion.lat, posicion.lng];
  capaPosicion?.remove();
  capaPosicion = L.layerGroup([
    L.circle(punto, { radius: posicion.precision, className: 'posicion-precision', interactive: false }),
    L.circleMarker(punto, { radius: 8, className: 'posicion-punto', interactive: false }),
  ]).addTo(mapa);
  mapa.setView(punto, Math.max(mapa.getZoom(), 15));

  const cercanas = obras
    .map((obra) => ({ obra, km: distancia(obra) }))
    .sort((a, b) => a.km - b.km)
    .slice(0, CERCANAS);
  abrirHoja({
    titulo: 'Cerca tuyo',
    contenido: cercanas.length
      ? el('div', { class: 'filas' }, cercanas.map(({ obra, km }) => filaObra(obra, {
        detalle: `${formatoDistancia(km)} · ${lugarCorto(obra)}`,
        alTocar: () => { cerrarHoja({ inmediato: true }); enfocar(obra); },
      })))
      : el('p', { class: 'tenue' }, 'No hay obras con coordenadas cargadas.'),
  });
}

// ---- Panel de mapa (desde la ficha de una obra) ----

// Un mapa en un panel grande, centrado en la obra, con un botón para agrandar que lleva a la
// página del mapa. Es un mapa aparte del de la pestaña Mapa: se crea al abrir y se descarta.
export function abrirMapaObra(obra) {
  if (!window.L || !tieneCoordenadas(obra)) return;
  const lienzo = el('div', { class: 'mapa-panel' });
  let mapaPanel = null;
  const agrandar = el('a', { class: 'boton boton-chico', href: `#/mapa?obra=${encodeURIComponent(obra.id)}` }, icono('mapa'), 'Agrandar');
  abrirHoja({
    titulo: obra.nombre, contenido: lienzo, clase: 'hoja-mapa', acciones: agrandar,
    alCerrar: () => { mapaPanel?.remove(); mapaPanel = null; },
  });
  const punto = [obra.ubicacion.lat, obra.ubicacion.lng];
  mapaPanel = L.map(lienzo, { zoomControl: false, attributionControl: true }).setView(punto, 16);
  L.control.zoom({ position: 'topright', zoomInTitle: 'Acercar', zoomOutTitle: 'Alejar' }).addTo(mapaPanel);
  mapaPanel.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19, crossOrigin: true,
    attribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">colaboradores de OpenStreetMap</a>',
  }).addTo(mapaPanel);
  L.marker(punto, { icon: L.divIcon({ className: `marcador marco-${colorMarco(obra)}`, html: '<span></span>', iconSize: [40, 40] }), title: obra.nombre, alt: obra.nombre }).addTo(mapaPanel);
  // La hoja entra con una transición: hay que avisarle a Leaflet el tamaño final.
  // y volver a centrar en la obra, porque el centro se calculó con el tamaño de antes.
  setTimeout(() => { mapaPanel?.invalidateSize(); mapaPanel?.setView(punto, 16); }, 320);
}
