import { simbolo, registrarColoresSimbolos } from './js/grafica.js';

const simbolos = await (await fetch('data/simbolos.json', { cache: 'no-store' })).json();
const html = await (await fetch('index-app.html', { cache: 'no-store' })).text();
const cargaApp = new DOMParser().parseFromString(html, 'text/html').getElementById('carga');
const svgB = await (await fetch('carga-b.svg.html', { cache: 'no-store' })).text();
const cargaB = cargaApp.cloneNode(true);
cargaB.querySelector('svg').outerHTML = svgB;
registrarColoresSimbolos(simbolos.colores);

const h = (etiqueta, props = {}, ...hijos) => {
  const nodo = document.createElement(etiqueta);
  for (const [clave, valor] of Object.entries(props)) {
    if (clave === 'dataset') Object.assign(nodo.dataset, valor);
    else nodo[clave] = valor;
  }
  nodo.append(...hijos.flat(Infinity).filter(Boolean));
  return nodo;
};

// Cada símbolo con foto de referencia. Las fotos se leen de referencias/, un enlace a
// ~/medianeras-originales/referencias/simbolos que crea servir.sh (no entra al repo).
const CON_FOTO = [
  ['estilos', 'Moderno', ['savoye/images.jpeg']],
  ['estilos', 'Arquitectura orgánica', ['guggenheim new york/guggenheim-model-6.jpg']],
  ['argentina', '1900', ['colon/Fachada_del_Teatro_Colón_en_Buenos_Aires,_Argentina.jpg']],
  ['argentina', '1990', ['biblioteca nacional/bibliotecanacionalcnm.jpg', 'biblioteca nacional/15998538130-Biblioteca-Nacional-773x458.jpg']],
  ['argentina', '1930', ['kavanagh/kava.webp', 'kavanagh/kavan.png']],
  ['argentina', '1940', ['casa puente/Screenshot 2026-10-18 at 02.14.53.png', 'casa puente/puente.avif']],
  ['argentina', '1960', ['banco de londres/londres.png']],
  ['argentina', '1950', ['casa curutchet/curut.png']],
  ['argentina', '1970', ['somisa/somisq.jpeg', 'somisa/somisa.webp']],
  ['argentina', '1980', ['recoleta/cultu reco.jpg']],
  ['argentina', '2000', ['puente de la mujer/mujer.jpg']],
  ['argentina', '2010', ['Centro Cultural Kirschner/1081612757_0_0_3000_2000_600x0_80_0_0_5ac5d6b0bad27a749eb428dada033483.jpg', 'Centro Cultural Kirschner/U7SKV43T23MD3XO27QZNIY5YRQ.avif', 'Centro Cultural Kirschner/Buenos_Aires_Centrum_Kirchner.jpg']],
  ['mundo', '1950', ['seagram/seagramexrt.webp', 'seagram/Seagram-Bldg.jpg']],
  ['mundo', '1970', ['pompidou/IMG_3603.jpeg', 'pompidou/av_19293.webp']],
  ['mundo', '1900', ['stoclet/stoclet.jpg']],
  ['mundo', '1910', ['la pedrera:casa mila/Casa_Milà,_general_view.jpg']],
  ['mundo', '1930', ['paimio/paimio.jpg']],
  ['mundo', '1940', ['eames/eames.jpeg']],
  ['mundo', '1990', ['bilbao guggenhiem/guggen.jpg']],
  ['mundo', '2000', ['St mary axe/790423.jpg']],
  ['mundo', '2010', ['CCTV/china.png']],
];
// ?solo=mundo-1950 muestra solo ese símbolo (sin la pantalla de carga).
const solo = new URLSearchParams(location.search).get('solo');
const elegidos = solo ? CON_FOTO.filter(([c, d]) => `${c}-${d}` === solo) : CON_FOTO;
const rutaFoto = (a) => `referencias/${a.split('/').map(encodeURIComponent).join('/')}`;

function foto(archivos) {
  if (!archivos.length) return h('div', { className: 'foto' }, h('p', { className: 'sin-foto', textContent: 'Sin foto de referencia.' }));
  return h('div', { className: 'foto' }, archivos.map((a) => h('img', { src: rutaFoto(a), alt: '' })), h('p', { textContent: archivos.join(' · ') }));
}

function panel(tema, partitura, decada, coleccion) {
  return h('div', { className: 'muestra', dataset: { tema } },
    simbolo(partitura, { ancho: 390, alto: 132 }),
    h('h3', { textContent: partitura.obra ?? decada }),
    h('p', { className: 'dato', textContent: coleccion === 'estilos' ? 'ESTILO' : `${decada}s · ${coleccion.toUpperCase()} · ${partitura.lugar} · ${partitura.anio}` }),
    tema === 'claro' && h('p', { className: 'nota', textContent: partitura.nota }));
}

function cargaPanel(tema, version) {
  const original = version === 'A' ? cargaApp : cargaB;
  const caja = h('div', { className: 'carga-demo' }, document.importNode(original, true));
  return h('div', { className: 'muestra', dataset: { tema } }, caja,
    h('h3', { textContent: 'Pantalla de carga' }),
    h('p', { className: 'dato', textContent: 'EN LA APP: SKYLINE «EL SIGLO»' }),
    h('button', { type: 'button', className: 'boton boton-chico repetir', textContent: 'Repetir animación',
      onclick: () => caja.replaceChildren(document.importNode(original, true)) }));
}

document.getElementById('filas').replaceChildren(...[
  !solo && h('div', { className: 'fila' }, foto(['skyline/depositphotos_58959203-stock-illustration-buenos-aires.jpg']), cargaPanel('claro', 'A'), cargaPanel('oscuro', 'A')),
  ...elegidos.map(([coleccion, decada, archivos]) => {
    const partitura = coleccion === 'estilos' ? simbolos.estilos[decada] : simbolos.decadas[coleccion][decada];
    return h('div', { className: 'fila' }, foto(archivos), panel('claro', partitura, decada, coleccion), panel('oscuro', partitura, decada, coleccion));
  }),
].filter(Boolean));
