# Museo Soumaya (Ciudad de México), medido sobre referencias/simbolos/museo/images (7).jpeg (700 px de ancho).
# Un reloj de arena torcido forrado de placas: la silueta sale de los bordes medidos fila por fila, la sombra
# es la lengua oscura que baja de arriba a la izquierda y las juntas de las placas, cortes escalonados
# (una fila sí y otra no, corridos media placa), como los hexágonos. Abajo solo el canto de acero que sigue el borde:
# sin zócalo ni jardín, el forro queda flotando. Uso: soumaya.py <simbolos.json> (reescribe programas.Museo).
import json, re, sys

PASO = 11                                     # px entre líneas (línea de 1 y separación de 0.3)
PX = PASO / 1.3                               # px por unidad
X0, X1, Y0, Y1 = 60, 650, 130, 590

def tramo(puntos, y):                         # interpola x en una lista [(y, x)]
    for (ya, xa), (yb, xb) in zip(puntos, puntos[1:]):
        if ya <= y <= yb: return xa + (xb - xa) * (y - ya) / (yb - ya)
    return None

IZQ = [(150, 73), (160, 73), (180, 92), (200, 112), (220, 128), (240, 144), (260, 154), (280, 167), (300, 172),
       (330, 180), (360, 184), (390, 182), (420, 176), (450, 166), (480, 155), (510, 142), (545, 125), (560, 150), (578, 200)]
DER = [(128, 615), (150, 610), (170, 596), (200, 575), (230, 556), (260, 537), (290, 523), (310, 515), (340, 513),
       (380, 515), (420, 522), (460, 540), (490, 565), (515, 600), (540, 640), (560, 560), (580, 470)]
SOMBRA = [(80, 155), (350, 148), (385, 260), (330, 372), (260, 330), (175, 290)]
BRILLO = [(250, 385), (440, 380), (480, 520), (330, 565), (140, 545), (180, 430)]

def dentro(poligono, x, y):
    c = False
    for (xa, ya), (xb, yb) in zip(poligono, poligono[-1:] + poligono[:-1]):
        if (ya > y) != (yb > y) and x < xa + (xb - xa) * (y - ya) / (yb - ya): c = not c
    return c

def suave(poligono, x, y, r=18):                               # 0 a 1, con el borde difuminado
    return sum(dentro(poligono, x + dx, y + dy) for dx in (-r, 0, r) for dy in (-r, 0, r)) / 9

def casco(x, y):                                               # dentro del forro de placas
    izq = 73 + (150 - y) / 22 * (615 - 73) if y < 150 else tramo(IZQ, y)
    der = tramo(DER, max(y, 128))
    return izq is not None and der is not None and izq <= x <= der and y < 578

def color(x, y):
    if casco(x, y):
        if y < 150 - (x - 73) / 542 * 22 + 10: return 'so-borde'          # filo claro de arriba
        if y > 500 and not casco(x, y + PASO): return 'so-canto'                    # canto de acero al pie del forro
        return 'placa'
    return None

TONOS = ['so-1', 'so-2', 'so-3', 'so-4', 'so-5']                # de oscuro a claro
PLACA, CORTE = 2.0, 0.35                                       # largo de placa y de junta, en unidades

def tono(x, y, n):
    # Cada placa entera con un tono: sombra y brillo difuminados más una variación propia de cada placa.
    v = 0.6 - 0.62 * suave(SOMBRA, x, y) + 0.3 * suave(BRILLO, x, y) + ((n * 2654435761) % 1000 / 1000 - 0.5) * 0.2
    return TONOS[max(0, min(4, int(v * 5)))]

def linea(puntos, corrido):
    # puntos: (x, y) en px, uno por cada 0.25 de largo; las juntas cortan solo las placas.
    out, guia = [], len(puntos) * 7919
    for i, (x, y) in enumerate(puntos):
        c = color(x, y)
        u = i * 0.25 + corrido
        if c == 'placa':
            n = int(u // PLACA) + guia
            c = 'so-junta' if u % PLACA >= PLACA - CORTE else tono(x - (u % PLACA) * PX + PLACA * PX / 2, y, n)
            if c == 'so-junta' and suave(SOMBRA, x, y) > 0.5: c = 'so-junta-o'
        c = c or '-'
        if out and out[-1][0] == c: out[-1][1] += 0.25
        else: out.append([c, 0.25])
    while out and out[-1][0] == '-': out.pop()
    return ', '.join(f'{c} {round(l, 2):g}' for c, l in out)

def version():
    paso_a = PX * 0.25                                         # muestreo a lo largo
    filas = int((Y1 - Y0) / PASO)
    largo = int((X1 - X0) / paso_a)
    lineas = [linea([(X0 + (k + 0.5) * paso_a, Y0 + r * PASO + PX / 2) for k in range(largo)], (r % 2) * PLACA / 2)
              for r in range(filas)]
    while lineas and not lineas[-1]: lineas.pop()
    return {'direccion': 'horizontal', 'separacion': 0.3, 'largo': round(largo * 0.25, 2), 'lineas': [l or '- 0.25' for l in lineas]}

COLORES = {
    'so-borde': {'claro': '#f4f3ef', 'oscuro': '#f4f3ef'},
    'so-1': {'claro': '#5f646b', 'oscuro': '#5f646b'},
    'so-2': {'claro': '#868c93', 'oscuro': '#868c93'},
    'so-3': {'claro': '#a9aeb4', 'oscuro': '#a9aeb4'},
    'so-4': {'claro': '#c6cacd', 'oscuro': '#c6cacd'},
    'so-5': {'claro': '#e3e5e6', 'oscuro': '#e3e5e6'},
    'so-junta': {'claro': '#8a9097', 'oscuro': '#8a9097'},
    'so-junta-o': {'claro': '#4b5058', 'oscuro': '#4b5058'},
    'so-canto': {'claro': '#eef0f1', 'oscuro': '#eef0f1'},
}

p = version()
texto = open(sys.argv[1]).read()
colores = ''.join(f'    "{k}": {{ "claro": "{v["claro"]}", "oscuro": "{v["oscuro"]}" }},\n' for k, v in COLORES.items())
texto = re.sub(r'    "so-[^"]+": \{[^}]*\},\n', '', texto)                  # los colores de antes, si estaban
i = texto.index('"colores": {') + len('"colores": {\n')
texto = texto[:i] + colores + texto[i:]
a = texto.index('    "Museo": {', texto.index('"programas"'))
b = texto.index('\n    }', a) + len('\n    }')
nota = ('El Museo Soumaya (Ciudad de México), de frente como en la foto: el reloj de arena torcido forrado de placas, '
        'en ladrillos de cinco grises, con la lengua de sombra que baja de arriba a la izquierda, el filo claro arriba '
        'y el canto de acero abajo.')
entrada = ('    "Museo": {\n' + ',\n'.join([f'      "nota": {json.dumps(nota, ensure_ascii=False)}',
           *[f'      "{k}": {json.dumps(v)}' for k, v in p.items() if k != 'lineas'],
           '      "lineas": [\n' + ',\n'.join(f'        {json.dumps(l)}' for l in p['lineas']) + '\n      ]']) + '\n    }')
texto = texto[:a] + entrada + texto[b:]
json.loads(texto)
open(sys.argv[1], 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'])
