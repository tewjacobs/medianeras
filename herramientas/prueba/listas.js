// Prueba de listas más cortas: índice de estilos, índice de arquitectos y panel de un país.
// Usa los datos reales de la app; todo se dibuja acá, sin tocar la app.
import { el } from './js/ui.js';

const cargar = async (r) => (await fetch(r, { cache: 'no-store' })).json();
const [crudo, perfiles] = await Promise.all([cargar('data/obras.json'), cargar('data/perfiles.json')]);
const obras = Array.isArray(crudo) ? crudo : crudo.obras;
const estilos = perfiles.estilos;

// Familias propuestas (5), con su época aproximada y el color de marco que ya usa su estilo principal.
const FAMILIAS = [
  { nombre: 'Gótico y neogótico', epoca: 'siglos XII–XIX', color: 'vino', estilos: ['Gótico perpendicular', 'Neogótico'] },
  { nombre: 'Historicismos', epoca: '1800–1940', color: 'teja', estilos: ['Historicismo', 'Academicismo', 'Beaux-Arts', 'Neorrenacimiento francés', 'Italianizante', 'Neocolonial', 'Barroco eduardiano', 'Pintoresquismo'] },
  { nombre: 'Art déco', epoca: '1920–1950', color: 'jade', estilos: ['Art déco', 'Streamline Moderne'] },
  { nombre: 'Moderno', epoca: '1920–1980', color: 'petroleo', estilos: ['Moderno', 'Racionalismo', 'Brutalismo', 'Moderno tardío', 'Arquitectura orgánica'] },
  { nombre: 'Contemporáneo', epoca: '1975–hoy', color: 'ciruela', estilos: ['Posmodernismo', 'Arquitectura contemporánea', 'Neofuturismo'] },
];
const familiaDe = (estilo) => FAMILIAS.find((f) => f.estilos.includes(estilo));
const cuenta = (estilo) => obras.filter((o) => o.estilo === estilo).length;
const ancestros = (e) => { const r = []; while (estilos[e]?.padre) { e = estilos[e].padre; r.push(e); } return r; };
const conHijos = (e) => obras.filter((o) => o.estilo && [o.estilo, ...ancestros(o.estilo)].includes(e)).length;
const orden = (a, b) => a.localeCompare(b, 'es');
const c = (color) => `--c: var(--${color})`;

const tel = (titulo, sub, ...hijos) => el('div', { class: 'tel' }, el('h3', {}, titulo), sub && el('p', { class: 'sub' }, sub), hijos);
const caso = (titulo, nota, nodo) => el('figure', {}, el('figcaption', {}, titulo, el('small', {}, nota)), nodo);

// ---- 1. Índice de estilos ----
function estilosHoy() {
  const usados = Object.keys(estilos).filter((e) => conHijos(e) > 0);
  const raices = usados.filter((e) => !estilos[e].padre || !usados.includes(estilos[e].padre)).sort(orden);
  const rama = (e, n) => [el('div', { class: 'renglon' }, el('span', { class: n ? 'hijo' : '', style: n ? `padding-left:${(n - 1) * 18}px` : null }, e), el('span', { class: 'cant' }, conHijos(e))),
    ...usados.filter((h) => estilos[h].padre === e).sort(orden).flatMap((h) => rama(h, n + 1))];
  return tel('Estilos', `${usados.length} en total`, raices.flatMap((r) => rama(r, 0)));
}
function estilosFamiliasA() {
  return tel('Estilos', '5 familias · 18 estilos', FAMILIAS.map((f) => {
    const usados = f.estilos.filter(cuenta);
    const total = usados.reduce((s, e) => s + cuenta(e), 0);
    return el('section', { class: 'familia', style: c(f.color) },
      el('div', { class: 'familia-cab' }, el('b', {}, f.nombre), el('span', { class: 'cant' }, total)),
      el('p', { class: 'familia-epoca' }, f.epoca),
      el('div', { class: 'chips' }, usados.sort((a, b) => cuenta(b) - cuenta(a)).map((e) =>
        el('a', { class: 'chip', href: '#' }, e, el('span', { class: 'cant' }, cuenta(e))))));
  }));
}
function estilosFamiliasB() {
  return tel('Estilos', '5 familias · tocá una para ver sus estilos', el('div', { class: 'tarjetas' }, FAMILIAS.map((f) => {
    const usados = f.estilos.filter(cuenta).sort((a, b) => cuenta(b) - cuenta(a));
    return el('a', { class: 'tarjeta', href: '#', style: `${c(f.color)}` },
      el('b', {}, f.nombre),
      el('small', {}, usados.join(' · ')),
      el('span', { class: 'num' }, usados.reduce((s, e) => s + cuenta(e), 0)));
  })));
}

// ---- 2. Índice de arquitectos ----
const arquitectos = [...new Set(obras.flatMap((o) => o.arquitectos ?? []))].sort(orden);
const obrasDe = (a) => obras.filter((o) => (o.arquitectos ?? []).includes(a));
const colorDe = (o) => familiaDe(o.estilo)?.color ?? 'cal';

function arqHoy() {
  return tel('Arquitectos', `${arquitectos.length} en total`, arquitectos.map((a) =>
    el('div', { class: 'renglon' }, el('span', {}, a), el('span', { class: 'cant' }, obrasDe(a).length))));
}
function arqFotos() {
  return tel('Arquitectos', `${arquitectos.length} · con la foto de su obra`, el('div', { class: 'grilla-arq' }, arquitectos.map((a) => {
    const o = obrasDe(a)[0];
    const foto = o.fotos?.[0]?.archivo;
    return el('a', { class: 'arq', href: '#', style: c(colorDe(o)) }, foto ? el('img', { src: foto, alt: ''}) : el('div', { class: 'sin' }), el('span', {}, a));
  })));
}
function arqFamilias() {
  return tel('Arquitectos', `${arquitectos.length} · por la familia de sus obras`, FAMILIAS.map((f) => {
    const suyos = arquitectos.filter((a) => obrasDe(a).some((o) => familiaDe(o.estilo) === f));
    if (!suyos.length) return null;
    return el('section', { class: 'familia', style: c(f.color) },
      el('div', { class: 'familia-cab' }, el('b', {}, f.nombre), el('span', { class: 'cant' }, suyos.length)),
      el('div', { class: 'nombres', style: 'margin-top:6px' }, suyos.map((a) => el('a', { href: '#', class: obrasDe(a).length > 1 ? 'varias' : '' }, a))));
  }));
}

// ---- 3. Panel de un país ----
const PAIS = 'Estados Unidos';
const delPais = obras.filter((o) => o.ubicacion?.pais === PAIS);
const FILAS = [
  ['Arquitectos', (o) => o.arquitectos ?? []], ['Estilos', (o) => (o.estilo ? [o.estilo] : [])],
  ['Décadas', (o) => { const a = o.anio_finalizacion ?? o.anio_proyecto ?? o.decada; return a ? [`${Math.floor(a / 10) * 10}s`] : []; }],
  ['Materiales', (o) => o.materiales ?? []], ['Programas', (o) => (o.programa ? [o.programa] : [])],
];
const conteo = (f) => { const m = new Map(); for (const o of delPais) for (const v of f(o)) m.set(v, (m.get(v) ?? 0) + 1); return [...m].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0]), 'es')); };
const chip = ([v, n]) => el('span', { class: 'chip' }, v, n > 1 && el('span', { class: 'cant' }, n));
const cabPais = (...x) => tel(PAIS, `${delPais.length} obras`, ...x, el('div', { class: 'simbolo-falso' }, 'símbolo y obras'));

function panelHoy() {
  return cabPais(el('dl', { class: 'tablero' }, FILAS.map(([t, f]) => [el('dt', {}, t), el('dd', {}, conteo(f).sort((a, b) => String(a[0]).localeCompare(String(b[0]), 'es')).map(chip))])));
}
function panelPrimeros() {
  return cabPais(el('dl', { class: 'tablero' }, FILAS.map(([t, f]) => {
    const todos = conteo(f);
    const dd = el('dd', {}, todos.slice(0, 3).map(chip));
    if (todos.length > 3) {
      const b = el('button', { class: 'mas', type: 'button', onclick: () => { b.replaceWith(...todos.slice(3).map(chip)); } }, `+${todos.length - 3}`);
      dd.append(b);
    }
    return [el('dt', {}, t), dd];
  })));
}
function panelCuentas() {
  const abierto = el('div', { class: 'abierto' });
  const botones = FILAS.map(([t, f]) => {
    const todos = conteo(f);
    const b = el('button', { type: 'button', 'aria-pressed': 'false', onclick: () => {
      const ya = b.getAttribute('aria-pressed') === 'true';
      botones.forEach((x) => x.setAttribute('aria-pressed', 'false'));
      abierto.replaceChildren();
      if (!ya) { b.setAttribute('aria-pressed', 'true'); abierto.append(el('div', { class: 'chips' }, todos.map(chip))); }
    } }, el('b', {}, todos.length), ` ${t.toLowerCase()}`);
    return b;
  });
  return cabPais(el('div', { class: 'cuentas' }, botones), abierto);
}

document.getElementById('pagina').append(
  el('h2', { class: 'prueba' }, '1. La lista de estilos'),
  el('p', { class: 'nota' }, 'Hoy es un árbol de 18 renglones. La idea: 5 familias grandes por época, con sus estilos adentro. En A se ven todos los estilos de una; en B, primero las familias (tarjetas) y al tocar, sus estilos. Ojo: Neogótico pasa de Historicismos a Gótico, y Barroco eduardiano y Pintoresquismo entran en Historicismos.'),
  el('div', { class: 'fila' },
    caso('Hoy', 'árbol con sangrías', estilosHoy()),
    caso('A · Familias con sus estilos', 'cada familia con su color', estilosFamiliasA()),
    caso('B · Tarjetas de familia', 'un paso más, pero entra en una pantalla', estilosFamiliasB())),
  el('h2', { class: 'prueba' }, '2. La lista de arquitectos'),
  el('p', { class: 'nota' }, `Hoy son ${arquitectos.length} renglones, casi todos con un «1». En A, cada arquitecto con la foto de su obra (tres por fila, se reconoce de un vistazo). En B, agrupados por la familia de sus obras, en dos columnas (en negrita, los que tienen más de una).`),
  el('div', { class: 'fila' },
    caso('Hoy', 'un renglón por arquitecto', arqHoy()),
    caso('A · Con la foto de su obra', 'grilla de 3', arqFotos()),
    caso('B · Por familia, en dos columnas', 'más corto, sin fotos', arqFamilias())),
  el('h2', { class: 'prueba' }, `3. El panel de un país (${PAIS})`),
  el('p', { class: 'nota' }, 'Hoy muestra todos los chips de todo y empuja las obras muy abajo. En A, los 3 más repetidos de cada fila y un «+N» para ver el resto. En B, una sola fila de cuentas; al tocar una se abre esa lista. Lo mismo serviría para estilos, arquitectos y décadas.'),
  el('div', { class: 'fila' },
    caso('Hoy', 'todo abierto', panelHoy()),
    caso('A · Los 3 primeros y «+N»', 'ordenados por cantidad', panelPrimeros()),
    caso('B · Solo cuentas, se abren al tocar', 'lo más corto', panelCuentas())),
);

const tema = (t) => document.querySelectorAll('.tel').forEach((n) => { n.dataset.tema = t; });
document.getElementById('claro').onclick = () => tema('claro');
document.getElementById('oscuro').onclick = () => tema('oscuro');
tema(location.hash === '#oscuro' ? 'oscuro' : 'claro');
