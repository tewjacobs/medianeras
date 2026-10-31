# Estadio Monumental de River (Deportivo), desde arriba, medido sobre la foto cenital de referencias/simbolos/deportes/
# (Galeria-cenital-River-Plate.avif pasada a 1200 px de ancho) y simétrico sobre el centro (597, 309). Líneas
# horizontales sin separación: el óvalo de la bandeja alta con la banda roja, una cinta que va pegada al anillo por
# costados y cabeceras y se abre hacia afuera en las esquinas, el anillo oscuro, la bandeja baja con sus escaleras rojas,
# el pasto de las cabeceras, la pista y la cancha con franjas de corte y sus líneas.
# Uso: monumental.py <simbolos.json> (pone programas.Deportivo).
import sys, math
from armar import Lienzo, guardar

CX, CY = 597, 309
PX = 5                                             # px por unidad y por fila
X0, Y0 = CX - 396, CY - 318
N = 2.6                                            # el óvalo: entre elipse y rectángulo

def s(dx, dy, a, b, n=N): return (abs(dx / a) ** n + abs(dy / b) ** n) ** (1 / n)

def pista(dx, dy, r):
    # Distancia "de pista": rectas arriba y abajo y curvas en las puntas (centros a ±105 px del eje).
    ex = max(0, abs(dx) - 105)
    return math.hypot(ex, dy) / r

# Banda roja de la bandeja alta, calcada de la foto cenital y unida en una sola cinta: bordes de adentro y de afuera
# (0 junto al anillo, 1 en el borde) según el ángulo (0 en el medio del costado, 1 en el medio de la cabecera).
ROJO_ADENTRO = ((0, 0), (0.2, 0), (0.33, 0.03), (0.4, 0.16), (0.46, 0.4), (0.51, 0.66), (0.545, 0.86), (0.575, 0.97),
                (0.605, 0.86), (0.64, 0.6), (0.68, 0.24), (0.72, 0), (1, 0))
ROJO_AFUERA = ((0, 0.03), (0.08, 0.12), (0.2, 0.3), (0.3, 0.46), (0.4, 0.7), (0.47, 0.9), (0.52, 1.03), (0.63, 1.03),
               (0.68, 0.88), (0.75, 0.62), (0.83, 0.38), (0.92, 0.14), (1, 0.03))

def suave(t, puntos):
    # Curva suave (Catmull-Rom) que pasa por los puntos (t, valor).
    for k in range(len(puntos) - 1):
        (t1, v1), (t2, v2) = puntos[k], puntos[k + 1]
        if t <= t2:
            v0 = puntos[k - 1][1] if k else v1
            v3 = puntos[k + 2][1] if k + 2 < len(puntos) else v2
            u = (t - t1) / (t2 - t1)
            return 0.5 * (2 * v1 + (v2 - v0) * u + (2 * v0 - 5 * v1 + 4 * v2 - v3) * u * u + (3 * v1 - v0 - 3 * v2 + v3) * u ** 3)
    return puntos[-1][1]

def color(dx, dy):
    so = s(dx, dy, 393, 318)
    if so > 1: return '-'
    if so > 0.972: return 'mo-borde'
    sd = s(dx, dy, 297, 250)
    if sd > 1:                                     # bandeja alta
        r = (sd - 1) / ((sd - 1) + (1 - so))         # 0 adentro, 1 afuera
        phi = math.atan2(abs(dy) / 318, abs(dx) / 393) / (math.pi / 2)
        if suave(phi, ROJO_ADENTRO) <= r <= suave(phi, ROJO_AFUERA): return 'mo-rojo'
        th = math.atan2(dy, dx)
        if (th * 40 / math.pi) % 1 < 0.08: return 'mo-gris'
        return 'mo-blanco'
    if s(dx, dy, 279, 238) > 1: return 'mo-anillo'
    if s(dx, dy, 245, 196) > 1:                    # bandeja baja con sus escaleras
        th = math.atan2(dy, dx)
        return 'mo-rojo' if (th * 28 / math.pi) % 1 < 0.1 else 'mo-blanco'
    # Bancos de suplentes: dos techitos en el pasto detrás de la pista, a los lados de la mitad (solo de un lado).
    for cx in (-38, 38):
        if dy < 0 and abs(dx - cx) <= 18 and 147 <= -dy <= 162:
            return 'mo-banco-l' if -dy < 152 or abs(abs(dx - cx) - 18) < 1.5 else 'mo-banco'
    pt = pista(dx, dy, 143)
    if pt > 1: return 'mo-cesped'
    if pt > 112 / 143:                             # la pista, con dos líneas de carril
        u = (pt * 143 - 112) / 31
        tol = 0.05 + 0.03 * abs(dy) / 143
        return 'mo-carril' if min(abs(u - 1 / 3), abs(u - 2 / 3)) < tol else 'mo-pista'
    # Cancha: líneas y franjas de corte.
    ax, ay = abs(dx), abs(dy)
    v = PX * 0.25                                  # medio grosor de las líneas verticales (en px)
    h = PX / 2                                     # las horizontales ocupan una fila entera
    if ay <= 102 + h and ax <= 152 + v:
        if abs(ay - 102) <= h or abs(ax - 152) < v or ax < v: return 'mo-cal'
        if abs(math.hypot(dx, dy) - 32) < v + h * ay / 32: return 'mo-cal'
        for prof, alto in ((50, 62), (18, 28)):    # área grande y área chica
            if ax >= 152 - prof and ay <= alto + h and (abs(ax - (152 - prof)) < v or abs(ay - alto) <= h): return 'mo-cal'
    return 'mo-cesped' if int((dx + 600) // 26) % 2 else 'mo-cesped-o'

def version():
    filas = round(636 / PX)
    l = Lienzo(786 / PX, filas)
    for f in range(filas):
        y = Y0 + f * PX + PX / 2
        for i in range(l.n):
            x = X0 + (i + 0.5) * PX / 4
            l.c[f][i] = color(x - CX, y - CY)
    return {'nota': ('El Monumental de River, desde arriba: el óvalo de la bandeja alta con la banda roja que baja en diagonal '
                     'de las cabeceras y sigue por los costados, el anillo oscuro, la bandeja baja con sus escaleras rojas, '
                     'la pista de atletismo con sus carriles, los bancos de suplentes y la cancha con sus franjas y sus líneas: bordes, mitad, círculo central y áreas.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'mo-borde': ('#8f8f8a', '#8f8f8a'), 'mo-blanco': ('#e6e3db', '#e6e3db'), 'mo-gris': ('#bdbab2', '#bdbab2'),
    'mo-rojo': ('#cf3038', '#cf3038'), 'mo-anillo': ('#33343a', '#33343a'), 'mo-pista': ('#b8553d', '#b8553d'),
    'mo-carril': ('#e3a48f', '#e3a48f'), 'mo-banco': ('#3a3d44', '#3a3d44'), 'mo-banco-l': ('#c9ccd2', '#c9ccd2'),
    'mo-cesped': ('#3f8a3c', '#3f8a3c'), 'mo-cesped-o': ('#357a33', '#357a33'), 'mo-cal': ('#f2f0ea', '#f2f0ea'),
}

p = version()
p.update(placa='riv-suelo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='riv-suelo-marco')
guardar(sys.argv[1], 'programas', 'Deportivo', p, COLORES, 'mo-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
