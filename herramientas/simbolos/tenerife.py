# Auditorio de Tenerife (Santiago Calatrava), calcado de referencias/simbolos/tardomoderna/Tenerife_auditorio_5-1920x1430.jpg.
# Líneas horizontales sin separación: cada celda (1 de alto, 0.25 de largo) toma el color medio de su pedazo de foto y se
# clasifica en pocos tonos: el cielo se inunda desde arriba (solo avanza por azules fuertes que cambian suave), las cáscaras
# blancas al sol, las que están en sombra (azuladas), la ola de hormigón, su cara de abajo en sombra, lo oscuro y el muro.
# Después se alisa con la moda de los vecinos para que no queden pelusas.
# Uso: tenerife.py <simbolos.json> (pone estilos.Moderno tardío). Necesita la foto en ~/medianeras-originales.
import sys, os
from collections import Counter
from PIL import Image
from armar import guardar

FOTO = os.path.expanduser('~/medianeras-originales/referencias/simbolos/tardomoderna/Tenerife_auditorio_5-1920x1430.jpg')
K = 1920 / 900                                  # medidas tomadas sobre la foto achicada a 900 px
X0, X1, Y0, Y1, PASO = 45, 885, 92, 462, 5      # recorte y px por fila
MURO = 68                                       # desde esta fila, el muro de la explanada

def muestra():
    filas, cols = int((Y1 - Y0) / PASO), int((X1 - X0) / (PASO / 4))
    g = Image.open(FOTO).convert('RGB').crop((int(X0 * K), int(Y0 * K), int(X1 * K), int(Y1 * K))).resize((cols, filas), Image.BOX)
    return g.load(), cols, filas

def cielo(px, W, H):
    azul = lambda p: p[2] - p[0] > 60 and p[2] > 190
    hecho, pila = set(), [(c, 0) for c in range(W)] + [(500, 56)]   # el cielo de arriba y el triangulito bajo la ola
    while pila:
        c, f = pila.pop()
        if (c, f) in hecho or not azul(px[c, f]): continue
        hecho.add((c, f))
        for n in ((c + 1, f), (c - 1, f), (c, f + 1), (c, f - 1)):
            if 0 <= n[0] < W and 0 <= n[1] < H and max(abs(a - b) for a, b in zip(px[c, f], px[n])) < 22: pila.append(n)
    hecho |= {(c, f) for f in range(62) for c in range(150)}       # nubes y montañas del fondo, a la izquierda
    return hecho

def tono(p, f):
    r, g, b = p; l = (r + g + b) / 3
    if f >= MURO: return 'tt-muro' if l < 170 else 'tt-blanco'
    if l > 185: return 'tt-blanco'
    if l < 65: return 'tt-oscuro'
    if b - r > 45: return 'tt-azul'
    return 'tt-ola' if l > 100 else 'tt-ola-s'

def moda(grid, rx=3, ry=1):
    H, W = len(grid), len(grid[0])
    return [[Counter(grid[ff][cc] for ff in range(max(0, f - ry), min(H, f + ry + 1))
                     for cc in range(max(0, c - rx), min(W, c + rx + 1))).most_common(1)[0][0] for c in range(W)] for f in range(H)]

def entrada(grid):
    # La boca bajo el arco, redibujada: su hueco sale del calco (y se ensancha parejo hacia abajo); adentro, el canto gris
    # del arco, el techo encendido, la faja recta del balcón con su baranda y el vidrio con columnas parejas.
    luz, BALCON, previo, tramos = ('tt-blanco', 'tt-azul', '-'), 62, None, {}
    for f in range(50, MURO):
        a = b = 300
        if grid[f][a] in luz: continue
        while a > 0 and grid[f][a - 1] not in luz: a -= 1
        while b < len(grid[f]) - 1 and grid[f][b + 1] not in luz: b += 1
        if previo: a, b = min(a, previo[0]), max(b, previo[1])
        tramos[f] = previo = (a, b)
    for f in range(44, MURO):                                         # sin motas grises en la cáscara de encima
        for c in range(170, 460):
            if grid[f][c] in ('tt-ola', 'tt-ola-s') and not (f in tramos and tramos[f][0] <= c <= tramos[f][1]):
                grid[f][c] = 'tt-blanco'
    for f, (a, b) in tramos.items():
        fila, arriba = grid[f], [tramos.get(f - k) for k in (1, 2)]
        for c in range(a, b + 1):
            canto = c < a + 6 or c > b - 6 or any(t is None or not t[0] <= c <= t[1] for t in arriba)
            fila[c] = 'tt-ola-s' if canto else 'tt-ola' if f == BALCON else 'tt-luz'
            if not canto and ((f == BALCON + 1 and c % 6 < 2) or (f > BALCON + 1 and c % 16 < 2)): fila[c] = 'tt-montante'

def limpiar(grid):
    # Abajo, sin azules sueltos (escalera de la izquierda, terraza de la derecha) y sin tramos de menos de 1.
    for f in range(56, len(grid)):
        for c, col in enumerate(grid[f]):
            if col == 'tt-azul': grid[f][c] = 'tt-blanco' if c < 130 else 'tt-ola-s'
    for fila in grid:
        c = 0
        while c < len(fila):
            d = c
            while d < len(fila) and fila[d] == fila[c]: d += 1
            if d - c < 4 and c > 0: fila[c:d] = [fila[c - 1]] * (d - c)
            c = d
    entrada(grid)
    for f in range(62, MURO):                                         # el ala baja de la izquierda y su escalera
        grid[f][4:124] = ['tt-blanco'] * 120
        a = 52 + (f - 62) * 6
        grid[f][a:a + 10] = ['tt-ola'] * 10
    for f in range(MURO, len(grid)): grid[f] = ['tt-muro'] * len(grid[f])
    return grid

def version():
    px, W, H = muestra()
    vacio = cielo(px, W, H)
    grid = moda([['-' if (c, f) in vacio else tono(px[c, f], f) for c in range(W)] for f in range(H)])
    grid = limpiar(grid[:MURO + 3])                                  # el muro, de tres filas
    lineas = []
    for fila in grid:
        tramos = []
        for col in fila:
            if tramos and tramos[-1][0] == col: tramos[-1][1] += 0.25
            else: tramos.append([col, 0.25])
        while tramos and tramos[-1][0] == '-': tramos.pop()
        lineas.append(', '.join(f'{c} {l:g}' for c, l in tramos) or '- 0.25')
    return {'nota': ('El Auditorio de Tenerife (Santiago Calatrava, 2003), de frente como en la foto desde el mar, calcado: '
                     'la ola de hormigón gris que nace a la derecha, sube y se afina hasta la punta sobre la izquierda, con su '
                     'cara de abajo en sombra; debajo, las cáscaras blancas, al sol y en sombra azulada; la boca oscura de la '
                     'entrada bajo el arco; abajo, el muro de la explanada.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': W / 4, 'lineas': lineas}

COLORES = {
    'tt-blanco': ('#ecebe6', '#ecebe6'), 'tt-azul': ('#a3b1c6', '#a3b1c6'), 'tt-ola': ('#a29f9a', '#a29f9a'),
    'tt-ola-s': ('#6c6b70', '#6c6b70'), 'tt-oscuro': ('#2c2f3a', '#2c2f3a'), 'tt-muro': ('#7a6a62', '#7a6a62'),
    'tt-luz': ('#2c2f3a', '#d4a95c'), 'tt-montante': ('#6c6b70', '#8a6a3a'),
}

p = version()
p.update(placa='au-cielo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='au-cielo-marco')
guardar(sys.argv[1], 'estilos', 'Moderno tardío', p, COLORES, 'tt-|au-(?!cielo)')
print(len(p['lineas']), 'líneas, largo', p['largo'])
