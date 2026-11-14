# Alwyn Court (Harde & Short, Nueva York), de frente a la esquina, simétrico: medido sobre
# referencias/simbolos/neorenacimiernto frances/images.jpeg (la esquina, los 12 pisos y las bandas) y
# IMG_0276a_resize.jpg (pilares con rombos y cartelas coronadas, cabezales con salamandras, columnitas talladas,
# cortinas, la balaustrada sobre la planta baja, toldos, zócalo con paneles, la marquesina de la puerta).
# Para que se lea la esquina: los tramos se angostan al alejarse, el lado derecho queda en sombra (colores -s)
# y la vereda baja en V hacia el cordón de la esquina, con el poste del semáforo. Luz desde la izquierda.
# Uso: alwyn.py <simbolos.json> (pone estilos."Renacimiento francés").
import sys
from armar import Lienzo, guardar

LARGO = 150
CX = 75
ESQ = 26
# Un lado, del borde a la esquina: los tramos lejanos más angostos (se ven de costado).
LADO = [('pilar', 5.5), ('tramo', 19.5), ('pilar', 6.5), ('tramo', 22), ('pilar', 7.5)]
PISO, VIDRIO = 13, 8                      # filas por piso y de ventana (el resto, antepecho tallado)
CORNISA, BAJA, CALLE = 15, 18, 6
BANDAS = {10: 'friso', 5: 'balaustrada', 3: 'balcon'}   # banda bajo esos pisos
CABEZALES = (12, 9)                       # pisos con cabezal de salamandras bajo las ventanas
FILAS = CORNISA + 11 * PISO + 3 * 3 + BAJA + CALLE

def q(x): return round(x * 4) / 4

MARGEN = 1                                # la cornisa vuela 1 unidad sobre el cuerpo a cada lado

def partes():
    x, izq = MARGEN, []
    for t, w in LADO:
        izq.append((x, x + w, t)); x += w
    der = [(LARGO - b, LARGO - a, t) for a, b, t in reversed(izq)]
    return izq + [(CX - ESQ / 2, CX + ESQ / 2, 'esquina')] + der

def ventanas(a, b):
    # Tres ventanas en el tramo a–b, simétricas sobre su eje. En la esquina las de los costados son más angostas.
    cx, w = (a + b) / 2, b - a
    if w == ESQ:
        return [(cx - 8.75, cx - 5.25), (cx - 2.5, cx + 2.5), (cx + 5.25, cx + 8.75)]
    v, e = q(w * 0.215), q(w * 0.09)
    m = v / 2 + e + v / 2
    return [(cx - m - v / 2, cx - m + v / 2), (cx - v / 2, cx + v / 2), (cx + m - v / 2, cx + m + v / 2)]

# ── piezas ──────────────────────────────────────────────────────────────────────────────

def rombo(l, a, b, f0, alto):
    # Panel del pilar, simétrico: marco parejo, rombo de tres anillos (borde claro, faja tallada, centro claro)
    # con la medalla en el medio, y hojitas en los cuatro rincones.
    cx = (a + b) / 2
    l.rect('al-ornato-o', a + 0.5, b - 0.5, f0, f0 + alto)
    l.rect('al-ornato', a + 0.75, b - 0.75, f0, f0 + alto)
    ancho = q((b - a) / 2 - 0.75)
    m = alto // 2                                                         # alto impar: fila del medio exacta
    for k in range(alto):
        w = q(ancho * (m + 0.5 - abs(k - m)) / (m + 0.5))
        f = f0 + k
        if w >= 0.25: l.rect('al-cornisa', cx - w, cx + w, f, f + 1)
        if w >= 1: l.rect('al-ornato-o', cx - w + 0.5, cx + w - 0.5, f, f + 1)
        if w >= 1.5: l.rect('al-piedra-c', cx - w + 0.75, cx + w - 0.75, f, f + 1)
    l.rect('al-cornisa', cx - 0.5, cx + 0.5, f0 + m - 1, f0 + m + 2)          # medalla
    l.rect('al-ornato-o', cx - 0.25, cx + 0.25, f0 + m, f0 + m + 1)
    for f in (f0 + 1, f0 + alto - 2):                                     # hojitas de los rincones
        l.rect('al-cornisa', a + 1, a + 1.5, f, f + 1)
        l.rect('al-cornisa', b - 1.5, b - 1, f, f + 1)

def ventana(l, x0, x1, f, n):
    # Guillotina de dos hojas, todas iguales: marco blanco con su dintel, vidrios con un reflejo, el riel
    # del medio; alféizar y sombra a la derecha.
    l.rect('al-ornato-o', x0 - 0.25, x1 + 0.25, f - 1, f)                 # dintel
    l.rect('al-marco', x0, x1, f, f + VIDRIO)
    l.rect('al-vidrio', x0 + 0.5, x1 - 0.5, f + 1, f + 4)
    l.rect('al-vidrio', x0 + 0.5, x1 - 0.5, f + 5, f + VIDRIO)
    if x1 - x0 >= 4:                                                      # reflejo, solo en las anchas
        l.rect('al-vidrio-l', x0 + 0.5, x0 + 0.75, f + 1, f + 3)
        l.rect('al-vidrio-l', x0 + 0.5, x0 + 0.75, f + 5, f + 7)
    l.rect('al-sombra', x1, x1 + 0.25, f, f + VIDRIO)
    l.rect('al-cornisa', x0 - 0.25, x1 + 0.25, f + VIDRIO, f + VIDRIO + 1)

def columnita(l, a, b, f0, f1):
    # Parteluz tallado: capitel, fuste con anillos, basa.
    if b - a <= 0: return
    l.rect('al-ornato', a, b, f0, f1)
    for f in range(f0 + 1, f1, 2):
        l.rect('al-ornato-o', a, b, f, f + 1)
    l.rect('al-cornisa', a - 0.25, b + 0.25, f0, f0 + 1)
    l.rect('al-cornisa', a - 0.25, b + 0.25, f1 - 1, f1)

def antepecho(l, a, b, f, vs):
    # Bajo cada ventana un panel enmarcado y simétrico: marco claro, fondo tallado, medalla oval en el medio
    # y dos rosetas iguales a los lados; entre paneles, un dado con su roseta.
    l.rect('al-ornato-o', a + 0.5, b - 0.5, f, f + 4)
    for x0, x1 in vs:
        cx = (x0 + x1) / 2
        l.rect('al-cornisa', x0, x1, f, f + 4)                            # marco
        l.rect('al-ornato', x0 + 0.25, x1 - 0.25, f + 1, f + 3)
        l.rect('al-cornisa', cx - 0.75, cx + 0.75, f + 1, f + 3)          # medalla oval
        l.rect('al-ornato-o', cx - 0.25, cx + 0.25, f + 1, f + 3)
        d = q((x1 - x0) / 4 + 0.25)                                       # dos rosetas iguales a los lados
        if d >= 1.25:
            for s in (-1, 1):
                l.rect('al-cornisa', cx + s * d - 0.25, cx + s * d + 0.25, f + 1, f + 3)
    for (_, x1), (y0, _) in zip(vs, vs[1:]):
        m = (x1 + y0) / 2
        l.rect('al-cornisa', m - 0.5, m + 0.5, f + 1, f + 3)
        l.rect('al-ornato-o', m - 0.25, m + 0.25, f + 1, f + 3)

def cabezal(l, a, b, f):
    # Cabezal que vuela sobre el tramo, con las dos salamandras en las puntas y la medalla del medio.
    cx = (a + b) / 2
    l.rect('al-cornisa', a + 0.5, b - 0.5, f, f + 1)
    l.rect('al-ornato', a + 1, b - 1, f + 1, f + 3)
    for k in range(int((b - a - 4) / 2)):
        l.rect('al-cornisa', a + 2 + k * 2, a + 2.5 + k * 2, f + 2, f + 3)
    l.rect('al-cornisa', cx - 1.25, cx + 1.25, f + 1, f + 3)
    l.rect('al-ornato-o', cx - 0.5, cx + 0.5, f + 2, f + 3)
    l.rect('al-cornisa', a + 0.5, b - 0.5, f + 3, f + 4)
    l.rect('al-sombra', a + 1, b - 1, f + 4, f + 5)
    for x, s in ((a + 0.5, 1), (b - 0.5, -1)):                            # salamandras
        x0, x1 = sorted((x, x + s * 2))
        l.rect('al-salamandra', x0, x1, f + 1, f + 3)
        x0, x1 = sorted((x + s * 0.5, x + s * 1.5))
        l.rect('al-salamandra', x0, x1, f + 3, f + 6)
        x0, x1 = sorted((x + s * 1.5, x + s * 2.5))
        l.rect('al-salamandra', x0, x1, f, f + 1)
    for k in (-3, 3):                                                     # colgantes
        l.rect('al-ornato-o', cx + k - 0.25, cx + k + 0.25, f + 4, f + 6)

def cartela(l, cx, f):
    # Cartela coronada en la cabeza del pilar: corona, escudo con borde, volutas y el colgante abajo.
    for d in (-1.5, 0, 1.5):
        l.rect('al-cornisa', cx + d - 0.25, cx + d + 0.25, f, f + 1)
    l.rect('al-cornisa', cx - 2, cx + 2, f + 1, f + 2)
    l.rect('al-ornato-o', cx - 2, cx + 2, f + 2, f + 3)
    l.rect('al-cornisa', cx - 2.5, cx + 2.5, f + 3, f + 7)
    l.rect('al-ornato', cx - 1.5, cx + 1.5, f + 3, f + 7)
    l.rect('al-cornisa', cx - 1, cx + 1, f + 4, f + 6)
    l.rect('al-ornato-o', cx - 0.25, cx + 0.25, f + 4, f + 6)
    l.rect('al-cornisa', cx - 1.5, cx + 1.5, f + 7, f + 8)
    l.rect('al-cornisa', cx - 0.75, cx + 0.75, f + 8, f + 9)
    l.rect('al-ornato-o', cx - 0.25, cx + 0.25, f + 9, f + 12)
    l.rect('al-cornisa', cx - 0.5, cx + 0.5, f + 11, f + 12)
    for s in (-1, 1):                                                     # volutas
        x0, x1 = sorted((cx + s * 2.5, cx + s * 3.25))
        l.rect('al-ornato-o', x0, x1, f + 4, f + 6)

# ── partes del edificio ─────────────────────────────────────────────────────────────────

def piso(l, f, n):
    for a, b, t in partes():
        if t == 'pilar':
            rombo(l, a, b, f, PISO)
            continue
        vs = ventanas(a, b)
        for x0, x1 in vs: ventana(l, x0, x1, f, n)
        for (_, x1), (y0, _) in zip(vs, vs[1:]):
            columnita(l, x1 + 0.5, y0 - 0.5, f, f + VIDRIO)
        columnita(l, a + 0.5, vs[0][0] - 0.5, f, f + VIDRIO)
        columnita(l, vs[-1][1] + 0.5, b - 0.5, f, f + VIDRIO)
        antepecho(l, a, b, f + VIDRIO + 1, vs)
        if n in CABEZALES:
            if t == 'tramo': cabezal(l, a, b, f + VIDRIO + 1)
            else: balconcito(l, f + VIDRIO + 1)
    esquina_redonda(l, f, f + PISO)

def balconcito(l, f):
    a, b = CX - ESQ / 2 + 3, CX + ESQ / 2 - 3
    l.rect('al-cornisa', a, b, f, f + 1)
    l.rect('al-sombra', a, b, f + 1, f + 3)
    for k in range(int((b - a) / 1.25)):
        l.rect('al-balaustre', a + 0.25 + k * 1.25, a + 0.75 + k * 1.25, f + 1, f + 3)
        l.rect('al-balaustre', a + k * 1.25, a + 1 + k * 1.25, f + 2, f + 3)
    l.rect('al-cornisa', a - 0.5, b + 0.5, f + 3, f + 4)
    for k in range(int((b - a) / 2)):
        l.rect('al-ornato-o', a + 0.5 + k * 2, a + 1.25 + k * 2, f + 4, f + 5)   # ménsulas

def esquina_redonda(l, f0, f1):
    # La esquina es una torre redonda: canto claro a la izquierda, se oscurece hacia la derecha.
    a, b = CX - ESQ / 2, CX + ESQ / 2
    l.rect('al-cornisa', a, a + 0.75, f0, f1)
    l.rect('al-piedra-c', a + 0.75, a + 1.75, f0, f1)
    l.rect('al-piedra-s', b - 2.5, b - 1.5, f0, f1)
    l.rect('al-ornato-o', b - 1.5, b - 0.75, f0, f1)
    l.rect('al-sombra', b - 0.75, b, f0, f1)

def banda(l, f, tipo):
    # 4 filas bajo un piso (la primera pisa el antepecho).
    l.rect('al-cornisa', 0, LARGO, f, f + 1)
    for a, b, t in partes():
        if t == 'pilar':                                                  # dado macizo sobre el pilar
            cx = (a + b) / 2
            l.rect('al-cornisa', a + 0.25, b - 0.25, f + 1, f + 3)
            l.rect('al-ornato', a + 0.75, b - 0.75, f + 1, f + 3)
            l.rect('al-cornisa', cx - 0.5, cx + 0.5, f + 1, f + 3)
            l.rect('al-ornato-o', cx - 0.25, cx + 0.25, f + 1, f + 3)
        elif tipo == 'friso':                                             # roleos centrados en el tramo
            l.rect('al-ornato', a, b, f + 1, f + 3)
            n = int((b - a) / 3)
            x0 = a + q(((b - a) - n * 3) / 2)
            for k in range(n):
                x = x0 + k * 3
                l.rect('al-cornisa', x + 0.5, x + 1, f + 1, f + 2)
                l.rect('al-cornisa', x + 1, x + 2, f + 2, f + 3)
                l.rect('al-cornisa', x + 2, x + 2.5, f + 1, f + 2)
                l.rect('al-ornato-o', x + 1.25, x + 1.75, f + 1, f + 2)
        else:                                                             # balaustres centrados en el tramo
            l.rect('al-sombra', a, b, f + 1, f + 3)
            n = int((b - a - 0.5) / 1.25)
            x0 = a + q(((b - a) - (n - 1) * 1.25 - 1) / 2)
            for k in range(n):
                x = x0 + k * 1.25
                l.rect('al-balaustre', x + 0.25, x + 0.75, f + 1, f + 2)
                l.rect('al-balaustre', x, x + 1, f + 2, f + 3)
    l.rect('al-cornisa', 0, LARGO, f + 3, f + 4)
    l.rect('al-ornato-o', 0, LARGO, f + 4, f + 5)
    if tipo == 'balcon':
        # El balcón curvo de la esquina, como en la foto: vuela más ancho, baranda de paneles tallados con una
        # cartela redonda entre postecitos, moldura gruesa y ménsulas de hojas con sus colgantes.
        a, b = CX - ESQ / 2 - 2.5, CX + ESQ / 2 + 2.5
        l.rect('al-cornisa', a - 0.5, b + 0.5, f - 2, f - 1)              # pasamanos
        l.rect('al-ornato-o', a, b, f - 1, f + 3)
        n = int((b - a) / 2.5)
        x = a + ((b - a) - n * 2.5) / 2
        for k in range(n + 1):
            l.rect('al-cornisa', x + k * 2.5 - 0.25, x + k * 2.5 + 0.25, f - 1, f + 3)   # postecitos
        for k in range(n):
            m = x + k * 2.5 + 1.25
            l.rect('al-ornato', m - 1, m + 1, f - 1, f + 3)
            l.rect('al-cornisa', m - 0.5, m + 0.5, f - 1, f)              # cartela redonda
            l.rect('al-cornisa', m - 0.75, m - 0.5, f, f + 2)
            l.rect('al-cornisa', m + 0.5, m + 0.75, f, f + 2)
            l.rect('al-cornisa', m - 0.5, m + 0.5, f + 2, f + 3)
            l.rect('al-ornato-o', m - 0.25, m + 0.25, f + 1, f + 2)
        l.rect('al-cornisa', a - 0.5, b + 0.5, f + 3, f + 4)              # moldura gruesa
        l.rect('al-ornato', a - 0.25, b + 0.25, f + 4, f + 5)
        for k in range(int((b - a) / 0.75)):
            l.rect('al-cornisa', a + k * 0.75, a + k * 0.75 + 0.25, f + 4, f + 5)
        for k in range(n + 1):                                            # ménsulas con colgante
            m = x + k * 2.5
            l.rect('al-cornisa', m - 0.5, m + 0.5, f + 5, f + 6)
            l.rect('al-ornato', m - 0.25, m + 0.25, f + 6, f + 7)
            l.rect('al-ornato-o', m - 0.25, m + 0.25, f + 7, f + 8)

def cornisa(l):
    l.rect('al-cornisa', 0, LARGO, 0, 2)
    l.rect('al-ornato', 0, LARGO, 2, 3)
    for k in range(int(LARGO / 1.5)):                                     # óvalos y dardos
        l.rect('al-cornisa', k * 1.5 + 0.5, k * 1.5 + 1, 3, 4)
    l.rect('al-sombra', 0, LARGO, 4, 5)
    l.rect('al-ornato-o', 0, LARGO, 5, 8)
    for k in range(int(LARGO / 3)):                                       # ménsulas de dos tonos
        x = k * 3 + 0.75
        l.rect('al-cornisa', x, x + 1.5, 5, 6)
        l.rect('al-ornato', x + 0.25, x + 1.25, 6, 8)
        l.rect('al-cornisa', x + 0.5, x + 1, 7, 8)
        l.rect('al-sombra', x + 1.5, x + 1.75, 5, 8)
    for k in range(int(LARGO)):                                           # dentículos
        l.rect('al-cornisa', k + 0.25, k + 0.75, 8, 9)
    l.rect('al-cornisa', 0, LARGO, 9, 10)
    l.rect('al-ornato', 0, LARGO, 10, CORNISA - 1)                        # friso de hojas
    for k in range(int(LARGO / 2.5)):
        x = k * 2.5
        l.rect('al-ornato-o', x + 0.5, x + 1, 11, 13)
        l.rect('al-cornisa', x + 1.5, x + 2, 12, 13)
    l.rect('al-sombra', 0, LARGO, CORNISA - 1, CORNISA)
    for a, b, t in partes():
        if t == 'pilar': cartela(l, (a + b) / 2, 9)

def planta_baja(l, f):
    l.rect('al-piedra', 0, LARGO, f, f + BAJA)
    l.rect('al-cornisa', 0, LARGO, f, f + 1)
    l.rect('al-ornato', 0, LARGO, f + 1, f + 2)
    for a, b, t in partes():                                              # perlas centradas en cada tramo
        n = int((b - a) / 2)
        x0 = a + q(((b - a) - n * 2) / 2)
        for k in range(n):
            l.rect('al-ornato-o', x0 + k * 2 + 0.75, x0 + k * 2 + 1.25, f + 1, f + 2)
    for a, b, t in partes():
        if t == 'tramo':
            for x0, x1 in ventanas(a, b):
                cx = (x0 + x1) / 2
                # Toldo: frente azul y costado claro, con la faja de abajo.
                l.rect('al-toldo', x0 - 0.5, cx + 0.5, f + 3, f + 7)
                l.rect('al-toldo-b', cx + 0.5, x1 + 0.5, f + 3, f + 7)
                l.rect('al-toldo-o', x0 - 0.5, x1 + 0.5, f + 7, f + 8)
                l.rect('al-marco', x0 - 0.25, x1 + 0.25, f + 8, f + 13)
                l.rect('al-vidrio', x0 + 0.25, x1 - 0.25, f + 8, f + 12)
                l.rect('al-luz', x0 + 0.75, x0 + 1.25, f + 10, f + 11)
                l.rect('al-luz', x1 - 1.25, x1 - 0.75, f + 9, f + 10)
                l.rect('al-ornato-o', x0, x1, f + 14, f + 15)              # panel del zócalo
                l.rect('al-piedra-c', x0 + 0.25, x1 - 0.25, f + 15, f + 16)
                l.rect('al-ornato-o', x0, x1, f + 16, f + 17)
            vs = ventanas(a, b)
            for (_, x1), (y0, _) in zip(vs, vs[1:]):
                columnita(l, x1 + 0.75, y0 - 0.75, f + 2, f + 13)
        elif t == 'esquina':
            r = 4
            l.rect('al-cornisa', CX - r - 1, CX + r + 1, f + 7, f + BAJA)
            l.rect('al-puerta', CX - r, CX + r, f + 9, f + BAJA)
            for k in range(r):                                           # arco con la reja dorada iluminada
                w = q((r * r - (k + 0.5) ** 2) ** 0.5)
                l.rect('al-luz', CX - w, CX + w, f + 9 - k, f + 10 - k)
                l.rect('al-puerta', CX - w + 0.5, CX + w - 0.5, f + 9 - k, f + 10 - k)
            for x in (-2, 0, 2):
                l.rect('al-luz', CX + x - 0.25, CX + x + 0.25, f + 6, f + 9)
            l.rect('al-luz', CX - r + 0.75, CX + r - 0.75, f + 10, f + 11)
            l.rect('al-puerta-l', CX - 0.25, CX + 0.25, f + 11, f + BAJA)
            l.rect('al-luz', CX - 1, CX - 0.5, f + 13, f + 14)            # tiradores
            l.rect('al-luz', CX + 0.5, CX + 1, f + 13, f + 14)
            # Marquesina curva gris con su número y los caños de bronce.
            l.rect('al-marquesina', CX - 7, CX + 7, f + 4, f + 5)
            l.rect('al-marquesina', CX - 6, CX + 6, f + 3, f + 4)
            l.rect('al-marquesina', CX - 4.5, CX + 4.5, f + 2, f + 3)
            l.rect('al-marquesina-o', CX - 7, CX + 7, f + 5, f + 6)
            l.rect('al-cornisa', CX - 0.75, CX + 0.75, f + 3, f + 4)
            for s in (-1, 1):
                l.rect('al-bronce', CX + s * 6.75 - 0.25, CX + s * 6.75 + 0.25, f + 6, f + BAJA)
                l.rect('al-farol', CX + s * 9.5 - 0.5, CX + s * 9.5 + 0.5, f + 7, f + 10)
                l.rect('al-luz', CX + s * 9.5 - 0.25, CX + s * 9.5 + 0.25, f + 8, f + 9)
                for k, w in enumerate((0.5, 1, 1.5, 1.5, 1)):             # macetas con arbolitos
                    l.rect('al-arbusto', CX + s * 9.5 - w, CX + s * 9.5 + w, f + 9 + k, f + 10 + k)
                l.rect('al-maceta', CX + s * 9.5 - 1.25, CX + s * 9.5 + 1.25, f + 14, f + BAJA)
            esquina_redonda(l, f + 2, f + 4)
        else:
            l.rect('al-piedra-c', a + 0.5, a + 1, f + 2, f + BAJA)
            l.rect('al-sombra', b - 0.75, b - 0.25, f + 2, f + BAJA)
            l.rect('al-ornato-o', a + 1.5, b - 1.5, f + 4, f + 5)          # paneles del pilar
            l.rect('al-ornato-o', a + 1.5, b - 1.5, f + 11, f + 12)
            l.rect('al-ornato-o', a + 1.5, a + 1.75, f + 4, f + 12)
            l.rect('al-ornato-o', a + 1.5, b - 1.5, f + 14, f + 15)
            l.rect('al-ornato-o', a + 1.5, b - 1.5, f + 16, f + 17)
    l.rect('al-zocalo', 0, LARGO, f + BAJA - 1, f + BAJA)

def calle(l, f):
    # Vereda plana de baldosas (juntas simétricas desde la esquina), cordón y calle.
    l.rect('al-vereda', 0, LARGO, f, f + 3)
    for k in range(0, int(CX), 4):
        for x in (CX - k, CX + k):
            l.rect('al-vereda-o', x, x + 0.25, f, f + 3)
    l.rect('al-cordon', 0, LARGO, f + 3, f + 4)
    l.rect('al-calle', 0, LARGO, f + 4, f + CALLE)

def arbol(l, x, f_suelo, alto):
    # Árbol pelado de la vereda, simétrico: tronco y tres pares de ramas rectas que suben abriéndose.
    l.rect('al-arbol', x - 0.25, x + 0.25, f_suelo - alto, f_suelo)
    for f_rama, largo in ((f_suelo - alto + 12, 5), (f_suelo - alto + 7, 4), (f_suelo - alto + 3, 3)):
        for k in range(largo):
            for s in (-1, 1):
                d = 0.25 + k * 0.5
                xa, xb = sorted((x + s * d, x + s * (d + 0.5)))
                l.rect('al-arbol', xa, xb, f_rama - k, f_rama - k + 1)
    l.rect('al-cantero', x - 1, x + 1, f_suelo, f_suelo + 1)

def semaforo(l, x, f_suelo):
    l.rect('al-poste', x - 0.25, x + 0.25, f_suelo - 20, f_suelo + 2)
    l.rect('al-poste', x - 0.5, x + 0.5, f_suelo + 1, f_suelo + 2)
    l.rect('al-semaforo', x + 0.25, x + 1.5, f_suelo - 17, f_suelo - 12)
    l.rect('al-rojo', x + 0.5, x + 1.25, f_suelo - 16, f_suelo - 15)
    l.rect('al-verde', x + 0.5, x + 1.25, f_suelo - 14, f_suelo - 13)
    l.rect('al-poste', x - 4, x, f_suelo - 20, f_suelo - 19)              # brazo del farol
    l.rect('al-luz', x - 4.5, x - 3, f_suelo - 19, f_suelo - 18)

SOMBREABLES = {'al-piedra', 'al-piedra-c', 'al-piedra-s', 'al-ornato', 'al-ornato-o', 'al-cornisa', 'al-balaustre',
               'al-marco', 'al-zocalo', 'al-sombra', 'al-salamandra'}

def espejo(l, f_fin):
    # Simetría exacta: la cornisa entera y, en el resto, todo lo que está fuera de la torre de la esquina
    # se copia del lado izquierdo al derecho (la torre conserva su luz de un lado).
    n = len(l.c[0])
    for r, fila in enumerate(l.c[:f_fin]):
        hasta = n // 2 if r < CORNISA else round((CX - ESQ / 2) * 4)
        for i in range(hasta):
            fila[n - 1 - i] = fila[i]

def sombra_lado(l):
    # El lado derecho mira a la sombra. Sin corte brusco: la mitad derecha de la torre redonda pasa a media
    # sombra (-m) y desde ahí el lado entero queda en sombra suave (-s).
    medio, fin = round(CX * 4), round((CX + ESQ / 2) * 4)
    for fila in l.c:
        for i in range(medio, len(fila)):
            if fila[i] in SOMBREABLES: fila[i] += '-m' if i < fin else '-s'

def version():
    l = Lienzo(LARGO, FILAS)
    l.rect('al-piedra', 0, LARGO, 0, FILAS - CALLE)
    f = CORNISA
    for n in range(12, 1, -1):
        piso(l, f, n); f += PISO
        if n in BANDAS: banda(l, f - 1, BANDAS[n]); f += 3
    planta_baja(l, f); f += BAJA
    cornisa(l)
    # La cornisa vuela con perfil curvo: cada moldura se mete un poco más que la de arriba hasta el muro.
    perfil = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3}
    for r, fila in enumerate(l.c[:f]):
        m = perfil.get(r, MARGEN * 4)
        for i in list(range(0, m)) + list(range(len(fila) - m, len(fila))): fila[i] = '-'
    espejo(l, f)
    sombra_lado(l)
    calle(l, f)
    x = LADO[0][1] + LADO[1][1] + LADO[2][1] / 2                          # árboles frente a los pilares del medio
    arbol(l, x, f + 1, 22)
    arbol(l, LARGO - x, f + 1, 22)
    semaforo(l, CX + 12, f + 2)
    return {'nota': 'Alwyn Court, en Nueva York, de frente a la esquina: la torre redonda de la esquina con la '
                    'puerta, la marquesina, faroles y macetas; los tramos de tres ventanas entre pilares con rombos '
                    'y cartelas coronadas, columnitas talladas, antepechos con medallas, cabezales con salamandras, '
                    'la cornisa con ménsulas, el friso, las balaustradas y el balcón curvo; la planta baja con '
                    'toldos y zócalo de paneles; la vereda en V con los árboles y el semáforo. El lado derecho, en sombra.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

# La piedra es pareja y el relieve suave, como en la foto: tonos cercanos entre sí.
PIEDRA = {
    'al-piedra': '#ddd4c6', 'al-piedra-c': '#e4dccf', 'al-piedra-s': '#cfc5b5',
    'al-ornato': '#cec2b0', 'al-ornato-o': '#b9ac99', 'al-sombra': '#a69a87',
    'al-cornisa': '#e8e0d3', 'al-balaustre': '#e3dbce', 'al-salamandra': '#bfb29f',
    'al-marco': '#ece6dc', 'al-zocalo': '#b3a794',
}

def oscurecer(h, f):
    return '#' + ''.join(f'{round(int(h[i:i + 2], 16) * f):02x}' for i in (1, 3, 5))

COLORES = {}
for k, v in PIEDRA.items():
    COLORES[k] = (v, v)
    COLORES[k + '-m'] = (oscurecer(v, 0.95), oscurecer(v, 0.95))
    COLORES[k + '-s'] = (oscurecer(v, 0.89), oscurecer(v, 0.89))
COLORES.update({
    'al-vidrio': ('#2e3236', '#2e3236'), 'al-vidrio-l': ('#4a525a', '#4a525a'), 'al-cortina': ('#cfcac0', '#cfcac0'),
    'al-aire': ('#d6d6d2', '#d6d6d2'), 'al-aire-o': ('#9a9a96', '#9a9a96'),
    'al-toldo': ('#2f6c9e', '#2f6c9e'), 'al-toldo-b': ('#c9ced3', '#c9ced3'), 'al-toldo-o': ('#1f4a6e', '#1f4a6e'),
    'al-puerta': ('#3b2a20', '#3b2a20'), 'al-puerta-l': ('#6e4c35', '#6e4c35'), 'al-bronce': ('#b8954f', '#b8954f'),
    'al-marquesina': ('#6a6863', '#6a6863'), 'al-marquesina-o': ('#4a4844', '#4a4844'),
    'al-farol': ('#2f2f2c', '#2f2f2c'), 'al-luz': ('#f0cf85', '#f0cf85'),
    'al-arbusto': ('#3f5a35', '#3f5a35'), 'al-maceta': ('#cfc8bb', '#cfc8bb'),
    'al-arbol': ('#4a4038', '#4a4038'), 'al-cantero': ('#5a4a3c', '#5a4a3c'),
    'al-poste': ('#3a3d40', '#3a3d40'), 'al-semaforo': ('#2a2c2e', '#2a2c2e'),
    'al-rojo': ('#d9483b', '#d9483b'), 'al-verde': ('#3fbf7a', '#3fbf7a'),
    'al-vereda': ('#b1aca3', '#8a867f'), 'al-vereda-o': ('#99948b', '#726e68'),
    'al-cordon': ('#7d7972', '#5f5c57'), 'al-calle': ('#4a4a4a', '#333333'),
    'renac-lavanda': ('#7b6f86', '#2a2430'), 'renac-lavanda-marco': ('#849079', '#d5dbcf'),
})

p = version()
p.update(placa='renac-lavanda', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
         marco='renac-lavanda-marco')
guardar(sys.argv[1], 'estilos', 'Renacimiento francés', p, COLORES, 'al-|renac-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
