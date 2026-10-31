# Torre de Cápsulas Nakagin (Kisho Kurokawa, Tokio), medida sobre referencias/simbolos/nagakin/
# allsizestokyonakagincapsuletowerflic.jpg (850 px de ancho). Líneas horizontales sin separación: columnas de cápsulas
# a distintas alturas, muchas con ojo de buey y otras ciegas, con la sombra de abajo (las que asoman más, con sombra más larga y
# el costado oscuro); detrás, los núcleos de óxido, el de la derecha con su techo inclinado; abajo, el basamento.
# Uso: nakagin.py <simbolos.json> (pone estilos.Metabolismo).
import sys
from armar import Lienzo, guardar

X = lambda px: (px - 40) / 20                 # px a unidades (una cápsula de frente: 100 px = 5)
F = lambda py: round((py - 130) / 13)         # px a fila (una cápsula: 90 px = 7 filas)
CAPSULA = 7                                   # filas: seis de cara y una de sombra
TECHO, PB, PIE = F(1600), F(1740), F(1850)

# Columnas: x de los bordes en px, alto donde arranca y si se ve de frente o de costado.
COLUMNAS = [
    (60, 100, 1000, 'lado'), (100, 215, 920, 'frente'), (245, 305, 590, 'lado'), (305, 445, 480, 'frente'),
    (455, 525, 640, 'lado'), (525, 640, 525, 'frente'), (640, 720, 560, 'lado'),
]

def capsula(l, a, b, f, tipo, asoma, ojo):
    cara = 'nk-cara' if tipo == 'frente' else 'nk-cara-o'
    l.rect(cara, a, b, f, f + 6)
    l.rect('nk-sombra', a, b, f + 6, f + 7 + asoma)
    if asoma: l.rect('nk-costado', b - 0.5, b, f, f + 6)
    if not ojo: return
    d = min(3.5, (b - a) * 0.62)                               # ojo de buey: aro y vidrio oscuro
    c = (a + b) / 2
    for fila, w in ((f + 1, d * 0.7), (f + 2, d), (f + 3, d), (f + 4, d * 0.7)):
        l.rect('nk-aro', c - w / 2, c + w / 2, fila, fila + 1)
        l.rect('nk-ojo', c - w / 2 + 0.25, c + w / 2 - 0.25, fila, fila + 1)

def version():
    l = Lienzo(X(760), PIE)
    l.rect('nk-nucleo', X(305), X(610), F(480), TECHO)         # el núcleo, que asoma entre las cápsulas
    l.rect('nk-nucleo', X(215), X(305), F(590), TECHO)
    # El núcleo de la derecha: un bloque de base horizontal y techo inclinado que sube a la derecha,
    # con su cara del costado, más oscura, a la izquierda.
    base, alto, bajo = F(480), F(140), F(270)
    for f in range(alto, base):
        x = X(600) - (f - alto + 1) / (bajo - alto) * (X(600) - X(360)) if f < bajo else X(360)
        l.rect('nk-oxido-o', x, X(395), f, f + 1)
        l.rect('nk-oxido', max(x, X(395)), X(600), f, f + 1)
    l.rect('nk-oxido', X(165), X(265), F(640), F(920))         # el de la izquierda, cortado en diagonal arriba
    for f in range(F(590), F(640)):
        l.rect('nk-oxido', X(265) - (f - F(590) + 1) / (F(640) - F(590)) * (X(265) - X(165)), X(265), f, f + 1)
    for f in (F(850), F(875)):                                 # rejillas al pie
        l.rect('nk-oxido-o', X(175), X(255), f, f + 1)
    for k, (x0, x1, y, tipo) in enumerate(COLUMNAS):
        a, b = X(x0) + 0.25, X(x1) - 0.25
        f, i = F(y), 0
        while f + CAPSULA <= TECHO:
            asoma = 1 if (k + i) % 3 == 0 else 0
            ojo = (k * 7 + i * 3) % 5 not in ((0, 3) if tipo == 'frente' else (0, 2, 3))   # algunas, ciegas
            capsula(l, a, b, f, tipo, asoma, ojo)
            f += CAPSULA; i += 1
    l.rect('nk-base', X(30), X(740), TECHO, PB)                # basamento con la faja de vidrio
    x = X(30) + 0.5
    while x + 1.5 <= X(740) - 0.5:
        l.rect('nk-vidrio', x + 0.25, x + 1.5, TECHO + 2, PB - 2)
        x += 1.5
    l.rect('nk-pb', X(60), X(720), PB, PIE)                    # planta baja metida, con pilares
    for px in (90, 260, 430, 600):
        l.rect('nk-base', X(px), X(px) + 0.75, PB, PIE)
    return {'nota': ('La Torre de Cápsulas Nakagin (Kisho Kurokawa, Tokio), de frente: columnas de cápsulas blancas a '
                     'distintas alturas, muchas con su ojo de buey y otras ciegas; detrás, los dos núcleos de óxido de '
                     'techo inclinado, el de la derecha más alto; abajo, el basamento con su faja de vidrio.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'nk-cara': ('#e6e4de', '#e6e4de'), 'nk-cara-o': ('#bdbab2', '#bdbab2'), 'nk-sombra': ('#6d6b67', '#6d6b67'),
    'nk-costado': ('#8f8c86', '#8f8c86'), 'nk-aro': ('#9f9c95', '#9f9c95'), 'nk-ojo': ('#3a4247', '#3a4247'),
    'nk-oxido': ('#7a4128', '#7a4128'), 'nk-oxido-o': ('#55301f', '#55301f'), 'nk-nucleo': ('#45423f', '#45423f'),
    'nk-base': ('#ebeae5', '#ebeae5'), 'nk-vidrio': ('#4a565e', '#4a565e'), 'nk-pb': ('#2f3134', '#2f3134'),
}

p = version()
p.update(placa='metabolismo-anil', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='metabolismo-anil-marco')
COLORES.update({'metabolismo-anil': ('#4b5a7d', '#1b2030'), 'metabolismo-anil-marco': ('#b4a582', '#e4dfcf')})
guardar(sys.argv[1], 'estilos', 'Metabolismo', p, COLORES, 'nk-|metabolismo-anil')
print(len(p['lineas']), 'líneas, largo', p['largo'])
