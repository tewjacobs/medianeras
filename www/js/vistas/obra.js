// Ficha de una obra: fotos con crédito, datos, listas que la incluyen y mis visitas.

import { el, icono, galeria, creditoFoto, sinFoto, marcaEjemplo, tarjetaEntrada, mensaje } from '../ui.js';
import { entradasDiario, tieneCoordenadas, NIVELES_UBICACION } from '../datos.js';
import { rutaFiltrada, faceta } from '../filtros.js';

const ESTADOS = { existente: 'Existente', demolida: 'Demolida', modificada: 'Modificada' };

export async function render(contenedor, { datos, partes, titulo }) {
  const obra = datos.porId.get(partes[1]);
  if (!obra) {
    titulo('Obra no encontrada');
    contenedor.append(mensaje('No encontramos esa obra', `No hay ninguna obra con el id "${partes[1] ?? ''}".`,
      el('a', { class: 'boton', href: '#/' }, 'Ver todas las obras')));
    return;
  }
  titulo(obra.nombre);

  const u = obra.ubicacion ?? {};
  const fotos = obra.fotos ?? [];
  const enlace = (clave, valor) => el('a', { href: rutaFiltrada({ [clave]: valor }) }, valor);
  const enlaces = (clave, valores) => valores.flatMap((v, i) => (i ? [', ', enlace(clave, v)] : [enlace(clave, v)]));

  // Migas de ubicación: cada nivel lleva a la grilla filtrada hasta ese nivel.
  const migas = [];
  const acumulado = {};
  for (const nivel of NIVELES_UBICACION) {
    if (!u[nivel]) break;
    acumulado[nivel] = u[nivel];
    if (migas.length) migas.push(' › ');
    migas.push(el('a', { href: rutaFiltrada({ ...acumulado }), title: faceta(nivel).etiqueta }, u[nivel]));
  }

  const filas = [
    ['Arquitectos', obra.arquitectos?.length ? enlaces('arquitecto', obra.arquitectos) : null],
    ['Proyecto', obra.anio_proyecto],
    ['Finalización', obra.anio_finalizacion],
    ['Estilo', obra.estilo && enlace('estilo', obra.estilo)],
    ['Materiales', obra.materiales?.length ? enlaces('material', obra.materiales) : null],
    ['Programa', obra.programa && enlace('programa', obra.programa)],
    ['Estado', ESTADOS[obra.estado] ?? obra.estado],
    ['Ubicación', migas.length ? migas : null],
    ['Dirección', u.direccion],
  ].filter(([, valor]) => valor != null && valor !== '');

  const coordenadas = tieneCoordenadas(obra);
  const listas = datos.listas.filter((l) => l.obras.includes(obra.id));

  contenedor.append(
    el('div', { class: 'ficha-fotos' },
      fotos.length ? galeria(fotos, { alt: obra.nombre, pie: creditoFoto }) : sinFoto(),
    ),
    el('div', { class: 'ficha' },
      el('div', { class: 'ficha-encabezado' },
        obra.ejemplo && marcaEjemplo(),
        el('h2', { class: 'ficha-titulo' }, obra.nombre),
        obra.otros_nombres?.length > 0 && el('p', { class: 'tenue' }, `También: ${obra.otros_nombres.join(' · ')}`),
      ),
      el('div', { class: 'acciones' },
        el('a', { class: 'boton boton-primario', href: `#/nueva?obra=${encodeURIComponent(obra.id)}` }, icono('mas'), 'Registrar visita'),
        coordenadas && el('a', { class: 'boton', href: `#/mapa?obra=${encodeURIComponent(obra.id)}` }, icono('mapa'), 'Ver en el mapa'),
        coordenadas && el('a', {
          class: 'boton', target: '_blank', rel: 'noopener',
          href: `https://maps.apple.com/?daddr=${u.lat},${u.lng}&q=${encodeURIComponent(obra.nombre)}`,
        }, icono('ruta'), 'Cómo llegar'),
      ),
      obra.descripcion && el('p', { class: 'ficha-descripcion' }, obra.descripcion),
      el('dl', { class: 'ficha-datos' }, filas.map(([nombre, valor]) => [el('dt', {}, nombre), el('dd', {}, valor)])),
      listas.length > 0 && el('section', { class: 'ficha-seccion' },
        el('h3', {}, 'En listas'),
        el('div', { class: 'chips' }, listas.map((l) => el('a', { class: 'chip', href: `#/lista/${encodeURIComponent(l.id)}` }, l.titulo))),
      ),
    ),
  );

  const visitas = (await entradasDiario(datos)).filter((e) => e.obra_id === obra.id);
  contenedor.querySelector('.ficha').append(el('section', { class: 'ficha-seccion' },
    el('h3', {}, visitas.length ? `Mis visitas (${visitas.length})` : 'Mis visitas'),
    visitas.length
      ? el('div', { class: 'entradas' }, visitas.map((e) => tarjetaEntrada(e, datos, { conObra: false })))
      : el('p', { class: 'tenue' }, 'Todavía no registraste visitas a esta obra.'),
  ));
}
