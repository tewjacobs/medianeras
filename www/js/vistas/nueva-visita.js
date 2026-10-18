// Registrar (o editar) una visita desde el teléfono. Se guarda en el dispositivo
// hasta que se exporta desde el Diario.

import { el, icono, botonIcono, filaObra, urlTemporal, mensaje, aviso, abrirHoja, cerrarHoja } from '../ui.js';
import { hoyISO, normalizar, lugarCorto, compararTexto, tieneCoordenadas, distanciaKm, formatoDistancia } from '../datos.js';
import { obtenerVisita, guardarVisita, borrarVisita, listarVisitas, pedirPersistencia } from '../plataforma/almacen.js';
import { obtenerUbicacion, ultimaUbicacion } from '../plataforma/ubicacion.js';
import { elegirFotos, prepararFoto } from '../plataforma/fotos.js';

const MAX_RESULTADOS = 12;

// Como panel (desde el botón VISITA o desde una obra): `obra` viene elegida; `sugeridas` (ids)
// aparecen primero en la lista. Al guardar se cierra el panel y se queda en la vista actual.
export function abrirNuevaVisita(datos, { obra = null, sugeridas = [], alGuardar } = {}) {
  const contenido = el('div', { class: 'visita-panel' });
  abrirHoja({ titulo: 'Nueva visita', contenido, clase: 'hoja-alta' });
  render(contenido, {
    datos, params: new URLSearchParams(obra ? { obra } : {}), titulo: () => {}, sugeridas,
    alTerminar: () => { cerrarHoja(); alGuardar?.(); },
  });
}

// `alTerminar`: en un panel, qué hacer después de guardar (en la página, se va al Diario).
export async function render(contenedor, { datos, params, titulo, sugeridas = [], alTerminar }) {
  const primero = new Set(sugeridas);
  const idEditar = params.get('editar');
  const original = idEditar ? await obtenerVisita(idEditar).catch(() => null) : null;
  if (idEditar && !original) {
    titulo('Visita no encontrada');
    contenedor.append(mensaje('No encontramos esa visita', 'Solo se pueden editar las visitas guardadas en este teléfono.', el('a', { class: 'boton', href: '#/diario' }, 'Ir al diario')));
    return;
  }
  titulo(original ? 'Editar visita' : 'Nueva visita');

  const estado = {
    obra: datos.porId.get(original?.obra_id ?? params.get('obra')) ?? null,
    puntaje: original?.puntaje ?? null,
    fotos: (original?.fotos ?? []).map((f) => ({ ...f })),
  };

  // ---- Obra ----
  const selector = el('div', { class: 'selector-obra' });
  const busqueda = el('input', {
    type: 'search', placeholder: 'Buscar en el catálogo…', 'aria-label': 'Buscar obra', autocomplete: 'off', enterkeyhint: 'search',
    oninput: pintarResultados,
    onkeydown: (e) => { if (e.key === 'Enter') e.preventDefault(); },
  });
  const resultados = el('div', { class: 'filas' });
  const botonCerca = el('button', { type: 'button', class: 'boton', onclick: buscarCerca }, icono('ubicacion'), 'Cerca mío');

  function pintarSelector() {
    if (estado.obra) {
      selector.replaceChildren(
        filaObra(estado.obra, { alTocar: cambiarObra }),
        el('button', { type: 'button', class: 'boton boton-chico', onclick: cambiarObra }, 'Cambiar obra'),
      );
    } else {
      selector.replaceChildren(el('div', { class: 'barra-herramientas' }, busqueda, botonCerca), resultados);
      pintarResultados();
    }
  }

  function cambiarObra() {
    estado.obra = null;
    pintarSelector();
    busqueda.focus();
  }

  function pintarResultados() {
    const q = normalizar(busqueda.value);
    const posicion = ultimaUbicacion();
    const km = (o) => (posicion && tieneCoordenadas(o) ? distanciaKm(posicion, o.ubicacion) : Infinity);
    const lista = datos.obras
      .filter((o) => !q || normalizar([o.nombre, ...(o.otros_nombres ?? []), ...(o.arquitectos ?? []), lugarCorto(o)].join(' ')).includes(q))
      .sort((a, b) => (primero.has(b.id) - primero.has(a.id)) || (posicion ? km(a) - km(b) : 0) || compararTexto(a.nombre, b.nombre));
    resultados.replaceChildren(...lista.slice(0, MAX_RESULTADOS).map((obra) => filaObra(obra, {
      detalle: Number.isFinite(km(obra)) ? `${formatoDistancia(km(obra))} · ${lugarCorto(obra)}` : undefined,
      alTocar: () => { estado.obra = obra; pintarSelector(); },
    })));
    if (!lista.length) resultados.append(el('p', { class: 'tenue' }, 'No hay obras que coincidan. Solo se pueden registrar visitas a obras del catálogo.'));
    else if (lista.length > MAX_RESULTADOS) resultados.append(el('p', { class: 'tenue' }, `y ${lista.length - MAX_RESULTADOS} más: escribí para buscar.`));
  }

  async function buscarCerca() {
    botonCerca.disabled = true;
    try {
      await obtenerUbicacion();
      busqueda.value = '';
      pintarResultados();
    } catch (error) {
      aviso(error.message, { duracion: 7000 });
    } finally {
      botonCerca.disabled = false;
    }
  }

  // ---- Fecha y nota ----
  const fecha = el('input', { type: 'date', id: 'visita-fecha', value: original?.fecha ?? hoyISO(), max: hoyISO(), required: true });
  const nota = el('textarea', { id: 'visita-nota', rows: 5, placeholder: '¿Qué viste? ¿Qué te llamó la atención?' });
  nota.value = original?.nota ?? '';

  // ---- Puntaje ----
  const puntaje = el('div', { class: 'puntaje', role: 'radiogroup', 'aria-label': 'Puntaje' });
  function pintarPuntaje() {
    puntaje.replaceChildren(
      ...[1, 2, 3, 4, 5].map((n) => el('button', {
        type: 'button', role: 'radio', class: n <= (estado.puntaje ?? 0) ? 'activa' : '',
        'aria-checked': String(estado.puntaje === n), 'aria-label': `${n} de 5`,
        onclick: () => { estado.puntaje = estado.puntaje === n ? null : n; pintarPuntaje(); },
      }, '★')),
      el('span', { class: 'tenue' }, estado.puntaje ? 'Tocá de nuevo para quitarlo' : 'Opcional'),
    );
  }

  // ---- Fotos ----
  const listaFotos = el('div', { class: 'fotos-visita' });
  const estadoFotos = el('span', { class: 'tenue', role: 'status' });
  const botonFotos = el('button', { type: 'button', class: 'boton', onclick: agregarFotos }, icono('camara'), 'Agregar fotos');

  async function agregarFotos() {
    const archivos = await elegirFotos();
    if (!archivos.length) return;
    botonFotos.disabled = true;
    try {
      for (const [i, archivo] of archivos.entries()) {
        estadoFotos.textContent = `Preparando foto ${i + 1} de ${archivos.length}…`;
        estado.fotos.push({ blob: await prepararFoto(archivo), pie: '' });
      }
    } finally {
      botonFotos.disabled = false;
      estadoFotos.textContent = '';
      pintarFotos();
    }
  }

  function pintarFotos() {
    listaFotos.replaceChildren(...estado.fotos.map((foto, i) => el('div', { class: 'foto-visita' },
      el('img', { src: urlTemporal(foto.blob), alt: `Foto ${i + 1}` }),
      el('input', {
        type: 'text', value: foto.pie ?? '', placeholder: 'Pie de foto (opcional)', 'aria-label': `Pie de la foto ${i + 1}`,
        oninput: (e) => { foto.pie = e.target.value; },
        onkeydown: (e) => { if (e.key === 'Enter') e.preventDefault(); },
      }),
      botonIcono('cerrar', `Quitar foto ${i + 1}`, () => { estado.fotos.splice(i, 1); pintarFotos(); }, 'foto-quitar'),
    )));
  }

  // ---- Guardar / borrar ----
  const botonGuardar = el('button', { type: 'submit', class: 'boton boton-primario boton-ancho' }, original ? 'Guardar cambios' : 'Guardar visita');

  async function guardar(evento) {
    evento.preventDefault();
    if (!estado.obra) {
      aviso('Elegí la obra que visitaste');
      selector.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }
    if (!fecha.value) {
      aviso('Poné la fecha de la visita');
      fecha.focus();
      return;
    }
    botonGuardar.disabled = true;
    const ahora = new Date().toISOString();
    try {
      await guardarVisita({
        id: original?.id ?? (await nuevoId(fecha.value, estado.obra.id, datos)),
        obra_id: estado.obra.id,
        fecha: fecha.value,
        nota: nota.value.trim(),
        puntaje: estado.puntaje,
        fotos: estado.fotos.map(({ blob, pie }) => ({ blob, pie: (pie ?? '').trim() })),
        creada: original?.creada ?? ahora,
        modificada: ahora,
        exportada: false,
      });
    } catch (error) {
      console.error(error);
      aviso(`No se pudo guardar la visita: ${error.message}`, { duracion: 8000 });
      botonGuardar.disabled = false;
      return;
    }
    pedirPersistencia();
    aviso(original ? 'Visita actualizada' : 'Visita guardada en este teléfono');
    if (alTerminar) alTerminar();
    else location.replace('#/diario');
  }

  async function borrar() {
    if (!confirm('¿Borrar esta visita del teléfono? No se puede deshacer.')) return;
    await borrarVisita(original.id);
    aviso('Visita borrada');
    location.replace('#/diario');
  }

  const campo = (etiqueta, control, paraId) => el('div', { class: 'campo' }, el(paraId ? 'label' : 'span', { class: 'campo-etiqueta', for: paraId }, etiqueta), control);

  contenedor.append(el('form', { class: 'formulario formulario-visita', novalidate: true, onsubmit: guardar },
    campo('Obra', selector),
    campo('Fecha', fecha, 'visita-fecha'),
    campo('Puntaje', puntaje),
    campo('Nota', nota, 'visita-nota'),
    campo('Fotos', el('div', {}, listaFotos, el('div', { class: 'acciones' }, botonFotos, estadoFotos))),
    el('div', { class: 'acciones-formulario' },
      botonGuardar,
      original && el('button', { type: 'button', class: 'boton boton-peligro', onclick: borrar }, icono('basura'), 'Borrar visita'),
    ),
    !original && el('p', { class: 'tenue nota-pie' }, 'La visita queda guardada en este teléfono. Desde el Diario la exportás para sumarla al repositorio.'),
  ));

  pintarSelector();
  pintarPuntaje();
  pintarFotos();
}

// "AAAA-MM-DD-obra", con -2, -3… si ya existe.
async function nuevoId(fecha, obraId, datos) {
  const usados = new Set([...datos.diario.map((e) => e.id), ...(await listarVisitas().catch(() => [])).map((v) => v.id)]);
  const base = `${fecha}-${obraId}`;
  let id = base;
  for (let n = 2; usados.has(id); n++) id = `${base}-${n}`;
  return id;
}
