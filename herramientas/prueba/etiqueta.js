// Prueba de la etiqueta "pintoresquista" / "neo": ficha y grilla con las obras reales, tres diseños.
// Todo se dibuja acá, sin tocar la app.
import { el, tapaObra } from './js/ui.js';
import { cargarDatos, colorMarco, rangoAnios } from './js/datos.js';

const datos = await cargarDatos();
const obra = (id) => datos.obras.find((o) => o.id === id);

// Estilo provisorio de cada obra con la etiqueta puesta (se decide casa por casa después).
const EJEMPLOS = [
  ['casa-tudor-de-florida', 'pintoresquista', 'Tudor'],
  ['casa-maria', 'pintoresquista', 'a decidir'],
  ['chalet-amarillo-de-florida', 'pintoresquista', 'a decidir'],
  ['trinity-church', 'neo', 'Gótico'],
  ['st-luke-liverpool', 'neo', 'Gótico'],
  ['alwyn-court', 'neo', 'Renacimiento francés'],
];

const TEXTOS = {
  pintoresquista: {
    nombre: 'Pintoresquista', corto: 'Pint.', letra: 'P',
    ayuda: 'Casa de barrio hecha para parecer una casa de campo europea: un chalet vasco, una casa tudor inglesa, una granja normanda. Estuvieron de moda en Buenos Aires entre los años 20 y 50. El estilo que figura es el de la casa imitada.',
    explica: 'Casa de ciudad o de barrio que copia el aire de una casa de campo de otro lugar: el chalet vasco, la casa tudor inglesa, la granja normanda. Fue muy común en Buenos Aires entre los años 20 y 50. El estilo es el de la casa copiada; la etiqueta dice que es una copia.',
    lista: 'Ver las 7 pintoresquistas',
  },
  neo: {
    nombre: 'Neo', corto: 'Neo', letra: 'N',
    ayuda: 'Obra hecha a propósito en un estilo de otra época, mucho después de que pasó: una iglesia gótica del siglo XIX, una casa colonial de 1930. El estilo que figura es el original; «neo» avisa que es una versión posterior.',
    explica: 'Obra que vuelve a un estilo de otra época, mucho después de que pasó: una iglesia gótica hecha en el siglo XIX, una casa colonial de los años 30. El estilo es el original; la etiqueta dice que es una vuelta.',
    lista: 'Ver todas las neo',
  },
};

const VARIANTES = [
  ['D · Letra grande', 'la P o la N junto al nombre. Pasá el mouse por la tapa: sube la palabra; pasalo por el «?»: se abre la explicación al costado', 'd'],
];

// Dónde cae la foto dentro del recuadro (entra entera: si es apaisada queda más baja; si es vertical, más angosta).
function ajustarAFoto(t, grande, nodo) {
  const img = t.querySelector('img:not(.con-encuadre)');
  if (!img) return;
  const apoyar = () => {
    const b = grande ? 0.07 : 0.09, lado = 1 - 2 * b, prop = img.naturalWidth / img.naturalHeight;
    const vert = prop > 1 ? (lado - lado / prop) / 2 : 0, horiz = prop < 1 ? (lado - lado * prop) / 2 : 0;
    nodo.style.top = `${(b + vert) * 100}%`; nodo.style.right = `${(b + horiz) * 100}%`;
  };
  if (img.complete && img.naturalWidth) apoyar(); else img.addEventListener('load', apoyar);
}

// La tarjetita que sube sobre la tapa al pasar el mouse (en la compu).
const desliza = (texto) => el('div', { class: 'desliza' }, el('b', {}, texto.nombre), el('span', { class: 'ayuda', tabindex: 0, 'aria-label': `Qué es ${texto.nombre.toLowerCase()}` }, '?'));
// La explicación, fuera de la tapa: se abre al pasar por el «?».
const globo = (texto) => el('div', { class: 'globo', role: 'tooltip' }, el('b', {}, texto.nombre), el('p', {}, texto.ayuda));

function tarjeta(v, o, tipo, grande) {
  const texto = TEXTOS[tipo];
  const t = tapaObra(o, { grande });
  if (v === 'b') {
    const isla = el('span', { class: 'isla' }, grande ? texto.nombre : texto.letra);
    t.append(isla);
    ajustarAFoto(t, grande, isla);
  }
  if (!grande) t.append(desliza(texto));
  return el('div', { class: `tarj tarj-${v}`, style: `--familia: var(--${colorMarco(o)})` },
    t,
    v === 'c' && el('div', { class: 'base' }, texto.nombre),
    !grande && globo(texto),
    !grande && el('div', { class: 'tarj-pie' }, el('span', {}, o.nombre), v === 'd' && el('b', { class: 'letra' }, texto.letra)));
}

const etiqueta = (v, nombre, onclick) => el('button', { class: `etq v-${v}`, onclick }, nombre);

function ficha(v, [id, tipo, estilo]) {
  const o = obra(id);
  const t = TEXTOS[tipo];
  const explica = el('div', { class: 'explica', hidden: true }, t.explica, el('a', { href: '#' }, `${t.lista} →`));
  const etq = etiqueta(v, t.nombre, () => { explica.hidden = !explica.hidden; });
  const autoria = [rangoAnios(o), ...(o.arquitectos ?? [])].filter(Boolean).join(' · ');
  return el('div', { style: `--familia: var(--${colorMarco(o)})` },
    el('div', { class: 'ficha-tapa' }, tarjeta(v, o, tipo, true)),
    el('div', { class: 'ficha' },
      el('h2', { class: 'ficha-titulo' }, o.nombre), v !== 'c' && etq, explica,
      autoria && el('p', { class: 'ficha-autoria' }, autoria),
      el('p', { class: 'estilo-linea' }, `Estilo: ${estilo}`)));
}

const grilla = (v) => el('div', { class: 'grilla' }, EJEMPLOS.map(([id, tipo]) => tarjeta(v, obra(id), tipo, false)));

document.getElementById('pagina').append(...VARIANTES.map(([titulo, nota, v]) =>
  el('figure', {}, el('figcaption', {}, titulo, el('small', {}, nota)),
    el('div', { class: 'tel' }, ficha(v, EJEMPLOS[0]), el('div', { class: 'separa' }), grilla(v), el('div', { class: 'separa' }), ficha(v, EJEMPLOS[3])))));

// En el iPhone no hay mouse: la letra lleva un «?» en la esquina y se toca para abrir o cerrar la explicación.
document.addEventListener('click', (e) => {
  const boton = document.body.classList.contains('tactil') && e.target.closest('.letra');
  document.querySelectorAll('.tarj.mostrar-globo').forEach((n) => { if (!boton || n !== boton.closest('.tarj')) n.classList.remove('mostrar-globo'); });
  if (boton) boton.closest('.tarj').classList.toggle('mostrar-globo');
});
const tactil = (si) => document.body.classList.toggle('tactil', si);
tactil(matchMedia('(hover: none)').matches || location.search.includes('iphone'));
document.getElementById('iphone').onclick = () => tactil(!document.body.classList.contains('tactil'));

const tema = (t) => document.querySelectorAll('.tel').forEach((n) => { n.dataset.tema = t; });
document.getElementById('claro').onclick = () => tema('claro');
document.getElementById('oscuro').onclick = () => tema('oscuro');
tema(location.hash === '#oscuro' ? 'oscuro' : 'claro');
// Para la captura: ?mostrar deja abierta la tarjetita de la primera obra de cada grilla.
if (location.search.includes('mostrar') && !document.body.classList.contains('tactil')) document.querySelectorAll('.grilla .tarj:first-child').forEach((n) => n.classList.add('mostrar', 'mostrar-globo'));
if (location.search.includes('abrir')) document.querySelector('.grilla .tarj')?.classList.add('mostrar-globo');
