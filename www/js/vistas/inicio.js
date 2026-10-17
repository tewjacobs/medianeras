// Inicio: grilla de obras con búsqueda y filtros. El estado de los filtros vive en la URL.

import { el, icono, tarjetaObra, mensaje, abrirHoja } from '../ui.js';
import { compararTexto } from '../datos.js';
import { FACETAS, leerFiltros, filtrosAQuery, conFiltro, filtrar, opciones, filtrosActivos } from '../filtros.js';

export function render(contenedor, { datos, params }) {
  let filtros = leerFiltros(params);
  const obras = [...datos.obras].sort((a, b) => compararTexto(a.nombre, b.nombre));

  const buscador = el('input', {
    type: 'search', class: 'buscador', placeholder: 'Buscar obra, arquitecto/a…', 'aria-label': 'Buscar',
    value: filtros.q ?? '', enterkeyhint: 'search', autocomplete: 'off',
    oninput: () => cambiar({ ...filtros, q: buscador.value.trim() || undefined }),
  });
  const contadorFiltros = el('span', { class: 'insignia' });
  const botonFiltros = el('button', { type: 'button', class: 'boton boton-filtros', onclick: abrirFiltros }, icono('filtros'), 'Filtros', contadorFiltros);
  const chips = el('div', { class: 'chips' });
  const resumen = el('p', { class: 'resumen tenue' });
  const grilla = el('div', { class: 'grilla' });

  contenedor.append(el('div', { class: 'barra-herramientas' }, buscador, botonFiltros), chips, resumen, grilla);

  let hoja = null;

  function cambiar(nuevos) {
    filtros = nuevos;
    const query = filtrosAQuery(filtros);
    history.replaceState(null, '', query ? `#/?${query}` : '#/');
    pintar();
  }

  function pintar() {
    const resultado = filtrar(obras, filtros);
    const activos = filtrosActivos(filtros);

    contadorFiltros.textContent = activos.length || '';
    contadorFiltros.hidden = activos.length === 0;
    chips.replaceChildren(...activos.map(({ faceta, nombre }) => el('button', {
      type: 'button', class: 'chip', 'aria-label': `Quitar filtro ${faceta.etiqueta}: ${nombre}`,
      onclick: () => cambiar(conFiltro(filtros, faceta.clave, null)),
    }, nombre, el('span', { 'aria-hidden': 'true' }, '×'))));

    resumen.textContent = resultado.length === 1 ? '1 obra' : `${resultado.length} obras`;
    grilla.replaceChildren(...resultado.map((obra) => tarjetaObra(obra)));
    if (resultado.length === 0) {
      grilla.append(datos.obras.length === 0
        ? mensaje('Todavía no hay obras', 'Cargalas en data/obras.json (ver README).')
        : mensaje('Ninguna obra coincide', 'Probá sacando algún filtro.', el('button', { type: 'button', class: 'boton', onclick: limpiar }, 'Limpiar filtros')));
    }
    if (hoja) pintarHoja(resultado.length);
  }

  function limpiar() {
    buscador.value = '';
    cambiar({});
  }

  function abrirFiltros() {
    hoja = abrirHoja({ titulo: 'Filtros', contenido: el('div', { class: 'formulario' }), pie: [], alCerrar: () => { hoja = null; } });
    pintar();
  }

  function pintarHoja(cantidad) {
    const campos = FACETAS.map((faceta) => {
      const lista = opciones(obras, filtros, faceta);
      const bloqueado = faceta.padre && !filtros[faceta.padre];
      if (lista.length === 0 && !filtros[faceta.clave]) return null;
      const select = el('select', {
        id: `filtro-${faceta.clave}`, disabled: bloqueado,
        onchange: () => cambiar(conFiltro(filtros, faceta.clave, select.value || null)),
      },
      el('option', { value: '' }, bloqueado ? `Elegí antes ${FACETAS.find((f) => f.clave === faceta.padre).etiqueta.toLowerCase()}` : 'Todos'),
      lista.map(({ valor, nombre, cantidad: n }) => el('option', { value: valor, selected: filtros[faceta.clave] === valor }, `${nombre} (${n})`)));
      return el('label', { class: 'campo', for: select.id }, el('span', {}, faceta.etiqueta), select);
    });
    hoja.cuerpo.firstChild.replaceChildren(...campos.filter(Boolean));
    hoja.pie.replaceChildren(
      el('button', { type: 'button', class: 'boton', onclick: limpiar }, 'Limpiar'),
      el('button', { type: 'button', class: 'boton boton-primario', onclick: () => hoja.cerrar() }, cantidad === 1 ? 'Ver 1 obra' : `Ver ${cantidad} obras`),
    );
  }

  pintar();
}
