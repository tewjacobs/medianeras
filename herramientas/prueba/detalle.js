import { simbolo, registrarColoresSimbolos } from './js/grafica.js';

const simbolos = await (await fetch('data/simbolos.json', { cache: 'no-store' })).json();
registrarColoresSimbolos(simbolos.colores);
// Versiones anteriores (antes.json, por clave), para ver antes y después.
const antes = await fetch('antes.json', { cache: 'no-store' }).then((r) => (r.ok ? r.json() : {}), () => ({}));

const h = (etiqueta, props = {}, ...hijos) => {
  const nodo = Object.assign(document.createElement(etiqueta), props);
  nodo.append(...hijos.flat(Infinity).filter(Boolean));
  return nodo;
};

// Cada obra: colección, clave, título y su foto de referencia.
const OBRAS = [
  ['programas', 'Deportivo', 'Deportivo · Monumental de River (desde arriba)', 'deportes/https___s3.amazonaws.com_arc-wordpress-client-uploads_infobae-wp_wp-content_uploads_2019_02_08155342_Galeria-cenital-River-Plate.avif'],
];

const rutaFoto = (a) => `referencias/${a.split('/').map(encodeURIComponent).join('/')}`;
const caja = (p, tema, opciones) => {
  const c = h('div', {}, simbolo(p, { ancho: 100, alto: 100, fijo: true, clase: 'tapa-grafica', ...opciones }));
  c.dataset.tema = tema;
  return c;
};

document.getElementById('obras').replaceChildren(...OBRAS.map(([coleccion, clave, titulo, foto]) => {
  const p = simbolos[coleccion]?.[clave] ?? simbolos.decadas[coleccion][clave];
  const { placa, aire, marco, ...sinFondo } = p;
  const viejo = antes[clave];
  return h('section', {}, h('h2', { textContent: titulo }), h('div', { className: 'fila' },
    h('div', { className: 'foto' }, h('img', { src: rutaFoto(foto), alt: '' })),
    viejo && h('div', { className: 'par' }, h('b', { textContent: 'Antes' }),
      caja({ ...viejo, placa, aire, marco }, 'claro', { margen: 8, superficie: 0.42 }), caja({ ...viejo, placa, aire, marco }, 'oscuro', { margen: 8, superficie: 0.42 })),
    h('div', { className: 'par' }, viejo && h('b', { textContent: 'Después' }),
      caja(sinFondo, 'claro', { margen: 2 }), caja(sinFondo, 'oscuro', { margen: 2 }),
      caja(p, 'claro', { margen: 8, superficie: 0.42 }), caja(p, 'oscuro', { margen: 8, superficie: 0.42 }))));
}));
