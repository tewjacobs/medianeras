import { simbolo, medidasSimbolo, registrarColoresSimbolos } from './js/grafica.js';

const simbolos = await (await fetch('data/simbolos.json', { cache: 'no-store' })).json();

const h = (etiqueta, props = {}, ...hijos) => {
  const nodo = Object.assign(document.createElement(etiqueta), props);
  nodo.append(...hijos.flat(Infinity).filter(Boolean));
  return nodo;
};

// Cada obra: colección y clave en simbolos.json, sus fotos y tres fondos (claro, oscuro) para elegir.
const OBRAS = [
  ['mundo', '1910', 'La Pedrera: Barcelona', ['la pedrera:casa mila/Casa_Milà,_general_view.jpg'], {
    'A · cielo mediterráneo': ['#bcd6e8', '#1d2a3a'],
    'B · arena': ['#e9d9bc', '#3d3427'],
    'C · terracota suave': ['#e8c3ad', '#45302a'],
  }],
  ['mundo', '1930', 'Paimio: bosque finlandés', ['paimio/paimio.jpg'], {
    'A · verde pino': ['#c3d3bf', '#1f2b22'],
    'B · blanco nórdico': ['#dfe6ea', '#262c33'],
    'C · abedul': ['#d6d8c6', '#2d2f27'],
  }],
  ['mundo', '1950', 'Seagram: el atardecer de la foto', ['seagram/seagramexrt.webp', 'seagram/Seagram-Bldg.jpg'], {
    'A · atardecer naranja': ['#f0c9a0', '#4a3226'],
    'B · azul crepúsculo': ['#b9c4dc', '#1c2236'],
    'C · rosa ocaso': ['#eccbc8', '#3d2a30'],
  }],
  ['mundo', '1970', 'Pompidou: la plaza y el cielo de París', ['pompidou/IMG_3603.jpeg', 'pompidou/av_19293.webp'], {
    'A · gris plaza': ['#d8d4cc', '#33312d'],
    'B · cielo gris celeste': ['#c9d6de', '#232c33'],
    'C · piedra clara': ['#e8dfcf', '#3a352c'],
  }],
  ['mundo', '1990', 'Guggenheim Bilbao: la ría y el monte', ['bilbao guggenhiem/guggen.jpg'], {
    'A · gris lluvia': ['#cfd4d6', '#2a2f33'],
    'B · verde monte': ['#c6d2b8', '#232b20'],
    'C · ría azul gris': ['#bccbd2', '#1f2a30'],
  }],
];

const colores = { ...simbolos.colores };
OBRAS.forEach(([, clave, , , fondos]) => Object.entries(fondos).forEach(([nombre, [claro, oscuro]]) => {
  colores[`f-${clave}-${nombre[0]}`] = { claro, oscuro };
}));
registrarColoresSimbolos(colores);

const rutaFoto = (a) => `referencias/${a.split('/').map(encodeURIComponent).join('/')}`;
const tapa = (p, tema) => {
  const caja = h('div', {}, simbolo(p, { ancho: 100, alto: 100, margen: 8, fijo: true, superficie: 0.42, clase: 'tapa-grafica' }));
  caja.dataset.tema = tema;
  return caja;
};

// Como los elegidos: un borde de fondo de 1.5 más el 6 % del lado mayor, y el marco en tinta.
const aire = (p) => { const m = medidasSimbolo(p); return Math.round((1.5 + 0.06 * Math.max(m.ancho, m.alto)) * 10) / 10; };

document.getElementById('obras').replaceChildren(...OBRAS.map(([coleccion, clave, titulo, fotos, fondos]) => {
  const p = simbolos[coleccion]?.[clave] ?? simbolos.decadas[coleccion][clave];
  return h('section', {}, h('h2', { textContent: titulo }), h('div', { className: 'fila' },
    h('div', { className: 'foto' }, fotos.length ? fotos.map((a) => h('img', { src: rutaFoto(a), alt: '' })) : h('p', { textContent: 'Sin foto de referencia.' })),
    h('div', { className: 'opcion' }, h('b', { textContent: 'Hoy · sin fondo' }), h('div', { className: 'par' }, tapa(p, 'claro'), tapa(p, 'oscuro'))),
    Object.keys(fondos).map((nombre) => {
      const conFondo = { ...p, placa: `f-${clave}-${nombre[0]}`, aire: aire(p), marco: 'tinta' };
      return h('div', { className: 'opcion' }, h('b', { textContent: nombre }), h('div', { className: 'par' }, tapa(conFondo, 'claro'), tapa(conFondo, 'oscuro')));
    })));
}));
