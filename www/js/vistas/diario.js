// Diario: visitas publicadas + guardadas en el teléfono, agrupadas por año.

import { el, icono, tarjetaEntrada, mensaje, abrirHoja, aviso } from '../ui.js';
import { entradasDiario, COLORES_MARCO } from '../datos.js';
import { listarVisitas, guardarVisita, borrarVisita } from '../plataforma/almacen.js';
import { compartirArchivo, descargarArchivo, puedeCompartir } from '../plataforma/compartir.js';
import { armarExportacion } from '../exportar.js';

export async function render(contenedor, ctx) {
  const { datos } = ctx;
  const [entradas, locales] = await Promise.all([entradasDiario(datos), listarVisitas().catch(() => [])]);
  const publicadas = new Set(datos.diario.map((e) => e.id));
  const pendientes = locales.filter((v) => !publicadas.has(v.id));
  const yaPublicadas = locales.filter((v) => publicadas.has(v.id));

  if (pendientes.length) {
    const sinExportar = pendientes.filter((v) => !v.exportada).length;
    contenedor.append(el('div', { class: 'panel' },
      el('p', {}, pendientes.length === 1 ? 'Tenés 1 visita guardada solo en este teléfono' : `Tenés ${pendientes.length} visitas guardadas solo en este teléfono`,
        sinExportar === 0 ? ' (ya exportadas).' : sinExportar < pendientes.length ? ` (${sinExportar} sin exportar).` : '.'),
      el('p', { class: 'tenue' }, 'Exportá para sumarlas al repositorio y no perderlas.'),
      el('button', { type: 'button', class: 'boton boton-primario', onclick: () => exportar(pendientes, ctx) }, icono('compartir'), 'Exportar visitas'),
    ));
  }

  if (yaPublicadas.length) {
    contenedor.append(el('div', { class: 'panel' },
      el('p', {}, yaPublicadas.length === 1 ? '1 visita del teléfono ya está publicada en el diario.' : `${yaPublicadas.length} visitas del teléfono ya están publicadas en el diario.`),
      el('button', {
        type: 'button', class: 'boton',
        onclick: async () => {
          if (!confirm('¿Borrar del teléfono las copias de las visitas que ya están publicadas?')) return;
          await Promise.all(yaPublicadas.map((v) => borrarVisita(v.id)));
          aviso('Copias borradas del teléfono');
          ctx.recargar();
        },
      }, icono('basura'), 'Borrar copias del teléfono'),
    ));
  }

  if (!entradas.length) {
    contenedor.append(mensaje('Tu diario está vacío', 'Registrá tu primera visita desde el botón + de abajo.',
      el('a', { class: 'boton boton-primario', href: '#/nueva' }, 'Registrar visita')));
    return;
  }

  let anio = null;
  let grupo = null;
  for (const entrada of entradas) {
    const anioEntrada = entrada.fecha.slice(0, 4);
    if (anioEntrada !== anio) {
      anio = anioEntrada;
      grupo = el('div', { class: 'entradas entradas-grilla' });
      contenedor.append(el('section', { class: 'diario-anio' }, el('h2', { class: 'separador' }, anio), grupo));
    }
    // El color del recuadro va rotando por la paleta, de una entrada a la siguiente.
    grupo.append(tarjetaEntrada(entrada, datos, { compacta: true, color: COLORES_MARCO[grupo.childElementCount % COLORES_MARCO.length] }));
  }
}

// En dos pasos: primero se arma el ZIP y después se comparte con un toque nuevo
// (iOS solo abre el menú Compartir si viene directo de un toque).
async function exportar(visitas, ctx) {
  const { cuerpo, pie } = abrirHoja({ titulo: 'Exportar visitas', contenido: el('p', { class: 'tenue' }, 'Preparando el archivo…'), pie: [] });
  let archivo;
  try {
    archivo = await armarExportacion(visitas);
  } catch (error) {
    console.error(error);
    cuerpo.replaceChildren(el('p', {}, 'No se pudo armar el archivo de exportación.'));
    return;
  }
  const tamano = archivo.size < 1048576
    ? `${Math.max(1, Math.round(archivo.size / 1024))} KB`
    : `${(archivo.size / 1048576).toFixed(1).replace('.', ',')} MB`;
  cuerpo.replaceChildren(
    el('p', {}, `${archivo.name} · ${tamano}`),
    el('p', { class: 'tenue' }, `Incluye ${visitas.length === 1 ? '1 visita' : `${visitas.length} visitas`} en el formato de diario.json, con sus fotos y un LEEME con los pasos para sumarlas al repo.`),
  );

  const marcarExportadas = async () => {
    await Promise.all(visitas.filter((v) => !v.exportada).map((v) => guardarVisita({ ...v, exportada: true })));
    ctx.recargar();
  };
  const entregar = async (accion) => {
    const resultado = await accion();
    if (resultado === 'cancelado') return;
    aviso(resultado === 'compartido' ? 'Visitas exportadas' : 'Archivo descargado');
    await marcarExportadas();
  };

  pie.replaceChildren(
    el('button', { type: 'button', class: 'boton', onclick: () => entregar(() => { descargarArchivo(archivo); return 'descargado'; }) }, 'Descargar'),
    puedeCompartir(archivo) && el('button', { type: 'button', class: 'boton boton-primario', onclick: () => entregar(() => compartirArchivo(archivo)) }, icono('compartir'), 'Compartir'),
  );
}
