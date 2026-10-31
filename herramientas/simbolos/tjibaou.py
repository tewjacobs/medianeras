# Centro Cultural Tjibaou (Renzo Piano, Numea), medido sobre referencias/simbolos/cultura/images.jpeg (448 px de ancho).
# Tres "cases" de frente, en líneas verticales: una de cada tres es una costilla de madera que sube suelta por
# arriba del cuerpo hasta su punta; las de en medio son el cuerpo de tablillas horizontales (tabla y junta, como
# el rayado), la piel de adentro que asoma arriba y los aros de la reja. Abajo, la cáscara gris de cada case.
# Vistas un poco de costado (la cumbre corrida a la derecha) y con luz de la izquierda.
# Uso: tjibaou.py <simbolos.json> (reescribe programas.Cultural).
import json, re, sys

PASO = 3.5                                    # px entre líneas (línea de 1 y separación de 0.3)
PX = PASO / 1.3                               # px por unidad
X0, X1, Y0, PIE = 38, 372, 300, 447
CORRIDO = 0.5                                 # cuánto se corre la cumbre hacia la derecha (parte del medio ancho)
ANILLO = 9                                    # px entre los aros de la reja

# Cada case: centro, medio ancho, alto de lo más ancho, punta de las costillas y arranque del cuerpo (en el eje).
CASES = [
    {'cx': 92, 'a': 51, 'yw': 405, 'yt': 338, 'yc': 377, 'cascara': (92, 30, 408)},
    {'cx': 212, 'a': 60, 'yw': 400, 'yt': 306, 'yc': 353, 'cascara': (213, 35, 400)},
    {'cx': 327, 'a': 41, 'yw': 415, 'yt': 353, 'yc': 393, 'cascara': (328, 22, 418)},
]

def cumbre(c, dx, desde):                     # altura de la cúpula (de puntas o de cuerpo) a dx del eje
    # Vista un poco de costado: lo más alto corrido a la derecha, que cae empinado; a la izquierda baja largo y más bajo.
    s = CORRIDO * c['a']
    t = abs(dx - s) / (c['a'] - s if dx > s else c['a'] + s)
    p = 3 if dx > s else 1.8
    alto = (c['yw'] - desde) * (1 if dx > s else 0.6 + 0.4 * (1 - t))
    return c['yw'] - alto * max(0, 1 - t ** p) ** (1 / p)

def en_cascara(c, x, y):
    cx, w, tope = c['cascara']
    t = abs(x - cx) / w
    return t < 1 and y >= PIE - (PIE - tope) * (1 - t ** 2.5) ** (1 / 2.5)

def tono(c, x, y):                            # de claro (izquierda, al sol) a oscuro (derecha, en sombra)
    v = (x - c['cx']) / c['a'] + (y - c['yc']) / 140
    return 'tj-1' if v < -0.45 else 'tj-2' if v < 0.2 else 'tj-3'

def linea(k):
    x = X0 + (k + 0.5) * PASO
    c = min(CASES, key=lambda c: abs(x - c['cx']))
    dx = x - c['cx']
    if abs(dx) > c['a'] - 2: return '- 0.25'
    costilla = int(dx / PASO + 99.5001) % 3 == 0 or abs(dx) > c['a'] - 2 - PASO   # una de cada tres; las del borde, costillas
    salto = ((k * 2654435761) % 1000 / 1000 - 0.3) * 14 + (10 if k % 9 == 0 else 0)   # puntas desparejas, algunas más altas
    punta = cumbre(c, dx, c['yt']) - (salto if costilla else -6)
    cuerpo = cumbre(c, dx, c['yc'])
    dentro = cuerpo - 0.35 * (cuerpo - cumbre(c, dx, c['yt']))  # hasta acá se ven las tablillas de la piel de adentro
    sol = dx < CORRIDO * c['a']
    out = []
    for i in range(int((PIE - Y0) / PX * 4)):
        u = i * 0.25
        y = Y0 + (u + 0.125) * PX
        tabla = (y - Y0) % (1.3 * PX) < PX                     # tablillas y aros a la misma altura en todas las líneas
        if en_cascara(c, x, y):
            col = 'tj-cascara-c' if not en_cascara(c, x, y - 0.6 * PX) else 'tj-cascara' if costilla else 'tj-cascara-o'
        elif y < punta: col = '-'
        elif costilla: col = 'tj-costilla' if y < cuerpo else 'tj-costilla-c' if sol else 'tj-costilla-o'
        elif (y - Y0) % ANILLO < 0.3 * PX and y < cuerpo: col = 'tj-reja'
        elif y < dentro: col = '-'
        elif y < cuerpo: col = 'tj-dentro' if tabla else '-'
        else: col = tono(c, x, y) if tabla else 'tj-junta'
        if out and out[-1][0] == col: out[-1][1] += 0.25
        else: out.append([col, 0.25])
    while out and out[0][0] == '-': out.pop(0)                 # las líneas se alinean abajo
    return ', '.join(f'{c} {round(l, 2):g}' for c, l in out) or '- 0.25'

def version():
    lineas = [linea(k) for k in range(int((X1 - X0) / PASO))]
    while lineas and lineas[-1] == '- 0.25': lineas.pop()
    while lineas and lineas[0] == '- 0.25': lineas.pop(0)
    largo, travesia = round((PIE - Y0) / PX, 2), len(lineas) * 1.3 - 0.3
    aire = round((1.5 + 0.06 * max(largo, travesia)) * 10) / 10
    return {'direccion': 'vertical', 'alinear': 'fin', 'separacion': 0.3, 'largo': largo, 'placa': 'cultural-araucaria', 'aire': aire,
            'marco': 'cultural-araucaria-marco', 'lineas': lineas}

COLORES = {
    'tj-costilla': {'claro': '#e9c27e', 'oscuro': '#e9c27e'},
    'tj-costilla-c': {'claro': '#f3d9a4', 'oscuro': '#f3d9a4'},
    'tj-costilla-o': {'claro': '#b9844a', 'oscuro': '#b9844a'},
    'tj-reja': {'claro': '#b8834c', 'oscuro': '#b8834c'},
    'tj-1': {'claro': '#e6a95b', 'oscuro': '#e6a95b'},
    'tj-2': {'claro': '#cf7f3d', 'oscuro': '#cf7f3d'},
    'tj-3': {'claro': '#a75a2b', 'oscuro': '#a75a2b'},
    'tj-dentro': {'claro': '#9a5a2c', 'oscuro': '#9a5a2c'},
    'tj-junta': {'claro': '#7a3f1f', 'oscuro': '#7a3f1f'},
    'tj-cascara': {'claro': '#b9b2b3', 'oscuro': '#b9b2b3'},
    'tj-cascara-c': {'claro': '#dcd6d4', 'oscuro': '#dcd6d4'},
    'tj-cascara-o': {'claro': '#8d8689', 'oscuro': '#8d8689'},
}

p = version()
texto = open(sys.argv[1]).read()
colores = ''.join(f'    "{k}": {{ "claro": "{v["claro"]}", "oscuro": "{v["oscuro"]}" }},\n' for k, v in COLORES.items())
texto = re.sub(r'    "tj-[^"]+": \{[^}]*\},\n', '', texto)                  # los colores de antes, si estaban
i = texto.index('"colores": {') + len('"colores": {\n')
texto = texto[:i] + colores + texto[i:]
a = texto.index('    "Cultural": {', texto.index('"programas"'))
b = texto.index('\n    }', a) + len('\n    }')
nota = ('El Centro Cultural Tjibaou (Renzo Piano, Numea), de frente: tres "cases" de madera, cada una con sus costillas '
        'que suben sueltas hasta puntas desparejas, el cuerpo de tablillas al sol de un lado y en sombra del otro, '
        'la reja más arriba y la cáscara gris al pie.')
entrada = ('    "Cultural": {\n' + ',\n'.join([f'      "nota": {json.dumps(nota, ensure_ascii=False)}',
           *[f'      "{k}": {json.dumps(v)}' for k, v in p.items() if k != 'lineas'],
           '      "lineas": [\n' + ',\n'.join(f'        {json.dumps(l)}' for l in p['lineas']) + '\n      ]']) + '\n    }')
texto = texto[:a] + entrada + texto[b:]
json.loads(texto)
open(sys.argv[1], 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'])
