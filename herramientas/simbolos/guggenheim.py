# Museo Guggenheim de Nueva York (Wright), medido sobre referencias/simbolos/guggenheim new york/stringio.jpg
# (750 px de ancho) y enderezado de frente. Líneas horizontales sin separación: la espiral blanca de bandas que se
# ensanchan hacia arriba, con las ranuras oscuras entre una y otra y la sombra a la derecha; el Monitor a la
# izquierda, con su techo oscuro y su faja de vidrio; la torre de piedra de atrás con sus ventanas corridas;
# la losa larga de la base con el nombre y la planta baja metida.
# Uso: guggenheim.py <simbolos.json> (pone estilos.Arquitectura orgánica).
import sys
from armar import Lienzo, guardar

X = lambda px: round((px - 195) / 8 * 4) / 4       # px a unidades (8 px = 1)
F = lambda py: round((py - 25) / 8)                # px a fila

def cilindro(l, a, b, f):
    # Una fila de cilindro: sombra en los dos bordes, luz a la izquierda del centro.
    for t0, t1, c in ((0, 0.05, 'gg-sombra'), (0.05, 0.15, 'gg-cara'), (0.15, 0.45, 'gg-luz'), (0.45, 0.72, 'gg-cara'),
                      (0.72, 0.9, 'gg-sombra'), (0.9, 1, 'gg-sombra-o')):
        l.rect(c, a + (b - a) * t0, a + (b - a) * t1, f, f + 1)

def banda(l, x0, x1, y0, y1):
    # Una vuelta de la espiral, con las puntas redondeadas arriba y abajo.
    a, b, f0, f1 = X(x0), X(x1), F(y0), F(y1)
    for f in range(f0, f1):
        m = 0.75 if f == f0 else 0.5 if f == f1 - 1 and f1 - f0 > 2 else 0
        cilindro(l, a + m, b - m, f)

def version():
    l = Lienzo(X(960), F(685))
    # La torre de atrás: piedra con juntas finas y cuatro ventanas corridas.
    l.rect('gg-torre', X(215), X(540), F(70), F(545))
    for px in range(255, 540, 40):
        l.rect('gg-junta', X(px), X(px) + 0.25, F(70), F(545))
    for f in range(F(70) + 4, F(545), 5):
        l.rect('gg-junta', X(215), X(540), f, f + 1)
    for py in (235, 265, 295, 325):
        l.rect('gg-ventana', X(375), X(465), F(py), F(py) + 1)
    l.rect('gg-cara', X(505), X(585), F(305), F(400))          # la caja de la escalera
    l.rect('gg-sombra', X(570), X(585), F(305), F(400))
    # La espiral: cuatro vueltas que se angostan hacia abajo, con ranuras oscuras finas.
    for x0, x1, y0, y1 in ((508, 912, 428, 436), (530, 898, 476, 484), (552, 886, 512, 520)):
        l.rect('gg-ranura', X(x0), X(x1), F(y0), F(y1))
    for x0, x1, y0, y1 in ((488, 922, 335, 428), (514, 908, 436, 476), (538, 894, 484, 512), (556, 884, 520, 540)):
        banda(l, x0, x1, y0, y1)
    # El Monitor: techo oscuro de puntas redondas, faja de vidrio con montantes y el cuerpo blanco.
    l.rect('gg-techo', X(235), X(490), F(420), F(428))
    l.rect('gg-techo', X(225), X(500), F(428), F(440))
    l.rect('gg-vidrio', X(245), X(490), F(440), F(462))
    for px in range(255, 490, 20):
        l.rect('gg-cara', X(px), X(px) + 0.25, F(440), F(462))
    l.rect('gg-cara', X(205), X(500), F(462), F(540))          # el cuerpo, liso, con la sombra del balcón
    l.rect('gg-sombra', X(205), X(209), F(462), F(540))
    l.rect('gg-sombra', X(215), X(495), F(500), F(504))
    # La losa larga de la base con el nombre, y la planta baja metida con sus vidrios.
    l.rect('gg-luz', X(205), X(955), F(540), F(640))           # la losa, lisa, con su punta redonda en sombra
    l.rect('gg-sombra', X(205), X(209), F(540), F(640))
    l.rect('gg-sombra', X(900), X(940), F(540), F(640))
    l.rect('gg-sombra-o', X(940), X(955), F(540), F(640))
    x = X(560)
    for i in range(30):
        if i % 7 != 6: l.rect('gg-letra', x, x + 0.5, F(622), F(622) + 1)
        x += 1.25
    l.rect('gg-pb', X(225), X(935), F(640), F(685))
    l.rect('gg-vidrio', X(240), X(920), F(648), F(685))
    for px in range(240, 921, 34):
        l.rect('gg-pb', X(px), X(px) + 0.5, F(648), F(685))
    return {'nota': ('El Guggenheim de Nueva York (Wright, 1943–1959), de frente desde la Quinta Avenida: la espiral blanca de '
                     'bandas que se ensanchan hacia arriba, con las ranuras oscuras entre vuelta y vuelta; el Monitor a la '
                     'izquierda, con su techo oscuro y su faja de vidrio; detrás, la torre de piedra con sus ventanas corridas; '
                     'abajo, la losa larga con el nombre y la planta baja metida.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'gg-cara': ('#e8dfcc', '#e8dfcc'), 'gg-luz': ('#f4ecdc', '#f4ecdc'), 'gg-sombra': ('#cbc1ad', '#cbc1ad'), 'gg-sombra-o': ('#aba08b', '#aba08b'),
    'gg-ranura': ('#34363a', '#34363a'), 'gg-torre': ('#b2aa9c', '#b2aa9c'), 'gg-junta': ('#a2998a', '#a2998a'),
    'gg-ventana': ('#45464a', '#45464a'), 'gg-techo': ('#2b2a29', '#2b2a29'), 'gg-vidrio': ('#76878f', '#76878f'),
    'gg-letra': ('#55534f', '#55534f'), 'gg-pb': ('#3a3937', '#3a3937'),
}

p = version()
p.update(placa='organica-cherokee', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='organica-cherokee-marco')
COLORES.update({'organica-cherokee': ('#9e3b2c', '#351410'), 'organica-cherokee-marco': ('#61c4d3', '#caebef')})
guardar(sys.argv[1], 'estilos', 'Arquitectura orgánica', p, COLORES, 'gg-|organica-cherokee')
print(len(p['lineas']), 'líneas, largo', p['largo'])
