// Filtros de la grilla. Las opciones de cada filtro se calculan desde los datos,
// con la cantidad de obras que quedarían al elegirlas.

import { SIN_DATO, ESTADOS, decadaClave, etiquetaDecada, normalizar, compararTexto, estiloConAncestros, anioReferencia } from './datos.js';

const nivel = (clave) => (obra) => [obra.ubicacion?.[clave] || SIN_DATO];
const nombreUbicacion = (v) => (v === SIN_DATO ? 'Sin especificar' : v);

// `ruta`: el tipo de perfil al que lleva cada valor (#/<ruta>/<slug>).
export const FACETAS = [
  { clave: 'decada', ruta: 'decada', etiqueta: 'Década', valores: (o) => [decadaClave(o)], nombre: etiquetaDecada, numerico: true },
  { clave: 'anio', ruta: 'anio', etiqueta: 'Año', valores: (o) => { const a = anioReferencia(o); return a === null ? [] : [String(a)]; }, numerico: true },
  { clave: 'estilo', ruta: 'estilo', etiqueta: 'Estilo', valores: (o) => (o.estilo ? estiloConAncestros(o.estilo) : []) },
  { clave: 'material', ruta: 'material', etiqueta: 'Material', valores: (o) => o.materiales ?? [] },
  { clave: 'arquitecto', ruta: 'arquitecto', etiqueta: 'Arquitecto/a', valores: (o) => o.arquitectos ?? [] },
  { clave: 'programa', ruta: 'programa', etiqueta: 'Programa', valores: (o) => (o.programa ? [o.programa] : []) },
  { clave: 'estado', ruta: 'estado', etiqueta: 'Estado', valores: (o) => (o.estado ? [o.estado] : []), nombre: (v) => ESTADOS[v] ?? v },
  // Ubicación en cascada: cada nivel se habilita cuando está elegido el anterior.
  { clave: 'pais', ruta: 'pais', etiqueta: 'País', valores: nivel('pais'), nombre: nombreUbicacion },
  { clave: 'provincia', ruta: 'provincia', etiqueta: 'Provincia / estado', valores: nivel('provincia'), nombre: nombreUbicacion, padre: 'pais' },
  { clave: 'ciudad', ruta: 'ciudad', etiqueta: 'Partido / ciudad', valores: nivel('ciudad'), nombre: nombreUbicacion, padre: 'provincia' },
  { clave: 'barrio', ruta: 'barrio', etiqueta: 'Barrio / localidad', valores: nivel('barrio'), nombre: nombreUbicacion, padre: 'ciudad' },
];

// Orden de la grilla (?orden=…). "visita" y "puntaje" usan las estadísticas de visitas.
export const ORDENES = {
  nombre: 'Nombre',
  anio: 'Año',
  agregada: 'Agregadas recientemente',
  visita: 'Visitadas recientemente',
  puntaje: 'Mejor puntuadas',
};

const porClave = new Map(FACETAS.map((f) => [f.clave, f]));

export function nombreValor(faceta, valor) {
  return faceta.nombre ? faceta.nombre(valor) : valor;
}

export function descendientes(clave) {
  const hijos = [];
  for (let hijo = FACETAS.find((f) => f.padre === clave); hijo; hijo = FACETAS.find((f) => f.padre === hijo.clave)) {
    hijos.push(hijo.clave);
  }
  return hijos;
}

export function leerFiltros(params) {
  const filtros = {};
  for (const { clave } of FACETAS) if (params.get(clave)) filtros[clave] = params.get(clave);
  if (params.get('q')) filtros.q = params.get('q');
  if (ORDENES[params.get('orden')]) filtros.orden = params.get('orden');
  if (params.get('visitadas') === 'si') filtros.visitadas = 'si';
  return filtros;
}

export function filtrosAQuery(filtros) {
  const params = new URLSearchParams();
  for (const { clave } of FACETAS) if (filtros[clave]) params.set(clave, filtros[clave]);
  if (filtros.q) params.set('q', filtros.q);
  if (filtros.orden) params.set('orden', filtros.orden);
  if (filtros.visitadas) params.set('visitadas', filtros.visitadas);
  return params.toString();
}

// Cambia un filtro y borra los niveles de ubicación que dependen de él.
export function conFiltro(filtros, clave, valor) {
  const nuevos = { ...filtros };
  for (const hijo of descendientes(clave)) delete nuevos[hijo];
  if (valor) nuevos[clave] = valor;
  else delete nuevos[clave];
  return nuevos;
}

// `visitadas`: ids de las obras con alguna visita (para ?visitadas=si).
function cumple(obra, filtros, excluidas, visitadas) {
  if (filtros.visitadas && visitadas && !visitadas.has(obra.id)) return false;
  for (const faceta of FACETAS) {
    const valor = filtros[faceta.clave];
    if (valor && !excluidas.has(faceta.clave) && !faceta.valores(obra).includes(valor)) return false;
  }
  if (filtros.q) {
    const texto = normalizar([obra.nombre, ...(obra.otros_nombres ?? []), ...(obra.arquitectos ?? []), obra.ubicacion?.direccion].join(' '));
    if (!texto.includes(normalizar(filtros.q))) return false;
  }
  return true;
}

export function filtrar(obras, filtros, { visitadas } = {}) {
  return obras.filter((o) => cumple(o, filtros, new Set(), visitadas));
}

// Ordena según filtros.orden. `estadisticas`: Map obra_id → { ultima, promedio } (datos.js).
// "Agregadas" usa el campo `agregada` y, si falta, el orden de obras.json (la última es la más nueva).
export function ordenar(obras, orden, { estadisticas = new Map(), todas = obras } = {}) {
  const lista = [...obras];
  const posicion = new Map(todas.map((o, i) => [o.id, i]));
  const porNombre = (a, b) => compararTexto(a.nombre, b.nombre);
  const criterios = {
    nombre: porNombre,
    anio: (a, b) => (anioReferencia(a) ?? 9999) - (anioReferencia(b) ?? 9999) || porNombre(a, b),
    agregada: (a, b) => (b.agregada ?? '').localeCompare(a.agregada ?? '') || posicion.get(b.id) - posicion.get(a.id),
    visita: (a, b) => (estadisticas.get(b.id)?.ultima ?? '').localeCompare(estadisticas.get(a.id)?.ultima ?? '') || porNombre(a, b),
    puntaje: (a, b) => (estadisticas.get(b.id)?.promedio ?? 0) - (estadisticas.get(a.id)?.promedio ?? 0) || porNombre(a, b),
  };
  return lista.sort(criterios[orden] ?? porNombre);
}

// Opciones de una faceta con su conteo, ignorando el valor elegido en esa faceta y en sus niveles hijos.
export function opciones(obras, filtros, faceta) {
  const excluidas = new Set([faceta.clave, ...descendientes(faceta.clave)]);
  const conteo = new Map();
  for (const obra of obras) {
    if (!cumple(obra, filtros, excluidas)) continue;
    for (const valor of new Set(faceta.valores(obra))) conteo.set(valor, (conteo.get(valor) ?? 0) + 1);
  }
  return [...conteo]
    .map(([valor, cantidad]) => ({ valor, cantidad, nombre: nombreValor(faceta, valor) }))
    .sort((a, b) => {
      if (a.valor === SIN_DATO || b.valor === SIN_DATO) return (a.valor === SIN_DATO) - (b.valor === SIN_DATO);
      return faceta.numerico ? Number(a.valor) - Number(b.valor) : compararTexto(a.nombre, b.nombre);
    });
}

export function filtrosActivos(filtros) {
  return FACETAS.filter((f) => filtros[f.clave]).map((f) => ({
    faceta: f,
    valor: filtros[f.clave],
    nombre: nombreValor(f, filtros[f.clave]),
  }));
}

// Link a la grilla completa con filtros.
export function rutaFiltrada(filtros) {
  const query = filtrosAQuery(filtros);
  return query ? `#/obras?${query}` : '#/obras';
}

export function faceta(clave) {
  return porClave.get(clave);
}
