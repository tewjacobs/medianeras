# Villa Erba (Cernobbio, lago de Como), de frente desde el lago, medida en px sobre
# referencias/simbolos/italianizante/images (2).jpeg (739 de ancho); los detalles (frontis, ménsulas, la torre),
# de Villa_Erba_004.jpeg y 808acf….jpg. Tres cuerpos: a la izquierda el pabellón con el portón en arco entre
# pilastras con paneles y la ventana en arco con balcón; en el medio cuatro ventanas con frontis curvo arriba y
# cuatro puertas con frontis de volutas abajo, y el balcón central sobre ménsulas; a la derecha tres ventanas en
# arco, su balcón y la logia con columnas. Planta baja almohadillada. Encima, la cornisa de ménsulas, la balaustrada
# con jarrones y las tejas detrás; la torre mirador con esquinas de sillares, el óculo con su guirnalda, tres arcos
# entre pilastras, la cornisa de ménsulas y la terraza con jarrones. Delante: la terraza, la escalinata, los bojes,
# el muro del lago y el agua. Luz desde la izquierda: sombras a la derecha y debajo de cornisas y balcones.
# Uso: erba.py <simbolos.json> (pone estilos."Italianizante").
import sys
from armar import Lienzo, guardar

X0, X1, Y0, Y1 = 132, 560, 48, 392
LARGO = 150
S = LARGO / (X1 - X0)
FILAS = round((Y1 - Y0) * S) + 1

def U(x): return round((x - X0) * S * 4) / 4
def F(y): return round((y - Y0) * S)
def R(l, c, x0, x1, y0, y1): l.rect(c, U(x0), U(x1), F(y0), F(y1))
def q(x): return round(x * 4) / 4
def sim(l, c, cx, w, f0, f1): l.rect(c, cx - w, cx + w, f0, f1)          # rectángulo simétrico en unidades
def eje(x0, x1): return q((U(x0) + U(x1)) / 2)                           # eje de un tramo, en la grilla de 0.25

def arco(l, c, cx, r, f, f1):
    # Arco de medio punto de radio r (unidades) que arranca en la fila f y baja recto hasta f1.
    sim(l, c, cx, r, f, f1)
    for k in range(int(r + 0.5)):
        w = q((r * r - (k + 0.5) ** 2) ** 0.5)
        if w > 0: sim(l, c, cx, w, f - 1 - k, f - k)

def vano(l, cx, w, f0, f1, arcado=False, alfeizar=True, travesano=None):
    # Ventana o puerta de vidrio de medio ancho w, simétrica: marco claro, parteluz, sombra a la derecha y alféizar.
    sim(l, 'er-marco', cx, w + 0.75, f0 - (0 if arcado else 1), f1)
    if arcado:
        sim(l, 'er-marco', cx, w + 0.25, f0 - 1, f0); sim(l, 'er-marco', cx, w - 0.75, f0 - 2, f0 - 1)
        if w > 1.25: sim(l, 'er-vidrio', cx, w - 1.25, f0 - 1, f0)
        sim(l, 'er-vidrio', cx, w - 0.5, f0, f0 + 1); sim(l, 'er-vidrio', cx, w, f0 + 1, f1)
    else:
        sim(l, 'er-vidrio', cx, w, f0, f1)
    sim(l, 'er-marco', cx, 0.25, f0 + 1, f1)
    if travesano: sim(l, 'er-marco', cx, w, travesano, travesano + 1)
    l.rect('er-sombra', cx + w + 0.75, cx + w + 1.25, f0, f1)
    if alfeizar: sim(l, 'er-cornisa', cx, w + 1.25, f1, f1 + 1)

def frontis_segmento(l, cx, w, f0):
    # Frontis curvo sobre una ventana cuyo vidrio arranca en f0: cornisa, arco bajo y la venera del medio.
    sim(l, 'er-cornisa', cx, w + 1.25, f0 - 2, f0 - 1)
    sim(l, 'er-cornisa', cx, w + 0.5, f0 - 3, f0 - 2)
    sim(l, 'er-cornisa', cx, w - 0.75, f0 - 4, f0 - 3)
    sim(l, 'er-ornato', cx, 0.5, f0 - 3, f0 - 2)
    l.rect('er-sombra', cx + w + 0.5, cx + w + 1.25, f0 - 3, f0 - 2)

def frontis_cartela(l, cx, w, f0):
    # Frontis curvo partido sobre una puerta: cornisa, las dos mitades que suben hacia el medio terminando
    # en voluta, y la cartela que asoma en el hueco.
    sim(l, 'er-cornisa', cx, w + 1.5, f0 - 2, f0 - 1)
    for sg in (-1, 1):
        for f, w0, w1 in ((f0 - 3, 1, w + 1), (f0 - 4, 1, w - 0.25)):
            a, b = sorted((cx + sg * w0, cx + sg * w1))
            l.rect('er-cornisa', a, b, f, f + 1)
        a, b = sorted((cx + sg * 1, cx + sg * 1.5))
        l.rect('er-ornato', a, b, f0 - 4, f0 - 3)                           # voluta
    sim(l, 'er-cornisa', cx, 0.5, f0 - 5, f0 - 2)                          # cartela
    sim(l, 'er-ornato', cx, 0.25, f0 - 4, f0 - 3)
    l.rect('er-sombra', cx + w + 1, cx + w + 1.5, f0 - 2, f0 - 1)

def balaustrada_u(l, a, b, f0, f1, color='er-balaustre', hueco='er-sombra'):
    l.rect(hueco, a, b, f0 + 1, f1 - 1)
    l.rect(color, a, b, f0, f0 + 1)
    l.rect(color, a, b, f1 - 1, f1)
    n = int((b - a - 0.5) / 1.25) + 1
    x = a + q(((b - a) - (n - 1) * 1.25 - 0.5) / 2)
    for k in range(n):
        l.rect(color, x + k * 1.25, x + k * 1.25 + 0.5, f0 + 1, f1 - 1)
    l.rect('er-sombra', a, b, f1, f1 + 1)

def mensulas_u(l, a, b, f, paso=1.5):
    n = int((b - a - 0.75) / paso) + 1
    x = a + q(((b - a) - (n - 1) * paso - 0.75) / 2)
    for k in range(n):
        l.rect('er-cornisa', x + k * paso, x + k * paso + 0.75, f, f + 2)
        l.rect('er-sombra', x + k * paso + 0.75, x + k * paso + 1, f, f + 2)

def estatua(l, cx, f):
    # Estatua sobre su pedestal, de pie en la fila f (el piso de la terraza).
    sim(l, 'er-cornisa', cx, 1, f - 3, f)
    l.rect('er-sombra', cx + 0.5, cx + 1, f - 3, f)
    sim(l, 'er-balaustre', cx, 0.5, f - 7, f - 3)
    sim(l, 'er-balaustre', cx, 0.25, f - 8, f - 7)
    l.rect('er-balaustre', cx + 0.5, cx + 1, f - 7, f - 6)                # brazo
    l.rect('er-sombra', cx + 0.25, cx + 0.5, f - 6, f - 3)

def maceta(l, cx, f):
    # Maceta de piedra con un boj redondo, apoyada en la fila f.
    sim(l, 'er-cornisa', cx, 0.5, f - 1, f)
    sim(l, 'er-cornisa', cx, 0.75, f - 2, f - 1)
    sim(l, 'er-boj', cx, 0.5, f - 4, f - 2); sim(l, 'er-boj', cx, 0.75, f - 3, f - 2)
    l.rect('er-boj-l', cx - 0.5, cx, f - 4, f - 3)

def balaustrada(l, x0, x1, y0, y1, color='er-balaustre', hueco='er-sombra'):
    # Pasamanos, zócalo y balaustres de 0.5 cada 1.25, centrados en el tramo (en unidades, para que quede parejo).
    a, b, f0, f1 = U(x0), U(x1), F(y0), F(y1)
    l.rect(hueco, a, b, f0 + 1, f1 - 1)
    l.rect(color, a, b, f0, f0 + 1)
    l.rect(color, a, b, f1 - 1, f1)
    n = int((b - a - 0.5) / 1.25) + 1
    x = a + round(((b - a) - (n - 1) * 1.25 - 0.5) / 2 * 4) / 4
    for k in range(n):
        l.rect(color, x + k * 1.25, x + k * 1.25 + 0.5, f0 + 1, f1 - 1)
    l.rect('er-sombra', a, b, f1, f1 + 1)                                 # sombra que tira en la pared

def mensulas(l, x0, x1, y, paso=2.5):
    # Ménsulas debajo de un balcón o de una cornisa, centradas en el tramo.
    a, b, f = U(x0), U(x1), F(y)
    n = int((b - a - 0.75) / paso) + 1
    x = a + round(((b - a) - (n - 1) * paso - 0.75) / 2 * 4) / 4
    for k in range(n):
        l.rect('er-cornisa', x + k * paso, x + k * paso + 0.75, f, f + 2)
        l.rect('er-sombra', x + k * paso + 0.75, x + k * paso + 1, f, f + 2)

def ventana(l, x0, x1, y0, y1, arco=False):
    # Vidrio oscuro con marco claro, parteluz y jamba en sombra a la derecha; arco: punta redondeada.
    R(l, 'er-marco', x0 - 2, x1 + 2, y0 - 2, y1 + 1)
    R(l, 'er-vidrio', x0, x1, y0 + (3 if arco else 0), y1)
    if arco:
        R(l, 'er-vidrio', x0 + 2, x1 - 2, y0 + 1, y0 + 3)
        R(l, 'er-vidrio', x0 + 4, x1 - 4, y0, y0 + 1)
    R(l, 'er-marco', (x0 + x1) / 2 - 0.6, (x0 + x1) / 2 + 0.6, y0 + 4, y1)
    R(l, 'er-sombra', x1 + 2, x1 + 3.5, y0 - 1, y1 + 1)
    R(l, 'er-cornisa', x0 - 3, x1 + 3, y1 + 1, y1 + 3)                     # alféizar

def frontis_curvo(l, x0, x1, y):
    # Frontis de segmento (ventanas de arriba del medio): cornisa y arco bajo encima.
    R(l, 'er-cornisa', x0 - 4, x1 + 4, y - 4, y - 2)
    R(l, 'er-cornisa', x0 - 2, x1 + 2, y - 6, y - 4)
    R(l, 'er-cornisa', x0 + 2, x1 - 2, y - 8, y - 6)
    R(l, 'er-sombra', x0 - 4, x1 + 4, y - 2, y - 1)

def frontis_volutas(l, x0, x1, y):
    # Frontis de volutas (puertas de abajo): cornisa, las dos volutas y el mascarón del medio.
    R(l, 'er-cornisa', x0 - 5, x1 + 5, y - 4, y - 2)
    R(l, 'er-sombra', x0 - 5, x1 + 5, y - 2, y - 1)
    for a in (x0 - 4, x1 - 1):
        R(l, 'er-cornisa', a, a + 5, y - 9, y - 4)
        R(l, 'er-ornato', a + 1.5, a + 3.5, y - 8, y - 6)
    c = (x0 + x1) / 2
    R(l, 'er-cornisa', c - 3, c + 3, y - 11, y - 4)
    R(l, 'er-ornato', c - 1.5, c + 1.5, y - 9, y - 6)

def almohadillado(l, x0, x1, y0, y1):
    # Juntas horizontales de la piedra, una cada tres filas.
    for f in range(F(y0) + 2, F(y1), 3):
        l.rect('er-junta', U(x0), U(x1), f, f + 1)

def jarron(l, x, y):
    # Jarrón sobre un pilar: x es el centro y y el pie, en px.
    c, f = U(x), F(y)
    l.rect('er-cornisa', c - 1.25, c + 1.25, f - 2, f)
    l.rect('er-cornisa', c - 0.75, c + 0.75, f - 4, f - 2)
    l.rect('er-cornisa', c - 0.25, c + 0.25, f - 5, f - 4)
    l.rect('er-sombra', c + 0.75, c + 1.25, f - 2, f)

def torre(l):
    a, b = 442, 500
    R(l, 'er-piedra', a, b, 98, 160)
    almohadillado(l, a, b, 98, 160)
    for y in range(100, 158, 6):                                         # esquinas de sillares, alternados
        w = 5 if (y // 6) % 2 else 3.5
        R(l, 'er-cornisa', a, a + w, y, y + 5)
        R(l, 'er-sombra', b - w, b, y, y + 5)
    R(l, 'er-sombra', b - 2, b, 98, 160)
    # El óculo con su guirnalda, dibujado en unidades sobre el eje exacto de la torre: moldura redonda, vidrio,
    # guirnaldas que cuelgan a los lados y el moño de arriba. Medio ancho de cada fila redondeado para caer en
    # la grilla de 0.25 a los dos lados del eje (así queda simétrico).
    cx, cy = (U(a) + U(b)) / 2, F(133)
    def fila(color, f, w):
        w = round(w * 4) / 4 - 0.125
        if w > 0: l.rect(color, cx - w, cx + w, f, f + 1)
    for d in range(-4, 4):                                              # filas del círculo, centro entre dos
        y = d + 0.5
        fila('er-cornisa', cy + d, (16.5 - y * y) ** 0.5)               # moldura (radio 4)
        if abs(y) < 3: fila('er-vidrio', cy + d, (7.6 - y * y) ** 0.5)  # vidrio (radio 2.75)
    for d, w0, w1 in ((-1, 3.6, 6.5), (0, 3.6, 6.5), (1, 4, 5.9), (2, 4.6, 5.4)):   # guirnaldas
        for sg in (-1, 1):
            x0, x1 = sorted((cx + sg * (round(w0 * 4) / 4 - 0.125), cx + sg * (round(w1 * 4) / 4 - 0.125)))
            l.rect('er-ornato', x0, x1, cy + d, cy + d + 1)
    fila('er-ornato', cy - 5, 1.4)                                      # moño de arriba
    fila('er-ornato', cy - 6, 0.6)
    for d in range(-3, 3):                                              # sombra dentro de la moldura, a la derecha
        y = d + 0.5
        w = round((7.6 - y * y) ** 0.5 * 4) / 4 - 0.125
        if abs(y) < 3: l.rect('er-sombra', cx + w - 0.75, cx + w, cy + d, cy + d + 1)
    # Cornisa bajo el campanario, el campanario de tres arcos entre pilastras.
    R(l, 'er-cornisa', a - 3, b + 3, 96, 101); R(l, 'er-sombra', a - 3, b + 3, 101, 103)
    R(l, 'er-piedra', a + 1, b - 1, 73, 96)
    for k, x in enumerate((448, 466, 484)):
        R(l, 'er-pilastra', x - 3, x - 1, 76, 96)
        R(l, 'er-marco', x - 1, x + 11, 76, 96)
        R(l, 'er-vidrio', x + 1, x + 9, 82, 95)
        R(l, 'er-vidrio', x + 3, x + 7, 79, 82)
        R(l, 'er-sombra', x + 9, x + 11, 82, 96)
    R(l, 'er-pilastra', 495, 497, 76, 96)
    R(l, 'er-sombra', b - 2, b - 1, 73, 96)
    # Cornisa de ménsulas y terraza con balaustrada y jarrones en las esquinas.
    R(l, 'er-cornisa-g', a - 6, b + 6, 66, 71)
    mensulas(l, a - 2, b + 2, 71, paso=2)
    R(l, 'er-sombra', a - 6, b + 6, 70, 71)
    balaustrada(l, a - 4, b + 4, 56, 66, hueco='-')
    R(l, 'er-cornisa-g', a - 4, b + 4, 56, 58)                           # pasamanos y zócalo grisáceos
    l.rect('er-cornisa-g', U(a - 4), U(b + 4), F(66) - 1, F(66))
    for x in (a - 4, b + 4):
        R(l, 'er-cornisa', x - 3, x + 3, 54, 66)
        jarron(l, x, 54)

def version():
    l = Lienzo(LARGO, FILAS)
    torre(l)
    # Arriba se nota el cambio entre cuerpos: el del medio está más atrás, con las tejas rojas entre los
    # balaustres; los pabellones de las puntas salen hacia adelante, con la cornisa más volada y más honda y
    # un ático de piedra (sin tejas a la vista) con pedestales y jarrones.
    R(l, 'er-teja', 262, 414, 156, 178)
    R(l, 'er-teja-o', 262, 414, 156, 159)
    balaustrada(l, 262, 414, 165, 178, hueco='er-teja-o')
    l.rect('er-cornisa-g', U(262), U(414), F(178) - 1, F(178))
    l.rect('er-cornisa-g', U(262), U(414), F(165), F(165) + 1)                # pasamanos                # zócalo de la balaustrada, grisáceo
    R(l, 'er-sombra', 372, 378, 148, 156)                               # chimenea
    R(l, 'er-piedra', 147, 552, 179, 324)
    almohadillado(l, 147, 552, 262, 322)
    R(l, 'er-cornisa-g', 262, 414, 178, 185)                               # cornisa del medio, más baja y chata
    R(l, 'er-sombra', 262, 414, 185, 187)
    mensulas(l, 264, 412, 187, paso=3)
    for a, b, pilares in ((140, 266, (150, 256)), (410, 556, (420, 546))):
        R(l, 'er-sombra', a + 4, b - 4, 160, 174)                        # ático de piedra
        balaustrada(l, a + 4, b - 4, 160, 174, hueco='er-sombra')
        l.rect('er-cornisa-g', U(a + 4), U(b - 4), F(174) - 1, F(174))
        R(l, 'er-cornisa-g', a + 4, b - 4, 158, 161)                     # pasamanos ancho
        for x in pilares:
            R(l, 'er-cornisa', x - 5, x + 5, 156, 174)
            R(l, 'er-sombra', x + 3.5, x + 5, 156, 174)
            jarron(l, x, 156)
        R(l, 'er-cornisa-g', a, b, 174, 183)                               # cornisa volada
        R(l, 'er-cornisa-o', a, b, 181, 183)
        R(l, 'er-sombra', a + 2, b - 2, 183, 187)                        # sombra honda
        mensulas(l, a + 6, b - 6, 186, paso=2.5)
    R(l, 'er-sombra', 262, 268, 187, 256)                                # el pabellón tira sombra sobre el medio
    R(l, 'er-friso', 147, 552, 191, 196)
    R(l, 'er-cornisa', 147, 552, 256, 261)
    R(l, 'er-sombra', 147, 552, 261, 263)
    for a, b in ((147, 158), (250, 262), (414, 426), (541, 552)):         # pilastras de las esquinas de cada cuerpo
        R(l, 'er-pilastra', a, b, 196, 322)
        almohadillado(l, a, b, 196, 322)
        R(l, 'er-sombra', b - 1.5, b, 196, 322)
    # Cada cuerpo con su eje: todo lo de un cuerpo se dibuja simétrico respecto de él.
    cI, cM, cD = eje(158, 250), eje(262, 414), eje(426, 541)
    alto0, alto1 = F(210), F(241)                                       # ventanas de arriba
    # Pabellón de la izquierda: arriba la ventana en arco entre dos más chicas y el balcón sobre ménsulas;
    # abajo el portón en arco con su clave, entre paneles con medallón.
    vano(l, cI, 2.5, alto0, alto1 - 1, arcado=True)
    for sg in (-1, 1):
        vano(l, cI + sg * 7.5, 1.75, F(220), alto1 - 1)
    balaustrada_u(l, cI - 12.5, cI + 12.5, alto1, alto1 + 5)
    mensulas_u(l, cI - 12, cI + 12, alto1 + 5)
    for sg in (-1, 1):                                                  # paneles a los lados del portón
        x = cI + sg * 10
        sim(l, 'er-pilastra', x, 2, F(268), F(320))
        sim(l, 'er-sombra', x, 1.5, F(268) + 1, F(320) - 1)
        sim(l, 'er-pilastra', x, 1.25, F(268) + 1, F(320) - 2)
        sim(l, 'er-ornato', x, 0.75, F(278), F(278) + 2)                 # medallón con su cinta
        sim(l, 'er-ornato', x, 0.25, F(278) + 2, F(278) + 4)
    f = F(278)                                                          # arranque del arco del portón
    arco(l, 'er-marco', cI, 5.25, f, F(321))
    arco(l, 'er-vidrio', cI, 4.25, f, F(321))
    sim(l, 'er-marco', cI, 4.25, f, f + 1)                               # imposta: abanico arriba, puerta abajo
    sim(l, 'er-marco', cI, 0.25, f + 1, F(321))
    sim(l, 'er-marco', cI, 4.25, f + 7, f + 8)
    l.rect('er-sombra', cI + 3.75, cI + 4.25, f + 1, F(321))
    sim(l, 'er-cornisa', cI, 0.75, f - 6, f - 3)                         # clave
    # Cuerpo del medio: cuatro ventanas con frontis curvo y cuatro puertas con frontis de volutas;
    # el balcón del medio sobre tres ménsulas grandes, con paneles entre ellas.
    for d in (-23, -7.75, 7.75, 23):
        vano(l, cM + d, 2, F(214), alto1 - 1)
        frontis_segmento(l, cM + d, 2, F(214))
        vano(l, cM + d, 2.25, F(290), F(321), alfeizar=False, travesano=F(290) + 3)
        frontis_cartela(l, cM + d, 2.25, F(290) - 1)
    balaustrada_u(l, cM - 13, cM + 13, alto1, alto1 + 5)
    for d in (-12, 0, 12):                                              # ménsulas: anchas arriba, angostas abajo
        sim(l, 'er-cornisa', cM + d, 1, alto1 + 5, alto1 + 7)
        sim(l, 'er-cornisa', cM + d, 0.5, alto1 + 7, alto1 + 9)
        l.rect('er-sombra', cM + d + 0.5, cM + d + 1, alto1 + 6, alto1 + 9)
    for d in (-6, 6):                                                   # paneles con relieve entre ménsulas
        sim(l, 'er-ornato', cM + d, 2.5, alto1 + 6, alto1 + 8)
        sim(l, 'er-pilastra', cM + d, 2, alto1 + 6, alto1 + 7)
    # Pabellón de la derecha: tres ventanas en arco con balcón; abajo la logia con columnas, entre dos
    # ventanas con su ventanita de entrepiso.
    for d in (-13.5, 0, 13.5):
        vano(l, cD + d, 2.5, alto0, alto1 - 1, arcado=True)
    balaustrada_u(l, cD - 9.5, cD + 9.5, alto1, alto1 + 5)
    mensulas_u(l, cD - 9, cD + 9, alto1 + 5)
    f = F(280)
    arco(l, 'er-marco', cD, 7.25, f, F(322))
    arco(l, 'er-logia', cD, 6.25, f, F(322))
    vano(l, cD, 2, f + 3, F(322), arcado=True, alfeizar=False)           # puerta del fondo de la logia
    for sg in (-1, 1):                                                  # columnas con capitel
        x = cD + sg * 5
        sim(l, 'er-cornisa', x, 0.75, f + 1, F(322))
        sim(l, 'er-cornisa', x, 1.25, f, f + 1)
        l.rect('er-sombra', x + 0.25, x + 0.75, f + 1, F(322))
    sim(l, 'er-cornisa', cD, 0.75, f - 9, f - 6)                         # clave
    for sg in (-1, 1):
        vano(l, cD + sg * 13.5, 2, F(290), F(320))
        vano(l, cD + sg * 13.5, 1.5, F(268), F(276), alfeizar=False)
    # Terraza: zócalo, balaustradas, estatuas en las puntas y macetas con bojes sobre los pilares.
    piso = F(320)
    R(l, 'er-zocalo', 140, 556, 320, 328)
    l.rect('er-cornisa', U(140), U(556), piso, piso + 1)
    for a, b in ((U(150), U(250)), (U(420), U(556))):
        balaustrada_u(l, a, b, piso - 3, piso)
    estatua(l, U(150) + 1, piso - 3); estatua(l, U(556) - 1, piso - 3)
    for x in (U(185), U(220), U(455), U(490), U(525)):
        maceta(l, x, piso - 3)
    # Pasto con el cerco de bojes contra el muro y bojes redondos parejos a los dos lados de la escalinata.
    cE = eje(340, 410)
    R(l, 'er-pasto', X0, X1, 328, 357)
    abajo = F(357)
    l.rect('er-boj-o', 0, LARGO, abajo - 2, abajo)
    l.rect('er-boj', 0, LARGO, abajo - 2, abajo - 1)
    for x in range(0, LARGO, 3):
        l.rect('er-boj-l', x + 0.5, x + 1.25, abajo - 2, abajo - 1)
    paso = 9
    for sg in (-1, 1):
        for k in range(8):
            x = cE + sg * (11 + k * paso)
            if not 2 < x < LARGO - 2: continue
            f0 = piso + 2 + (k % 2) * 2
            for d, w in ((0, 1.5), (1, 2.25), (2, 2.5), (3, 2.25)):       # copa redonda
                sim(l, 'er-boj', x, w, f0 + d, f0 + d + 1)
            l.rect('er-boj-l', x - 1.75, x - 0.5, f0 + 1, f0 + 2)
            l.rect('er-boj-o', x + 1, x + 2.25, f0 + 2, f0 + 4)
    # Escalinata: un escalón por fila, cada vez más ancha, con muretes, y el farol.
    for k, f in enumerate(range(piso, abajo)):
        w = 6 + k * 0.5
        sim(l, 'er-zocalo', cE, w + 1, f, f + 1)                         # muretes
        sim(l, 'er-cornisa' if k % 2 == 0 else 'er-escalon', cE, w, f, f + 1)
    xf = cE - 12                                                        # farol
    l.rect('er-farol', xf - 0.25, xf + 0.25, piso - 6, abajo - 2)
    sim(l, 'er-farol', xf, 0.75, piso - 8, piso - 6)
    sim(l, 'er-luz', xf, 0.25, piso - 8, piso - 6)
    # Muro del lago de sillares con su albardilla, la escalera que baja al agua y el agua con el reflejo
    # de la villa, ondas y palos de amarre.
    R(l, 'er-muro', X0, X1, 357, 372)
    l.rect('er-muro-l', 0, LARGO, abajo, abajo + 1)
    l.rect('er-muro-o', 0, LARGO, abajo + 1, abajo + 2)
    agua = F(372)
    for k, f in enumerate(range(abajo + 2, agua, 2)):                   # hiladas de sillares, juntas trabadas
        l.rect('er-muro-o', 0, LARGO, f + 1, f + 2)
        for x in range(3 * (k % 2), LARGO, 6):
            l.rect('er-muro-o', x, x + 0.25, f, f + 1)
    for k, f in enumerate(range(abajo, agua)):                          # escalera al agua
        sim(l, 'er-cornisa' if k % 2 == 0 else 'er-escalon', cE, 4.5, f, f + 1)
    sim(l, 'er-muro-o', cE, 5, abajo, abajo + 1)
    sim(l, 'er-cornisa', cE, 4.5, abajo, abajo + 1)
    R(l, 'er-agua', X0, X1, 372, Y1)
    for k, f in enumerate((agua, agua + 1)):                            # reflejo de la villa, cortado
        for x in range(int(U(150)) + 2 * k, int(U(552)) - 2, 5):
            l.rect('er-agua-r', x, x + 3, f, f + 1)
    for k, f in enumerate(range(agua + 3, F(Y1), 2)):                    # ondas
        x = (k % 3) * 4
        while x < LARGO:
            l.rect('er-agua-l', x, min(x + 3, LARGO), f, f + 1)
            x += 13
    for x in (cE - 22, cE + 30):                                        # palos de amarre
        l.rect('er-palo', x, x + 0.5, agua - 1, F(Y1))
        l.rect('er-palo-l', x, x + 0.25, agua - 1, F(Y1))
    return {'nota': ('Villa Erba, en Cernobbio, desde el lago de Como: los tres cuerpos de piedra con la planta baja '
                     'almohadillada, ventanas en arco y con frontis curvos y de volutas, balcones sobre ménsulas, la '
                     'logia de columnas, la cornisa de ménsulas, la balaustrada con jarrones y las tejas; la torre '
                     'mirador con sillares, óculo y tres arcos; la terraza con estatuas y macetas, la escalinata con el farol, los bojes, el muro de sillares y el agua con su reflejo.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

COLORES = {
    'er-piedra': ('#dcc6aa', '#dcc6aa'), 'er-pilastra': ('#d3bb9d', '#d3bb9d'), 'er-sombra': ('#ab9479', '#ab9479'),
    'er-junta': ('#ccb597', '#ccb597'),
    'er-cornisa': ('#ebdcc6', '#ebdcc6'), 'er-cornisa-o': ('#aea999', '#aea999'), 'er-cornisa-g': ('#c8c3b4', '#c8c3b4'), 'er-friso': ('#cdb497', '#cdb497'), 'er-ornato': ('#c2a786', '#c2a786'),
    'er-marco': ('#e8d8c0', '#e8d8c0'), 'er-vidrio': ('#2e3a3b', '#2e3a3b'), 'er-logia': ('#7d6c5a', '#7d6c5a'),
    'er-balaustre': ('#e8d9c3', '#e8d9c3'), 'er-teja': ('#c0704f', '#c0704f'), 'er-teja-o': ('#9a543a', '#9a543a'),
    'er-zocalo': ('#c9b79f', '#c9b79f'), 'er-escalon': ('#b3a28b', '#b3a28b'),
    'er-pasto': ('#7d9a4e', '#6a8442'), 'er-boj': ('#4f6b35', '#45602e'), 'er-boj-l': ('#6b8a46', '#5d7b3d'),
    'er-boj-o': ('#3f5629', '#374d24'),
    'er-muro': ('#9c968a', '#77726a'), 'er-muro-l': ('#b6b0a4', '#8b867d'),
    'er-agua': ('#7f8c8a', '#3f4847'), 'er-agua-l': ('#9eaaa7', '#56605e'), 'er-agua-r': ('#93968a', '#4d5450'),
    'er-muro-o': ('#8a8478', '#66625a'), 'er-farol': ('#3a3a36', '#3a3a36'), 'er-luz': ('#f0d58a', '#f0d58a'),
    'er-palo': ('#5c4a38', '#5c4a38'), 'er-palo-l': ('#7a6650', '#7a6650'),
    'italia-lago': ('#8d948a', '#272b27'), 'italia-lago-marco': ('#726b75', '#d8d4d8'),
}

p = version()
p.update(placa='italia-lago', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
         marco='italia-lago-marco')
guardar(sys.argv[1], 'estilos', 'Italianizante', p, COLORES, 'er-|italia-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
