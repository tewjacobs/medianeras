# Sanatorio de Paimio (Alvar Aalto), de frente, pasado a vista frontal desde referencias/simbolos/paimio/paimio.jpg (la
# foto está en perspectiva: se tomaron la cantidad de pisos y de niveles, los colores y el orden de los toldos).
# Líneas horizontales sin separación: a la izquierda, el pabellón blanco de los pacientes con su grilla de ventanas y el
# borde oscuro del techo; a la derecha, el ala de las terrazas: seis niveles con losas blancas, los cuatro de arriba con
# toldos naranja y verde agua alternados (el de arriba con las cortinas rojas) y los dos de abajo vidriados; arriba, el
# alero curvo; en la punta, la torre blanca con la escalera roja.
# Uso: paimio.py <simbolos.json> (pone decadas.mundo.1930).
import sys, random
from armar import Lienzo, escribir, con_colores

ALA, TORRE, FIN_X = 60, 108, 114        # dónde empiezan el ala de las terrazas y la torre, y el largo total
ARRIBA, PISO, NIVEL = 9, 6, 7           # primera fila de los edificios; filas por piso (pacientes) y por nivel (terrazas)
ABAJO = ARRIBA + 7 * PISO               # 7 pisos de pacientes = 6 niveles de terrazas
TOLDOS = ['pa-naranja', 'pa-verde', 'pa-naranja', 'pa-verde', None, None]

def version():
    l = Lienzo(FIN_X, ABAJO + 1)
    # El pabellón de los pacientes: revoque blanco, borde del techo y ventanas iguales en grilla.
    l.rect('pa-revoque', 0, ALA + 0.5, ARRIBA - 2, ABAJO)        # a la misma altura que el alero de las terrazas
    l.rect('pa-techo', 0, ALA, ARRIBA - 3, ARRIBA - 2)
    azar = random.Random(7)                                           # la sombra moteada de los pinos, en la mitad
    for _ in range(140):                                              # izquierda: más tupida abajo y hacia la punta
        f = ARRIBA - 2 + int((ABAJO - ARRIBA + 2) * azar.random() ** 0.6)
        x = ALA / 2 * azar.random() ** 1.6
        l.rect('pa-moteado', x, x + azar.choice((1, 1.5, 2, 3)), f, f + azar.choice((1, 1, 2)))
    for p in range(7):
        f = ARRIBA + 1 + p * PISO + 1
        for x in range(2, ALA - 2, 4):
            l.rect('pa-marco', x, x + 2, f, f + 3)
            l.rect('pa-ventana', x + 0.25, x + 1.75, f, f + 3)
            l.rect('pa-ventana-s', x + 0.25, x + 1.75, f, f + 1)      # el dintel hace sombra arriba
            l.rect('pa-marco', x - 0.25, x + 2.25, f + 3, f + 4)      # el alféizar
    # El ala de las terrazas: por nivel, losa, toldo (o vidrio), baranda y lo de adentro.
    for n, toldo in enumerate(TOLDOS):
        f = ARRIBA + n * NIVEL
        l.rect('pa-losa', ALA, TORRE + 2, f, f + 1)
        if toldo:
            l.rect('pa-adentro', ALA + 0.5, TORRE, f + 1, f + NIVEL)
            if n == 0:
                for x in range(ALA + 1, TORRE - 2, 3):                 # las cortinas rojas del nivel de arriba
                    l.rect('pa-cortina', x, x + 2, f + 3, f + NIVEL)
            l.rect(toldo, ALA + 0.5, TORRE - 3, f + 1, f + 2)        # el toldo inclinado: claro arriba, sombra abajo
            l.rect(toldo, ALA + 0.5, TORRE - 2, f + 2, f + 3)
            l.rect(toldo + '-s', ALA + 0.5, TORRE - 2, f + 3, f + 4)
        else:
            l.rect('pa-vidrio', ALA + 0.5, TORRE, f + 1, f + NIVEL)
            for x in range(ALA + 2, TORRE, 2):
                l.rect('pa-losa', x, x + 0.25, f + 1, f + NIVEL)
        l.rect('pa-losa', ALA + 0.5, TORRE, f + NIVEL - 2, f + NIVEL - 2 + 1)   # la baranda
    # El alero de arriba, con su sombra.
    l.rect('pa-losa', ALA, FIN_X - 0.5, ARRIBA - 2, ARRIBA)
    l.rect('pa-techo', ALA, FIN_X - 0.5, ARRIBA - 3, ARRIBA - 2)
    l.rect('pa-sombra', ALA, TORRE, ARRIBA - 1, ARRIBA)
    # La torre de la punta: blanca, con su hueco en sombra y la escalera roja en zigzag.
    l.rect('pa-losa', TORRE, FIN_X, ARRIBA - 2, ABAJO)
    l.rect('pa-sombra', TORRE + 1.5, FIN_X - 1.5, ARRIBA, ABAJO)
    for f in range(ARRIBA, ABAJO):
        k = (f - ARRIBA) % NIVEL
        x = TORRE + 1.5 + (k if (f - ARRIBA) // NIVEL % 2 == 0 else NIVEL - 1 - k) * 0.5
        l.rect('pa-rojo', x, x + 0.5, f, f + 1)
    for n in range(7):                                                  # las losas redondeadas que pasan delante
        l.rect('pa-losa', TORRE - 0.5, FIN_X, ARRIBA + n * NIVEL, ARRIBA + n * NIVEL + 1)
    l.rect('pa-zocalo', 0, FIN_X, ABAJO, ABAJO + 1)
    return {'nota': ('Sanatorio de Paimio (Alvar Aalto, 1929–1933), de frente: a la izquierda, el pabellón blanco de los '
                     'pacientes con su grilla de ventanas iguales y el borde oscuro del techo; a la derecha, el ala de las '
                     'terrazas, seis niveles de losas blancas: los cuatro de arriba con toldos naranja y verde agua alternados '
                     '(el de arriba con las cortinas rojas) y los dos de abajo vidriados; arriba, el alero curvo que sube en la '
                     'punta; en la punta, la torre blanca con la escalera roja.'),
            'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'pa-revoque': ('#eeece5', '#eeece5'), 'pa-techo': ('#6b5a45', '#6b5a45'),
    'pa-marco': ('#d9d6cd', '#d9d6cd'), 'pa-ventana': ('#5d6a73', '#5d6a73'), 'pa-ventana-s': ('#47525a', '#47525a'),
    'pa-moteado': ('#dfddd5', '#dfddd5'), 'pa-losa': ('#f7f5ef', '#f7f5ef'),
    'pa-adentro': ('#4a4f52', '#4a4f52'), 'pa-sombra': ('#9c9b95', '#9c9b95'), 'pa-cortina': ('#b8262a', '#b8262a'),
    'pa-naranja': ('#ea7a2c', '#ea7a2c'), 'pa-naranja-s': ('#b5531c', '#b5531c'),
    'pa-verde': ('#1d9c8b', '#1d9c8b'), 'pa-verde-s': ('#116a5f', '#116a5f'),
    'pa-vidrio': ('#5f7480', '#5f7480'), 'pa-rojo': ('#c8352b', '#c8352b'), 'pa-zocalo': ('#3a3a36', '#3a3a36'),
}

ruta = sys.argv[1]
p = version()
p['aire'] = round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10
escribir(ruta, 'mundo', '1930', p, sacar=('grosor', 'alto'))
texto = con_colores(open(ruta).read(), COLORES, 'pa-')
open(ruta, 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'])
