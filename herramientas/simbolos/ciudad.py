# Ciudad Universitaria (Pabellón III, Núñez), símbolo del programa Educativo. De frente y simétrico, medido a ojo
# sobre referencias/simbolos/estudios:academico/images (6).jpeg y (5).jpeg (los detalles de cerca).
# La placa larga y baja: cornisa, cuatro tiras de ventanas corridas entre bandejas de hormigón premoldeado (canto de
# arriba con luz, frente con las juntas de los paneles, panza inclinada en sombra), equipos de aire colgados abajo
# de cada bandeja, ventanales con el teclado de paños chicos arriba, reflejos del cielo y algunas cortinas; planta
# baja escondida bajo la losa (nervios en sombra), canteros bajos con poco pasto y la escalera ancha a la izquierda
# que baja a la vereda (foto de frente que mandó el usuario); dos árboles. Sin el charco.
# Uso: ciudad.py <simbolos.json> (pone programas.Educativo).
import sys
from armar import Lienzo, guardar, con_sombras

LARGO = 150
X0, X1 = 3, 147                     # el edificio
PISOS = 4                           # planta baja y cuatro pisos (publicación de la FADU)
G0 = 5                              # primera fila de vidrio
ALTO_PISO = 9                       # 6 de vidrio + 3 de bandeja
PB = G0 + PISOS * ALTO_PISO         # 41: la losa del primer piso; debajo, la planta baja retirada
PISO_PB, VEREDA, FONDO = 51, 57, 61
ESC0, ESC1 = 8, 32                  # la escalera, en la punta izquierda (pedido del usuario)

def h(*v):
    # Un número "al azar" pero fijo, para variar paños y equipos sin que cambie entre corridas.
    n = 7
    for x in v: n = (n * 31 + int(x) * 17 + 11) % 1009
    return n

def bandeja(l, f, x0=X0, x1=X1):
    # Canto de arriba con luz, frente con las juntas de los paneles y la panza inclinada en sombra.
    l.rect('cu-h-c', x0, x1, f, f + 1)
    l.rect('cu-h', x0, x1, f + 1, f + 2)
    x = x0 + 1.5
    while x < x1 - 1:
        l.rect('cu-junta', x, x + 0.25, f + 1, f + 2)
        x += 3
    x = x0 + 0.75
    while x < x1 - 1:                                            # chorreaduras: el hormigón gastado
        if h(x, f) % 3 == 0: l.rect('cu-h-m', x, x + 0.5 + (h(f, x) % 3) * 0.25, f + 1, f + 2)
        x += 2.25
    l.rect('cu-h-o', x0, x1, f + 2, f + 3)
    l.rect('cu-h-c', x0, x0 + 0.5, f + 1, f + 2)                 # la punta de la izquierda, con luz
    l.rect('cu-h-s', x1 - 0.5, x1, f, f + 3)                     # la de la derecha, en sombra

def ventanas(l, g, piso):
    # Seis filas: la sombra de la bandeja con los equipos, el teclado de paños chicos y los ventanales.
    a, b = X0 + 1, X1 - 1
    l.rect('cu-v-o', a, b, g, g + 1)
    l.rect('cu-v-m', a, b, g + 1, g + 2)
    x = a
    while x < b:
        l.rect('cu-marco', x, x + 0.25, g + 1, g + 2)
        x += 1.25
    paso = 2.5
    for k in range(int((b - a) / paso)):
        x = a + k * paso
        r = h(piso, k)
        for f in range(g + 2, g + 6):
            for i in range(round(x * 4), round((x + paso) * 4)):
                u = i / 4
                if r % 9 == 0: c = 'cu-cortina' if f < g + 5 else 'cu-cortina-o'      # cortina baja
                elif r % 13 == 0: c = 'cu-v-m'                                          # paño en sombra
                else:
                    d = (u + (f - g) * 1.0 + piso * 5) % 24
                    c = 'cu-v-c' if d < 1.25 else 'cu-v' if f < g + 5 else 'cu-v-m'
                l.c[f][i] = c
        l.rect('cu-marco', x, x + 0.25, g + 1, g + 6)
    # los equipos de aire, colgados debajo de la bandeja
    for k in range(int((b - a) / 5)):
        if h(k, piso, 3) % 4: continue
        x = a + k * 5 + 1.25
        l.rect('cu-aire', x, x + 1, g, g + 1)
        l.rect('cu-aire-o', x + 0.75, x + 1, g, g + 1)
    # las puntas: el hormigón que cierra la tira
    l.rect('cu-h-c', X0, X0 + 1, g, g + 6)
    l.rect('cu-h-s', X1 - 1, X1, g, g + 6)

def planta_baja(l):
    # Bien escondida bajo el primer piso: la panza de la losa con sus nervios en sombra, el vidriado oscuro
    # retirado con sus parantes y algún paño claro (carteles), y los pilares gruesos (cara izquierda con luz).
    l.rect('cu-pb-o', X0, X1, PB, PB + 3)
    x = X0 + 1
    while x < X1 - 1:                                            # los nervios de la losa, vistos desde abajo
        l.rect('cu-h-o-s', x, x + 0.75, PB, PB + 2)
        l.rect('cu-nervio', x, x + 0.75, PB + 2, PB + 3)
        x += 3
    l.rect('cu-pb', X0 + 4, X1 - 4, PB + 3, PISO_PB)
    x = X0 + 4
    while x < X1 - 4:
        l.rect('cu-pb-m', x, x + 0.25, PB + 3, PISO_PB)
        if h(x) % 7 == 0: l.rect('cu-pb-c', x + 0.5, x + 2, PB + 5, PB + 8)    # un cartel adentro
        x += 2.5
    l.rect('cu-pb-m', X0 + 4, X1 - 4, PB + 5, PB + 6)
    l.rect('cu-pb-o', X0 + 4, X1 - 4, PB + 3, PB + 4)                       # la sombra de la losa
    for k in range(7):
        a = X0 + 8 + k * (X1 - X0 - 18) / 6
        l.rect('cu-h-c', a, a + 1, PB + 3, PISO_PB)
        l.rect('cu-h-s', a + 1, a + 2, PB + 3, PISO_PB)
    l.rect('cu-h-c', X0 - 2, X1 + 2, PISO_PB - 1, PISO_PB)                  # el borde del piso de la planta baja

def arbol(l, cu, fc, r, tonos):
    # Copa de varias matas (luz arriba a la izquierda), borde mordido y huecos; tronco con dos ramas.
    claro, medio, oscuro, muy = tonos
    for f in range(fc, VEREDA):
        w = 0.5 if f < fc + r else 0.75
        l.rect('cu-tronco', cu, cu + w, f, f + 1)
    for k in range(4):
        l.rect('cu-tronco', cu - 0.5 - k * 0.5, cu - k * 0.5, fc + 6 - k, fc + 7 - k)
        l.rect('cu-tronco', cu + 0.75 + k * 0.5, cu + 1.25 + k * 0.5, fc + 5 - k, fc + 6 - k)
    matas = ((0, -0.2, 1.0), (-0.9, 0.25, 0.7), (0.95, 0.15, 0.75), (-0.35, -0.85, 0.6), (0.5, -0.7, 0.65),
             (0.1, 0.55, 0.6), (-1.4, 0.5, 0.45), (1.4, 0.45, 0.45))
    for f in range(fc - 2 * r, fc + r + 2):
        for i in range(round((cu - 2.6 * r) * 4), round((cu + 2.6 * r) * 4)):
            xx = (i / 4 - cu) / (1.25 * r)
            yy = (f + 0.5 - fc) / r
            dentro = None
            for mx, my, mr in matas:
                d = ((xx - mx) ** 2 + (yy - my) ** 2) / (mr * mr)
                if d < 1 and (dentro is None or d < dentro[0]): dentro = (d, mx, my, mr)
            if dentro is None: continue
            d, mx, my, mr = dentro
            k = (i * 7 + f * 13) % 17
            if d > 0.8 and k < 6: continue
            if k == 3 and d < 0.6: continue
            luz = (xx - mx) / mr + (yy - my) / mr
            c = claro if luz < -0.5 else oscuro if luz > 0.5 else medio
            if k in (5, 11): c = claro if luz < 0.2 else medio
            if yy > 0.6 and k % 4 == 0: c = muy
            if 0 <= f < len(l.c) and 0 <= i < l.n: l.c[f][i] = c

def suelo(l):
    # Poco verde: canteros bajos con el murito de hormigón claro y una franja de pasto arriba; a la izquierda la
    # escalera ancha que baja de la planta baja a la vereda, entre dos zancas que bajan en rampa.
    l.rect('cu-pasto', X0 - 2, X1 + 2, PISO_PB, PISO_PB + 2)
    for f in (PISO_PB, PISO_PB + 1):
        x = (f % 2) * 0.75
        while x < LARGO:
            l.rect('cu-pasto-c' if f == PISO_PB else 'cu-pasto-o', x + X0, x + X0 + 0.5, f, f + 1)
            x += 2.25
    l.rect('cu-blanco-c', X0 - 2, X1 + 2, PISO_PB + 2, PISO_PB + 3)
    l.rect('cu-blanco', X0 - 2, X1 + 2, PISO_PB + 3, VEREDA)
    x = X0 + 4
    while x < X1:
        l.rect('cu-blanco-o', x, x + 0.25, PISO_PB + 3, VEREDA)
        x += 12
    l.rect('cu-blanco-o', X1 + 1.5, X1 + 2, PISO_PB + 2, VEREDA)
    # la escalera
    for k, f in enumerate(range(PISO_PB - 1, VEREDA)):
        l.rect('cu-esc-c' if k % 2 == 0 else 'cu-esc', ESC0, ESC1, f, f + 1)
    for k, f in enumerate(range(PISO_PB - 1, VEREDA)):              # zancas que bajan en rampa hacia afuera
        l.rect('cu-blanco-c', ESC0 - 1.5 - k * 0.5, ESC0, f, f + 1)
        l.rect('cu-blanco-o', ESC1, ESC1 + 1.5 + k * 0.5, f, f + 1)
    for x in (ESC0 + 0.5, (ESC0 + ESC1) / 2, ESC1 - 0.75):         # pasamanos
        l.rect('cu-hierro', x, x + 0.25, PISO_PB - 3, VEREDA - 1)
    l.rect('cu-hierro', ESC0 + 0.5, ESC1 - 0.5, PISO_PB - 3, PISO_PB - 2)
    # la vereda
    l.rect('cu-vereda-c', 0, LARGO, VEREDA, VEREDA + 1)
    l.rect('cu-vereda', 0, LARGO, VEREDA + 1, FONDO)
    x = 2
    while x < LARGO:
        l.rect('cu-vereda-o', x, x + 0.25, VEREDA + 1, FONDO)
        x += 5

def version():
    l = Lienzo(LARGO, FONDO)
    # la cornisa: más ancha, con el canto de arriba con luz
    l.rect('cu-h-c', X0 - 0.5, X1 + 0.5, 0, 1)
    l.rect('cu-h', X0 - 0.5, X1 + 0.5, 1, 4)
    x = X0 + 1.5
    while x < X1 - 1:
        l.rect('cu-junta', x, x + 0.25, 1, 4)
        x += 3
    l.rect('cu-h-o', X0 - 0.5, X1 + 0.5, 4, 5)
    l.rect('cu-h-s', X1, X1 + 0.5, 0, 5)
    for p in range(PISOS):
        g = G0 + p * ALTO_PISO
        ventanas(l, g, p)
        bandeja(l, g + 6)
    planta_baja(l)
    suelo(l)
    arbol(l, 47, 40, 8, ('cu-hoja-a-c', 'cu-hoja-a', 'cu-hoja-a-o', 'cu-hoja-oo'))
    arbol(l, 136, 41, 8, ('cu-hoja-c', 'cu-hoja', 'cu-hoja-o', 'cu-hoja-oo'))
    return {'nota': 'La Ciudad Universitaria de Buenos Aires (Pabellón III), de frente: la placa larga de ventanas '
                    'corridas entre bandejas de hormigón, la planta baja escondida bajo la losa y la escalera que baja a la vereda.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

SOMBREABLES = ('cu-h', 'cu-h-c', 'cu-h-o')
COLORES = {
    'cu-h': ('#8f897f', '#857f75'), 'cu-h-c': ('#aaa397', '#9d968a'), 'cu-h-o': ('#4f4a44', '#47433d'),
    'cu-junta': ('#6f695f', '#666057'), 'cu-h-m': ('#77716a', '#6e6862'),
    'cu-v': ('#5b7284', '#526777'), 'cu-v-c': ('#8ea3b2', '#7f93a1'), 'cu-v-m': ('#45586a', '#3e4f5f'),
    'cu-v-o': ('#242c33', '#20272d'), 'cu-marco': ('#a9aca8', '#9a9d99'),
    'cu-cortina': ('#b9b4a8', '#aaa59a'), 'cu-cortina-o': ('#9d988d', '#908b81'),
    'cu-aire': ('#a8a6a0', '#9a9892'), 'cu-aire-o': ('#6b6965', '#62605c'),
    'cu-pb': ('#2c3236', '#272c30'), 'cu-pb-o': ('#1d2124', '#1a1d20'), 'cu-pb-m': ('#4d575e', '#444d53'),
    'cu-pasto': ('#647f3a', '#55702f'), 'cu-pasto-c': ('#748f44', '#62793a'),
    'cu-vereda': ('#8e8a83', '#7d7a73'), 'cu-vereda-c': ('#aba79f', '#97938c'), 'cu-vereda-o': ('#76726c', '#67645e'),
    'cu-esc': ('#7a756d', '#6d6962'), 'cu-esc-c': ('#b3ada2', '#a19b91'), 'cu-hierro': ('#3a3836', '#3a3836'),
    'cu-pasto-o': ('#566f32', '#4a612b'), 'cu-nervio': ('#6a645b', '#615b53'), 'cu-pb-c': ('#8f949a', '#7f848a'),
    'cu-blanco': ('#c4bfb4', '#aea99f'), 'cu-blanco-c': ('#dcd7cc', '#c4bfb5'), 'cu-blanco-o': ('#9a958b', '#88837a'),
    'cu-graf1': ('#c4553e', '#b04c37'), 'cu-graf2': ('#3f6fae', '#38629a'), 'cu-graf3': ('#d9ad3a', '#c29b34'),
    'cu-hoja': ('#5f8636', '#527530'), 'cu-hoja-c': ('#80a547', '#6f913d'), 'cu-hoja-o': ('#43632a', '#3a5724'),
    'cu-hoja-oo': ('#2f4a20', '#2a421c'),
    'cu-hoja-a': ('#a3a142', '#8e8c3a'), 'cu-hoja-a-c': ('#c5bd5a', '#ada64f'), 'cu-hoja-a-o': ('#76772f', '#676829'),
    'cu-tronco': ('#5a4a3b', '#4f4134'),
    'educativo-tipa': ('#8a9a4e', '#232913'), 'educativo-tipa-marco': ('#f3ead9', '#dcd6ec'),
}
con_sombras(COLORES, SOMBREABLES)

if __name__ == '__main__':
    p = version()
    p.update(placa='educativo-tipa', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
             marco='educativo-tipa-marco')
    guardar(sys.argv[1], 'programas', 'Educativo', p, COLORES, 'cu-|educativo-')
    print(len(p['lineas']), 'líneas, largo', p['largo'])
