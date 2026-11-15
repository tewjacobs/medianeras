# Banderas con el sistema nuevo (Lienzo): proporciones oficiales, planas (sin sombreado, pedido del usuario).
# Reino Unido: Union Jack 1:2 (60 × 30 de diseño, dibujada al triple, simétrica, con bordes suaves): aspa blanca de 6 con la roja de 2
# centrada (pedido del usuario; en la oficial va corrida), cruz blanca de 10 y roja de 6.
# Estados Unidos: 10:19, trece franjas, cantón de 7 franjas y 0.76 del alto, 50 estrellas en 9 filas (6 y 5).
# Uso: banderas.py <simbolos.json>
import sys, math
from armar import Lienzo, guardar

def color_uk(x, y, W, H):
    # El color de un punto (x a lo ancho, y hacia abajo, en unidades del diseño de 60 × 30). Se calcula en el
    # cuarto de arriba a la izquierda (xm, ym) para que las cuatro aspas sean idénticas. La roja va centrada en
    # la blanca (pedido del usuario; en la oficial va corrida), así cruza justo por el medio.
    xm, ym = min(x, W - x), min(y, H - y)
    if abs(x - W / 2) < 3 or abs(y - H / 2) < 3: return 'uk-rojo'
    if abs(x - W / 2) < 5 or abs(y - H / 2) < 5: return 'uk-blanco'
    d = (ym - xm * H / W) * W / math.hypot(W, H)          # positiva: hacia la línea del medio
    if abs(d) >= 3: return 'uk-azul'
    return 'uk-rojo' if abs(d) < 1 else 'uk-blanco'

def reino_unido():
    E = 3                                               # dibujo al triple del diseño de 60 × 30
    W, H = 60, 30
    l = Lienzo(W * E, H * E)
    for f in range(H * E):
        for i in range(W * E * 4):
            x = (i + 0.5) / 4 / E
            # cuatro muestras a lo alto de la fila: si quedan dos y dos, el color intermedio (borde suave)
            ms = [color_uk(x, (f + (k + 0.5) / 4) / E, W, H) for k in range(4)]
            a = max(set(ms), key=ms.count)
            otros = [m for m in ms if m != a]
            l.c[f][i] = a if ms.count(a) > 2 or not otros else mezcla(a, otros[0])
    return {'nota': 'Bandera del Reino Unido (Union Jack): la cruz roja de San Jorge con su filete blanco sobre las '
                    'aspas de San Andrés y San Patricio.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': W * E, 'lineas': l.lineas()}

def mezcla(a, b):
    return 'uk-m-' + '-'.join(sorted((a[3:], b[3:])))

# La estrella elegida (de varias formas de rasterizar una de cinco puntas, la más pareja), en cuartos de
# unidad por fila; se estampa igual en las cincuenta, así son todas idénticas.
ESTRELLA = (
    '................#................',
    '...............###...............',
    '.............#######.............',
    '........#################........',
    '...........###########...........',
    '..........#####...#####..........',
)

def estrella(l, cx, cy):
    i0, f0 = round(cx * 4) - 16, round(cy) - 3
    for df, fila in enumerate(ESTRELLA):
        for di, ch in enumerate(fila):
            if ch == '#' and 0 <= f0 + df < len(l.c) and 0 <= i0 + di < l.n: l.c[f0 + df][i0 + di] = 'us-estrella'

def estados_unidos():
    # Medidas oficiales (en partes del alto): cantón 0.5385 × 0.76, estrellas de 0.0616 de diámetro,
    # separadas 0.054 en alto y 0.063 en ancho. Franjas de 8 filas para que las estrellas tengan forma.
    H = 104
    W = round(H * 1.9 * 4) / 4
    l = Lienzo(W, H)
    for k in range(13): l.rect('us-rojo' if k % 2 == 0 else 'us-blanco', 0, W, k * 8, k * 8 + 8)
    ca, ch = round(H * 0.76 * 4) / 4, 56
    l.rect('us-azul', 0, ca, 0, ch)
    E, F, G, K = 0.054 * H, 0.054 * H, 0.063 * H, 0.063 * H
    for fila in range(9):
        cy = E + fila * F
        n = 6 if fila % 2 == 0 else 5
        for k in range(n):
            cx = G + (2 * k + fila % 2) * K
            estrella(l, cx, cy)
    return {'nota': 'Bandera de Estados Unidos: trece franjas rojas y blancas y el cantón azul con las cincuenta '
                    'estrellas en nueve filas de seis y cinco.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': W, 'lineas': l.lineas()}

COLORES = {
    'uk-azul': ('#1f3d7a', '#2a4a8a'), 'uk-rojo': ('#c8202f', '#c8303c'), 'uk-blanco': ('#f4f1ea', '#e6e3dc'),
    'us-azul': ('#2a3b6e', '#34467c'), 'us-rojo': ('#b52a36', '#b8343f'), 'us-blanco': ('#f4f1ea', '#e6e3dc'),
    'us-estrella': ('#f4f1ea', '#e6e3dc'),
}
def medio(a, b): return '#' + ''.join(f'{(int(a[i:i + 2], 16) + int(b[i:i + 2], 16)) // 2:02x}' for i in (1, 3, 5))
for a, b in (('azul', 'blanco'), ('azul', 'rojo'), ('blanco', 'rojo')):
    COLORES[f'uk-m-{a}-{b}'] = tuple(medio(COLORES['uk-' + a][k], COLORES['uk-' + b][k]) for k in range(2))

if __name__ == '__main__':
    for clave, p in (('Reino Unido', reino_unido()), ('Estados Unidos', estados_unidos())):
        p['placa'] = 'noche'
        guardar(sys.argv[1], 'paises', clave, p, COLORES, 'uk-|us-|bd-')
        print(clave, len(p['lineas']), 'líneas, largo', p['largo'])
