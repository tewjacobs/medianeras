// Sugerencias (por mail, con el texto ya escrito) y contacto del proyecto.
// Sin mail cargado, los botones de sugerir no aparecen.

import { el, icono, flecha, encabezadoFila } from './ui.js';

export const CONTACTO = {
  mail: null,
  instagram: 'jagten.arq',
};

const mailto = (asunto, cuerpo) =>
  `mailto:${CONTACTO.mail}?subject=${encodeURIComponent(asunto)}&body=${encodeURIComponent(cuerpo)}`;

// Las fotos que manda otra persona necesitan su permiso y su nombre para el crédito.
const PERMISO = `- ¿La sacaste vos?
- ¿Con qué nombre te damos el crédito?
- ¿Nos das permiso para publicarla en jagten?`;

export function botonSugerirFoto(obra) {
  if (!CONTACTO.mail) return null;
  return el('a', {
    class: 'boton boton-sugerir',
    href: mailto(`Sugerencia de foto: ${obra.nombre}`, `Obra: ${obra.nombre} (${obra.id})

Adjuntá la foto a este mail y contanos:
${PERMISO}
- ¿Cuándo la sacaste, más o menos?
`),
  }, icono('camara'), 'Sugerir foto');
}

export function botonSugerirObra() {
  if (!CONTACTO.mail) return null;
  return el('a', {
    class: 'boton boton-sugerir',
    href: mailto('Sugerencia de obra', `Nombre de la obra:
Arquitecto/a:
Año:
Lugar (ciudad y país):
Dónde leer sobre ella (link o libro):

Si tenés fotos propias, adjuntalas y contanos:
${PERMISO}
`),
  }, icono('inicio'), 'Sugerir una obra');
}

// Bloque del pie del inicio: los canales de contacto, aparte de las sugerencias.
export function bloqueContacto() {
  const canales = [
    CONTACTO.instagram && ['Instagram', `@${CONTACTO.instagram}`, `https://www.instagram.com/${CONTACTO.instagram}/`],
    CONTACTO.mail && ['Mail', CONTACTO.mail, `mailto:${CONTACTO.mail}`],
  ].filter(Boolean);
  return el('section', { class: 'contacto' }, encabezadoFila('Contacto'),
    el('div', { class: 'contacto-enlaces' }, canales.map(([nombre, dato, href]) =>
      el('a', { href, target: href.startsWith('http') ? '_blank' : null, rel: 'noopener' },
        el('span', {}, el('strong', {}, nombre), el('span', {}, dato)), flecha()))));
}
