// Inicio: filas temáticas (filas.js), las décadas en grilla y el link a todas las obras.

import { el, agregar, flecha, encabezadoFila, filaHorizontal, esqueletoFila, mensaje } from '../ui.js';
import { entradasDiario, estadisticasVisitas, rutaPerfil, TIPOS_PERFIL, partituraDe, colorPerfil, partituraObra, colorMarco } from '../datos.js';
import { separador, simbolo, simboloNeutro } from '../grafica.js';
import { FILAS_INICIO, MAXIMO, decadasConObras } from '../filas.js';
import { enlacesIndices } from './perfil.js';
import { botonSugerirObra, pieDePagina } from '../contacto.js';

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

  agregar(contenedor, [separador('inicio:decadas', 360), decadas(datos),
    el('a', { class: 'todas-las-obras', href: '#/obras' },
      el('span', { class: 'todas-texto' }, el('strong', {}, 'Todas las obras'),
        el('span', { class: 'todas-datos' }, resumen().split(' · ').map((dato) => el('span', {}, dato)))),
      iconosObras(datos), flecha()),
    botonSugerirObra() && el('div', { class: 'sugerir-obra' }, botonSugerirObra()),
    el('nav', { class: 'explorar', 'aria-label': 'Explorar' }, encabezadoFila('Explorar'), el('div', { class: 'explorar-enlaces' }, enlacesIndices())),
    pieDePagina()]);
}

// El símbolo de cada obra en chiquito, como una tira de íconos. Si dos obras comparten dibujo
// (por ejemplo, el de su estilo), va una sola vez.
function iconosObras(datos) {
  const partituras = new Map();
  for (const obra of datos.obras) {
    const partitura = partituraObra(datos, obra) ?? simboloNeutro(colorMarco(obra));
    partituras.set(JSON.stringify(partitura), partitura);
  }
  return el('span', { class: 'todas-iconos', 'aria-hidden': 'true' }, [...partituras.values()].map((partitura) =>
    simbolo(partitura, { ancho: 100, alto: 100, margen: 8, fijo: true, superficie: 0.42, clase: 'todas-icono' })));
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

// Las décadas en grilla: el símbolo de cada una (colección Mundo) en una tapa, con nombre y cantidad.
function decadas(datos) {
  return el('section', { class: 'fila fila-decadas' },
    encabezadoFila('Por década'),
    el('div', { class: 'decadas-grilla' }, decadasConObras(datos).map(([decada, obras]) => {
      const color = colorPerfil('decada', decada, obras);
      return el('a', { class: 'decada', href: rutaPerfil('decada', decada) },
        el('div', { class: `tapa marco-${color}` },
          simbolo(partituraDe(datos, 'decada', decada) ?? simboloNeutro(color), { ancho: 100, alto: 100, margen: 8, fijo: true, superficie: 0.42, clase: 'tapa-grafica' })),
        el('span', { class: 'decada-nombre' }, `${decada}s`),
        el('span', { class: 'decada-cantidad' }, obras.length === 1 ? '1 obra' : `${obras.length} obras`));
    })),
  );
}

