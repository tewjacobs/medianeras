# Taller Sterner (Ernest Delune, rue du Lac 6, Ixelles, Bruselas), la fachada de frente.
# Medida en px sobre referencias/simbolos/art nouveau/rkh79myno1l71.jpg reducida a 750 × 1000.
# Solo la fachada (sin los vecinos, pedido del usuario): ladrillo claro con esquinas de piedra.
# Arriba el mirador de madera clara: alero con cabios curvos, paños vidriados (los de abajo de bloques de
# vidrio), base con tableros, baranda de hierro con latigazo y ménsulas. Abajo, las dos ménsulas huecas de
# piedra, la ventana de la izquierda con las esquinas curvas, el gran vitral redondo de violetas sobre el
# ventanal que baja en escalones, la imposta, la puerta en arco de herradura con su columnita y el ojo
# redondo, la gárgola, la ventana del sótano con la reja de latigazo y la vereda.
# Sombreado con luz arriba a la izquierda: sombra debajo del mirador, de imposta y antepechos, adentro de
# cada hueco (arriba y a la izquierda) y en las caras que miran a la derecha; anillos con degradé.
# Uso: sterner.py <simbolos.json> (pone estilos."Art nouveau").
import sys, math
from armar import Lienzo, guardar, con_sombras

S = 0.22                                   # unidades por px
X0, X1, Y0, Y1 = 120, 605, 28, 1036
SUELO = 1000
LARGO = round((X1 - X0) * S)
FILAS = round((Y1 - Y0) * S)
FL, FR = 122, 603                          # bordes de la fachada

def q(x): return round(x * 4) / 4
def ux(px): return q((px - X0) * S)
def fy(py): return round((py - Y0) * S)
def py(f): return Y0 + (f + 0.5) / S
def px(i): return X0 + (i + 0.5) / 4 / S    # centro de la columna i (de 0.25)

def P(l, c, x0, x1, y0, y1):
    l.rect(c, ux(x0), ux(x1), fy(y0), max(fy(y0) + 1, fy(y1)))

def celdas(l, x0, x1, y0, y1, color):
    # Pinta celda por celda lo que diga color(x, y) (en px de la foto); None deja lo que había.
    for f in range(max(0, fy(y0)), min(FILAS, fy(y1))):
        for i in range(max(0, round(ux(x0) * 4)), min(l.n, round(ux(x1) * 4))):
            c = color(px(i), py(f))
            if c: l.c[f][i] = c

def disco(l, cx, cy, r, color):
    # Círculo: color(dx, dy) con dx, dy relativos al centro (px).
    celdas(l, cx - r, cx + r, cy - r, cy + r,
           lambda x, y: color(x - cx, y - cy) if (x - cx) ** 2 + (y - cy) ** 2 <= r * r else None)

def anillo_luz(cl, cm, cs):
    # Degradé de un anillo con luz arriba a la izquierda.
    def color(dx, dy):
        d = (-dx - dy) / (math.hypot(dx, dy) or 1)
        return cl if d > 0.45 else cs if d < -0.45 else cm
    return color

def ladrillo(l, x0, x1, y0, y1, c='an-ladrillo', j='an-junta'):
    # Ladrillo claro: hiladas de dos filas con la junta abajo y llagas trabadas.
    P(l, c, x0, x1, y0, y1)
    for f in range(fy(y0), fy(y1)):
        if f % 2: l.rect(j, ux(x0), ux(x1), f, f + 1)
        else:
            x = ux(x0) + (f // 2 % 2) * 1.5
            while x < ux(x1):
                l.rect(j, x, x + 0.25, f, f + 1)
                x += 3

def sillares(l, x0, x1, y0, y1, corto, paso=26, alterna=True):
    # Esquina de piedra: sillares de `paso` px de alto, uno largo y otro corto (`corto` px), con la junta.
    k = 0
    y = y0
    while y < y1:
        b = min(y1, y + paso)
        b1 = x0 + corto if alterna and k % 2 else x1
        P(l, 'an-piedra', x0, b1, y, b)
        P(l, 'an-piedra-c', x0, b1, y, y + 4)
        y = b + 5
        k += 1

def sillares_der(l, x0, x1, y0, y1, corto, paso=26):
    # Como sillares, pero los cortos pegados al lado derecho.
    k, y = 0, y0
    while y < y1:
        b = min(y1, y + paso)
        a = x1 - corto if k % 2 else x0
        P(l, 'an-piedra', a, x1, y, b)
        P(l, 'an-piedra-c', a, x1, y, y + 4)
        P(l, 'an-piedra-s', x1 - 4, x1, y, b)                     # canto de la derecha, en sombra
        y = b + 5
        k += 1

# Vitrales: fondo ámbar con varillas de plomo, ramos de violetas y hojas turquesa.
VIOLETAS = ('an-violeta', 'an-lila', 'an-purpura', 'an-violeta', 'an-azul', 'an-purpura')

def violeta(l, x, y, k):
    # Una violeta prolija: dos pétalos arriba, dos a los lados con el ojo dorado, uno abajo en sombra.
    c = VIOLETAS[k % len(VIOLETAS)]
    o = 'an-violeta-o' if c != 'an-azul' else 'an-azul-o'
    u, f = ux(x), fy(y)
    l.rect(c, u - 1, u - 0.25, f - 1, f)
    l.rect(c, u + 0.5, u + 1.25, f - 1, f)
    l.rect(c, u - 1.25, u, f, f + 1)
    l.rect('an-oro', u, u + 0.25, f, f + 1)
    l.rect(c, u + 0.25, u + 1.5, f, f + 1)
    l.rect(o, u - 0.5, u + 0.75, f + 1, f + 2)

def ramo(l, cx, cy, r, k0=0):
    # Racimo redondo de violetas, cada una separada de la otra.
    k = k0
    for j, dy in enumerate(range(-int(r), int(r) + 1, 14)):
        w = math.sqrt(max(0, r * r - dy * dy))
        x = cx - w + (j % 2) * 6.5
        while x <= cx + w:
            violeta(l, x, cy + dy, k)
            x += 13
            k += 1

def tallos(l, x0, x1, y0, y1, n, abre=0.0, c='an-tallo'):
    # Varillas que suben del pie y se abren hacia arriba (abre: cuánto se curvan hacia afuera).
    for f in range(fy(y0), fy(y1)):
        t = (py(f) - y0) / (y1 - y0)                             # 0 arriba, 1 abajo
        for k in range(n):
            s = (k + 0.5) / n - 0.5
            x = (x0 + x1) / 2 + s * (x1 - x0) * (1 - abre * t * t)
            l.rect(c, ux(x), ux(x) + 0.25, f, f + 1)

def hojas(l, x0, x1, y0, y1):
    # Hojas turquesa en abanico, como palmas que nacen abajo en el medio: anchas en el medio y en punta.
    P(l, 'an-turquesa-o', x0, x1, y0, y1)
    bx, alto = (x0 + x1) / 2, y1 - y0
    for k, a in enumerate((-62, -38, -14, 14, 38, 62)):
        ang = math.radians(a)
        for f in range(fy(y0), fy(y1)):
            t = (y1 - py(f)) / alto                                 # 0 abajo, 1 arriba
            x = bx + math.sin(ang) * alto * 1.4 * t
            w = 3.2 * math.sin(math.pi * min(1, t * 1.1))           # ancho de la hoja
            if w <= 0.3: continue
            c = 'an-turquesa-c' if k % 2 else 'an-turquesa'
            a0, a1 = max(ux(x0), ux(x - w)), min(ux(x1), ux(x + w))
            if a1 > a0:
                l.rect(c, a0, a1, f, f + 1)
                l.rect('an-turquesa-o', ux(x), ux(x) + 0.25, f, f + 1) if a0 < ux(x) < a1 else None   # nervio

def pano(l, x0, x1, y0, y1, motivo):
    # Paño de vitral con su motivo y el plomo del borde.
    if motivo == 'hojas': hojas(l, x0, x1, y0, y1)
    else:
        P(l, 'an-ambar', x0, x1, y0, y1)
        P(l, 'an-ambar-c', x0, (x0 + x1) / 2, y0, y1)              # más luz del lado de la izquierda
        for f in range(fy(y0), fy(y1)):                            # tallos claros que suben y se curvan
            t = (py(f) - y0) / (y1 - y0)
            for k, s in enumerate((0.2, 0.42, 0.6, 0.8)):
                x = x0 + (x1 - x0) * s + 9 * (1 - t) ** 2 * (1 if k % 2 else -1)
                if x0 < x < x1 - 1: l.rect('an-tallo', ux(x), ux(x) + 0.25, f, f + 1)
        if motivo in ('violetas', 'ramito'):                        # ramo en diagonal, como en la foto
            cx, cy = ((x0 + x1) / 2, (y0 + y1) / 2) if motivo == 'violetas' else (x1 - 14, y1 - 22)
            for k, (ddx, ddy) in enumerate(((-9, 6), (3, 3), (-3, -6), (9, -6), (-12, 15), (6, -14), (0, 12))):
                violeta(l, cx + ddx, cy + ddy, k + (2 if x0 > 470 else 0))

def version():
    l = Lienzo(LARGO, FILAS)

    # Fachada: ladrillo claro y esquinas de piedra.
    ladrillo(l, FL, FR, 40, SUELO)
    sillares(l, FL, FL + 30, 52, SUELO, 18)
    sillares_der(l, FR - 30, FR, 52, SUELO, 18)
    for x0, x1 in ((FL + 12, 182), (552, FR - 12)):                 # remates de los pilares
        P(l, 'an-piedra', x0, x1, 32, 54)
        P(l, 'an-piedra-c', x0, x1, 32, 37)
        P(l, 'an-piedra-s', x0 + 6, x1 - 6, 46, 54)
        P(l, 'an-piedra-s', x1 - 5, x1, 32, 54)

    # Mirador.
    P(l, 'an-ladrillo-s', FL, FR, 338, 372)                        # sombra que tira sobre la pared
    for f in range(fy(338), fy(372)):
        if f % 2: l.rect('an-junta-s', ux(FL), ux(FR), f, f + 1)
    m = Lienzo(LARGO, FILAS)                                       # el mirador se dibuja aparte y después se tuerce
    # Base: antepecho volado, tableros con moldura, viga y ménsulas en ese.
    P(m, 'an-madera', 140, 595, 262, 306)
    P(m, 'an-madera-c', 140, 232, 262, 306)                       # cara de la izquierda (en ángulo), con luz
    P(m, 'an-madera-s', 500, 595, 262, 306)                       # cara de la derecha, en sombra
    for x0, x1 in ((150, 224), (248, 302), (322, 408), (432, 488), (510, 586)):
        izq, der = x0 < 240, x0 > 500
        P(m, 'an-madera-ss' if der else 'an-madera-s', x0, x1, 270, 300)   # tablero rehundido
        P(m, 'an-madera-s' if der else 'an-madera-c' if izq else 'an-madera', x0 + 3, x1 - 3, 273, 297)
        P(m, 'an-madera-ss' if der else 'an-madera-s', x0, x1, 270, 273)  # sombra arriba y a la izquierda adentro
        P(m, 'an-madera-ss' if der else 'an-madera-s', x0, x0 + 3, 270, 300)
        P(m, 'an-madera' if der else 'an-madera-c', x0, x1, 297, 300)     # canto de abajo con luz
        P(m, 'an-madera' if der else 'an-madera-c', x1 - 3, x1, 270, 300)
    for x0, x1 in ((232, 240), (500, 508)):                       # aristas del mirador
        P(m, 'an-madera-c', x0, x0 + 3, 262, 306)
        P(m, 'an-madera-s', x1 - 3, x1, 262, 306)
    P(m, 'an-madera-c', 136, 599, 254, 258)                       # antepecho: canto con luz, frente, sombra abajo
    P(m, 'an-madera', 136, 599, 258, 262)
    P(m, 'an-madera-ss', 140, 595, 262, 265)
    P(m, 'an-madera', 136, 599, 306, 314)                          # viga de abajo
    P(m, 'an-madera-c', 136, 599, 306, 308)
    P(m, 'an-madera-ss', 140, 595, 314, 318)
    for x in (148, 197, 227, 265, 305, 342, 380, 417, 457, 497, 527, 585):
        for f in range(fy(314), fy(340)):                         # ménsula en ese: ancha arriba, fina abajo
            t = (py(f) - 314) / 26
            w = 5 - 3 * t
            m.rect('an-madera', ux(x - w), ux(x + w), f, f + 1)
            m.rect('an-madera-c', ux(x - w), ux(x - w) + 0.25, f, f + 1)
            m.rect('an-madera-ss', ux(x + w), ux(x + w) + 0.75, f, f + 1)   # su sombra
    P(m, 'an-madera-ss', 140, 595, 338, 342)
    # Paños vidriados: arriba el cielo reflejado, abajo bloques de vidrio.
    for x0, x1, lado in ((150, 232, 'i'), (240, 307, 'f'), (315, 362, 'f'), (370, 420, 'f'), (427, 490, 'f'),
                         (500, 585, 'd')):
        P(m, 'an-vidrio-c' if lado == 'i' else 'an-vidrio-s' if lado == 'd' else 'an-vidrio', x0, x1, 104, 254)
        P(m, 'an-vidrio-c' if lado != 'd' else 'an-vidrio', x0, x0 + 6, 104, 186)   # brillo
        P(m, 'an-vidrio-s', x0, x1, 104, 110)                     # sombra del dintel en el vidrio
        P(m, 'an-bloque' if lado != 'd' else 'an-bloque-s', x0, x1, 186, 254)
        for y in range(186, 254, 17):
            P(m, 'an-bloque-j', x0, x1, y, y + 3)
        for x in range(x0 + 2, x1, 20):
            P(m, 'an-bloque-j', x, x + 3, 186, 254)
    P(m, 'an-interior', 248, 304, 114, 236)                       # el cuarto de adentro: pared y una ventana
    P(m, 'an-interior-o', 258, 300, 124, 226)
    for x in (270, 284):
        P(m, 'an-interior', x, x + 3, 124, 226)
    for y in (148, 174, 200):
        P(m, 'an-interior', 258, 300, y, y + 3)
    P(m, 'an-bloque', 248, 304, 186, 254)
    for y in range(186, 254, 17):
        P(m, 'an-bloque-j', 248, 304, y, y + 3)
    for x0, x1 in ((140, 150), (232, 240), (307, 315), (362, 370), (420, 427), (490, 500), (585, 595)):
        P(m, 'an-madera', x0, x1, 100, 254)                       # montantes: canto con luz y sombra a la derecha
        P(m, 'an-madera-c', x0, x0 + 3, 100, 254)
        P(m, 'an-madera-s', x1 - 2, x1, 100, 254)
        P(m, 'an-vidrio-s', x1, x1 + 3, 110, 254)
    # Baranda de hierro (medida sobre un recorte de 452 × 260 de la foto): barra de arriba con las puntas
    # en rulo, dos parantes, el respaldo curvo de "sillón" con los brazos enrulados, el lazo del medio, tres
    # barras abajo y cuatro gotas colgando. Su sombra cae corrida en el tablero.
    def bx(x): return 300 + (x - 35) * 0.346
    def by(y): return 238 + (y - 30) * 0.346
    def curva(c, pts, d, g=0.5):
        # Línea por puntos (en px del recorte), fila por fila, de grosor g unidades.
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            n = max(2, int(abs(yb - ya) * 0.346 * S * 3) + int(abs(xb - xa) * 0.346 * S * 4))
            for k in range(n + 1):
                x, y = bx(xa + (xb - xa) * k / n) + d, by(ya + (yb - ya) * k / n) + d
                m.rect(c, ux(x) - g / 2, ux(x) + g / 2, fy(y), fy(y) + 1)
    for d, c in ((4, 'an-madera-s'), (0, 'an-reja')):
        curva(c, [(35, 32), (395, 32)], d)                                    # barra de arriba
        curva(c, [(35, 32), (30, 45), (45, 50)], d)
        curva(c, [(395, 32), (400, 45), (385, 50)], d)
        for x in (162, 269):
            curva(c, [(x, 32), (x, 215)], d)                                  # parantes
        curva(c, [(45, 72), (110, 58), (215, 48), (320, 58), (385, 72)], d)  # respaldo
        curva(c, [(45, 72), (70, 95), (95, 118), (110, 128), (122, 120), (112, 108)], d)   # brazo izquierdo
        curva(c, [(385, 72), (360, 95), (335, 118), (320, 128), (308, 120), (318, 108)], d)
        curva(c, [(182, 52), (180, 80), (198, 98), (215, 100), (232, 98), (250, 80), (248, 52)], d)  # lazo
        curva(c, [(198, 60), (200, 82), (215, 88), (230, 82), (232, 60)], d)
        for y, a, b in ((100, 135, 295), (140, 100, 330), (160, 105, 325)):  # barras de abajo
            curva(c, [(a, y), (b, y)], d)
        curva(c, [(140, 100), (132, 92), (140, 86)], d)
        curva(c, [(290, 100), (298, 92), (290, 86)], d)
        for x in (100, 185, 245, 325):                                        # gotas
            curva(c, [(x, 160), (x, 185)], d)
            curva(c, [(x - 5, 185), (x + 5, 185)], d, 1)
    # Alero: corona clara arriba, cielorraso en sombra (más hondo arriba) y cabios curvos.
    for f in range(fy(58), fy(100)):
        t = (py(f) - 58) / 42
        m.rect('an-madera-ss' if t < 0.45 else 'an-madera-s', ux(140), ux(595), f, f + 1)
    for f in range(fy(32), fy(60)):
        d = max(0, (60 - py(f)) * 0.55)                            # esquinas de arriba en chanfle
        m.rect('an-madera', ux(138 + d), ux(597 - d), f, f + 1)
        m.rect('an-madera-c', ux(138 + d), ux(138 + d) + 1, f, f + 1)
        m.rect('an-madera-s', ux(597 - d) - 1, ux(597 - d), f, f + 1)
    P(m, 'an-madera-c', 152, 583, 32, 37)                          # tapa con luz
    P(m, 'an-madera-s', 146, 589, 46, 49)                          # moldura
    P(m, 'an-madera-c', 140, 595, 49, 52)
    P(m, 'an-madera-ss', 140, 595, 58, 61)                         # sombra de la corona
    for x in (157, 182, 207, 232, 262, 296, 330, 365, 400, 437, 472, 500, 530, 557, 580):
        s = (x - 368) / 220                                        # los de las puntas se curvan hacia afuera
        for f in range(fy(60), fy(98)):
            t = (py(f) - 60) / 38
            xx = x + s * 16 * (1 - t) ** 2
            m.rect('an-madera', ux(xx) - 0.5, ux(xx) + 0.25, f, f + 1)
            m.rect('an-madera-c', ux(xx) - 0.5, ux(xx) - 0.25, f, f + 1)
            m.rect('an-madera-ss', ux(xx) + 0.25, ux(xx) + 0.5, f, f + 1)
    P(m, 'an-madera', 138, 597, 92, 100)                           # solera
    P(m, 'an-madera-c', 138, 597, 92, 94)
    P(m, 'an-madera-ss', 140, 595, 100, 104)
    # Las caras en ángulo se van hacia atrás: sus líneas bajan hacia afuera, como se ve en la foto (no es una
    # caja rectangular). Se corre cada columna hacia abajo, más cuanto más afuera.
    for i in range(m.n):
        x = px(i)
        s = 16 * (232 - x) / 96 if x < 232 else 16 * (x - 500) / 99 if x > 500 else 0
        d = round(max(0, s) * S)
        for f in range(FILAS - 1, -1, -1):
            j = i
            if py(f) >= 100:                                       # el cuerpo, 6 % más angosto: el alero sale más
                j = round(ux(368) * 4 + (i - ux(368) * 4) / 0.94)
                if not 0 <= j < m.n: continue
            c = m.c[f][j]
            if c != '-' and f + d < FILAS: l.c[f + d][i] = c
    # El mirador vuela: sombra sobre el pilar de la derecha.
    l.sombra(ux(597), ux(FR), fy(54), fy(342), ('an-ladrillo', 'an-junta', 'an-piedra', 'an-piedra-c'))

    # Ménsulas de piedra huecas a los lados, debajo del mirador.
    for x0, x1 in ((FL, 162), (566, FR)):
        P(l, 'an-piedra', x0, x1, 354, 396)
        P(l, 'an-piedra-c', x0, x1, 354, 359)
        cx = (x0 + x1) / 2
        disco(l, cx + 1, 384, 12, lambda dx, dy: ('an-piedra-ss' if dx < 3 else 'an-piedra-s') if dy < 4 else None)
        P(l, 'an-piedra-s', x1 - 4, x1, 359, 396)

    # Ventana de la izquierda (medida sobre el recorte de la foto): marco de piedra con orejas dentadas,
    # carpintería crema; arriba una fila de vidrios chicos (los de afuera con la esquina curva) y tres paños;
    # travesaño; abajo tres paños, el del medio con el fondo curvo y dos vidrios chicos debajo.
    sillares(l, 164, 188, 356, 615, 12, 24)
    sillares_der(l, 300, 324, 356, 615, 12, 24)
    P(l, 'an-piedra', 175, 314, 356, 366)
    P(l, 'an-piedra-c', 175, 314, 356, 359)
    P(l, 'an-marco', 186, 306, 362, 596)
    P(l, 'an-marco-c', 186, 189, 362, 596)
    def pano_v(x0, x1, y0, y1, curva=None):
        # Vidrio claro con un reflejo arriba a la izquierda; curva: 'ti'/'td' esquina de arriba, 'u' fondo curvo.
        def col(x, y):
            if curva in ('ti', 'td'):
                cx = x0 + 10 if curva == 'ti' else x1 - 10
                if (x < cx if curva == 'ti' else x > cx) and y < y0 + 10 and (x - cx) ** 2 + (y - y0 - 10) ** 2 > 100: return None
            if curva == 'u':
                r = (x1 - x0) / 2
                if y > y1 - r and (x - x0 - r) ** 2 + (y - y1 + r) ** 2 > r * r: return None
            return 'an-cristal-c' if (x - x0) + (y - y0) * 0.5 < 10 else 'an-cristal'
        celdas(l, x0, x1, y0, y1, col)
    pano_v(192, 215, 366, 393, 'ti')
    pano_v(219, 270, 366, 393)
    pano_v(274, 300, 366, 393, 'td')
    for x0, x1 in ((192, 215), (219, 270), (274, 300)):
        pano_v(x0, x1, 398, 490)
    P(l, 'an-cortina', 222, 268, 404, 488)
    P(l, 'an-marco', 186, 306, 490, 512)                           # travesaño
    P(l, 'an-marco-c', 186, 306, 490, 493)
    pano_v(192, 215, 514, 592)
    pano_v(274, 300, 514, 592)
    pano_v(219, 270, 514, 572, 'u')
    pano_v(219, 243, 576, 592)
    pano_v(247, 270, 576, 592)
    P(l, 'an-piedra', 170, 318, 596, 608)                          # antepecho con molduras
    P(l, 'an-piedra-c', 170, 318, 596, 599)
    P(l, 'an-piedra-s', 170, 318, 605, 608)
    P(l, 'an-ladrillo-s', 175, 314, 608, 613)

    # Vitral grande: el ventanal que baja en escalones, el ojo redondo y el anillo de piedra.
    # El anillo es medio círculo arriba que sigue recto en las jambas, con las mismas bandas: así se unen
    # sin escalón. Radios: canto 103, moldura con su ranura 91–89, borde del hueco 78.
    def banda(d, lado):
        # Color de la banda a la distancia d del centro; lado -1 izquierda, 1 derecha, 0 arriba.
        if d > 99: return 'an-piedra-c' if lado <= 0 else 'an-piedra-s'
        if 89 <= d <= 91: return 'an-piedra-s' if lado <= 0 else 'an-piedra-c'
        return 'an-piedra'
    def anillo(dx, dy):
        d = math.hypot(dx, dy)
        if dy > 0 or d > 103 or d < 78: return None
        a = (-dx - dy) / (d or 1)                                   # luz arriba a la izquierda
        c = banda(d, -1 if a > 0.45 else 1 if a < -0.45 else 0)
        if c == 'an-piedra' and a < -0.45: c = 'an-piedra-s' if d < 84 else c
        return c
    disco(l, 453, 482, 103, anillo)
    for x in range(350, 557):
        d = abs(x + 0.5 - 453)
        if 78 <= d <= 103:
            P(l, banda(d, -1 if x < 453 else 1), x, x + 1, 482, 662)
    for x0, x1, y1 in ((374, 532, 740), (374, 480, 792), (374, 426, 838)):   # cara de adentro, solo en el vano
        P(l, 'an-piedra-s', x0, x1, 520, y1)
    P(l, 'an-marco', 378, 528, 522, 740)
    P(l, 'an-marco', 378, 476, 740, 792)
    P(l, 'an-marco', 378, 422, 792, 838)
    # Primera fila: seis paños de violetas colgados de la curva del ojo.
    for k, (x0, x1) in enumerate(((381, 400), (404, 426), (430, 451), (455, 476), (480, 502), (506, 525))):
        P(l, 'an-ambar', x0, x1, 530, 588)
        for j, y in enumerate(range(532, 590, 8)):
            violeta(l, (x0 + x1) / 2 + (4 if j % 2 else -4), y, k + j)
    for x0, x1, y0, y1, m in ((381, 420, 596, 690, 'tallos'), (429, 475, 596, 690, 'tallos'),
                              (484, 525, 596, 690, 'ramito'), (381, 420, 697, 737, 'violetas'),
                              (429, 475, 697, 737, 'violetas'), (484, 525, 697, 737, 'hojas'),
                              (381, 420, 745, 788, 'violetas'), (429, 475, 745, 788, 'hojas'),
                              (381, 420, 796, 834, 'hojas')):
        pano(l, x0, x1, y0, y1, m)
    for y0, y1, x0, x1 in ((737, 746, 476, 542), (788, 797, 420, 500), (834, 843, 364, 440)):
        P(l, 'an-piedra', x0, x1, y0, y1 + 3)                      # antepechos en escalón
        P(l, 'an-piedra-c', x0, x1, y0, y0 + 3)
        P(l, 'an-ladrillo-s', x0, x1, y1 + 3, y1 + 10)
    # El ojo: ámbar con varillas que suben y se abren, guirnalda de violetas y el ramo del medio.
    disco(l, 453, 482, 78, lambda dx, dy: 'an-marco')
    disco(l, 456, 485, 74, lambda dx, dy: 'an-ambar-o' if dx < -60 or dy < -60 else None)
    disco(l, 453, 482, 72, lambda dx, dy: ('an-ambar-c' if dx < -20 else 'an-ambar') if dy > -35 else 'an-ambar-o')
    for f in range(fy(430), fy(553)):                              # tallos: del pie del ramo hasta la guirnalda
        t = (553 - py(f)) / 123
        for s in (-1, -0.7, -0.4, -0.15, 0.15, 0.4, 0.7, 1):
            x = 453 + s * 62 * math.sin(t * math.pi / 2) ** 1.3
            if (x - 453) ** 2 + (py(f) - 482) ** 2 < 70 * 70: l.rect('an-tallo', ux(x), ux(x) + 0.25, f, f + 1)
    for rr, a0, a1, n in ((64, 166, 374, 24), (54, 172, 368, 19), (44, 184, 356, 14), (34, 210, 330, 7)):
        for k in range(n):                                         # guirnalda en arco, tupida, que cae a los lados
            a = math.radians(a0 + (a1 - a0) * k / (n - 1))
            violeta(l, 453 + rr * math.cos(a), 482 + rr * math.sin(a), k + rr)
    ramo(l, 453, 506, 20, 3)
    P(l, 'an-hierro', 372, 534, 480, 484)                          # barras de hierro en cruz
    for x in (424, 480):
        disco(l, 453, 482, 74, lambda dx, dy, x=x: 'an-hierro' if abs(dx + 453 - x - 1) < 2 else None)
    for x in (372, 534):
        P(l, 'an-hierro', x - 4, x + 4, 478, 486)

    # Imposta que corta la fachada.
    for x0, x1 in ((FL, 350), (556, FR)):
        P(l, 'an-piedra', x0, x1, 654, 670)
        P(l, 'an-piedra-c', x0, x1, 654, 659)
        P(l, 'an-piedra-s', x0, x1, 666, 670)
        P(l, 'an-ladrillo-s', x0, x1, 670, 678)

    # Planta baja: piedra grande entre la puerta y el ventanal, y alrededor de la ventana del sótano.
    for y0, y1, x0, x1 in ((742, 790, 335, 374), (796, 844, 335, 364), (850, 896, 268, 368), (902, 948, 268, 330),
                           (902, 948, 336, 368), (954, 1000, 268, 368)):
        P(l, 'an-piedra', x0, x1, y0, y1)
        P(l, 'an-piedra-c', x0, x1, y0, y0 + 4)
        P(l, 'an-piedra-s', x1 - 4, x1, y0, y1)
    sillares_der(l, 532, 560, 678, SUELO, 14, 30)
    # Ventana del sótano: tres vidrios oscuros en su marco crema, y la reja de latigazo: barrotes con la punta
    # en llama, dos arcos que nacen abajo en el medio y suben a las esquinas, y el tulipán del centro.
    P(l, 'an-piedra', 368, 540, 882, 898)
    P(l, 'an-piedra-c', 368, 540, 882, 885)
    P(l, 'an-marco', 374, 536, 898, SUELO)
    for x0, x1 in ((380, 428), (434, 482), (488, 530)):
        P(l, 'an-vidrio-o', x0, x1, 904, SUELO - 4)
        P(l, 'an-vidrio-or', x0, x0 + 8, 904, SUELO - 4)            # reflejo
    BC = 457
    for x in list(range(386, 446, 12)) + [BC] + list(range(468, 530, 12)):   # barrotes
        P(l, 'an-reja', x - 1, x + 1, 914, 996)
        for f in range(fy(898), fy(914)):                          # punta en llama: ese hacia arriba
            t = (py(f) - 898) / 16
            dx = 3 * math.sin(t * math.pi * 1.5)
            l.rect('an-reja', ux(x + dx) - 0.25, ux(x + dx) + 0.25, f, f + 1)
    P(l, 'an-reja', 378, 534, 912, 915)
    P(l, 'an-reja', 378, 534, 993, 997)
    for x in range(round(BC - 76), round(BC + 77)):               # el paraguas: dos arcos que bajan del centro
        d = abs(x - BC) / 76
        y = 916 + 50 * (1 - math.sqrt(max(0, 1 - d * d)))
        P(l, 'an-reja', x, x + 1, y, y + 3)
    for f in range(fy(916), fy(985)):                              # tulipán: varas que suben y se abren arriba
        t = (985 - py(f)) / 69
        for s in (-1, -0.45, 0.45, 1):
            x = BC + s * 20 * t ** 2
            l.rect('an-reja', ux(x) - 0.25, ux(x) + 0.25, f, f + 1)
    disco(l, BC, 986, 7, lambda dx, dy: 'an-reja' if dx * dx + dy * dy > 12 else None)

    # Puerta: arco de herradura de dovelas con su moldura. Adentro, toda de madera: la hoja de la izquierda
    # (vidrio de arriba con flores, travesaño, dos vidrios que terminan en la curva grande y, debajo de la
    # curva, tres tableros altos) y el ojo de la derecha (vidrio de arriba, travesaño, dos vidrios chicos).
    # Medida sobre ed54mo75tk7e1.jpg.
    CX, CY, R = 233, 801, 82                                        # el hueco
    OY, OR = 784, 102                                               # el contorno de afuera
    P(l, 'an-piedra', 130, 335, OY, SUELO)
    def dovelas(dx, dy):
        d = math.hypot(dx, dy + CY - OY)
        a = (-dx - dy) / (math.hypot(dx, dy) or 1)
        if d > OR - 4: return 'an-piedra-c' if a > -0.3 else 'an-piedra-s'      # moldura de afuera
        if d > OR - 8: return 'an-piedra-s' if a > -0.3 else 'an-piedra'        # su ranura
        ang = math.degrees(math.atan2(dy, dx)) % 360
        if ang % 20 < 1.8: return 'an-piedra-s'                                   # juntas de las dovelas
        return 'an-piedra-c' if a > 0.6 else 'an-piedra'
    disco(l, CX, OY, OR, lambda dx, dy: dovelas(dx, dy + OY - CY))
    for y in (842, 900, 956):                                       # juntas de las piedras de la jamba
        P(l, 'an-piedra-s', 130, 153, y, y + 3)
    P(l, 'an-piedra-c', 130, 134, OY, SUELO)
    def hueco(x, y, r=R):
        # El hueco: el círculo y, a la izquierda del eje, recto hasta el piso.
        return (x - CX) ** 2 + (y - CY) ** 2 <= r * r or (y >= CY and CX - r <= x < CX)
    def en_circ(x, y, r): return (x - CX) ** 2 + (y - CY) ** 2 <= r * r
    celdas(l, 140, 330, 715, 990, lambda x, y: 'an-piedra-s' if hueco(x, y) else None)        # cara de adentro
    celdas(l, 140, 330, 715, 990, lambda x, y: 'an-puerta-o' if hueco(x, y, R - 3) else None)  # canto del marco
    celdas(l, 140, 330, 715, 990, lambda x, y: 'an-puerta' if hueco(x, y, R - 6) else None)
    # Vidrios de arriba: oscuros de día, flores en la curva y varillas claras en abanico.
    def fan(x, y): return en_circ(x, y, R - 12) and y < 790
    celdas(l, 160, 232, 720, 790, lambda x, y: 'an-vidrio-d' if fan(x, y) else None)
    celdas(l, 270, 312, 720, 790, lambda x, y: 'an-vidrio-d' if fan(x, y) else None)
    for f in range(fy(722), fy(790)):                               # varillas en abanico desde el pie de la
        t = (790 - py(f)) / 68                                       # columna: en la hoja suben hacia la izquierda,
        for x0, d, s in ((232, -1, (0.25, 0.5, 0.75, 1.0)), (268, 1, (0.35, 0.8))):   # en el ojo hacia la derecha
            t2 = (790 - py(f) - 1 / S) / 68                          # la fila de abajo: se une sin cortes
            for k in s:
                xa = x0 + d * 75 * k * math.sin(t * math.pi / 2) ** 1.4
                xb = x0 + d * 75 * k * math.sin(max(0, t2) * math.pi / 2) ** 1.4
                for x in (xa, xb):
                    if not fan(x, py(f)): break
                else:
                    l.rect('an-tallo-d', ux(min(xa, xb)), max(ux(max(xa, xb)), ux(min(xa, xb)) + 0.25), f, f + 1)
    for k, (x, y) in enumerate(((186, 742), (199, 733), (212, 731), (224, 733), (192, 755), (217, 748),
                                (283, 740), (296, 752))):
        violeta(l, x, y, k)
    for x0, x1 in ((156, 236), (266, 316)):                          # travesaños
        celdas(l, x0, x1, 790, 803, lambda x, y: ('an-puerta-c' if y < 793 else 'an-puerta') if hueco(x, y, R - 3) else None)
    # Vidrios de abajo: terminan contra la curva grande (radio 66). Hoja: oscuro y hojas verdes; ojo: igual.
    def bajo(x, y): return y >= 806 and en_circ(x, y, R - 16)
    def redondeado(x, y, x0, x1, r=10):
        # Esquinas de arriba curvas en cada ventanita.
        for cx in (x0 + r, x1 - r):
            if (x < x0 + r if cx == x0 + r else x > x1 - r) and y < 806 + r:
                return (x - cx) ** 2 + (y - 806 - r) ** 2 <= r * r
        return True
    for x0, x1, c in ((166, 193, 'an-vidrio-d'), (198, 230, 'an-hoja-v'), (270, 284, 'an-hoja-v'), (288, 304, 'an-vidrio-d')):
        celdas(l, x0, x1, 806, 880, lambda x, y, c=c, x0=x0, x1=x1: c if bajo(x, y) and redondeado(x, y, x0, x1) else None)
    for f in range(fy(808), fy(876)):                                # hojas en diagonal
        k = f - fy(808)
        for x0, x1 in ((198, 230), (270, 284)):
            x = x1 - 4 - (k * 2.5) % (x1 - x0 - 4)                  # bajan hacia la izquierda
            if bajo(x, py(f)) and redondeado(x, py(f), x0, x1): l.rect('an-hoja-vc', ux(x), ux(x) + 0.75, f, f + 1)
    # La curva grande: un canto con luz arriba y la sombra abajo, en la hoja y en el ojo.
    celdas(l, 150, 316, 806, 890, lambda x, y: ('an-puerta-c' if math.hypot(x - CX, y - CY) < R - 13
           else 'an-puerta-o' if math.hypot(x - CX, y - CY) > R - 9 else None)
           if hueco(x, y, R - 6) and R - 16 < math.hypot(x - CX, y - CY) <= R - 6 and y > 806 else None)
    # Tableros: debajo de la curva, tres altos con su moldura fina (canto oscuro) y el centro con luz.
    for x0, x1 in ((159, 180), (185, 206), (211, 231)):
        celdas(l, x0, x1, 820, 984, lambda x, y: ('an-puerta-o' if x < x0 + 2 or x > x1 - 2 or
               not hueco(x, y - 5, R - 6) or en_circ(x, y - 5, R - 6) else 'an-puerta-c' if x < x0 + 6 else 'an-puerta')
               if y > CY and not en_circ(x, y, R - 4) else None)
        P(l, 'an-puerta-o', x0, x1, 980, 984)
    P(l, 'an-puerta-c', 153, 157, 805, 990)
    P(l, 'an-hierro', 191, 194, 884, 902)                             # tirador
    for y0, y1 in ((806, 836), (962, 990)):                           # bisagras con rulo
        P(l, 'an-hierro', 154, 158, y0, y1)
        P(l, 'an-hierro', 154, 172, y0 + 4, y0 + 7)
        P(l, 'an-hierro', 169, 173, y0 + 7, y0 + 13)
    P(l, 'an-piedra', 146, 246, 990, 996)                             # dos escalones
    P(l, 'an-piedra-c', 146, 246, 990, 992)
    P(l, 'an-piedra', 140, 252, 996, SUELO)
    P(l, 'an-piedra-c', 140, 252, 996, 997)
    # Columnita: fuste, capitel que sostiene el arco, y la gárgola curva hacia la derecha.
    P(l, 'an-piedra', 237, 263, 716, 866)
    P(l, 'an-piedra-c', 237, 241, 716, 866)
    P(l, 'an-piedra-s', 258, 263, 716, 866)
    P(l, 'an-piedra-s', 263, 266, 730, 866)                           # su sombra en la madera
    P(l, 'an-piedra', 233, 266, 714, 730)
    P(l, 'an-piedra-c', 233, 266, 714, 717)
    P(l, 'an-piedra-s', 236, 263, 727, 730)
    for f in range(fy(860), fy(894)):
        t = (py(f) - 860) / 34
        x0 = 233 + 4 * t
        x1 = 262 + 18 * math.sin(min(1, t * 1.15) * math.pi / 2) - (8 * (t - 0.75) / 0.25 if t > 0.75 else 0)
        l.rect('an-piedra-c' if t < 0.45 else 'an-piedra', ux(x0), ux(x1), f, f + 1)
        l.rect('an-piedra-s', ux(x1) - 0.5, ux(x1), f, f + 1)
    P(l, 'an-piedra-ss', 238, 276, 894, 899)
    P(l, 'an-hierro', 247, 252, 846, 856)                             # el número

    # Vereda de baldosas y cordón.
    P(l, 'an-vereda', X0, X1, SUELO, Y1)
    P(l, 'an-vereda-s', X0, X1, SUELO, SUELO + 5)
    for f in range(fy(SUELO) + 1, FILAS - 2):
        if (f - fy(SUELO)) % 3 == 0: l.rect('an-vereda-j', 0, LARGO, f, f + 1)
        else:
            x = ((f - fy(SUELO)) // 3 % 2) * 2.5
            while x < LARGO:
                l.rect('an-vereda-j', x, x + 0.25, f, f + 1)
                x += 5
    P(l, 'an-cordon', X0, X1, Y1 - 9, Y1)
    P(l, 'an-cordon-c', X0, X1, Y1 - 9, Y1 - 6)

    return {'nota': 'El taller Sterner en Ixelles (Bruselas), de Ernest Delune: casa angosta '
                    'de ladrillo claro y piedra, con el mirador de madera, el gran vitral redondo de violetas '
                    'sobre el ventanal en escalones, la puerta en arco de herradura con su columnita y el ojo '
                    'redondo, la gárgola y las rejas de latigazo.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

SOMBREABLES = ('an-bloque', 'an-ladrillo', 'an-junta', 'an-piedra', 'an-madera', 'an-vidrio', 'an-cristal', 'an-marco',
               'an-vecino', 'an-blanco', 'an-vereda')
COLORES = {
    'an-ladrillo': ('#c4b48e', '#ae9f7d'), 'an-junta': ('#d8ccb2', '#c1b69e'),
    'an-piedra': ('#dacdb0', '#c4b89c'), 'an-piedra-c': ('#e9dfc7', '#d3c9b2'),
    'an-madera': ('#d3c29c', '#bdae8b'), 'an-madera-c': ('#e4d7b8', '#cfc3a5'),
    'an-vidrio': ('#a9bccb', '#8a9cab'), 'an-vidrio-c': ('#cbd8e2', '#a9b6c1'), 'an-vidrio-o': ('#2d2a28', '#262422'), 'an-vidrio-or': ('#4a4743', '#3e3b38'),
    'an-interior': ('#e3e0d8', '#c4c1ba'), 'an-interior-o': ('#4c4a47', '#403e3b'), 'an-bloque': ('#c9d3d6', '#a9b2b5'), 'an-bloque-j': ('#e8ecec', '#c9cdcd'),
    'an-cristal': ('#8f937f', '#7c806e'), 'an-cristal-c': ('#b4b8a6', '#9da190'), 'an-cortina': ('#dfe8ef', '#bec7ce'),
    'an-cortina-o': ('#5c4a3e', '#4f4036'),
    'an-marco': ('#dccfae', '#c6ba9c'), 'an-marco-c': ('#f3ecd8', '#ddd6c2'), 'an-marco-p': ('#8a5a2b', '#7a4f25'),
    'an-ambar': ('#ad8f3e', '#9c8137'), 'an-ambar-c': ('#c0a24c', '#ad9244'), 'an-ambar-o': ('#7f7650', '#726a48'),
    'an-tallo': ('#bcc8cc', '#aab5b9'),
    'an-violeta': ('#4a4078', '#433a6d'), 'an-lila': ('#6c5a92', '#625285'), 'an-purpura': ('#7a2f58', '#6e2a4f'),
    'an-azul': ('#3f5288', '#394a7b'), 'an-violeta-o': ('#2f2a4a', '#2a2643'), 'an-azul-o': ('#29365a', '#253151'),
    'an-oro': ('#c7b866', '#b5a75d'),
    'an-turquesa': ('#3f9a98', '#398b89'), 'an-turquesa-c': ('#86c9c0', '#79b5ad'), 'an-turquesa-o': ('#25566a', '#214d5f'),
    'an-hierro': ('#2c3550', '#28304a'), 'an-reja': ('#a9d6c6', '#97c2b3'),
    'an-puerta-l': ('#a3652a', '#925a25'), 'an-vidrio-d': ('#4a4a3e', '#403f36'),
    'an-vidrio-dc': ('#5c5b4c', '#504f42'), 'an-tallo-d': ('#9a9a82', '#8a8a74'),
    'an-hoja-v': ('#2f5a3a', '#2a5034'), 'an-hoja-vc': ('#6fa35c', '#649452'),
    'an-puerta': ('#b8742f', '#a6692b'), 'an-puerta-c': ('#d39250', '#bf8448'), 'an-puerta-o': ('#7d4a1c', '#6e4119'),
    'an-pizarra': ('#5e646d', '#50565e'), 'an-pizarra-o': ('#454a52', '#3a3f46'),
    'an-cornisa': ('#2c3036', '#26292e'), 'an-cornisa-c': ('#4a5059', '#40454d'),
    'an-vecino': ('#a5523f', '#8f4737'), 'an-vecino-j': ('#c99a86', '#ad8574'), 'an-vecino-f': ('#cdbfa8', '#b3a692'),
    'an-blanco': ('#ebe9e3', '#cfcdc8'), 'an-blanco-c': ('#f7f6f2', '#dddcd8'),
    'an-cano': ('#5d7085', '#4f6072'), 'an-cano-c': ('#7f93a8', '#6d7f91'),
    'an-farol': ('#2f4b3c', '#2a4436'), 'an-farol-c': ('#4d6f5c', '#456453'),
    'an-globo': ('#f2efe6', '#e6e2d6'), 'an-globo-c': ('#ffffff', '#f4f2ec'), 'an-globo-s': ('#cfcabd', '#bdb8ab'),
    'an-vereda': ('#a49e94', '#8a857c'), 'an-vereda-j': ('#8b857b', '#736e66'),
    'an-cordon': ('#8d8a84', '#77746f'), 'an-cordon-c': ('#b8b5ae', '#9d9a94'),
    'nouveau-fondo': ('#efe6d2', '#2b2722'), 'nouveau-fondo-marco': ('#2b2722', '#efe6d2'),
}
con_sombras(COLORES, SOMBREABLES)
con_sombras(COLORES, ('an-piedra-s', 'an-madera-s'), 0.85, 's')        # an-piedra-ss / an-madera-ss: más hondo

if __name__ == '__main__':
    p = version()
    p.update(placa='nouveau-fondo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
             marco='nouveau-fondo-marco')
    guardar(sys.argv[1], 'estilos', 'Art nouveau', p, COLORES, 'an-|nouveau-')
    print(len(p['lineas']), 'líneas, largo', p['largo'])
