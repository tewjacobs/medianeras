// Visitas guardadas en el teléfono (IndexedDB).
// Para Capacitor: se puede dejar igual (IndexedDB funciona en la app nativa) o
// reemplazar el interior por @capacitor/filesystem manteniendo estas mismas funciones.
//
// Una visita: { id, obra_id, fecha, nota, puntaje, fotos: [{ blob, pie }], creada, modificada, exportada }
// Las fotos se guardan como ArrayBuffer + tipo (más robusto que Blob en Safari) y se devuelven como Blob.

const BASE = 'medianeras'; // nombre viejo de la app: no cambiarlo, o se pierden las visitas guardadas
const VERSION = 1;
const VISITAS = 'visitas';

let conexion = null;

function abrir() {
  conexion ??= new Promise((resolver, rechazar) => {
    const pedido = indexedDB.open(BASE, VERSION);
    pedido.onupgradeneeded = () => pedido.result.createObjectStore(VISITAS, { keyPath: 'id' });
    pedido.onsuccess = () => resolver(pedido.result);
    pedido.onerror = () => {
      conexion = null;
      rechazar(pedido.error);
    };
  });
  return conexion;
}

async function operar(modo, accion) {
  const db = await abrir();
  return new Promise((resolver, rechazar) => {
    const transaccion = db.transaction(VISITAS, modo);
    const pedido = accion(transaccion.objectStore(VISITAS));
    transaccion.oncomplete = () => resolver(pedido.result);
    transaccion.onerror = () => rechazar(transaccion.error);
    transaccion.onabort = () => rechazar(transaccion.error ?? new Error('Se canceló el guardado'));
  });
}

const aBlob = (visita) => ({
  ...visita,
  fotos: visita.fotos.map(({ datos, tipo, pie }) => ({ blob: new Blob([datos], { type: tipo }), pie })),
});

export async function listarVisitas() {
  return (await operar('readonly', (s) => s.getAll())).map(aBlob);
}

export async function obtenerVisita(id) {
  const visita = await operar('readonly', (s) => s.get(id));
  return visita ? aBlob(visita) : null;
}

export async function guardarVisita(visita) {
  // La conversión va antes de abrir la transacción: IndexedDB la cierra si se espera en el medio.
  const fotos = await Promise.all(visita.fotos.map(async ({ blob, pie }) => ({ datos: await blob.arrayBuffer(), tipo: blob.type, pie })));
  await operar('readwrite', (s) => s.put({ ...visita, fotos }));
}

export function borrarVisita(id) {
  return operar('readwrite', (s) => s.delete(id));
}

// Pide al navegador que no borre estos datos para liberar espacio.
export async function pedirPersistencia() {
  try {
    return (await navigator.storage?.persist?.()) ?? false;
  } catch {
    return false;
  }
}
