# Lancaster House (Manchester), la esquina de Whitworth Street y Princess Street, de frente y simétrica,
# como Alwyn Court: la torre de la ochava en el eje y las dos fachadas a los lados, con los tramos que se
# angostan al alejarse para que se lea la esquina; la fachada derecha en sombra suave.
# Medida a ojo sobre referencias/simbolos/barroco eduardiano/67_Whitworth_Street.jpg (torre y remate,
# recortes lan-arriba y lan-abajo) y images (10).jpeg / features.jpg (fachada larga, ventanas en arco y óculos).
# Torre: fuste de terracota ocre con una ventana por piso (frontis triangulares y curvos alternados),
# caras de la ochava más angostas; arriba de la cornisa, el cuerpo cuadrado con dos pisos de ventanitas
# y los torreones de los lados con su remate; el cuerpo ochavado almohadillado con arcos altos, el balcón
# con ménsulas, el cuerpo de las volutas con su nicho, la linterna de columnitas y la cúpula con la punta.
# Fachadas: planta baja y primer piso de piedra almohadillada, cornisa gruesa, siete pisos de ladrillo rojo
# con fajas ocres, ventanas de guillotina en pares (en arco arriba, con óculo en el último), cornisa con
# dentículos y baranda. En la vereda, faroles y el semáforo de la esquina.
# Uso: lancaster.py <simbolos.json> (pone estilos."Barroco eduardiano").
import sys
from armar import Lienzo, guardar

LARGO = 100
CX = LARGO / 2
FILAS = 236
BASE = 230                                 # vereda
TOPE = 90                                  # baranda de las fachadas

def q(x): return round(x * 4) / 4

def tono(c, lado):
    # Del lado derecho, la versión en sombra del color (si la hay).
    return c + '-s' if lado > 0 and c + '-s' in COLORES else c

def R(l, c, a, b, f0, f1):
    # De a a b desde el eje, a los dos lados (el derecho en sombra).
    a, b = q(a), q(b)
    l.rect(tono(c, -1), CX - b, CX - a, f0, f1)
    l.rect(tono(c, 1), CX + a, CX + b, f0, f1)

def C(l, c, a, b, f0, f1):
    # Centrado en el eje (la cara del frente de la torre), sin sombra.
    l.rect(c, CX + q(a), CX + q(b), f0, f1)

# Pisos de las fachadas: (arriba, abajo, tipo).
PISOS = [(96, 107, 'oculo'), (107, 119, 'arco'), (119, 131, 'arco'), (131, 143, 'recta'), (143, 155, 'recta'),
         (155, 167, 'recta'), (167, 179, 'recta'), (179, 191, 'recta')]
BAHIAS = [(11, 21), (21, 30.5), (30.5, 39.5), (39.5, 48)]       # tramos de cada fachada, cada vez más angostos

def ventana(l, x0, x1, f0, f1, cab='recta', pintar=R):
    # Ventana de guillotina: marco blanco, cuatro vidrios, telar rojo oscuro; la cabeza en arco o recta.
    pintar(l, 'la-telar', x0 - 0.25, x1 + 0.25, f0, f1)
    pintar(l, 'la-marco', x0, x1, f0, f1)
    m = (x0 + x1) / 2
    pintar(l, 'la-vidrio', x0 + 0.25, m - 0.25 if x1 - x0 >= 2 else x1 - 0.25, f0 + 1, (f0 + f1) // 2)
    pintar(l, 'la-vidrio', m + 0.25, x1 - 0.25, f0 + 1, (f0 + f1) // 2)
    pintar(l, 'la-vidrio', x0 + 0.25, m - 0.25, (f0 + f1) // 2 + 1, f1 - 1)
    pintar(l, 'la-vidrio', m + 0.25, x1 - 0.25, (f0 + f1) // 2 + 1, f1 - 1)
    if cab == 'arco':                                            # arco de medio punto con dovelas ocres
        w = (x1 - x0) / 2
        for k, d in enumerate((0.55, 0.85, 1)):
            pintar(l, 'la-piedra-c', m - w * d - 0.5, m + w * d + 0.5, f0 - 3 + k, f0 - 2 + k)
        pintar(l, 'la-marco', m - w * 0.5, m + w * 0.5, f0 - 2, f0 - 1)
        pintar(l, 'la-vidrio', m - w * 0.8 + 0.25, m + w * 0.8 - 0.25, f0 - 1, f0)
        pintar(l, 'la-piedra-c', m - 0.25, m + 0.25, f0 - 4, f0 - 2)       # clave
    else:
        pintar(l, 'la-piedra-c', x0 - 0.5, x1 + 0.5, f0 - 1, f0)            # dintel
    pintar(l, 'la-piedra-c', x0 - 0.5, x1 + 0.5, f1, f1 + 1)                # alféizar

def frontis(l, m, w, f, curvo, pintar=C):
    # Frontis sobre la ventana de la torre: triangular o curvo, con su sombra.
    for k in range(3):
        hw = w * ((k + 1) / 3 if not curvo else (0.7, 0.9, 1)[k])
        pintar(l, 'la-piedra-c', m - hw, m + hw, f - 3 + k, f - 2 + k)
    pintar(l, 'la-piedra-o', m - w, m + w, f - 0, f + 1)

def almohadillado(l, a, b, f0, f1, cara=R, paso=2):
    # Juntas horizontales de la piedra almohadillada, y verticales corridas por hilada.
    for f in range(f0, f1):
        if (f - f0) % paso == paso - 1:
            cara(l, 'la-piedra-o', a, b, f, f + 1)
        elif (f - f0) // paso % 2 == 0:
            x = a + 2
            while x < b - 0.5:
                cara(l, 'la-piedra-o', x, x + 0.25, f, f + 1)
                x += 4

def version():
    l = Lienzo(LARGO, FILAS)

    # Fachadas: ladrillo rojo con fajas ocres en los pilares, de la baranda a la cornisa del primer piso.
    R(l, 'la-ladrillo', 11, 50, TOPE, 192)
    for f in range(98, 192, 2):
        R(l, 'la-ladrillo-o', 11, 50, f, f + 1)                    # hiladas del ladrillo
    for a, b in BAHIAS:                                            # pilares entre tramos con fajas ocres
        R(l, 'la-ladrillo', b - 1, b + 1, 96, 192)
        for f in range(96, 192, 4):
            R(l, 'la-piedra', b - 1, b + 1, f, f + 2)
        R(l, 'la-ladrillo-o', b + 1, b + 1.25, 96, 192)
    for f0, f1, tipo in PISOS:
        for a, b in BAHIAS:
            m, w = (a + b) / 2, (b - a)
            if tipo == 'oculo':                                    # último piso: un óculo por tramo
                r = min(2.5, w * 0.22)
                for k, d in enumerate((0.5, 0.9, 1, 1, 0.9, 0.5)):
                    R(l, 'la-piedra-c', m - r * d - 0.5, m + r * d + 0.5, f0 + 2 + k, f0 + 3 + k)
                    R(l, 'la-vidrio', m - r * d * 0.7, m + r * d * 0.7, f0 + 2 + k, f0 + 3 + k)
                R(l, 'la-marco', m - 0.25, m + 0.25, f0 + 2, f0 + 8)
                continue
            g = 0.5 if w > 9 else 0.25                             # dos ventanas por tramo
            ventana(l, a + w * 0.18, m - g, f0 + 3, f1 - 1, tipo)
            ventana(l, m + g, b - w * 0.18, f0 + 3, f1 - 1, tipo)
    # Cornisa grande con dentículos y la baranda.
    R(l, 'la-piedra', 11, 50, TOPE + 2, 96)
    R(l, 'la-piedra-c', 11, 50, TOPE + 2, TOPE + 3)
    for x in range(0, 156):
        if x % 2 == 0: R(l, 'la-piedra-o', 11 + x * 0.25, 11.25 + x * 0.25, 94, 95)
    R(l, 'la-piedra-o', 11, 50, 95, 96)
    # Pretil con balaustres parejos, cada uno sobre su lugar, y dados sobre los pilares.
    R(l, 'la-piedra', 17, 50, TOPE - 1, TOPE + 2)
    R(l, 'la-piedra-c', 17, 50, TOPE - 6, TOPE - 5)                 # pasamanos
    x = 17.75
    while x < 49.5:
        R(l, 'la-piedra', x, x + 0.5, TOPE - 5, TOPE - 1)           # balaustre
        R(l, 'la-piedra-c', x + 0.125 if False else x, x + 0.25, TOPE - 4, TOPE - 2)
        x += 1
    for a, b in BAHIAS[1:]:
        R(l, 'la-piedra', b - 1, b + 1, TOPE - 7, TOPE + 2)          # dado
        R(l, 'la-piedra-c', b - 1.25, b + 1.25, TOPE - 8, TOPE - 7)
    # Mansarda del fondo: techo de pizarra con una buhardilla de piedra por tramo.
    R(l, 'la-pizarra', 17, 50, TOPE - 9, TOPE - 6)
    R(l, 'la-pizarra-c', 17, 50, TOPE - 10, TOPE - 9)
    for a, b in BAHIAS[1:]:
        m = (a + b) / 2
        R(l, 'la-piedra', m - 1.75, m + 1.75, TOPE - 13, TOPE - 6)
        for k, hw in enumerate((0.75, 1.5, 2.25)):                  # frontis de la buhardilla
            R(l, 'la-piedra-c', m - hw, m + hw, TOPE - 16 + k, TOPE - 15 + k)
        R(l, 'la-marco', m - 1, m + 1, TOPE - 12, TOPE - 6)
        R(l, 'la-vidrio', m - 0.75, m + 0.75, TOPE - 11, TOPE - 6)

    # Primer piso y planta baja de piedra almohadillada, con la cornisa gruesa arriba.
    R(l, 'la-piedra', 11, 50, 192, BASE)
    almohadillado(l, 11, 50, 196, BASE)
    R(l, 'la-piedra-c', 10, 50, 192, 194)
    R(l, 'la-piedra-o', 10, 50, 194, 195)
    for a, b in BAHIAS:
        m, w = (a + b) / 2, b - a
        for x0, x1 in ((a + w * 0.18, m - 0.5), (m + 0.5, b - w * 0.18)):
            ventana(l, x0, x1, 198, 209, 'recta')
            cm = (x0 + x1) / 2                                      # cabeza con dovelas y clave
            R(l, 'la-piedra-c', x0 - 0.75, x1 + 0.75, 196, 197)
            R(l, 'la-piedra-c', cm - 0.5, cm + 0.5, 195, 197)
            R(l, 'la-piedra-o', x0 - 0.75, x1 + 0.75, 210, 211)      # repisa con su sombra
        R(l, 'la-piedra-c', a + 0.5, b - 0.5, 211, 212)              # faja del primer piso
        R(l, 'la-piedra-o', a + 0.5, b - 0.5, 212, 213)
        ventana(l, a + 1.75, b - 1.75, 217, 226, 'arco')            # vidrieras grandes de abajo
        for k, d in enumerate((0.6, 0.85, 1)):                      # arco de dovelas alrededor
            R(l, 'la-piedra-o', m - (w / 2 - 1.25) * d, m + (w / 2 - 1.25) * d, 213 + k, 214 + k)
        R(l, 'la-piedra-c', m - 0.5, m + 0.5, 212, 215)              # clave
        R(l, 'la-zocalo', a, b, 226, BASE)                           # zócalo de granito
        R(l, 'la-zocalo-c', a, b, 226, 227)
        R(l, 'la-hierro', m - 2, m + 2, 227, 229)                    # rejilla del sótano
        for xx in range(int((m - 1.75) * 4), int((m + 1.75) * 4), 3):
            R(l, 'la-zocalo', xx / 4, xx / 4 + 0.25, 227, 229)
    for a, b in BAHIAS:                                              # pilares almohadillados entre tramos
        R(l, 'la-piedra', b - 1, b + 1, 196, 226)
        for f in range(196, 226, 3):
            R(l, 'la-piedra-o', b - 1, b + 1, f + 2, f + 3)
            R(l, 'la-piedra-c', b - 1, b - 0.75, f, f + 2)

    # Torreones al lado de la torre, sobre la baranda: dos pisos de ventanitas y su remate.
    R(l, 'la-piedra', 11, 17, 70, TOPE + 2)
    R(l, 'la-piedra-o', 16.5, 17, 70, TOPE + 2)
    R(l, 'la-piedra-c', 11, 11.5, 70, TOPE + 2)                       # pilastras de las esquinas
    R(l, 'la-piedra-c', 16, 16.5, 70, TOPE + 2)
    for f in range(70, TOPE + 2, 2):                                   # sillares de las esquinas, alternados
        w = 1.25 if (f // 2) % 2 else 0.75
        R(l, 'la-piedra-c', 11, 11 + w, f, f + 1)
        R(l, 'la-piedra-c', 17 - w, 17, f, f + 1)
        R(l, 'la-piedra-o', 11, 17, f + 1, f + 2) if False else None
    for f in (74, 83):
        ventana(l, 12.75, 15.25, f, f + 5, 'recta')
        for k, hw in enumerate((0.75, 1.5)):                            # frontis chiquito
            R(l, 'la-piedra-c', 14 - hw, 14 + hw, f - 3 + k, f - 2 + k)
    R(l, 'la-piedra-c', 11, 17, 80, 81)                                 # faja entre los dos pisos
    R(l, 'la-piedra-o', 11, 17, 81, 82)
    R(l, 'la-piedra-c', 10.5, 17.5, 68, 70)                          # cornisita
    for k in range(6):                                              # remate en pirámide y bola
        R(l, 'la-piedra', 14 - (k + 1) * 0.5, 14 + (k + 1) * 0.5, 62 + k, 63 + k)
    R(l, 'la-piedra-c', 13.75, 14.25, 59, 60)
    R(l, 'la-piedra-c', 13.5, 14.5, 60, 62)

    # Torre: fuste de la ochava (cara del frente y dos caras en sesgo), de la cornisa del primer piso a TOPE.
    R(l, 'la-piedra-m', 7, 11, 69, BASE)                            # caras en sesgo
    C(l, 'la-piedra', -7, 7, 69, BASE)
    for f in range(72, 192, 4):                                     # juntas de la terracota
        C(l, 'la-piedra-o', -7, 7, f, f + 1)
        R(l, 'la-piedra-o', 7, 11, f, f + 1)
    C(l, 'la-piedra-c', -7, -6.5, 69, BASE)                          # aristas con luz
    R(l, 'la-piedra-o', 10.75, 11, 69, BASE)
    for i, (f0, f1, tipo) in enumerate(PISOS + [(179, 191, 'recta')][:0]):
        ventana(l, -2, 2, f0 + 3, f1 - 1, 'arco' if tipo == 'arco' else 'recta', pintar=C)
        if tipo == 'recta': frontis(l, 0, 3, f0 + 2, i % 2 == 0)
        ventana(l, 8.25, 9.75, f0 + 3, f1 - 1, 'recta')             # ventana angosta en cada sesgo
        C(l, 'la-piedra-c', -7.5, 7.5, f1, f1 + 1)                   # faja por piso
        R(l, 'la-piedra-c', 7, 11, f1, f1 + 1)
    # Primer piso y puerta de la ochava: arco de medio punto con clave tallada y el cartel.
    almohadillado(l, -7, 7, 196, BASE, cara=C)
    ventana(l, -2, 2, 198, 209, 'recta', pintar=C)
    frontis(l, 0, 3.5, 197, True)
    C(l, 'la-piedra-c', -7.5, 7.5, 192, 194)
    for k, d in enumerate((0.5, 0.8, 0.95, 1)):
        C(l, 'la-piedra-c', -3.5 * d - 0.75, 3.5 * d + 0.75, 213 + k, 214 + k)
        C(l, 'la-puerta', -3.5 * d, 3.5 * d, 214 + k, 215 + k)
    C(l, 'la-puerta', -3.5, 3.5, 217, BASE)
    C(l, 'la-puerta-c', -0.25, 0.25, 218, BASE)
    for x in (-1.5, 0, 1.5):                                         # abanico de la puerta
        C(l, 'la-oro', x - 0.125, x + 0.125, 215, 217)
    C(l, 'la-oro', -2.5, 2.5, 217, 218)
    for f in (221, 226):                                             # tableros de las dos hojas
        for x0 in (-3, 0.5):
            C(l, 'la-puerta-c', x0, x0 + 2.5, f, f + 1)
            C(l, 'la-puerta-c', x0, x0 + 0.25, f, f + 4)
            C(l, 'la-puerta-c', x0 + 2.25, x0 + 2.5, f, f + 4)
    for s in (-1, 1):                                                # pilastras con capitel
        C(l, 'la-piedra-c', s * 5 - 0.75, s * 5 + 0.75, 213, BASE)
        C(l, 'la-piedra-o', s * 5 + 0.5, s * 5 + 0.75, 213, BASE)
        C(l, 'la-piedra-c', s * 5 - 1.25, s * 5 + 1.25, 212, 213)
    C(l, 'la-piedra-c', -6.25, 6.25, 210, 212)                       # entablamento con el cartel
    C(l, 'la-cartel', -3.5, 3.5, 210, 212)
    for x in range(-12, 12, 2):
        C(l, 'la-oro', x / 4, x / 4 + 0.25, 211, 212)                # letras de LANCASTER HOUSE
    C(l, 'la-piedra-c', -0.75, 0.75, 212, 214)                       # clave
    ventana(l, 8.25, 9.75, 199, 209, 'recta')
    ventana(l, 8.25, 9.75, 216, 227, 'recta')

    # Cuerpo cuadrado sobre la cornisa: dos pisos de ventanitas con frontis.
    C(l, 'la-piedra-c', -12, 12, 67, 70)
    C(l, 'la-piedra-o', -11, 11, 70, 71)
    for f0 in (72, 80):
        ventana(l, -1.75, 1.75, f0 + 1, f0 + 6, 'recta', pintar=C)
        frontis(l, 0, 2.75, f0, f0 == 80)
    # Cuerpo ochavado almohadillado con arcos altos y pilastras.
    C(l, 'la-piedra', -8, 8, 46, 67)
    R(l, 'la-piedra-m', 5.5, 8, 46, 67)
    almohadillado(l, -8, 8, 47, 67, cara=C)
    for m in (-4.25, 0, 4.25):
        w = 1.25 if m else 1.5
        C(l, 'la-telar', m - w, m + w, 52, 64)
        for k, d in enumerate((0.5, 0.85, 1)):
            C(l, 'la-telar', m - w * d, m + w * d, 49 + k, 50 + k)
        C(l, 'la-vidrio', m - w + 0.25, m + w - 0.25, 52, 63)
        for f in range(53, 63, 2):
            C(l, 'la-telar', m - w + 0.25, m + w - 0.25, f, f + 1)    # persianas
        C(l, 'la-piedra-c', m - w - 0.5, m + w + 0.5, 64, 65)
    for x in (-8, -6.25, 6.25, 8):
        C(l, 'la-piedra-c', x - 0.25 if x < 0 else x - 0.5, x + 0.5 if x < 0 else x + 0.25, 46, 67)   # pilastras
    # Balcón con ménsulas.
    C(l, 'la-piedra-c', -10, 10, 42, 44)
    C(l, 'la-piedra-o', -10, 10, 44, 45)
    for x in range(-9, 10, 2):
        C(l, 'la-piedra', x - 0.25, x + 0.25, 45, 47)
    for x in range(-9, 10):
        C(l, 'la-hierro', x, x + 0.25, 39, 42)
    C(l, 'la-hierro', -9.5, 9.5, 38, 39)
    # Cuerpo de las volutas con el nicho.
    C(l, 'la-piedra', -6.5, 6.5, 24, 42)
    R(l, 'la-piedra-m', 4.5, 6.5, 24, 42)
    for s in (-1, 1):                                               # volutas: consolas que se abren hacia abajo
        for k, w in enumerate((0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 2.75, 2.5)):
            a, b = 6.5, 6.5 + w
            C(l, 'la-piedra', -b if s < 0 else a, -a if s < 0 else b, 30 + k, 31 + k)
            e = (b - 0.25) * s                                      # canto claro de la consola
            C(l, 'la-piedra-c', min(e, e + 0.25 * s), max(e, e + 0.25 * s), 30 + k, 31 + k)
        for f, d in ((38, 8.25), (39, 8), (40, 8.25)):              # el ojo de la voluta
            C(l, 'la-piedra-o', s * d - 0.25, s * d + 0.25, f, f + 1)
    C(l, 'la-telar', -2, 2, 28, 40)                                  # nicho en arco
    for k, d in enumerate((0.5, 0.85)):
        C(l, 'la-telar', -2 * d, 2 * d, 26 + k, 27 + k)
    C(l, 'la-vidrio', -1.5, 1.5, 29, 39)
    C(l, 'la-piedra-c', -0.25, 0.25, 25, 27)
    for f in range(27, 41, 3):
        C(l, 'la-piedra-o', -6.5, -2.5, f, f + 1)
        C(l, 'la-piedra-o', 2.5, 6.5, f, f + 1)
    C(l, 'la-piedra-c', -7.5, 7.5, 22, 24)                           # cornisa de la linterna
    # Linterna de columnitas con arcos y la cúpula con la punta.
    C(l, 'la-piedra-o', -5, 5, 12, 22)
    for x in (-4.5, -2.25, 0, 2.25, 4.5):
        C(l, 'la-piedra', x - 0.5, x + 0.5, 12, 22)
    for x in (-3.375, -1.125, 1.125, 3.375):
        C(l, 'la-piedra', x - 1.125, x + 1.125, 12, 13)
        C(l, 'la-piedra', x - 1.125, x - 0.5, 13, 14)
        C(l, 'la-piedra', x + 0.5, x + 1.125, 13, 14)
    C(l, 'la-piedra-c', -5.5, 5.5, 11, 12)
    for k, hw in enumerate((1.5, 2.75, 3.75, 4.5, 5, 5.25)):
        C(l, 'la-piedra', -hw, hw, 5 + k, 6 + k)
        C(l, 'la-piedra-c', -hw, -hw + 1, 5 + k, 6 + k)
    C(l, 'la-piedra-c', -0.75, 0.75, 3, 5)
    C(l, 'la-hierro', -0.25, 0.25, 0, 3)

    # Vereda, faroles y el semáforo de la esquina.
    l.rect('la-vereda', 0, LARGO, BASE, FILAS)
    l.rect('la-vereda-o', 0, LARGO, BASE + 2, BASE + 3)
    for x in range(0, LARGO * 4, 24):
        l.rect('la-vereda-o', x / 4, x / 4 + 0.25, BASE + 3, FILAS)
    l.rect('la-cordon', 0, LARGO, FILAS - 1, FILAS)
    for s in (-1, 1):
        x = CX + s * 25.75
        l.rect('la-hierro', x - 0.25, x + 0.25, BASE - 22, BASE)
        l.rect('la-hierro', x - 0.75, x + 0.75, BASE - 2, BASE)
        l.rect('la-hierro', x - 0.5, x + 0.5, BASE - 24, BASE - 22)
        l.rect('la-farol', x - 0.75, x + 0.75, BASE - 27, BASE - 24)
        l.rect('la-hierro', x - 1, x + 1, BASE - 28, BASE - 27)
        x = CX + s * 10
        l.rect('la-hierro', x - 0.25, x + 0.25, BASE - 15, BASE)
        l.rect('la-semaforo', x - 0.75, x + 0.75, BASE - 21, BASE - 15)
        for f, c in ((BASE - 20, 'la-luz-r'), (BASE - 18, 'la-luz-a'), (BASE - 16, 'la-luz-v')):
            l.rect(c if c == 'la-luz-v' else 'la-semaforo-o', x - 0.25, x + 0.25, f, f + 1)
    return {'nota': 'Lancaster House, en Manchester: la torre de la esquina con su cúpula, linterna de columnitas, '
                    'volutas y balcón, y las dos fachadas de ladrillo rojo con fajas de terracota ocre, ventanas '
                    'en arco y óculos arriba, sobre la planta baja de piedra almohadillada.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

def oscurecer(h, k=0.93):
    return '#' + ''.join(f'{round(int(h[i:i + 2], 16) * k):02x}' for i in (1, 3, 5))

BASICOS = {
    'la-piedra': '#c08a60', 'la-piedra-c': '#cf9c72', 'la-piedra-o': '#a9774f', 'la-piedra-m': '#b58058',
    'la-ladrillo': '#b2634f', 'la-ladrillo-o': '#a65946', 'la-telar': '#8e4a3a',
    'la-marco': '#e4dccd', 'la-vidrio': '#3a3e45', 'la-pizarra': '#7a7470', 'la-pizarra-c': '#8e8782',
    'la-zocalo': '#9a7a62', 'la-zocalo-c': '#ad8c72', 'la-cartel': '#4a3a30',
    'la-puerta': '#2d2420', 'la-puerta-c': '#4a3c33', 'la-oro': '#c9a45a', 'la-hierro': '#262626',
}
COLORES = {k: (v, v) for k, v in BASICOS.items()}
COLORES.update({k + '-s': (oscurecer(v), oscurecer(v)) for k, v in BASICOS.items()
                if k not in ('la-hierro', 'la-puerta', 'la-oro')})
COLORES.update({
    'la-farol': ('#f1e3b5', '#f1e3b5'), 'la-semaforo': ('#2f3a2f', '#2f3a2f'), 'la-semaforo-o': ('#1c221c', '#1c221c'),
    'la-luz-v': ('#5fd08a', '#5fd08a'), 'la-luz-r': ('#d84a3a', '#d84a3a'), 'la-luz-a': ('#e6b440', '#e6b440'),
    'la-vereda': ('#b9b4ab', '#76726c'), 'la-vereda-o': ('#9a958b', '#5c5954'), 'la-cordon': ('#8a857c', '#4d4a46'),
    'eduardiano-fondo': ('#d9dccf', '#3a3d36'),
})

p = version()
p.update(placa='eduardiano-fondo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10)
guardar(sys.argv[1], 'estilos', 'Barroco eduardiano', p, COLORES, 'la-|eduardiano-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
