// Perfil de un arquitecto, estilo, material, programa, estado, lugar, década o año, y los índices
// de cada tipo (#/arquitectos, #/estilos…). Una sola vista que se configura por tipo.

import { el, flecha, mensaje, agregar, bandaPerfil, enlacePerfil, chipsPerfil } from '../ui.js';
import {
  TIPOS_PERFIL, NIVELES_UBICACION, nombrePerfil, rutaPerfil, perfilDe, partituraDe,
  ancestrosEstilo, hijosEstilo, estiloConAncestros, compararTexto, anioReferencia,
} from '../datos.js';
import { separador, colorCss } from '../grafica.js';
import { grillaObras, cargarEstadisticas } from './obras.js';

export const INDICES = Object.fromEntries(Object.entries(TIPOS_PERFIL).map(([tipo, def]) => [def.indice, tipo]));

const plural = (n) => (n === 1 ? '1 obra' : `${n} obras`);

// Fondos con poco contraste para un cabezal entero: van en blanco y negro.
const EN_BLANCO_Y_NEGRO = [['estilos', 'Brutalismo']];

// ---- Qué obras tiene un perfil ----

export function obrasDePerfil(datos, tipo, valor) {
  if (tipo === 'estilo') return datos.obras.filter((o) => o.estilo && estiloConAncestros(o.estilo).includes(valor));
  return datos.obras.filter((o) => TIPOS_PERFIL[tipo].valores(o).includes(valor));
}

// El valor de un perfil a partir del slug de la dirección. Por ahora solo existen los perfiles
// que tienen obras.
function valorDeSlug(datos, tipo, s) {
  const valor = datos.slugs[tipo]?.get(s);
  return valor && obrasDePerfil(datos, tipo, valor).length ? valor : null;
}

// Facetas que no tiene sentido mostrar en la grilla de un perfil.
function facetasFijas(tipo) {
  if (NIVELES_UBICACION.includes(tipo)) return NIVELES_UBICACION.slice(0, NIVELES_UBICACION.indexOf(tipo) + 1);
  if (tipo === 'anio') return ['anio', 'decada'];
  return [tipo];
}

// ---- Perfil ----

export function render(contenedor, { datos, partes, params, titulo }) {
  const tipo = partes[0];
  const def = TIPOS_PERFIL[tipo];
  const valor = valorDeSlug(datos, tipo, partes[1] ?? '');
  if (!valor) {
    titulo('No encontrado');
    contenedor.append(mensaje(`No encontramos ese ${def.singular.toLowerCase()}`, null,
      el('a', { class: 'boton', href: `#/${def.indice}` }, `Ver ${def.plural.toLowerCase()}`)));
    return;
  }
  const nombre = nombrePerfil(tipo, valor);
  const conDecadas = tipo === 'decada' || tipo === 'anio';
  titulo(nombre);

  const obras = obrasDePerfil(datos, tipo, valor);
  const perfil = perfilDe(datos, tipo, valor);
  // Décadas y años: la colección del país filtrado (si tiene) o la del mundo. Si el filtro de
  // país cambia en la grilla, la banda y su leyenda se rehacen.
  const cabezal = el('div', { class: 'perfil-cabezal' });
  const banda = el('div', { class: 'perfil-cabeza' });
  const pintarBanda = (pais) => {
    const partitura = partituraDe(datos, tipo, valor, { pais });
    colorCabezal(cabezal, datos, partitura);
    banda.replaceChildren(...[bandaPerfil(datos, tipo, valor, { pais })].filter(Boolean));
    if (conDecadas && partitura?.obra) banda.append(el('p', { class: 'perfil-simbolo' }, `${partitura.obra} · ${partitura.lugar} · ${partitura.anio}`));
  };
  let paisActual = params.get('pais');
  pintarBanda(paisActual);
  const grilla = grillaObras({
    datos, obras, params, ruta: rutaPerfil(tipo, valor), fija: facetasFijas(tipo),
    titulo: el('h3', { class: 'perfil-obras' }, 'Obras', el('span', {}, obras.length)),
    alCambiar: conDecadas ? (filtros) => { if ((filtros.pais ?? null) !== paisActual) { paisActual = filtros.pais ?? null; pintarBanda(paisActual); } } : null,
  });

  // El cabezal, en el color del símbolo: texto, categorías (jerarquía o años) y el símbolo apoyado
  // sobre las flechas (en la compu, el símbolo a la derecha). Debajo, las obras.
  agregar(cabezal, [
    el('div', { class: 'perfil perfil-texto' },
      el('nav', { class: 'migas', 'aria-label': 'Ubicación' }, migas(datos, tipo, valor, obras)),
      el('h2', { class: 'perfil-nombre' }, nombre),
      el('p', { class: 'perfil-datos' }, lineaDatos(tipo, valor, perfil, obras)),
      perfil.descripcion && descripcion(perfil.descripcion),
    ),
    el('div', { class: 'perfil perfil-bloques' },
      resumen(tipo, obras, tipo === 'pais' ? valor : null),
      tipo === 'estilo' && jerarquia(datos, valor),
      conDecadas && tira(datos, tipo, valor, params.get('pais')),
    ),
    banda,
    separador(`perfil:${tipo}:${valor}`, 360),
  ]);
  agregar(contenedor, [cabezal, grilla]);
  cargarEstadisticas(datos, grilla);
}

// Fondo del cabezal: la placa del símbolo, con textos y flechas en el color de su marco. Sin placa
// (o con poco contraste), en blanco y negro: el tema oscuro adentro, como la cabecera.
function colorCabezal(nodo, datos, partitura) {
  const bn = !partitura?.placa || EN_BLANCO_Y_NEGRO.some(([seccion, nombre]) => datos.simbolos?.[seccion]?.[nombre] === partitura);
  if (bn) {
    nodo.dataset.tema = 'oscuro';
    nodo.style.removeProperty('--banda');
    nodo.style.removeProperty('--detalle');
  } else {
    delete nodo.dataset.tema;
    nodo.style.setProperty('--banda', colorCss(partitura.placa));
    nodo.style.setProperty('--detalle', colorCss(partitura.marco ?? 'tinta'));
  }
}

function migas(datos, tipo, valor, obras) {
  const def = TIPOS_PERFIL[tipo];
  const partes = [el('a', { href: `#/${def.indice}` }, def.plural)];
  const sumar = (nodo) => partes.push(' › ', nodo);
  if (tipo === 'estilo') {
    for (const ancestro of ancestrosEstilo(datos, valor).reverse()) sumar(enlacePerfil('estilo', ancestro));
  } else if (NIVELES_UBICACION.includes(tipo)) {
    const u = obras[0]?.ubicacion ?? {};
    for (const nivel of NIVELES_UBICACION.slice(0, NIVELES_UBICACION.indexOf(tipo))) if (u[nivel]) sumar(enlacePerfil(nivel, u[nivel]));
  } else if (tipo === 'anio') {
    sumar(enlacePerfil('decada', String(Math.floor(Number(valor) / 10) * 10)));
  }
  return partes;
}

function lineaDatos(tipo, valor, perfil, obras) {
  const partes = [];
  if (tipo === 'arquitecto') {
    if (perfil.nacimiento || perfil.muerte) partes.push(`${perfil.nacimiento ?? '?'}–${perfil.muerte ?? ''}`);
    if (perfil.fundacion) partes.push(`Desde ${perfil.fundacion}`);
    if (perfil.pais) partes.push(perfil.pais);
  }
  if (tipo === 'decada') partes.push(`Década de ${valor}`);
  // Los años de sus obras, salvo en décadas y años (ya lo dicen).
  const anios = obras.map(anioReferencia).filter((a) => a !== null);
  if (anios.length && tipo !== 'decada' && tipo !== 'anio' && tipo !== 'arquitecto') {
    const [min, max] = [Math.min(...anios), Math.max(...anios)];
    partes.push(min === max ? String(min) : `${min}–${max}`);
  }
  partes.push(plural(obras.length));
  return partes.join(' · ');
}

// Descripción cortada a unas 5 líneas, con "más" si es larga.
function descripcion(texto) {
  const parrafo = el('p', { class: 'perfil-descripcion' }, texto);
  const boton = el('button', { type: 'button', class: 'mas', hidden: true, onclick: () => { parrafo.classList.add('abierta'); boton.remove(); } }, 'más');
  requestAnimationFrame(() => { boton.hidden = parrafo.scrollHeight <= parrafo.clientHeight + 2; });
  return el('div', {}, parrafo, boton);
}

// Lo que dicen las obras del perfil, como el panel de un director en Letterboxd.
// Dentro del perfil de un país, las décadas llevan el filtro de ese país (y así usan su colección).
function resumen(tipo, obras, pais) {
  const filas = [
    ['arquitecto', 'Arquitectos'], ['estilo', 'Estilos'], ['decada', 'Décadas'], ['pais', 'Países'], ['material', 'Materiales'], ['programa', 'Programas'],
  ].filter(([t]) => t !== tipo && !(NIVELES_UBICACION.includes(tipo) && t === 'pais'));
  const contenido = filas.map(([t, etiqueta]) => {
    const conteo = new Map();
    for (const obra of obras) for (const v of TIPOS_PERFIL[t].valores(obra)) conteo.set(v, (conteo.get(v) ?? 0) + 1);
    if (!conteo.size) return null;
    const valores = [...conteo.keys()].sort(t === 'decada' ? (a, b) => a - b : compararTexto);
    const query = pais && (t === 'decada') ? { pais } : null;
    return [el('dt', {}, etiqueta), el('dd', {}, chipsPerfil(t, valores, query))];
  }).filter(Boolean);
  return contenido.length ? el('dl', { class: 'perfil-resumen' }, contenido) : null;
}

function jerarquia(datos, estilo) {
  const [padre] = ancestrosEstilo(datos, estilo);
  const hijos = hijosEstilo(datos, estilo);
  if (!padre && !hijos.length) return null;
  // Chips con la cantidad de obras de cada estilo.
  const chips = (estilos) => el('div', { class: 'chips-datos' }, estilos.map((e) => el('a', { class: 'chip-dato', href: rutaPerfil('estilo', e) },
    e, el('span', { class: 'chip-cantidad' }, obrasDePerfil(datos, 'estilo', e).length))));
  return el('dl', { class: 'perfil-resumen perfil-jerarquia' },
    padre && [el('dt', {}, 'Viene de'), el('dd', {}, chips([padre]))],
    hijos.length > 0 && [el('dt', {}, 'Incluye'), el('dd', {}, chips(hijos.sort(compararTexto)))],
  );
}

// ‹ 1940s · 1950 1951 … 1959 · 1960s ›
function tira(datos, tipo, valor, pais) {
  const extra = pais ? `?${new URLSearchParams({ pais })}` : '';
  const decada = tipo === 'decada' ? Number(valor) : Math.floor(Number(valor) / 10) * 10;
  // Solo llevan a un perfil los años y décadas que tienen obras; los demás son texto.
  const conObras = new Set(datos.obras.flatMap(TIPOS_PERFIL.anio.valores));
  const decadasConObras = new Set(datos.obras.flatMap(TIPOS_PERFIL.decada.valores));
  const anio = (a) => (conObras.has(String(a))
    ? el('a', { class: 'tira-anio con-obras', href: rutaPerfil('anio', String(a)) + extra, 'aria-current': tipo === 'anio' && String(a) === valor ? 'page' : null }, a)
    : el('span', { class: 'tira-anio' }, a));
  const otra = (d, texto) => (decadasConObras.has(String(d))
    ? el('a', { class: 'tira-decada', href: rutaPerfil('decada', String(d)) + extra }, texto)
    : el('span', { class: 'tira-anio' }, texto));
  const nodo = el('nav', { class: 'tira', 'aria-label': 'Años' },
    otra(decada - 10, `‹ ${decada - 10}s`),
    tipo === 'decada' ? el('strong', { class: 'tira-decada' }, `${decada}s`) : otra(decada, `${decada}s`),
    Array.from({ length: 10 }, (_, k) => anio(decada + k)),
    otra(decada + 10, `${decada + 10}s ›`),
  );
  requestAnimationFrame(() => nodo.querySelector('[aria-current]')?.scrollIntoView({ inline: 'center', block: 'nearest' }));
  return nodo;
}

// ---- Índices ----

export function renderIndice(contenedor, { datos, partes, titulo }) {
  const tipo = INDICES[partes[0]];
  const def = TIPOS_PERFIL[tipo];
  titulo(def.plural);
  const cantidad = (v) => obrasDePerfil(datos, tipo, v).length;
  const valores = [...datos.slugs[tipo].values()].filter((v) => cantidad(v) > 0);
  const fila = (v, nivel = 0) => el('li', { class: 'indice-fila', style: nivel ? `--nivel:${nivel}` : null },
    el('a', { href: rutaPerfil(tipo, v) }, el('span', {}, nombrePerfil(tipo, v)), el('span', { class: 'indice-puntos', 'aria-hidden': 'true' }), el('span', { class: 'indice-cantidad' }, cantidad(v))));

  let filas;
  if (tipo === 'estilo') {
    // Árbol: las raíces y, debajo, sus descendientes.
    const estilos = datos.perfiles.estilos ?? {};
    const raices = valores.filter((v) => !estilos[v]?.padre || !valores.includes(estilos[v].padre)).sort(compararTexto);
    const rama = (v, nivel) => [fila(v, nivel), ...hijosEstilo(datos, v).filter((h) => valores.includes(h)).sort(compararTexto).flatMap((h) => rama(h, nivel + 1))];
    filas = raices.flatMap((r) => rama(r, 0));
  } else {
    const numerico = tipo === 'decada' || tipo === 'anio';
    filas = valores.sort(numerico ? (a, b) => b - a : (a, b) => compararTexto(nombrePerfil(tipo, a), nombrePerfil(tipo, b))).map((v) => fila(v));
  }
  contenedor.append(
    el('div', { class: 'perfil' }, el('h2', { class: 'perfil-nombre' }, def.plural), el('p', { class: 'perfil-datos' }, `${valores.length} en total`)),
    filas.length ? el('ul', { class: 'indice' }, filas) : mensaje('Todavía no hay ninguno'),
  );
}

// Enlaces a los índices, para el pie del inicio.
export function enlacesIndices() {
  return ['arquitecto', 'estilo', 'decada', 'pais', 'material', 'programa'].map((t) =>
    el('a', { href: `#/${TIPOS_PERFIL[t].indice}` }, TIPOS_PERFIL[t].plural, flecha()));
}

