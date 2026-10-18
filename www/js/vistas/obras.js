// Grilla de obras con búsqueda, filtros y orden. El estado vive en la URL. Se usa en #/obras
// (todas las obras) y dentro de cada perfil (las obras de ese perfil, sin su propia faceta).

import { el, icono, tarjetaObra, mensaje, abrirHoja, estrellas, agregar } from '../ui.js';
import { entradasDiario, estadisticasVisitas } from '../datos.js';
import { FACETAS, ORDENES, leerFiltros, filtrosAQuery, conFiltro, filtrar, ordenar, opciones, filtrosActivos } from '../filtros.js';

// En #/obras el buscador es el de la cabecera (app.js), que avisa con el evento "medianeras:buscar".
export function render(contenedor, { datos, params }) {
  const grilla = grillaObras({ datos, obras: datos.obras, params, ruta: '#/obras', buscadorPropio: false });
  contenedor.append(grilla);
  cargarEstadisticas(datos, grilla);
}

// Las visitas del teléfono pueden tardar: la grilla se muestra antes y se reordena cuando llegan.
export function cargarEstadisticas(datos, grilla) {
  entradasDiario(datos).then((entradas) => grilla.actualizarEstadisticas(estadisticasVisitas(entradas)));
}

// `obras`: el universo de la grilla · `ruta`: la dirección base, a la que se suman los filtros ·
// `fija`: claves de faceta que no se muestran (la propia del perfil).
// `alCambiar(filtros)`: avisa cada cambio de filtros (el perfil de una década lo usa para la banda).
export function grillaObras({ datos, obras: universo, params, ruta, estadisticas = new Map(), fija = [], titulo, alCambiar, buscadorPropio = true }) {
  let filtros = leerFiltros(params);
  let visitadas = new Set(estadisticas.keys());
  const facetas = FACETAS.filter((f) => !fija.includes(f.clave));
  const raiz = el('div', { class: 'grilla-obras' });

  const buscador = el('input', {
    type: 'search', class: 'buscador', placeholder: 'Buscar obra, arquitecto/a…', 'aria-label': 'Buscar',
    value: filtros.q ?? '', enterkeyhint: 'search', autocomplete: 'off',
    oninput: () => cambiar({ ...filtros, q: buscador.value.trim() || undefined }),
  });
  const contadorFiltros = el('span', { class: 'insignia' });
  const botonFiltros = el('button', { type: 'button', class: 'boton boton-filtros', onclick: abrirFiltros }, icono('filtros'), 'Filtros', contadorFiltros);
  const selectorOrden = el('select', {
    class: 'selector-orden', 'aria-label': 'Ordenar por',
    onchange: () => cambiar({ ...filtros, orden: selectorOrden.value === 'nombre' ? undefined : selectorOrden.value }),
  }, Object.entries(ORDENES).map(([valor, nombre]) => el('option', { value: valor, selected: (filtros.orden ?? 'nombre') === valor }, nombre)));
  const chips = el('div', { class: 'chips' });
  const resumen = el('p', { class: 'resumen' });
  const grilla = el('div', { class: 'grilla' });

  agregar(raiz, [
    titulo,
    el('div', { class: 'barra-herramientas' }, buscadorPropio ? buscador : null, botonFiltros),
    el('div', { class: 'barra-orden' }, resumen, el('label', { class: 'orden' }, el('span', {}, 'Orden'), selectorOrden)),
    chips, grilla,
  ]);

  let hoja = null;

  function cambiar(nuevos) {
    filtros = nuevos;
    const query = filtrosAQuery(filtros);
    history.replaceState(null, '', query ? `${ruta}?${query}` : ruta);
    alCambiar?.(filtros);
    pintar();
  }

  function detalle(obra) {
    if (filtros.orden === 'puntaje') {
      const promedio = estadisticas.get(obra.id)?.promedio;
      return promedio ? estrellas(Math.round(promedio)) : null;
    }
    if (filtros.orden === 'visita') return estadisticas.get(obra.id)?.ultima ?? null;
    return null;
  }

  function pintar() {
    const resultado = ordenar(filtrar(universo, filtros, { visitadas }), filtros.orden, { estadisticas, todas: datos.obras });
    const activos = filtrosActivos(filtros).filter(({ faceta }) => !fija.includes(faceta.clave));

    contadorFiltros.textContent = activos.length || '';
    contadorFiltros.hidden = activos.length === 0;
    chips.replaceChildren();
    agregar(chips, [
      ...activos.map(({ faceta, nombre }) => el('button', {
        type: 'button', class: 'chip', 'aria-label': `Quitar filtro ${faceta.etiqueta}: ${nombre}`,
        onclick: () => cambiar(conFiltro(filtros, faceta.clave, null)),
      }, nombre, el('span', { 'aria-hidden': 'true' }, '×'))),
      filtros.visitadas && el('button', { type: 'button', class: 'chip', onclick: () => cambiar({ ...filtros, visitadas: undefined }) },
        'Visitadas', el('span', { 'aria-hidden': 'true' }, '×')),
    ]);

    resumen.textContent = resultado.length === 1 ? '1 obra' : `${resultado.length} obras`;
    grilla.replaceChildren(...resultado.map((obra) => tarjetaObra(obra, { detalle: detalle(obra) })));
    if (resultado.length === 0) {
      grilla.append(universo.length === 0
        ? mensaje('Todavía no hay obras', 'Cargalas en data/obras.json (ver README).')
        : mensaje('Ninguna obra coincide', 'Probá sacando algún filtro.', el('button', { type: 'button', class: 'boton', onclick: limpiar }, 'Limpiar filtros')));
    }
    if (hoja) pintarHoja(resultado.length);
  }

  function limpiar() {
    buscador.value = '';
    cambiar(filtros.orden ? { orden: filtros.orden } : {});
  }

  function abrirFiltros() {
    hoja = abrirHoja({ titulo: 'Filtros', contenido: el('div', { class: 'formulario' }), pie: [], alCerrar: () => { hoja = null; } });
    pintar();
  }

  function pintarHoja(cantidad) {
    const campos = facetas.map((faceta) => {
      const lista = opciones(universo, filtros, faceta);
      const bloqueado = faceta.padre && !filtros[faceta.padre] && !fija.includes(faceta.padre);
      if (lista.length === 0 && !filtros[faceta.clave]) return null;
      const select = el('select', {
        id: `filtro-${faceta.clave}`, disabled: bloqueado,
        onchange: () => cambiar(conFiltro(filtros, faceta.clave, select.value || null)),
      },
      el('option', { value: '' }, bloqueado ? `Elegí antes ${FACETAS.find((f) => f.clave === faceta.padre).etiqueta.toLowerCase()}` : 'Todos'),
      lista.map(({ valor, nombre, cantidad: n }) => el('option', { value: valor, selected: filtros[faceta.clave] === valor }, `${nombre} (${n})`)));
      return el('label', { class: 'campo', for: select.id }, el('span', {}, faceta.etiqueta), select);
    });
    const soloVisitadas = el('input', { type: 'checkbox', checked: Boolean(filtros.visitadas), onchange: () => cambiar({ ...filtros, visitadas: soloVisitadas.checked ? 'si' : undefined }) });
    hoja.cuerpo.firstChild.replaceChildren(
      ...campos.filter(Boolean),
      el('label', { class: 'campo-check' }, soloVisitadas, el('span', {}, 'Solo las que visité')),
    );
    hoja.pie.replaceChildren(
      el('button', { type: 'button', class: 'boton', onclick: limpiar }, 'Limpiar'),
      el('button', { type: 'button', class: 'boton boton-primario', onclick: () => hoja.cerrar() }, cantidad === 1 ? 'Ver 1 obra' : `Ver ${cantidad} obras`),
    );
  }

  if (!buscadorPropio) {
    const alBuscar = (e) => {
      if (!raiz.isConnected) { window.removeEventListener('medianeras:buscar', alBuscar); return; }
      buscador.value = e.detail;
      cambiar({ ...filtros, q: e.detail || undefined });
    };
    window.addEventListener('medianeras:buscar', alBuscar);
  }
  raiz.actualizarEstadisticas = (nuevas) => {
    estadisticas = nuevas;
    visitadas = new Set(estadisticas.keys());
    pintar();
  };
  pintar();
  return raiz;
}

