import { simbolo, simboloNeutro, registrarColoresSimbolos } from './js/grafica.js';

// Tres maneras de ordenar el índice de estilos, con los datos reales. ?tema=oscuro para verlo en oscuro.
const [simbolos, perfiles, obras] = await Promise.all(['simbolos', 'perfiles', 'obras'].map(async (n) =>
  (await fetch(`data/${n}.json`, { cache: 'no-store' })).json()));
registrarColoresSimbolos(simbolos.colores);
const tema = new URLSearchParams(location.search).get('tema') === 'oscuro' ? 'oscuro' : 'claro';
document.documentElement.dataset.tema = tema;

const h = (etiqueta, props = {}, ...hijos) => {
  const nodo = Object.assign(document.createElement(etiqueta), props);
  nodo.append(...hijos.flat(Infinity).filter(Boolean));
  return nodo;
};

const estilos = perfiles.estilos;
const lista = Array.isArray(obras) ? obras : obras.obras;
const ancestros = (e) => { const r = [e]; while (estilos[r.at(-1)]?.padre) r.push(estilos[r.at(-1)].padre); return r; };
const cantidad = (e) => lista.filter((o) => o.estilo && ancestros(o.estilo).includes(e)).length;
const color = (e) => ancestros(e).map((a) => estilos[a]?.color).find(Boolean) ?? 'petroleo';
const hijos = (e) => Object.keys(estilos).filter((h) => estilos[h].padre === e).sort((a, b) => a.localeCompare(b, 'es'));
const raices = Object.keys(estilos).filter((e) => !estilos[e].padre).sort((a, b) => a.localeCompare(b, 'es'));
const rama = (e) => [e, ...hijos(e).flatMap(rama)];

const dibujo = (e, lado) => simbolo(simbolos.estilos?.[e] ?? simboloNeutro(color(e)),
  { ancho: lado, alto: lado, margen: Math.round(lado * 0.08), fijo: true, superficie: 0.42, clase: 'tapa-grafica' });
const tapa = (e) => h('a', { className: 'ix-ficha' + (cantidad(e) ? '' : ' sin-obras') }, h('div', { className: 'caja' + (simbolos.estilos?.[e] ? '' : ' sin-simbolo') }, dibujo(e, 100)),
  h('span', { className: 'nombre', textContent: e }), h('span', { className: 'cuenta', textContent: `${cantidad(e)} obra${cantidad(e) === 1 ? "" : "s"}` }));


// Familias amplias (propuesta; si se elige, se suma a perfiles.json). Cada una: nombre, color, estilos en orden.
const SEIS = [
  ['Del gótico al barroco', 'vino', ['Gótico', 'Gótico perpendicular', 'Tudor', 'Renacimiento francés', 'Colonial', 'Barroco jesuítico']],
  ['Siglo XIX y Belle Époque', 'teja', ['Neoclásico', 'Historicismo', 'Italianizante', 'Neorrománico', 'Neobizantino', 'Neomudéjar', 'Neoegipcio', 'Eclecticismo', 'Academicismo', 'Beaux-Arts', 'Barroco eduardiano', 'Art nouveau', 'Modernismo catalán', 'Secesión vienesa', 'Liberty']],
  ['Casas pintorescas', 'oliva', ['Pintoresquismo', 'Estilo Mar del Plata', 'Chalet californiano']],
  ['Moderno', 'petroleo', ['Art déco', 'Streamline Moderne', 'Expresionismo', 'Moderno', 'Racionalismo', 'Estilo internacional', 'Arquitectura orgánica', 'Brutalismo', 'Moderno tardío', 'High-tech']],
  ['Contemporáneo', 'niebla', ['Posmodernismo', 'Arquitectura contemporánea', 'Neofuturismo', 'Minimalismo']],
];
const CUATRO = [
  ['Antes de 1800', 'vino', SEIS[0][2]],
  ['Siglo XIX y Belle Époque', 'teja', [...SEIS[1][2], ...SEIS[2][2]]],
  ['Moderno', 'petroleo', SEIS[3][2]],
  ['Contemporáneo', 'niebla', SEIS[4][2]],
];
for (const familias of [SEIS, CUATRO]) {
  const sueltos = Object.keys(estilos).filter((e) => !familias.some(([, , l]) => l.includes(e)));
  if (sueltos.length) console.warn('Sin familia:', sueltos);
}
const opcion = (familias) => () => familias.map(([n, c, l]) => h('section', { className: 'familia', style: `--fam: var(--${c})` },
  h('h3', {}, n, h('span', { className: 'cuenta-familia', textContent: ` · ${l.length} estilos` })),
  h('div', { className: 'ix-grilla' }, l.filter((e) => estilos[e]).map(tapa))));

document.getElementById('opciones').replaceChildren(
  ...[['A1 · Cinco familias', opcion(SEIS)], ['A2 · Cuatro familias', opcion(CUATRO)]]
    .map(([t, f]) => h('div', { className: 'telefono' }, h('h2', { textContent: t }), h('div', { className: 'pantalla' }, h('h1', { textContent: 'Estilos' }), f()))));
