// Opciones para elegir: botón de visita, cabecera, flechas, "Todas las obras", chips y ficha con
// pestañas. Usa las piezas reales de la app (tapas, galería, datos) en claro y en oscuro.

import { cargarDatos, colorMarco, rangoAnios, NIVELES_UBICACION, ancestrosEstilo, rutaPerfil, nombrePerfil, formatoFecha } from './js/datos.js';
import { el, icono, tapaObra, galeria, creditoFoto, estrellas } from './js/ui.js';
import { logo } from './js/grafica.js';

const datos = await cargarDatos();
const NS = 'http://www.w3.org/2000/svg';
function s(etiqueta, atributos = {}, ...hijos) {
  const n = document.createElementNS(NS, etiqueta);
  for (const [k, v] of Object.entries(atributos)) n.setAttribute(k, v);
  n.append(...hijos.flat());
  return n;
}

// ---------- 1. Botón de visita: la Price Tower en 24 px ----------

// Cuadrado de 15 de lado girado 30°, centrado en (12, 12).
const cuadrado = (() => {
  const a = Math.PI / 6;
  return [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([x, y]) => {
    const [px, py] = [x * 7.5, y * 7.5];
    return `${(12 + px * Math.cos(a) - py * Math.sin(a)).toFixed(2)},${(12 + px * Math.sin(a) + py * Math.cos(a)).toFixed(2)}`;
  }).join(' ');
})();
const brazos = (desde, hasta) => [[1, 0], [-1, 0], [0, 1], [0, -1]].map(([dx, dy]) =>
  `M${12 + dx * desde} ${12 + dy * desde}L${12 + dx * hasta} ${12 + dy * hasta}`).join('');

const VISITA = {
  A: {
    nombre: 'A · Contorno y cruz llena',
    nota: 'El cuadrado en línea de tinta y la cruz roja llena, con el hueco del centro.',
    dibujo: () => s('svg', { viewBox: '0 0 24 24', class: 'pt', 'aria-hidden': 'true' },
      s('polygon', { points: cuadrado, fill: 'none', stroke: 'currentColor', 'stroke-width': 1.7 }),
      s('path', { d: brazos(2.6, 11.8), stroke: 'var(--rojo)', 'stroke-width': 2.8, fill: 'none' })),
  },
  B: {
    nombre: 'B · Cuadrado lleno',
    nota: 'El cuadrado lleno de tinta y la cruz roja encima, separada por un filete del color del fondo. Es la que más pesa a 24 px.',
    dibujo: () => s('svg', { viewBox: '0 0 24 24', class: 'pt', 'aria-hidden': 'true' },
      s('polygon', { points: cuadrado, fill: 'currentColor' }),
      s('path', { d: brazos(2.4, 11.8), stroke: 'var(--papel)', 'stroke-width': 4.4, fill: 'none' }),
      s('path', { d: brazos(2.4, 11.8), stroke: 'var(--rojo)', 'stroke-width': 2.6, fill: 'none' })),
  },
  C: {
    nombre: 'C · Muros huecos',
    nota: 'Como la pantalla de carga: cada brazo son dos líneas rojas paralelas. A 24 px se lee, pero es la más fina.',
    dibujo: () => s('svg', { viewBox: '0 0 24 24', class: 'pt', 'aria-hidden': 'true' },
      s('polygon', { points: cuadrado, fill: 'none', stroke: 'currentColor', 'stroke-width': 1.5 }),
      s('path', { d: brazos(2.4, 11.8), stroke: 'var(--rojo)', 'stroke-width': 3.6, fill: 'none' }),
      s('path', { d: brazos(2.4, 11.9), stroke: 'var(--papel)', 'stroke-width': 1.4, fill: 'none' })),
  },
};

function barra(dibujo) {
  const pestana = (ic, txt, extra = '') => el('a', { class: extra }, ic, el('span', {}, txt));
  return el('nav', { class: 'barra' },
    pestana(icono('grilla'), 'Obras'), pestana(icono('mapa'), 'Mapa'),
    dibujo ? pestana(dibujo(), 'Visita', 'visita') : pestana(icono('mas'), 'Visita', 'visita-mas'),
    pestana(icono('diario'), 'Diario'), pestana(icono('listas'), 'Listas'));
}

function seccionVisita() {
  return [
    el('div', { class: 'opcion' }, el('p', { class: 'rotulo' }, 'Hoy: el "+" en el recuadro rojo'), barra(null)),
    ...Object.values(VISITA).map((v) => el('div', { class: 'opcion' },
      el('p', { class: 'rotulo' }, el('b', {}, v.nombre), ` — ${v.nota}`),
      barra(v.dibujo),
      el('div', { class: 'tamanos' }, [24, 32, 48].map((px) => {
        const d = v.dibujo(); d.style.width = d.style.height = `${px}px`;
        return el('figure', {}, d, el('figcaption', {}, `${px} px`));
      })))),
  ];
}

// ---------- 2. Cabecera ----------

const BUSQUEDAS = {
  S1: { nombre: 'S1 · Tres filetes', nota: 'Sin caja: tres líneas finas paralelas abajo. En foco, la del medio se pone roja.' },
  S2: { nombre: 'S2 · Banda rayada', nota: 'Caja con un filete y, a la izquierda, una banda de rayas verticales finas. En foco, las rayas en rojo.' },
  S3: { nombre: 'S3 · Doble filete', nota: 'Dos filetes paralelos, uno adentro del otro. En foco, el de adentro en rojo.' },
};

function cabecera(clase, foco) {
  const campo = el('div', { class: `campo-b ${clase.toLowerCase()}${foco ? ' foco' : ''}` },
    el('input', { type: 'search', placeholder: 'Buscar obra, arquitecto/a…', value: foco ? 'Wright' : '' }));
  return el('div', { class: 'cab' },
    el('div', { class: 'cab-fila' }, logo(), el('span', { class: 'logo-nombre' }, 'medianeras')),
    el('div', { class: 'cab-busca' }, campo,
      el('button', { class: 'cab-btn', type: 'button' }, icono('buscar')),
      el('button', { class: 'cab-btn tema', type: 'button' }, icono('tema'))));
}

function seccionCabecera() {
  return Object.entries(BUSQUEDAS).map(([clave, b]) => el('div', { class: 'opcion' },
    el('p', { class: 'rotulo' }, el('b', {}, b.nombre), ` — ${b.nota}`),
    cabecera(clave, false),
    el('p', { class: 'foco-nota' }, 'En foco (escribiendo):'),
    cabecera(clave, true)));
}

// ---------- 3. Flechas, "Todas las obras" y chips ----------

const FLECHAS = {
  F1: { nombre: 'F1 · Paralelas que convergen', nota: 'Tres líneas paralelas; las de afuera doblan y se juntan en la punta.',
    dibujo: () => s('svg', { viewBox: '0 0 22 14', class: 'flecha', 'aria-hidden': 'true', fill: 'none', stroke: 'currentColor', 'stroke-width': 1.3 },
      s('path', { d: 'M0 2.5H13L20.5 7L13 11.5H0M0 7H20.5' })) },
  F2: { nombre: 'F2 · Escalonada', nota: 'Rayas apiladas de distinto largo que forman la punta, como la pirámide del Louvre acostada.',
    dibujo: () => s('svg', { viewBox: '0 0 22 14', class: 'flecha', 'aria-hidden': 'true' },
      [8, 13, 17, 21, 17, 13, 8].map((l, i) => s('rect', { x: 0, y: 0.5 + i * 1.9, width: l, height: 1.1, fill: 'currentColor' }))) },
  F3: { nombre: 'F3 · Doble trazo', nota: 'Una línea doble con la punta también doble, como dos trazos paralelos.',
    dibujo: () => s('svg', { viewBox: '0 0 22 14', class: 'flecha', 'aria-hidden': 'true', fill: 'none', stroke: 'currentColor', 'stroke-width': 1.1 },
      s('path', { d: 'M0 6H17M0 8.4H17M12.5 1.5L19 7.2L12.5 12.9M15.2 1.5L21.6 7.2L15.2 12.9' })) },
};

function seccionFlechas() {
  return Object.values(FLECHAS).map((f) => el('div', { class: 'opcion' },
    el('p', { class: 'rotulo' }, el('b', {}, f.nombre), ` — ${f.nota}`),
    el('div', { class: 'muestra-flechas' },
      el('div', { class: 'encab' }, el('span', {}, 'Agregadas recientemente'), el('a', { class: 'ver-mas-m' }, 'Ver más', f.dibujo())),
      el('div', { class: 'fila-m' }, el('span', {}, 'Arquitectos'), f.dibujo()),
      el('a', { class: 'todas t1-simple', style: 'border:1px solid var(--tinta);min-height:52px;padding:0 14px' },
        el('span', { class: 'todas-texto' }, el('strong', {}, 'Todas las obras (5)')), f.dibujo()))));
}

function seccionTodas() {
  const obras = datos.obras;
  const texto = el('span', { class: 'todas-texto' }, el('strong', {}, 'Todas las obras'), el('span', {}, `${obras.length} obras · 3 países`));
  const f = () => FLECHAS.F1.dibujo();
  return [
    el('div', { class: 'opcion' },
      el('p', { class: 'rotulo' }, el('b', {}, 'T1 · Con rayas'), ' — Filete de tinta; a la derecha, un bloque de rayas finas con la cantidad.'),
      el('a', { class: 'todas t1' }, texto.cloneNode(true), el('span', { class: 'rayas' }, el('span', { class: 'num' }, obras.length), ))),
    el('div', { class: 'opcion' },
      el('p', { class: 'rotulo' }, el('b', {}, 'T2 · Franja de color'), ' — Fondo suave del color de la familia, entre dos filetes dobles.'),
      el('a', { class: 'todas t2' }, texto.cloneNode(true), f())),
    el('div', { class: 'opcion' },
      el('p', { class: 'rotulo' }, el('b', {}, 'T3 · Bloque con tapas'), ' — Bloque de tinta, como el lomo de un disco, con las tapas chiquitas de las obras.'),
      el('a', { class: 'todas t3' }, texto.cloneNode(true), el('span', { class: 'mini' }, obras.slice(0, 4).map((o) => tapaObra(o))), f())),
  ];
}

// Chips de la ficha: cada dato lleva a su perfil, con el fondo suave del color de la obra.
function chip(tipo, valor, familia, intensidad) {
  return el('a', { class: 'chip-f', href: rutaPerfil(tipo, valor), style: `--familia: var(--${familia}); --intensidad: ${intensidad}` }, nombrePerfil(tipo, valor));
}

function datosChips(obra, intensidad = '16%') {
  const fam = colorMarco(obra);
  const c = (tipo, valores) => el('div', { class: 'chips-m' }, valores.map((v) => chip(tipo, v, fam, intensidad)));
  const u = obra.ubicacion ?? {};
  const filas = [
    ['Arquitectos', obra.arquitectos?.length && c('arquitecto', obra.arquitectos)],
    ['Año', c('anio', [obra.anio_proyecto, obra.anio_finalizacion].filter(Boolean).map(String))],
    ['Década', c('decada', [String(Math.floor((obra.anio_finalizacion ?? obra.anio_proyecto) / 10) * 10)])],
    ['Estilo', obra.estilo && c('estilo', [...ancestrosEstilo(datos, obra.estilo).reverse(), obra.estilo])],
    ['Materiales', obra.materiales?.length && c('material', obra.materiales)],
    ['Programa', obra.programa && c('programa', [obra.programa])],
    ['Estado', obra.estado && c('estado', [obra.estado])],
  ].filter(([, v]) => v);
  return el('dl', { class: 'datos-chips' }, filas.map(([k, v]) => [el('dt', {}, k), el('dd', {}, v)]));
}

function seccionChips() {
  const obra = datos.porId.get('solomon-r-guggenheim-museum');
  const fam = colorMarco(obra);
  const botones = (estilo) => el('div', { class: 'acciones' },
    el('a', { class: 'boton boton-primario' }, icono('mas'), 'Registrar visita'),
    el('a', { class: `boton ${estilo}`, style: `--familia: var(--${fam})` }, icono('mapa'), 'Ver en el mapa'),
    el('a', { class: `boton ${estilo}`, style: `--familia: var(--${fam})` }, icono('ruta'), 'Cómo llegar'));
  return [
    el('div', { class: 'opcion' },
      el('p', { class: 'rotulo' }, el('b', {}, 'Chips suaves (16 %)'), ' — los datos de la ficha como chips del color de la obra; los botones secundarios con el mismo fondo.'),
      datosChips(obra, '16%'), el('div', { style: 'height:12px' }), botones('boton-f')),
    el('div', { class: 'opcion' },
      el('p', { class: 'rotulo' }, el('b', {}, 'Chips un poco más marcados (26 %)'), ' — más color, para comparar.'),
      datosChips(obra, '26%')),
    el('div', { class: 'opcion' },
      el('p', { class: 'rotulo' }, el('b', {}, 'Hoy'), ' — links subrayados y botones con filete.'),
      botones('')),
  ];
}

// ---------- 4. Ficha con pestañas ----------

// Planos de ejemplo, dibujados acá (no son de ninguna obra real).
function planoEjemplo(tipo) {
  const linea = { fill: 'none', stroke: 'var(--tinta)', 'stroke-width': 2 };
  if (tipo === 'planta') return s('svg', { viewBox: '0 0 300 200' },
    s('rect', { x: 20, y: 20, width: 260, height: 160, ...linea, 'stroke-width': 5 }),
    s('path', { d: 'M140 20V110M140 140V180M20 100H90M115 100H140M200 20V80M200 105V180', ...linea }),
    s('path', { d: 'M60 20H110', stroke: 'var(--papel-2)', 'stroke-width': 6 }), s('path', { d: 'M60 20H110', ...linea, 'stroke-width': 1 }),
    s('path', { d: 'M230 180H270', stroke: 'var(--papel-2)', 'stroke-width': 6 }), s('path', { d: 'M230 180H270M230 180A40 40 0 0 1 270 140', ...linea, 'stroke-width': 1 }));
  return s('svg', { viewBox: '0 0 300 200' },
    s('path', { d: 'M10 180H290', ...linea, 'stroke-width': 3 }),
    s('rect', { x: 40, y: 60, width: 220, height: 120, ...linea, 'stroke-width': 4 }),
    s('path', { d: 'M40 120H260M30 60H270', ...linea }),
    s('path', { d: 'M150 60V180', ...linea, 'stroke-dasharray': '4 4', 'stroke-width': 1 }));
}

function ficha(obra, { planos = [] } = {}) {
  const u = obra.ubicacion ?? {};
  const fam = colorMarco(obra);
  const visitas = datos.diario.filter((e) => e.obra_id === obra.id);
  const lugares = NIVELES_UBICACION.filter((n) => u[n]).map((n) => chip(n, u[n], fam, '16%'));
  const paneles = [
    ['Datos', [datosChips(obra), obra.descripcion && el('p', { class: 'ficha-descripcion' }, obra.descripcion)]],
    ['Ubicación', [el('div', { class: 'chips-m' }, lugares), u.direccion && el('p', { class: 'ficha-descripcion' }, u.direccion),
      Number.isFinite(u.lat) && el('p', { class: 'ubicacion-coord' }, `${u.lat}, ${u.lng}`),
      el('div', { class: 'acciones' }, el('a', { class: 'boton boton-f', style: `--familia: var(--${fam})` }, icono('mapa'), 'Ver en el mapa'),
        el('a', { class: 'boton boton-f', style: `--familia: var(--${fam})` }, icono('ruta'), 'Cómo llegar'))]],
    obra.fotos?.length && ['Fotos', [el('div', { style: 'margin: 0 -16px' }, galeria(obra.fotos, { alt: obra.nombre, pie: creditoFoto }))]],
    planos.length && ['Planos', planos.map((p) => el('figure', { class: 'plano' }, planoEjemplo(p.tipo),
      el('figcaption', {}, `${p.pie} · ${p.autor} · ${p.licencia}`)))],
    ['Visitas', visitas.length ? visitas.map((e) => el('div', { class: 'entrada-m' },
      el('time', {}, formatoFecha(e.fecha)), estrellas(e.puntaje), e.nota && el('p', {}, e.nota)))
      : [el('p', { class: 'tenue' }, 'Todavía no registraste visitas a esta obra.')]],
  ].filter(Boolean);

  const botones = [];
  const cuerpos = [];
  paneles.forEach(([nombre, contenido], i) => {
    const cuerpo = el('div', { class: 'panel-ficha', hidden: i !== 0 }, contenido);
    const boton = el('button', { type: 'button', 'aria-selected': String(i === 0), onclick: () => {
      botones.forEach((b, k) => b.setAttribute('aria-selected', String(k === i)));
      cuerpos.forEach((c, k) => { c.hidden = k !== i; });
    } }, nombre);
    botones.push(boton); cuerpos.push(cuerpo);
  });

  return el('div', { class: 'ficha-m' },
    el('div', { class: 'ficha-tapa' }, tapaObra(obra, { grande: true })),
    el('div', { class: 'cabecera-ficha' },
      el('h2', {}, obra.nombre),
      el('p', { class: 'linea' }, [rangoAnios(obra), ...(obra.arquitectos ?? [])].filter(Boolean).join(' · ')),
      el('div', { class: 'acciones' }, el('a', { class: 'boton boton-primario' }, icono('mas'), 'Registrar visita'),
        el('a', { class: 'boton boton-f', style: `--familia: var(--${fam})` }, icono('mapa'), 'Mapa'))),
    el('div', { class: 'pestanas-ficha', role: 'tablist' }, botones),
    cuerpos);
}

function seccionFicha() {
  return [
    el('div', { class: 'opcion' }, el('p', { class: 'rotulo' }, el('b', {}, 'Guggenheim'), ' — sin planos: la pestaña PLANOS no aparece. Tocá las pestañas.'),
      ficha(datos.porId.get('solomon-r-guggenheim-museum'))),
    el('div', { class: 'opcion' }, el('p', { class: 'rotulo' }, el('b', {}, 'Obra de ejemplo con planos'), ' — planta y corte dibujados para la prueba, con su crédito y licencia como las fotos.'),
      ficha(datos.porId.get('ejemplo-casa-belgrano'), { planos: [
        { tipo: 'planta', pie: 'Planta baja', autor: 'Medianeras (plano de ejemplo)', licencia: 'CC0' },
        { tipo: 'corte', pie: 'Corte A-A', autor: 'Medianeras (plano de ejemplo)', licencia: 'CC0' },
      ] })),
  ];
}

// ---------- Armado ----------

const SECCIONES = [
  ['1. Botón de visita', 'La Price Tower simplificada en lugar del "+". Abajo de cada barra, el símbolo a 24, 32 y 48 px.', seccionVisita],
  ['2. Cabecera', 'Logo más grande (42 px) con el nombre del mismo tamaño; el botón de tema a la derecha de la lupa; tres búsquedas.', seccionCabecera],
  ['3a. Flechas', 'En VER MÁS, en la lista de Explorar y en Todas las obras.', seccionFlechas],
  ['3b. Todas las obras', 'Tres recuadros.', seccionTodas],
  ['3c. Chips y botones con color', 'Fondo suave del color de la familia de la obra, como los chips de Letterboxd.', seccionChips],
  ['4. Ficha con pestañas', 'Siempre arriba: tapa, nombre, años y arquitecto, botones. Debajo: DATOS · UBICACIÓN · FOTOS · PLANOS · VISITAS. Solo se ve la pestaña elegida.', seccionFicha],
];

document.getElementById('opciones').replaceChildren(...SECCIONES.map(([titulo, nota, armar]) =>
  el('section', { class: 'seccion' }, el('h2', {}, titulo), el('p', {}, nota),
    el('div', { class: 'columnas' }, ['claro', 'oscuro'].map((tema) => el('div', { class: 'telefono', dataset: { tema } }, armar()))))));
