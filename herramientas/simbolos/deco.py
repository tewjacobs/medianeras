# Estación Texas & Pacific (Fort Worth), de frente y simétrica (referencias/simbolos/art deco/: la postal y la foto
# de frente). Las dos torres de las puntas con su linterna octogonal de techo escalonado y pináculos; el bloque del
# medio con pilares claros que suben de corrido entre las ventanas, el friso de relieves arriba con el bloque
# escalonado, el mástil y la bandera, y dos bandas de ornamento; la base de piedra de dos pisos con ventanales y la entrada del medio (el ventanal de
# cuadrícula, la marquesina verde y las puertas de bronce); el zócalo de granito y la vereda.
# Uso: deco.py <simbolos.json> (pone estilos."Art déco").
import sys
from armar import Lienzo, guardar

LARGO, FILAS = 150, 131
C = 75                                              # eje
T0, T1 = 4, 24                                      # torre izquierda (la derecha es su espejo)
B0, B1 = T1, LARGO - T1                             # bloque del medio
BAHIA, N = 6, 17                                    # 17 bahías de 6 entre las torres
PISO0, PISOS, ALTO = 30, 12, 6                      # primer piso del bloque, cantidad y filas por piso
BASE, ZOCALO, SUELO = 102, 123, 127                 # arranque de la base, zócalo y vereda

def dos(l, color, x0, x1, f0, f1):
    # Pinta en la torre izquierda y lo mismo, corrido, en la derecha (la luz viene siempre de la izquierda).
    l.rect(color, x0, x1, f0, f1)
    l.rect(color, x0 + LARGO - T0 - T1, x1 + LARGO - T0 - T1, f0, f1)

def torre(l):
    a, b = T0, T1
    m = (a + b) / 2                                                     # eje de la torre
    dos(l, 'dc-ladrillo', a, b, 18, BASE)                               # ladrillo ocre, como el bloque
    dos(l, 'dc-sombra', b - 1, b, 18, BASE)                              # canto contra el bloque
    for x in (m - 8, m + 7):                                            # nervios que suben de corrido y
        dos(l, 'dc-nervio', x, x + 1, 12, BASE)                          # pasan la cornisa como aletas
        dos(l, 'dc-crema', x + 0.25, x + 0.75, 11, 12)
    for x in (m - 6, m + 5):                                            # ventanas angostas a los lados
        for k in range(PISOS):
            f = PISO0 + k * ALTO
            dos(l, 'dc-vidrio', x, x + 1, f + 1, f + 4)
    for x in (m - 6, m - 3, m, m + 3):                                  # zigzag bajo la corona
        dos(l, 'dc-oro-o', x - 1, x - 0.5, 19, 20); dos(l, 'dc-oro-o', x + 0.5, x + 1, 19, 20)
        dos(l, 'dc-oro-o', x - 0.5, x + 0.5, 20, 21)
    # Tira del medio, como en la postal: una ventanita por piso con su alféizar claro en un canal de ladrillo
    # oscuro, entre marcos de piedra clara que rematan en cascada: los de afuera terminan más abajo con un
    # escalón, los de adentro suben hasta la corona y abrazan un panel alto y angosto con su ranura.
    dos(l, 'dc-nervio', m - 2, m + 2, 25, BASE)
    for k in range(PISOS + 1):
        f = PISO0 + k * ALTO
        dos(l, 'dc-vidrio', m - 1.5, m + 1.5, f + 1, f + 4)
        dos(l, 'dc-crema-l', m - 1.5, m + 1.5, f + 4, f + 5)             # alféizar claro
    for x in (m - 4.5, m + 3):                                          # marcos de afuera, con su escalón
        dos(l, 'dc-crema-l', x, x + 1.5, 36, BASE)
        dos(l, 'dc-crema-l', x + (0.75 if x < m else 0), x + (1.5 if x < m else 0.75), 34, 36)
    for x in (m - 3, m + 2):                                            # marcos de adentro, hasta arriba
        dos(l, 'dc-crema-l', x, x + 1, 19, BASE)
    dos(l, 'dc-crema-l', m - 2, m + 2, 19, 25)                           # panel alto de arriba
    dos(l, 'dc-nervio', m - 0.5, m + 0.5, 20, 24)                        # y su ranura
    dos(l, 'dc-sombra', m + 4.5, m + 5, 36, BASE)                        # sombra de los marcos, a la derecha
    dos(l, 'dc-sombra', m + 3, m + 3.5, 19, 34)
    # Corona: cornisa con zigzag, pináculos en las esquinas.
    dos(l, 'dc-crema', a - 1, b + 1, 15, 18)
    dos(l, 'dc-sombra', a - 1, b + 1, 17, 18)
    dos(l, 'dc-sombra', a, b, 18, 19)                                    # sombra que tira la cornisa
    for x in range(-10, 10, 2):                                          # zigzag de la cornisa, desde el eje
        dos(l, 'dc-oro-o', m + x, m + x + 0.5, 15, 16); dos(l, 'dc-oro-o', m + x + 1.5, m + x + 2, 15, 16)
        dos(l, 'dc-oro-o', m + x + 0.5, m + x + 1.5, 16, 17)
    pinaculo(l, a - 1); pinaculo(l, b - 1)
    linterna(l, m)

def pie_torre(l):
    # La torre en la base: sigue la tira del medio con una ventana alta y angosta, líneas claras finas de
    # corrido y, arriba, un panel oscuro con zigzag claro a cada lado.
    m = (T0 + T1) / 2
    for x0, x1 in ((m - 8.5, m - 3.5), (m + 3.5, m + 8.5)):
        dos(l, 'dc-marco', x0, x1, BASE + 1, BASE + 5)
        for k in range(4):                                              # zigzag claro: dos V seguidas
            x = x0 + 0.5 + k
            dos(l, 'dc-crema-l', x, x + 0.5, BASE + 2 + k % 2, BASE + 3 + k % 2)
            dos(l, 'dc-crema-l', x + 0.5, x + 1, BASE + 3 - k % 2, BASE + 4 - k % 2)
    for x in (m - 3, m + 2):                                            # los marcos de adentro siguen bajando
        dos(l, 'dc-crema-l', x, x + 1, BASE, ZOCALO)
    dos(l, 'dc-nervio', m - 2, m + 2, BASE, BASE + 5)
    dos(l, 'dc-vidrio', m - 1.5, m + 1.5, BASE + 1, BASE + 4)
    dos(l, 'dc-vidrio', m - 1.5, m + 1.5, BASE + 6, ZOCALO - 1)          # ventana alta y angosta
    dos(l, 'dc-marco', m - 0.25, m + 0.25, BASE + 6, ZOCALO - 1)
    for f in (BASE + 10, BASE + 15):
        dos(l, 'dc-marco', m - 1.5, m + 1.5, f, f + 1)
    dos(l, 'dc-piedra-o', m - 1.5, m + 1.5, ZOCALO - 1, ZOCALO)
    for x in (m - 6.5, m + 6):                                          # líneas claras finas de corrido
        dos(l, 'dc-piedra-l', x, x + 0.5, BASE + 5, ZOCALO)

def pinaculo(l, x):
    # Pináculo bajo y macizo de 2 de ancho que arranca en x, con su tapa; sombra a la derecha.
    dos(l, 'dc-crema', x, x + 2, 12, 15)
    dos(l, 'dc-sombra', x + 1.25, x + 2, 12, 15)
    dos(l, 'dc-crema', x + 0.25, x + 1.75, 11, 12)

def linterna(l, m):
    # Tambor octogonal recto, casi tan ancho como la torre: ranuras de a pares arriba en cada cara y una
    # cornisita fina a media altura. Encima, sobre un alero del ancho del tambor, el techo en zigurat bajo
    # y ancho, con una raya en sombra bajo cada escalón y el remate plano.
    dos(l, 'dc-crema', m - 8, m + 8, 5, 15)
    dos(l, 'dc-crema-l', m - 8, m - 5.5, 5, 15)                          # cara que da a la luz
    dos(l, 'dc-sombra', m + 5.5, m + 8, 5, 15)                           # cara en sombra
    dos(l, 'dc-nervio', m - 8, m + 8, 11, 12)                            # cornisita del tambor
    dos(l, 'dc-vidrio', m - 0.5, m + 0.5, 12, 13)                        # ventanita bajo la cornisita
    for x in (m - 3, m - 1.75, m + 1.25, m + 2.5):                       # ranuras de a pares, al frente
        dos(l, 'dc-vidrio', x, x + 0.5, 6, 10)
    for x in (m - 7.25, m - 6.25, m + 5.75, m + 6.75):                   # y en las caras de costado
        dos(l, 'dc-vidrio', x, x + 0.5, 6, 10)
    dos(l, 'dc-crema-l', m - 8.5, m + 8.5, 4, 5)                         # alero
    dos(l, 'dc-sombra', m + 6, m + 8.5, 4, 5)
    for f, w in ((3, 7), (2, 5.5), (1, 4), (0, 2.5)):                    # escalones, sombra alternada
        dos(l, 'dc-sombra' if f % 2 else 'dc-crema', m - w, m + w, f, f + 1)
        if not f % 2: dos(l, 'dc-sombra', m + w - 1, m + w, f, f + 1)

def bloque(l):
    # El paño de ladrillo y el pretil: un friso ancho de relieves densos (una celosía de rombos por bahía) donde
    # los pilares suben y terminan en punta; en el medio un bloque escalonado con el mástil y la bandera.
    l.rect('dc-ladrillo', B0, B1, 22, BASE)
    l.rect('dc-crema', B0, B1, 22, PISO0 - 1)
    l.rect('dc-crema-l', B0, B1, 22, 23)                                 # albardilla
    l.rect('dc-sombra', B0, B1, PISO0 - 2, PISO0 - 1)
    for f, w in ((19, 4.5), (18, 3), (17, 1.5)):                         # bloque escalonado del medio
        l.rect('dc-crema', C - w, C + w, f, 22)
    l.rect('dc-sombra', C + 3.75, C + 4.5, 19, 22)                       # costado en sombra
    l.rect('dc-nervio', C - 3.5, C + 3.5, 20, 21)                        # relieve del bloque
    l.rect('dc-marco', C - 0.25, C + 0.25, 3, 17)                        # mástil
    l.rect('dc-oro-o', C - 0.5, C + 0.5, 2, 3)
    for f in range(3, 8):                                               # bandera, del lado del mástil el cantón
        l.rect('dc-rojo' if f % 2 else 'dc-blanco', C + 0.25, C + 8.25, f, f + 1)
    l.rect('dc-azul', C + 0.25, C + 3.75, 3, 6)
    for i in range(N):
        c = B0 + i * BAHIA + BAHIA / 2                                  # centro de la bahía
        for f in (23, 25, 27):                                          # celosía de rombos del friso
            for x0, x1 in ((c - 2, c - 1.5), (c - 0.25, c + 0.25), (c + 1.5, c + 2)):
                if f > 23 or x1 - x0 < 0.6: l.rect('dc-nervio', x0, x1, f, f + 1)
        for f in (24, 26):
            l.rect('dc-nervio', c - 1.5, c - 0.5, f, f + 1); l.rect('dc-nervio', c + 0.5, c + 1.5, f, f + 1)
        for k in range(PISOS):
            f = PISO0 + k * ALTO
            l.rect('dc-vidrio', c - 1.5, c + 1.5, f + 1, f + 5)
            l.rect('dc-marco', c - 0.25, c + 0.25, f + 1, f + 5)
            if k == 0:                                                  # las de arriba, con cabeza en punta
                l.rect('dc-vidrio', c - 1, c + 1, f, f + 1)
                l.rect('dc-vidrio', c - 0.5, c + 0.5, f - 1, f)
                l.rect('dc-oro-o', c - 1, c + 1, f + 5, f + 6)          # antepecho con ornato
            else:
                l.rect('dc-sombra', c - 1.5, c + 1.5, f, f + 1)          # dintel en sombra
    for i in range(N + 1):                                              # los pilares suben al friso, en punta
        x = B0 + i * BAHIA
        l.rect('dc-crema-l', x - 0.75, x + 0.75, 24, PISO0 - 1)
        l.rect('dc-crema-l', x - 0.25, x + 0.25, 23, 24)
        l.rect('dc-sombra', x + 0.75, x + 1, 24, PISO0 - 1)
    for i in range(N + 1):
        x = B0 + i * BAHIA
        l.rect('dc-crema', x - 0.75, x + 0.75, PISO0 - 1, BASE)
        l.rect('dc-sombra', x + 0.75, x + 1.25, PISO0 - 1, BASE)
    # Dos bandas de ornamento: abajo del segundo piso y arriba de la base, con remates sobre los pilares.
    for f in (PISO0 + 2 * ALTO, BASE - 2):
        l.rect('dc-crema', B0, B1, f, f + 1)
        for i in range(N + 1):
            x = B0 + i * BAHIA
            l.rect('dc-oro-o', x - 0.5, x + 0.5, f - 1, f)

def base(l):
    l.rect('dc-piedra', T0, LARGO - T0, BASE, ZOCALO)
    l.rect('dc-sombra', T0, LARGO - T0, BASE, BASE + 1)
    centro = range(N // 2 - 1, N // 2 + 2)                              # las tres bahías de la entrada
    # Friso de relieves arriba de la base: un zigurat chico por bahía y un rombo sobre cada pilastra.
    l.rect('dc-piedra-o', T0, LARGO - T0, BASE + 4, BASE + 5)
    for i in range(N):
        c = B0 + i * BAHIA + BAHIA / 2
        l.rect('dc-piedra-o', c - 0.5, c + 0.5, BASE + 1, BASE + 2)
        l.rect('dc-piedra-o', c - 1.5, c + 1.5, BASE + 2, BASE + 3)
    for i in range(N + 1):
        x = B0 + i * BAHIA
        l.rect('dc-piedra-o', x - 0.25, x + 0.25, BASE + 1, BASE + 4)
    # Ventanales de cuadrícula en dos tramos, con el antepecho en relieve entre los dos.
    for i in range(N):
        c = B0 + i * BAHIA + BAHIA / 2
        if i in centro: continue
        l.rect('dc-vidrio', c - 2, c + 2, BASE + 6, ZOCALO - 1)
        for x in (c - 0.75, c + 0.5):
            l.rect('dc-marco', x, x + 0.25, BASE + 6, ZOCALO - 1)
        for f in (BASE + 9, BASE + 16, BASE + 19):
            l.rect('dc-marco', c - 2, c + 2, f, f + 1)
        l.rect('dc-piedra-o', c - 2, c + 2, BASE + 12, BASE + 14)        # antepecho
        l.rect('dc-piedra', c - 1, c + 1, BASE + 12, BASE + 13)        # panel en relieve
    # Pilastras claras de corrido entre los ventanales, con sombra a la derecha.
    for i in range(N + 1):
        x = B0 + i * BAHIA
        if i in (N // 2 - 1 + 1, N // 2 + 1): continue                  # las de adentro de la entrada
        l.rect('dc-piedra-l', x - 0.75, x + 0.75, BASE + 5, ZOCALO)
        l.rect('dc-piedra-o', x + 0.75, x + 1, BASE + 5, ZOCALO)
    # La entrada: ventanal de cuadrícula, marquesina verde y puertas de bronce, centrados en el eje.
    a, b = C - 8, C + 8
    l.rect('dc-piedra-o', a, b, BASE + 5, ZOCALO)
    l.rect('dc-vidrio', a + 1, b - 1, BASE + 6, BASE + 14)
    for x in range(-6, 7, 2):
        l.rect('dc-marco', C + x - 0.25, C + x + 0.25, BASE + 6, BASE + 14)
    for f in (BASE + 8, BASE + 11):
        l.rect('dc-marco', a + 1, b - 1, f, f + 1)
    l.rect('dc-verde', a - 1, b + 1, BASE + 14, BASE + 15)
    l.rect('dc-verde-o', a - 1, b + 1, BASE + 15, BASE + 16)
    l.rect('dc-bronce', a + 1, b - 1, BASE + 17, ZOCALO)
    for x in range(-6, 6, 3):
        l.rect('dc-vidrio', C + x + 0.5, C + x + 2.5, BASE + 18, ZOCALO)
    # Zócalo de granito y vereda.
    l.rect('dc-granito', T0, LARGO - T0, ZOCALO, SUELO)
    l.rect('dc-bronce', a + 1, b - 1, ZOCALO, SUELO)
    l.rect('dc-vereda', 0, LARGO, SUELO, FILAS)
    for x in range(3, LARGO, 12): l.rect('dc-junta', x, x + 0.25, SUELO + 1, FILAS)

def version():
    l = Lienzo(LARGO, FILAS)
    bloque(l)
    torre(l)
    base(l)
    pie_torre(l)
    return {'nota': ('La estación Texas & Pacific de Fort Worth, de frente: las dos torres con su linterna de techo '
                     'escalonado, el bloque de pilares claros con el friso de relieves y la bandera, la base de piedra con la '
                     'marquesina verde y las puertas de bronce, el zócalo de granito y la vereda.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

COLORES = {
    'dc-crema': ('#ead7a0', '#ead7a0'), 'dc-ladrillo': ('#c79f5c', '#c79f5c'), 'dc-sombra': ('#a98447', '#a98447'),
    'dc-nervio': ('#b48f52', '#b48f52'), 'dc-vidrio': ('#33302c', '#33302c'), 'dc-marco': ('#6c5f4c', '#6c5f4c'),
    'dc-oro-o': ('#b38a2c', '#b38a2c'),
    'dc-crema-l': ('#f4e7c2', '#f4e7c2'), 'dc-piedra-o': ('#c9c0aa', '#c9c0aa'), 'dc-piedra': ('#e4ddcb', '#e4ddcb'),
    'dc-rojo': ('#b8433a', '#b8433a'), 'dc-blanco': ('#f4f0e6', '#f4f0e6'), 'dc-azul': ('#33477a', '#33477a'),
    'dc-verde': ('#6f9c78', '#6f9c78'), 'dc-verde-o': ('#41664b', '#41664b'), 'dc-piedra-l': ('#f3efe4', '#f3efe4'), 'dc-bronce': ('#a7834a', '#a7834a'),
    'dc-granito': ('#8a5f55', '#8a5f55'), 'dc-vereda': ('#b3aea4', '#6f6b64'), 'dc-junta': ('#9a958b', '#5d5a54'),
    'deco-terracota': ('#c97b5c', '#4d2619'), 'deco-terracota-marco': ('#2b1a14', '#f1dfd3'),
}

p = version()
p.update(placa='deco-terracota', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
         marco='deco-terracota-marco')
guardar(sys.argv[1], 'estilos', 'Art déco', p, COLORES, 'dc-|deco-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
