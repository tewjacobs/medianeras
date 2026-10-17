// Filtros de la grilla. Las opciones de cada filtro se calculan desde los datos,
// con la cantidad de obras que quedarían al elegirlas.

import { SIN_DATO, decadaClave, etiquetaDecada, normalizar, compararTexto } from './datos.js';

const nivel = (clave) => (obra) => [obra.ubicacion?.[clave] || SIN_DATO];
const nombreUbicacion = (v) => (v === SIN_DATO ? 'Sin especificar' : v);

export const FACETAS = [
  { clave: 'decada', etiqueta: 'Década', valores: (o) => [decadaClave(o)], nombre: etiquetaDecada, numerico: true },
  { clave: 'estilo', etiqueta: 'Estilo', valores: (o) => (o.estilo ? [o.estilo] : []) },
  { clave: 'material', etiqueta: 'Material', valores: (o) => o.materiales ?? [] },
  { clave: 'arquitecto', etiqueta: 'Arquitecto/a', valores: (o) => o.arquitectos ?? [] },
  { clave: 'programa', etiqueta: 'Programa', valores: (o) => (o.programa ? [o.programa] : []) },
  // Ubicación en cascada: cada nivel se habilita cuando está elegido el anterior.
  { clave: 'pais', etiqueta: 'País', valores: nivel('pais'), nombre: nombreUbicacion },
  { clave: 'provincia', etiqueta: 'Provincia / estado', valores: nivel('provincia'), nombre: nombreUbicacion, padre: 'pais' },
  { clave: 'ciudad', etiqueta: 'Partido / ciudad', valores: nivel('ciudad'), nombre: nombreUbicacion, padre: 'provincia' },
  { clave: 'barrio', etiqueta: 'Barrio / localidad', valores: nivel('barrio'), nombre: nombreUbicacion, padre: 'ciudad' },
];

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
  return filtros;
}

export function filtrosAQuery(filtros) {
  const params = new URLSearchParams();
  for (const { clave } of FACETAS) if (filtros[clave]) params.set(clave, filtros[clave]);
  if (filtros.q) params.set('q', filtros.q);
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

function cumple(obra, filtros, excluidas) {
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

export function filtrar(obras, filtros) {
  return obras.filter((o) => cumple(o, filtros, new Set()));
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

// Link a la grilla con filtros (por ejemplo, desde la ficha de una obra).
export function rutaFiltrada(filtros) {
  const query = filtrosAQuery(filtros);
  return query ? `#/?${query}` : '#/';
}

export function faceta(clave) {
  return porClave.get(clave);
}
