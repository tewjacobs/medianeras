// Carga de los JSON de /data, índices y funciones de formato.
// No hay ningún lugar, estilo ni arquitecto escrito acá: todo sale de los datos.

import { listarVisitas } from './plataforma/almacen.js';
import { hashTexto } from './grafica.js';

export const SIN_DATO = '_';

let promesa = null;

export function cargarDatos() {
  promesa ??= Promise.all(['obras', 'diario', 'listas'].map(cargarJSON))
    .then(([obras, diario, listas]) => indexar(obras, diario, listas))
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

function indexar(obras, diario, listas) {
  const porId = new Map();
  for (const obra of obras) {
    if (porId.has(obra.id)) console.warn(`obras.json: el id "${obra.id}" está repetido`);
    porId.set(obra.id, obra);
  }
  const avisar = (donde, id) => console.warn(`${donde}: la obra "${id}" no existe en obras.json`);
  for (const entrada of diario) if (!porId.has(entrada.obra_id)) avisar(`diario.json (${entrada.id})`, entrada.obra_id);
  for (const lista of listas) for (const id of lista.obras) if (!porId.has(id)) avisar(`listas.json (${lista.id})`, id);

  return { obras, porId, diario, listas };
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

export function decadaClave(obra) {
  const anio = anioReferencia(obra);
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

// El color propio de la obra si lo tiene; si no, uno estable calculado desde su estilo
// (todas las obras de un estilo comparten color) o, sin estilo, desde su id.
export function colorMarco(obra) {
  if (COLORES_MARCO.includes(obra.color)) return obra.color;
  return COLORES_MARCO[hashTexto(obra.estilo ? `estilo:${obra.estilo}` : `obra:${obra.id}`) % COLORES_MARCO.length];
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
