# Casas Estudio de Diego Rivera y Frida Kahlo (Juan O'Gorman, San Ángel, Ciudad de México), de frente desde la
# calle, medidas en px sobre referencias/simbolos/racionalismo/images (2).jpeg (636 de ancho). A la izquierda, la casa
# blanca de Diego, los tanques rojos y el caño; en el medio, el
# cuerpo blanco bajo, los pilotes y el puente con baranda roja; a la derecha, el cubo azul de Frida con ventanales de
# marco rojo y baranda en la azotea; el portón. Delante, el cerco de cactus órgano, el tezontle y la vereda.
# Uso: ogorman.py <simbolos.json> (pone estilos."Racionalismo").
import sys, random
from armar import Lienzo, guardar

X0, X1, Y0 = 12, 615, 30
LARGO = 210
S = LARGO / (X1 - X0)
SUELO = 318                                          # donde termina el cerco y empieza el tezontle (px)
FILAS = round((350 - Y0) * S) + 1

def U(x): return round((x - X0) * S * 4) / 4
def F(y): return round((y - Y0) * S) + 1
def R(l, c, x0, x1, y0, y1): l.rect(c, U(x0), U(x1), F(y0), F(y1))

def ventanal(l, x0, x1, y0, y1, marco, paso=3, cortinas=(), filas=0):
    # Ventanal de hierro: vidrio oscuro, marco y parantes cada `paso` unidades; algunos paños con cortina.
    a, b, f0, f1 = U(x0), U(x1), F(y0), F(y1)
    l.rect(marco, a - 0.5, b + 0.5, f0 - 1, f1 + 1)
    l.rect('og-vidrio', a, b, f0, f1)
    for k in cortinas:
        l.rect('og-cortina', a + k * paso + 0.25, min(b, a + (k + 1) * paso), f0, f1)
    x = a + paso
    while x < b - 0.5:
        l.rect(marco, x, x + 0.5, f0, f1)
        x += paso
    if marco == 'og-hierro': l.rect('og-gris', a - 1, b + 1, f1 + 1, f1 + 2)    # alféizar
    filas = filas or (2 if f1 - f0 > 5 else 1)
    for k in range(1, filas):                                    # travesaños parejos
        f = f0 + round(k * (f1 - f0) / filas)
        l.rect(marco, a, b, f, f + 1)

def baranda(l, x0, x1, y0, y1, paso=10):
    # Baranda de caño rojo fino y baja: un caño arriba y parantes delgados (60 % del alto medido).
    a, b, f1 = U(x0), U(x1), F(y1)
    f0 = f1 - max(2, round((F(y1) - F(y0)) * 0.6))
    l.rect('og-rojo', a, b, f0, f0 + 1)
    x = a
    while x <= b - 0.25:
        l.rect('og-rojo', x, x + 0.25, f0, f1)
        x += paso
    l.rect('og-rojo', b - 0.25, b, f0, f1)

def version():
    l = Lienzo(LARGO, FILAS)
    # Casa de Diego: el cuerpo blanco con su cornisa y sus ventanas.
    R(l, 'og-blanco', 18, 182, 98, SUELO)
    R(l, 'og-gris', 14, 186, 95, 100)
    for y0, y1, tramos in ((114, 132, ((28, 76), (122, 170))), (155, 173, ((28, 62), (80, 112), (130, 170))),
                           (214, 248, ((28, 75), (80, 112), (122, 170)))):
        for a, b in tramos:
            ventanal(l, a, b, y0, y1, 'og-hierro')
    R(l, 'og-sombra', 18, 182, 100, 103)
    R(l, 'og-sombra', 176, 182, 100, SUELO)                          # canto en sombra (luz desde la izquierda)
    # Tanques rojos sobre su bastidor, y el caño (bajan hasta el techo).
    for x in (82, 116): R(l, 'og-gris', x, x + 3, 64, 95)
    R(l, 'og-gris', 80, 121, 64, 67)
    for a, b in ((84, 100), (101, 117)):
        R(l, 'og-rojo', a, b, 44, 64); R(l, 'og-rojo-o', b - 4, b, 44, 64); R(l, 'og-rojo-o', a, b, 44, 46)
        R(l, 'og-rojo-l', a, a + 3, 46, 64); R(l, 'og-rojo-o', a, b, 54, 56)
    R(l, 'og-rojo', 121, 131, 34, 95); R(l, 'og-rojo-o', 128, 131, 34, 95); R(l, 'og-rojo-o', 119, 133, 30, 36)
    # Cuerpo blanco bajo del medio, con su ventana corrida y la baranda de la terraza.
    R(l, 'og-blanco', 182, 330, 142, SUELO)
    R(l, 'og-gris', 182, 332, 139, 144)
    R(l, 'og-sombra', 182, 186, 144, SUELO)
    ventanal(l, 250, 318, 160, 178, 'og-hierro')
    ventanal(l, 250, 318, 214, 248, 'og-hierro')
    R(l, 'og-sombra', 324, 330, 144, SUELO)
    baranda(l, 236, 300, 118, 139)
    # Pilotes y puente gris con baranda roja, que sube hasta la azotea azul.
    R(l, 'og-gris', 290, 386, 138, 150); R(l, 'og-sombra', 290, 386, 148, 150)
    baranda(l, 292, 383, 116, 138)
    # La casa azul de Frida: el cubo, la baranda de la azotea, el tanquecito y los ventanales de marco rojo.
    R(l, 'og-azul', 383, 560, 117, SUELO)
    R(l, 'og-azul-o', 554, 560, 117, SUELO)
    R(l, 'og-azul-o', 383, 560, 117, 120)
    R(l, 'og-azul-base', 383, 560, 290, SUELO)
    R(l, 'og-azul-o', 383, 560, 193, 196)                            # entrepiso
    baranda(l, 383, 556, 90, 117, paso=11)
    R(l, 'og-rojo', 466, 486, 104, 117); R(l, 'og-rojo-o', 482, 486, 104, 117)
    ventanal(l, 391, 466, 131, 163, 'og-rojo', paso=4.25, filas=2, cortinas=(1,))
    ventanal(l, 473, 553, 123, 190, 'og-rojo', paso=4.25, filas=3, cortinas=(0, 4))
    ventanal(l, 392, 468, 200, 234, 'og-rojo', paso=4.25, filas=2)
    ventanal(l, 476, 555, 198, 232, 'og-rojo', paso=4.25, filas=2, cortinas=(3,))
    # El portón: pilares grises, losa volada con su sombra y cuatro hojas claras de marco rojo, con manija.
    R(l, 'og-cerco', 510, 520, 246, 334); R(l, 'og-cerco', 605, 615, 246, 334)
    R(l, 'og-gris', 504, 618, 238, 246); R(l, 'og-sombra', 510, 615, 246, 249)
    R(l, 'og-sombra', 520, 605, 249, 334)
    for k in range(4):
        a = 521 + k * 21
        R(l, 'og-rojo', a, a + 20, 252, 332)
        R(l, 'og-porton', a + 3, a + 17, 256, 328)
        R(l, 'og-porton-s', a + 3, a + 17, 256, 259)
    R(l, 'og-hierro', 559, 562, 286, 296); R(l, 'og-hierro', 563, 566, 286, 296)
    # El cerco de cactus órgano: columnas de altos distintos, con una costilla clara y el borde en sombra.
    r = random.Random(8)
    x = 14
    while x < 500:
        ancho = r.choice((6, 7, 8))
        tope = r.choice((246, 254, 260, 266, 272, 280))
        a, b = U(x), U(x + ancho)
        ft = F(tope)
        l.rect('og-cactus', a + 0.5, b - 0.5, ft, ft + 1)                 # punta redondeada
        l.rect('og-cactus', a, b, ft + 1, F(SUELO))
        l.rect('og-cactus-o', a, a + 0.5, ft + 1, F(SUELO))
        l.rect('og-cactus-l', a + (b - a) / 3, a + (b - a) / 3 + 0.25, ft + 1, F(SUELO))
        l.rect('og-cactus-l', a + 2 * (b - a) / 3, a + 2 * (b - a) / 3 + 0.25, ft + 2, F(SUELO))
        l.rect('og-cactus-l', a + 0.5, b - 0.5, ft, ft + 1)
        x += ancho + r.choice((4, 6, 8))
    # Tezontle rojo, cordón y vereda.
    l.rect('og-tezontle', 0, U(505), F(SUELO), F(336))
    l.rect('og-vereda', U(505), LARGO, F(330), F(336))
    l.rect('og-cordon', 0, LARGO, F(336), F(338))
    l.rect('og-vereda', 0, LARGO, F(338), FILAS)
    r = random.Random(3)
    for f in range(F(SUELO), F(336)):
        x = r.uniform(0, 3)
        while x < U(505):
            l.rect('og-tezontle-o', x, x + 0.5, f, f + 1)
            x += r.choice((2, 3, 4.5))
    for x in range(6, LARGO, 14): l.rect('og-junta', x, x + 0.25, F(338), FILAS)
    # La farola verde de la vereda, delante del cuerpo del medio.
    P = U(216)
    l.rect('og-farola', P - 0.5, P + 0.5, F(70), F(338))
    l.rect('og-farola', P - 1, P + 1, F(300), F(338))
    l.rect('og-farola', P - 1.5, P + 1.5, F(56), F(60))
    l.rect('og-farol', P - 1.25, P + 1.25, F(60), F(68))
    l.rect('og-farola', P - 1.5, P + 1.5, F(68), F(70))
    return {'nota': ('Las Casas Estudio de Diego Rivera y Frida Kahlo (Juan O\'Gorman, San Ángel), de frente desde la '
                     'calle: la casa blanca de Diego, los tanques y el '
                     'caño; el cuerpo bajo y el puente de baranda roja; el cubo azul de Frida con ventanales '
                     'de marco rojo; el portón, el cerco de cactus órgano, la farola, el tezontle y la vereda.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

COLORES = {
    'og-blanco': ('#efede6', '#efede6'), 'og-gris': ('#a9a7a0', '#a9a7a0'), 'og-sombra': ('#c9c6bd', '#c9c6bd'),
    'og-techo': ('#d8d5cc', '#d8d5cc'), 'og-vidrio': ('#2c3033', '#2c3033'), 'og-hierro': ('#5a5550', '#5a5550'),
    'og-cortina': ('#8f969c', '#8f969c'),
    'og-rojo': ('#b9483b', '#b9483b'), 'og-rojo-o': ('#93362c', '#93362c'), 'og-rojo-l': ('#cf6a5c', '#cf6a5c'),
    'og-azul': ('#3c78d0', '#3c78d0'), 'og-azul-o': ('#2c5ea8', '#2c5ea8'), 'og-azul-base': ('#2a3f66', '#2a3f66'),
    'og-cerco': ('#bdb8ac', '#bdb8ac'), 'og-porton': ('#e4ddd2', '#e4ddd2'), 'og-porton-s': ('#c9c1b3', '#c9c1b3'),
    'og-cactus': ('#6f8c4c', '#6f8c4c'), 'og-cactus-o': ('#4f6837', '#4f6837'), 'og-cactus-l': ('#8fa766', '#8fa766'),
    'og-tezontle': ('#8e4a36', '#7a3f2e'), 'og-tezontle-o': ('#733a2a', '#5f3123'), 'og-vereda': ('#b3aea4', '#6f6b64'), 'og-cordon': ('#d9b74a', '#b39535'), 'og-junta': ('#9a958b', '#5d5a54'),
    'og-farola': ('#2f4a3a', '#5c7a66'), 'og-farol': ('#e8e2c8', '#e8d58a'),
    'racionalismo-ocre': ('#d39a4a', '#4a3214'), 'racionalismo-ocre-marco': ('#2b2117', '#f1e3cf'),
}

p = version()
p.update(placa='racionalismo-ocre', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
         marco='racionalismo-ocre-marco')
guardar(sys.argv[1], 'estilos', 'Racionalismo', p, COLORES, 'og-|ra-|racionalismo-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
