// Price Tower, versión "planta" (op-art, simétrica de espejo), a partir del plano de
// referencias/simbolos/price tower/: el contorno del piso, los cuatro departamentos con la trama
// de 30°/150° que tiene el piso en el plano, los muros del núcleo en cruz (tres líneas
// paralelas, puntas rectas) y el núcleo hexagonal en el centro.
// Variantes:
//   cuadrado: contorno derecho; la cruz llega a los lados.
//   rombo:    el contorno girado 45°, como se ve inclinada la planta; la cruz llega a las puntas.
//   alas:     contorno derecho y los muros salen afuera como las alas de escalera del plano.
export const VARIANTES = ['cuadrado', 'rombo', 'alas'];

const H = 22, G = 4.4, HEX = 3.4;
const f = (x) => x.toFixed(2);
let ESC = 1;
const P = ([x, y]) => `${f(x * ESC + 32)} ${f(y * ESC + 32)}`;
const cerrado = (pts) => `M${pts.map(P).join('L')}Z`;
const rot90 = ([x, y], k) => { for (let i = 0; i < k; i++) [x, y] = [-y, x]; return [x, y]; };
const hexagono = (r) => Array.from({ length: 6 }, (_, k) => [r * Math.cos((Math.PI / 3) * k), r * Math.sin((Math.PI / 3) * k)]);

function geometria(v, escala = 1) {
  const D = H * 1.18;
  const parte = v === 'rombo'
    ? [[G / 2, G / 2], [D - G / 2, G / 2], [G / 2, D - G / 2]]
    : [[G / 2, G / 2], [H, G / 2], [H, H], [G / 2, H]];
  const contorno = v === 'rombo' ? [[0, -D], [D, 0], [0, D], [-D, 0]] : [[-H, -H], [H, -H], [H, H], [-H, H]];
  const alcance = v === 'rombo' ? D : v === 'alas' ? H + 6 : H;
  const partes = [0, 1, 2, 3].map((k) => parte.map((p) => rot90(p, k)));
  return { partes, contorno, alcance, escala };
}

// Trama de 30° y 150° dentro de una región (clipPath).
function trama(id, paso, ancho) {
  const lineas = [];
  for (const a of [30, 150]) {
    const r = (a * Math.PI) / 180;
    const [dx, dy] = [Math.cos(r) * 60 / ESC, Math.sin(r) * 60 / ESC];
    for (let c = -60; c <= 60; c += paso / ESC) {
      const [nx, ny] = [-Math.sin(r) * c, Math.cos(r) * c];
      lineas.push(`M${P([nx - dx, ny - dy])}L${P([nx + dx, ny + dy])}`);
    }
  }
  return `<path clip-path="url(#${id})" d="${lineas.join('')}" stroke="currentColor" stroke-width="${ancho}" fill="none"/>`;
}

// modo "carga": con las clases de la pantalla de carga (se dibuja en orden y el núcleo respira).
// modo "boton": lo mismo más simple y más grueso, para leerse a 24 px.
export function svgPlanta(v, modo = 'carga', prefijo = 'pt') {
  const g = geometria(v);
  ESC = 29.5 / (g.alcance + (v === 'rombo' ? 0.5 : 1.5));
  const boton = modo === 'boton';
  const id = `${prefijo}-${v}-${modo}`;
  const brazos = [0, 1, 2, 3].map((k) => {
    const desde = HEX * 0.9;
    const off = boton ? [0] : [-1.3, 0, 1.3];
    return off.map((o) => [[desde, o], [g.alcance, o]].map((p) => rot90(p, k)));
  });
  const alas = v === 'alas' ? [0, 1, 2, 3].map((k) => [[H, -G / 2 - 0.6], [H + 6, -G / 2 - 0.6], [H + 6, G / 2 + 0.6], [H, G / 2 + 0.6]].map((p) => rot90(p, k))) : [];
  const defs = `<defs><clipPath id="${id}">${g.partes.map((p) => `<path d="${cerrado(p)}"/>`).join('')}</clipPath></defs>`;
  if (boton) {
    return `<svg viewBox="0 0 64 64" aria-hidden="true" fill="none">${defs}`
      + `<g style="color: var(--tenue)">${trama(id, 7.5, 1.8)}</g>`
      + `<path d="${cerrado(g.contorno)}" stroke="currentColor" stroke-width="3.6" stroke-linejoin="miter"/>`
      + alas.map((a) => `<path d="${cerrado(a)}" stroke="currentColor" stroke-width="3" fill="var(--papel)"/>`).join('')
      + `<path d="${brazos.flat().map((l) => `M${P(l[0])}L${P(l[1])}`).join('')}" stroke="var(--rojo)" stroke-width="5.6"/>`
      + `<path d="${cerrado(hexagono(HEX + 1.2))}" fill="var(--papel)" stroke="currentColor" stroke-width="2.4"/></svg>`;
  }
  let i = 0;
  const caminos = [
    `<path class="carga-trazo" style="--i:${i++}" pathLength="1" d="${cerrado(g.contorno)}"/>`,
    ...alas.map((a) => `<path class="carga-trazo" style="--i:${i}" pathLength="1" d="${cerrado(a)}"/>`),
    `<g class="carga-trama" style="--i:${(i += 1)}">${trama(id, 4.4, 0.5)}</g>`,
    ...g.partes.map((pt) => `<path class="carga-trazo carga-fina" style="--i:${i}" pathLength="1" d="${cerrado(pt)}"/>`),
    ...brazos.map((grupo) => `<path class="carga-brazo carga-muro" style="--i:${(i += 1)}" pathLength="1" d="${grupo.map((l) => `M${P(l[0])}L${P(l[1])}`).join('')}"/>`),
    `<path class="carga-centro" d="${cerrado(hexagono(HEX))}"/>`,
  ];
  return `<svg class="carga-simbolo" viewBox="0 0 64 64" aria-hidden="true" focusable="false" fill="none" stroke-linecap="butt" stroke-linejoin="miter">\n      ${defs}\n      ${caminos.join('\n      ')}\n    </svg>`;
}
