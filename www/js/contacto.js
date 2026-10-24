// Sugerencias (por mail, con el texto ya escrito) y contacto del proyecto.
// Sin mail cargado, los botones de sugerir no aparecen.

import { el, icono } from './ui.js';

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

// Pie de página del inicio, como el de Letterboxd: secciones, redes y la línea de derechos.
// Las redes sin cuenta todavía se muestran sin link.
export function pieDePagina() {
  const redes = [
    ['instagram', 'Instagram', CONTACTO.instagram && `https://www.instagram.com/${CONTACTO.instagram}/`],
    ['tiktok', 'TikTok'],
    ['youtube', 'YouTube'],
    ['x', 'X'],
    ['mail', 'Mail', CONTACTO.mail && `mailto:${CONTACTO.mail}`],
  ];
  return el('footer', { class: 'pie', 'data-tema': 'oscuro' },
    el('nav', { class: 'pie-enlaces', 'aria-label': 'Secciones' },
      [['Todas las obras', '#/obras'], ['Mapa', '#/mapa'], ['Diario', '#/diario'], ['Listas', '#/listas']]
        .map(([texto, href]) => el('a', { href }, texto))),
    el('div', { class: 'pie-redes' }, redes.map(([nombre, etiqueta, href]) => href
      ? el('a', { href, 'aria-label': etiqueta, title: etiqueta, target: href.startsWith('http') ? '_blank' : null, rel: 'noopener' }, icono(nombre))
      : el('span', { class: 'pie-sin-enlace', title: `${etiqueta}: próximamente` }, icono(nombre)))),
    CONTACTO.instagram && el('p', { class: 'pie-cuenta' }, `@${CONTACTO.instagram}`),
    el('p', { class: 'pie-legal' }, `© ${new Date().getFullYear()} jagten. Fotos del catálogo: todos los derechos reservados.`));
}
