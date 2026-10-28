import { simbolo, medidasSimbolo, registrarColoresSimbolos } from './js/grafica.js';

const simbolos = await (await fetch('data/simbolos.json', { cache: 'no-store' })).json();

const h = (etiqueta, props = {}, ...hijos) => {
  const nodo = Object.assign(document.createElement(etiqueta), props);
  nodo.append(...hijos.flat(Infinity).filter(Boolean));
  return nodo;
};

// Cada obra: colección y clave en simbolos.json, sus fotos y tres fondos (claro, oscuro) para elegir.
const OBRAS = [
  ['argentina', '1960', 'Colegio Manuel Belgrano (Córdoba): hormigón, cielorraso de madera y ventana corrida roja', ['60s argentina/Belgrano_por_fuera_027.jpg', '60s argentina/IMG-20200918-WA0002-1024x738.jpg'], {
    'A · algarrobo': ['#a9b08e', '#2a2d20'],
    'B · arena serrana': ['#ddd0b0', '#38331f'],
    'C · durazno': ['#e8c4a4', '#45332a'],
  }],
];

// El marco es el color invertido de su propio fondo, como los elegidos.
const invertir = (hex) => '#' + (0xffffff - parseInt(hex.slice(1), 16)).toString(16).padStart(6, '0');
const colores = { ...simbolos.colores };
OBRAS.forEach(([coleccion, clave, , , fondos]) => Object.entries(fondos).forEach(([nombre, [claro, oscuro]]) => {
  colores[`f-${coleccion}-${clave}-${nombre[0]}`] = { claro, oscuro };
  colores[`f-${coleccion}-${clave}-${nombre[0]}-marco`] = { claro: invertir(claro), oscuro: invertir(oscuro) };
}));
registrarColoresSimbolos(colores);

const rutaFoto = (a) => `referencias/${a.split('/').map(encodeURIComponent).join('/')}`;
const tapa = (p, tema) => {
  const caja = h('div', {}, simbolo(p, { ancho: 100, alto: 100, margen: 8, fijo: true, superficie: 0.42, clase: 'tapa-grafica' }));
  caja.dataset.tema = tema;
  return caja;
};

// Como los elegidos: un borde de fondo de 1.5 más el 6 % del lado mayor.
const aire = (p) => { const m = medidasSimbolo(p); return Math.round((1.5 + 0.06 * Math.max(m.ancho, m.alto)) * 10) / 10; };

document.getElementById('obras').replaceChildren(...OBRAS.map(([coleccion, clave, titulo, fotos, fondos]) => {
  const p = simbolos[coleccion]?.[clave] ?? simbolos.decadas[coleccion][clave];
  return h('section', {}, h('h2', { textContent: titulo }), h('div', { className: 'fila' },
    h('div', { className: 'foto' }, fotos.length ? fotos.map((a) => h('img', { src: rutaFoto(a), alt: '' })) : h('p', { textContent: 'Sin foto de referencia.' })),
    h('div', { className: 'opcion' }, h('b', { textContent: p.placa ? 'Hoy' : 'Hoy · sin fondo' }), h('div', { className: 'par' }, tapa(p, 'claro'), tapa(p, 'oscuro'))),
    Object.keys(fondos).map((nombre) => {
      const conFondo = { ...p, placa: `f-${coleccion}-${clave}-${nombre[0]}`, aire: aire(p), marco: `f-${coleccion}-${clave}-${nombre[0]}-marco` };
      return h('div', { className: 'opcion' }, h('b', { textContent: nombre }), h('div', { className: 'par' }, tapa(conFondo, 'claro'), tapa(conFondo, 'oscuro')));
    })));
}));
