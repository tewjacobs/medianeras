# Chalet californiano de Ciudad Evita (La Matanza), de frente.
# Medida en px sobre referencias/simbolos/chalet californiano/Screenshot 2026-11-15 at 12.43.44.png,
# reducida a 1400 × 875, recortada de x 260 a 1010 e y 330 a 570 y agrandada al doble (1500 × 480).
# A la izquierda el ala baja con techo a cuatro aguas de tejas coloniales, la pared blanca con la ventana
# de reja ornamental y el pilar de piedra; la galería con la pared terracota, la ventana enrejada y la
# puerta de madera; dos chimeneas con su sombrerete. A la derecha el hastial a dos aguas, poco empinado,
# con el borde de tejas, la ventana en arco de persiana sobre el revoque blanco que baja en diagonal (la
# escalera de adentro), la piedra laja, el farol negro, la puerta baja en arco y el ala del costado con su
# ventanita en arco. Delante, el jardín: pastos, el arbusto redondo, el buzón, el formio y los adoquines.
# Sombreado con luz arriba a la izquierda: sombra debajo de los aleros, adentro de la galería y de cada
# hueco (arriba y a la izquierda), caras de la derecha más oscuras.
# Uso: chalet.py <simbolos.json> (pone estilos."Chalet californiano").
import sys, math
from armar import Lienzo, guardar, con_sombras

S = 0.16                                   # unidades por px
X0, X1, Y0, Y1 = 40, 1484, 28, 488
SUELO = 405
LARGO = round((X1 - X0) * S)
FILAS = round((Y1 - Y0) * S)
EJE = 1050                                 # eje del hastial
PEND = 0.31                                # pendiente del hastial

def q(x): return round(x * 4) / 4
def ux(px): return q((px - X0) * S)
def fy(py): return round((py - Y0) * S)
def py(f): return Y0 + (f + 0.5) / S
def px(i): return X0 + (i + 0.5) / 4 / S

def P(l, c, x0, x1, y0, y1):
    l.rect(c, ux(x0), ux(x1), fy(y0), max(fy(y0) + 1, fy(y1)))

def celdas(l, x0, x1, y0, y1, color):
    for f in range(max(0, fy(y0)), min(FILAS, fy(y1))):
        for i in range(max(0, round(ux(x0) * 4)), min(l.n, round(ux(x1) * 4))):
            c = color(px(i), py(f))
            if c: l.c[f][i] = c

def arco(l, x0, x1, y0, y1, color):
    # Hueco con remate de medio punto: color(x, y) dentro.
    r = (x1 - x0) / 2
    cx, cy = (x0 + x1) / 2, y0 + r
    celdas(l, x0, x1, y0, y1, lambda x, y: color(x, y) if y >= cy or (x - cx) ** 2 + (y - cy) ** 2 <= r * r else None)

def tejas(l, x0, x1, y0, y1, borde=None):
    # Tejas coloniales vistas de frente: canales verticales (cobija clara y canal oscuro) y las hiladas
    # corridas media teja; algunas tejas más viejas. `borde(y)` da los límites (izq, der) en px por fila.
    for f in range(fy(y0), fy(y1)):
        y = py(f)
        a, b = borde(y) if borde else (x0, x1)
        if b <= a: continue
        k = f - fy(y0)
        l.rect('ce-teja', ux(a), ux(b), f, f + 1)
        x = ux(x0) + (k // 3 % 2) * 0.75
        n = 0
        while x < ux(b):
            if x >= ux(a):
                l.rect('ce-teja-c', x, min(ux(b), x + 0.5), f, f + 1)            # lomo con luz
                l.rect('ce-teja-s', min(ux(b), x + 1), min(ux(b), x + 1.5), f, f + 1)  # canal en sombra
                if (n * 5 + k // 3 * 3) % 11 == 0:
                    l.rect('ce-teja-v', x, min(ux(b), x + 1), f, f + 1)            # teja vieja, grisácea
            x += 1.5
            n += 1
        if k % 3 == 2: l.rect('ce-teja-s', ux(a), ux(b), f, f + 1)              # sombra de cada hilada

def piedra(l, x0, x1, y0, y1):
    # Piedra laja: hiladas de dos o tres filas, piedras de largo desparejo y cuatro tonos; la junta abajo de
    # cada hilada (en sombra) y a veces cortada por una piedra más alta; el canto de arriba de cada una con luz.
    P(l, 'ce-piedra', x0, x1, y0, y1)
    f, h = fy(y0), 0
    while f < fy(y1):
        alto = (2, 3, 2, 2, 3)[h % 5]
        x, n = ux(x0) - ((h * 7) % 5) * 0.75, 0
        while x < ux(x1):
            w = (4.5, 6, 3.5, 7, 5, 3)[(n * 5 + h * 3) % 6]
            c = ('ce-piedra', 'ce-piedra-c', 'ce-piedra-o', 'ce-piedra', 'ce-piedra-r')[(n * 3 + h * 2) % 5]
            a, b = max(ux(x0), x + 0.25), min(ux(x1), x + w)
            if b > a:
                l.rect(c, a, b, f, min(f + alto - 1, fy(y1)))
                l.rect('ce-piedra-c', a, min(b, a + w * 0.6), f, f + 1) if c != 'ce-piedra-c' else None
                l.rect('ce-junta', max(ux(x0), x), max(ux(x0), x) + 0.25, f, min(f + alto - 1, fy(y1)))
            x += w
            n += 1
        if f + alto - 1 < fy(y1):
            l.rect('ce-junta', ux(x0), ux(x1), f + alto - 1, f + alto)
        f += alto
        h += 1

def persiana(l, x0, x1, y0, y1):
    # Persiana en arco: tablillas horizontales, marco y la sombra del hueco arriba a la izquierda.
    arco(l, x0 - 10, x1 + 10, y0 - 10, y1, lambda x, y: 'ce-blanco-c' if x < (x0 + x1) / 2 else 'ce-blanco-s')
    arco(l, x0 - 6, x1 + 6, y0 - 6, y1, lambda x, y: 'ce-marco')
    arco(l, x0, x1, y0, y1, lambda x, y: 'ce-tablilla' if fy(y) % 2 else 'ce-tablilla-o')
    arco(l, x0, x1, y0, y0 + 14, lambda x, y: 'ce-tablilla-s')
    P(l, 'ce-marco-s', x0, x0 + 6, y0 + (x1 - x0) / 2, y1)
    P(l, 'ce-marco', (x0 + x1) / 2 - 3, (x0 + x1) / 2 + 3, y0 + 4, y1)             # junta de las dos hojas

def version():
    l = Lienzo(LARGO, FILAS)

    # Techo principal a cuatro aguas, con el limatesa a la izquierda y dos chimeneas.
    for x, w, top in ((480, 34, 44), (585, 40, 38)):
        P(l, 'ce-ladrillo', x - w / 2, x + w / 2, top + 14, 84)
        P(l, 'ce-ladrillo-s', x + w / 2 - 8, x + w / 2, top + 14, 84)
        P(l, 'ce-teja', x - w / 2 - 6, x + w / 2 + 6, top, top + 10)              # sombrerete de tejas
        P(l, 'ce-teja-c', x - w / 2 - 6, x, top, top + 4)
        P(l, 'ce-teja-s', x - w / 2 - 6, x + w / 2 + 6, top + 10, top + 14)
        P(l, 'ce-ladrillo-s', x - 6, x + 6, top + 14, top + 22)
    def borde(y):
        t = (y - 78) / (205 - 78)
        return 230 - 180 * t, 1000                                             # sigue abajo del hastial
    tejas(l, 50, 1000, 78, 207, borde)
    for f in range(fy(78), fy(207)):
        a = 230 - 180 * (py(f) - 78) / 127
        l.rect('ce-teja-c', ux(a), ux(a) + 1, f, f + 1)                             # limatesa con luz
        l.rect('ce-teja-s', ux(a) + 1, ux(a) + 1.5, f, f + 1)
    P(l, 'ce-teja-c', 230, 1000, 74, 80)                                           # cumbrera
    P(l, 'ce-teja-s', 230, 1000, 80, 83)
    P(l, 'ce-teja-s', 50, 800, 200, 207)                                           # bocas de las tejas
    for x in range(52, 800, 13):
        P(l, 'ce-teja', x, x + 8, 200, 207)
    P(l, 'ce-blanco', 50, 800, 207, 214)                                           # tabla del alero
    P(l, 'ce-blanco-s', 50, 800, 214, 220)

    # Ala izquierda: piedra de la esquina, pared blanca, ventana con reja ornamental.
    P(l, 'ce-blanco', 66, 432, 218, SUELO)                                         # revoque blanco, sin piedra
    P(l, 'ce-blanco-c', 66, 72, 218, SUELO)                                        # esquina con luz
    P(l, 'ce-blanco-s', 66, 432, 218, 230)                                         # sombra del alero
    P(l, 'ce-vidrio', 214, 388, 242, 374)                                         # vidrio parejo, sin sombras
    for k in range(7):                                                             # reja: 6 × 5 cuadros iguales,
        x = 214 + k * 29                                                           # cada uno con su aro
        P(l, 'ce-reja', x - 2, x + 2, 242, 374)
    for k in range(6):
        y = 242 + k * 26.4
        P(l, 'ce-reja', 212, 390, y - 1.5, y + 1.5)
    celdas(l, 214, 388, 242, 374, lambda x, y: 'ce-reja'
           if 6 <= math.hypot((x - 214) % 29 - 14.5, (y - 242) % 26.4 - 13.2) <= 9 else None)
    P(l, 'ce-marco', 208, 214, 236, 380)                                           # marco
    P(l, 'ce-marco', 392, 398, 236, 380)
    P(l, 'ce-marco', 208, 398, 236, 242)
    P(l, 'ce-blanco-s', 214, 392, 242, 246)
    P(l, 'ce-blanco-c', 204, 398, 374, 382)                                        # alféizar
    P(l, 'ce-blanco-s', 208, 394, 382, 388)

    # Pilar de piedra y la galería en sombra.
    P(l, 'ce-galeria', 480, 800, 218, 362)
    P(l, 'ce-terracota', 486, 536, 226, 362)
    piedra(l, 536, 800, 226, 362)
    P(l, 'ce-marco', 540, 680, 222, 326)                                           # ventana con reja
    P(l, 'ce-vidrio', 546, 674, 228, 320)
    P(l, 'ce-vidrio-c', 546, 560, 228, 320)
    P(l, 'ce-cortina', 612, 674, 228, 320)
    P(l, 'ce-marco', 607, 612, 228, 320)                                           # las dos hojas
    for x in range(550, 675, 14):                                                  # reja con puntas
        P(l, 'ce-reja', x, x + 3, 232, 320)
        P(l, 'ce-reja', x - 1, x + 4, 236, 240)
    for y in (262, 298):
        P(l, 'ce-reja', 546, 674, y, y + 3)
    P(l, 'ce-blanco-c', 534, 686, 326, 332)                                        # alféizar
    P(l, 'ce-marco', 708, 782, 220, 362)                                           # puerta de madera
    P(l, 'ce-puerta', 714, 776, 226, 362)
    P(l, 'ce-marco', 714, 776, 226, 230)
    for x0, x1 in ((720, 742), (748, 770)):                                        # cuatro tableros en relieve
        for y0, y1 in ((236, 290), (298, 354)):
            P(l, 'ce-puerta-o', x0, x1, y0, y1)
            P(l, 'ce-puerta-c', x0, x1 - 3, y0, y0 + 3)
            P(l, 'ce-puerta-c', x0, x0 + 3, y0, y1 - 3)
            P(l, 'ce-puerta', x0 + 3, x1 - 3, y0 + 3, y1 - 3)
    P(l, 'ce-oro', 764, 768, 290, 298)
    P(l, 'ce-oro', 755, 759, 270, 274)
    P(l, 'ce-negro', 680, 704, 232, 250)                                           # farolito de la galería
    # Toda la galería queda en sombra, más honda arriba.
    l.sombra(ux(480), ux(800), fy(218), fy(362), ('ce-terracota', 'ce-piedra', 'ce-piedra-c', 'ce-piedra-o', 'ce-piedra-r',
             'ce-vidrio-c', 'ce-puerta-c', 'ce-blanco-c',
             'ce-junta', 'ce-blanco', 'ce-vidrio', 'ce-cortina', 'ce-reja', 'ce-marco', 'ce-puerta', 'ce-puerta-o',
             'ce-galeria'))
    P(l, 'ce-galeria-s', 480, 800, 218, 232)
    P(l, 'ce-piso', 480, 800, 362, SUELO)
    for f in range(fy(362), fy(SUELO)):
        if f % 2: l.rect('ce-piso-s', ux(480), ux(800), f, f + 1)
    P(l, 'ce-blanco', 432, 482, 218, SUELO)                                        # pilar revocado
    P(l, 'ce-blanco-s', 474, 482, 218, SUELO)                                      # canto del pilar en sombra
    P(l, 'ce-maceta', 486, 518, 352, SUELO)                                        # maceta con la planta
    P(l, 'ce-maceta-c', 486, 494, 352, SUELO)
    for k, x in enumerate(range(482, 524, 6)):
        P(l, 'ce-hoja' if k % 2 else 'ce-hoja-c', x, x + 4, 312 + (k % 3) * 10, 352)

    # Ala del costado, a la derecha: un cuerpo aparte, más atrás, con su propio techito a dos aguas.
    AE, AM, AL = 1400, 80, 186                                       # eje, medio ancho y alero del ala
    def am(y): return (y - (AL - AM * 0.55)) / 0.55                  # medio ancho del borde a la altura y
    celdas(l, 1300, X1, 120, AL + 6, lambda x, y: 'ce-teja' if abs(x - AE) <= am(y) + 6 else None)
    celdas(l, 1300, X1, 120, AL + 6, lambda x, y: ('ce-teja-c' if x < AE else 'ce-teja-s')
           if am(y) - 10 < abs(x - AE) <= am(y) - 1 else None)
    celdas(l, 1300, X1, 120, AL + 6, lambda x, y: ('ce-blanco-c' if x < AE else 'ce-blanco-s')
           if am(y) - 26 < abs(x - AE) <= am(y) - 10 else None)
    celdas(l, 1300, X1, 120, SUELO, lambda x, y: 'ce-blanco' if abs(x - AE) <= am(y) - 26 and abs(x - AE) <= AM - 8 else None)
    piedra(l, AE - AM + 8, AE + AM - 8, 205, SUELO)
    P(l, 'ce-blanco-s', AE - AM + 8, AE + AM - 8, 186, 196)
    P(l, 'ce-piedra-s', AE + AM - 14, AE + AM - 8, 205, SUELO)
    P(l, 'ce-sombra', 1300, AE - AM + 8, 150, SUELO)                 # el entrante entre el hastial y el ala
    arco(l, AE - 26, AE + 26, 224, 300, lambda x, y: 'ce-marco')
    arco(l, AE - 20, AE + 20, 230, 294, lambda x, y: 'ce-vidrio')
    P(l, 'ce-reja', AE - 2, AE + 2, 230, 294)
    P(l, 'ce-reja', AE - 20, AE + 20, 258, 261)
    P(l, 'ce-blanco-c', AE - 30, AE + 30, 300, 306)

    # Hastial: borde de tejas, tabla blanca, revoque blanco arriba y piedra laja abajo.
    def medio(y): return (y - 36) / PEND                                          # medio ancho del borde a la altura y
    # Cada fila corre ~27 px el borde: las bandas son más anchas que eso, así la diagonal se lee seguida.
    celdas(l, 740, 1360, 30, 150, lambda x, y: 'ce-teja' if abs(x - EJE) <= medio(y) + 6 else None)
    celdas(l, 740, 1360, 30, 150, lambda x, y: ('ce-teja-c' if x < EJE else 'ce-teja-s')
           if medio(y) - 14 < abs(x - EJE) <= medio(y) - 2 else None)
    celdas(l, 740, 1360, 30, 150, lambda x, y: ('ce-blanco-c' if x < EJE else 'ce-blanco-s')
           if medio(y) - 44 < abs(x - EJE) <= medio(y) - 14 else None)
    celdas(l, 795, 1305, 50, SUELO, lambda x, y: 'ce-blanco' if abs(x - EJE) <= medio(y) - 44 else None)
    P(l, 'ce-teja-s', 760, 790, 138, 150)                                          # bocas de las tejas de los bordes
    P(l, 'ce-teja-s', 1310, 1340, 138, 150)
    # La piedra sube a la derecha; el revoque baja en diagonal (la escalera de adentro).
    def bajo_diagonal(x, y):
        if abs(x - EJE) > medio(y) - 44: return False
        if 1000 <= x <= 1104: return y > 284
        # El revoque baja en escalones que siguen las hiladas (cada 3 filas), no en una rampa lisa.
        yd = 240 - (x - 800) * 0.22 if x < 1000 else 150
        return y > Y0 + (math.ceil((yd - Y0) * S / 3) * 3) / S
    celdas(l, 795, 1305, 140, SUELO, lambda x, y: 'ce-piedra' if bajo_diagonal(x, y) else None)
    piedra_mask = [[l.c[f][i] == 'ce-piedra' for i in range(l.n)] for f in range(FILAS)]
    piedra(l, 795, 1305, 140, SUELO)
    for f in range(fy(140), fy(SUELO)):                                            # la laja solo donde iba piedra
        for i in range(round(ux(795) * 4), round(ux(1305) * 4)):
            if not piedra_mask[f][i] and l.c[f][i].startswith(('ce-piedra', 'ce-junta')):
                l.c[f][i] = 'ce-blanco'
    # Sombra finita del revoque (que está un poco adelante) sobre la piedra de abajo.
    for f in range(fy(140), fy(SUELO)):
        for i in range(round(ux(795) * 4), round(ux(1305) * 4)):
            if l.c[f][i].startswith(('ce-piedra', 'ce-junta')) and l.c[f - 1][i] == 'ce-blanco':
                l.c[f][i] = 'ce-piedra-s'
    P(l, 'ce-blanco-s', 1300, 1305, 140, SUELO)
    persiana(l, 1004, 1098, 112, 206)                                              # ventana alta en arco
    persiana(l, 902, 998, 274, 398)                                                # puerta baja en arco
    P(l, 'ce-negro', 896, 904, 160, 172)                                           # farol de pared
    P(l, 'ce-negro', 888, 912, 172, 178)
    P(l, 'ce-farol', 890, 910, 178, 206)
    P(l, 'ce-farol-c', 892, 900, 180, 204)
    P(l, 'ce-negro', 888, 912, 206, 212)
    P(l, 'ce-negro', 897, 903, 212, 222)
    P(l, 'ce-negro', 880, 896, 186, 190)

    # Adoquines.
    P(l, 'ce-adoquin', X0, X1, SUELO, Y1)
    for f in range(fy(SUELO), FILAS):
        k = f - fy(SUELO)
        x = ux(X0) + (k % 2) * 0.75
        while x < LARGO:
            l.rect('ce-adoquin-s', x, x + 0.25, f, f + 1)
            if (round(x * 4) + k * 3) % 5 == 0: l.rect('ce-adoquin-c', x + 0.25, x + 1.25, f, f + 1)
            x += 1.5
    P(l, 'ce-blanco-s', X0, X1, SUELO, SUELO + 6)
    piedra(l, 1300, X1, 398, 440)                                                  # cantero de piedra
    P(l, 'ce-piedra-c', 1300, X1, 398, 404)

    # Jardín: pastos a la izquierda, arbusto redondo, buzón, el formio y flores rosas.
    celdas(l, X0, 200, 392, Y1, lambda x, y: ('ce-hoja-c' if (x - 100) + (y - 430) < -20 else 'ce-hoja')
           if ((x - 110) / 70) ** 2 + ((y - 450) / 55) ** 2 <= 1 else None)
    for k, x in enumerate(range(190, 400, 12)):                                    # pastos ornamentales
        top = 372 + (k * 37 % 30)
        for f in range(fy(top), fy(Y1)):
            t = (py(f) - top) / (Y1 - top)
            xx = x + (1 - t) * (12 if k % 2 else -12)
            l.rect(('ce-pasto', 'ce-pasto-c', 'ce-pasto-r')[k % 3], ux(xx), ux(xx) + 0.5, f, f + 1)
    celdas(l, 450, 840, 368, Y1, lambda x, y: (('ce-arbusto-c' if (x - 600) + (y - 400) < -40 else
           'ce-arbusto-s' if (x - 660) + (y - 430) > 70 else 'ce-arbusto') if (i := (round(x / 9) + round(y / 8))) % 3 else 'ce-arbusto-s')
           if ((x - 620) / 120) ** 2 + ((y - 470) / 62) ** 2 <= 1 else None)
    P(l, 'ce-negro', 708, 716, 380, Y1)                                            # buzón sobre su poste
    P(l, 'ce-negro', 690, 734, 350, 392)
    P(l, 'ce-farol-c', 694, 702, 356, 386)
    P(l, 'ce-negro', 686, 738, 346, 352)
    for k in range(30):                                                            # formio: hojas en abanico
        a = math.radians(-160 + k * 140 / 29)
        largo = 120 + (k * 53 % 45)
        bx, by = 1150 + (k % 5 - 2) * 4, 448
        for f in range(fy(by - largo * abs(math.sin(a))), fy(by)):
            t = (by - py(f)) / (largo * abs(math.sin(a)) or 1)
            x = bx + math.cos(a) * largo * t * (0.6 + 0.4 * t)
            c = ('ce-formio', 'ce-formio-c', 'ce-formio-o', 'ce-formio')[k % 4]
            l.rect(c, ux(x) - 0.25, ux(x) + 0.75 * (1 - t) + 0.25, f, f + 1)
    for x, y in ((1330, 352), (1352, 340), (1440, 330), (1418, 362)):
        P(l, 'ce-flor', x - 6, x + 6, y, y + 8)
    for k, x in enumerate(range(1310, X1, 14)):
        P(l, 'ce-hoja' if k % 2 else 'ce-hoja-c', x, x + 5, 360 + (k % 3) * 8, 400)

    return {'nota': 'Un chalet californiano de Ciudad Evita: techos de tejas coloniales, el hastial poco '
                    'empinado con la ventana en arco de persiana, revoque blanco y piedra laja, la galería con '
                    'la puerta de madera, la reja ornamental, el farol negro y el jardín con el formio.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

SOMBREABLES = ('ce-piedra-r', 'ce-vidrio-c', 'ce-puerta-c', 'ce-blanco-c', 'ce-teja', 'ce-blanco', 'ce-piedra', 'ce-piedra-c', 'ce-piedra-o', 'ce-junta', 'ce-terracota',
               'ce-vidrio', 'ce-cortina', 'ce-reja', 'ce-marco', 'ce-puerta', 'ce-puerta-o', 'ce-galeria',
               'ce-ladrillo', 'ce-tablilla', 'ce-piso', 'ce-arbusto', 'ce-adoquin')
COLORES = {
    'ce-teja': ('#b8664a', '#a85d44'), 'ce-teja-c': ('#d08868', '#be7c5f'), 'ce-teja-v': ('#a78c7c', '#987f71'),
    'ce-blanco': ('#f1eee6', '#dcd9d1'), 'ce-blanco-c': ('#fbfaf6', '#e8e6e0'),
    'ce-piedra': ('#d9cfb4', '#c4bba2'), 'ce-piedra-c': ('#e8e0c9', '#d3cbb5'), 'ce-piedra-o': ('#c4b694', '#b0a385'), 'ce-piedra-r': ('#d2c2a2', '#bdae91'),
    'ce-junta': ('#ada184', '#9a8f75'), 'ce-terracota': ('#c4693f', '#b05e39'),
    'ce-vidrio': ('#3b3f44', '#33373b'), 'ce-vidrio-c': ('#5a6168', '#4e545a'), 'ce-cortina': ('#d9d4c8', '#c2bdb2'),
    'ce-reja': ('#f4f2ec', '#dedcd6'), 'ce-marco': ('#e9e5da', '#d3cfc5'),
    'ce-puerta': ('#8e4d26', '#7f4522'), 'ce-puerta-c': ('#ad6535', '#9b5a30'), 'ce-puerta-o': ('#6a3819', '#5f3216'), 'ce-oro': ('#d9b45a', '#c6a352'),
    'ce-sombra': ('#9c968a', '#86817a'), 'ce-galeria': ('#b9b1a0', '#a69f8f'), 'ce-ladrillo': ('#b5603f', '#a25639'),
    'ce-tablilla': ('#f3f1eb', '#dddbd5'), 'ce-tablilla-o': ('#b9b5ab', '#a5a198'),
    'ce-piso': ('#9a5a3e', '#8a5038'),
    'ce-negro': ('#1f1f1f', '#1a1a1a'), 'ce-farol': ('#5a5440', '#4f4a39'), 'ce-farol-c': ('#c9b98a', '#b6a87d'),
    'ce-maceta': ('#8f8f8a', '#80807b'), 'ce-maceta-c': ('#b0b0aa', '#9e9e98'),
    'ce-hoja': ('#4f7a3a', '#467034'), 'ce-hoja-c': ('#79a352', '#6c934a'),
    'ce-pasto': ('#9c8a4e', '#8c7c46'), 'ce-pasto-c': ('#c2ad6a', '#ae9b5f'), 'ce-pasto-r': ('#8a4f3e', '#7c4738'),
    'ce-arbusto': ('#7fae45', '#729d3e'), 'ce-arbusto-c': ('#a7cc62', '#96b858'),
    'ce-formio': ('#4b5a35', '#43512f'), 'ce-formio-c': ('#7d8c4e', '#707e46'), 'ce-formio-o': ('#2f3a24', '#2a3420'),
    'ce-flor': ('#e98aa8', '#d67e9a'),
    'ce-adoquin': ('#9a948c', '#7f7a73'), 'ce-adoquin-c': ('#b3ada4', '#958f88'),
    'californiano-fondo': ('#efe6d2', '#2b2722'), 'californiano-fondo-marco': ('#2b2722', '#efe6d2'),
}
con_sombras(COLORES, SOMBREABLES)

if __name__ == '__main__':
    p = version()
    p.update(placa='californiano-fondo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
             marco='californiano-fondo-marco')
    guardar(sys.argv[1], 'estilos', 'Chalet californiano', p, COLORES, 'ce-|californiano-')
    print(len(p['lineas']), 'líneas, largo', p['largo'])
