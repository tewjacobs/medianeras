# Material: piedra arenisca. Un paño de muro de sillería como el de la catedral de Manchester
# (referencias/simbolos/gotico perpendicular/): hiladas de alturas distintas con piezas de largos distintos,
# cada sillar con su tono (miel, ocre, rosado) jaspeado, la veta en capas que ondulan, juntas hundidas,
# cantos gastados y comidos (menos prolija, más real: pedido del usuario); arriba una moldura de goterón que
# vuela, con su sombra, y el hollín en manchas y chorreaduras despareja.
# Uso: arenisca.py <simbolos.json> (pone materiales."Piedra arenisca").
import sys, math
from armar import Lienzo, guardar, con_sombras

LARGO, FILAS = 96, 48
TONOS = ('ar-miel', 'ar-ocre', 'ar-miel', 'ar-rosa', 'ar-ocre', 'ar-miel', 'ar-gris')

def h(*v):
    n = 5
    for x in v: n = (n * 37 + int(x * 4) * 13 + 7) % 997
    return n

def ruido(x, y, escala):
    # Ruido suave (valores al azar en una grilla, interpolados): manchas que cambian de a poco, no de a celdas.
    gx, gy = x / escala, y / escala
    x0, y0 = int(gx), int(gy)
    tx, ty = gx - x0, gy - y0
    tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
    v = lambda a, b: ((a * 73856093) ^ (b * 19349663) ^ int(escala * 83492791)) % 1000 / 1000
    return (v(x0, y0) * (1 - tx) + v(x0 + 1, y0) * tx) * (1 - ty) + (v(x0, y0 + 1) * (1 - tx) + v(x0 + 1, y0 + 1) * tx) * ty

def sillar(l, a, b, f0, f1, t):
    # La pieza, sin dibujar a regla: el tono jaspeado (manchas suaves más claras y más oscuras, poros), la veta en
    # capas que ondulan, cantos que la luz toma a medias (arriba y a la izquierda) y en sombra (abajo y a la
    # derecha), y las esquinas y bordes comidos por el tiempo.
    c = TONOS[t % len(TONOS)]
    fase = (t % 7) * 0.9
    for f in range(f0, f1):
        for i in range(round(a * 4), round(b * 4)):
            x = i / 4
            n = ruido(x + t * 3, f, 3) * 0.6 + ruido(x, f + t, 1.2) * 0.4
            k = c + '-m' if n > 0.66 else c + '-v' if n < 0.3 else c
            ondula = 0.6 * math.sin(x / 4.5 + fase)
            if round(f + ondula) % 3 == 0 and ruido(x, f * 2 + t, 2.5) > 0.35: k = c + '-v'      # la veta
            if h(i, f, t) % 41 == 0: k = c + '-t'                                         # un poro
            l.c[f][i] = k
    # cantos: la luz los toma a medias, la sombra entera
    for i in range(round(a * 4), round(b * 4)):
        if ruido(i / 4, f0 + t, 2) > 0.3: l.c[f0][i] = c + '-c'
        l.c[f1 - 1][i] = c + '-s'
    for f in range(f0, f1):
        if ruido(a, f + t, 1.5) > 0.25: l.rect(c + '-c', a, a + 0.25, f, f + 1)
        l.rect(c + '-s', b - 0.5, b, f, f + 1)
    # el borde comido: bocados chicos en las esquinas y a lo largo del canto
    for (x, f) in ((a, f0), (b - 0.75, f0), (a, f1 - 1), (b - 0.75, f1 - 1)):
        if h(x, f, t) % 2 == 0: l.rect('ar-junta', x, x + 0.75, f, f + 1)
    for i in range(round(a * 4) + 4, round(b * 4) - 4):
        if ruido(i * 0.9, f0 + t * 5, 1.3) > 0.9: l.c[f0][i] = 'ar-junta'
        if ruido(i * 0.9, f1 + t * 7, 1.3) > 0.92: l.c[f1 - 1][i] = 'ar-junta'

def version():
    l = Lienzo(LARGO, FILAS)
    l.rect('ar-junta', 0, LARGO, 0, FILAS)
    # la moldura de goterón: canto de arriba con luz, la cara, el goterón y la sombra que echa
    for i in range(l.n):
        x = i / 4
        l.c[0][i] = 'ar-miel-c' if ruido(x, 0, 2) > 0.25 else 'ar-miel'
        for f in (1, 2): l.c[f][i] = 'ar-miel-m' if ruido(x, f, 2.5) > 0.6 else 'ar-miel-v' if ruido(x, f, 2.5) < 0.3 else 'ar-miel'
        l.c[3][i] = 'ar-miel-v'
        l.c[4][i] = 'ar-miel-s'
        l.c[5][i] = 'ar-sombra'
    # las hiladas: alturas de 5 a 10 filas, piezas de largos muy distintos, trabadas con la de arriba
    f, k = 6, 0
    while f < FILAS:
        alto = (8, 6, 10, 7, 5, 9, 7)[k % 7]
        f1 = min(FILAS, f + alto)
        x = -((h(k) % 16) * 0.75)
        n = 0
        while x < LARGO:
            largo = 9 + (h(k, n) % 19)
            junta = 0.5 if h(n, k) % 3 else 0.75
            sillar(l, max(0, x), min(LARGO, x + largo - junta), f, f1 - 1 if f1 < FILAS else f1, h(k, n))
            x += largo
            n += 1
        f, k = f1, k + 1
    # el hollín: manchas irregulares, más cerradas arriba bajo la moldura y en chorreaduras que bajan
    # despareja; donde el agua lava, la piedra queda limpia. Oscurece el tono de cada sillar (las juntas quedan).
    for f in range(6, FILAS):
        for i in range(l.n):
            c = l.c[f][i]
            if not c.startswith('ar-') or c.split('-')[1] not in ('miel', 'ocre', 'rosa', 'gris'): continue
            x = i / 4
            chorro = ruido(x * 0.6, 0, 1.5) - (f - 6) / 30                   # columnas anchas que bajan y se apagan
            mancha = ruido(x, f, 6) - 0.45 - (f - 6) / 60
            arriba = 1 - (f - 6) / 5
            v = max(chorro * 1.4, mancha * 1.6, arriba)
            if v > 0.62: l.c[f][i] = 'ar-' + c.split('-')[1] + '-h'
            elif v > 0.4: l.c[f][i] = 'ar-' + c.split('-')[1] + '-t'
    return {'nota': 'Piedra arenisca: sillares de tonos miel, ocre y rosado en hiladas de alturas distintas, '
                    'jaspeados, con la veta en capas, los bordes gastados, juntas hundidas y el hollín manchado '
                    'que baja de la moldura.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

COLORES = {
    'ar-miel': ('#c9ab7c', '#b89c70'), 'ar-ocre': ('#b8935f', '#a68555'), 'ar-rosa': ('#c49a82', '#b38c76'),
    'ar-gris': ('#b0a089', '#9f917c'),
    'ar-junta': ('#6e5c47', '#62523f'), 'ar-sombra': ('#5a4a39', '#504233'),
}
PIEDRA = ('ar-miel', 'ar-ocre', 'ar-rosa', 'ar-gris')
con_sombras(COLORES, PIEDRA, 0.78)
def aclarar(h, k=0.25):
    return '#' + ''.join(f'{round(int(h[i:i + 2], 16) + (255 - int(h[i:i + 2], 16)) * k):02x}' for i in (1, 3, 5))
COLORES.update({c + '-c': tuple(aclarar(v) for v in COLORES[c]) for c in PIEDRA})
con_sombras(COLORES, PIEDRA, 0.9, '-v')                  # la veta y las manchas oscuras
COLORES.update({c + '-m': tuple(aclarar(v, 0.1) for v in COLORES[c]) for c in PIEDRA})   # manchas claras
con_sombras(COLORES, PIEDRA, 0.5, '-h')                  # el hollín
con_sombras(COLORES, PIEDRA, 0.7, '-t')                  # el hollín que se va apagando

if __name__ == '__main__':
    p = version()
    guardar(sys.argv[1], 'materiales', 'Piedra arenisca', p, COLORES, 'ar-')
    print(len(p['lineas']), 'líneas, largo', p['largo'])
