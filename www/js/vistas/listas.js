// Listas temáticas: índice y detalle.

import { el, tarjetaObra, imagenObra, sinFoto, mensaje } from '../ui.js';

export function render(contenedor, { datos }) {
  if (!datos.listas.length) {
    contenedor.append(mensaje('Todavía no hay listas', 'Cargalas en data/listas.json (ver README).'));
    return;
  }
  contenedor.append(el('div', { class: 'grilla' }, datos.listas.map((lista) => {
    const obras = obrasDe(lista, datos);
    const portada = obras.find((o) => o.fotos?.length);
    return el('a', { class: 'tarjeta', href: `#/lista/${encodeURIComponent(lista.id)}` },
      el('div', { class: 'tarjeta-foto' }, portada ? imagenObra(portada) : sinFoto()),
      el('div', { class: 'tarjeta-texto' },
        el('h3', {}, lista.titulo),
        el('p', { class: 'tenue' }, obras.length === 1 ? '1 obra' : `${obras.length} obras`),
        lista.descripcion && el('p', { class: 'tarjeta-descripcion' }, lista.descripcion),
      ),
    );
  })));
}

export function renderDetalle(contenedor, { datos, partes, titulo }) {
  const lista = datos.listas.find((l) => l.id === partes[1]);
  if (!lista) {
    titulo('Lista no encontrada');
    contenedor.append(mensaje('No encontramos esa lista', null, el('a', { class: 'boton', href: '#/listas' }, 'Ver todas las listas')));
    return;
  }
  titulo(lista.titulo);
  const obras = obrasDe(lista, datos);
  contenedor.append(
    el('div', { class: 'encabezado-lista' },
      el('h2', {}, lista.titulo),
      lista.descripcion && el('p', { class: 'tenue' }, lista.descripcion),
      el('p', { class: 'tenue' }, obras.length === 1 ? '1 obra' : `${obras.length} obras`),
    ),
    el('div', { class: 'grilla' }, obras.map((obra) => tarjetaObra(obra))),
  );
}

function obrasDe(lista, datos) {
  return lista.obras.map((id) => datos.porId.get(id)).filter(Boolean);
}
