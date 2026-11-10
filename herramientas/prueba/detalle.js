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
  ['estilos', 'Streamline Moderne', 'Streamline Moderne · Edificio El Planeta', 'el planeta/Edificio_El_Planeta,_Atlántida.jpg'],
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

// Fondos a elegir para Streamline Moderne (Uruguay), cada uno en tapa clara y oscura.
const FONDOS = {
  'Rambla (hoy)': ['streamline-rambla', '#2f5f58', '#14302c', '#f4e1d8', '#f4e1d8'],
  'Celeste de la bandera': ['f-celeste', '#6f9fcf', '#1d3550', '#1f2a44', '#f4e1d8'],
  'Sol de Mayo': ['f-sol', '#d9a23a', '#4a3410', '#3a2410', '#f4e1d8'],
  'Mate y yerba': ['f-yerba', '#6f7f3c', '#252c13', '#f4e1d8', '#f4e1d8'],
  'Río color de león': ['f-rio', '#9c7650', '#2d2115', '#f4e1d8', '#f4e1d8'],
};
const extra = {};
for (const [id, c, o, mc, mo] of Object.values(FONDOS)) {
  extra[id] = { claro: c, oscuro: o };
  extra[`${id}-marco`] = { claro: mc, oscuro: mo };
}
registrarColoresSimbolos({ ...simbolos.colores, ...extra });
const sm = simbolos.estilos['Streamline Moderne'];
document.getElementById('obras').append(h('section', {}, h('h2', { textContent: 'Fondos para Streamline Moderne' }),
  h('div', { className: 'fila' }, ...Object.entries(FONDOS).map(([nombre, [id]]) => h('div', { className: 'par' },
    h('b', { textContent: nombre }),
    caja({ ...sm, placa: id, marco: `${id}-marco` }, 'claro', { margen: 8, superficie: 0.42 }),
    caja({ ...sm, placa: id, marco: `${id}-marco` }, 'oscuro', { margen: 8, superficie: 0.42 }))))));
