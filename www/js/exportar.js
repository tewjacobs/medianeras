// Arma un ZIP con las visitas del teléfono en el formato de diario.json,
// con las fotos en las rutas donde van dentro de www/.

import { crearZip } from './lib/zip.js';
import { hoyISO } from './datos.js';

const EXTENSIONES = { 'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp', 'image/heic': 'heic', 'image/gif': 'gif' };

const LEEME = `Visitas exportadas desde Jagten
====================================

1. Descomprimí este ZIP dentro de la carpeta www/ del repositorio.
   Las fotos quedan en www/img/diario/<id-de-la-visita>/.
2. Abrí diario-nuevas.json, copiá las entradas y pegalas dentro del array
   de www/data/diario.json (separadas por comas).
3. Borrá diario-nuevas.json y este LEEME.txt.
4. Validá el JSON:  python3 -m json.tool www/data/diario.json
5. Commit y push. Cuando la app vea las visitas publicadas, te va a ofrecer
   borrar las copias del teléfono.
`;

export async function armarExportacion(visitas) {
  const archivos = [];
  const entradas = [...visitas]
    .sort((a, b) => a.fecha.localeCompare(b.fecha) || a.id.localeCompare(b.id))
    .map((visita) => ({
      id: visita.id,
      obra_id: visita.obra_id,
      fecha: visita.fecha,
      nota: visita.nota,
      puntaje: visita.puntaje ?? null,
      fotos: visita.fotos.map((foto, i) => {
        const archivo = `img/diario/${visita.id}/${i + 1}.${EXTENSIONES[foto.blob.type] ?? 'jpg'}`;
        archivos.push({ nombre: archivo, datos: foto.blob });
        return { archivo, pie: foto.pie ?? '' };
      }),
    }));

  const zip = await crearZip([
    { nombre: 'LEEME.txt', datos: LEEME },
    { nombre: 'diario-nuevas.json', datos: `${JSON.stringify(entradas, null, 2)}\n` },
    ...archivos,
  ]);
  return new File([zip], `jagten-visitas-${hoyISO()}.zip`, { type: 'application/zip' });
}
