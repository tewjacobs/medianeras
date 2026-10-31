# 30 St Mary Axe (Foster + Partners), de frente, con el perfil medido sobre referencias/simbolos/St mary axe/790423.jpg
# (434 px de ancho; la base, tapada en la foto, se cierra con el 87 % del ancho máximo). Líneas horizontales sin
# separación. La piel se arma sobre un cilindro visto de frente (cada celda tiene su ángulo): la red de diagonales de
# acero blanco con una horizontal cada media malla, que forma los triángulos, y las seis bandas oscuras en espiral
# siguiendo esas diagonales. Arriba, la cúpula oscura con sus anillos; abajo, la planta baja vidriada y la vereda.
# Uso: smaxe.py <simbolos.json> (pone decadas.mundo.2000).
import sys, math
from armar import Lienzo, escribir, con_colores

FILAS, R = 100, 16                   # filas de la torre y medio ancho máximo
ANILLO = 15                          # fila del anillo de la cúpula
M, P = 18, 12                        # mallas alrededor (tres por espiral) y filas por malla
# Perfil: (altura de 0 a 1 desde la punta, medio ancho de 0 a 1), medido sobre la foto.
PERFIL = [(0, 0), (0.013, 0.2), (0.03, 0.32), (0.05, 0.41), (0.07, 0.48), (0.1, 0.55), (0.13, 0.6), (0.15, 0.63),
          (0.2, 0.7), (0.26, 0.77), (0.33, 0.84), (0.4, 0.9), (0.47, 0.94), (0.54, 0.98), (0.62, 1), (0.75, 0.98),
          (0.85, 0.95), (0.95, 0.9), (1, 0.87)]

def medio(t):
    for (a, ra), (b, rb) in zip(PERFIL, PERFIL[1:]):
        if a <= t <= b: return R * (ra + (rb - ra) * (t - a) / (b - a))
    return R * PERFIL[-1][1]

def version():
    l = Lienzo(2 * R + 1, FILAS + 3)
    C = R + 0.5
    for f in range(FILAS):
        h = medio((f + 0.5) / FILAS)
        if h < 0.5: continue
        for i in range(round((C - h) * 4), round((C + h) * 4)):
            x0, x1 = i / 4 - C, (i + 1) / 4 - C
            th = lambda x: math.asin(max(-1, min(1, x / h)))
            a0, a1 = th(x0) * M / (2 * math.pi), th(x1) * M / (2 * math.pi)
            borde = abs((x0 + x1) / 2) / h > 0.86
            d = (a1 - a0) * (1.2 if f >= ANILLO else 0)                       # las diagonales: de dos celdas en el tronco, finas en la cúpula
            cruza = lambda s: math.floor(a0 - d + s) != math.floor(a1 + s)    # una diagonal (una por malla) pasa por la celda
            sube, baja = cruza(f / P), cruza(-f / P)
            banda = math.floor((a0 + a1) / 2 - f / P) % 3 == 0                # las espirales oscuras
            if f < ANILLO:
                # La cúpula: la misma red sobre vidrio oscuro, con las diagonales claras que se juntan en la punta.
                if f in (ANILLO - 3, ANILLO - 1): c = 'sm-anillo'
                elif sube or baja: c = 'sm-cupula-l'
                elif f % (P // 2) == 0: c = 'sm-cupula-j'
                else: c = 'sm-cupula-o' if borde else 'sm-cupula'
            elif sube or baja:
                c = 'sm-linea-b' if banda else 'sm-linea-o' if borde else 'sm-acero'
            elif f % (P // 2) == 0:
                c = 'sm-linea-b' if banda else 'sm-junta'
            else:
                c = 'sm-oscuro' if banda else 'sm-vidrio-o' if borde else 'sm-vidrio'
            l.rect(c, i / 4, (i + 1) / 4, f, f + 1)
    l.rect('sm-punta', C - 0.5, C + 0.5, 0, 1)
    l.rect('sm-anillo', C - 0.25, C + 0.25, 1, 2)
    # La planta baja vidriada, metida, con sus columnas, y la vereda.
    h = medio(1) - 1
    l.rect('sm-hall', C - h, C + h, FILAS, FILAS + 2)
    for x in range(-int(h) + 1, int(h), 3):
        l.rect('sm-linea-o', C + x, C + x + 0.5, FILAS, FILAS + 2)
    l.rect('sm-vereda', 0, 2 * R + 1, FILAS + 2, FILAS + 3)
    return {'nota': ('30 St Mary Axe (Foster + Partners, 2001–2004), de frente, con el perfil medido sobre la foto: '
                     'angosta en la punta, más ancha un poco debajo de la mitad y apenas más angosta en la vereda. La piel '
                     'sobre el cilindro: la red de diagonales de acero blanco que forma triángulos y las seis bandas de '
                     'vidrio oscuro en espiral; arriba, la cúpula oscura con sus anillos; abajo, la planta baja vidriada.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': 2 * R + 1, 'lineas': l.lineas()}

COLORES = {
    'sm-vidrio': ('#7f9fb6', '#7f9fb6'), 'sm-vidrio-o': ('#587690', '#587690'), 'sm-junta': ('#adc3d3', '#adc3d3'), 'sm-acero': ('#eef1ee', '#eef1ee'),
    'sm-oscuro': ('#1f2a33', '#1f2a33'), 'sm-linea-o': ('#56656e', '#56656e'), 'sm-linea-b': ('#34424c', '#34424c'), 'sm-cupula': ('#24292e', '#24292e'), 'sm-cupula-o': ('#1b1f23', '#1b1f23'),
    'sm-cupula-l': ('#c4c6c4', '#c4c6c4'), 'sm-cupula-j': ('#3a3f44', '#3a3f44'),
    'sm-anillo': ('#d9dedc', '#d9dedc'), 'sm-punta': ('#c9d0cf', '#c9d0cf'), 'sm-hall': ('#3a4650', '#3a4650'),
    'sm-vereda': ('#9a948a', '#9a948a'),
}

ruta = sys.argv[1]
p = version()
p['aire'] = round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10
escribir(ruta, 'mundo', '2000', p, sacar=('grosor', 'alto', 'alinear', 'arcos', 'rectas', 'zonas'))
texto = con_colores(open(ruta).read(), COLORES, 'sm-')
open(ruta, 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'])
