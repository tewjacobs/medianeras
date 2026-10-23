// Gráfica de líneas: patrones SVG generados por código, tranquilos y de un solo color.
// Cada dibujo sale de una semilla de texto ("arquitecto:Frank Lloyd Wright"), así que
// el mismo perfil da siempre el mismo dibujo. Los colores son variables CSS del tema:
// al cambiar entre claro y oscuro, los dibujos cambian solos.
//
// Truco de las rayas paralelas: un mismo trazado se dibuja varias veces, del trazo más
// grueso al más fino, alternando el color de la raya y el del fondo. Lo que se ve son rayas
// finas y paralelas alrededor de cualquier curva (arco, U, S).

const NS = 'http://www.w3.org/2000/svg';

export const VARIANTES = ['arcos', 'abanico', 'cinta', 'ondas'];

// ---- Semilla y azar estable ----

// FNV-1a de 32 bits.
export function hashTexto(texto) {
  let h = 0x811c9dc5;
  for (const c of String(texto)) {
    h ^= c.codePointAt(0);
    h = Math.imul(h, 0x01000193);
  }
  return h >>> 0;
}

// mulberry32: números entre 0 y 1, siempre los mismos para la misma semilla.
function azar(semilla) {
  let a = hashTexto(semilla);
  const r = () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  r.entre = (min, max) => min + r() * (max - min);
  r.entero = (min, max) => Math.floor(r.entre(min, max + 1));
  r.elegir = (lista) => lista[Math.floor(r() * lista.length)];
  return r;
}

// ---- SVG ----

let contadorIds = 0;

export function svg(etiqueta, atributos = {}, ...hijos) {
  const nodo = document.createElementNS(NS, etiqueta);
  for (const [clave, valor] of Object.entries(atributos)) {
    if (valor == null) continue;
    if (clave === 'estilo') for (const [prop, v] of Object.entries(valor)) nodo.style.setProperty(prop, v);
    else nodo.setAttribute(clave, valor);
  }
  for (const hijo of hijos.flat(Infinity)) if (hijo) nodo.append(hijo);
  return nodo;
}

const n = (x) => Math.round(x * 100) / 100;

function recorte(...formas) {
  const id = `grafica-${++contadorIds}`;
  return { id, nodo: svg('clipPath', { id }, formas) };
}

// Rayas paralelas alrededor del trazado `d`: la central y `anillos` a cada lado,
// de grosor `trazo`, cada `paso`. `acento` pinta la raya central de otro color.
function rayas(d, { anillos, trazo, paso, linea, fondo, acento, punta = 'butt' }) {
  const trazos = [];
  const trazado = (ancho, tono) => svg('path', {
    d, fill: 'none', 'stroke-width': n(ancho), 'stroke-linecap': punta, 'stroke-linejoin': 'round', estilo: { stroke: tono },
  });
  for (let k = anillos; k >= 0; k--) {
    trazos.push(trazado(2 * k * paso + trazo, k === 0 && acento ? acento : linea));
    if (k > 0) trazos.push(trazado(2 * k * paso - trazo, fondo));
  }
  return svg('g', {}, trazos);
}

// ---- Variantes ----
// Cada una recibe el azar, el tamaño y la paleta { fondo, tono(p) }: tono(p) mezcla el
// color de la familia con el fondo (p = 100: color pleno; p bajo: casi el fondo).

// ARCOS: U concéntricas alrededor de un segmento con punta redonda.
function arcos(r, W, H, { fondo, tono }) {
  const paso = Math.min(W, H) * r.entre(0.055, 0.075);
  const anillos = r.entero(2, 4);
  const orientacion = r.elegir(['arriba', 'abajo', 'izquierda', 'derecha']);
  const fuera = Math.max(W, H);
  const t = r.entre(0.2, 0.8);
  const hondo = r.entre(0.35, 0.65);
  const d = {
    arriba: `M${n(W * t)} ${-fuera}V${n(H * hondo)}`,
    abajo: `M${n(W * t)} ${H + fuera}V${n(H * (1 - hondo))}`,
    izquierda: `M${-fuera} ${n(H * t)}H${n(W * hondo * 0.6)}`,
    derecha: `M${W + fuera} ${n(H * t)}H${n(W - W * hondo * 0.6)}`,
  }[orientacion];
  return rayas(d, { anillos, trazo: paso * 0.24, paso, linea: tono(70), fondo, punta: 'round' });
}

// ABANICO: líneas finas que convergen hacia un punto fuera de un círculo.
function abanico(r, W, H, { tono }) {
  const R = Math.min(W, H) * r.entre(0.34, 0.44);
  const cx = W * r.entre(0.2, 0.8);
  const cy = H / 2;
  const sentido = r() < 0.5 ? 1 : -1;
  const distancia = R * r.entre(1.6, 2.6);
  const px = cx + R * r.entre(-0.5, 0.5);
  const py = cy + sentido * distancia;
  const centro = Math.atan2(cy - py, cx - px);
  const apertura = Math.asin(Math.min(0.99, R / Math.hypot(cx - px, cy - py)));
  const cuantas = r.entero(9, 13);
  const largo = distancia + R * 2;
  const clip = recorte(svg('circle', { cx: n(cx), cy: n(cy), r: n(R) }));
  const lineas = [];
  for (let i = 0; i < cuantas; i++) {
    const a = centro - apertura + (2 * apertura * (i + 0.5)) / cuantas;
    lineas.push(svg('path', {
      d: `M${n(px)} ${n(py)}L${n(px + largo * Math.cos(a))} ${n(py + largo * Math.sin(a))}`,
      fill: 'none', 'stroke-width': n(R * 0.035), estilo: { stroke: tono(70) },
    }));
  }
  return [svg('defs', {}, clip.nodo), svg('g', { 'clip-path': `url(#${clip.id})` }, lineas)];
}

// CINTA: un haz de pocas rayas paralelas que cruza en S; como mucho, una de otro color.
function cinta(r, W, H, { fondo, tono, acento }) {
  const paso = H * r.entre(0.05, 0.07);
  const anillos = r.entero(2, 3);
  const y1 = H * r.entre(0.2, 0.4);
  const y2 = H * r.entre(0.6, 0.8);
  const [ya, yb] = r() < 0.5 ? [y1, y2] : [y2, y1];
  const d = `M${n(-W * 0.2)} ${n(ya)}C${n(W * r.entre(0.3, 0.5))} ${n(ya)} ${n(W * r.entre(0.5, 0.7))} ${n(yb)} ${n(W * 1.2)} ${n(yb)}`;
  return rayas(d, { anillos, trazo: paso * 0.24, paso, linea: tono(70), fondo, acento });
}

// ONDAS: rayas horizontales finas con una loma suave. Con `lineas`, es un separador.
function ondas(r, W, H, { fondo, tono, lineas }) {
  const separador = lineas != null;
  const paso = separador ? H / (lineas * 2 + 2) : H * r.entre(0.07, 0.1);
  const anillos = separador ? Math.floor(lineas / 2) : Math.ceil(H / (2 * paso)) + 2;
  const yc = separador ? H / 2 + paso * 0.8 : H * r.entre(0.45, 0.6);
  const x0 = W * r.entre(0.2, 0.8);
  const s = separador ? paso * r.entre(5, 8) : W * r.entre(0.1, 0.18);
  const A = separador ? paso * 1.6 : H * r.entre(0.12, 0.22);
  const d = `M${n(-W * 0.2)} ${n(yc)}H${n(x0 - s)}C${n(x0 - s / 2)} ${n(yc)} ${n(x0 - s / 2)} ${n(yc - A)} ${n(x0)} ${n(yc - A)}`
    + `C${n(x0 + s / 2)} ${n(yc - A)} ${n(x0 + s / 2)} ${n(yc)} ${n(x0 + s)} ${n(yc)}H${n(W * 1.2)}`;
  return rayas(d, { anillos, trazo: separador ? 1 : paso * 0.2, paso, linea: tono(separador ? 100 : 65), fondo });
}

const DIBUJOS = { arcos, abanico, cinta, ondas };

// ---- API ----

// `familia`: un color de marco (petroleo, follaje, cielo, mar) o cualquier color CSS.
// `fondo`: color de fondo del dibujo. Líneas y formas son mezclas de la familia con el fondo.
// `acento`: en la cinta, la raya central va en rojo.
export function patron(semilla, {
  variante, ancho = 400, alto = 112, familia = 'petroleo', fondo = 'var(--papel)', acento = false, lineas = null, clase = 'grafica',
} = {}) {
  const r = azar(semilla);
  const elegida = DIBUJOS[variante] ? variante : r.elegir(VARIANTES);
  const color = /^[a-z]+$/.test(familia) ? `var(--${familia})` : familia;
  const tono = (p) => (p >= 100 ? color : `color-mix(in srgb, ${color} ${p}%, ${fondo})`);
  const acentoColor = acento ? `color-mix(in srgb, var(--rojo) 75%, ${fondo})` : null;
  return svg('svg', {
    class: `${clase} grafica-${elegida}`, viewBox: `0 0 ${n(ancho)} ${n(alto)}`, preserveAspectRatio: 'xMidYMid slice',
    'aria-hidden': 'true', focusable: 'false',
  },
  svg('rect', { x: -1, y: -1, width: ancho + 2, height: alto + 2, estilo: { fill: fondo } }),
  DIBUJOS[elegida](r, ancho, alto, { fondo, tono, lineas, acento: acentoColor }));
}

// Separador entre bloques grandes: tres rayas finas con una loma.
export function separador(semilla, ancho = 360) {
  return patron(semilla, {
    variante: 'ondas', ancho, alto: 14, lineas: 3,
    familia: 'color-mix(in srgb, var(--tinta) 28%, var(--papel))', clase: 'separador-grafico',
  });
}

// ---- Logo ----

// Lanzas de jagten: las luces encendidas de la mitad de arriba del Seagram (símbolo de la década
// de 1950), cada tramo hecho lanza, sobre el vidrio oscuro. Colores fijos (--logo-*), grilla de 48 × 48.
// Cada lanza: [desde, punta, altura]; asta fina y punta de hoja (rombo largo) de 5 de largo.
const LANZAS = [[33.6, 40.6, 6.75], [29.3, 36.3, 9.75], [25, 32, 12.75], [27.9, 36.2, 15.75], [25, 33.4, 18.75],
  [16.3, 23.3, 21.75], [30.7, 40.6, 21.75], [23.5, 30.5, 24.75], [9.1, 16.1, 27.75], [23.5, 33.4, 27.75], [13.5, 29, 30.75],
  [7.7, 20.4, 33.75], [19.2, 34.8, 36.75], [22.1, 40.6, 39.75], [23.5, 30.5, 42.75]];

export function logo({ clase = 'logo-simbolo' } = {}) {
  const fill = { fill: 'var(--logo-luz)' };
  return svg('svg', { class: clase, viewBox: '0 0 48 48', 'aria-hidden': 'true', focusable: 'false' },
    svg('rect', { width: 48, height: 48, estilo: { fill: 'var(--logo-torre)' } }),
    ...LANZAS.flatMap(([x, punta, y]) => [
      svg('rect', { x, y: y - 0.3, width: n(punta - x - 4.5), height: 0.6, estilo: fill }),
      svg('polygon', { points: `${n(punta - 5)},${y} ${n(punta - 3.4)},${n(y - 0.9)} ${punta},${y} ${n(punta - 3.4)},${n(y + 0.9)}`, estilo: fill }),
    ]));
}

// ---- Símbolos de perfil ----
//
// Un símbolo es una "partitura" de líneas paralelas (data/simbolos.json, formato en el README).
// Cada línea es un texto con tramos "color largo" separados por comas:
//   "celeste 17, sol 6, celeste 17"
//   "(fachada 1, vidrio 0.6) x12"   repite el grupo 12 veces
//   "- 4"                          tramo vacío (deja ver el fondo)
//   "… celeste 40 …"               los "…" estiran el primer o el último tramo hasta el borde
// Los colores son los del tema (tinta, papel, rojo, petroleo, follaje, cielo, mar, tenue)
// o los definidos en "colores" del mismo archivo, con un valor para claro y otro para oscuro.

export const COLORES_TEMA = ['tinta', 'papel', 'papel-2', 'tenue', 'filete', 'rojo', 'petroleo', 'follaje', 'cielo', 'mar'];
const coloresPropios = new Set();

function colorCss(nombre) {
  if (COLORES_TEMA.includes(nombre)) return `var(--${nombre})`;
  if (!coloresPropios.has(nombre)) console.warn(`Símbolo: el color "${nombre}" no está en "colores" de simbolos.json`);
  return `var(--simbolo-${nombre}, var(--tinta))`;
}

// Crea (o actualiza) una hoja de estilos con los colores propios de los símbolos, uno por tema.
export function registrarColoresSimbolos(colores = {}) {
  for (const nombre of Object.keys(colores)) coloresPropios.add(nombre);
  const regla = (tema) => Object.entries(colores)
    .map(([nombre, valor]) => `--simbolo-${nombre}: ${typeof valor === 'string' ? valor : valor[tema]};`).join(' ');
  let hoja = document.getElementById('colores-simbolos');
  if (!hoja) {
    hoja = document.createElement('style');
    hoja.id = 'colores-simbolos';
    document.head.append(hoja);
  }
  hoja.textContent = `:root, [data-tema="claro"] { ${regla('claro')} } [data-tema="oscuro"] { ${regla('oscuro')} }`;
}

export function leerLinea(texto) {
  let t = String(texto).trim();
  const antes = /^(…|\.\.\.)/.test(t);
  const despues = /(…|\.\.\.)$/.test(t);
  t = t.replace(/^(…|\.\.\.)|(…|\.\.\.)$/g, '');
  t = t.replace(/\(([^()]*)\)\s*[x×]\s*(\d+)/g, (_, grupo, veces) => Array(Number(veces)).fill(grupo).join(','));
  const tramos = t.split(',').map((x) => x.trim()).filter(Boolean).map((x) => {
    const m = x.match(/^(\S+)\s+(\d+(?:\.\d+)?)$/);
    if (!m) throw new Error(`Tramo mal escrito: "${x}" (se espera "color largo")`);
    return { color: m[1], largo: Number(m[2]) };
  });
  return { antes, despues, tramos };
}

// Símbolo neutro para los perfiles que no tienen uno propio: una sola línea fina, de borde a
// borde, en el color de la familia, en una banda baja.
export function simboloNeutro(familia = 'petroleo') {
  return { direccion: 'horizontal', alto: 48, escala: 0.1, lineas: [`… ${familia} 10 …`] };
}

// `alto` de la banda: el de la partitura si lo trae (los símbolos verticales suelen pedir más).
// `escala` (de la partitura): achica el dibujo dentro de la banda; 1 es lo más grande que entra.
// `placa` (de la partitura): color de un rectángulo detrás del dibujo, para las banderas.
// `arcos` (de la partitura): líneas curvas paralelas, para lo que no se puede dibujar recto
//   (el arco de un puente). Cada arco: { color, desde, hasta, base, flecha, lineas }, en las
//   mismas unidades que los tramos; `base` es el número de línea donde apoya y `flecha` cuánto sube.
//   Con `relleno: true` el arco es una figura llena (la parte de arriba de un portal) que apoya
//   en el borde de arriba de la línea `base`.
// `anio` (0 a 9): debajo del dibujo, diez marcas, una por año; la de ese año en rojo.
// `fijo`: usar el alto pedido aunque la partitura traiga otro (las tapas son cuadradas).
// `sinFondo`: sin el rectángulo de fondo (para poner varios símbolos juntos, como en el skyline).
export function simbolo(partitura, { ancho = 400, alto: altoBanda = 132, margen = 16, anio = null, fijo = false, sinFondo = false, clase = 'grafica simbolo' } = {}) {
  const alto = fijo ? altoBanda : (partitura.alto ?? altoBanda);
  const vertical = partitura.direccion === 'vertical';
  const grosor = partitura.grosor ?? 1;
  const separacion = partitura.separacion ?? 1;
  const lineas = (partitura.lineas ?? []).map(leerLinea);
  const largoDe = (linea) => linea.tramos.reduce((suma, t) => suma + t.largo, 0);
  const largo = Math.max(1, partitura.largo ?? 0, ...lineas.map(largoDe));
  const travesia = lineas.length * grosor + Math.max(0, lineas.length - 1) * separacion;
  const conAnio = Number.isInteger(anio);
  const lugarAnio = conAnio ? 18 : 0;

  // Escala: que entre en la banda, en las dos direcciones.
  const largoDisponible = (vertical ? alto - lugarAnio : ancho) - 2 * margen;
  const travesiaDisponible = (vertical ? ancho : alto - lugarAnio) - 2 * margen;
  const escala = Math.min(largoDisponible / largo, travesiaDisponible / Math.max(travesia, 1)) * (partitura.escala ?? 1);
  const bordeLargo = vertical ? alto : ancho;
  const inicioLargo = ((vertical ? alto - lugarAnio : ancho) - largo * escala) / 2;
  const inicioTravesia = ((vertical ? ancho : alto - lugarAnio) - travesia * escala) / 2;
  const alinear = partitura.alinear ?? 'inicio';

  const rects = [];
  lineas.forEach((linea, i) => {
    const propio = largoDe(linea);
    const corrimiento = alinear === 'centro' ? (largo - propio) / 2 : alinear === 'fin' ? largo - propio : 0;
    let a = inicioLargo + corrimiento * escala;
    const b = inicioTravesia + i * (grosor + separacion) * escala;
    linea.tramos.forEach((tramo, k) => {
      let desde = a;
      let hasta = a + tramo.largo * escala;
      a = hasta;
      if (k === 0 && linea.antes) desde = 0;
      if (k === linea.tramos.length - 1 && linea.despues) hasta = bordeLargo;
      if (tramo.color === '-') return;
      // Sin separación, cada línea pisa apenas la siguiente: así no quedan juntas finas entre filas.
      const solape = separacion === 0 ? 0.6 : 0;
      const [x, y, w, h] = vertical ? [b, desde, grosor * escala + solape, hasta - desde] : [desde, b, hasta - desde, grosor * escala + solape];
      rects.push(svg('rect', { x: n(x), y: n(y), width: n(w), height: n(h), estilo: { fill: colorCss(tramo.color) } }));
    });
  });

  // Arcos: semielipses paralelas; cada una más angosta y más baja que la anterior.
  const paso = (grosor + separacion);
  const punto = (u, v) => (vertical
    ? [inicioTravesia + v * escala, inicioLargo + u * escala]
    : [inicioLargo + u * escala, inicioTravesia + v * escala]);
  const curvas = (partitura.arcos ?? []).flatMap((arco) => (arco.relleno ? [arcoLleno(arco)] : Array.from({ length: arco.lineas ?? 1 }, (_, k) => {
    const desde = arco.desde + k * paso;
    const hasta = arco.hasta - k * paso;
    const flecha = arco.flecha - k * paso;
    const base = arco.base * paso + grosor / 2;
    const [x0, y0] = punto(desde, base);
    const [x1] = punto(hasta, base);
    return svg('path', {
      d: `M${n(x0)} ${n(y0)}A${n((x1 - x0) / 2)} ${n(flecha * escala)} 0 0 1 ${n(x1)} ${n(y0)}`,
      fill: 'none', 'stroke-width': n(grosor * escala), estilo: { stroke: colorCss(arco.color) },
    });
  })));
  function arcoLleno(arco) {
    const [x0, y0] = punto(arco.desde, arco.base * paso);
    const [x1] = punto(arco.hasta, arco.base * paso);
    return svg('path', {
      d: `M${n(x0)} ${n(y0)}A${n((x1 - x0) / 2)} ${n(arco.flecha * escala)} 0 0 1 ${n(x1)} ${n(y0)}Z`,
      estilo: { fill: colorCss(arco.color) },
    });
  }

  // Caja del dibujo (sin los tramos estirados hasta el borde).
  const caja = vertical
    ? { x: inicioTravesia, y: inicioLargo, w: travesia * escala, h: largo * escala }
    : { x: inicioLargo, y: inicioTravesia, w: largo * escala, h: travesia * escala };

  const placa = partitura.placa && svg('rect', {
    x: n(caja.x - 1.5 * escala), y: n(caja.y - 1.5 * escala), width: n(caja.w + 3 * escala), height: n(caja.h + 3 * escala),
    estilo: { fill: colorCss(partitura.placa) },
  });

  const marcas = [];
  if (conAnio) {
    const ancho10 = caja.w / 10;
    for (let k = 0; k < 10; k++) {
      const elegido = k === anio;
      marcas.push(svg('rect', {
        x: n(caja.x + k * ancho10 + ancho10 * 0.15), y: n(caja.y + caja.h + (partitura.placa ? 1.5 * escala : 0) + 9),
        width: n(ancho10 * 0.7), height: elegido ? 5 : 2.5,
        estilo: { fill: elegido ? 'var(--rojo)' : 'var(--filete)' },
      }));
    }
  }

  return svg('svg', { class: clase, viewBox: `0 0 ${n(ancho)} ${n(alto)}`, preserveAspectRatio: 'xMidYMid meet', 'aria-hidden': 'true', focusable: 'false' },
    !sinFondo && svg('rect', { x: 0, y: 0, width: ancho, height: alto, estilo: { fill: colorCss(partitura.fondo ?? 'papel') } }),
    placa, rects, curvas, marcas);
}

// Ancho y alto del dibujo de una partitura, en sus unidades (sin márgenes ni tramos estirados).
export function medidasSimbolo(partitura) {
  const lineas = (partitura.lineas ?? []).map(leerLinea);
  const largo = Math.max(1, partitura.largo ?? 0, ...lineas.map((l) => l.tramos.reduce((a, t) => a + t.largo, 0)));
  const grosor = partitura.grosor ?? 1;
  const separacion = partitura.separacion ?? 1;
  const travesia = lineas.length * grosor + Math.max(0, lineas.length - 1) * separacion;
  return partitura.direccion === 'vertical' ? { ancho: travesia, alto: largo } : { ancho: largo, alto: travesia };
}

// Skyline: varios símbolos uno al lado del otro sobre una misma línea de suelo. Cada edificio
// es { partitura, altura } con la altura en proporción al alto total (0 a 1). Cada uno queda en
// su propio <svg> con la clase "edificio", --i (su orden) y --filas (sus líneas), para animarlos.
export function skyline(edificios, { alto = 100, separacion = 3, suelo = 2, clase = 'skyline' } = {}) {
  let x = 0;
  const piezas = edificios.map(({ partitura, altura }, i) => {
    const m = medidasSimbolo(partitura);
    const h = altura * (alto - suelo);
    const w = h * (m.ancho / m.alto);
    const pieza = simbolo(partitura, { ancho: w, alto: h, margen: 0, fijo: true, sinFondo: true, clase: 'edificio' });
    pieza.setAttribute('x', n(x));
    pieza.setAttribute('y', n(alto - suelo - h));
    pieza.setAttribute('width', n(w));
    pieza.setAttribute('height', n(h));
    pieza.style.setProperty('--i', i);
    pieza.style.setProperty('--filas', (partitura.lineas ?? []).length || 10); // para animarlo fila por fila
    x += w + separacion;
    return pieza;
  });
  const ancho = x - separacion;
  return svg('svg', { class: clase, viewBox: `0 0 ${n(ancho)} ${n(alto)}`, 'aria-hidden': 'true', focusable: 'false' },
    piezas,
    svg('rect', { x: -2, y: n(alto - suelo), width: n(ancho + 4), height: suelo, estilo: { fill: 'var(--tinta)' } }));
}
