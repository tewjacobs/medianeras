import { separador, logo, simbolo, simboloNeutro, registrarColoresSimbolos, hashTexto } from './js/grafica.js';
import { tarjetaObra } from './js/ui.js';
import { COLORES_MARCO } from './js/datos.js';

const obras = await (await fetch('data/obras.json')).json();
const simbolos = await (await fetch('data/simbolos.json', { cache: 'no-store' })).json();
const html = await (await fetch('index-app.html')).text();
const cargaApp = new DOMParser().parseFromString(html, 'text/html').getElementById('carga');
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
const familiaDe = (semilla) => COLORES_MARCO[hashTexto(semilla) % COLORES_MARCO.length];
const ANCHO = 390;

function tamLogo(px, clase) {
  const s = logo();
  s.style.width = `${px}px`;
  s.style.height = `${px}px`;
  if (clase) s.classList.add(clase);
  return s;
}

function seccionLogo() {
  return h('div', { className: 'logo' },
    h('p', { className: 'logo-titulo', textContent: '5b·2 sobre una grilla de 48 × 48 con coordenadas enteras: las dos perspectivas en rojo, con la misma inclinación (sube 2 cada 3); el costado del alto termina justo donde termina el frente del bajo y el del bajo, justo en el borde del vidrio.' }),
    h('div', { className: 'logo-cabecera cabecera-marca' }, tamLogo(22), h('span', { className: 'logo-nombre', textContent: 'medianeras' })),
    h('div', { className: 'logo-iconos' },
      h('figure', {}, tamLogo(150), h('figcaption', { textContent: 'grande' })),
      h('figure', {}, tamLogo(60, 'icono-app'), h('figcaption', { textContent: 'ícono app' })),
      h('figure', {}, tamLogo(22), h('figcaption', { textContent: '22 px' }))));
}

function bandera({ partitura, nombre, linea, nota, anio = null, mostrarPartitura = true }) {
  return h('div', { className: 'bandera' },
    simbolo(partitura, { ancho: ANCHO, alto: 132, anio }),
    h('div', { className: 'bandera-texto' },
      h('h3', { textContent: nombre }),
      linea && h('p', { textContent: linea }),
      nota && h('p', { className: 'nota', textContent: nota }),
      mostrarPartitura && h('details', { className: 'partitura' },
        h('summary', { textContent: 'ver la partitura' }),
        h('pre', { textContent: JSON.stringify(partitura, null, 1).replace(/\n\s*/g, '\n').replace(/^\{\n|\n\}$/g, '') }))));
}

const CON_SIMBOLO = [
  ['paises', 'Argentina', '2 OBRAS'],
  ['paises', 'Estados Unidos', '2 OBRAS'],
  ['paises', 'Uruguay', '1 OBRA'],
  ['arquitectos', 'Frank Lloyd Wright', '1867–1959 · ESTADOS UNIDOS · 1 OBRA'],
  ['arquitectos', 'D. H. Burnham & Company', 'ESTADOS UNIDOS · 1 OBRA'],
  ['estilos', 'Moderno', '3 OBRAS'],
  ['estilos', 'Arquitectura orgánica', 'MODERNO › ORGÁNICA · 1 OBRA'],
  ['estilos', 'Beaux-Arts', 'ACADEMICISMO › BEAUX-ARTS · 1 OBRA'],
];

const SIN_SIMBOLO = [
  ['arquitecto', 'Estudio de ejemplo', '2 OBRAS'],
  ['material', 'Revoque', '1 OBRA'],
];

const MATERIALES = ['Ladrillo', 'Hormigón armado', 'Hormigón visto', 'Madera', 'Vidrio', 'Acero', 'Piedra caliza', 'Terracota'];
const PROGRAMAS = ['Museo', 'Vivienda unifamiliar', 'Vivienda colectiva', 'Oficinas', 'Cultural'];

const AÑOS = [[1936, 'EN LA DÉCADA DEL KAVANAGH'], [1959, 'EN LA DÉCADA DE LA CASA CURUTCHET'], [1972, 'EN LA DÉCADA DE SOMISA']];

const decadas = (coleccion) => Object.entries(simbolos.decadas[coleccion]).map(([decada, partitura]) => bandera({
  partitura, nombre: `${decada}s`, linea: `${partitura.obra.toUpperCase()} · ${partitura.lugar.toUpperCase()} · ${partitura.anio}`, nota: partitura.nota,
}));

const lista = (tipo, nombres) => nombres.map((nombre) => bandera({ partitura: simbolos[tipo][nombre], nombre, nota: simbolos[tipo][nombre].nota }));

function columna(tema) {
  const cajaCarga = h('div', { className: 'carga-demo' }, document.importNode(cargaApp, true));
  const repetir = h('button', { type: 'button', className: 'boton boton-chico', textContent: 'Repetir animación',
    onclick: () => cajaCarga.replaceChildren(document.importNode(cargaApp, true)) });
  
  return h('div', { className: 'columna', dataset: { tema } },
    h('p', { className: 'titulo-col', textContent: tema === 'claro' ? 'Claro · Another Green World' : 'Oscuro · Pinback' }),

    h('h2', { textContent: 'Logo' }),
    seccionLogo(),

    h('h2', { textContent: 'Estilos' }),
    CON_SIMBOLO.filter(([tipo]) => tipo === 'estilos').map(([tipo, nombre, linea]) => bandera({ partitura: simbolos[tipo][nombre], nombre, linea, nota: simbolos[tipo][nombre].nota })),

    h('h2', { textContent: 'Banderas y obras de arquitectos' }),
    CON_SIMBOLO.filter(([tipo]) => tipo !== 'estilos').map(([tipo, nombre, linea]) => {
      const partitura = simbolos[tipo][nombre];
      return bandera({ partitura, nombre, linea, nota: partitura.nota });
    }),

    h('h2', { textContent: 'Décadas · Argentina (la que usa la app)' }),
    decadas('argentina'),

    h('h2', { textContent: 'Décadas · Mundo' }),
    decadas('mundo'),

    h('h2', { textContent: 'Años: el símbolo de su década con una marca' }),
    h('p', { className: 'nota', textContent: 'Debajo del dibujo, diez marcas, una por año de la década; la de ese año va en rojo y más alta.' }),
    AÑOS.map(([anio, linea]) => bandera({
      partitura: simbolos.decadas.argentina[String(Math.floor(anio / 10) * 10)], nombre: String(anio), linea, anio: anio % 10, mostrarPartitura: false,
    })),

    h('h2', { textContent: 'Materiales' }),
    lista('materiales', MATERIALES),

    h('h2', { textContent: 'Programas' }),
    lista('programas', PROGRAMAS),

    h('h2', { textContent: 'Sin símbolo (neutro)' }),
    SIN_SIMBOLO.map(([tipo, nombre, linea]) => bandera({
      partitura: simboloNeutro(familiaDe(`${tipo}:${nombre}`)), nombre, linea, nota: 'Una sola línea fina en el color de su familia.', mostrarPartitura: false,
    })),

    h('h2', { textContent: 'Tapas: obras actuales y obras sin foto' }),
    h('div', { className: 'grilla' },
      obras.map((obra) => tarjetaObra(obra)),
      ['casa-curutchet', 'kavanagh', 'banco-londres', 'teatro-san-martin', 'mirador-ciudad', 'pabellon-x', 'galeria-y'].map((id, i) =>
        tarjetaObra({ id, nombre: `Sin foto: ${id}`, estilo: `estilo-${i % 4}`, anio_finalizacion: 1950 + i * 3, fotos: [] }))),

    h('h2', { textContent: 'Separadores' }),
    separador('inicio:decadas', ANCHO - 32),
    h('p', { className: 'nota', textContent: 'POR DÉCADA' }),

    h('h2', { textContent: 'Pantalla de carga: planta de la Price Tower' }),
    cajaCarga, h('p', {}, repetir),
  );
}

document.getElementById('columnas').replaceChildren(columna('claro'), columna('oscuro'));
