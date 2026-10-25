// Ficha de una obra. Siempre visibles arriba: la tapa, el nombre, años y arquitectos, y los
// botones. Debajo, pestañas (DATOS · UBICACIÓN · FOTOS · PLANOS; las que no tienen contenido no
// aparecen), y aparte las visitas, como reseñas: las más recientes y un VER MÁS a todas.
// #/obra/<id>/visitas es la página con todas las visitas de la obra.

import { el, icono, flecha, creditoFoto, tarjetaEntrada, mensaje, tapaObra, chipsPerfil, grillaFotos, encabezadoFila, estrellas, textoLargo } from '../ui.js';
import { abrirMapaObra } from './mapa.js';
import { abrirNuevaVisita } from './nueva-visita.js';
import { botonSugerirFoto } from '../contacto.js';
import { entradasDiario, tieneCoordenadas, NIVELES_UBICACION, ancestrosEstilo, rangoAnios, decadaClave, SIN_DATO, colorMarco, formatoFecha } from '../datos.js';

const RECIENTES = 3;

export async function render(contenedor, { datos, partes, titulo, recargar }) {
  const obra = datos.porId.get(partes[1]);
  if (!obra) {
    titulo('Obra no encontrada');
    contenedor.append(mensaje('No encontramos esa obra', `No hay ninguna obra con el id "${partes[1] ?? ''}".`,
      el('a', { class: 'boton', href: '#/obras' }, 'Ver todas las obras')));
    return;
  }
  contenedor.style.setProperty('--familia', `var(--${colorMarco(obra)})`);
  if (partes[2] === 'visitas') return renderVisitas(contenedor, { datos, obra, titulo });
  titulo(obra.nombre);

  const u = obra.ubicacion ?? {};
  const coordenadas = tieneCoordenadas(obra);
  const autoria = [rangoAnios(obra), ...(obra.arquitectos ?? [])].filter(Boolean).join(' · ');
  const comoLlegar = coordenadas && el('a', {
    class: 'boton', target: '_blank', rel: 'noopener',
    href: `https://maps.apple.com/?daddr=${u.lat},${u.lng}&q=${encodeURIComponent(obra.nombre)}`,
  }, flecha('paralela'), 'Cómo llegar');
  // "Ver en el mapa" y "Registrar visita" abren paneles; los links quedan por si el JS no llega.
  const enPanel = (accion) => (e) => { e.preventDefault(); accion(); };
  const botonMapa = () => coordenadas && el('a', {
    class: 'boton', href: `#/mapa?obra=${encodeURIComponent(obra.id)}`, onclick: enPanel(() => abrirMapaObra(obra)),
  }, icono('mapa'), 'Ver en el mapa');
  const verMapa = botonMapa();

  // En la compu, la tapa a la izquierda y lo principal a la derecha, a la misma altura.
  contenedor.append(
    el('div', { class: 'ficha-cabeza' },
    el('div', { class: 'ficha-tapa' }, tapaObra(obra, { grande: true })),
    el('div', { class: 'ficha' },
      el('div', { class: 'ficha-encabezado' },
        el('h2', { class: 'ficha-titulo' }, obra.nombre),
        autoria && el('p', { class: 'ficha-autoria' }, autoria),
        obra.otros_nombres?.length > 0 && el('p', { class: 'tenue' }, `También: ${obra.otros_nombres.join(' · ')}`),
      ),
      el('div', { class: 'acciones' },
        el('a', {
          class: 'boton boton-primario', href: `#/nueva?obra=${encodeURIComponent(obra.id)}`,
          onclick: enPanel(() => abrirNuevaVisita(datos, { obra: obra.id, alGuardar: recargar })),
        }, icono('mas'), 'Registrar visita'),
        verMapa,
        botonSugerirFoto(obra),
      ),
      // Debajo de los botones: el resumen (dos líneas) y, con "Ver más", la descripción completa.
      descripcionObra(obra),
    ),
    ),
    pestanas([
      ['Datos', panelDatos(datos, obra)],
      ['Ubicación', panelUbicacion(obra, [botonMapa(), comoLlegar])],
      obra.fotos?.length > 0 && ['Fotos', grillaFotos(obra.fotos, { alt: obra.nombre, pie: creditoFoto })],
      obra.planos?.length > 0 && ['Planos', grillaFotos(obra.planos, { alt: `Plano de ${obra.nombre}`, pie: creditoPlano })],
    ].filter(Boolean)),
  );

  const lugar = el('section', { class: 'ficha-visitas' });
  contenedor.append(lugar);
  const visitas = (await entradasDiario(datos)).filter((e) => e.obra_id === obra.id);
  lugar.append(
    encabezadoFila(visitas.length ? `Visitas (${visitas.length})` : 'Visitas', visitas.length ? `#/obra/${encodeURIComponent(obra.id)}/visitas` : null),
    visitas.length
      ? el('div', { class: 'resenas' }, visitas.slice(0, RECIENTES).map(resena))
      : el('p', { class: 'tenue ficha-sin-visitas' }, 'Todavía no registraste visitas a esta obra.'),
  );
}

// Pestañas: solo se ve el panel elegido.
function pestanas(paneles) {
  const botones = [];
  const cuerpos = paneles.map(([nombre, contenido], i) => {
    const id = `panel-${nombre.toLowerCase().normalize('NFD').replace(/[^a-z]/g, '')}`;
    botones.push(el('button', {
      type: 'button', role: 'tab', id: `${id}-pestana`, 'aria-controls': id, 'aria-selected': String(i === 0),
      onclick: () => elegir(i),
    }, nombre));
    return el('div', { class: 'panel-ficha', role: 'tabpanel', id, 'aria-labelledby': `${id}-pestana`, hidden: i !== 0 }, contenido);
  });
  function elegir(i) {
    botones.forEach((b, k) => b.setAttribute('aria-selected', String(k === i)));
    cuerpos.forEach((c, k) => { c.hidden = k !== i; });
  }
  return el('div', { class: 'ficha-pestanas' }, el('div', { class: 'pestanas-ficha', role: 'tablist' }, botones), cuerpos);
}

// Los datos como chips que llevan a su perfil.
function panelDatos(datos, obra) {
  const anios = [obra.anio_proyecto, obra.anio_finalizacion].filter(Number.isFinite).map(String).filter((v, i, a) => a.indexOf(v) === i);
  const filas = [
    ['Arquitectos', obra.arquitectos?.length && chipsPerfil('arquitecto', obra.arquitectos)],
    [obra.anio_proyecto && obra.anio_finalizacion && anios.length > 1 ? 'Proyecto · fin' : 'Año', anios.length && chipsPerfil('anio', anios)],
    ['Década', decadaClave(obra) !== SIN_DATO && chipsPerfil('decada', [decadaClave(obra)])],
    ['Estilo', obra.estilo && chipsPerfil('estilo', [...ancestrosEstilo(datos, obra.estilo).reverse(), obra.estilo])],
    ['Materiales', obra.materiales?.length && chipsPerfil('material', obra.materiales)],
    ['Programa', obra.programa && chipsPerfil('programa', [obra.programa])],
    ['Estado', obra.estado && chipsPerfil('estado', [obra.estado])],
  ].filter(([, v]) => v);
  const listas = datos.listas.filter((l) => l.obras.includes(obra.id));
  return [
    el('dl', { class: 'ficha-datos' }, filas.map(([nombre, valor]) => [el('dt', {}, nombre), el('dd', {}, valor)])),
    listas.length > 0 && el('dl', { class: 'ficha-datos' }, el('dt', {}, 'En listas'), el('dd', {},
      el('div', { class: 'chips-datos' }, listas.map((l) => el('a', { class: 'chip-dato', href: `#/lista/${encodeURIComponent(l.id)}` }, l.titulo))))),
  ];
}

// "resumen": una o dos líneas. "descripcion": el texto completo, que reemplaza al resumen al
// tocar "Ver más". Si hay solo uno de los dos, se muestra ese (cortado si es largo).
function descripcionObra(obra) {
  const { resumen, descripcion } = obra;
  if (!resumen) return descripcion ? textoLargo(descripcion, { lineas: 2, clase: 'ficha-descripcion' }) : null;
  const texto = el('p', { class: 'ficha-descripcion texto-largo abierta' }, resumen);
  if (!descripcion) return texto;
  const boton = el('button', { type: 'button', class: 'mas', onclick: () => { texto.textContent = descripcion; boton.remove(); } }, 'Ver más');
  return el('div', { class: 'texto-largo-caja' }, texto, boton);
}

function panelUbicacion(obra, botones) {
  const u = obra.ubicacion ?? {};
  const niveles = NIVELES_UBICACION.filter((n) => u[n]);
  return [
    niveles.length > 0 && el('div', { class: 'chips-datos' }, niveles.map((n) => chipsPerfil(n, [u[n]]).firstChild)),
    u.direccion && el('p', { class: 'ficha-direccion' }, u.direccion),
    tieneCoordenadas(obra) && el('p', { class: 'ficha-coordenadas' }, `${u.lat}, ${u.lng}`),
    botones.some(Boolean) && el('div', { class: 'acciones' }, botones),
  ];
}

// Planos: mismo crédito que las fotos, con el tipo (planta, corte, vista) adelante.
function creditoPlano(plano) {
  const pie = creditoFoto(plano);
  if (plano.tipo || plano.pie) pie.prepend(`${[plano.tipo, plano.pie].filter(Boolean).join(' · ')} · `);
  return pie;
}

// Una visita como reseña: fecha, puntaje y nota.
function resena(entrada) {
  return el('article', { class: 'resena' },
    el('header', { class: 'resena-cabecera' },
      el('time', { datetime: entrada.fecha }, formatoFecha(entrada.fecha)),
      estrellas(entrada.puntaje),
      entrada.local && el('span', { class: 'marca-local' }, 'En el teléfono'),
    ),
    entrada.nota && el('p', { class: 'resena-nota' }, entrada.nota),
  );
}

async function renderVisitas(contenedor, { datos, obra, titulo }) {
  titulo(`Visitas · ${obra.nombre}`);
  const visitas = (await entradasDiario(datos)).filter((e) => e.obra_id === obra.id);
  contenedor.append(
    el('div', { class: 'perfil' },
      el('nav', { class: 'migas' }, el('a', { href: `#/obra/${encodeURIComponent(obra.id)}` }, obra.nombre)),
      el('h2', { class: 'perfil-nombre' }, 'Visitas'),
      el('p', { class: 'perfil-datos' }, visitas.length === 1 ? '1 visita' : `${visitas.length} visitas`),
    ),
    visitas.length
      ? el('div', { class: 'entradas' }, visitas.map((e) => tarjetaEntrada(e, datos, { conObra: false })))
      : el('p', { class: 'tenue ficha-sin-visitas' }, 'Todavía no registraste visitas a esta obra.'),
  );
}
