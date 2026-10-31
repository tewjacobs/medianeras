# Casa Milà, La Pedrera (Antoni Gaudí), de frente, medida sobre referencias/simbolos/la pedrera:casa mila/
# Casa_Milà,_general_view.jpg (achicada a 900 px). Líneas horizontales sin separación: las losas que ondulan como olas
# (claras, con su sombra abajo), la piedra entre ellas y las ventanas en columnas (huecos de esquinas redondeadas, con vidrios azules, celestes u oscuros),
# con los balcones de hierro retorcido en grises;
# arriba, el ático blanco con sus ventanitas cuadradas y el borde del techo ondulado, y las chimeneas; abajo, la planta
# baja en sombra con sus aberturas entre pilares gruesos.
# Uso: pedrera.py <simbolos.json> (pone decadas.mundo.1910).
import sys, math
from armar import Lienzo, escribir, con_colores

X0, X1 = 110, 745                                   # el frente, en px
X = lambda px: round((px - X0) / 5 * 4) / 4         # px a unidades (5 px = 1)
F = lambda py: round((py - 15) / 5)                 # px a fila
LOSAS = [200, 262, 324, 388, 456, 526]              # altura media de cada losa (la primera cierra el ático)
SUELO = 650
# Columnas de ventanas (px) y, por piso (0 = el de arriba), los balcones de hierro: (desde, hasta).
VENTANAS = [(118, 150), (180, 228), (268, 300), (318, 345), (365, 410), (440, 465), (480, 505), (530, 580),
            (615, 640), (690, 724)]
HIERROS = {0: [(258, 300), (510, 612), (692, 745)], 1: [(288, 332), (522, 590)], 2: [(292, 332), (500, 602)],
           3: [(330, 352), (505, 622)], 4: [(392, 440), (560, 640)]}

# Los vidrios: azul, celeste u oscuro, apagados y alternados, con una fila apenas más clara arriba.
VIDRIOS = [('pd-azul', 'pd-azul-luz'), ('pd-celeste', 'pd-celeste-luz'), ('pd-ventana', 'pd-ventana-luz')]

def ola(k, x):
    # La altura (px) de la losa k en x: una onda larga y otra corta, cada losa con su fase.
    return LOSAS[k] + 10 * math.sin(2 * math.pi * (x - X0) / 230 + k * 1.1) + 4 * math.sin(2 * math.pi * x / 95 + k * 2)

def techo(x):
    return 128 + 14 * math.sin(2 * math.pi * (x - X0) / 270 + 0.8) + 4 * math.sin(2 * math.pi * x / 110)

def columnas(a, b):
    # Las columnas de 0.25 de la grilla entre a y b (px), con su x en px.
    i = round(X(a) * 4)
    while i < round(X(b) * 4):
        yield i / 4, X0 + i / 4 * 5
        i += 1

def version():
    l = Lienzo(X(X1), F(SUELO) + 1)
    # Las chimeneas, detrás del borde del techo: formas apiladas que se angostan, con ojos oscuros.
    for c, base, pisos in ((265, 120, [(26, 40), (22, 30), (16, 20), (10, 14)]), (360, 95, [(10, 18), (8, 16)]),
                           (557, 110, [(34, 30), (26, 22), (18, 18), (10, 14), (14, 12), (4, 10)]), (672, 118, [(12, 14), (8, 10)])):
        y = base
        for media, alto in pisos:
            l.rect('pd-chimenea', X(c - media), X(c + media), F(y - alto), F(y))
            l.rect('pd-chimenea-o', X(c + media * 0.4), X(c + media), F(y - alto), F(y))
            y -= alto
        for dx, dy in ((-12, 20), (6, 26), (-4, 34)):
            if dy < base - y: l.rect('pd-ojo', X(c + dx), X(c + dx) + 0.75, F(base - dy), F(base - dy) + 1)
    # El frente: el ático blanco sobre el borde ondulado del techo, la piedra de los pisos y la planta baja en sombra.
    for x, px in columnas(X0, X1):
        l.rect('pd-atico', x, x + 0.25, F(techo(px)), F(ola(0, px)))
        l.rect('pd-borde', x, x + 0.25, F(techo(px)), F(techo(px)) + 1)
        l.rect('pd-piedra', x, x + 0.25, F(ola(0, px)), F(ola(5, px)))
        l.rect('pd-planta', x, x + 0.25, F(ola(5, px)), F(SUELO))
    for i, xc in enumerate(range(150, 720, 45)):                    # las ventanitas del ático, siguiendo la onda
        y = (techo(xc) + ola(0, xc)) / 2 + (6 if i % 2 else -4)
        l.rect('pd-ojo', X(xc), X(xc + 8), F(y), F(y) + 2)
    # Las ventanas de cada piso: huecos en la piedra, sin marco, de esquinas redondeadas; algunas con la persiana baja.
    for k in range(5):
        for a, b in VENTANAS:
            c = (a + b) / 2
            f0, f1 = F(ola(k, c) + 14), F(ola(k + 1, c) - 8)
            vidrio, reflejo = VIDRIOS[(k * 2 + VENTANAS.index((a, b))) % 3]
            for f in range(f0, f1):
                m = 0.75 if f in (f0, f1 - 1) else 0.25 if f in (f0 + 1, f1 - 2) else 0
                l.rect(vidrio, X(a) + m, X(b) - m, f, f + 1)
                if f == f0 + 1: l.rect(reflejo, X(a) + m, X(b) - m, f, f + 1)   # apenas más claro arriba
            if (k + a) % 3 == 0:
                l.rect('pd-persiana', X(a) + 0.75, X(b) - 0.75, f0, f0 + 1)
                l.rect('pd-persiana', X(a) + 0.25, X(b) - 0.25, f0 + 1, f0 + 3)
    # Las losas: una banda clara que sigue la onda, con su sombra abajo.
    for k in range(6):
        for x, px in columnas(X0, X1):
            y = ola(k, px)
            l.rect('pd-losa', x, x + 0.25, F(y - 7), F(y + 4))
            l.rect('pd-sombra', x, x + 0.25, F(y + 4), F(y + 9))
    # Los balcones de hierro: una banda gris clara bajo la baranda oscura, que se comba hacia el medio, con dos
    # hierros ondulados que se entrelazan.
    for k, tramos in HIERROS.items():
        for a, b in tramos:
            b = min(b, X1)
            for x, px in columnas(a, b):
                y = ola(k + 1, px)
                t = (px - a) / (b - a)
                arriba, abajo = F(y - 18 - 6 * math.sin(math.pi * t)), F(y - 2)
                l.rect('pd-hierro-c', x, x + 0.25, arriba, abajo)
                l.rect('pd-hierro', x, x + 0.25, arriba, arriba + 1)
                medio = (arriba + 1 + abajo) / 2
                for fase in (0, math.pi):
                    f = round(medio + (abajo - arriba - 2) / 2 * math.sin(px * 0.2 + fase) - 0.5)
                    l.rect('pd-hierro', x, x + 0.25, f, f + 1)
    # La planta baja: aberturas oscuras entre pilares gruesos, con el arco de arriba siguiendo la losa.
    for a, b in ((118, 165), (200, 255), (300, 352), (398, 452), (475, 540), (565, 640), (665, 724)):
        for x, px in columnas(a, b):
            l.rect('pd-hueco', x, x + 0.25, F(ola(5, px) + 34 + 10 * abs(2 * (px - a) / (b - a) - 1) ** 2), F(SUELO))
    l.rect('pd-vereda', X(X0), X(X1), F(SUELO), F(SUELO) + 1)
    return {'nota': ('Casa Milà, La Pedrera (Antoni Gaudí, 1906–1912), de frente, medida sobre la foto: las losas que ondulan '
                     'como olas, claras y con su sombra; la piedra entre ellas y las ventanas en columnas (huecos de esquinas redondeadas), con los balcones de '
                     'hierro retorcido; arriba, el ático blanco con sus ventanitas y el borde ondulado del techo, y las '
                     'chimeneas; abajo, la planta baja en sombra con sus aberturas entre pilares gruesos.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'pd-piedra': ('#d6cab5', '#d6cab5'), 'pd-losa': ('#f3ede1', '#f3ede1'), 'pd-sombra': ('#9d907a', '#9d907a'),
    'pd-atico': ('#efe9dd', '#efe9dd'), 'pd-borde': ('#a99d89', '#a99d89'), 'pd-planta': ('#bfb39e', '#bfb39e'),
    'pd-ventana': ('#3e4247', '#3e4247'), 'pd-ventana-luz': ('#474c52', '#474c52'),
    'pd-azul': ('#4c5d6e', '#4c5d6e'), 'pd-azul-luz': ('#56687a', '#56687a'),
    'pd-celeste': ('#6f8494', '#6f8494'), 'pd-celeste-luz': ('#7b8f9e', '#7b8f9e'), 'pd-persiana': ('#8c877e', '#8c877e'),
    'pd-hierro': ('#57544f', '#57544f'), 'pd-hierro-c': ('#87827a', '#87827a'), 'pd-hueco': ('#33312e', '#33312e'), 'pd-chimenea': ('#e8e0d0', '#e8e0d0'),
    'pd-chimenea-o': ('#c8bda9', '#c8bda9'), 'pd-ojo': ('#55504a', '#55504a'), 'pd-vereda': ('#8f877a', '#8f877a'),
}

ruta = sys.argv[1]
p = version()
p['aire'] = round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10
escribir(ruta, 'mundo', '1910', p, sacar=('grosor', 'alinear', 'alto', 'arcos', 'rectas', 'zonas'))
texto = con_colores(open(ruta).read(), COLORES, 'pd-')
open(ruta, 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'])
