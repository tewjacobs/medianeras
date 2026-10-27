# Casa Eames (1949), medida sobre referencias/simbolos/eames/eames.jpeg: 7 paños (el segundo doble).
# Mezcla filas horizontales (estructura y vidrios de arriba), rayas verticales (vidrios) y paños llenos
# (blanco, azul, rojo, madera). Escribe líneas, zonas y rectas en la década 1940 de Mundo.
import json, sys

COL, MOD = 0.5, 5.3
GROSOR, SEPARACION = 1.25, 0.35  # filas más altas: la casa se estira
PASO = GROSOR + SEPARACION
ARRIBA, FRANJA, ABAJO = range(1, 7), 7, range(8, 12)

# x de inicio de cada paño (el 2 es doble)
x, xs = COL, []
for doble in (0, 1, 0, 0, 0, 0, 0):
    xs.append(x); x += MOD * (2 if doble else 1) + COL * (1 if doble else 0) + COL
ANCHO = x

def fila(r):
    if r == 0: return [('hierro', ANCHO)]
    t = []
    def pano(color, largo=MOD): t.extend([(color, largo), ('hierro', COL)])
    t.append(('hierro', COL))
    pano('-')                                                                          # 1: galería abierta, solo la columna
    pano('hierro' if r == FRANJA else '-', 2 * MOD + COL)                              # 2: zonas
    pano('-')                                                                          # 3: rayas
    pano('panel-blanco' if r in (5, 6) else 'vidrio-claro' if r in ARRIBA else 'hierro' if r == FRANJA else '-')  # 4
    pano('sol' if r == FRANJA else '-')                                                # 5: zonas
    pano('panel-blanco' if r in (5, 6, 7) else 'vidrio-claro' if r in ARRIBA else '-') # 6
    pano('panel-blanco' if r in (5, 6, 7) else 'vidrio-claro')                         # 7
    out = []
    for c, l in t:
        if out and out[-1][0] == c: out[-1][1] += l
        else: out.append([c, l])
    return ', '.join(f'{c} {round(l, 2):g}' for c, l in out)

lineas = [fila(r) if r else f'hierro {ANCHO:g}' for r in range(12)] + [f'follaje {ANCHO:g}']
z = lambda color, desde, hasta, primera, ultima, **o: {'color': color, 'desde': round(desde, 2), 'hasta': round(hasta, 2), 'primera': primera, 'ultima': ultima, **o}
b2 = xs[1]
zonas = [
    z('panel-blanco', b2, b2 + 2 * MOD + COL, 1, 6),
    z('interior', b2, b2 + MOD, 8, 11, relleno='rayas'),
    z('interior', b2 + MOD + COL, b2 + 2 * MOD + COL, 8, 11),
    z('panel-blanco', b2 + MOD + COL + 1.2, b2 + MOD + COL + 2.2, 8, 8),
    z('vidrio-claro', xs[2], xs[2] + MOD, 1, 11, relleno='rayas'),
    z('hierro', xs[3], xs[3] + MOD, 8, 11),
    z('eames-azul', xs[4], xs[4] + MOD, 1, 6),
    z('madera', xs[4], xs[4] + MOD, 8, 11),
    z('vidrio-claro', xs[5], xs[5] + MOD, 8, 11, relleno='rayas'),
    z('rojo', xs[5], xs[5] + 3, 9, 10),
]
alto_x = 3 * PASO  # la cruz va de la línea 8 a la 11
rectas = [{'color': 'acero', 'desde': round(xs[3], 2), 'hasta': round(xs[3] + MOD, 2), 'base': 9.5, 'subida': round(s, 2)} for s in (alto_x, -alto_x)]

ruta = sys.argv[1]
texto = open(ruta).read()
i = texto.index('"1940": {', texto.index('"mundo"', texto.index('"decadas"')))
a = texto.index('"lineas": [', i); b = texto.index(']', a) + 1
lista = lambda nombre, cosas: f'"{nombre}": [\n' + ',\n'.join(' ' * 10 + json.dumps(c, ensure_ascii=False) for c in cosas) + '\n' + ' ' * 8 + ']'
for viejo in ('zonas', 'rectas'):  # si ya estaban, se sacan
    if texto[b:].startswith(f',\n        "{viejo}": ['): b = texto.index(']', b + 5) + 1
texto = texto[:a] + lista('lineas', lineas) + ',\n        ' + lista('zonas', zonas) + ',\n        ' + lista('rectas', rectas) + texto[b:]
open(ruta, 'w').write(texto)
json.loads(texto)
print(len(lineas), 'líneas, ancho', round(ANCHO, 2))
