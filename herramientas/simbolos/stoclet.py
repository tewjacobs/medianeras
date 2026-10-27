# Palacio Stoclet (Hoffmann, 1905–1911), medido en píxeles sobre referencias/simbolos/stoclet/stoclet.jpg
# (achicada a 1200 de ancho y recortada desde x 60, y 110): 15 px por unidad, filas de 19,5 px.
# Mármol en filas; ventanas, techos, torre, cipreses y reja en zonas.
import json, sys

X0, PX, Y0, PASO_PX = 70, 15, 5, 19.5
u = lambda x: round((x - X0) / PX * 2) / 2   # a una grilla de media unidad, para que todo alinee
fila = lambda y: int((y - Y0) // PASO_PX)
ANCHO = u(1060)
FILAS = 22

# Fachada de mármol por fila: tramos en px.
def fachada(r):
    if r <= 1: return []
    if r <= 3: return [(455, 500)]
    if r <= 6: return [(440, 515)]
    if r <= 11: return [(395, 620)]
    if r <= 14: return [(80, 620), (660, 1035)]
    if r <= 19: return [(70, 1055)]
    return []

def linea(r):
    if r == 21: return f'stoclet-muro {ANCHO:g}'   # murito de la reja
    t, x = [], X0
    for a, b in fachada(r):
        t += [('-', u(a) - u(x)), ('stoclet-muro', u(b) - u(a))]; x = b
    t.append(('-', ANCHO - u(x)))
    return ', '.join(f'{c} {round(l, 2):g}' for c, l in t if l > 0)

zonas = []
def z(color, x0, x1, r0, r1=None, **o):
    zonas.append({'color': color, 'desde': u(x0), 'hasta': u(x1), 'primera': r0, 'ultima': r1 if r1 is not None else r0, **o})

# Torre: estrías y estatuas de cobre arriba; baranda sobre el bloque.
z('cobre', 455, 500, 0, 1, relleno='rayas')   # torre: todo centrado en x 477
z('stoclet-borde', 455, 500, 2, 3, relleno='rayas', fondo='stoclet-muro')
z('stoclet-borde', 440, 515, 4, 5, relleno='rayas', fondo='stoclet-muro')
z('hierro', 400, 555, 6, relleno='rayas')
z('stoclet-muro', 557, 587, 6, 14)                       # chimenea de la derecha
# Techo de cobre del ala izquierda, que se abre hacia abajo, y su chimenea.
for r, (a, b) in zip((9, 10, 11), ((170, 395), (140, 395), (100, 395))): z('cobre', a, b, r)
z('stoclet-borde', 165, 178, 10, 11)
# Ventanas del ala izquierda (dos pisos) y la cúpula del mirador.
for a in (95, 140, 260, 305, 350):   # mismas ventanas, mismo paso
    b = a + 18
    z('vidrio', a, b, 13); z('vidrio', a, b, 15, 16)
z('cobre', 185, 245, 13); z('vidrio', 192, 238, 14, 16)
# Galería de entrada: alero de cobre y sombra debajo.
z('cobre', 70, 300, 17); z('sombra', 70, 300, 18, 19)
# Bloque central: ventanal de la escalera, ventanas chicas, ventana en arco y bordes de bronce.
z('vidrio', 415, 445, 7, 19); z('stoclet-muro', 429, 431, 7, 19)
z('vidrio', 540, 556, 10, 11); z('vidrio', 540, 556, 14)
z('vidrio', 560, 600, 17, 19)
for x, r0, r1 in ((395, 7, 19), (480, 7, 19), (620, 7, 14), (725, 15, 19), (815, 15, 19), (965, 15, 19)):
    z('stoclet-borde', x - 2, x + 2, r0, r1)
# Pabellón de la derecha: ventanas altas, cornisa y galería abierta en sombra.
for k in range(6): z('vidrio', 672 + k * 60, 672 + k * 60 + 36, 12, 13)   # pabellón: seis iguales
z('stoclet-borde', 660, 1035, 14)
z('hierro', 815, 965, 16); z('sombra', 815, 965, 17, 19)   # galería centrada en el pabellón
# Cipreses en cono y cercos.
for r, (a, b) in zip((15, 16, 17, 18), ((670, 685), (660, 695), (650, 705), (643, 712))): z('follaje', a, b, r)
z('follaje', 620, 722, 19, 20)
for c in (378, 457, 533, 600):
    for r, m in zip((16, 17, 18, 19), (5, 8, 11, 13)): z('follaje', c - m, c + m, r)
z('follaje', 110, 175, 18, 20); z('follaje', 255, 320, 18, 20)
# Reja adelante.
z('hierro', 70, 1060, 20, relleno='rayas')

lineas = [linea(r) for r in range(FILAS)]
ruta = sys.argv[1]
texto = open(ruta).read()
i = texto.index('"1900": {', texto.index('"mundo"', texto.index('"decadas"')))
a = texto.index('"lineas": [', i); b = texto.index(']', a) + 1
lista = lambda nombre, cosas: f'"{nombre}": [\n' + ',\n'.join(' ' * 10 + json.dumps(c, ensure_ascii=False) for c in cosas) + '\n' + ' ' * 8 + ']'
if texto[b:].startswith(',\n        "zonas": ['): b = texto.index(']', b + 5) + 1
texto = texto[:a] + lista('lineas', lineas) + ',\n        ' + lista('zonas', zonas) + texto[b:]
open(ruta, 'w').write(texto)
json.loads(texto)
print(len(lineas), 'líneas,', len(zonas), 'zonas, ancho', ANCHO)
