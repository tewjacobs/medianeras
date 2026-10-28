import { simbolo, medidasSimbolo, registrarColoresSimbolos } from './js/grafica.js';

const simbolos = await (await fetch('data/simbolos.json', { cache: 'no-store' })).json();

const h = (etiqueta, props = {}, ...hijos) => {
  const nodo = Object.assign(document.createElement(etiqueta), props);
  nodo.append(...hijos.flat(Infinity).filter(Boolean));
  return nodo;
};

// Cada obra: colección y clave en simbolos.json, sus fotos y tres fondos (claro, oscuro) para elegir.
const OBRAS = [
  ['estilos', 'Brutalismo', 'Brutalismo · La Pyramide (Abiyán): hormigón claro escalonado', ['brutalismo/pyramide.jpg', 'brutalismo/La_Pyramide_Abidjan.png'], {
    'A · laterita': ['#c98a6a', '#3d2620'],
    'B · laguna': ['#9fb3a0', '#1f2b25'],
    'C · harmatán': ['#d9c7a8', '#3a3226'],
  }],
  ['programas', 'Hotel', "Hotel · Hôtel de l'Indépendance (Dakar): celdas en punta y ladrillo", ['hotel/01_07_Hotel Independence Dakar_02.jpg.3069039.jpg', 'hotel/72_big.jpg'], {
    'A · buganvilla': ['#e3a7b4', '#41262d'],
    'B · baobab': ['#a8ab95', '#2c2d24'],
    'C · cola': ['#b9655a', '#3a1f1c'],
  }],
  ['programas', 'Templo', 'Templo · gopuram del Meenakshi (Madurai): pisos de figuras de colores', ['religioso/images (9).jpeg', 'religioso/images (10).jpeg'], {
    'A · azafrán': ['#e8a85a', '#43301a'],
    'B · granito rosado': ['#d5b8ab', '#3b2e2a'],
    'C · hoja de banano': ['#8fa070', '#252d1d'],
  }],
  ['programas', 'Museo', 'Museo · pared de sala con tres cuadros (dibujo, sin foto)', [], {
    'A · verde salón': ['#7d977b', '#1d2620'],
    'B · rojo pompeyano': ['#a8483a', '#2f1714'],
    'C · gris paloma': ['#cfc9c0', '#33302c'],
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
