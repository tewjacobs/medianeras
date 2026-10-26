import { simbolo, medidasSimbolo, registrarColoresSimbolos } from './js/grafica.js';

const simbolos = await (await fetch('data/simbolos.json', { cache: 'no-store' })).json();
registrarColoresSimbolos({ ...simbolos.colores, 'prueba-cielo': { claro: '#bcd5df', oscuro: '#1a2530' } });

const h = (etiqueta, props = {}, ...hijos) => {
  const nodo = Object.assign(document.createElement(etiqueta), props);
  nodo.append(...hijos.flat(Infinity).filter(Boolean));
  return nodo;
};

// Los símbolos de obras (no banderas ni materiales): décadas, estilos y programas.
const obras = [
  ...Object.entries(simbolos.decadas.argentina).map(([k, p]) => [`AR ${k}`, p]),
  ...Object.entries(simbolos.decadas.mundo).map(([k, p]) => [`MUNDO ${k}`, p]),
  ...Object.entries(simbolos.estilos).filter(([, p]) => (p.lineas ?? []).length > 12).map(([k, p]) => [k, p]),
  ...Object.entries(simbolos.programas).map(([k, p]) => [k, p]),
];

const LADO = 100, MARGEN = 8, UTIL = LADO - 2 * MARGEN;

// Tamaño: cuánto achicar cada dibujo respecto de "lo más grande que entra".
const TAMANOS = {
  actual: { titulo: 'A · Como hoy', texto: 'Cada dibujo crece hasta tocar un borde (con algunos achicados a mano).', escala: (p) => p.escala ?? 1 },
  superficie: { titulo: 'B · Misma superficie', texto: 'Todos ocupan la misma área: los anchos y bajos se achican, los angostos crecen hasta donde entran.',
    escala: (p) => igualar(p, (m) => Math.sqrt((UTIL * UTIL * 0.42) / (m.ancho * m.alto))) },
  alto: { titulo: 'C · Mismo alto', texto: 'Todos con el mismo alto (como en una foto de skyline); los muy anchos se achican para entrar.',
    escala: (p) => igualar(p, (m) => (UTIL * 0.7) / m.alto) },
};
function igualar(p, deseada) {
  const m = medidasSimbolo(p);
  const entra = Math.min(UTIL / m.ancho, UTIL / m.alto);
  return Math.min(1, deseada(m) / entra);
}

const FONDOS = {
  actual: { titulo: '1 · Como hoy', texto: 'Solo algunos tienen fondo (Tenerife, el puente, el Monumental).', placa: (p) => p.placa },
  cielo: { titulo: '2 · Todos con cielo', texto: 'Los que no tienen fondo propio llevan un cielo suave (noche azul en oscuro).', placa: (p) => p.placa ?? 'prueba-cielo' },
  gris: { titulo: '3 · Todos con placa neutra', texto: 'Los que no tienen fondo propio llevan una placa del gris del papel.', placa: (p) => p.placa ?? 'papel-2' },
};

const params = new URLSearchParams(location.search);
let tamano = params.get('tamano') ?? 'actual';
let fondo = params.get('fondo') ?? 'actual';

function grilla(tema) {
  const caja = h('div', { className: 'grilla' });
  caja.dataset.tema = tema;
  caja.append(...obras.map(([nombre, p]) => {
    const partitura = { ...p, escala: TAMANOS[tamano].escala(p), placa: FONDOS[fondo].placa(p) };
    return h('figure', {}, simbolo(partitura, { ancho: LADO, alto: LADO, margen: MARGEN, fijo: true, clase: 'tapa-grafica' }),
      h('figcaption', { textContent: nombre }));
  }));
  return caja;
}

function botones(opciones, actual, elegir) {
  return h('div', { className: 'botones' }, Object.entries(opciones).map(([clave, o]) =>
    h('button', { type: 'button', className: `boton boton-chico${clave === actual ? ' elegido' : ''}`, textContent: o.titulo, title: o.texto,
      onclick: () => { elegir(clave); dibujar(); } })));
}

function dibujar() {
  history.replaceState(null, '', `?tamano=${tamano}&fondo=${fondo}`);
  document.getElementById('controles').replaceChildren(
    h('p', {}, h('b', { textContent: 'Tamaño: ' }), TAMANOS[tamano].texto), botones(TAMANOS, tamano, (c) => { tamano = c; }),
    h('p', {}, h('b', { textContent: 'Fondo: ' }), FONDOS[fondo].texto), botones(FONDOS, fondo, (c) => { fondo = c; }));
  document.getElementById('grillas').replaceChildren(grilla('claro'), grilla('oscuro'));
}
dibujar();
