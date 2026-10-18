// Ficha de una obra: la tapa grande, los datos (cada uno lleva a su perfil), las fotos con
// crédito, las listas que la incluyen y mis visitas.

import { el, icono, galeria, creditoFoto, tarjetaEntrada, mensaje, tapaObra, enlacePerfil, enlacesPerfil } from '../ui.js';
import { entradasDiario, tieneCoordenadas, NIVELES_UBICACION, ancestrosEstilo, rangoAnios, decadaClave, anioReferencia } from '../datos.js';

export async function render(contenedor, { datos, partes, titulo }) {
  const obra = datos.porId.get(partes[1]);
  if (!obra) {
    titulo('Obra no encontrada');
    contenedor.append(mensaje('No encontramos esa obra', `No hay ninguna obra con el id "${partes[1] ?? ''}".`,
      el('a', { class: 'boton', href: '#/obras' }, 'Ver todas las obras')));
    return;
  }
  titulo(obra.nombre);

  const u = obra.ubicacion ?? {};
  const fotos = obra.fotos ?? [];
  const anio = (a) => Number.isFinite(a) && enlacePerfil('anio', String(a));

  // Ubicación: cada nivel lleva a su perfil.
  const migas = [];
  for (const nivel of NIVELES_UBICACION) {
    if (!u[nivel]) break;
    if (migas.length) migas.push(' › ');
    migas.push(enlacePerfil(nivel, u[nivel]));
  }
  // Estilo con su familia: "Moderno › Arquitectura orgánica".
  const estilo = obra.estilo && [...ancestrosEstilo(datos, obra.estilo).reverse(), obra.estilo]
    .flatMap((e, i) => (i ? [' › ', enlacePerfil('estilo', e)] : [enlacePerfil('estilo', e)]));

  const filas = [
    ['Arquitectos', obra.arquitectos?.length ? enlacesPerfil('arquitecto', obra.arquitectos) : null],
    ['Proyecto', anio(obra.anio_proyecto)],
    ['Finalización', anio(obra.anio_finalizacion)],
    ['Década', anioReferencia(obra) !== null && enlacePerfil('decada', decadaClave(obra))],
    ['Estilo', estilo],
    ['Materiales', obra.materiales?.length ? enlacesPerfil('material', obra.materiales) : null],
    ['Programa', obra.programa && enlacePerfil('programa', obra.programa)],
    ['Estado', obra.estado && enlacePerfil('estado', obra.estado)],
    ['Ubicación', migas.length ? migas : null],
    ['Dirección', u.direccion],
  ].filter(([, valor]) => valor != null && valor !== '' && valor !== false);
  const autoria = [rangoAnios(obra), ...(obra.arquitectos ?? [])].filter(Boolean).join(' · ');

  const coordenadas = tieneCoordenadas(obra);
  const listas = datos.listas.filter((l) => l.obras.includes(obra.id));

  contenedor.append(
    el('div', { class: 'ficha-tapa' }, tapaObra(obra, { grande: true })),
    el('div', { class: 'ficha' },
      el('div', { class: 'ficha-encabezado' },
        el('h2', { class: 'ficha-titulo' }, obra.nombre),
        autoria && el('p', { class: 'ficha-autoria' }, autoria),
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
      fotos.length > 0 && el('section', { class: 'ficha-seccion ficha-galeria' },
        el('h3', {}, fotos.length === 1 ? 'Foto' : `Fotos (${fotos.length})`),
        galeria(fotos, { alt: obra.nombre, pie: creditoFoto }),
      ),
      listas.length > 0 && el('section', { class: 'ficha-seccion' },
        el('h3', {}, 'En listas'),
        el('div', { class: 'chips' }, listas.map((l) => el('a', { class: 'chip', href: `#/lista/${encodeURIComponent(l.id)}` }, l.titulo))),
      ),
    ),
  );

  // Las fotos de la visita que ya están en la galería de arriba no se repiten.
  const enGaleria = new Set(fotos.map((f) => f.archivo));
  const visitas = (await entradasDiario(datos))
    .filter((e) => e.obra_id === obra.id)
    .map((e) => ({ ...e, fotos: (e.fotos ?? []).filter((f) => !enGaleria.has(f.archivo)) }));
  contenedor.querySelector('.ficha').append(el('section', { class: 'ficha-seccion' },
    el('h3', {}, visitas.length ? `Mis visitas (${visitas.length})` : 'Mis visitas'),
    visitas.length
      ? el('div', { class: 'entradas' }, visitas.map((e) => tarjetaEntrada(e, datos, { conObra: false })))
      : el('p', { class: 'tenue' }, 'Todavía no registraste visitas a esta obra.'),
  ));
}
