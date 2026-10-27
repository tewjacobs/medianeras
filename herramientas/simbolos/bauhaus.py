# Bauhaus de Dessau (Gropius, 1925–1926): el frente de la entrada, medido sobre la vista de frente de
# referencias/simbolos/Bauhaus/ (y los colores de las fotos). El bloque gris lleno, con la losa de arriba,
# la columna de letras, las cuatro ventanas rojas con sus montantes, el alero, la puerta naranja y la
# escalera; atrás, a la izquierda, la columnita del ala; a la derecha, el anexo bajo, que tapa apenas al bloque.
import json, sys

X0 = 4.3            # lugar para la escalera, a la izquierda del bloque
BLOQUE, ANEXO = 20, 6
ANCHO = X0 + BLOQUE + ANEXO
FILAS = 25          # 0 a 24; la 25 es el pasto

def fila(r):
    if r == 0: t = [('-', X0 - 1.8), ('panel-blanco', 1.8 + BLOQUE + 0.4), ('-', ANEXO - 0.4)]
    else:
        t = [('-', ANCHO)]                                            # bloque, columna y anexo: zonas
        if r == 24: t = [('hormigon', X0), ('-', ANCHO - X0)]          # escalón de abajo
        elif r == 23: t = [('-', X0 - 3), ('hormigon', 3), ('-', ANCHO - X0)]
    out = []
    for c, l in t:
        if out and out[-1][0] == c: out[-1][1] += l
        else: out.append([c, l])
    return ', '.join(f'{c} {round(l, 2):g}' for c, l in out)

lineas = [fila(r) for r in range(FILAS)] + [f'follaje {ANCHO:g}']
z = lambda color, desde, hasta, primera, ultima=None, **o: {'color': color, 'desde': round(desde, 2), 'hasta': round(hasta, 2), 'primera': primera, 'ultima': ultima if ultima is not None else primera, **o}
v0, v1 = X0 + 10.4, X0 + 18.4   # ventanas
zonas = [
    z('bau-gris', X0, X0 + BLOQUE, 1, 24),                                         # bloque lleno
    *[z('blanco', X0 + 2, X0 + 4.3, r) for r in (5, 7, 9, 11, 13, 15, 17)],       # BAUHAUS
    *[z('bau-rojo', v0, v1, a, b) for a, b in ((3, 5), (9, 11), (15, 17), (21, 23))],
    *[z('blanco', x, x + 0.2, a, b) for a, b in ((3, 5), (9, 11), (15, 17), (21, 23)) for x in (v0 + 2, v0 + 4, v0 + 6)],
    z('panel-blanco', X0 - 1.4, X0 - 0.6, 1, 19),                                  # columnita del ala
    z('bau-anexo', X0 + BLOQUE - 0.8, ANCHO, 21, 24),                              # anexo, tapa un poco al bloque
    z('hierro', X0 - 2.5, X0 + 3.5, 20),                                           # alero
    z('sombra', X0, X0 + 3.5, 21, 24),                                             # entrada en sombra
    z('bau-puerta', X0 + 0.6, X0 + 2.4, 21, 24),                                   # puerta
]

ruta = sys.argv[1]
texto = open(ruta).read()
i = texto.index('"1920": {', texto.index('"mundo"', texto.index('"decadas"')))
a = texto.index('"lineas": [', i); b = texto.index(']', a) + 1
lista = lambda nombre, cosas: f'"{nombre}": [\n' + ',\n'.join(' ' * 10 + json.dumps(c, ensure_ascii=False) for c in cosas) + '\n' + ' ' * 8 + ']'
if texto[b:].startswith(',\n        "zonas": ['): b = texto.index(']', b + 5) + 1
texto = texto[:a] + lista('lineas', lineas) + ',\n        ' + lista('zonas', zonas) + texto[b:]
open(ruta, 'w').write(texto)
json.loads(texto)
print(len(lineas), 'líneas, ancho', round(ANCHO, 2))
