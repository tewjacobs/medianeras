// Generador mínimo de archivos ZIP, sin compresión (las fotos JPEG ya vienen comprimidas).
// archivos: [{ nombre: 'carpeta/archivo.jpg', datos: Blob | string }] → Blob

const TABLA_CRC = Array.from({ length: 256 }, (_, n) => {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  return c >>> 0;
});

function crc32(bytes) {
  let crc = 0xffffffff;
  for (const byte of bytes) crc = TABLA_CRC[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}

function fechaDos(fecha) {
  return {
    hora: (fecha.getHours() << 11) | (fecha.getMinutes() << 5) | (fecha.getSeconds() >> 1),
    dia: ((fecha.getFullYear() - 1980) << 9) | ((fecha.getMonth() + 1) << 5) | fecha.getDate(),
  };
}

export async function crearZip(archivos) {
  const codificador = new TextEncoder();
  const { hora, dia } = fechaDos(new Date());
  const partes = [];
  const central = [];
  let desplazamiento = 0;

  for (const { nombre, datos } of archivos) {
    const contenido = typeof datos === 'string' ? codificador.encode(datos) : new Uint8Array(await datos.arrayBuffer());
    const nombreBytes = codificador.encode(nombre);
    const crc = crc32(contenido);

    const local = new DataView(new ArrayBuffer(30));
    local.setUint32(0, 0x04034b50, true);
    local.setUint16(4, 20, true);
    local.setUint16(6, 0x0800, true); // nombres en UTF-8
    local.setUint16(8, 0, true); // sin compresión
    local.setUint16(10, hora, true);
    local.setUint16(12, dia, true);
    local.setUint32(14, crc, true);
    local.setUint32(18, contenido.length, true);
    local.setUint32(22, contenido.length, true);
    local.setUint16(26, nombreBytes.length, true);
    local.setUint16(28, 0, true);
    partes.push(local, nombreBytes, contenido);

    const entrada = new DataView(new ArrayBuffer(46));
    entrada.setUint32(0, 0x02014b50, true);
    entrada.setUint16(4, 20, true);
    entrada.setUint16(6, 20, true);
    entrada.setUint16(8, 0x0800, true);
    entrada.setUint16(10, 0, true);
    entrada.setUint16(12, hora, true);
    entrada.setUint16(14, dia, true);
    entrada.setUint32(16, crc, true);
    entrada.setUint32(20, contenido.length, true);
    entrada.setUint32(24, contenido.length, true);
    entrada.setUint16(28, nombreBytes.length, true);
    entrada.setUint32(42, desplazamiento, true);
    central.push(entrada, nombreBytes);

    desplazamiento += 30 + nombreBytes.length + contenido.length;
  }

  const tamCentral = central.reduce((total, p) => total + p.byteLength, 0);
  const fin = new DataView(new ArrayBuffer(22));
  fin.setUint32(0, 0x06054b50, true);
  fin.setUint16(8, archivos.length, true);
  fin.setUint16(10, archivos.length, true);
  fin.setUint32(12, tamCentral, true);
  fin.setUint32(16, desplazamiento, true);

  return new Blob([...partes, ...central, fin], { type: 'application/zip' });
}
