// Elegir o sacar fotos, y achicarlas antes de guardarlas.
// Para Capacitor: reemplazar el interior de elegirFotos() por Camera.pickImages()
// / Camera.getPhoto() de @capacitor/camera, devolviendo igual un array de Blob/File.

let entradaAnterior = null;

// Tiene que llamarse directamente desde un toque del usuario (iOS lo exige para abrir el selector).
export function elegirFotos() {
  entradaAnterior?.remove();
  const entrada = document.createElement('input');
  entrada.type = 'file';
  entrada.accept = 'image/*';
  entrada.multiple = true;
  entrada.hidden = true;
  document.body.append(entrada);
  entradaAnterior = entrada;
  return new Promise((resolver) => {
    const terminar = () => {
      resolver([...(entrada.files ?? [])]);
      entrada.remove();
    };
    entrada.addEventListener('change', terminar, { once: true });
    entrada.addEventListener('cancel', terminar, { once: true });
    entrada.click();
  });
}

// Reduce la foto a ladoMax píxeles y la pasa a JPEG. Si algo falla, devuelve el archivo original.
export async function prepararFoto(archivo, { ladoMax = 1600, calidad = 0.82 } = {}) {
  const url = URL.createObjectURL(archivo);
  try {
    const imagen = new Image();
    imagen.src = url;
    await imagen.decode();
    const escala = Math.min(1, ladoMax / Math.max(imagen.naturalWidth, imagen.naturalHeight));
    const lienzo = document.createElement('canvas');
    lienzo.width = Math.round(imagen.naturalWidth * escala);
    lienzo.height = Math.round(imagen.naturalHeight * escala);
    lienzo.getContext('2d').drawImage(imagen, 0, 0, lienzo.width, lienzo.height);
    const blob = await new Promise((resolver) => lienzo.toBlob(resolver, 'image/jpeg', calidad));
    return blob ?? archivo;
  } catch (error) {
    console.warn('No se pudo achicar la foto; se guarda la original', error);
    return archivo;
  } finally {
    URL.revokeObjectURL(url);
  }
}
