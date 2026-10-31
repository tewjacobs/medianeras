# Villa Savoye (Le Corbusier), de frente, medida sobre referencias/simbolos/savoye/images.jpeg (achicada a 900 px).
# Líneas horizontales sin separación: arriba, el solario con sus dos volúmenes curvos (sombreados en la punta redonda),
# el muro del medio con su ranura y el caño alto; la caja blanca con la baranda de la rampa en diagonal y la ventana
# corrida con montantes desparejos y algún reflejo; la sombra de la losa; los pilotes (los de adelante enteros, los de
# atrás grises) y el vidrio curvo de la planta baja con sus barrotes y la puerta; la base blanca de un solo piso.
# Uso: savoye.py <simbolos.json> (pone estilos.Moderno).
import sys
from armar import Lienzo, guardar

X = lambda px: round((px - 70) / 5 * 4) / 4          # px a unidades (5 px = 1)
F = lambda py: round((py - 30) / 5)                  # px a fila
MONTANTES = [118, 197, 245, 270, 317, 365, 410, 457, 505, 553, 600, 648, 695, 745]
REFLEJOS = [(457, 505), (505, 553), (695, 745), (745, 803)]   # paños con árboles reflejados

def cilindro(l, a, b, f0, f1, redondo):
    # Un volumen curvo de frente: blanco, con la punta redonda (izquierda o derecha) en sombra que se va aclarando
    # y las esquinas de arriba de ese lado comidas.
    l.rect('sv-blanco', a, b, f0, f1)
    for k, c in enumerate(('sv-sombra-2', 'sv-sombra', 'sv-sombra-1')):
        x = a + k * 2 if redondo == 'izq' else b - (k + 1) * 2
        l.rect(c, x, x + 2, f0, f1)
    for f, m in ((f0, 2), (f0 + 1, 0.75)):
        if redondo == 'izq': l.rect('-', a, a + m, f, f + 1)
        else: l.rect('-', b - m, b, f, f + 1)

def version():
    l = Lienzo(X(820), F(386))
    # El solario.
    cilindro(l, X(200), X(382), F(45), F(113), 'izq')
    l.rect('sv-blanco', X(382), X(565), F(57), F(113))              # el muro del medio, con su ranura
    l.rect('sv-sombra-1', X(382), X(565), F(57), F(57) + 1)
    l.rect('sv-ranura', X(395), X(447), F(80), F(90))
    l.rect('sv-sombra', X(395), X(447), F(80), F(80) + 1)
    l.rect('sv-blanco', X(567), X(580), F(37), F(113))              # el caño alto
    l.rect('sv-sombra-1', X(576), X(580), F(37), F(113))
    cilindro(l, X(585), X(702), F(35), F(113), 'der')
    # La caja: blanca, con la baranda de la rampa en diagonal y la ventana corrida.
    l.rect('sv-blanco', X(78), X(815), F(113), F(265))
    l.rect('sv-sombra-1', X(78), X(815), F(113), F(113) + 1)
    for f in range(F(118), F(175)):                                  # dos caños paralelos que suben a la derecha
        t = (f - F(118)) / (F(175) - F(118))
        for d in (0, 3):
            x = X(265 - (265 - 210) * t) + d
            l.rect('sv-sombra-2', x, x + 1, f, f + 1)                # tan largo como lo que avanza por fila: sin cortes
    l.rect('sv-marco', X(88), X(803), F(177), F(218))
    for a, b in zip([88] + MONTANTES, MONTANTES + [803]):
        l.rect('sv-reflejo' if (a, b) in REFLEJOS else 'sv-ventana', X(a) + 0.5, X(b) - 0.25, F(177) + 1, F(218) - 1)
    l.rect('sv-sombra-1', X(78), X(815), F(250), F(265))            # la parte baja de la caja, apenas en sombra
    l.rect('sv-sombra', X(78), X(815), F(265), F(272))              # la losa vista desde abajo
    # La base: un solo piso, una losa blanca plana, con la sombra de la caja arriba y el canto adelante.
    l.rect('sv-base', X(55), X(838), F(358), F(382))
    l.rect('sv-base-s', X(55), X(838), F(358), F(364))
    l.rect('sv-base-canto', X(55), X(838), F(382), F(386))
    # El vidrio curvo, simétrico: más oscuro hacia los costados, barrotes parejos y la puerta en el medio.
    l.rect('sv-vidrio', X(335), X(558), F(272), F(358))
    for a, b in ((335, 360), (533, 558)):
        l.rect('sv-vidrio-o', X(a), X(b), F(272), F(358))
    for x in range(338, 558, 6):
        l.rect('sv-barrote', X(x), X(x) + 0.25, F(272), F(358))
    l.rect('sv-puerta', X(415), X(478), F(288), F(358))
    for x in (415, 436, 457, 476):
        l.rect('sv-barrote', X(x), X(x) + 0.5, F(288), F(358))
    l.rect('sv-barrote', X(415), X(478), F(288), F(288) + 1)
    # Los pilotes: los de atrás, en sombra, apoyan más arriba (más lejos); los de adelante bajan hasta el frente de la
    # base, redondos (luz a la izquierda, sombra a la derecha) y con su sombrita en el suelo.
    for x in (200, 255, 638, 693):
        l.rect('sv-pilote-o', X(x) - 0.75, X(x) + 0.75, F(272), F(358))
    for x in (120, 283, 446.5, 610, 773):
        l.rect('sv-blanco', X(x) - 1.25, X(x) + 1.25, F(272), F(380))
        l.rect('sv-sombra-1', X(x) + 0.5, X(x) + 1.25, F(272), F(380))
        l.rect('sv-base-s', X(x) + 1.25, X(x) + 4, F(378), F(380))
    return {'nota': ('La Villa Savoye (Le Corbusier, 1928–1931), de frente, medida sobre la foto: arriba, el solario con sus '
                     'dos volúmenes curvos, el muro del medio con su ranura y el caño alto; la caja blanca con la baranda de '
                     'la rampa en diagonal y la ventana corrida de montantes desparejos, con algún reflejo de los árboles; la '
                     'sombra de la losa; los pilotes, los de adelante blancos y los de atrás en sombra; el vidrio curvo de la '
                     'planta baja con sus barrotes y la puerta; la base blanca de un solo piso, con la sombra de la caja.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'sv-blanco': ('#f2f1ec', '#f2f1ec'), 'sv-sombra-1': ('#e1e0da', '#e1e0da'), 'sv-sombra': ('#cdccc5', '#cdccc5'),
    'sv-sombra-2': ('#b4b3ac', '#b4b3ac'), 'sv-marco': ('#15171a', '#15171a'), 'sv-ventana': ('#2b3036', '#2b3036'),
    'sv-reflejo': ('#4d5e55', '#4d5e55'), 'sv-vidrio': ('#2f3838', '#2f3838'), 'sv-barrote': ('#56605f', '#56605f'),
    'sv-puerta': ('#3d4645', '#3d4645'), 'sv-pilote-o': ('#bdbcb5', '#bdbcb5'), 'sv-base': ('#f4f3ee', '#f4f3ee'), 'sv-base-s': ('#dcdad3', '#dcdad3'),
    'sv-base-canto': ('#c9c7bf', '#c9c7bf'), 'sv-vidrio-o': ('#232a2a', '#232a2a'), 'sv-ranura': ('#8fa9c2', '#8fa9c2'),
}

p = version()
p.update(placa='savoye-fondo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='savoye-fondo-marco')
guardar(sys.argv[1], 'estilos', 'Moderno', p, COLORES, 'sv-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
