# A House for Essex (FAT con Grayson Perry, Wrabness, 2015), el lado largo, en elevación.
# Medida en px sobre referencias/simbolos/posmodernismo/Arquitectura_postmoderno-less_is_nore…jpg (750 × 529).
# Cuatro cuerpos que bajan de izquierda a derecha, como un telescopio, más el anexo bajo de la izquierda.
# En elevación pura: cada techo es un faldón rectangular (los hastiales quedan de canto, así que los
# extremos son verticales y los cortes, rectos). Faldones de chapa dorada con juntas alzadas, buhardillas
# con capotas en arco y ventanas rojas de guillotina; paredes con la misma cantidad de piezas que la casa:
# azulejos verdes con una figura en su nicho (6 × 6) y bandas de triángulos verdes y blancos (6 de base,
# 3 líneas de alto); pilastras doradas entre cuerpos. Remates: el farol en rombo, el huevo de arlequín
# sobre su chimenea, la figura de Julie y la rueda. Abajo, el prado.
# Todo lo simétrico se arma en unidades desde su centro (centrado()), así los dos lados quedan iguales.
# Uso: essex.py <simbolos.json> (pone estilos."Posmodernismo").
import sys, math
from armar import Lienzo, guardar, oscurecer, con_sombras

S = 0.38                                   # unidades por px
X0, X1, Y0, Y1 = 36, 690, 44, 462
SUELO = 444                                # paredes un sexto más bajas que en la foto
LARGO = round((X1 - X0) * S)
FILAS = round((Y1 - Y0) * S)

def q(x): return round(x * 4) / 4

# La grilla: la fachada se arma en módulos de 6 (un azulejo = la base de un triángulo). Cada cuerpo mide un
# número entero de módulos y las pilastras, todas de 2, van entre cuerpos. C son los centros de las pilastras,
# en unidades; los px de la foto se reacomodan a esta grilla tramo por tramo (reubicar()).
MODULOS = (3, 13, 9, 6, 4)                                  # anexo, A, B, C, D
C = [15]
for n in MODULOS: C.append(C[-1] + 6 * n + 2)
LARGO = C[-1] + 15                                            # el mismo margen a los dos lados
VIEJOS = (74.5, 129.5, 348.5, 508.5, 613, 673.5)              # dónde estaban en la foto, en px

def reubicar(px):
    nuevos = [X0 + c / S for c in C]
    k = 0 if px < VIEJOS[1] else len(VIEJOS) - 2 if px >= VIEJOS[-2] else max(i for i in range(len(VIEJOS) - 1) if VIEJOS[i] <= px)
    t = (px - VIEJOS[k]) / (VIEJOS[k + 1] - VIEJOS[k])
    return nuevos[k] + t * (nuevos[k + 1] - nuevos[k])

def ux(px): return q((reubicar(px) - X0) * S)
def pared(k): return C[k] + 1, C[k + 1] - 1                   # de pilastra a pilastra, en unidades
def fy(py): return round((py - Y0) * S)
def py(f): return Y0 + (f + 0.5) / S         # centro de la fila, en px

def P(l, c, x0, x1, y0, y1):
    l.rect(c, ux(x0), ux(x1), fy(y0), max(fy(y0) + 1, fy(y1)))

def centrado(l, c, cu, hu, f0, f1=None):
    # Tramo simétrico: centro cu y medio ancho hu, en unidades.
    hu = q(hu)
    l.rect(c, cu - hu, cu + hu, f0, f0 + 1 if f1 is None else f1)

def triangulos(l, a, b, f0, hileras, base=6, alto=3):
    # `hileras` de triángulos de `alto` líneas desde la fila f0, entre a y b (unidades), alineados desde a:
    # verdes para arriba, blancos para abajo, cada hilada corrida media pieza. Devuelve la fila donde terminan.
    l.rect('es-blanco', a, b, f0, f0 + alto * hileras)
    for f in range(f0, f0 + alto * hileras):
        k, j = divmod(f - f0, alto)
        hw = q(base / 2 * (j + 0.5) / alto)                     # medio ancho: un escalón parejo por línea
        c = a + (k % 2) * base / 2
        while c - hw < b:
            l.rect('es-verde', max(a, c - hw), min(b, c + hw), f, f + 1)
            c += base
    return f0 + alto * hileras

# Un azulejo de 6 × 6: la junta, el marco, el nicho en arco y la figura (cabeza y hombros).
AZULEJO = (
    (),
    (('es-verde', .25, 5.75), ('es-verde-c', 2, 4)),
    (('es-verde', .25, 5.75), ('es-verde-c', 1.5, 4.5), ('es-nicho', 2, 4)),
    (('es-verde', .25, 5.75), ('es-verde-c', 1.5, 4.5), ('es-nicho', 2, 4), ('es-cara', 2.75, 3.25)),
    (('es-verde', .25, 5.75), ('es-verde-c', 1.5, 4.5), ('es-nicho', 2, 4), ('es-cara', 2.5, 3.5)),
    (('es-verde', .25, 5.75), ('es-verde-c', 1.25, 4.75), ('es-verde-o', 4.5, 4.75)),
)

def azulejos(l, a, b, f0, f1):
    # Azulejos de 6 × 6 entre a y b (unidades), alineados desde a, de la fila f0 a la f1.
    l.rect('es-junta', a, b, f0, f1)
    for f in range(f0, f1):
        x = a
        while x + 6 <= b + 0.01:
            for c, d, h in AZULEJO[(f - f0) % 6]: l.rect(c, x + d, x + h, f, f + 1)
            x += 6

def pilastra(l, cu, f0, f1):
    # Todas de 2, centradas en cu: luz a la izquierda, sombra a la derecha.
    l.rect('es-oro', cu - 1, cu + 1, f0, f1)
    l.rect('es-oro-c', cu - 1, cu - 0.5, f0, f1)
    l.rect('es-oro-o', cu + 0.5, cu + 1, f0, f1)

# Sombras: cada color de la casa tiene su versión en sombra (-s), un poco más oscura.
CON_SOMBRA = ('es-oro', 'es-oro-c', 'es-oro-o', 'es-verde', 'es-verde-c', 'es-verde-o', 'es-junta', 'es-nicho',
              'es-cara', 'es-blanco', 'es-negro', 'es-negro-c', 'es-rojo', 'es-rojo-o', 'es-vidrio', 'es-vidrio-c',
              'es-cielo', 'es-sombra', 'es-vidrio-m', 'es-vidrio-o', 'es-rojo-c')

def sombra(l, a, b, f0, f1):
    l.sombra(a, b, f0, f1, CON_SOMBRA)

def faldon(l, a, b, y0, y1, junta=6):
    # Faldón rectangular de chapa dorada entre a y b (unidades): cumbrera arriba, juntas alzadas marcadas
    # cada `junta` unidades (sombra y luz), y los cantos de los hastiales, verticales.
    l.rect('es-oro', a, b, fy(y0), fy(y1))
    x = a + junta
    while x < b - 2:
        l.rect('es-oro-o', x, x + 0.5, fy(y0) + 1, fy(y1))
        l.rect('es-oro-c', x + 0.5, x + 0.75, fy(y0) + 1, fy(y1))
        x += junta
    l.rect('es-oro-c', a, b, fy(y0), fy(y0) + 1)                 # cumbrera
    l.rect('es-oro-c', a, a + 0.5, fy(y0), fy(y1))               # cantos
    l.rect('es-oro-o', b - 0.75, b, fy(y0), fy(y1))

def alero(l, a, b, y0, y1):
    l.rect('es-oro-c', a, b, fy(y0), fy(y1))
    l.rect('es-oro', a, b, fy(y0) + 1, fy(y1) - 1)
    l.rect('es-oro-o', a, b, fy(y1) - 1, fy(y1))

def arco(l, c, cu, hu, f0, f1):
    # Medio punto de medio ancho hu (unidades) con centro cu, desde la fila f0 hasta f1: simétrico.
    filas_arco = max(1, round(hu))
    for f in range(f0, f1):
        k = f - f0
        if k < filas_arco:
            t = 1 - (k + 0.5) / filas_arco
            h = hu * math.sqrt(max(0, 1 - t * t))
        else: h = hu
        if h >= 0.25: centrado(l, c, cu, h, f)

def buhardilla(l, x0, x1, ytop, y1, capota=10):
    # Capota dorada en arco con su sombra, y la ventana roja: abanico del arco que refleja el cielo,
    # dos hojas de guillotina con sus paños, reflejos y el alféizar.
    cu = ux((x0 + x1) / 2)
    hv = q((x1 - x0) / 2 * S)
    hc = hv + q(capota * S)
    f0, f1 = fy(ytop), fy(y1)
    fc = f0 - round(capota * S)
    arco(l, 'es-oro-s', cu + 0.75, hc, fc + 1, f1 + 1)           # la sombra de la capota sobre el techo
    arco(l, 'es-oro-o', cu, hc, fc, f1 + 1)                       # el borde de la derecha, en sombra
    arco(l, 'es-oro-c', cu - 0.5, hc - 0.5, fc, f1 + 1)           # la luz de la izquierda
    arco(l, 'es-oro', cu, hc - 1, fc + 1, f1 + 1)
    arco(l, 'es-oro-s', cu + 0.5, hv + 1, f0 - 2, f1)             # la cara de adentro, en sombra
    l.rect('es-oro-o', cu + hc - 1, cu + hc - 0.5, fc + round(hc), f1 + 1)   # el costado en sombra
    arco(l, 'es-sombra', cu, hv + 0.5, f0 - 1, f1)               # el hueco
    arco(l, 'es-rojo', cu, hv, f0, f1)
    m = 0.75 if hv >= 5 else 0.5
    fa = f0 + max(1, round(hv))                                   # arranque del arco
    arco(l, 'es-cielo', cu, hv - m, f0 + 1, fa)
    l.rect('es-rojo', cu - hv, cu + hv, fa, fa + 1)               # travesaño del arranque
    mm = (fa + f1) // 2 if f1 - fa > 7 else f1 - 1                # encuentro de las dos hojas
    for g0, g1 in ((fa + 1, mm), (mm + 1, f1 - 1)) if f1 - fa > 7 else ((fa + 1, f1 - 1),):
        pano(l, cu - hv + m, cu - 0.25, g0, g1)
        pano(l, cu + 0.25, cu + hv - m, g0, g1)
    if f1 - fa > 7:
        l.rect('es-rojo', cu - hv + m, cu + hv - m, mm, mm + 1)
        l.rect('es-rojo-o', cu - hv + m, cu + hv - m, mm + 1, mm + 2) if f1 - fa > 14 else None
    l.rect('es-rojo', cu - 0.25, cu + 0.25, fa, f1 - 1)           # parteluz
    l.rect('es-rojo-c', cu - hv, cu - hv + 0.25, fa, f1)          # canto con luz del marco
    l.rect('es-rojo-o', cu + hv - 0.25, cu + hv, fa, f1)          # canto en sombra del marco
    centrado(l, 'es-oro-c', cu, hc, f1, f1 + 1)                   # alféizar
    centrado(l, 'es-oro-o', cu, hc - 0.5, f1 + 1, f1 + 2)

def pano(l, a, b, f0, f1):
    # Un paño de vidrio (unidades a-b, filas f0-f1): sombra del marco arriba, el cielo reflejado más claro
    # en el primer tercio y dos reflejos en diagonal.
    if b - a < 0.5 or f1 <= f0: return
    l.rect('es-vidrio', a, b, f0, f1)
    l.rect('es-vidrio-m', a, b, f0, f0 + max(1, (f1 - f0) // 3))
    l.rect('es-vidrio-o', a, b, f0, f0 + 1)
    for f in range(f0 + 1, f1):
        x = a + 0.5 + (f - f0) * 0.5
        for d, w in ((0, 0.5), (1.0, 0.25)):
            xa, xb = max(a, x + d), min(b, x + d + w)
            if xa < xb: l.rect('es-vidrio-c', xa, xb, f, f + 1)

def cono(l, cx, y0, y1, k):
    for f in range(fy(y0), fy(y1)):
        h = (py(f) - y0) * k * S
        if h < 0.25: continue
        cu = ux(cx)
        centrado(l, 'es-oro-c', cu, h, f)
        l.rect('es-oro-o', cu, cu + q(h), f, f + 1)

def circulo(l, c, cx, cy, r):
    for f in range(fy(cy - r), fy(cy + r) + 1):
        d = r * r - (py(f) - cy) ** 2
        if d > 0: centrado(l, c, ux(cx), math.sqrt(d) * S, f)

def version():
    l = Lienzo(LARGO, FILAS)

    # Los faldones, de atrás para adelante: cada cuerpo baja un escalón y su techo arranca donde
    # termina el anterior, con el corte vertical.
    TOPES = (225, 128, 165, 201, 234)                             # cumbreras, en px
    ALEROS = ((356, 366), (262, 280), (283, 300), (304, 322), (322, 338))
    for k in (4, 3, 2, 1, 0):
        faldon(l, C[k] - 1, C[k + 1] + 1, TOPES[k], ALEROS[k][0] + 2)
    l.rect('es-oro-o', C[0] - 1, C[1] + 1, fy(278), fy(278) + 1)     # el quiebre del anexo

    # Los faldones se oscurecen hacia el alero y hacia el canto de la derecha.
    for k in range(5):
        a, b = C[k] - 1, C[k + 1] + 1
        sombra(l, a, b, fy(ALEROS[k][0]) - 3, fy(ALEROS[k][0]))
        sombra(l, b - 1.5, b, fy(TOPES[k]) + 1, fy(ALEROS[k][0]))

    # Buhardillas.
    for x0 in (163, 260):
        buhardilla(l, x0, x0 + 62, 140, 255, 12)
    for x0 in (379, 448):
        buhardilla(l, x0, x0 + 42, 206, 280, 8)
    for x0 in (523, 566):
        buhardilla(l, x0, x0 + 25, 254, 300, 5)
    for x0 in (620, 645):
        buhardilla(l, x0, x0 + 16, 294, 320, 4)

    # Aleros, que vuelan un poco más allá de las pilastras.
    for k in (4, 3, 2, 1, 0):
        alero(l, C[k] - 1.5, C[k + 1] + 1.5, *ALEROS[k])

    # Paredes, banda por banda como en la foto (a: hileras de azulejos, t: hileras de triángulos;
    # la última de azulejos llega hasta el suelo).
    BANDAS = ((('a', 2), ('t', 3)), (('t', 3), ('a', 4), ('t', 7)), (('a', 4), ('t', 8)),
              (('a', 2), ('t', 6)), (('a', 1), ('t', 6)))
    for k in range(5):
        a, b = pared(k)
        f = fy(ALEROS[k][1])
        for tipo, n in BANDAS[k]:
            if tipo == 't': f = triangulos(l, a, b, f, n)
            else:
                azulejos(l, a, b, f, f + 6 * n)
                f += 6 * n
        azulejos(l, a, b, f, fy(SUELO))
    for k in range(6):                                            # pilastras, desde el alero más bajo de los dos lados
        tope = min(ALEROS[j][1] for j in (k - 1, k) if 0 <= j < 5)
        pilastra(l, C[k], fy(tope), fy(SUELO))

    # La sombra de cada alero sobre su pared, y la del pie.
    for k in range(5):
        sombra(l, C[k] - 1, C[k + 1] + 1, fy(ALEROS[k][1]), fy(ALEROS[k][1]) + 2)
    sombra(l, C[0] - 1, C[5] + 1, fy(SUELO) - 1, fy(SUELO))

    # Puerta vidriera roja en B, de cuatro módulos justos: marco de piedra clara, marco rojo con luz y sombra,
    # montante de tres paños, dos hojas de a dos por tres paños, manijas de bronce y el escalón.
    a, _ = pared(2)
    da, db = a + 12, a + 36
    ft, fs = fy(374), fy(SUELO)
    l.rect('es-oro-c', da, db, ft, fs)
    l.rect('es-oro-o', db - 0.75, db, ft, fs)
    l.rect('es-rojo', da + 1, db - 1, ft + 1, fs)
    l.rect('es-rojo-c', da + 1, da + 1.5, ft + 1, fs)
    l.rect('es-rojo-o', db - 1.75, db - 1, ft + 1, fs)
    ga, gb = da + 2, db - 2
    fm = ft + 7                                                    # el montante
    for k in range(3):
        pano(l, ga + k * (gb - ga) / 3 + (0.25 if k else 0), ga + (k + 1) * (gb - ga) / 3 - (0.25 if k < 2 else 0), ft + 2, fm)
    c = (da + db) / 2
    f0, f1 = fm + 1, fs - 2
    filas = [round(f0 + k * (f1 - f0) / 3) for k in range(4)]
    for x0, x1 in ((ga, c - 0.75), (c + 0.75, gb)):
        cc = q((x0 + x1) / 2)
        for g0, g1 in zip(filas, filas[1:]):
            pano(l, x0, cc - 0.25, g0, g1 - 1)
            pano(l, cc + 0.25, x1, g0, g1 - 1)
        l.rect('es-rojo', cc - 0.25, cc + 0.25, f0, f1)
    l.rect('es-rojo-o', c - 0.5, c + 0.5, f0, fs)                   # el encuentro de las hojas
    l.rect('es-oro-o', c - 2, c - 1.25, f0 + 6, f0 + 9)             # manijas
    l.rect('es-oro-o', c + 1.25, c + 2, f0 + 6, f0 + 9)
    l.rect('es-piedra', da - 1.5, db + 1.5, fs - 2, fs)            # el escalón
    l.rect('es-piedra-o', da - 1.5, db + 1.5, fs - 1, fs)

    # La rueda: un disco de plata con aros concéntricos, sobre una media luna con los cuernos para arriba,
    # en su palo y su cono dorado.
    cono(l, 556, 188, 201, 0.5)
    centrado(l, 'es-plata-o', ux(556), 0.5, fy(168), fy(190))
    cu = ux(556)
    for f in range(fy(166), fy(181)):                              # la media luna: la mitad de abajo de un aro
        y = py(f)
        d1, d2 = 14 ** 2 - (y - 166) ** 2, 10.5 ** 2 - (y - 166) ** 2
        if d1 <= 0: continue
        h1, h2 = q(math.sqrt(d1) * S), q(math.sqrt(d2) * S) if d2 > 0 else 0
        l.rect('es-plata', cu - h1, cu - h2, f, f + 1)
        l.rect('es-plata-o', cu + h2, cu + h1, f, f + 1)
    for r, c in ((12, 'es-plata-o'), (10.5, 'es-plata'), (8, 'es-plata-c'), (6.5, 'es-plata'), (4, 'es-plata-o'), (2, 'es-plata-c')):
        circulo(l, c, 556, 148, r)
    centrado(l, 'es-plata-o', ux(556), 0.25, fy(133), fy(136))     # la puntita

    # Julie: la figura de plata con los brazos abiertos hacia abajo, en su palo y su cono.
    cono(l, 469, 156, 166, 0.5)
    cj = ux(469)
    centrado(l, 'es-plata-o', cj, 0.5, fy(150), fy(158))
    circulo(l, 'es-plata-o', 469, 98, 4.5)                         # cabeza
    for y0, y1, h in ((102.5, 105, 1.5), (105, 108, 5), (108, 116, 4.5), (116, 121, 3), (121, 129, 5),
                      (129, 140, 3.5), (140, 150, 2)):
        for f in range(fy(y0), fy(y1)):
            centrado(l, 'es-plata-o', cj, h * S, f)               # cuello, hombros, torso, cintura, cadera, piernas
            l.rect('es-plata', cj - q(h * S), cj - q(h * S * 0.3), f, f + 1)   # la luz de la izquierda
    centrado(l, 'es-sombra', cj, 0.125, fy(132), fy(150))         # entre las piernas
    for f in range(fy(106), fy(126)):                              # los brazos, separados del cuerpo
        t = (py(f) - 106) / 20
        x = (6 + t * 6) * S
        l.rect('es-plata-o', cj - x - 0.75, cj - x, f, f + 1)
        l.rect('es-plata-o', cj + x, cj + x + 0.75, f, f + 1)

    # La chimenea de triángulos grandes, con su capitel dorado, y el huevo de arlequín encima.
    cc = ux(347.5)
    fa, fb = fy(116), fy(165)
    hch = 6                                                       # tres triángulos de 4 justos
    triangulos(l, cc - hch, cc + hch, fa + 2, (fb - fa - 2) // 4, base=4, alto=4)
    l.rect('es-verde-o', cc + hch - 0.5, cc + hch, fa + 2, fb)
    centrado(l, 'es-oro-c', cc, hch + 0.75, fa)                    # capitel
    centrado(l, 'es-oro', cc, hch + 0.5, fa + 1)
    fe0, fe1 = fy(60), fa
    for f in range(fe0, fe1):
        t = (f - fe0 + 0.5) / (fe1 - fe0)
        h = 14 * S * math.sqrt(max(0, 1 - ((t - 0.56) / (0.56 if t < 0.56 else 0.46)) ** 2))
        if h < 0.5: h = 0.5
        centrado(l, 'es-blanco', cc, h, f)
        for i in range(round((cc - h) * 4), round((cc + h) * 4)):
            x = i / 4 + 0.125 - cc
            X, Y = x / 1.5, (f - fe0 + 0.5) / 3                   # rombos de 3 de ancho y 6 líneas de alto
            a, j = round(X), round(Y)
            if (a + j) % 2: a, j = min(((a + 1, j), (a - 1, j), (a, j + 1), (a, j - 1)),
                                       key=lambda c: abs(X - c[0]) + abs(Y - c[1]))
            if a % 2 == 0:
                l.c[f][i] = 'es-verde-o' if x > h * 0.4 else 'es-verde'
        l.rect('es-sombra-c', cc + q(h) - 0.25, cc + q(h), f, f + 1)
    centrado(l, 'es-plata-o', cc, 0.25, fe0 - 3, fe0)

    # El farol: un octaedro alto de vidrio con las aristas de hierro, la puntita arriba y el cono dorado.
    cf = ux(178)
    ym, arriba, abajo, ancho = 80, 26, 30, 12
    for f in range(fy(ym - arriba), fy(ym + abajo)):
        y = py(f)
        h = ancho * (1 - abs(y - ym) / (arriba if y < ym else abajo))
        if h <= 0: continue
        hu = q(h * S)
        centrado(l, 'es-farol', cf, hu, f)
        l.rect('es-hierro', cf - hu, cf - hu + 0.5, f, f + 1)     # aristas de afuera
        l.rect('es-hierro', cf + hu - 0.5, cf + hu, f, f + 1)
        l.rect('es-hierro', cf - 0.25, cf + 0.25, f, f + 1)       # la arista del medio
        l.rect('es-farol-o', cf + 0.25, cf + hu - 0.5, f, f + 1)  # la cara de la derecha, más oscura
    centrado(l, 'es-hierro', cf, ancho * S, fy(ym), fy(ym) + 1)
    centrado(l, 'es-hierro', cf, 0.25, fy(ym - arriba - 6), fy(ym - arriba))
    centrado(l, 'es-plata-o', cf, 0.25, fy(ym + abajo), fy(122))
    cono(l, 178, 116, 128, 0.6)

    # El prado.
    l.rect('es-pasto', 0, LARGO, fy(SUELO), FILAS)
    for f in range(fy(SUELO) + 1, FILAS):
        x = (f % 2) * 1.0
        while x < LARGO:
            l.rect('es-pasto-c', x, x + 0.5, f, f + 1)
            x += 2
    l.rect('es-zocalo', C[0] - 1, C[5] + 1, fy(SUELO) - 1, fy(SUELO))
    return {'nota': 'A House for Essex (FAT con Grayson Perry, 2015): los cuatro cuerpos que bajan como un '
                    'telescopio, techos de chapa dorada con buhardillas en arco y ventanas rojas, azulejos verdes '
                    'con figuras y bandas de triángulos, y los remates: farol, huevo, Julie y la rueda.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

COLORES = {
    'es-verde': ('#3a5524', '#3a5524'), 'es-verde-o': ('#2c441a', '#2c441a'), 'es-verde-c': ('#516e31', '#516e31'),
    'es-junta': ('#233218', '#233218'), 'es-nicho': ('#2c3f1c', '#2c3f1c'), 'es-cara': ('#a9b06e', '#a9b06e'),
    'es-blanco': ('#efede4', '#e6e3d8'),
    'es-oro': ('#d6c595', '#d2c08e'), 'es-oro-o': ('#b3a06b', '#b3a06b'), 'es-oro-c': ('#e9dfbc', '#e3d8b2'),
    'es-sombra': ('#8a7a52', '#8a7a52'), 'es-sombra-c': ('#c9c3b0', '#c9c3b0'),
    'es-rojo': ('#b42c28', '#b42c28'), 'es-rojo-o': ('#7e1d1b', '#7e1d1b'),
    'es-vidrio': ('#2f3a4a', '#2f3a4a'), 'es-vidrio-c': ('#5d6d82', '#5d6d82'),
    'es-vidrio-m': ('#3c495b', '#3c495b'), 'es-vidrio-o': ('#222a36', '#222a36'),
    'es-rojo-c': ('#d4544a', '#d4544a'), 'es-piedra': ('#c9c2b0', '#a8a192'), 'es-piedra-o': ('#9e9886', '#7f7a6e'),
    'es-cielo': ('#9aa7b6', '#9aa7b6'), 'es-cielo-c': ('#b9c3cf', '#b9c3cf'),
    'es-plata': ('#cfd3d6', '#cfd3d6'), 'es-plata-o': ('#8e9499', '#8e9499'), 'es-plata-c': ('#f2f4f5', '#f2f4f5'),
    'es-hierro': ('#2b2d30', '#2b2d30'), 'es-farol': ('#c9d4dc', '#c9d4dc'), 'es-farol-o': ('#9eabb5', '#9eabb5'),
    'es-negro': ('#1d221b', '#1d221b'), 'es-negro-c': ('#353d31', '#353d31'),
    'es-agua': ('#8a9aa6', '#5c6c78'), 'es-agua-c': ('#a9b6bf', '#73838e'), 'es-costa': ('#5a6650', '#3e4838'),
    'es-campo': ('#7f9a4c', '#5d7438'), 'es-poste': ('#7a6a54', '#8a7a64'), 'es-alambre': ('#6a5c4a', '#7a6c5a'),
    'es-pasto': ('#6a8a3a', '#55702e'), 'es-pasto-c': ('#7a9a44', '#627e36'),
    'es-zocalo': ('#3a3a34', '#3a3a34'),
    'pos-bosque': ('#4f6a52', '#1a241b'), 'pos-bosque-marco': ('#f3ead9', '#e5dbe4'),
}

con_sombras(COLORES, CON_SOMBRA)
COLORES['es-oro-s'] = tuple(oscurecer(v, 0.88) for v in COLORES['es-oro'])

if __name__ == '__main__':
    p = version()
    p.update(placa='pos-bosque', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
             marco='pos-bosque-marco')
    guardar(sys.argv[1], 'estilos', 'Posmodernismo', p, COLORES, 'es-|pos-')
    print(len(p['lineas']), 'líneas, largo', p['largo'])
