// Tema claro / oscuro / automático. En automático sigue lo que informa el navegador
// (que en Chrome puede ser distinto del modo del sistema: Chrome tiene su propio ajuste).

import { leerPreferencia, guardarPreferencia } from './plataforma/preferencias.js';
import { el, abrirHoja } from './ui.js';

export const OPCIONES_TEMA = [
  { valor: 'auto', nombre: 'Automático', detalle: 'Sigue al teléfono o al navegador' },
  { valor: 'claro', nombre: 'Claro', detalle: 'Papel arena' },
  { valor: 'oscuro', nombre: 'Oscuro', detalle: 'Noche azulada' },
];

const sistemaOscuro = window.matchMedia('(prefers-color-scheme: dark)');

export function temaElegido() {
  const valor = leerPreferencia('tema', 'auto');
  return OPCIONES_TEMA.some((o) => o.valor === valor) ? valor : 'auto';
}

export function aplicarTema(eleccion = temaElegido()) {
  const tema = eleccion === 'auto' ? (sistemaOscuro.matches ? 'oscuro' : 'claro') : eleccion;
  document.documentElement.dataset.tema = tema;
  // La barra de estado del iPhone toma el color del fondo
  const fondo = getComputedStyle(document.documentElement).getPropertyValue('--papel').trim();
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', fondo);
}

export function elegirTema(eleccion) {
  guardarPreferencia('tema', eleccion);
  aplicarTema(eleccion);
}

export function iniciarTema() {
  aplicarTema();
  sistemaOscuro.addEventListener('change', () => {
    if (temaElegido() === 'auto') aplicarTema('auto');
  });
}

export function abrirSelectorTema() {
  const actual = temaElegido();
  const opciones = OPCIONES_TEMA.map((o) => el('label', { class: 'opcion-tema' },
    el('input', {
      type: 'radio', name: 'tema', value: o.valor, checked: o.valor === actual,
      onchange: () => elegirTema(o.valor),
    }),
    el('span', {}, el('strong', {}, o.nombre), el('span', { class: 'tenue' }, o.detalle)),
  ));
  abrirHoja({ titulo: 'Apariencia', contenido: el('div', { class: 'opciones-tema', role: 'radiogroup' }, opciones) });
}
