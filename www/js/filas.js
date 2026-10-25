// Filas del inicio. Cada fila dice de dónde salen sus obras y adónde lleva VER MÁS.
// `obras(ctx)` puede ser async (las filas sociales, más adelante, traerán datos de un servidor).
// Si devuelve una lista vacía, la fila no se muestra.

import { rutaPerfil, hoyISO, TIPOS_PERFIL } from './datos.js';
import { ordenar } from './filtros.js';
import { estrellas } from './ui.js';

export const MAXIMO = 12;

// ctx: { datos, estadisticas }. Las filas con `visitas: true` reciben `estadisticas` ya resuelto
// (Map obra_id → { ultima, visitas, promedio }); para las demás es una promesa que no hace falta esperar.
export const FILAS_INICIO = [
  {
    id: 'visitadas',
    visitas: true,
    titulo: 'Visitadas recientemente',
    obras: ({ datos, estadisticas }) => ordenar(datos.obras.filter((o) => estadisticas.has(o.id)), 'visita', { estadisticas }),
    verMas: '#/obras?orden=visita&visitadas=si',
  },
  {
    id: 'agregadas',
    titulo: 'Agregadas recientemente',
    obras: ({ datos }) => ordenar(datos.obras, 'agregada', { todas: datos.obras }),
    verMas: '#/obras?orden=agregada',
  },
  {
    id: 'puntuadas',
    visitas: true,
    titulo: 'Mejor puntuadas',
    obras: ({ datos, estadisticas }) => ordenar(datos.obras.filter((o) => estadisticas.get(o.id)?.promedio), 'puntaje', { estadisticas }),
    detalle: ({ estadisticas }) => (obra) => estrellas(Math.round(estadisticas.get(obra.id).promedio)),
    verMas: '#/obras?orden=puntaje&visitadas=si',
  },
  {
    // Rota por día entre quienes tienen 2 obras o más.
    id: 'arquitecto',
    elegir: ({ datos }) => {
      const conteo = new Map();
      for (const obra of datos.obras) for (const a of obra.arquitectos ?? []) conteo.set(a, (conteo.get(a) ?? 0) + 1);
      const candidatos = [...conteo].filter(([, n]) => n >= 2).map(([a]) => a).sort();
      if (!candidatos.length) return null;
      const dia = Math.floor(Date.parse(hoyISO()) / 86400000);
      return candidatos[dia % candidatos.length];
    },
    titulo: 'Del arquitecto/a',
    subtitulo: (ctx, arquitecto) => arquitecto,
    obras: ({ datos }, arquitecto) => ordenar(datos.obras.filter((o) => o.arquitectos?.includes(arquitecto)), 'anio'),
    verMas: (ctx, arquitecto) => rutaPerfil('arquitecto', arquitecto),
  },
  {
    id: 'este-anio',
    titulo: 'Construidas este año',
    obras: ({ datos }) => datos.obras.filter((o) => o.anio_finalizacion === new Date().getFullYear()),
    verMas: () => rutaPerfil('anio', String(new Date().getFullYear())),
  },
  // Más adelante: { id: 'amigos', titulo: 'Popular entre tus amigos', obras: async (ctx) => … }
];

// Décadas con obras, de la más reciente a la más vieja.
export function decadasConObras(datos) {
  const porDecada = new Map();
  for (const obra of datos.obras) {
    const [clave] = TIPOS_PERFIL.decada.valores(obra);
    if (!clave) continue;
    porDecada.set(clave, [...(porDecada.get(clave) ?? []), obra]);
  }
  return [...porDecada].sort((a, b) => Number(b[0]) - Number(a[0]));
}

