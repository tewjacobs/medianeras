// Prueba de las décadas del inicio en grilla o en tira, con los datos y símbolos reales.
import { el } from './js/ui.js';
import { cargarDatos, partituraDe, colorPerfil, rutaPerfil } from './js/datos.js';
import { simbolo, simboloNeutro } from './js/grafica.js';
import { decadasConObras } from './js/filas.js';

const datos = await cargarDatos();
const tarjeta = ([decada, obras]) => {
  const color = colorPerfil('decada', decada, obras);
  const p = partituraDe(datos, 'decada', decada) ?? simboloNeutro(color);
  return el('a', { href: `../../www/index.html#${rutaPerfil('decada', decada).slice(1)}` },
    el('div', { class: `tapa marco-${color}` }, simbolo(p, { ancho: 100, alto: 100, margen: 8, fijo: true, superficie: 0.42, clase: 'tapa-grafica' })),
    el('div', { class: 'd-nombre' }, `${decada}s`),
    el('div', { class: 'd-cant' }, obras.length === 1 ? '1 obra' : `${obras.length} obras`));
};
const lista = decadasConObras(datos);
const tel = (clase) => el('div', { class: 'tel' }, el('h3', {}, 'Por década'), el('div', { class: clase }, lista.map(tarjeta)), el('div', { class: 'resto' }, 'lo que sigue del inicio'));
document.getElementById('pagina').append(
  el('figure', {}, el('figcaption', {}, 'A · Grilla de tres', el('small', {}, `${lista.length} décadas en ${Math.ceil(lista.length / 3)} filas`)), tel('d-grilla')),
  el('figure', {}, el('figcaption', {}, 'B · Tira deslizable', el('small', {}, 'una sola fila; se desliza con el dedo')), tel('d-tira')),
);
const tema = (t) => document.querySelectorAll('.tel').forEach((n) => { n.dataset.tema = t; });
document.getElementById('claro').onclick = () => tema('claro');
document.getElementById('oscuro').onclick = () => tema('oscuro');
tema(location.hash === '#oscuro' ? 'oscuro' : 'claro');
