# Museo M+ (Herzog & de Meuron), de frente, medido sobre referencias/simbolos/m+/av_imagen.webp (achicada a 1200 px):
# la foto real, con la torre de aletas en gris cálido. Líneas horizontales sin separación: la torre plana de aletas
# horizontales (una fila aleta y una de sombra), con las losas cada ocho filas, franjas de ventanas prolijas (no
# calcadas: en la foto la luz las deforma), módulos de aletas en dos tonos y las puntas asomando en el borde derecho;
# las patas en V, con luz y sombra, sobre el jardín bajo de la terraza; el canto claro y el basamento negro con sus
# aletas verticales redondeadas; la planta baja de hormigón, retirada, con sus huecos.
# Uso: mmas.py <simbolos.json> (pone decadas.mundo.2020).
import sys
from armar import Lienzo, escribir, con_colores

ANCHO, TA, TB = 98, 10, 74            # largo total; la torre va de TA a TB
TORRE = 52                            # filas de la torre
PATAS = TORRE + 2                     # el jardín (bajo) y las patas
PODIO = PATAS + 1                     # el canto claro y el basamento
BAJA = PODIO + 7
FIN = BAJA + 3

# Ventanas: (piso, desde, hasta), en unidades desde el borde izquierdo de la torre; como las de la foto, arriba.
VENTANAS = [(1, 16, 24), (1, 34, 48), (2, 16, 24), (2, 36, 48), (3, 38, 48)]

def version():
    l = Lienzo(ANCHO, FIN)
    # La torre: aletas y sombras alternadas, las losas, las ventanas más claras de la foto y las puntas a la derecha.
    # Por módulos de cuatro de ancho: las aletas en dos tonos alternados (en damero por piso), con la junta entre
    # módulos; en las filas de sombra, el fondo más oscuro en el medio de cada módulo.
    for f in range(TORRE):
        piso = f // 8
        for m in range(0, TB - TA, 4):
            x = TA + m
            if f % 8 == 7: c = 'mm-losa'
            elif f % 2: c = 'mm-hueco'
            else: c = 'mm-aleta' if (m // 4 + piso) % 2 else 'mm-aleta-b'
            l.rect(c, x, x + 4, f, f + 1)
            if f % 8 != 7:
                l.rect('mm-junta', x, x + 0.25, f, f + 1)
                if f % 2: l.rect('mm-hueco-o', x + 1, x + 3, f, f + 1)
        if f % 8 != 7:                                                # como en el basamento: cada unidad, medio y luz
            for x in range(TA, TB):
                l.rect('mm-t-medio' if f % 2 == 0 else 'mm-t-hueco', x + 0.25, x + 0.5, f, f + 1)
                if f % 2 == 0: l.rect('mm-t-luz', x + 0.5, x + 0.75, f, f + 1)
        if f % 2 == 0: l.rect('mm-punta', TB - 0.75, TB, f, f + 1)
    l.rect('mm-canto-t', TA, TA + 0.5, 0, TORRE)
    # Las ventanas: franjas horizontales prolijas entre aletas, con montantes parejos.
    for piso, a, b in VENTANAS:
        for f in range(piso * 8 + 1, piso * 8 + 6, 2):
            l.rect('mm-ventana', TA + a, TA + b, f, f + 1)
            for x in range(a, b + 1, 2):
                l.rect('mm-montante', TA + x - 0.25, TA + x, f, f + 1)
    l.rect('mm-losa', TA, TB, 0, 1)
    # El jardín de la terraza, detrás de las patas en V.
    for f in range(TORRE, PODIO):
        for x in range(ANCHO * 4):
            k = (x * 5 + f * 7) % 31
            l.rect('mm-flor' if k == 0 else 'mm-pasto-c' if k < 9 else 'mm-pasto', x / 4, x / 4 + 0.25, f, f + 1)
    l.rect('mm-camino', 30, 41, TORRE + 1, PATAS)
    l.rect('mm-camino', 78, 88, TORRE + 1, PATAS)
    for x in (16, 30, 44, 58, 70):
        for k, f in enumerate(range(TORRE, PATAS)):
            l.rect('mm-pata', x - 1.5 + k * 0.5, x - 0.75 + k * 0.5, f, f + 1)       # cada pata: luz a la izquierda
            l.rect('mm-pata-o', x - 0.75 + k * 0.5, x - 0.5 + k * 0.5, f, f + 1)
            l.rect('mm-pata', x + 0.5 - k * 0.5, x + 1.25 - k * 0.5, f, f + 1)
            l.rect('mm-pata-o', x + 1.25 - k * 0.5, x + 1.5 - k * 0.5, f, f + 1)
    # El basamento negro: canto claro arriba y aletas verticales.
    l.rect('mm-canto', 0, ANCHO, PATAS, PODIO)
    l.rect('mm-podio', 0, ANCHO, PODIO, BAJA)
    for x in range(ANCHO):                                            # cada aleta, redondeada: luz, medio y sombra
        l.rect('mm-podio-m', x + 0.25, x + 0.5, PODIO, BAJA)
        l.rect('mm-podio-l', x + 0.5, x + 0.75, PODIO, BAJA)
    l.rect('mm-podio-s', 0, ANCHO, BAJA - 1, BAJA)
    # La planta baja, retirada: hormigón con sus huecos oscuros.
    l.rect('mm-sombra', 0, ANCHO, BAJA, BAJA + 1)
    l.rect('mm-hormigon', 2, ANCHO - 6, BAJA + 1, BAJA + 3)
    for a, b in ((8, 14), (30, 46), (60, 64), (78, 84)):
        l.rect('mm-sombra', a, b, BAJA + 1, BAJA + 3)
    return {'nota': ('Museo M+ (Herzog & de Meuron, 2021), de frente como en la foto: la torre plana de aletas gris cálido, '
                     'con sus losas, algunas ventanas grises y las puntas de las aletas en el borde; las patas en V que la '
                     'levantan sobre el jardín de la terraza; el basamento negro con sus aletas verticales y su canto claro; '
                     'la planta baja de hormigón, retirada.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': ANCHO, 'lineas': l.lineas()}

COLORES = {
    'mm-aleta': ('#968d84', '#968d84'), 'mm-hueco': ('#59534e', '#59534e'), 'mm-losa': ('#34302d', '#34302d'), 'mm-ventana': ('#9a9a96', '#9a9a96'),
    'mm-punta': ('#c4bcb3', '#c4bcb3'), 'mm-montante': ('#6f6f6c', '#6f6f6c'), 'mm-pasto': ('#4d6a34', '#4d6a34'), 'mm-pasto-c': ('#6f8a45', '#6f8a45'),
    'mm-flor': ('#a8452e', '#a8452e'), 'mm-camino': ('#cfcac0', '#cfcac0'), 'mm-pata': ('#d9d4ca', '#d9d4ca'),
    'mm-canto': ('#d6d2ca', '#d6d2ca'), 'mm-podio': ('#1c1c1b', '#1c1c1b'), 'mm-podio-l': ('#3a3734', '#3a3734'),
    'mm-sombra': ('#2a2826', '#2a2826'), 'mm-hormigon': ('#a7a59f', '#a7a59f'), 'mm-podio-m': ('#2c2b29', '#2c2b29'),
    'mm-podio-s': ('#121211', '#121211'), 'mm-pata-o': ('#a29d93', '#a29d93'), 'mm-aleta-b': ('#8a8178', '#8a8178'),
    'mm-junta': ('#57504a', '#57504a'), 'mm-hueco-o': ('#3a3633', '#3a3633'), 'mm-canto-t': ('#5f5852', '#5f5852'), 'mm-t-medio': ('#7d756d', '#7d756d'),
    'mm-t-luz': ('#ada49a', '#ada49a'), 'mm-t-hueco': ('#3d3935', '#3d3935'),
}

ruta = sys.argv[1]
p = version()
p['aire'] = round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10
escribir(ruta, 'mundo', '2020', p, sacar=('grosor', 'alto', 'alinear', 'arcos', 'rectas', 'zonas'))
texto = con_colores(open(ruta).read(), COLORES, 'mm-')
open(ruta, 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'])
