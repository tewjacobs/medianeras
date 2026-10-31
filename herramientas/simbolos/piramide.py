# La Pyramide de Abiyán (Rinaldo Olivieri), de frente y simétrica, medida sobre referencias/simbolos/brutalismo/
# La_Pyramide_Abidjan.png (de frente) y pyramide.jpg / images.jpeg (detalles). Líneas horizontales sin separación: la torre
# lisa de hormigón en el medio, más alta que todo, con sus dos cabezas; detrás, la corona de parasoles con su faja
# vidriada y el cuello; catorce pisos que se ensanchan hacia abajo, cada uno con su alero inclinado claro y la faja
# oscura de ventanas; la losa y los pilotes de la planta baja.
# Uso: piramide.py <simbolos.json> (pone estilos.Brutalismo).
import sys
from armar import Lienzo, guardar

ANCHO, C = 106, 53                   # largo total y eje
TORRE = 12                           # media torre
CORONA, FIN_CORONA = 12, 29          # parasoles
CAJA = FIN_CORONA + 1                # la caja blanca con ventanas, debajo de la corona
PISOS, ALTO_PISO, PRIMER = 14, 5, 40
LOSA = PRIMER + PISOS * ALTO_PISO    # fila de la losa de la planta baja
FIN = LOSA + 13

# Locales de la planta baja: los huecos entre pilotes (desde el eje) y, por lado, cartel, letras y toldo.
BAHIAS = [(39, 45), (31, 37), (23, 29), (14, 21)]
LOCALES_IZQ = [('py-cartel-azul', 'py-cartel-amarillo', None), ('py-cartel-rojo', 'py-blanco', 'py-cartel-rojo'),
               ('py-cartel-verde', 'py-blanco', None), ('py-cartel-amarillo', 'py-sombra', 'py-cartel-verde')]
LOCALES_DER = [('py-cartel-rojo', 'py-blanco', None), ('py-cartel-amarillo', 'py-sombra', 'py-cartel-azul'),
               ('py-cartel-azul', 'py-blanco', None), ('py-cartel-verde', 'py-blanco', 'py-cartel-rojo')]

def par(l, color, a, b, f0, f1):
    # Un rectángulo y su reflejo: de a a b (medido desde el eje) a los dos lados.
    l.rect(color, C - b, C - a, f0, f1)
    l.rect(color, C + a, C + b, f0, f1)

def version():
    l = Lienzo(ANCHO, FIN)
    # La corona: parasoles oscuros con listones, canto arriba y faja de hormigón abajo.
    par(l, 'py-parasol', 0, 35, CORONA, FIN_CORONA)
    for x in range(1, 35):
        par(l, 'py-liston', x, x + 0.25, CORONA + 1, FIN_CORONA)
    par(l, 'py-liston', 0, 35, CORONA, CORONA + 1)
    par(l, 'py-hormigon', 0, 35, FIN_CORONA, CAJA)
    # La caja blanca: marco y ventanas iguales.
    par(l, 'py-blanco', 0, 32, CAJA, CAJA + 5)
    for x in range(1, 31, 3):
        par(l, 'py-vidrio', x, x + 2, CAJA + 1, CAJA + 4)
    par(l, 'py-sombra', 0, 32, CAJA + 5, CAJA + 6)
    # El cuello: sombra con columnas.
    par(l, 'py-sombra', 0, 25, CAJA + 6, PRIMER)
    for x in (15, 20, 25):
        par(l, 'py-hormigon', x - 1.5, x, CAJA + 6, PRIMER)
    # Los pisos: alero de listones con el canto claro (más corto, para que se lea inclinado) y juntas entre
    # paneles; debajo, la sombra y la faja de ventanas con parantes. Algunas plantas cuelgan del alero.
    for k in range(PISOS):
        f, h = PRIMER + k * ALTO_PISO, 25 + k * 1.92
        par(l, 'py-alero-c', 0, h - 1, f, f + 1)
        par(l, 'py-alero', 0, h, f + 1, f + 3)
        for x in range(1, int(h)):
            par(l, 'py-alero-s', x, x + 0.25, f + 1, f + 3)
        for x in range(6, int(h) - 1, 6):
            par(l, 'py-sombra', x, x + 0.5, f + 1, f + 3)
        par(l, 'py-sombra', 0, h - 1.5, f + 3, f + 4)
        par(l, 'py-ventana', 0, h - 2, f + 4, f + 5)
        for x in range(3, int(h) - 2, 3):
            par(l, 'py-hormigon', x, x + 0.5, f + 4, f + 5)
        par(l, 'py-hormigon', h - 2, h - 1.5, f + 3, f + 5)
        if k in (2, 5, 9, 11):
            x = 14 + (k * 7) % (h - 18)
            par(l, 'py-planta', x, x + 2, f + 2, f + 4)
            par(l, 'py-planta', x + 0.5, x + 1.5, f + 4, f + 5)
    # La losa de la planta baja y los pilotes; entre pilotes, locales: cartel con letras, toldo a rayas en
    # algunos, vidriera con parantes y puerta en el medio. Cada lado con sus carteles.
    h = 25 + PISOS * 1.92
    par(l, 'py-hormigon', 0, h, LOSA, LOSA + 3)
    par(l, 'py-sombra', 0, h - 3, LOSA + 3, FIN)
    for lado, locales in ((-1, LOCALES_IZQ), (1, LOCALES_DER)):
        def r(color, a, b, f0, f1):
            l.rect(color, C - b, C - a, f0, f1) if lado < 0 else l.rect(color, C + a, C + b, f0, f1)
        for (a, b), (cartel, letra, toldo) in zip(BAHIAS, locales):
            r(cartel, a, b, LOSA + 4, LOSA + 7)
            for x in range(int(a * 2) + 2, int(b * 2) - 2):
                if x % 3: r(letra, x / 2, x / 2 + 0.5, LOSA + 5, LOSA + 6)
            if toldo:
                for x in range(int(a * 2), int(b * 2)):
                    r(toldo if x % 2 else 'py-blanco', x / 2, x / 2 + 0.5, LOSA + 7, LOSA + 8)
            r('py-vidrio', a, b, LOSA + 8, FIN - 1)
            for x in (a + 1.5, b - 2):
                r('py-sombra', x, x + 0.25, LOSA + 8, FIN - 1)
            m = (a + b) / 2
            r('py-puerta', m - 1, m + 1, LOSA + 9, FIN - 1)
    for x in range(int(h) - 4, 0, -8):
        par(l, 'py-hormigon', x - 2, x, LOSA + 3, FIN)
    # La torre, delante de todo: dos cabezas arriba, la grilla del encofrado y ventanitas cuadradas.
    l.rect('py-torre', C - TORRE, C - 1.5, 0, FIN)
    l.rect('py-torre', C + 1.5, C + TORRE, 0, FIN)
    l.rect('py-torre', C - 1.5, C + 1.5, 3, FIN)
    for f in range(8, FIN, 8):
        l.rect('py-junta', C - TORRE, C + TORRE, f, f + 1)
    for x in (-6, 0, 6):
        l.rect('py-junta', C + x - 0.25, C + x, 3, FIN)
    l.rect('py-torre-s', C + TORRE - 1.5, C + TORRE, 0, FIN)
    for n, f in enumerate(range(13, LOSA, 8)):
        for x in ((-9, 3) if n % 2 else (-3, 8)):
            l.rect('py-ventana', C + x, C + x + 1, f, f + 1)
    return {'nota': ('La Pyramide de Abiyán (Rinaldo Olivieri, 1973), de frente y simétrica: la torre lisa de hormigón en el '
                     'medio, más alta que todo, con sus dos cabezas; detrás, arriba, la corona de parasoles oscuros con su faja '
                     'vidriada; catorce pisos que se ensanchan hacia abajo, cada uno con su alero inclinado claro y la faja de '
                     'ventanas; abajo, la losa y los pilotes de la planta baja.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': ANCHO, 'lineas': l.lineas()}

COLORES = {
    'py-torre': ('#a39b8c', '#a39b8c'), 'py-torre-s': ('#857d70', '#857d70'), 'py-junta': ('#968e80', '#968e80'),
    'py-hormigon': ('#b4ab9a', '#b4ab9a'), 'py-alero': ('#cfbd94', '#cfbd94'), 'py-alero-s': ('#a8946c', '#a8946c'),
    'py-ventana': ('#3a3530', '#3a3530'), 'py-sombra': ('#4a443d', '#4a443d'), 'py-parasol': ('#3b3936', '#3b3936'),
    'py-liston': ('#6a655d', '#6a655d'), 'py-vidrio': ('#8f9a9c', '#8f9a9c'), 'py-alero-c': ('#e6d8b4', '#e6d8b4'),
    'py-blanco': ('#ddd8cc', '#ddd8cc'), 'py-puerta': ('#2c2925', '#2c2925'),
    'py-cartel-azul': ('#2f5c9a', '#2f5c9a'), 'py-cartel-amarillo': ('#e3bf3c', '#e3bf3c'),
    'py-cartel-rojo': ('#b23a2a', '#b23a2a'), 'py-cartel-verde': ('#3d7550', '#3d7550'), 'py-planta': ('#5e7a3c', '#5e7a3c'),
}

p = version()
p.update(placa='brut-laterita', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='brut-laterita-marco')
guardar(sys.argv[1], 'estilos', 'Brutalismo', p, COLORES, 'py-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
