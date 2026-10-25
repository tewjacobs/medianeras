// Carga de los JSON de /data, índices y funciones de formato.
// No hay ningún lugar, estilo ni arquitecto escrito acá: todo sale de los datos.

import { listarVisitas } from './plataforma/almacen.js';
import { hashTexto, registrarColoresSimbolos } from './grafica.js';

export const SIN_DATO = '_';

let promesa = null;
let actuales = null; // los datos ya indexados, para las funciones que no los reciben (color del marco)

export function cargarDatos() {
  // obras, diario y listas son obligatorios; perfiles y símbolos son optativos: si faltan o
  // tienen un error, la app arranca igual sin ellos.
  promesa ??= Promise.all([
    ...['obras', 'diario', 'listas'].map(cargarJSON),
    ...['perfiles', 'simbolos'].map(cargarOptativo),
  ])
    .then(([obras, diario, listas, perfiles, simbolos]) => {
      actuales = indexar(obras, diario, listas, perfiles, simbolos);
      // Los colores propios de los símbolos (con su valor para claro y para oscuro) se cargan
      // como variables CSS; sin esto, los tramos de esos colores no se ven.
      registrarColoresSimbolos(simbolos.colores ?? {});
      return actuales;
    })
    .catch((error) => {
      promesa = null; // permite reintentar
      throw error;
    });
  return promesa;
}

async function cargarJSON(nombre) {
  const respuesta = await fetch(`data/${nombre}.json`);
  if (!respuesta.ok) throw new Error(`No se pudo cargar data/${nombre}.json (${respuesta.status})`);
  try {
    return await respuesta.json();
  } catch {
    throw new Error(`data/${nombre}.json tiene un error de formato JSON`);
  }
}

// Los datos ya cargados (o null antes de la primera carga).
export function datosActuales() {
  return actuales;
}

async function cargarOptativo(nombre) {
  try {
    return await cargarJSON(nombre);
  } catch (error) {
    console.warn(`${error.message}: se sigue sin ese archivo`);
    return {};
  }
}

function indexar(obras, diario, listas, perfiles = {}, simbolos = {}) {
  const porId = new Map();
  for (const obra of obras) {
    if (porId.has(obra.id)) console.warn(`obras.json: el id "${obra.id}" está repetido`);
    porId.set(obra.id, obra);
  }
  const avisar = (donde, id) => console.warn(`${donde}: la obra "${id}" no existe en obras.json`);
  for (const entrada of diario) if (!porId.has(entrada.obra_id)) avisar(`diario.json (${entrada.id})`, entrada.obra_id);
  for (const lista of listas) for (const id of lista.obras) if (!porId.has(id)) avisar(`listas.json (${lista.id})`, id);

  const datos = { obras, porId, diario, listas, perfiles, simbolos, slugs: indexarSlugs(obras, perfiles) };
  revisarJerarquia(perfiles.estilos ?? {});
  return datos;
}

// Entradas publicadas (diario.json) + visitas guardadas en este teléfono, más recientes primero.
// Si una visita local ya fue publicada (mismo id), se muestra solo la publicada.
export async function entradasDiario(datos) {
  let locales = [];
  try {
    locales = await listarVisitas();
  } catch (error) {
    console.warn('No se pudieron leer las visitas guardadas en el teléfono', error);
  }
  const publicadas = new Set(datos.diario.map((e) => e.id));
  return [
    ...datos.diario.map((e) => ({ ...e, local: false })),
    ...locales.filter((v) => !publicadas.has(v.id)).map((v) => ({ ...v, local: true })),
  ].sort(compararEntradas);
}

export function compararEntradas(a, b) {
  return b.fecha.localeCompare(a.fecha) || (b.creada ?? '').localeCompare(a.creada ?? '') || b.id.localeCompare(a.id);
}

// ---- Años y décadas ----

export function anioReferencia(obra) {
  const anio = obra.anio_finalizacion ?? obra.anio_proyecto;
  return Number.isFinite(anio) ? anio : null;
}

// Sin años, sirve el campo optativo `decada` (por ejemplo 2000).
export function decadaClave(obra) {
  const anio = anioReferencia(obra) ?? (Number.isFinite(obra.decada) ? obra.decada : null);
  return anio === null ? SIN_DATO : String(Math.floor(anio / 10) * 10);
}

export function etiquetaDecada(clave) {
  return clave === SIN_DATO ? 'Sin fecha' : `Década de ${clave}`;
}

export function rangoAnios(obra) {
  const { anio_proyecto: p, anio_finalizacion: f } = obra;
  if (p && f && p !== f) return `${p}–${f}`;
  return String(f ?? p ?? '');
}

// ---- Color del marco ----

// Cuatro marcos por tema. Los nombres son lugares fijos; el color de cada uno en cada tema
// está en estilos.css.
export const COLORES_MARCO = ['petroleo', 'follaje', 'cielo', 'mar'];

const colorValido = (c) => (COLORES_MARCO.includes(c) ? c : null);

// 1. El color propio de la obra ("color" en obras.json).
// 2. El "color" de su estilo o del ancestro más cercano que lo tenga (perfiles.json): así una
//    familia de estilos comparte color.
// 3. Si no, uno estable calculado desde el estilo raíz o, sin estilo, desde el id de la obra.
export function colorMarco(obra) {
  return colorValido(obra.color) ?? (obra.estilo ? colorEstilo(obra.estilo) : COLORES_MARCO[hashTexto(`obra:${obra.id}`) % 4]);
}

export function colorEstilo(estilo) {
  const estilos = actuales?.perfiles?.estilos ?? {};
  const cadena = actuales ? [estilo, ...ancestrosEstilo(actuales, estilo)] : [estilo];
  for (const e of cadena) if (colorValido(estilos[e]?.color)) return estilos[e].color;
  return COLORES_MARCO[hashTexto(`estilo:${cadena.at(-1)}`) % COLORES_MARCO.length];
}

// El color de un perfil: un estilo, el de su familia; los demás, el más frecuente entre sus
// obras (en un empate, el de la obra más antigua); sin obras, uno calculado desde el nombre.
export function colorPerfil(tipo, valor, obras) {
  if (tipo === 'estilo') return colorEstilo(valor);
  if (!obras.length) return COLORES_MARCO[hashTexto(`${tipo}:${valor}`) % COLORES_MARCO.length];
  const conteo = new Map();
  const ordenadas = [...obras].sort((a, b) => (anioReferencia(a) ?? 9999) - (anioReferencia(b) ?? 9999));
  for (const obra of ordenadas) conteo.set(colorMarco(obra), (conteo.get(colorMarco(obra)) ?? 0) + 1);
  return [...conteo].sort((a, b) => b[1] - a[1])[0][0];
}

// ---- Perfiles ----

// Cada tipo de perfil: de dónde salen sus valores en una obra, su sección en perfiles.json y en
// simbolos.json, y cómo se nombra. La ruta es `#/<tipo>/<slug>`; el índice, `#/<indice>`.
export const TIPOS_PERFIL = {
  arquitecto: { indice: 'arquitectos', seccion: 'arquitectos', singular: 'Arquitecto/a', plural: 'Arquitectos', valores: (o) => o.arquitectos ?? [] },
  estilo: { indice: 'estilos', seccion: 'estilos', singular: 'Estilo', plural: 'Estilos', valores: (o) => (o.estilo ? [o.estilo] : []) },
  material: { indice: 'materiales', seccion: 'materiales', singular: 'Material', plural: 'Materiales', valores: (o) => o.materiales ?? [] },
  programa: { indice: 'programas', seccion: 'programas', singular: 'Programa', plural: 'Programas', valores: (o) => (o.programa ? [o.programa] : []) },
  estado: { indice: 'estados', seccion: 'estados', singular: 'Estado', plural: 'Estados', valores: (o) => (o.estado ? [o.estado] : []) },
  pais: { indice: 'paises', seccion: 'paises', singular: 'País', plural: 'Países', valores: (o) => lugar(o, 'pais') },
  provincia: { indice: 'provincias', seccion: 'provincias', singular: 'Provincia / estado', plural: 'Provincias', valores: (o) => lugar(o, 'provincia') },
  ciudad: { indice: 'ciudades', seccion: 'ciudades', singular: 'Partido / ciudad', plural: 'Ciudades', valores: (o) => lugar(o, 'ciudad') },
  barrio: { indice: 'barrios', seccion: 'barrios', singular: 'Barrio / localidad', plural: 'Barrios', valores: (o) => lugar(o, 'barrio') },
  decada: { indice: 'decadas', seccion: 'decadas', singular: 'Década', plural: 'Décadas', valores: (o) => (decadaClave(o) === SIN_DATO ? [] : [decadaClave(o)]) },
  anio: { indice: 'anios', seccion: 'anios', singular: 'Año', plural: 'Años', valores: (o) => [o.anio_proyecto, o.anio_finalizacion].filter(Number.isFinite).map(String).filter((v, i, a) => a.indexOf(v) === i) },
};

export const ESTADOS = { existente: 'Existente', demolida: 'Demolida', modificada: 'Modificada' };

const lugar = (obra, nivel) => (obra.ubicacion?.[nivel] ? [obra.ubicacion[nivel]] : []);

export function nombrePerfil(tipo, valor) {
  if (tipo === 'decada') return `${valor}s`;
  if (tipo === 'estado') return ESTADOS[valor] ?? valor;
  return valor;
}

// "Frank Lloyd Wright" → "frank-lloyd-wright"
export function slug(texto) {
  return normalizar(texto).replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || '-';
}

export function rutaPerfil(tipo, valor) {
  return `#/${tipo}/${slug(valor)}`;
}

// Por tipo, slug → nombre, con todo lo que aparece en las obras y en perfiles.json.
function indexarSlugs(obras, perfiles) {
  const slugs = {};
  for (const [tipo, def] of Object.entries(TIPOS_PERFIL)) {
    const mapa = new Map();
    const sumar = (valor) => {
      const s = slug(valor);
      if (mapa.has(s) && mapa.get(s) !== valor) console.warn(`perfiles: "${valor}" y "${mapa.get(s)}" dan el mismo link (${tipo}/${s})`);
      else mapa.set(s, valor);
    };
    for (const obra of obras) def.valores(obra).forEach(sumar);
    Object.keys(perfiles[def.seccion] ?? {}).forEach(sumar);
    slugs[tipo] = mapa;
  }
  return slugs;
}

export function perfilDe(datos, tipo, valor) {
  return datos.perfiles[TIPOS_PERFIL[tipo].seccion]?.[valor] ?? {};
}

// ---- Jerarquía de estilos ----

function revisarJerarquia(estilos) {
  for (const [nombre, { padre }] of Object.entries(estilos)) {
    if (!padre) continue;
    if (!estilos[padre]) console.warn(`perfiles.json: el estilo "${nombre}" tiene como padre "${padre}", que no está en estilos`);
    const vistos = new Set([nombre]);
    for (let p = padre; p; p = estilos[p]?.padre) {
      if (vistos.has(p)) { console.warn(`perfiles.json: la jerarquía de "${nombre}" forma un ciclo`); break; }
      vistos.add(p);
    }
  }
}

// Del más cercano al más lejano: Racionalismo → [Moderno].
export function ancestrosEstilo(datos, estilo) {
  const estilos = datos.perfiles.estilos ?? {};
  const lista = [];
  for (let p = estilos[estilo]?.padre; p && !lista.includes(p) && p !== estilo; p = estilos[p]?.padre) lista.push(p);
  return lista;
}

// Para filtrar: un estilo cuenta también como todos sus ancestros (filtrar por Moderno trae
// las obras de Racionalismo).
export function estiloConAncestros(estilo) {
  return actuales ? [estilo, ...ancestrosEstilo(actuales, estilo)] : [estilo];
}

export function hijosEstilo(datos, estilo) {
  return Object.entries(datos.perfiles.estilos ?? {}).filter(([, e]) => e.padre === estilo).map(([nombre]) => nombre);
}

// ---- Estadísticas de visitas ----

// Por obra: última visita (fecha), cantidad de visitas y promedio de puntaje (si hay).
export function estadisticasVisitas(entradas) {
  const porObra = new Map();
  for (const e of entradas) {
    const s = porObra.get(e.obra_id) ?? { ultima: '', visitas: 0, puntajes: [] };
    s.visitas++;
    if (e.fecha > s.ultima) s.ultima = e.fecha;
    if (e.puntaje) s.puntajes.push(e.puntaje);
    porObra.set(e.obra_id, s);
  }
  for (const s of porObra.values()) s.promedio = s.puntajes.length ? s.puntajes.reduce((a, b) => a + b, 0) / s.puntajes.length : null;
  return porObra;
}

// ---- Símbolos ----

// La partitura del símbolo de un perfil, o null si no tiene (y entonces va el neutro).
// Programas: si el nombre completo no tiene, se prueba con lo de antes del paréntesis.
// Estilos: si no tiene, el de su ancestro más cercano que tenga.
// Décadas: la colección "mundo", salvo en el contexto de un país que tenga la suya (por ejemplo,
// dentro del perfil de Argentina o con el filtro país = Argentina). Los años usan el de su década.
export function partituraDe(datos, tipo, valor, { pais = null } = {}) {
  const simbolos = datos.simbolos ?? {};
  if (tipo === 'decada' || tipo === 'anio') {
    const decada = tipo === 'decada' ? valor : String(Math.floor(Number(valor) / 10) * 10);
    return simbolos.decadas?.[coleccionDecadas(datos, pais)]?.[decada] ?? null;
  }
  const seccion = simbolos[TIPOS_PERFIL[tipo]?.seccion] ?? {};
  if (seccion[valor]) return seccion[valor];
  if (tipo === 'programa') return seccion[String(valor).replace(/\s*\(.*$/, '')] ?? null;
  if (tipo === 'estilo') {
    for (const ancestro of ancestrosEstilo(datos, valor)) if (seccion[ancestro]) return seccion[ancestro];
  }
  return null;
}

// La colección de décadas de un país (su nombre normalizado: "argentina") o, si no tiene, "mundo".
export function coleccionDecadas(datos, pais) {
  const clave = pais ? normalizar(pais) : null;
  return clave && datos.simbolos?.decadas?.[clave] ? clave : 'mundo';
}

// Para la tapa de una obra sin foto: el símbolo de su arquitecto o, si no tiene, el de su estilo.
export function partituraObra(datos, obra) {
  for (const arquitecto of obra.arquitectos ?? []) {
    const p = partituraDe(datos, 'arquitecto', arquitecto);
    if (p) return p;
  }
  return obra.estilo ? partituraDe(datos, 'estilo', obra.estilo) : null;
}

// ---- Ubicación ----

export const NIVELES_UBICACION = ['pais', 'provincia', 'ciudad', 'barrio'];

const sinRepetir = (valores) => valores.filter((v, i) => v && valores.indexOf(v) === i);

export function lugarCorto(obra) {
  const u = obra.ubicacion ?? {};
  return (sinRepetir([u.barrio, u.ciudad]).join(', ') || sinRepetir([u.provincia, u.pais]).join(', '));
}

export function tieneCoordenadas(obra) {
  return Number.isFinite(obra.ubicacion?.lat) && Number.isFinite(obra.ubicacion?.lng);
}

export function distanciaKm(a, b) {
  const rad = (g) => (g * Math.PI) / 180;
  const dLat = rad(b.lat - a.lat);
  const dLng = rad(b.lng - a.lng);
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(dLng / 2) ** 2;
  return 6371 * 2 * Math.asin(Math.sqrt(h));
}

export function formatoDistancia(km) {
  if (km < 1) return `${Math.max(10, Math.round(km * 100) * 10)} m`;
  if (km < 10) return `${km.toFixed(1).replace('.', ',')} km`;
  return `${Math.round(km).toLocaleString('es-AR')} km`;
}

// ---- Texto y fechas ----

export function normalizar(texto) {
  return String(texto ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
}

export function compararTexto(a, b) {
  return String(a).localeCompare(String(b), 'es', { sensitivity: 'base', numeric: true });
}

// Fecha "AAAA-MM-DD" → "15 de enero de 2026" (sin pasar por UTC, para que no cambie el día).
export function formatoFecha(iso, { conAnio = true } = {}) {
  const [a, m, d] = iso.split('-').map(Number);
  const opciones = { day: 'numeric', month: 'long', ...(conAnio && { year: 'numeric' }) };
  return new Date(a, m - 1, d).toLocaleDateString('es-AR', opciones);
}

export function hoyISO() {
  const h = new Date();
  return [h.getFullYear(), String(h.getMonth() + 1).padStart(2, '0'), String(h.getDate()).padStart(2, '0')].join('-');
}

export function esUrl(texto) {
  return /^https?:\/\//i.test(texto ?? '');
}
