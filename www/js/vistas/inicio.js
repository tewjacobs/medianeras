// Inicio: filas temáticas (filas.js), las décadas desplegables y el link a todas las obras.

import { el, icono, encabezadoFila, filaHorizontal, esqueletoFila, mensaje } from '../ui.js';
import { entradasDiario, estadisticasVisitas, rutaPerfil, TIPOS_PERFIL } from '../datos.js';
import { separador } from '../grafica.js';
import { ordenar } from '../filtros.js';
import { FILAS_INICIO, MAXIMO, decadasConObras } from '../filas.js';
import { leerPreferencia, guardarPreferencia } from '../plataforma/preferencias.js';
import { enlacesIndices } from './perfil.js';

export function render(contenedor, { datos }) {
  if (!datos.obras.length) {
    contenedor.append(mensaje('Todavía no hay obras', 'Cargalas en data/obras.json (ver README).'));
    return;
  }
  // Las visitas del teléfono pueden tardar: todo se pinta enseguida y las filas que dependen de
  // las visitas se completan cuando llegan.
  const entradas = entradasDiario(datos);
  const ctx = { datos, estadisticas: entradas.then(estadisticasVisitas) };

  const paises = new Set(datos.obras.flatMap(TIPOS_PERFIL.pais.valores));
  const plural = (n, uno, varios) => `${n} ${n === 1 ? uno : varios}`;
  const resumen = (visitas) => [plural(datos.obras.length, 'obra', 'obras'), visitas, plural(paises.size, 'país', 'países')].filter(Boolean).join(' · ');
  const linea = el('p', { class: 'resumen-inicio' }, resumen());
  contenedor.append(linea);
  entradas.then((lista) => { linea.textContent = resumen(plural(lista.length, 'visita', 'visitas')); });

  // Cada fila tiene su lugar fijo y se pinta apenas resuelve, con un esqueleto mientras tanto.
  for (const fila of FILAS_INICIO) {
    const lugar = el('section', { class: 'fila' }, esqueletoFila());
    contenedor.append(lugar);
    pintarFila(lugar, fila, ctx);
  }

  contenedor.append(separador('inicio:decadas', 360), decadas(datos), separador('inicio:todas', 360),
    el('a', { class: 'todas-las-obras', href: '#/obras' }, `Todas las obras (${datos.obras.length})`, icono('flecha')),
    el('nav', { class: 'explorar', 'aria-label': 'Explorar' }, encabezadoFila('Explorar'), el('div', { class: 'explorar-enlaces' }, enlacesIndices())));
}

async function pintarFila(lugar, fila, ctx) {
  try {
    const eleccion = fila.elegir ? fila.elegir(ctx) : undefined;
    if (fila.elegir && eleccion == null) { lugar.remove(); return; }
    const conVisitas = fila.visitas ? { ...ctx, estadisticas: await ctx.estadisticas } : ctx;
    const obras = (await fila.obras(conVisitas, eleccion)).slice(0, MAXIMO);
    if (!obras.length) { lugar.remove(); return; }
    const valor = (x) => (typeof x === 'function' ? x(ctx, eleccion) : x);
    lugar.replaceChildren(
      encabezadoFila(valor(fila.titulo), valor(fila.verMas), { subtitulo: fila.subtitulo && valor(fila.subtitulo) }),
      filaHorizontal(obras, { detalle: fila.detalle?.(conVisitas) }),
    );
  } catch (error) {
    console.warn(`No se pudo armar la fila "${fila.id}"`, error);
    lugar.remove();
  }
}

// Una fila desplegable por década. Las que se abren se recuerdan en el teléfono.
function decadas(datos) {
  let guardadas = [];
  try { guardadas = JSON.parse(leerPreferencia('decadas-abiertas', '[]')); } catch { /* se empieza con todas cerradas */ }
  const abiertas = new Set(Array.isArray(guardadas) ? guardadas : []);
  const guardar = () => guardarPreferencia('decadas-abiertas', JSON.stringify([...abiertas]));
  return el('section', { class: 'fila fila-decadas' },
    encabezadoFila('Por década'),
    decadasConObras(datos).map(([decada, obras]) => {
      const detalles = el('details', {
        class: 'decada', open: abiertas.has(decada),
        ontoggle: () => { if (detalles.open) abiertas.add(decada); else abiertas.delete(decada); guardar(); },
      },
      el('summary', {},
        el('span', { class: 'decada-nombre' }, `${decada}s`),
        el('span', { class: 'decada-puntos', 'aria-hidden': 'true' }),
        el('span', { class: 'decada-cantidad' }, obras.length),
      ),
      filaHorizontal(ordenar(obras, 'anio')),
      el('a', { class: 'ver-mas', href: rutaPerfil('decada', decada) }, `Ver la década de ${decada}`, icono('flecha')),
      );
      return detalles;
    }),
  );
}

