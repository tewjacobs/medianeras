import { simbolo, registrarColoresSimbolos } from './js/grafica.js';

const simbolos = await (await fetch('data/simbolos.json', { cache: 'no-store' })).json();

const h = (etiqueta, props = {}, ...hijos) => {
  const nodo = Object.assign(document.createElement(etiqueta), props);
  nodo.append(...hijos.flat(Infinity).filter(Boolean));
  return nodo;
};

// Los símbolos con fondo y marco (las banderas no llevan marco).
const conMarco = [
  ...Object.entries(simbolos.decadas.mundo).map(([k, p]) => [`${p.obra} · ${k}s`, p]),
  ...Object.entries(simbolos.estilos).map(([k, p]) => [k, p]),
  ...Object.entries(simbolos.programas).map(([k, p]) => [k, p]),
].filter(([, p]) => p.placa && p.marco);

// El color invertido de cada fondo, en claro y en oscuro.
const invertir = (hex) => `#${(0xffffff ^ parseInt(hex.slice(1), 16)).toString(16).padStart(6, '0')}`;
const colores = { ...simbolos.colores };
conMarco.forEach(([, p]) => {
  const fondo = simbolos.colores[p.placa];
  colores[`inv-${p.placa}`] = { claro: invertir(fondo.claro), oscuro: invertir(fondo.oscuro) };
});
registrarColoresSimbolos(colores);

const tapa = (p, tema) => {
  const caja = h('div', {}, simbolo(p, { ancho: 100, alto: 100, margen: 8, fijo: true, superficie: 0.42, clase: 'tapa-grafica' }));
  caja.dataset.tema = tema;
  return caja;
};

document.getElementById('obras').replaceChildren(...conMarco.map(([nombre, p]) => {
  const invertido = { ...p, marco: `inv-${p.placa}` };
  return h('section', {}, h('h2', { textContent: nombre }), h('div', { className: 'fila' },
    h('div', { className: 'opcion' }, h('b', { textContent: 'Hoy · tinta' }), h('div', { className: 'par' }, tapa(p, 'claro'), tapa(p, 'oscuro'))),
    h('div', { className: 'opcion' }, h('b', { textContent: 'Invertido del fondo' }), h('div', { className: 'par' }, tapa(invertido, 'claro'), tapa(invertido, 'oscuro')))));
}));
