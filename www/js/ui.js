// Piezas de interfaz compartidas. Los textos que vienen de los datos se insertan
// siempre como texto (nunca como HTML).

import { rangoAnios, lugarCorto, formatoFecha, esUrl, colorMarco } from './datos.js';
import { patronTapa } from './grafica.js';

export function el(etiqueta, props = {}, ...hijos) {
  const nodo = document.createElement(etiqueta);
  for (const [clave, valor] of Object.entries(props ?? {})) {
    if (valor == null || valor === false) continue;
    if (clave === 'class') nodo.className = valor;
    else if (clave === 'dataset') Object.assign(nodo.dataset, valor);
    else if (clave.startsWith('on')) nodo.addEventListener(clave.slice(2), valor);
    else if (['value', 'checked', 'disabled', 'selected', 'hidden'].includes(clave)) nodo[clave] = valor;
    else nodo.setAttribute(clave, valor === true ? '' : valor);
  }
  agregar(nodo, hijos);
  return nodo;
}

function agregar(nodo, hijos) {
  for (const hijo of hijos.flat(Infinity)) {
    if (hijo == null || hijo === false || hijo === '') continue;
    nodo.append(hijo instanceof Node ? hijo : String(hijo));
  }
}

// ---- Íconos (SVG fijos, no vienen de los datos) ----

const ICONOS = {
  grilla: '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
  mapa: '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
  mas: '<path d="M12 5v14M5 12h14"/>',
  diario: '<path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15H6.5A1.5 1.5 0 0 0 5 19.5z"/><path d="M5 19.5A1.5 1.5 0 0 0 6.5 21H19v-3"/><path d="M9 7.5h6"/>',
  listas: '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/>',
  atras: '<path d="M15 5l-7 7 7 7"/>',
  filtros: '<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>',
  ubicacion: '<circle cx="12" cy="12" r="3.5"/><circle cx="12" cy="12" r="7.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22"/>',
  inicio: '<path d="M4 11l8-6.5 8 6.5"/><path d="M6.5 9.5V20h11V9.5"/>',
  cerrar: '<path d="M6 6l12 12M18 6L6 18"/>',
  camara: '<path d="M4 8h3.2l1.8-2.5h6l1.8 2.5H20v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
  compartir: '<path d="M12 15V3.5M7.5 8L12 3.5 16.5 8"/><path d="M5 12.5V20h14v-7.5"/>',
  ruta: '<path d="M5 12h14M13 6l6 6-6 6"/>',
  tema: '<circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor"/>',
  basura: '<path d="M4.5 7h15M10 7V4.5h4V7M6.5 7l1 13h9l1-13"/>',
};

export function icono(nombre) {
  const plantilla = document.createElement('template');
  plantilla.innerHTML = `<svg class="icono" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONOS[nombre] ?? ''}</svg>`;
  return plantilla.content.firstChild;
}

export function botonIcono(nombre, etiqueta, alTocar, clase = '') {
  return el('button', { type: 'button', class: `boton-icono ${clase}`, 'aria-label': etiqueta, title: etiqueta, onclick: alTocar }, icono(nombre));
}

// ---- URLs temporales para fotos guardadas en el teléfono ----

const urlsTemporales = new Set();

export function urlTemporal(blob) {
  const url = URL.createObjectURL(blob);
  urlsTemporales.add(url);
  return url;
}

export function liberarUrls() {
  for (const url of urlsTemporales) URL.revokeObjectURL(url);
  urlsTemporales.clear();
}

export function fuenteFoto(foto) {
  return foto.blob ? urlTemporal(foto.blob) : foto.archivo;
}

// ---- Obras ----

export const rutaObra = (id) => `#/obra/${encodeURIComponent(id)}`;

export function marcaEjemplo() {
  return el('span', { class: 'marca-ejemplo' }, 'Ejemplo');
}

export function sinFoto() {
  return el('div', { class: 'sin-foto' }, el('span', {}, 'Sin fotos'));
}

export function imagenObra(obra) {
  const foto = obra.fotos?.[0];
  return foto ? el('img', { src: foto.archivo, alt: obra.nombre, loading: 'lazy', decoding: 'async' }) : sinFoto();
}

export function lineaAutoria(obra) {
  return [(obra.arquitectos ?? []).join(', '), rangoAnios(obra)].filter(Boolean).join(' · ');
}

// Tapa: la foto enmarcada en un campo de color plano; sin foto, un patrón de líneas.
export function tapaObra(obra) {
  const foto = obra.fotos?.[0];
  return el('div', { class: `tapa marco-${colorMarco(obra)}` },
    foto ? el('img', { src: foto.archivo, alt: obra.nombre, loading: 'lazy', decoding: 'async' }) : patronTapa(obra.id),
    obra.ejemplo && marcaEjemplo(),
  );
}

export function tarjetaObra(obra, { detalle } = {}) {
  return el('a', { class: 'tarjeta', href: rutaObra(obra.id) },
    tapaObra(obra),
    el('div', { class: 'tarjeta-texto' },
      el('h3', {}, obra.nombre),
      el('p', {}, rangoAnios(obra) || 's/f'),
      detalle,
    ),
  );
}

// Fila compacta (miniatura + texto), para listas dentro de hojas y del diario.
export function filaObra(obra, { detalle, href, alTocar } = {}) {
  const contenido = [
    el('div', { class: 'fila-miniatura' }, imagenObra(obra)),
    el('div', { class: 'fila-texto' }, el('strong', {}, obra.nombre), el('span', { class: 'tenue' }, detalle ?? lugarCorto(obra))),
  ];
  return alTocar
    ? el('button', { type: 'button', class: 'fila-obra', onclick: alTocar }, contenido)
    : el('a', { class: 'fila-obra', href: href ?? rutaObra(obra.id) }, contenido);
}

export function creditoFoto(foto) {
  const partes = [];
  if (foto.autor) partes.push(`Foto: ${foto.autor}`);
  if (foto.licencia) partes.push(foto.licencia);
  return el('figcaption', { class: 'credito' },
    partes.join(' · '),
    foto.fuente && [
      partes.length ? ' · ' : '',
      esUrl(foto.fuente) ? el('a', { href: foto.fuente, target: '_blank', rel: 'noopener' }, 'Fuente') : foto.fuente,
    ],
  );
}

// Galería horizontal a ancho completo, con contador "1 / 3".
export function galeria(fotos, { alt = '', pie } = {}) {
  const pista = el('div', { class: 'galeria-pista' },
    fotos.map((foto) => el('figure', { class: 'galeria-foto' },
      el('img', { src: fuenteFoto(foto), alt: foto.pie || alt, loading: 'lazy', decoding: 'async' }),
      pie ? pie(foto) : null,
    )),
  );
  const contador = fotos.length > 1 ? el('span', { class: 'galeria-contador' }, `1 / ${fotos.length}`) : null;
  if (contador) {
    pista.addEventListener('scroll', () => {
      const actual = Math.round(pista.scrollLeft / pista.clientWidth) + 1;
      contador.textContent = `${Math.min(actual, fotos.length)} / ${fotos.length}`;
    }, { passive: true });
  }
  return el('div', { class: 'galeria' }, pista, contador);
}

// ---- Diario ----

export function estrellas(puntaje) {
  if (!puntaje) return null;
  return el('span', { class: 'estrellas', 'aria-label': `Puntaje: ${puntaje} de 5` }, '★'.repeat(puntaje) + '☆'.repeat(5 - puntaje));
}

export function tarjetaEntrada(entrada, datos, { conObra = true } = {}) {
  const obra = datos.porId.get(entrada.obra_id);
  return el('article', { class: 'entrada' },
    el('header', { class: 'entrada-cabecera' },
      el('time', { datetime: entrada.fecha }, formatoFecha(entrada.fecha)),
      estrellas(entrada.puntaje),
      entrada.local && el('span', { class: 'marca-local' }, entrada.exportada ? 'En el teléfono · exportada' : 'Solo en este teléfono'),
    ),
    conObra && (obra
      ? filaObra(obra)
      : el('p', { class: 'tenue' }, `Obra "${entrada.obra_id}" (no está en el catálogo)`)),
    entrada.nota && el('p', { class: 'entrada-nota' }, entrada.nota),
    entrada.fotos?.length > 0 && galeria(entrada.fotos, {
      alt: obra?.nombre,
      pie: (foto) => foto.pie && el('figcaption', { class: 'credito' }, foto.pie),
    }),
    entrada.local && el('div', { class: 'entrada-acciones' },
      el('a', { class: 'boton boton-chico', href: `#/nueva?editar=${encodeURIComponent(entrada.id)}` }, 'Editar'),
    ),
  );
}

// ---- Estados vacíos y mensajes ----

export function mensaje(titulo, texto, ...acciones) {
  return el('div', { class: 'mensaje' }, el('h2', {}, titulo), texto && el('p', { class: 'tenue' }, texto), acciones.length > 0 && el('div', { class: 'acciones' }, acciones));
}

let avisoActual = null;

export function aviso(texto, { accion, alTocar, duracion = 4000 } = {}) {
  avisoActual?.remove();
  const nodo = el('div', { class: 'aviso', role: 'status' },
    el('span', {}, texto),
    accion && el('button', { type: 'button', onclick: () => { nodo.remove(); alTocar(); } }, accion),
  );
  document.body.append(nodo);
  avisoActual = nodo;
  if (duracion) setTimeout(() => nodo.remove(), duracion);
}

// ---- Hoja inferior ----

let hojaActual = null;

export function abrirHoja({ titulo, contenido, pie, alCerrar }) {
  cerrarHoja({ inmediato: true });
  const cuerpo = el('div', { class: 'hoja-cuerpo' }, contenido);
  const cabecera = el('div', { class: 'hoja-cabecera' },
    el('div', { class: 'hoja-asa', 'aria-hidden': 'true' }),
    el('h2', {}, titulo),
    botonIcono('cerrar', 'Cerrar', () => cerrarHoja()),
  );
  const piso = pie ? el('div', { class: 'hoja-pie' }, pie) : null;
  const fondo = el('div', { class: 'hoja-fondo', onclick: () => cerrarHoja() });
  const hoja = el('div', { class: 'hoja', role: 'dialog', 'aria-modal': 'true', 'aria-label': titulo }, cabecera, cuerpo, piso);
  deslizarParaCerrar(cabecera, hoja);
  document.body.append(fondo, hoja);
  document.body.classList.add('con-hoja');
  requestAnimationFrame(() => {
    fondo.classList.add('abierta');
    hoja.classList.add('abierta');
  });
  hojaActual = { fondo, hoja, alCerrar };
  return { hoja, cuerpo, pie: piso, cerrar: () => cerrarHoja() };
}

export function cerrarHoja({ inmediato = false } = {}) {
  if (!hojaActual) return;
  const { fondo, hoja, alCerrar } = hojaActual;
  hojaActual = null;
  alCerrar?.();
  document.body.classList.remove('con-hoja');
  if (inmediato) {
    fondo.remove();
    hoja.remove();
    return;
  }
  fondo.classList.remove('abierta');
  hoja.classList.remove('abierta');
  hoja.style.removeProperty('--arrastre');
  setTimeout(() => { fondo.remove(); hoja.remove(); }, 250);
}

function deslizarParaCerrar(asa, hoja) {
  let inicio = null;
  asa.addEventListener('touchstart', (e) => { inicio = e.touches[0].clientY; hoja.classList.add('arrastrando'); }, { passive: true });
  asa.addEventListener('touchmove', (e) => {
    if (inicio === null) return;
    hoja.style.setProperty('--arrastre', `${Math.max(0, e.touches[0].clientY - inicio)}px`);
  }, { passive: true });
  asa.addEventListener('touchend', (e) => {
    const recorrido = e.changedTouches[0].clientY - inicio;
    inicio = null;
    hoja.classList.remove('arrastrando');
    if (recorrido > 80) cerrarHoja();
    else hoja.style.removeProperty('--arrastre');
  });
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') cerrarHoja();
});
