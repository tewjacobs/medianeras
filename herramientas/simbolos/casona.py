# Casona de montaña (referencias/simbolos/pintoresquismo/), de frente por el hastial y simétrica: el techo de tejas a
# dos aguas con alero y canecillos; el hastial de tablas verticales con su ventanita; dos pisos de entramado de
# madera y revoque blanco, cada uno con su galería de balaustres; la planta baja de piedra con esquinas de sillares
# y la puerta en arco de medio punto; el pasto.
# Uso: casona.py <simbolos.json> (pone estilos."Pintoresquismo").
import sys, random
from armar import Lienzo, guardar

LARGO, FILAS = 120, 112
C = 60                                              # eje
M0, M1 = 22, 98                                     # el muro
CUMBRE, ALERO = 19, 38                              # filas de la punta y del borde del alero (techo bajo)

def mitad(f):
    # Medio ancho del techo en la fila f (crece hacia abajo hasta pasar el muro).
    return 2 + (f - CUMBRE) * 46 / (ALERO - CUMBRE)

def pies(a, b, paso=3):
    # Posiciones (borde izquierdo, de 1 de ancho) cada `paso`, simétricas respecto del eje C.
    k = int((C - a) // paso)
    return [C - 0.5 + i * paso for i in range(-k, k + 1) if a <= C - 0.5 + i * paso and C + 0.5 + i * paso <= b]

def entramado(l, f0, f1):
    # Revoque blanco con postes y una viga de madera arriba.
    l.rect('pi-revoque', M0, M1, f0, f1)
    for x in pies(M0, M1):                                               # pies derechos parejos, simétricos
        l.rect('pi-madera', x, x + 1, f0, f1)
    l.rect('pi-madera', M0, M0 + 1, f0, f1); l.rect('pi-madera', M1 - 1, M1, f0, f1)
    l.rect('pi-madera', M0, M1, f0, f0 + 1)

def ventana(l, x, f0, f1, ancho=6):
    l.rect('pi-madera', x - 0.5, x + ancho + 0.5, f0 - 1, f1 + 1)       # marco
    l.rect('pi-vidrio', x, x + ancho, f0, f1)
    l.rect('pi-madera', x + ancho / 2 - 0.25, x + ancho / 2 + 0.25, f0, f1)
    l.rect('pi-reflejo', x, x + ancho / 2 - 0.25, f0, f0 + 1)

def galeria(l, f):
    # Galería que vuela del muro: pasamanos, balaustres, solera y cabezas de vigas (de la fila f a la f+10).
    a, b = 17, 103
    l.rect('pi-madera', a, b, f, f + 1)                                  # pasamanos
    for x in pies(a + 1, b - 1, 2.5):                                    # balaustres simétricos
        l.rect('pi-madera', x, x + 1, f + 1, f + 7)
    l.rect('pi-madera', a, b, f + 7, f + 8)                              # solera
    l.rect('pi-madera-o', a - 1, b + 1, f + 8, f + 9)                    # piso de la galería
    for x in pies(a, b, 5):                                              # cabezas de vigas
        l.rect('pi-madera-o', x - 0.25, x + 1.25, f + 9, f + 10)
    l.rect('pi-sombra', M0, M1, f + 9, f + 11)                           # sombra en el muro de abajo
    for x in (a, b - 1):                                                 # postes de las puntas
        l.rect('pi-madera-o', x, x + 1, f - 12, f + 9)

def piedra(l, f0, f1, semilla):
    # Mampostería en hiladas de dos filas, piezas de largo parecido y dos tonos cercanos (alguna más oscura),
    # junta vertical fina; esquinas de sillares claros alineados con las hiladas, uno largo y uno corto.
    r = random.Random(semilla)
    for k, f in enumerate(range(f0, f1, 2)):
        g = min(f + 2, f1)
        x = M0 + (0 if k % 2 == 0 else 2.5)
        while x < M1:
            largo = r.choice((4, 4.5, 5, 5.5))
            tono = 'pi-p3' if r.random() < 0.15 else r.choice(('pi-p1', 'pi-p2'))
            l.rect(tono, max(M0, x), min(M1, x + largo), f, g)
            l.rect('pi-junta', max(M0, x + largo - 0.5), min(M1, x + largo), f, g)
            x += largo
        ancho = 6 if k % 2 == 0 else 3.5
        for a, b in ((M0, M0 + ancho), (M1 - ancho, M1)):
            l.rect('pi-sillar', a, b, f, g)
            l.rect('pi-junta', b - 0.5 if a == M0 else a, b if a == M0 else a + 0.5, f, g)
        l.rect('pi-sillar-l', M0, M0 + ancho, f, f + 1); l.rect('pi-sillar-l', M1 - ancho, M1, f, f + 1)

def recortar(lineas):
    # Sin las filas vacías de arriba (el techo bajo deja cielo de sobra).
    while lineas and lineas[0] == '- 0.25': lineas = lineas[1:]
    return lineas

def version():
    l = Lienzo(LARGO, FILAS)
    # El hastial: el mismo entramado de revoque y listones, debajo del techo.
    for f in range(CUMBRE + 2, ALERO + 1):
        w = mitad(f) - 4
        a, b = max(M0, C - w), min(M1, C + w)
        l.rect('pi-revoque', a, b, f, f + 1)
        for x in pies(a, b):
            l.rect('pi-madera', x, x + 1, f, f + 1)
    l.rect('pi-madera', M0 + 8, M1 - 8, 30, 31)                          # viga intermedia
    ventana(l, 36, 32, 37, 4); ventana(l, M1 - 18, 32, 37, 4)
    l.rect('pi-madera', M0, M1, ALERO, ALERO + 1)                        # la viga del arranque del techo
    # Dos pisos de entramado, con sus ventanas y la puerta a la galería.
    for f0 in (39, 61):
        entramado(l, f0, f0 + 22)
        ventana(l, 30, f0 + 6, f0 + 14, 5); ventana(l, M1 - 13, f0 + 6, f0 + 14, 5)
        l.rect('pi-madera', C - 4.5, C + 4.5, f0 + 3, f0 + 15)          # puerta a la galería
        l.rect('pi-puerta', C - 3.5, C + 3.5, f0 + 4, f0 + 15)
        l.rect('pi-madera', C - 0.25, C + 0.25, f0 + 4, f0 + 15)
        galeria(l, f0 + 11)
    # Planta baja de piedra con la puerta en arco y la ventana chica.
    piedra(l, 83, 104, 4)
    l.rect('pi-sombra', M0, M1, 83, 84)
    BASE, R_EXT, R_INT = 93, 7.5, 5                                     # arranque del arco y radios
    for f in range(BASE - 8, 104):
        y = BASE - f - 0.5                                                 # altura sobre el arranque
        for r, c in ((R_EXT, 'pi-sillar'), (R_INT, 'pi-puerta')):
            if y <= 0: w = r
            elif y < r: w = round((r * r - y * y) ** 0.5 * 4) / 4
            else: continue
            l.rect(c, C - w, C + w, f, f + 1)
    for x in (C - 2.75, C - 0.25, C + 2.25):
        l.rect('pi-madera-o', x, x + 0.5, BASE - 3, 104)                   # tablas de la puerta
    for x in (M0 + 10, M1 - 13):                                            # ventanitas, una a cada lado
        l.rect('pi-vidrio', x, x + 3, 91, 95)
        l.rect('pi-sillar', x - 1, x + 4, 95, 96); l.rect('pi-sillar', x - 1, x + 4, 90, 91)
    # El techo de tejas: banda gruesa con su borde oscuro, alero de madera y canecillos.
    for f in range(CUMBRE, ALERO + 1):
        w = mitad(f)
        for lado in (-1, 1):
            ext = C + lado * w
            capas = (('pi-teja', 0, 2.5), ('pi-alero', 2.5, 5))          # tejas arriba, tabla del alero debajo
            for c, d0, d1 in capas:
                a, b = sorted((ext - lado * d0, ext - lado * d1))
                l.rect(c, a, b, f, f + 1)
    l.rect('pi-teja', C - 3, C + 3, CUMBRE, CUMBRE + 1)
    for x in range(int(C - mitad(ALERO)) + 2, int(C + mitad(ALERO)) - 1, 4):
        l.rect('pi-alero', x, x + 1.25, ALERO + 1, ALERO + 2)              # canecillos
    # El pasto y el escalón de la puerta.
    l.rect('pi-pasto', 0, LARGO, 104, FILAS)
    l.rect('pi-pasto-l', 0, LARGO, 104, 105)
    r = random.Random(2)
    for f in range(105, FILAS):
        x = r.uniform(0, 4)
        while x < LARGO:
            l.rect(r.choice(('pi-pasto-o', 'pi-pasto-l')), x, min(LARGO, x + r.choice((1, 1.5, 2))), f, f + 1)
            x += r.choice((4, 5, 7, 9))
    x = 1
    while x < LARGO - 1:                                                   # matitas que asoman
        if not (M0 - 1 < x < M1 + 1): l.rect('pi-pasto-o', x, x + 0.5, 103, 104)
        x += r.choice((2.5, 3.5, 5))
    l.rect('pi-sillar', C - 8, C + 8, 104, 105)
    return {'nota': ('Una casona de montaña de piedra y madera, de frente por el hastial: techo de tejas a dos aguas con '
                     'alero y canecillos, hastial de entramado bajo un techo bajo, dos pisos de entramado y revoque blanco con '
                     'galerías de balaustres, planta baja de piedra con esquinas de sillares y puerta en arco; el pasto.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': recortar(l.lineas())}

COLORES = {
    'pi-teja': ('#8b4a35', '#8b4a35'), 'pi-teja-o': ('#5e2f22', '#5e2f22'), 'pi-alero': ('#3b2a20', '#3b2a20'),
    'pi-tabla': ('#7a5a40', '#7a5a40'), 'pi-tabla-o': ('#4e3828', '#4e3828'),
    'pi-revoque': ('#ebe4d6', '#ebe4d6'), 'pi-madera': ('#4a3426', '#4a3426'), 'pi-madera-o': ('#33241b', '#33241b'),
    'pi-sombra': ('#b9ae9b', '#b9ae9b'), 'pi-vidrio': ('#262a2c', '#262a2c'), 'pi-reflejo': ('#56636a', '#56636a'),
    'pi-puerta': ('#5a3c2a', '#5a3c2a'),
    'pi-p1': ('#a8997f', '#a8997f'), 'pi-p2': ('#b8aa8f', '#b8aa8f'), 'pi-p3': ('#958770', '#958770'),
    'pi-junta': ('#7a6e5c', '#7a6e5c'), 'pi-sillar': ('#cfc3aa', '#cfc3aa'), 'pi-sillar-l': ('#ddd3bd', '#ddd3bd'),
    'pi-pasto': ('#6f8f3e', '#5f7c35'), 'pi-pasto-o': ('#58762f', '#4a6528'), 'pi-pasto-l': ('#86a352', '#718c44'),
    'pintoresquismo-monte': ('#a7b28c', '#262d20'), 'pintoresquismo-monte-marco': ('#2a2a1f', '#ece6d2'),
}

p = version()
p.update(placa='pintoresquismo-monte', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
         marco='pintoresquismo-monte-marco')
guardar(sys.argv[1], 'estilos', 'Pintoresquismo', p, COLORES, 'pi-|pintoresquismo-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
