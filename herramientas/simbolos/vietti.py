# Villa La Roccia (Luigi Vietti, Cannobio, Lago Maggiore), de frente, medida en px sobre la foto de época de
# referencias/simbolos/racionalismo/ (Casa-La-Roccia-Cannobio-4.jpg, 1200 de ancho). A la izquierda, la lámina alta
# y la rampa en arco con su baranda; en el medio y a la derecha, el cuerpo redondo: el tambor de arriba, dos losas
# muy voladas con canto blanco y panza en sombra, barandas de caño y vidrios corridos; la punta derecha sombreada
# como cilindro (luz desde la izquierda). Abajo, el muro de piedra seca, la mata, las rocas y el lago.
# Uso: vietti.py <simbolos.json> (pone estilos."Racionalismo").
import sys, random
from armar import Lienzo, guardar

X0, X1, Y0 = 150, 1090, 100
LARGO = 150
S = LARGO / (X1 - X0)                              # unidades por px
LAGO = 745                                         # donde empieza el agua (px)
FILAS = round((LAGO - Y0) * S) + 2 + 10

def U(x): return round((x - X0) * S * 4) / 4
def F(y): return round((y - Y0) * S) + 2

def R(l, c, x0, x1, y0, y1): l.rect(c, U(x0), U(x1), F(y0), F(y1))

def redondo(l, base, x0, x1, y0, y1, cola=70, tonos=('ra-s1', 'ra-s2', 'ra-s3')):
    # Volumen redondo: el tono base y, en la punta derecha (cola px), la sombra que se oscurece.
    R(l, base, x0, x1, y0, y1)
    paso = cola / len(tonos)
    for k, t in enumerate(tonos):
        R(l, t, x1 - cola + k * paso, x1 - cola + (k + 1) * paso, y0, y1)

def baranda(l, x0, x1, y_cano, y_pie, paso=6):
    # Caño corrido (una fila) y parantes cada `paso` unidades, claros sobre lo oscuro.
    f0, f1 = F(y_cano), F(y_pie)
    l.rect('ra-cano', U(x0), U(x1), f0, f0 + 1)
    x = U(x0)
    while x < U(x1):
        l.rect('ra-cano', x, x + 0.5, f0, f1)
        x += paso

def vidrios(l, x0, x1, y0, y1, paso=7):
    # Vidrio corrido con carpintería fina.
    R(l, 'ra-vidrio', x0, x1, y0, y1)
    x = U(x0) + 3
    while x < U(x1) - 1:
        l.rect('ra-carpinteria', x, x + 0.25, F(y0), F(y1))
        x += paso

def piedra(l, x0, x1, f0, f1, semilla):
    # Piedra seca: hiladas de dos filas, piezas de largo variado en tres tonos, con junta oscura.
    r = random.Random(semilla)
    a, b = U(x0), U(x1)
    for f in range(f0, f1, 2):
        x = a - r.choice((0, 1, 2))
        while x < b:
            largo = r.choice((3, 4, 4.5, 5, 6, 7))
            l.rect(r.choice(('ra-p1', 'ra-p2', 'ra-p3', 'ra-p2')), max(a, x), min(b, x + largo), f, min(f + 2, f1))
            l.rect('ra-junta', max(a, x + largo - 0.5), min(b, x + largo), f, min(f + 2, f1))
            x += largo

def panza(l, x0, x1, y0, y1, curva):
    # Panza de una losa redonda: en sombra, cada fila más corta a la derecha (la curva que se va) y más oscura.
    f0, f1 = F(y0), F(y1)
    n = max(1, f1 - f0)
    for i in range(n):
        der = x1 - curva * ((i + 1) / n) ** 1.6
        tono = ('ra-panza', 'ra-panza-o', 'ra-sombra')[min(2, i * 3 // n)]
        l.rect(tono, U(x0), U(der), f0 + i, f0 + i + 1)
        l.rect('ra-sombra', U(der) - 2, U(der), f0 + i, f0 + i + 1)

def losa(l, x0, x1, y0, y1):
    # Canto de losa: blanco con luz, la punta derecha redondeada y en sombra.
    redondo(l, 'ra-canto', x0, x1, y0, y1, cola=90, tonos=('ra-blanco', 'ra-s1', 'ra-s2'))
    l.rect('ra-s1', U(x0), U(x1) - 6, F(y1) - 1, F(y1))
    for f, m in ((F(y0), 1.5), (F(y1) - 1, 1)):
        l.rect('-', U(x1) - m, U(x1), f, f + 1)

def version():
    l = Lienzo(LARGO, FILAS)
    # El tambor de arriba, con sus ventanas, y la baranda de la terraza que lo rodea.
    redondo(l, 'ra-blanco', 470, 935, 122, 268, cola=130)
    R(l, 'ra-canto', 470, 880, 122, 128)
    R(l, 'ra-vidrio', 705, 815, 222, 252); R(l, 'ra-carpinteria', 758, 762, 222, 252)
    R(l, 'ra-vidrio', 518, 560, 190, 212)
    baranda(l, 412, 1030, 205, 262)
    # Losa de arriba: canto blanco grueso y panza en sombra que se curva hacia la derecha.
    losa(l, 400, 1042, 262, 300)
    panza(l, 412, 1040, 300, 372, curva=40)
    # Piso del medio: vidrios corridos, baranda y la losa con su panza grande.
    vidrios(l, 414, 1030, 372, 438)
    redondo(l, 'ra-vidrio', 960, 1030, 372, 438, cola=70, tonos=('ra-vidrio', 'ra-sombra'))
    baranda(l, 414, 1046, 380, 438)
    losa(l, 400, 1058, 436, 474)
    panza(l, 412, 1058, 474, 560, curva=80)
    vidrios(l, 450, 980, 540, 575, paso=9)
    # La lámina alta (a la izquierda, iluminada), con su canto en sombra.
    R(l, 'ra-blanco', 280, 412, 110, 630)
    R(l, 'ra-canto', 280, 400, 110, 118)
    R(l, 'ra-s1', 396, 412, 110, 630)
    # El cuerpo bajo de la izquierda y la rampa en arco (una fila por paso) con su baranda, sobre el pilar.
    R(l, 'ra-blanco', 205, 282, 405, 560)
    R(l, 'ra-s2', 205, 282, 405, 412)
    R(l, 'ra-blanco', 262, 400, 555, 632)
    fa, fb = F(447), F(562)
    for j, f in enumerate(range(fa, fb)):
        t = j / (fb - fa)
        xa = U(405 - (405 - 232) * t ** 0.8) - 1      # más tendida abajo: un arco
        l.rect('ra-canto', xa, xa + 3, f, f + 1)
        l.rect('ra-panza', xa, xa + 3, f + 1, f + 3)
        l.rect('ra-cano', xa + 1, xa + 1.5, f - 7, f)
        l.rect('ra-cano', xa, xa + 3, f - 8, f - 7)
    R(l, 'ra-sombra', 262, 300, 575, 632)                     # el hueco bajo el arco
    # Muro de piedra seca: la terraza baja de la izquierda y el muro curvo alto del cuerpo redondo.
    piedra(l, 150, 1090, F(628), F(LAGO), 3)
    piedra(l, 420, 1090, F(562), F(628), 7)
    R(l, 'ra-sombra', 420, 1090, 562, 568)
    R(l, 'ra-mata', 1060, 1090, 500, 600); R(l, 'ra-mata-o', 1072, 1090, 540, 600)
    # El lago con ondas.
    l.rect('ra-lago', 0, LARGO, F(LAGO), FILAS)
    r = random.Random(5)
    for f in range(F(LAGO) + 1, FILAS, 2):
        x = r.uniform(0, 8)
        while x < LARGO:
            largo = r.choice((3, 4, 6, 8))
            l.rect('ra-onda', x, min(LARGO, x + largo), f, f + 1)
            x += largo + r.choice((6, 9, 12, 15))
    return {'nota': ('La Villa La Roccia de Luigi Vietti (Cannobio, Lago Maggiore), de frente, como en la foto de época: '
                     'la lámina alta y la rampa en arco a la izquierda; el cuerpo redondo con el tambor de arriba, dos losas '
                     'muy voladas de canto blanco y panza en sombra, barandas de caño y vidrios corridos; el muro de piedra '
                     'seca, la mata, las rocas y el lago.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

COLORES = {
    'ra-blanco': ('#efebe2', '#efebe2'), 'ra-canto': ('#fbf9f3', '#fbf9f3'),
    'ra-s1': ('#d9d3c7', '#d9d3c7'), 'ra-s2': ('#bdb6a9', '#bdb6a9'), 'ra-s3': ('#9f988c', '#9f988c'),
    'ra-panza': ('#77736c', '#77736c'), 'ra-panza-o': ('#5f5b55', '#5f5b55'), 'ra-sombra': ('#45423e', '#45423e'),
    'ra-vidrio': ('#2f3232', '#2f3232'), 'ra-carpinteria': ('#8d8a84', '#8d8a84'), 'ra-cano': ('#dcd8cf', '#dcd8cf'),
    'ra-p1': ('#8f8778', '#8f8778'), 'ra-p2': ('#9c9483', '#9c9483'), 'ra-p3': ('#827a6c', '#827a6c'),
    'ra-junta': ('#625c52', '#625c52'), 'ra-roca': ('#5a5650', '#5a5650'),
    'ra-mata': ('#4c5e37', '#4c5e37'), 'ra-mata-o': ('#384629', '#384629'),
    'ra-lago': ('#56656a', '#34444a'), 'ra-onda': ('#7c8b8d', '#56676c'),
    'racionalismo-ocre': ('#c9893f', '#4a3214'), 'racionalismo-ocre-marco': ('#2b2117', '#f1e3cf'),
}

p = version()
p.update(placa='racionalismo-ocre', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
         marco='racionalismo-ocre-marco')
guardar(sys.argv[1], 'estilos', 'Racionalismo', p, COLORES, 'ra-|racionalismo-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
