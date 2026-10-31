# Guggenheim Bilbao (Frank Gehry), desde la ría, medido sobre referencias/simbolos/bilbao guggenhiem/guggen.jpg (1200 px).
# Líneas horizontales sin separación. Cada cáscara de titanio es un polígono medido en px de la foto y se sombrea por su
# pieza, no por la luz de la foto: cada una con un tono parejo (más claro, más oscuro, más cálido o más frío que sus
# vecinas) para que se lean los saltos entre volúmenes; adentro, se aclara u oscurece hasta dos pasos según la luz de
# la foto ajustada a una superficie suave (como una chapa curva, sin las manchas de los reflejos), y las juntas de las chapas apenas marcadas cada tres filas. Se pintan de
# atrás hacia adelante. Encima, la visera y el atrio; abajo, la escalera con el torreón de piedra, el cordón de caliza, el
# estanque, la base del atrio, el muelle y la ría. La araña de la explanada (una escultura) no va.
# Uso: bilbao.py <simbolos.json> (pone decadas.mundo.1990). Necesita la foto en ~/medianeras-originales.
import sys, os
from collections import Counter
from PIL import Image, ImageFilter
from armar import escribir, con_colores

FOTO = os.path.expanduser('~/medianeras-originales/referencias/simbolos/bilbao guggenhiem/guggen.jpg')

X0, X1, Y0, Y1, PASO = 0, 1085, 105, 505, 4
# Cáscaras: (polígono, tonos, juntas). Los tonos van por facetas: [(x hasta donde llega, tono), ...], cada faceta
# distinta de sus vecinas. La primera es el fondo oscuro que llena los huecos entre piezas.
CASCARAS = [
    ([(458, 300), (590, 300), (590, 240), (700, 240), (700, 262), (862, 262), (870, 250), (905, 272), (935, 384),
      (930, 430), (458, 430)], [(1085, 'gb-t5')], False),
    # La sala larga: la parte de abajo, con la punta izquierda (una tanda más) y el resto en sombra.
    ([(0, 352), (14, 340), (112, 334), (113, 322), (200, 325), (300, 333), (450, 345), (560, 362), (650, 345),
      (655, 430), (0, 430)], [(113, 'gb-t3'), (1085, 'gb-t5')], True),
    # La sala larga, arriba: dos bananas. La de la izquierda nace alta en la punta y baja en diagonal; la de atrás
    # nace en punta más a la derecha, se hunde en curva y vuelve a subir hacia la torre.
    ([(204, 223), (250, 231), (300, 246), (350, 265), (400, 279), (450, 288), (500, 289), (560, 280), (602, 272),
      (650, 280), (650, 330), (560, 340), (450, 328), (370, 313), (300, 298), (250, 283), (204, 266)], [(1085, 'gb-t1')], True),
    ([(112, 231), (150, 248), (204, 266), (250, 283), (300, 298), (370, 313), (450, 328), (560, 340), (650, 330),
      (650, 345), (560, 362), (450, 350), (300, 340), (200, 335), (112, 322)], [(1085, 'gb-t3')], True),
    # El tambor chico de atrás y la cáscara clara que asoma en el medio.
    ([(458, 252), (518, 252), (518, 300), (458, 300)], [(1085, 'gb-t3')], True),
    ([(518, 222), (560, 220), (602, 226), (602, 280), (560, 286), (518, 292)], [(1085, 'gb-t0')], True),
    # La flor, medida de cerca: el gris de abajo a la izquierda, la cáscara clara alta, el panel tostado delante,
    # el bloque de bronce del medio, el pétalo inclinado, las piezas de arriba y el filo oscuro de la derecha.
    ([(590, 228), (650, 232), (683, 250), (690, 300), (602, 300), (590, 290)], [(1085, 'gb-t3')], True),
    ([(645, 300), (668, 300), (664, 430), (645, 430), (640, 345)], [(1085, 'gb-t1')], True),
    ([(602, 223), (608, 200), (615, 183), (625, 170), (690, 175), (696, 181), (695, 240), (683, 252), (650, 240),
      (602, 228)], [(1085, 'gb-t0')], True),
    ([(648, 195), (680, 186), (718, 180), (718, 255), (690, 252), (650, 240)], [(1085, 'gb-calido')], True),
    ([(717, 175), (790, 173), (858, 173), (856, 200), (850, 235), (833, 267), (717, 267)], [(765, 'gb-t3'), (1085, 'gb-t2')], True),
    ([(678, 140), (700, 128), (722, 122), (735, 140), (742, 178), (700, 182), (690, 165)], [(1085, 'gb-t1')], True),
    ([(740, 125), (808, 120), (810, 173), (740, 175)], [(1085, 'gb-t4')], True),
    ([(808, 122), (838, 130), (842, 173), (810, 173)], [(1085, 'gb-t2')], True),
    ([(838, 128), (848, 135), (857, 173), (842, 173)], [(1085, 'gb-t5')], True),
    # A la derecha del atrio: el embudo oscuro de arriba, la cáscara dorada y la cinta plateada que se retuerce.
    ([(862, 200), (965, 200), (977, 192), (970, 272), (905, 272), (895, 250), (862, 250)],
     [(920, 'gb-t3'), (1085, 'gb-t4')], True),
    ([(828, 250), (872, 244), (880, 300), (862, 340), (870, 400), (880, 430), (835, 430), (840, 380), (845, 320),
      (835, 300)], [(1085, 'gb-calido')], True),
    ([(872, 244), (905, 262), (910, 300), (905, 340), (915, 380), (940, 430), (880, 430), (870, 400), (862, 340),
      (880, 300)], [(1085, 'gb-frio')], True),
    # El tambor de la derecha: más ancho arriba, se mete abajo sobre la caja de piedra.
    ([(905, 276), (1000, 270), (1082, 278), (1080, 305), (1070, 335), (1060, 360), (1056, 384), (935, 384), (915, 360),
      (908, 320)], [(960, 'gb-t3'), (1085, 'gb-t1')], True),
]

def adentro(x, y, pol):
    d = False
    for (xa, ya), (xb, yb) in zip(pol, pol[1:] + pol[:1]):
        if (ya > y) != (yb > y) and x < xa + (y - ya) * (xb - xa) / (yb - ya): d = not d
    return d

def ajuste(celdas, foto, base):
    # Cuadrados mínimos: la combinación de `base` que mejor sigue la luz de la foto, y su error.
    n = len(base(*celdas[0]))
    A = [[0.0] * (n + 1) for _ in range(n)]
    for q in celdas:
        v = base(*q)
        for i in range(n):
            for j in range(n): A[i][j] += v[i] * v[j]
            A[i][n] += v[i] * foto[q]
    for i in range(n):
        A[i][i] += 1e-3
        p = max(range(i, n), key=lambda r: abs(A[r][i])); A[i], A[p] = A[p], A[i]
        for r in range(n):
            if r != i:
                k = A[r][i] / A[i][i]
                A[r] = [a - k * b for a, b in zip(A[r], A[i])]
    w = [A[i][n] / A[i][i] for i in range(n)]
    luz = {q: sum(a * b for a, b in zip(w, base(*q))) for q in celdas}
    return luz, sum((luz[q] - foto[q]) ** 2 for q in celdas)

def suave(celdas, foto):
    # La luz de la foto sobre una cara, como una chapa curvada en una sola dirección: bandas que siguen el borde de la
    # pieza, de arriba abajo o de lado a lado (la que mejor sigue la foto), sin las manchas de los reflejos.
    if len(celdas) < 12: return {q: foto[q] for q in celdas}
    filas, cols = {}, {}
    for c, f in celdas:
        filas.setdefault(f, []).append(c); cols.setdefault(c, []).append(f)
    def rel(q, eje):
        c, f = q
        a, b = (min(filas[f]), max(filas[f])) if eje == 'x' else (min(cols[c]), max(cols[c]))
        return ((c if eje == 'x' else f) - a) / max(1, b - a)
    opciones = [ajuste(celdas, foto, lambda c, f, e=e: (1, rel((c, f), e), rel((c, f), e) ** 2)) for e in ('x', 'y')]
    return min(opciones, key=lambda r: r[1])[0]

def version():
    W, H = int((X1 - X0) / (PASO / 4)), int((Y1 - Y0) / PASO)
    xy = lambda c, f: (X0 + (c + 0.5) * PASO / 4, Y0 + (f + 0.5) * PASO)
    grid = [['-'] * W for _ in range(H)]
    foto = Image.open(FOTO).convert('L').filter(ImageFilter.GaussianBlur(9)).crop((X0, Y0, X1, Y1)).resize((W, H), Image.BOX).load()
    for pol, tonos, juntas in CASCARAS:
        dentro = {(c, f) for f in range(H) for c in range(W) if adentro(*xy(c, f), pol)}
        # Cada cara mantiene su tono, y adentro se aclara u oscurece hasta dos pasos según la luz de la foto.
        cara = {(c, f): next(n for hasta, n in tonos if xy(c, f)[0] < hasta) for c, f in dentro}
        paso = {}
        for n in set(cara.values()):
            k = [q for q in dentro if cara[q] == n]
            luz = suave(k, foto)
            media = sum(luz.values()) / len(k)
            paso.update({q: max(-2, min(2, round((media - luz[q]) / 16))) for q in k})
        for c, f in dentro:
            base, i = RAMPA[cara[c, f]]
            fam = FAMILIAS[base]
            tono = f'gb-{base}{max(0, min(len(fam) - 1, i + paso[c, f]))}'
            if juntas and (c, f - 1) not in dentro: tono = 'gb-canto'            # el canto de arriba, filoso
            elif juntas and f % 3 == 2: tono += '-j'
            grid[f][c] = tono
    for f in range(H):
        for c in range(W):
            x, y = xy(c, f)
            esc = 380 + (x - 60) * 88 / 230                           # borde de la escalera
            if y >= 478: grid[f][c] = 'gb-muelle'
            elif x < 70 and y >= 384 + 12 * (max(0, 25 - x) / 25) ** 2:
                grid[f][c] = 'gb-caliza' if y < 400 else 'gb-piedra'      # el torreón redondeado de piedra
            elif y > esc and x < 330:
                grid[f][c] = 'gb-escalon' if y < esc + 45 and f % 2 else 'gb-caliza'
            elif y >= 440: grid[f][c] = 'gb-caliza' if 645 <= x < 860 else 'gb-estanque'
            elif y >= 430: grid[f][c] = 'gb-caliza'
            elif 930 <= x < 1057 and y >= 384:                        # la caja de piedra bajo el tambor, con su ventana
                grid[f][c] = 'gb-g7' if x < 940 or (950 <= x < 970 and 395 <= y < 420) else 'gb-caliza'
            elif y >= 290 + 15 * ((x - 765) / (92 if x < 765 else 97)) ** 2 and 664 - (y - 300) * 0.12 <= x < 835:  # el atrio, bajo la visera
                claro = x < 792 + (y - 300) * 0.06
                if claro or grid[f][c] == '-' or grid[f][c][:4] == 'gb-g' and int(grid[f][c][4]) >= 5:
                    inclinado = (x - (y - 300) * (0.18 if claro else -0.12)) % 12 < 1.25
                    grid[f][c] = 'gb-montante' if inclinado else 'gb-vidrio-c' if claro else 'gb-vidrio'
            if 290 <= y < 430 and abs(x - 761) < 9 - (y - 300) * 0.03 + max(0, 312 - y) * 0.6: grid[f][c] = 'gb-columna'
            if adentro(x, y, [(725, 117), (780, 110), (781, 127), (730, 132)]): grid[f][c] = 'gb-vidrio'  # la caja vidriada de arriba
            # La visera: una cáscara curva sobre el atrio. Arriba sube en arco y cae a los dos lados; abajo, el canto
            # en otra curva más playa, y debajo la media luna verde de la cara de abajo.
            u = (x - 765) / (92 if x < 765 else 97)
            if abs(u) <= 1:
                arriba, canto = 250 + 50 * u * u, 290 + 15 * u * u
                if arriba <= y < canto:
                    grid[f][c] = 'gb-visera-c' if y < arriba + 14 else 'gb-canto' if y >= canto - PASO else 'gb-visera'
                elif canto <= y < canto + 8 and abs(u) < 0.75: grid[f][c] = 'gb-verde'
    grid += [['gb-muelle'] * W, ['gb-muelle-o'] * W, ['gb-ria'] * W, ['gb-ria-luz'] * W, ['gb-ria'] * W]
    lineas = []
    for fila in grid:
        tramos = []
        for col in fila:
            if tramos and tramos[-1][0] == col: tramos[-1][1] += 0.25
            else: tramos.append([col, 0.25])
        while tramos and tramos[-1][0] == '-': tramos.pop()
        lineas.append(', '.join(f'{c} {l:g}' for c, l in tramos) or '- 0.25')
    return {'nota': ('Guggenheim Bilbao (Frank Gehry, 1993–1997), desde la ría: las cáscaras de titanio, cada una con su '
                     'tono para que se lean los saltos entre volúmenes, con las juntas de las chapas (la sala larga de la izquierda, que termina en tandas sobre el '
                     'torreón de piedra; la torre alta, la flor, la visera sobre el atrio de vidrio, la cinta que se retuerce '
                     'y el tambor de la derecha sobre su caja de piedra); abajo, la escalera, el estanque, el muelle y la ría.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': W / 4, 'lineas': lineas}

def degrade(a, b, n):
    a, b = [int(a[i:i + 2], 16) for i in (1, 3, 5)], [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return ['#' + ''.join(f'{round(x + (y - x) * k / (n - 1)):02x}' for x, y in zip(a, b)) for k in range(n)]

# Familias de tonos (de claro a oscuro) y dónde cae cada tono de cara.
FAMILIAS = {'g': degrade('#f0ece4', '#3a3736', 9), 'c': degrade('#e2d2b4', '#8a7558', 5), 'f': degrade('#d2d7da', '#6f777c', 5)}
RAMPA = {'gb-t0': ('g', 1), 'gb-t1': ('g', 2), 'gb-t2': ('g', 3), 'gb-t3': ('g', 4), 'gb-t4': ('g', 5), 'gb-t5': ('g', 6),
         'gb-calido': ('c', 2), 'gb-frio': ('f', 2)}
oscurito = lambda h: '#' + ''.join(f'{int(int(h[i:i + 2], 16) * 0.93):02x}' for i in (1, 3, 5))

COLORES = {
    **{f'gb-{b}{i}': (v, v) for b, fam in FAMILIAS.items() for i, v in enumerate(fam)},
    **{f'gb-{b}{i}-j': (oscurito(v), oscurito(v)) for b, fam in FAMILIAS.items() for i, v in enumerate(fam)},
    'gb-canto': ('#f2efe8', '#f2efe8'), 'gb-caliza': ('#d8cdb8', '#d8cdb8'),
    'gb-vidrio': ('#3c4c52', '#3c4c52'), 'gb-vidrio-c': ('#6f8693', '#6f8693'), 'gb-columna': ('#cfc8bc', '#cfc8bc'),
    'gb-visera': ('#7f7569', '#7f7569'), 'gb-visera-c': ('#9c9184', '#9c9184'), 'gb-verde': ('#2f5547', '#2f5547'),
    'gb-piedra': ('#a9a296', '#a9a296'), 'gb-montante': ('#2c3a3e', '#2c3a3e'), 'gb-estanque': ('#3a3d38', '#3a3d38'),
    'gb-muelle': ('#b8ad98', '#b8ad98'), 'gb-escalon': ('#a89c88', '#a89c88'), 'gb-muelle-o': ('#6f6a52', '#6f6a52'),
    'gb-ria': ('#2f3a2e', '#2f3a2e'), 'gb-ria-luz': ('#8a7a50', '#8a7a50'),
}

if __name__ == '__main__':
    ruta = sys.argv[1]
    p = version()
    p['aire'] = round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10
    escribir(ruta, 'mundo', '1990', p, sacar=('grosor', 'alto', 'arcos', 'rectas', 'zonas'))
    texto = con_colores(open(ruta).read(), COLORES, 'gb-')
    open(ruta, 'w').write(texto)
    print(len(p['lineas']), 'líneas, largo', p['largo'])
