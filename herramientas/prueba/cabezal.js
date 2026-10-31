// Prueba del cabezal de los perfiles: carga la app real en marcos y le aplica cada variante encima.
// Cada ejemplo: ruta de la app, título, y dónde está su símbolo en simbolos.json.
import { simbolo } from './js/grafica.js';

const simbolos = await (await fetch('data/simbolos.json', { cache: 'no-store' })).json();

const EJEMPLOS = [
  ['programa/museo', 'Programa · Museo', ['programas', 'Museo']],
  ['estilo/brutalismo', 'Estilo · Brutalismo', ['estilos', 'Brutalismo']],
  ['decada/1950', 'Década · 1950', ['decadas', 'mundo', '1950']],
  ['programa/templo', 'Programa · Templo', ['programas', 'Templo']],
];

const VARIANTES = {
  A: 'A · color hasta pasar las flechas',
  B: 'B · color solo como título',
  C: 'C · blanco y negro',
};

// El estilo de cada variante, dentro del marco. --banda es el fondo y --detalle, el color de los textos y las flechas.
const BASE = `
  .banda-color { background: var(--banda); color: var(--detalle); margin: 0 calc(-1 * var(--margen, 0px)); padding: 18px var(--margen, 16px) 0; }
  .banda-color, .banda-color * { --tinta: var(--detalle); --tenue: var(--detalle); --filete: color-mix(in srgb, var(--detalle) 35%, transparent); }
  .banda-color a, .banda-color h2, .banda-color p, .banda-color dt, .banda-color dd, .banda-color span { color: var(--detalle) !important; }
  .banda-color .chip, .banda-color dd a { background: color-mix(in srgb, var(--detalle) 14%, transparent) !important; }
  .banda-color .banda-perfil { background: none; }
  .banda-color .separador-grafico rect, .banda-color .separador-grafico polygon { fill: var(--detalle) !important; }
  .banda-color .separador-grafico { margin-top: 0 !important; padding-bottom: 14px; }
  .banda-color .perfil-cabeza { display: flex; flex-direction: column; align-items: center; justify-content: flex-end; }
  .banda-color .perfil-simbolo { order: 2; font-size: 13px; padding: 4px 0 0; text-align: center; }
  .banda-color .banda-perfil { width: 100%; display: flex; justify-content: center; }
  .banda-color .banda-perfil svg { width: auto; height: 380px; max-width: 100%; }
  @media (max-width: 699px) {
    /* En el teléfono: texto, datos y, al final, el símbolo apoyado sobre las flechas. */
    .banda-color { display: flex; flex-direction: column; }
    .banda-color .perfil-arriba { display: contents; }
    .banda-color .perfil-texto { order: 1; }
    .banda-color .perfil-bloques { order: 2; }
    .banda-color .perfil-cabeza { order: 3; padding-top: 14px; }
    .banda-color .separador-grafico { order: 4; width: 100% !important; margin-left: 0 !important; }
  }
  @media (min-width: 700px) {
    .banda-color { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); column-gap: 32px; }
    .banda-color .perfil-arriba { display: contents; }
    .banda-color .perfil-texto { grid-column: 1; grid-row: 1; }
    .banda-color .perfil-bloques { grid-column: 1; grid-row: 2; }
    .banda-color .perfil-cabeza { grid-column: 2; grid-row: 1 / 3; align-self: end; padding: 0 !important; }
    .banda-color .separador-grafico { grid-column: 1 / -1; grid-row: 3; width: 100% !important; margin-left: 0 !important; }
  }
  .titulo-color.banda-color { grid-template-rows: auto auto; }
  .titulo-color.banda-color .perfil-cabeza { grid-row: 1; }
`;

function aplicar(doc, variante, placa, marco) {
  const arriba = doc.querySelector('.perfil-arriba');
  const bloques = doc.querySelector('.perfil-bloques');
  const flechas = doc.querySelector('.perfil-bloques + .separador-grafico');
  if (!arriba || doc.querySelector('.banda-color')) return !!arriba;
  const estilo = doc.createElement('style');
  estilo.textContent = BASE;
  doc.head.append(estilo);
  const banda = doc.createElement('div');
  banda.className = 'banda-color' + (variante === 'B' ? ' titulo-color' : '');
  banda.style.setProperty('--banda', variante === 'C' ? 'var(--tinta-fija, #1a1917)' : `var(--simbolo-${placa})`);
  banda.style.setProperty('--detalle', variante === 'C' ? '#f3f1ec' : `var(--simbolo-${marco})`);
  arriba.before(banda);
  if (variante === 'B') {
    // Solo el título y el símbolo en color; debajo, las flechas en color y el resto como siempre.
    banda.append(arriba, flechas);
  } else {
    banda.append(arriba, bloques, flechas);
  }
  return true;
}

function simboloGrande(doc, partitura) {
  const { placa, aire, marco, ...sin } = partitura;
  const nodo = simbolo(sin, { ancho: 600, alto: 420, margen: 0, sinFondo: true, superficie: 0.85 });
  // Recortado a lo que ocupa el dibujo, así los altos y angostos (el Seagram) crecen hasta el alto de la banda.
  const cabeza = doc.querySelector('.banda-perfil');
  if (!cabeza) return;
  cabeza.replaceChildren(doc.importNode(nodo, true));
  const dibujo = cabeza.querySelector('svg');
  requestAnimationFrame(() => {
    const caja = dibujo.getBBox();
    if (caja.width) dibujo.setAttribute('viewBox', `${caja.x} ${caja.y} ${caja.width} ${caja.height}`);
  });
}

function marcoApp(ruta, variante, partitura, tema, ancho, alto, escala) {
  const caja = document.createElement('div');
  caja.className = 'marco';
  caja.style.width = `${ancho * escala}px`;
  caja.style.height = `${alto * escala}px`;
  const f = document.createElement('iframe');
  f.width = ancho; f.height = alto;
  f.style.transform = `scale(${escala})`;
  f.src = `index-app.html#/${ruta}`;
  f.addEventListener('load', () => {
    const doc = f.contentDocument;
    doc.documentElement.dataset.tema = tema;
    const intentar = (n) => {
      if (aplicar(doc, variante, partitura.placa, partitura.marco)) simboloGrande(doc, partitura);
      else if (n > 0) setTimeout(() => intentar(n - 1), 150);
    };
    intentar(40);
  });
  caja.append(f);
  return caja;
}

function pintar(tema) {
  const raiz = document.getElementById('ejemplos');
  raiz.replaceChildren(...EJEMPLOS.map(([ruta, titulo, camino]) => {
    const partitura = camino.reduce((o, k) => o?.[k], simbolos);
    const seccion = document.createElement('section');
    const h = document.createElement('h2');
    h.textContent = titulo;
    const fila = document.createElement('div');
    fila.className = 'fila';
    for (const [clave, nombre] of Object.entries(VARIANTES)) {
      const fig = document.createElement('figure');
      const cap = document.createElement('figcaption');
      cap.textContent = nombre;
      fig.append(cap, marcoApp(ruta, clave, partitura, tema, 1200, 1000, 0.42));
      fila.append(fig);
    }
    const fig = document.createElement('figure');
    const cap = document.createElement('figcaption');
    cap.textContent = 'A · en el teléfono';
    fig.append(cap, marcoApp(ruta, 'A', partitura, tema, 390, 900, 0.55));
    fila.append(fig);
    seccion.append(h, fila);
    return seccion;
  }));
}

document.getElementById('claro').onclick = () => pintar('claro');
document.getElementById('oscuro').onclick = () => pintar('oscuro');
pintar('claro');
