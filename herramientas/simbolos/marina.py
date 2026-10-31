# Marina City (Bertrand Goldberg, Chicago), medido sobre referencias/simbolos/marina city/ (stringio.jpg y la de 2021).
# Las dos torres mazorca, iguales y de frente, en líneas horizontales sin separación. Cada piso de departamentos
# son dos líneas: el canto del balcón cortado en pétalos y, abajo, la sombra del balcón con los lados claros, así
# cada pétalo es una U. Los pétalos se angostan hacia los bordes, como en un cilindro, con luz de la izquierda.
# Abajo, el piso de vidrio con columnas y la cochera en espiral: losas corridas, arcos y columnas. Más ancha.
# Uso: marina.py <simbolos.json> (reescribe programas.Vivienda colectiva).
import json, math, re, sys

R = 7.4                                       # radio de la torre con los balcones, en unidades
R_COCHERA = R                                 # la cochera, del ancho de los balcones
PISOS, COCHERAS = 24, 8
PETALOS = 16                                  # balcones en toda la vuelta
ENTRANTE = 1.1                                # cuánto se mete la sombra respecto del canto: el borde festoneado
HUECO = 4.5                                   # entre las dos torres
ANCHO = 2 * R_COCHERA

def tono(x, r):                               # canto según el ángulo: claro a la izquierda, oscuro a la derecha
    luz = math.cos(math.asin(max(-1, min(1, x / r))) + 0.6)
    return 'mc-1' if luz > 0.8 else 'mc-2' if luz > 0.35 else 'mc-3'

def cortes(r, n, corrido):                    # x de los bordes de cada pieza que se ve de frente
    xs = [r * math.sin(-math.pi / 2 + (k + corrido) * 2 * math.pi / n) for k in range(n // 2 + 1)]
    return [-r] + [x for x in xs if -r < x < r] + [r]

def pieza(tramos, color, largo):              # suma un tramo, juntándolo con el anterior si es del mismo color
    if largo <= 0: return
    if tramos and tramos[-1][0] == color: tramos[-1][1] += largo
    else: tramos.append([color, largo])

def fila(r, dibujo):                          # una línea de una torre: centrada en ANCHO, vacío a los costados
    t = []
    pieza(t, '-', ANCHO / 2 - r)
    for color, largo in dibujo: pieza(t, color, largo)
    pieza(t, '-', ANCHO / 2 - r)
    return t

def canto():                                  # el borde del balcón, cortado en pétalos
    xs = cortes(R, PETALOS, 0.5); d = []
    for k, (a, b) in enumerate(zip(xs, xs[1:])):
        j = min(0.2, (b - a) / 4)
        izq, der = (0 if k == 0 else j), (0 if k == len(xs) - 2 else j)   # sin junta contra el cielo
        d += [['mc-junta', izq], [tono((a + b) / 2, R), b - a - izq - der], ['mc-junta', der]]
    return fila(R, d)

def techo():                                  # la losa de arriba, metida como la sombra
    xs = cortes(R, PETALOS, 0.5)
    return fila(R - ENTRANTE, recortar([[tono((a + b) / 2, R), b - a] for a, b in zip(xs, xs[1:])], ENTRANTE))

def sombra():                                 # dentro del balcón: oscuro, con los lados de la U claros
    xs = cortes(R, PETALOS, 0.5); d = []
    for a, b in zip(xs, xs[1:]):
        lado = (b - a) * 0.07
        d += [[tono(a, R), lado], ['mc-sombra', b - a - 2 * lado], [tono(b, R), lado]]
    return fila(R - ENTRANTE, recortar(d, ENTRANTE))

def recortar(d, m):                           # saca m de cada punta: el canto asoma más que la sombra
    for _ in range(2):
        resto = m
        while resto > 0:
            quita = min(resto, d[0][1]); d[0][1] -= quita; resto -= quita
            if d[0][1] <= 0: d.pop(0)
        d.reverse()
    return d

def losa(r):
    xs = [-r + k * 2 * r / 12 for k in range(13)]
    return fila(r, [[tono((a + b) / 2, r), b - a] for a, b in zip(xs, xs[1:])])

def hueco(r, ancho_col, color):               # cochera o vidrio: oscuro con columnas bajo las juntas de los pétalos
    xs = cortes(r, PETALOS, 0.5)[1:-1]; d = []; x = -r
    for c in xs:
        w = ancho_col * math.cos(math.asin(c / r))
        d += [[color, c - w / 2 - x], [tono(c, r), w]]; x = c + w / 2
    d.append([color, r - x])
    return fila(r, d)

def torre():
    filas = [techo()] + [sombra(), canto()] * PISOS
    filas += [hueco(R - ENTRANTE - 0.4, 0.4, 'mc-vidrio')] * 2 + [losa(R_COCHERA)]    # piso de vidrio, metido
    filas += [hueco(R_COCHERA - 0.7, 0.9, 'mc-sombra'), hueco(R_COCHERA - 0.7, 0.35, 'mc-sombra'), losa(R_COCHERA)] * COCHERAS
    return filas

def texto_de(t): return ', '.join(f'{c} {round(l, 2):g}' for c, l in t)

def version():
    una = torre()
    lineas = [texto_de(f + [['-', HUECO]] + f) for f in una]
    lineas = [re.sub(r'(, - [\d.]+)+$', '', l) for l in lineas]
    largo, travesia = round(2 * ANCHO + HUECO, 2), len(lineas)
    aire = round((1.5 + 0.06 * max(largo, travesia)) * 10) / 10
    return {'direccion': 'horizontal', 'separacion': 0, 'largo': largo, 'placa': 'vivienda-ladrillo', 'aire': aire,
            'marco': 'vivienda-ladrillo-marco', 'lineas': lineas}

COLORES = {
    'mc-1': {'claro': '#f1ecdf', 'oscuro': '#f1ecdf'},
    'mc-2': {'claro': '#d3cab8', 'oscuro': '#d3cab8'},
    'mc-3': {'claro': '#8c8476', 'oscuro': '#8c8476'},
    'mc-junta': {'claro': '#5d5850', 'oscuro': '#5d5850'},
    'mc-sombra': {'claro': '#3b3834', 'oscuro': '#3b3834'},
    'mc-vidrio': {'claro': '#2c3134', 'oscuro': '#2c3134'},
}

p = version()
texto = open(sys.argv[1]).read()
colores = ''.join(f'    "{k}": {{ "claro": "{v["claro"]}", "oscuro": "{v["oscuro"]}" }},\n' for k, v in COLORES.items())
texto = re.sub(r'    "mc-[^"]+": \{[^}]*\},\n', '', texto)                  # los colores de antes, si estaban
i = texto.index('"colores": {') + len('"colores": {\n')
texto = texto[:i] + colores + texto[i:]
a = texto.index('    "Vivienda colectiva": {', texto.index('"programas"'))
b = texto.index('\n    }', a) + len('\n    }')
nota = ('Marina City (Bertrand Goldberg, Chicago), de frente: las dos torres mazorca, con los balcones en pétalos '
        'que se angostan hacia los bordes, el piso de vidrio con columnas y, abajo, la cochera en espiral.')
entrada = ('    "Vivienda colectiva": {\n' + ',\n'.join([f'      "nota": {json.dumps(nota, ensure_ascii=False)}',
           *[f'      "{k}": {json.dumps(v)}' for k, v in p.items() if k != 'lineas'],
           '      "lineas": [\n' + ',\n'.join(f'        {json.dumps(l)}' for l in p['lineas']) + '\n      ]']) + '\n    }')
texto = texto[:a] + entrada + texto[b:]
json.loads(texto)
open(sys.argv[1], 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'])
