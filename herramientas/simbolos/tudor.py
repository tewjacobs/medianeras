# Casa natal de Shakespeare (Stratford-upon-Avon), el frente del jardín, de frente.
# Medida en px sobre referencias/simbolos/tudor/6778-0090…jpg, recortada de x 900 a 1500 e y 50 a 650
# y agrandada a 800 × 800 (tudor-centro). Eje del hastial en x 375; el dibujo va de x -185 a 935
# (las dos alas iguales y largas, como la casa en las otras fotos) y de y 100 (punta de la chimenea) a 800 (el sendero).
# Hastial de entramado de roble gris con relleno ocre: pendolón, jabalcones, collar, viga de atado,
# piso alto volado sobre la viga gruesa; ventana saliente (oriel) con techito de tejas, vidrios
# emplomados en rombos y ménsula; puerta de tablas con su alerito; alas a los lados con techo de tejas
# viejas; chimenea de piedra a la izquierda y otra atrás del hastial. Abajo, el escalón de piedra,
# el banco, las macetas en sus pilares, las malvas rosas y el sendero de lajas.
# Uso: tudor.py <simbolos.json> (pone estilos."Tudor").
import sys
from armar import Lienzo, guardar

S = 0.14                                   # unidades por px
X0, X1, Y0, Y1 = -185, 935, 100, 800
A = 375                                    # eje del hastial
LARGO = round((X1 - X0) * S)
FILAS = round((Y1 - Y0) * S)

def q(x): return round(x * 4) / 4
def ux(px): return q((px - X0) * S)
def fy(py): return round((py - Y0) * S)

def P(l, c, x0, x1, y0, y1):
    # Rectángulo en px de la foto.
    l.rect(c, ux(x0), ux(x1), fy(y0), max(fy(y0) + 1, fy(y1)))

def M(l, c, x0, x1, y0, y1):
    # Rectángulo y su espejo respecto del eje del hastial.
    P(l, c, x0, x1, y0, y1)
    P(l, c, 2 * A - x1, 2 * A - x0, y0, y1)

def diagonal(l, c, xa, ya, xb, yb, ancho, espejo=True):
    # Jabalcón de (xa, ya) a (xb, yb), de `ancho` px, fila por fila.
    fa, fb = fy(ya), fy(yb)
    for f in range(fa, fb + 1):
        t = (f - fa) / max(1, fb - fa)
        x = q(ux(xa) + (ux(xb) - ux(xa)) * t)                  # en unidades: mismo ancho en cada fila
        w = q(ancho * S)
        l.rect(c, x - w / 2, x + w / 2, f, f + 1)
        if espejo: l.rect(c, 2 * ux(A) - x - w / 2, 2 * ux(A) - x + w / 2, f, f + 1)

def tejas(l, x0, x1, y0, y1, desde=None):
    # Techo de tejas viejas: hiladas de dos filas, juntas corridas media teja por hilada, alguna más oscura.
    P(l, 'tu-teja', x0, x1, y0, y1)
    for f in range(fy(y0), fy(y1)):
        hilada = (f - fy(y0)) // 2
        if (f - fy(y0)) % 2 == 1:                                  # sombra de abajo de cada hilada
            l.rect('tu-teja-o', ux(x0), ux(x1), f, f + 1)
        x = ux(x0) + (hilada % 2) * 1.0
        k = 0
        while x < ux(x1):
            if (f - fy(y0)) % 2 == 0:
                l.rect('tu-teja-o', x, x + 0.25, f, f + 1)         # junta entre tejas
                if (k * 7 + hilada * 3) % 5 == 0:                  # tejas más claras, sueltas
                    l.rect('tu-teja-c', x + 0.25, min(ux(x1), x + 1.75), f, f + 1)
            x += 2
            k += 1

def chimenea(l, x0, x1, y0, y1):
    P(l, 'tu-chimenea', x0, x1, y0, y1)
    for f in range(fy(y0) + 2, fy(y1)):
        if f % 2 == 0: l.rect('tu-chimenea-o', ux(x0), ux(x1), f, f + 1)    # hiladas
        else:
            x = ux(x0) + (f // 2 % 2) * 1.25
            while x < ux(x1) - 0.25:
                l.rect('tu-chimenea-o', x, x + 0.25, f, f + 1)
                x += 2.5
    P(l, 'tu-chimenea-c', x0 - 6, x1 + 6, y0, y0 + 14)                    # coronamiento
    P(l, 'tu-chimenea-o', x0 - 6, x1 + 6, y0 + 14, y0 + 20)
    P(l, 'tu-chimenea-o', x1 - 12, x1, y0 + 20, y1)                       # lado en sombra

def emplomado(l, x0, x1, y0, y1):
    # Vidrio emplomado en rombos: plomo claro en cruz diagonal sobre el vidrio oscuro.
    P(l, 'tu-vidrio', x0, x1, y0, y1)
    a, b = ux(x0), ux(x1)
    for f in range(fy(y0), fy(y1)):
        k = (f - fy(y0)) % 4
        for d in (k * 0.5, 2 - k * 0.5):
            x = a + d
            while x < b:
                l.rect('tu-plomo', x, x + 0.25, f, f + 1)
                x += 2

def version():
    l = Lienzo(LARGO, FILAS)

    # Alas: techo de tejas y la pared de entramado.
    chimenea(l, 165, 255, 100, 175)                             # la de la izquierda sale de la cumbrera
    tejas(l, X0, X1, 160, 410)
    P(l, 'tu-teja-o', X0, X1, 400, 412)                       # borde del alero
    for f in range(fy(160), fy(412)):                          # las puntas del techo a cuatro aguas
        y = Y0 + (f + 0.5) / S
        d = q((410 - y) * 0.28 * S)
        l.rect('-', 0, d, f, f + 1)
        l.rect('-', LARGO - d, LARGO, f, f + 1)
        l.rect('tu-teja-o', d, d + 0.5, f, f + 1)              # limatesa
        l.rect('tu-teja-c', d + 0.5, d + 0.75, f, f + 1)
        l.rect('tu-teja-o', LARGO - d - 0.5, LARGO - d, f, f + 1)
    chimenea(l, 500, 565, 205, 300)                             # la de atrás del hastial
    for x0, x1 in ((X0 + 14, 115), (630, X1 - 14)):
        P(l, 'tu-relleno-s', x0, x1, 412, 728)
        for y0, y1 in ((412, 420), (465, 475), (548, 562), (632, 642), (715, 728)):
            P(l, 'tu-madera', x0, x1, y0, y1)
    M(l, 'tu-madera', X0 + 14, X0 + 30, 412, 728)               # postes de las esquinas, gruesos
    M(l, 'tu-madera-o', X0 + 30, X0 + 34, 412, 728)
    M(l, 'tu-chimenea', X0 + 8, 105, 728, 742)                  # zócalo de piedra de las alas
    M(l, 'tu-chimenea-o', X0 + 8, 105, 738, 742)
    for x in range(65, X0 + 34, -50):                           # pies derechos cada 50 px, simétricos
        M(l, 'tu-madera', x, x + 12, 412, 728)
    M(l, 'tu-madera-o', 104, 115, 412, 728)                    # sombra contra el hastial
    for x0 in (-85, -35):                                       # ventanas emplomadas del piso alto
        M(l, 'tu-madera', x0 - 6, x0 + 106, 474, 542)
        for k in range(4):
            M(l, 'tu-vidrio', x0 + k * 25, x0 + k * 25 + 22, 480, 536)
        M(l, 'tu-madera-c', x0 - 10, x0 + 110, 536, 546)
    for x0 in (-85, -35):
        for k in range(4):                                      # su emplomado
            emplomado(l, x0 + k * 25, x0 + k * 25 + 22, 480, 536)
            emplomado(l, 2 * A - (x0 + k * 25 + 22), 2 * A - (x0 + k * 25), 480, 536)
    for x0 in (-135, 15):                                       # ventanas de la planta baja
        M(l, 'tu-madera', x0 - 6, x0 + 56, 650, 712)
        emplomado(l, x0, x0 + 22, 656, 706)
        emplomado(l, x0 + 28, x0 + 50, 656, 706)
        emplomado(l, 2 * A - x0 - 22, 2 * A - x0, 656, 706)
        emplomado(l, 2 * A - x0 - 50, 2 * A - x0 - 28, 656, 706)

    # Hastial: triángulo de relleno, con el techo y la tabla de borde inclinados.
    ca = ux(A)
    for f in range(fy(110), fy(415)):
        hw = (f - fy(110) + 1) * 0.94                           # escalones parejos de 0.94: sin zigzag
        hw = round(hw * 4) / 4 if (f - fy(110)) % 4 else q(hw)
        # Bandas más anchas que el escalón, así cada diagonal se lee continua.
        l.rect('tu-teja', ca - hw, ca + hw, f, f + 1)           # filo de tejas
        l.rect('tu-madera-c', ca - hw + 1.25, ca + hw - 1.25, f, f + 1)   # tabla de borde, clara
        l.rect('tu-madera-o', ca - hw + 2.75, ca + hw - 2.75, f, f + 1)   # su sombra, un escalón de ancho
        l.rect('tu-relleno', ca - hw + 3.75, ca + hw - 3.75, f, f + 1)
    P(l, 'tu-relleno', 115, 630, 405, 728)
    for x0, x1, y0, y1 in ((130, 205, 562, 632), (218, 290, 642, 712), (305, 345, 562, 632),
                           (130, 205, 475, 540), (305, 400, 475, 540)):
        M(l, 'tu-relleno-s', x0, x1, y0, y0 + 10)                 # sombra bajo cada travesaño

    # Entramado del hastial (todo simétrico).
    P(l, 'tu-madera', A - 10, A + 10, 140, 292)                 # pendolón
    M(l, 'tu-madera', 290, 305, 228, 400)                        # pies derechos
    M(l, 'tu-madera', 200, 214, 325, 400)
    P(l, 'tu-madera', 290, 460, 283, 294)                        # collar
    diagonal(l, 'tu-madera', 224, 318, 292, 384, 13)             # jabalcones
    M(l, 'tu-madera-c', 108, 136, 392, 402)                      # cabeza de la viga, que asoma
    P(l, 'tu-madera', 100, 650, 392, 406)                        # viga de atado
    # Piso alto.
    for x in (115, 205, 290, 530, 615):
        P(l, 'tu-madera', x, x + 15, 406, 548)
    P(l, 'tu-madera', 115, 630, 465, 475)                        # travesaño
    P(l, 'tu-madera', 105, 640, 540, 556)                        # viga del volado
    P(l, 'tu-madera-o', 115, 630, 556, 562)                      # sombra del volado
    M(l, 'tu-madera-o', 140, 152, 412, 465)                      # canto en sombra de algunos paños
    # Planta baja.
    for x in (120, 205, 290, 345, 565, 615):
        P(l, 'tu-madera', x, x + 13, 562, 718)
    P(l, 'tu-madera', 115, 400, 632, 642)                        # travesaño, cortado por la puerta
    P(l, 'tu-madera', 515, 630, 632, 642)
    P(l, 'tu-madera', 110, 640, 712, 728)                        # solera
    P(l, 'tu-chimenea', 105, 645, 728, 742)                      # zócalo de piedra
    P(l, 'tu-chimenea-o', 105, 645, 738, 742)

    # Puerta de tablas con su marco y el alerito.
    P(l, 'tu-madera', 400, 520, 568, 718)
    P(l, 'tu-puerta', 413, 507, 578, 718)
    for x in range(424, 507, 16):
        P(l, 'tu-puerta-o', x, x + 3, 578, 718)                  # juntas de las tablas
    P(l, 'tu-puerta-o', 413, 507, 620, 626)                      # travesaños de atrás
    P(l, 'tu-puerta-o', 413, 507, 676, 682)
    P(l, 'tu-plomo', 488, 496, 640, 650)                         # aldaba
    P(l, 'tu-madera-c', 398, 522, 548, 558)                      # alerito
    P(l, 'tu-madera-o', 404, 516, 558, 568)

    # Oriel: techito de tejas a cuatro aguas, ventana de tres luces, ménsula.
    for f in range(fy(288), fy(350)):
        y = Y0 + (f + 0.5) / S
        k = f - fy(288)
        hw = q(50 * S) + k * 0.75
        c = ux(A + 5)
        l.rect('tu-teja', c - hw, c + hw, f, f + 1)
        if k % 2 == 1: l.rect('tu-teja-o', c - hw + 0.5, c + hw - 0.5, f, f + 1)
        l.rect('tu-teja-o', c - hw, c - hw + 0.25, f, f + 1)   # limatesas
        l.rect('tu-teja-o', c + hw - 0.25, c + hw, f, f + 1)
    l.rect('tu-teja-o', ux(A + 5) - q(50 * S) - 6.25, ux(A + 5) + q(50 * S) + 6.25, fy(350), fy(350) + 1)
    P(l, 'tu-madera', 298, 462, 352, 470)                        # bastidor
    for x0 in (312, 362, 412):
        emplomado(l, x0, x0 + 38, 360, 460)
    P(l, 'tu-madera-c', 292, 468, 460, 472)                      # alféizar
    for f in range(fy(472), fy(505)):                            # ménsula que se angosta
        y = Y0 + (f + 0.5) / S
        hw = 78 - (y - 472) * 0.9
        l.rect('tu-madera-o', ux(A + 5 - hw), ux(A + 5 + hw), f, f + 1)
        l.rect('tu-madera', ux(A + 5 - hw + 4), ux(A + 5 + hw - 4), f, f + 1)


    # Escalón, sendero, banco, macetas.
    P(l, 'tu-piedra', 250, 500, 742, 770)
    P(l, 'tu-piedra-o', 250, 500, 754, 758)
    P(l, 'tu-piedra', X0, X1, 770, 800)
    for x in range(260, 500, 46):
        P(l, 'tu-piedra-o', x, x + 3, 770, 800)
    P(l, 'tu-piedra-o', 230, 520, 784, 788)
    # Banco de listones adelante de la puerta.
    P(l, 'tu-banco', 408, 522, 690, 696)
    for x in range(412, 520, 10):
        P(l, 'tu-banco', x, x + 5, 696, 735)
    P(l, 'tu-banco-o', 408, 522, 735, 744)
    P(l, 'tu-banco', 408, 418, 744, 770)
    P(l, 'tu-banco', 512, 522, 744, 770)
    for x0 in (228, 532):                                        # pilares de piedra con macetas
        P(l, 'tu-chimenea', x0, x0 + 52, 742, 800)
        P(l, 'tu-chimenea-o', x0 + 40, x0 + 52, 742, 800)
        P(l, 'tu-maceta', x0 + 2, x0 + 50, 698, 742)
        P(l, 'tu-oro', x0 + 18, x0 + 34, 712, 726)               # sello dorado
        for k, dx in enumerate(range(x0 - 6, x0 + 58, 9)):       # pasto ornamental
            P(l, 'tu-pasto' if k % 2 else 'tu-pasto-c', dx, dx + 4, 640 + (k % 3) * 14, 698)

    # Malvas rosas a los lados (varas altas, con flores rosas), y follaje abajo.
    for x0, x1 in ((X0, 228), (582, X1)):
        P(l, 'tu-hoja', x0, x1, 700, 770)
        for f in range(fy(700), fy(770)):
            x = ux(x0) + ((f * 3) % 4) * 0.5
            while x < ux(x1):
                l.rect('tu-hoja-o' if f % 2 else 'tu-hoja-c', x, x + 0.5, f, f + 1)
                x += 2.25
    izq = [(-175, 520, 0), (-130, 450, 1), (-80, 560, 0), (-35, 490, 1), (10, 530, 0), (55, 600, 1),
           (100, 505, 0), (145, 590, 1), (190, 560, 0)]
    varas = izq + [(2 * A - x - 6, tope - 40, 1 - lado) for x, tope, lado in izq]
    def flor(c, x, y, rr):
        # Flor redonda: tres filas, la del medio más ancha, con el ojo oscuro.
        P(l, c, x - rr * 0.6, x + rr * 0.6, y - 8, y)
        P(l, c, x - rr, x + rr, y, y + 8)
        P(l, c, x - rr * 0.6, x + rr * 0.6, y + 8, y + 15)
        P(l, 'tu-flor-o', x - 3, x + 3, y, y + 8)
    for i, (x, tope, lado) in enumerate(varas):
        P(l, 'tu-hoja-o', x, x + 6, tope, 700)
        for k, y in enumerate(range(tope, 690, 24)):
            s = 1 if (k + lado) % 2 else -1
            if y < tope + 40:                                    # pimpollos verdes arriba
                P(l, 'tu-hoja-c', x - 4 + s * 6, x + 10 + s * 6, y, y + 10)
                continue
            c = ('tu-flor', 'tu-flor-c', 'tu-flor', 'tu-flor-r')[(i + k // 2) % 4]
            flor(c, x + 3 + s * 12, y, 10 + (k % 3) * 2)
            P(l, 'tu-hoja', x + 3 - s * 18, x + 3 - s * 2, y + 14, y + 22)   # hoja del otro lado
    return {'nota': 'La casa natal de Shakespeare en Stratford-upon-Avon, desde el jardín: el hastial de '
                    'entramado de roble con relleno ocre, la ventana saliente con vidrios emplomados, la puerta '
                    'de tablas, techos de tejas viejas, la chimenea de piedra y las malvas rosas del jardín.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

COLORES = {
    'tu-madera': ('#7a7064', '#7a7064'), 'tu-madera-o': ('#4d463e', '#4d463e'), 'tu-madera-c': ('#a1978a', '#a1978a'),
    'tu-relleno': ('#cfae80', '#cfae80'), 'tu-relleno-s': ('#b8966a', '#b8966a'),
    'tu-teja': ('#8c4a35', '#8c4a35'), 'tu-teja-o': ('#6a3526', '#6a3526'), 'tu-teja-c': ('#a8644a', '#a8644a'),
    'tu-chimenea': ('#aaa08c', '#aaa08c'), 'tu-chimenea-o': ('#837a68', '#837a68'), 'tu-chimenea-c': ('#c4bba7', '#c4bba7'),
    'tu-vidrio': ('#2a2c31', '#2a2c31'), 'tu-plomo': ('#9a968e', '#9a968e'),
    'tu-puerta': ('#735d45', '#735d45'), 'tu-puerta-o': ('#4f3f2f', '#4f3f2f'),
    'tu-piedra': ('#c9c0ad', '#8f897c'), 'tu-piedra-o': ('#a39a87', '#6c675d'),
    'tu-banco': ('#a68e6e', '#a68e6e'), 'tu-banco-o': ('#6f5e48', '#6f5e48'),
    'tu-maceta': ('#2e2e2b', '#2e2e2b'), 'tu-oro': ('#b9975a', '#b9975a'),
    'tu-pasto': ('#b9a46a', '#b9a46a'), 'tu-pasto-c': ('#d8c895', '#d8c895'),
    'tu-hoja': ('#4e6a3a', '#4e6a3a'), 'tu-hoja-o': ('#344829', '#344829'), 'tu-hoja-c': ('#7f9757', '#7f9757'),
    'tu-flor': ('#d97ca4', '#d97ca4'), 'tu-flor-c': ('#f1bcd2', '#f1bcd2'), 'tu-flor-r': ('#c43a52', '#c43a52'), 'tu-flor-o': ('#8a2a45', '#8a2a45'),
    'tudor-fondo': ('#e6dcc4', '#3b362c'),
}

p = version()
p.update(placa='tudor-fondo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10)
guardar(sys.argv[1], 'estilos', 'Tudor', p, COLORES, 'tu-|tudor-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
