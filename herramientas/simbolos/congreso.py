# Congreso Nacional de Brasilia (Oscar Niemeyer), de frente, medido sobre referencias/simbolos/brasilia/
# Brazilian_National_Congress.jpg (900 px de ancho). Líneas horizontales sin separación: las dos torres gemelas con sus
# puentes, la luz a la izquierda y juntas finas; la cúpula del Senado y el cuenco de la Cámara, sombreados como
# volúmenes (luz arriba a la izquierda); las velas lejanas; la plataforma: losa blanca, fachada vidriada con montantes
# y su sombra; la rampa; el espejo de agua y el pasto.
# Uso: congreso.py <simbolos.json> (pone decadas.mundo.1960).
import sys, math
from armar import Lienzo, escribir, con_colores

X = lambda px: round((px - 30) / 5 * 4) / 4           # px a unidades (5 px = 1)
F = lambda py: round((py - 50) / 5)                   # px a fila
TONOS = ['bc-luz', 'bc-cara', 'bc-cara-o', 'bc-sombra']

def volumen(l, centro, ancho_px, f, luz):
    # Una fila de un volumen redondo: de la luz (izquierda) a la sombra (derecha), en cuatro tonos.
    a, b = centro - ancho_px, centro + ancho_px
    cortes = [0, luz, min(1, luz + 0.3), min(1, luz + 0.55), 1]
    for c, t0, t1 in zip(TONOS, cortes, cortes[1:]):
        l.rect(c, X(a + (b - a) * t0), X(a + (b - a) * t1), f, f + 1)

def version():
    l = Lienzo(X(870), F(508))
    # Las velas lejanas, detrás de la plataforma.
    for a, b, c in ((435, 470, 412), (475, 530, 405)):
        for f in range(F(c), F(430)):
            t = (f - F(c)) / max(1, F(430) - F(c))
            l.rect('bc-lejos', X(a + (b - a) * 0.5 * (1 - t)), X(b), f, f + 1)
    # La cúpula del Senado: media esfera achatada.
    for f in range(F(375), F(430)):
        dy = (F(430) - f - 0.5) / (F(430) - F(375))
        volumen(l, 155, 105 * math.sqrt(max(0, 1 - dy * dy)), f, 0.22 + 0.18 * dy)
    # El cuenco de la Cámara: borde claro arriba, se cierra hacia abajo hasta su pie.
    l.rect('bc-luz', X(522), X(845), F(373), F(378))
    for f in range(F(378), F(420)):                                  # playo y tendido: se angosta parejo hasta la base
        dy = (f - F(378) + 0.5) / (F(420) - F(378))
        volumen(l, 683, 161 - 76 * dy ** 1.25, f, 0.35 - 0.2 * dy)
    for f in range(F(420), F(430)):                                  # la base, ancha y corta
        volumen(l, 683, 80, f, 0.3)
    # Las torres: luz a la izquierda, sombra a la derecha, juntas cada pocos pisos, puentes en el medio y arriba.
    for a, b in ((240, 297), (315, 375)):
        l.rect('bc-torre', X(a), X(b), F(57), F(430))
        l.rect('bc-torre-luz', X(a), X(a) + 2, F(57), F(430))
        l.rect('bc-torre-o', X(b) - 1.5, X(b), F(57), F(430))
        for f in range(F(57) + 4, F(430), 5):
            l.rect('bc-junta', X(a) + 2, X(b) - 1.5, f, f + 1)
    for y0, y1 in ((70, 78), (237, 283)):
        l.rect('bc-puente', X(297), X(315), F(y0), F(y1))
    for f in range(F(237), F(283), 2):
        l.rect('bc-vidrio', X(299), X(313), f, f + 1)
    # La plataforma: losa blanca, fachada vidriada con montantes y columnas, sombra al pie.
    l.rect('bc-losa', X(30), X(870), F(428), F(440))
    l.rect('bc-cara', X(30), X(870), F(438), F(440))
    l.rect('bc-vidrio', X(30), X(870), F(440), F(472))
    for x in range(36, 870, 16):
        l.rect('bc-montante', X(x), X(x) + 0.5, F(440), F(472))
    for x in range(40, 870, 64):
        l.rect('bc-losa', X(x), X(x) + 1, F(440), F(472))
    l.rect('bc-sombra-pie', X(30), X(870), F(472), F(478))
    # El espejo de agua y el pasto.
    l.rect('bc-agua', X(30), X(870), F(478), F(496))
    l.rect('bc-agua-luz', X(30), X(870), F(478), F(482))
    l.rect('bc-pasto', X(30), X(870), F(496), F(508))
    # La rampa: blanca, baja desde la losa hacia adelante y se ensancha.
    for f in range(F(435), F(496)):
        t = (f - F(435)) / (F(496) - F(435))
        l.rect('bc-losa', X(320 + 40 * t), X(345 + 85 * t), f, f + 1)
        l.rect('bc-cara-o', X(320 + 40 * t), X(320 + 40 * t) + 0.75, f, f + 1)
    return {'nota': ('Congreso Nacional (Oscar Niemeyer, 1958–1960), de frente, medido sobre la foto: las dos torres gemelas '
                     'con sus puentes, la luz a la izquierda y juntas finas; la cúpula del Senado y el cuenco de la Cámara, '
                     'sombreados como volúmenes; las velas lejanas; la plataforma con su losa blanca y su fachada vidriada; la '
                     'rampa que baja hacia adelante; el espejo de agua y el pasto.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'bc-luz': ('#f4f2ec', '#f4f2ec'), 'bc-cara': ('#e2dfd7', '#e2dfd7'), 'bc-cara-o': ('#cbc7bd', '#cbc7bd'),
    'bc-sombra': ('#aca89e', '#aca89e'), 'bc-lejos': ('#dcdad3', '#dcdad3'), 'bc-torre': ('#c9c8c2', '#c9c8c2'),
    'bc-torre-luz': ('#dfded8', '#dfded8'), 'bc-torre-o': ('#a7a6a0', '#a7a6a0'), 'bc-junta': ('#bdbcb6', '#bdbcb6'),
    'bc-puente': ('#9a9993', '#9a9993'), 'bc-vidrio': ('#3b4448', '#3b4448'), 'bc-losa': ('#efede7', '#efede7'),
    'bc-montante': ('#8b9396', '#8b9396'), 'bc-sombra-pie': ('#5b605f', '#5b605f'), 'bc-agua': ('#8a9ba3', '#8a9ba3'),
    'bc-agua-luz': ('#b8c6cc', '#b8c6cc'), 'bc-pasto': ('#5f8a3a', '#5f8a3a'),
}

ruta = sys.argv[1]
p = version()
p['aire'] = round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10
escribir(ruta, 'mundo', '1960', p, sacar=('grosor', 'arcos', 'rectas', 'zonas'))
texto = con_colores(open(ruta).read(), COLORES, 'bc-')
open(ruta, 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'])
