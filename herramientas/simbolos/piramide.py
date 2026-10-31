# La Pyramide de Abiyán (Rinaldo Olivieri), de frente y simétrica, medida sobre referencias/simbolos/brutalismo/
# La_Pyramide_Abidjan.png (de frente) y pyramide.jpg / images.jpeg (detalles). Líneas horizontales sin separación: la torre
# lisa de hormigón en el medio, más alta que todo, con sus dos cabezas; detrás, la corona de parasoles con su faja
# vidriada y el cuello; catorce pisos que se ensanchan hacia abajo, cada uno con su alero inclinado claro y la faja
# oscura de ventanas; la losa y los pilotes de la planta baja.
# Uso: piramide.py <simbolos.json> (pone estilos.Brutalismo).
import sys
from armar import Lienzo, guardar

ANCHO, C = 64, 32                    # largo total y eje
TORRE = 7                            # media torre
PISOS, ALTO_PISO, PRIMER = 14, 3, 24
CORONA = 7                           # fila donde arranca la corona (la torre la pasa)
LOSA = PRIMER + PISOS * ALTO_PISO    # fila de la losa de la planta baja
FIN = LOSA + 8

def par(l, color, a, b, f0, f1):
    # Un rectángulo y su reflejo: de a a b (medido desde el eje) a los dos lados.
    l.rect(color, C - b, C - a, f0, f1)
    l.rect(color, C + a, C + b, f0, f1)

def version():
    l = Lienzo(ANCHO, FIN)
    # La corona: parasoles oscuros con listones, la faja vidriada con montantes y el cuello de columnas.
    par(l, 'py-parasol', 0, 21, CORONA, CORONA + 10)
    for x in range(1, 21):
        par(l, 'py-liston', x, x + 0.25, CORONA, CORONA + 10)
    par(l, 'py-hormigon', 0, 21, CORONA + 10, CORONA + 11)
    par(l, 'py-vidrio', 0, 19.5, CORONA + 11, CORONA + 13)
    for x in range(2, 20, 2):
        par(l, 'py-hormigon', x - 0.25, x, CORONA + 11, CORONA + 13)
    par(l, 'py-hormigon', 0, 19.5, CORONA + 13, CORONA + 14)
    par(l, 'py-sombra', 0, 15, CORONA + 14, PRIMER)
    for x in (9, 12, 15):
        par(l, 'py-hormigon', x - 1, x, CORONA + 14, PRIMER)
    # Los pisos: alero claro en dos filas (la de arriba más corta, para que se vea inclinado) y la faja de ventanas.
    for k in range(PISOS):
        f, h = PRIMER + k * ALTO_PISO, 15 + k * 1.15
        par(l, 'py-alero', 0, h - 1.25, f, f + 1)
        par(l, 'py-alero-s', h - 1.25, h - 0.5, f, f + 1)
        par(l, 'py-alero', 0, h, f + 1, f + 2)
        par(l, 'py-ventana', 0, h - 1.5, f + 2, f + 3)
        par(l, 'py-hormigon', h - 1.5, h - 1, f + 2, f + 3)
    # La losa de la planta baja y los pilotes, con las vidrieras metidas.
    h = 15 + PISOS * 1.15
    par(l, 'py-hormigon', 0, h, LOSA, LOSA + 2)
    par(l, 'py-sombra', 0, h - 2, LOSA + 2, FIN)
    for x in range(4, int(h) - 2, 5):
        par(l, 'py-hormigon', x, x + 1.25, LOSA + 2, FIN)
    # La torre, delante de todo: dos cabezas arriba, juntas de encofrado y unas pocas ranuras.
    l.rect('py-torre', C - TORRE, C - 1, 0, FIN)
    l.rect('py-torre', C + 1, C + TORRE, 0, FIN)
    l.rect('py-torre', C - 1, C + 1, 2, FIN)
    l.rect('py-torre-s', C + TORRE - 1, C + TORRE, 0, FIN)
    for f in range(6, FIN, 6):
        l.rect('py-junta', C - TORRE, C + TORRE - 1, f, f + 1)
    for f in range(9, LOSA, 12):
        l.rect('py-ventana', C - 3.5, C - 2.5, f, f + 2)
        l.rect('py-ventana', C + 2.5, C + 3.5, f + 6, f + 8)
    return {'nota': ('La Pyramide de Abiyán (Rinaldo Olivieri, 1973), de frente y simétrica: la torre lisa de hormigón en el '
                     'medio, más alta que todo, con sus dos cabezas; detrás, arriba, la corona de parasoles oscuros con su faja '
                     'vidriada; catorce pisos que se ensanchan hacia abajo, cada uno con su alero inclinado claro y la faja de '
                     'ventanas; abajo, la losa y los pilotes de la planta baja.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': ANCHO, 'lineas': l.lineas()}

COLORES = {
    'py-torre': ('#a39b8c', '#a39b8c'), 'py-torre-s': ('#857d70', '#857d70'), 'py-junta': ('#968e80', '#968e80'),
    'py-hormigon': ('#b4ab9a', '#b4ab9a'), 'py-alero': ('#cfbd94', '#cfbd94'), 'py-alero-s': ('#a8946c', '#a8946c'),
    'py-ventana': ('#3a3530', '#3a3530'), 'py-sombra': ('#4a443d', '#4a443d'), 'py-parasol': ('#3b3936', '#3b3936'),
    'py-liston': ('#6a655d', '#6a655d'), 'py-vidrio': ('#8f9a9c', '#8f9a9c'),
}

p = version()
p.update(placa='brut-laterita', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='brut-laterita-marco')
guardar(sys.argv[1], 'estilos', 'Brutalismo', p, COLORES, 'py-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
