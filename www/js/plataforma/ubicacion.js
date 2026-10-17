// Ubicación del dispositivo.
// Para Capacitor: reemplazar el interior de obtenerUbicacion() por
// Geolocation.getCurrentPosition() de @capacitor/geolocation.

const MENSAJES = {
  1: 'No diste permiso para usar tu ubicación. En el iPhone: Ajustes → Privacidad y seguridad → Localización → Sitios de Safari.',
  2: 'No se pudo determinar tu ubicación. Probá de nuevo al aire libre.',
  3: 'Tardó demasiado en obtener tu ubicación. Probá de nuevo.',
};

let ultima = null;

export function ultimaUbicacion() {
  return ultima;
}

export function obtenerUbicacion() {
  return new Promise((resolver, rechazar) => {
    if (!window.isSecureContext) return rechazar(new Error('La ubicación solo funciona con https:// (o en localhost).'));
    if (!('geolocation' in navigator)) return rechazar(new Error('Este dispositivo no permite obtener la ubicación.'));
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => {
        ultima = { lat: coords.latitude, lng: coords.longitude, precision: coords.accuracy };
        resolver(ultima);
      },
      (error) => rechazar(new Error(MENSAJES[error.code] ?? 'No se pudo obtener tu ubicación.')),
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 60000 },
    );
  });
}
