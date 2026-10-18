// Tres versiones simétricas de la planta de la Price Tower, para el botón de visita y la carga.
// Todas con puntas rectas y brazos del mismo largo, para que la cruz se lea como un "+".
//   rombo:   cuadrado girado 45°; las cuatro partes son triángulos y la cruz corre entre ellos
//   recto:   cuadrado sin girar en cuatro cuartos; la cruz corre entre los cuartos y sobresale
//   corta30: cuadrado girado 30° en cuatro cuartos; cruz derecha y corta, que no sobresale
export const VERSIONES = ['rombo', 'recto', 'corta30'];

const H = 13, G = 3.2, C = 3.6, W = 3.4, E = 3.4, D_IN = 1.7;
const rot90 = ([x, y], k) => { for (let i = 0; i < k; i++) [x, y] = [-y, x]; return [x, y]; };
const girar = ([x, y], g) => { const a = g * Math.PI / 180; return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]; };

function geometria(v) {
  if (v === 'rombo') {
    const D = H * Math.SQRT2;
    const parte = [[C, G / 2], [D - G / 2, G / 2], [G / 2, D - G / 2], [G / 2, C], [C, C]];
    const k = D - 2.6;
    const linea = [[k - G / 2 - 1.4, G / 2 + 1.4], [G / 2 + 1.4, k - G / 2 - 1.4]];
    return { giro: 0, parte, linea, alcance: D + E, contorno: [[0, -D], [D, 0], [0, D], [-D, 0]] };
  }
  const giro = v === 'recto' ? 0 : 30;
  const parte = [[C, G / 2], [H, G / 2], [H, H], [G / 2, H], [G / 2, C], [C, C]];
  const linea = [[G / 2 + D_IN, H - D_IN], [H - D_IN, H - D_IN]];
  return { giro, parte, linea, alcance: v === 'recto' ? H + E : H * 0.92, contorno: [[-H, -H], [H, -H], [H, H], [-H, H]] };
}

// Devuelve el código SVG (texto). modo "carga": partes, líneas interiores, muros huecos y el
// centro que respira (clases de la pantalla de carga). modo "boton": contorno y cruz llena.
export function svgPriceTower(v, modo = 'carga') {
  const g = geometria(v);
  const pts = [];
  const partes = [0, 1, 2, 3].map((k) => g.parte.map((p) => girar(rot90(p, k), g.giro)));
  const lineas = [0, 1, 2, 3].map((k) => g.linea.map((p) => girar(rot90(p, k), g.giro)));
  const brazo = [[C, -W / 2], [g.alcance, -W / 2], [g.alcance, W / 2], [C, W / 2]];
  const brazos = [0, 1, 2, 3].map((k) => brazo.map((p) => rot90(p, k)));
  partes.flat().forEach((p) => pts.push(p)); brazos.flat().forEach((p) => pts.push(p));
  const ext = Math.max(...pts.map(([x, y]) => Math.max(Math.abs(x), Math.abs(y)))) + 1;
  const esc = 29 / ext;
  const P = ([x, y]) => `${(x * esc + 32).toFixed(2)} ${(y * esc + 32).toFixed(2)}`;
  const cerrado = (lista) => `M${lista.map(P).join('L')}Z`;
  const abierto = (lista) => `M${lista.map(P).join('L')}`;
  if (modo === 'boton') {
    const contorno = g.contorno.map((p) => girar(p, g.giro));
    const llena = [[0, 0], [g.alcance, 0]];
    const cruz = [0, 1, 2, 3].map((k) => abierto(llena.map((p) => rot90(p, k)))).join('');
    return `<svg viewBox="0 0 64 64" aria-hidden="true" fill="none">`
      + `<path d="${cerrado(contorno)}" stroke="currentColor" stroke-width="5"/>`
      + `<path d="${cruz}" stroke="var(--papel)" stroke-width="${(W + 4.6) * esc}"/>`
      + `<path d="${cruz}" stroke="var(--rojo)" stroke-width="${(W + 1.4) * esc}"/>`
      + `<path d="${cerrado([[-C + 0.5, -C + 0.5], [C - 0.5, -C + 0.5], [C - 0.5, C - 0.5], [-C + 0.5, C - 0.5]])}" fill="var(--papel)"/></svg>`;
  }
  let n = 0;
  const caminos = [
    ...partes.map((p) => `<path class="carga-trazo" style="--i:${n++}" pathLength="1" d="${cerrado(p)}"/>`),
    ...lineas.map((p) => `<path class="carga-trazo carga-fina" style="--i:${n++}" pathLength="1" d="${abierto(p)}"/>`),
    ...brazos.map((p) => `<path class="carga-brazo" style="--i:${n++}" pathLength="1" d="${abierto(p)}"/>`),
    `<path class="carga-centro" d="${cerrado([[-C + 0.6, -C + 0.6], [C - 0.6, -C + 0.6], [C - 0.6, C - 0.6], [-C + 0.6, C - 0.6]])}"/>`,
  ];
  return `<svg class="carga-simbolo" viewBox="0 0 64 64" aria-hidden="true" focusable="false" fill="none" stroke-linecap="butt" stroke-linejoin="miter">\n      ${caminos.join('\n      ')}\n    </svg>`;
}
