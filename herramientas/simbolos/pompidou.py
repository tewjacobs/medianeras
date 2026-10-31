# Centro Pompidou (Piano, Rogers y Franchini), de frente, medido sobre referencias/simbolos/pompidou/IMG_3603.jpeg
# (900 px de ancho). Líneas horizontales sin separación: detrás, el vidrio con montantes y las losas; delante, la
# estructura de caños blancos (once vanos, seis pisos) con las cruces de los tirantes; la escalera mecánica que sube un
# piso por vano, con su tubo vidriado encima de la panza roja; la pasarela de arriba, los paneles celestes, la caja roja
# del techo y la de abajo a la derecha; la planta baja metida y la plaza.
# Uso: pompidou.py <simbolos.json> (pone decadas.mundo.1970).
import sys
from armar import Lienzo, escribir, con_colores

X = lambda px: round((px - 25) / 5 * 4) / 4            # px a unidades (5 px = 1)
F = lambda py: round((py - 100) / 5)                   # px a fila
COLUMNAS = [60 + 71 * i for i in range(12)]            # de 60 a 841
PISOS = [142, 179, 216, 253, 290, 327, 345]            # techo, losas y alero de la planta baja
SUELO = 388
# La escalera: puntos (x, y) de la panza roja, de abajo a la izquierda hasta arriba a la derecha.
# La escalera, como en el edificio: tramos de igual pendiente que suben un piso por vano, de columna a columna, y
# descansos de un vano apoyados en las vigas; arriba desemboca en la pasarela del último piso.
C = COLUMNAS
ESCALERA = [(30, SUELO), (85, SUELO), (C[2], 327), (C[3], 327), (C[4], 290), (C[5], 290), (C[6], 253), (C[7], 253),
            (C[8], 216), (C[9], 216), (C[10], 179), (878, 179)]
GALERIAS = [(C[1], C[2], 327), (C[1], C[4], 290), (C[1], C[10], 179)]   # los pasillos vidriados que salen de los descansos

def recta(color, xa, ya, xb, yb, arriba=0, recorte=0):
    # Banda lisa de una línea de grosor con el borde de arriba de (xa, ya) a (xb, yb), en px; `arriba` la sube
    # de a filas y `recorte` le saca esa fracción en cada punta (para no tapar las juntas).
    xa, ya, xb, yb = xa + (xb - xa) * recorte, ya + (yb - ya) * recorte, xb - (xb - xa) * recorte, yb - (yb - ya) * recorte
    if xb < xa: xa, ya, xb, yb = xb, yb, xa, ya
    return {'color': color, 'desde': X(xa), 'hasta': X(xb), 'base': round(((ya + yb) / 2 - 100) / 5 - arriba, 2),
            'subida': round((ya - yb) / 5, 2)}

def version():
    l = Lienzo(X(890), F(SUELO) + 2)
    # Detrás: vidrio con montantes, losas, algunos carteles rojos y la fila de paneles celestes de arriba.
    l.rect('cp-vidrio', X(60), X(841), F(150), F(PISOS[-1]))
    x = 60
    while x < 841:
        l.rect('cp-montante', X(x), X(x) + 0.25, F(150), F(PISOS[-1]))
        x += 12
    for y in PISOS[1:-1]:
        l.rect('cp-losa', X(60), X(841), F(y), F(y) + 1)
    l.rect('cp-celeste', X(420), X(800), F(152), F(166))
    l.rect('cp-naranja', X(573), X(586), F(152), F(166))
    for y in (200, 245):
        l.rect('cp-rojo', X(158), X(205), F(y), F(y) + 2)
    l.rect('cp-pb', X(60), X(841), F(PISOS[-1]), F(SUELO))   # la planta baja, metida y oscura
    l.rect('cp-vidrio', X(560), X(700), F(355), F(SUELO))
    # Las cruces de los tirantes en cada vano y piso, y las escaleras en zigzag de las puntas (debajo de todo lo inclinado).
    rectas = []
    for xa, xb in zip(COLUMNAS, COLUMNAS[1:]):
        for ya, yb in zip(PISOS[1:-1], PISOS[2:-1]):           # el piso de arriba no: ahí va la pasarela
            rectas += [recta('cp-tirante', xa, ya, xb, yb, recorte=0.08), recta('cp-tirante', xb, ya, xa, yb, recorte=0.08)]
    for adentro, afuera in ((60, 25), (841, 885)):               # las escaleras de emergencia de las puntas: un tramo por
        for ya, yb in zip(PISOS[:-2], PISOS[1:-1]):               # piso, paralelos, que bajan hacia afuera (las vigas son
            rectas += [recta('cp-baranda', adentro, ya, afuera, yb, arriba=1, recorte=0.15),   # los descansos)
                       recta('cp-escalera', adentro, ya, afuera, yb, recorte=0.15)]
    # La estructura blanca: columnas y vigas en cada piso, de punta a punta.
    for x in COLUMNAS + [25, 42, 863, 885]:                       # (con los parantes de las jaulas de escalera)
        l.rect('cp-cano', X(x) - 0.25, X(x) + 0.5, F(140), F(SUELO))
    for y in PISOS[:-1]:
        l.rect('cp-cano', X(25), X(885), F(y), F(y) + 1)
    l.rect('cp-techo', X(25), X(885), F(136), F(140))         # la cercha del techo, con los domos de ventilación
    for c in COLUMNAS[2:10:2]:                                 # de a pares, cada dos vanos
        for x in (c + 22, c + 40):
            l.rect('cp-cano', X(x), X(x) + 1.5, F(132), F(136))
    # Los pasillos vidriados y la escalera: el tubo de vidrio en tres tonos (luz arriba, sombra abajo) sobre la panza
    # roja de la escalera o el canto blanco de los pasillos.
    tubo = lambda xa, ya, xb, yb: [recta(c, xa, ya, xb, yb, arriba=k) for k, c in ((1, 'cp-tubo-s'), (2, 'cp-tubo'), (3, 'cp-tubo-luz'))]
    for xa, xb, y in GALERIAS:
        rectas += [recta('cp-cano', xa, y, xb, y)] + tubo(xa, y, xb, y)
    for (xa, ya), (xb, yb) in zip(ESCALERA, ESCALERA[1:]):
        if ya == yb: xa -= 2                                          # los descansos pisan apenas el tramo de antes
        rectas += [recta('cp-rojo', xa, ya, xb, yb)] + tubo(xa, ya, xb, yb)
    # Las cajas rojas: la del techo sobre sus patas y la de abajo a la derecha.
    l.rect('cp-rojo', X(150), X(222), F(106), F(122))
    l.rect('cp-rojo-s', X(150), X(222), F(118), F(122))
    for x in (160, 185, 210):
        l.rect('cp-cano', X(x), X(x) + 0.5, F(122), F(136))
    l.rect('cp-rojo', X(712), X(760), F(345), F(SUELO))
    l.rect('cp-rojo-s', X(712), X(720), F(345), F(SUELO))
    l.rect('cp-plaza', X(0), X(890), F(SUELO), F(SUELO) + 2)
    return {'nota': ('Centro Pompidou (Piano, Rogers y Franchini, 1971–1977), de frente, medido sobre la foto de la plaza: '
                     'detrás, el vidrio con sus montantes y las losas; delante, la estructura de caños blancos, once vanos y '
                     'seis pisos con las cruces de los tirantes; la escalera mecánica que sube un piso por vano, con su tubo '
                     'vidriado encima de la panza roja; la pasarela de arriba, los paneles celestes, la caja roja del techo y '
                     'la de abajo a la derecha; la planta baja metida y la plaza.'),
            'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas(), 'rectas': rectas}

COLORES = {
    'cp-vidrio': ('#59626b', '#59626b'), 'cp-montante': ('#747c83', '#747c83'), 'cp-losa': ('#8d8f8e', '#8d8f8e'),
    'cp-celeste': ('#7cc3e0', '#7cc3e0'), 'cp-naranja': ('#e58a2b', '#e58a2b'), 'cp-rojo': ('#d8352a', '#d8352a'),
    'cp-rojo-s': ('#a3241c', '#a3241c'), 'cp-pb': ('#4d535a', '#4d535a'), 'cp-tirante': ('#6e767d', '#6e767d'), 'cp-escalera': ('#3f454b', '#3f454b'),
    'cp-baranda': ('#9aa1a7', '#9aa1a7'),
    'cp-cano': ('#eceae4', '#eceae4'), 'cp-techo': ('#c4c6c6', '#c4c6c6'), 'cp-tubo': ('#9db8d3', '#9db8d3'), 'cp-tubo-luz': ('#c6d7e7', '#c6d7e7'),
    'cp-tubo-s': ('#7792ae', '#7792ae'),
    'cp-plaza': ('#b5aa98', '#b5aa98'),
}

ruta = sys.argv[1]
p = version()
p['aire'] = round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10
escribir(ruta, 'mundo', '1970', p, sacar=('grosor',))
texto = con_colores(open(ruta).read(), COLORES, 'cp-')
open(ruta, 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'])
