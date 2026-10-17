// Entregar un archivo generado: menú Compartir del sistema o descarga.
// Para Capacitor: escribir el archivo con @capacitor/filesystem y abrir
// Share.share({ files: [uri] }) de @capacitor/share.

export function puedeCompartir(archivo) {
  return Boolean(navigator.canShare?.({ files: [archivo] }));
}

// Devuelve 'compartido', 'cancelado' o 'descargado'. Tiene que llamarse desde un toque del usuario.
export async function compartirArchivo(archivo) {
  if (puedeCompartir(archivo)) {
    try {
      await navigator.share({ files: [archivo] });
      return 'compartido';
    } catch (error) {
      if (error.name === 'AbortError') return 'cancelado';
      console.warn('Falló el menú Compartir; se descarga el archivo', error);
    }
  }
  descargarArchivo(archivo);
  return 'descargado';
}

export function descargarArchivo(archivo) {
  const url = URL.createObjectURL(archivo);
  const enlace = Object.assign(document.createElement('a'), { href: url, download: archivo.name, hidden: true });
  document.body.append(enlace);
  enlace.click();
  enlace.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}
