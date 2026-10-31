# Royal Infirmary de Glasgow, de frente y simétrico, medido sobre referencias/simbolos/hospital/images (7).jpeg
# (achicada a 900 px; eje en x = 447). Líneas horizontales sin separación: el cuerpo central alto con su baranda,
# torrecitas, el asta y la puerta en arco; a cada lado, entre huecos de sombra, un bloque medio, la torre con su tambor,
# su cúpula y su linterna, y el ala baja; piedra arenisca con cornisas y fajas, ventanas con su marco blanco.
# Uso: infirmary.py <simbolos.json> (pone programas.Salud).
import sys
from armar import Lienzo, guardar

EJE = 447
X = lambda px: round((px - 150) / 4 * 4) / 4          # px a unidades (4 px = 1)
F = lambda py: round((py - 86) / 4)                   # px a fila
SUELO = 310

def par(l, color, xa, xb, ya, yb):
    # Un rectángulo (en px) y su reflejo del otro lado del eje.
    l.rect(color, X(xa), X(xb), F(ya), F(yb))
    l.rect(color, X(2 * EJE - xb), X(2 * EJE - xa), F(ya), F(yb))

def muro(l, color, xa, xb, ya, yb):
    # Piedra con juntas cada tres filas y el costado derecho en sombra (las piezas que salen hacia adelante).
    par(l, color, xa, xb, ya, yb)
    for y in range(ya + 12 - (ya - 86) % 12, yb, 12):
        par(l, 'ri-junta', xa, xb, y, y + 4)
    par(l, 'ri-piedra-s', xb - 4, xb, ya, yb)

def ventanas(l, xs, ys, ancho=6, alto=12):
    # Todas iguales y sobre la grilla (las y caen en filas enteras): guardapolvo, tres filas de vidrio con su marco y
    # el parante del medio, y el alféizar.
    for x in xs:
        for y in ys:
            par(l, 'ri-piedra-o', x - 2, x + ancho + 2, y - 4, y)
            par(l, 'ri-marco', x - 1, x + ancho + 1, y, y + alto + 4)
            par(l, 'ri-ventana', x, x + ancho, y, y + alto)
            par(l, 'ri-ventana-s', x, x + 1, y, y + alto)
            par(l, 'ri-marco', x + ancho // 2, x + ancho // 2 + 1, y, y + alto)

def baranda(l, xa, xb, y):
    par(l, 'ri-cornisa', xa - 2, xb + 2, y + 6, y + 10)
    par(l, 'ri-baranda', xa, xb, y, y + 6)
    for x in range(xa + 4, xb - 2, 8):
        par(l, 'ri-piedra-o', x, x + 3, y + 1, y + 5)
        par(l, 'ri-cornisa', x, x + 2, y + 10, y + 14)                 # las ménsulas bajo la cornisa

def cuernito(l, x):
    # Un pináculo centrado en x: zócalo, fuste con luz a la izquierda, techito en punta y bolita.
    par(l, 'ri-piedra-o', x - 4, x + 4, 140, 148)
    par(l, 'ri-cupula', x - 2, x + 2, 124, 140)
    par(l, 'ri-cupula-luz', x - 2, x - 1, 124, 140)
    par(l, 'ri-cupula', x - 3, x + 3, 120, 124)
    par(l, 'ri-cupula', x - 1, x + 1, 112, 120)
    par(l, 'ri-cupula-luz', x - 2, x + 2, 108, 112)

def version():
    l = Lienzo(X(2 * EJE - 150), F(SUELO) + 1)
    PISOS = range(190, 300, 20)                                      # seis pisos, cada 5 filas
    # Las chimeneas, detrás de las barandas.
    for x in (176, 214, 252, 350, 372):
        y = 150 if x < 300 else 130
        par(l, 'ri-piedra-o', x, x + 10, y, y + 20)
        par(l, 'ri-cornisa', x - 2, x + 12, y, y + 4)
    # Las alas bajas de afuera.
    muro(l, 'ri-piedra', 150, 274, 176, SUELO)
    baranda(l, 150, 274, 166)
    for y in (182, 258):
        par(l, 'ri-piedra-o', 150, 274, y, y + 3)
    ventanas(l, range(158, 268, 18), PISOS)
    # Los bloques del medio, entre la torre y el cuerpo central.
    muro(l, 'ri-piedra', 330, 394, 156, SUELO)
    baranda(l, 330, 394, 146)
    par(l, 'ri-piedra-o', 330, 394, 182, 185)
    ventanas(l, (343, 359, 375), [166] + list(PISOS))
    # Los huecos de sombra entre las piezas.
    par(l, 'ri-hueco', 274, 290, 150, SUELO)
    par(l, 'ri-hueco', 394, 406, 146, SUELO)
    # Las torres de cúpula: fuste claro, tambor con su abertura, cúpula redondeada y linterna.
    muro(l, 'ri-piedra-luz', 288, 332, 150, SUELO)
    for y in range(154, SUELO, 8):                                   # las piedras de esquina, alternadas
        par(l, 'ri-piedra' if (y - 154) % 16 else 'ri-piedra-o', 288, 292 + ((y - 154) % 16 == 0) * 4, y, y + 4)
    par(l, 'ri-cornisa', 284, 336, 148, 154)
    ventanas(l, (299, 312), [162] + list(PISOS), ancho=7)
    # El tambor: cornisa, pilastras y tres aberturas en arco (la del medio más ancha).
    par(l, 'ri-cupula', 286, 334, 128, 148)
    par(l, 'ri-cupula-luz', 286, 290, 128, 148)
    par(l, 'ri-cornisa', 284, 336, 126, 130)
    for a, b in ((291, 299), (305, 315), (321, 329)):
        par(l, 'ri-hueco', a + 1, b - 1, 132, 134)
        par(l, 'ri-hueco', a, b, 134, 146)
    # La cúpula: redondeada, con luz a la izquierda, nervios y un ojo de buey.
    for y0, a, b in ((122, 287, 333), (118, 287, 333), (114, 288, 332), (110, 290, 330), (106, 294, 326), (102, 300, 320)):
        par(l, 'ri-cupula', a, b, y0, y0 + 4)
        par(l, 'ri-cupula-luz', a, a + (b - a) * 0.25, y0, y0 + 4)
        for x in (297, 310, 323):
            if a + 2 < x < b - 2: par(l, 'ri-nervio', x, x + 1, y0, y0 + 4)
    par(l, 'ri-cupula-luz', 306, 314, 110, 118)
    par(l, 'ri-hueco', 307, 313, 111, 117)
    # La linterna: cornisa, cuerpo con su abertura, cupulita y remate.
    par(l, 'ri-cornisa', 302, 318, 98, 102)
    par(l, 'ri-cupula', 305, 315, 90, 98)
    par(l, 'ri-hueco', 308, 312, 91, 97)
    par(l, 'ri-cupula-luz', 304, 316, 88, 90)
    par(l, 'ri-cupula', 307, 313, 86, 88)
    for x in (282, 338):                                             # los pináculos a los lados del tambor
        cuernito(l, x)
    # El cuerpo central: más alto, baranda con torrecitas, ventana ancha, ventanas en grilla y la puerta en arco.
    muro(l, 'ri-piedra', 406, EJE, 116, SUELO)
    par(l, 'ri-piedra', EJE - 4, EJE, 116, SUELO)                    # (el eje no lleva sombra)
    baranda(l, 406, EJE, 108)
    # Las torrecitas de las esquinas: cuerpo con su ranura, cornisa y techo en punta con remate.
    par(l, 'ri-cupula', 404, 416, 104, 120)
    par(l, 'ri-cupula-luz', 404, 406, 104, 120)
    par(l, 'ri-hueco', 409, 411, 106, 116)
    par(l, 'ri-cornisa', 402, 418, 102, 104)
    par(l, 'ri-cupula', 405, 415, 98, 102)
    par(l, 'ri-cupula', 407, 413, 94, 98)
    par(l, 'ri-cupula-luz', 405, 407, 98, 102)
    par(l, 'ri-cupula', 409, 411, 86, 94)
    par(l, 'ri-piedra-o', 406, EJE, 150, 153)
    par(l, 'ri-piedra-o', 406, EJE, 194, 197)
    par(l, 'ri-marco', 414, EJE, 158, 178)
    par(l, 'ri-ventana', 416, EJE, 160, 176)
    for x in (424, 436):
        par(l, 'ri-marco', x, x + 1, 160, 176)
    ventanas(l, (418, 434), [130] + list(PISOS)[1:-1], ancho=7)
    par(l, 'ri-hueco', 432, EJE, 284, SUELO)                         # la puerta en arco
    for y, a in ((278, 438), (281, 435)):
        par(l, 'ri-hueco', a, EJE, y, y + 3)
    l.rect('ri-cupula', X(EJE) - 0.25, X(EJE) + 0.25, F(66), F(108))  # el asta
    # El basamento almohadillado de punta a punta, con la puerta encima.
    for xa, xb in ((150, 274), (288, 332), (330, 394), (406, EJE)):
        par(l, 'ri-basa', xa, xb, 302, SUELO)
        for x in range(xa + 6, xb, 12):
            par(l, 'ri-junta', x, x + 1, 302, SUELO)
    par(l, 'ri-hueco', 432, EJE, 284, SUELO)
    l.rect('ri-cornisa', X(150), X(2 * EJE - 150), F(SUELO), F(SUELO) + 1)
    return {'nota': ('El Royal Infirmary de Glasgow, de frente y simétrico: el cuerpo central más alto, con su baranda, '
                     'torrecitas, el asta, la ventana ancha y la puerta en arco; a cada lado, entre huecos de sombra, un bloque '
                     'medio, la torre de piedra más clara con su tambor, su cúpula y su linterna, y el ala baja; piedra arenisca '
                     'con juntas, cornisas con ménsulas, piedras de esquina y el costado en sombra de cada pieza; ventanas iguales '
                     'en grilla con guardapolvo, marco blanco y parante; chimeneas, nervios en las cúpulas y basamento almohadillado.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'ri-piedra': ('#c49c66', '#c49c66'), 'ri-piedra-luz': ('#d6b37d', '#d6b37d'), 'ri-piedra-o': ('#a27e4e', '#a27e4e'),
    'ri-hueco': ('#463829', '#463829'), 'ri-cornisa': ('#6d5538', '#6d5538'), 'ri-baranda': ('#b28c5a', '#b28c5a'),
    'ri-ventana': ('#3a352f', '#3a352f'), 'ri-marco': ('#e6dcc7', '#e6dcc7'), 'ri-cupula': ('#574b41', '#574b41'),
    'ri-cupula-luz': ('#7b6d5f', '#7b6d5f'),
    'ri-junta': ('#b48d59', '#b48d59'), 'ri-piedra-s': ('#a9865a', '#a9865a'), 'ri-ventana-s': ('#26221e', '#26221e'),
    'ri-basa': ('#9c7a4e', '#9c7a4e'), 'ri-nervio': ('#6c5e51', '#6c5e51'),
}

p = version()
p.update(placa='salud-brezo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='salud-brezo-marco')
guardar(sys.argv[1], 'programas', 'Salud', p, COLORES, 'ri-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
