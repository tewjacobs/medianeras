// Preferencias chicas guardadas en el teléfono (por ahora, solo el tema).
// Para Capacitor: se puede reemplazar el interior por @capacitor/preferences manteniendo
// estas funciones. Ojo: el script del <head> de index.html lee la misma clave directamente,
// para aplicar el tema antes de pintar.

const PREFIJO = 'medianeras-';

export function leerPreferencia(clave, porDefecto = null) {
  try {
    return localStorage.getItem(PREFIJO + clave) ?? porDefecto;
  } catch {
    return porDefecto;
  }
}

export function guardarPreferencia(clave, valor) {
  try {
    localStorage.setItem(PREFIJO + clave, valor);
  } catch {
    // Sin almacenamiento (modo privado): la elección dura hasta cerrar la app.
  }
}
