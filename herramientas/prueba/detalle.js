import { simbolo, registrarColoresSimbolos } from './js/grafica.js';

const simbolos = await (await fetch('data/simbolos.json', { cache: 'no-store' })).json();
registrarColoresSimbolos(simbolos.colores);

const h = (etiqueta, props = {}, ...hijos) => {
  const nodo = Object.assign(document.createElement(etiqueta), props);
  nodo.append(...hijos.flat(Infinity).filter(Boolean));
  return nodo;
};

// Cada obra: colección, clave, título y su foto de referencia.
const OBRAS = [
  ['argentina', '1920', 'Palacio Barolo', 'barolo/345_palacio-barolo_editarq-pablo-corral_02.jpg'],
  ['argentina', '2000', 'Puente de la Mujer', 'puente de la mujer/mujer.jpg'],
];

const rutaFoto = (a) => `referencias/${a.split('/').map(encodeURIComponent).join('/')}`;
const caja = (p, tema, opciones) => {
  const c = h('div', {}, simbolo(p, { ancho: 100, alto: 100, fijo: true, clase: 'tapa-grafica', ...opciones }));
  c.dataset.tema = tema;
  return c;
};

document.getElementById('obras').replaceChildren(...OBRAS.map(([coleccion, clave, titulo, foto]) => {
  const p = simbolos.decadas[coleccion][clave];
  const { placa, aire, marco, ...sinFondo } = p;
  return h('section', {}, h('h2', { textContent: titulo }), h('div', { className: 'fila' },
    h('div', { className: 'foto' }, h('img', { src: rutaFoto(foto), alt: '' })),
    h('div', { className: 'par' },
      caja(sinFondo, 'claro', { margen: 2 }), caja(sinFondo, 'oscuro', { margen: 2 }),
      caja(p, 'claro', { margen: 8, superficie: 0.42 }), caja(p, 'oscuro', { margen: 8, superficie: 0.42 }))));
}));
