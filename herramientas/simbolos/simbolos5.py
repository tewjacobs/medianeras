# Ronda 6: Eames, Stoclet, Paimio, La Pedrera y CCK, medidos sobre sus fotos.
# Se corre sobre simbolos-ronda5.json.
import json, re, sys, math
origen, destino = sys.argv[1], sys.argv[2]
d = json.load(open(origen))

def f(x): return '%g' % round(x, 2)
def tramos(segs, total):
    out, x = [], 0
    for a, b, c in segs:
        a, b = max(a, x), min(b, total)
        if b - a < 0.01: continue
        if a > x + 0.005: out.append(f'- {f(a - x)}')
        out.append(f'{c} {f(b - a)}'); x = b
    if total - x > 0.005: out.append(f'- {f(total - x)}')
    return ', '.join(out) or f'- {f(total)}'
def fundir(celdas, paso):
    segs, i = [], 0
    while i < len(celdas):
        j = i
        while j < len(celdas) and celdas[j] == celdas[i]: j += 1
        if celdas[i]: segs.append((i * paso, j * paso, celdas[i]))
        i = j
    return segs

def por_rectangulos(regiones, x0, x1, y0, y1, filas, px_unidad, paso_px=3):
    """Regiones medidas sobre la foto (x0, x1, y0, y1, color), pintadas en orden (la última
    queda arriba). Devuelve una línea horizontal por fila, muestreada en el centro de la fila."""
    lineas = []
    alto_fila = (y1 - y0) / filas
    ancho = (x1 - x0) / px_unidad
    for i in range(filas):
        y = y0 + (i + 0.5) * alto_fila
        celdas = []
        for c in range(int((x1 - x0) / paso_px)):
            x = x0 + c * paso_px + paso_px / 2
            color = None
            for a, b, ya, yb, col in regiones:
                if a <= x < b and ya <= y < yb: color = col
            celdas.append(color)
        lineas.append(tramos(fundir(celdas, paso_px / px_unidad), ancho))
    return lineas

col = d['colores']
col.update({
  'panel-blanco': {'claro': '#e4ddd0', 'oscuro': '#ece6db'},
  'interior':     {'claro': '#b07a45', 'oscuro': '#c48c55'},
  'eames-azul':   {'claro': '#3c4fb0', 'oscuro': '#5566c4'},
  'stoclet-muro': {'claro': '#c4c8b8', 'oscuro': '#d3d6c8'},
  'stoclet-borde': {'claro': '#4b5a4f', 'oscuro': '#6f8072'},
  'cobre':        {'claro': '#6f9a86', 'oscuro': '#86b09c'},
  'toldo-naranja': {'claro': '#d9622b', 'oscuro': '#e2733c'},
  'toldo-verde':  {'claro': '#1f8a7a', 'oscuro': '#33a08f'},
  'pedrera':      {'claro': '#d2c6ad', 'oscuro': '#e0d6c0'},
  'pedrera-sombra': {'claro': '#a99c83', 'oscuro': '#bdb199'},
  'cck-piedra':   {'claro': '#c9c3b6', 'oscuro': '#dcd7cc'},
  'cck-columna':  {'claro': '#e1dcd2', 'oscuro': '#efebe4'},
  'ballena':      {'claro': '#56698a', 'oscuro': '#7286a8'},
  'ballena-2':    {'claro': '#687c9e', 'oscuro': '#8698b8'},
  'ballena-luz':  {'claro': '#c9d4e3', 'oscuro': '#dbe3ee'},
})
mu = d['decadas']['mundo']; ar = d['decadas']['argentina']

# ---------- Casa Eames (foto eames/) ----------
# Caja larga de x 110 a 505 y de y 100 a 230: estructura negra fina, siete paños por piso.
MONT = [110, 160, 258, 308, 358, 408, 458, 505]
ARRIBA = ['vidrio-claro', 'panel-blanco', 'reticula', 'reticula', 'eames-azul', 'reticula', 'reticula']
ABAJO = ['vidrio', 'interior', 'vidrio-claro', 'hierro', 'interior', 'rojo', 'reticula']
reg = [(110, 505, 100, 230, 'hierro')]
for (a, b), c1, c2 in zip(zip(MONT, MONT[1:]), ARRIBA, ABAJO):
    reg.append((a + 3, b - 2, 104, 163, c1))
    reg.append((a + 3, b - 2, 168, 227, c2))
# el paño blanco de arriba es doble (de 160 a 258, sin montante en el medio); el de abajo tiene uno
reg.append((160 + 3, 258 - 2, 104, 163, 'panel-blanco'))
reg.append((209, 211, 168, 227, 'hierro'))
# el rojo de abajo es un paño chico, con vidrio encima
reg.append((411, 456, 168, 196, 'vidrio-claro'))
eam = por_rectangulos(reg, 110, 505, 100, 230, 10, 12.5)
eam = [l.replace('reticula', 'vidrio-claro') if k % 3 else l.replace('reticula', 'hierro') for k, l in enumerate(eam)]
eam.append(f'follaje {f((505 - 110) / 12.5)}')
mu['1940'].update({
  'nota': 'Casa Eames (Charles y Ray Eames, 1949), medida sobre la foto: la caja larga de estructura negra fina con sus paños: arriba, el panel blanco doble, el azul y los vidrios con carpintería; abajo, los interiores cálidos, el paño oscuro con la cruz de arriostramiento y el rojo chico; adelante, el pasto.',
  'direccion': 'horizontal', 'alto': 132, 'grosor': 1, 'separacion': 0.3, 'lineas': eam})

# ---------- Palacio Stoclet (foto stoclet/) ----------
M, E, Rf, V = 'stoclet-muro', 'stoclet-borde', 'cobre', 'vidrio'
reg = [
  # ala izquierda con su techo de cobre
  (105, 345, 245, 395, M), (140, 345, 222, 250, Rf), (105, 345, 245, 250, E),
  (180, 235, 280, 305, Rf),                                            # la cupulita de cobre
  # cuerpo central, más alto, con la ventana alta de la escalera
  (340, 510, 192, 395, M), (340, 343, 192, 395, E), (507, 510, 192, 395, E), (340, 510, 192, 196, E),
  (356, 380, 196, 345, V), (404, 407, 196, 395, E),
  # la torre escalonada
  (370, 430, 120, 192, M), (370, 373, 120, 192, E), (427, 430, 120, 192, E),
  (380, 420, 100, 120, E), (390, 410, 88, 100, E),
  (345, 465, 178, 186, 'hierro'),                                      # la baranda de la terraza
  # ala derecha más baja, con ventanas de arco
  (540, 820, 258, 380, M), (540, 820, 258, 262, E), (540, 820, 290, 295, E),
  (610, 625, 290, 380, E), (800, 805, 258, 380, E),
  # el bajo de enfrente con el portal de arco
  (400, 620, 300, 395, M), (400, 620, 300, 304, E), (463, 498, 332, 375, V),
  # el cerco y los cercos verdes
  (95, 830, 380, 412, 'hierro'), (140, 190, 352, 395, 'follaje'), (240, 290, 352, 395, 'follaje'),
  (520, 585, 330, 412, 'follaje'), (840, 900, 290, 412, 'follaje'),
]
for x in range(150, 340, 40): reg.append((x, x + 14, 255, 272, V)); reg.append((x, x + 14, 300, 318, V))
for x in range(555, 800, 40): reg.append((x, x + 22, 266, 288, V))
for x in (455, 485): reg.append((x, x + 12, 205, 222, V)); reg.append((x, x + 12, 245, 262, V))
for x in (640, 680): reg.append((x, x + 32, 345, 360, V))
sto = por_rectangulos(reg, 95, 830, 88, 412, 16, 20)
sto.append(f'piedra {f((830 - 95) / 20)}')
mu['1900'].update({
  'nota': 'Palacio Stoclet (Josef Hoffmann, 1905–1911), medido sobre la foto: los volúmenes de mármol claro con los bordes marcados en bronce, el ala izquierda con su techo de cobre, el cuerpo central con la ventana alta de la escalera y la torre escalonada, el ala derecha más baja con ventanas de arco, el portal y, adelante, el cerco y los cercos verdes.',
  'direccion': 'horizontal', 'alto': 150, 'grosor': 1, 'separacion': 0.3, 'lineas': sto})

# ---------- Sanatorio de Paimio (foto paimio/) ----------
# De frente: el pabellón blanco de los pacientes, el doble de ancho que el ala de color y de la
# misma altura; entre los dos, una línea blanca alta; el ala de las terrazas con su remate
# curvo, las losas blancas, los toldos naranja y verde alternados y la escalera roja en la punta.
BLANCO_A, SEP, COLOR_A = 34, 1, 17
X0 = BLANCO_A + SEP
ANCHO_P = X0 + COLOR_A
pai = []
FILAS_P = 16
for i in range(FILAS_P):
    segs = [(BLANCO_A, X0, 'revoque')]                     # la línea blanca alta que los separa
    ultima = i == FILAS_P - 1
    # el pabellón de los pacientes
    if i == 0: segs.append((0, BLANCO_A, 'revoque'))
    elif ultima: segs.append((0, BLANCO_A, 'sombra'))
    elif (i - 1) % 3 == 0: segs.append((0, BLANCO_A, 'revoque'))
    else:
        x = 0.4
        while x < BLANCO_A - 0.4:
            segs += [(x - 0.4, x, 'revoque'), (x, min(x + 0.8, BLANCO_A), 'vidrio')]; x += 1.2
        segs.append((x - 0.4, BLANCO_A, 'revoque'))
    # el ala de las terrazas
    if i == 0: segs.append((X0 + 0.6, ANCHO_P - 0.6, 'revoque'))   # el remate curvo
    elif ultima: segs.append((X0, ANCHO_P, 'vidrio'))
    else:
        piso, j = (i - 1) // 3, (i - 1) % 3
        if j == 0: segs.append((X0, ANCHO_P, 'revoque'))
        elif j == 1: segs.append((X0, ANCHO_P, ('toldo-naranja' if piso % 2 == 0 else 'toldo-verde') if piso < 5 else 'vidrio'))
        else: segs += [(X0, ANCHO_P - 2.2, 'vidrio'), (ANCHO_P - 2.2, ANCHO_P - 1.4, 'rojo'), (ANCHO_P - 1.4, ANCHO_P, 'revoque')]
    pai.append(tramos(sorted(segs), ANCHO_P))
pai.append(f'follaje {ANCHO_P}')
mu['1930'].update({
  'nota': 'Sanatorio de Paimio (Alvar Aalto, 1929–1933), de frente: el pabellón blanco de los pacientes, el doble de ancho que el ala de color y de la misma altura, con su grilla de ventanas; entre los dos, una línea blanca alta; el ala de las terrazas con su remate curvo, las losas blancas, los toldos naranja y verde alternados y la escalera roja en la punta; el pasto adelante.',
  'direccion': 'horizontal', 'alto': 120, 'grosor': 1, 'separacion': 0.3, 'lineas': pai})

# ---------- La Pedrera (foto la pedrera/) ----------
# Líneas verticales: la fachada de piedra ondula de una línea a la otra; cada piso tiene sus
# ventanas oscuras y, en algunos tramos, los balcones de hierro; arriba, el ático con ventanitas,
# el techo ondulado y las chimeneas; abajo, la planta baja con sus aberturas.
ped = []
N = 34
for k in range(N):
    ola = lambda fase, amp: amp * math.sin(k * 0.36 + fase)
    segs = []                           # (largo, color), de arriba hacia abajo
    if k in (5, 6, 15, 16, 26):         # las chimeneas y guerreros
        segs += [('pedrera', 2.6)]
    segs += [('pedrera', 2.4 + ola(0, 1.2))]
    segs += [('vidrio', 0.5) if k % 4 == 1 else ('pedrera', 0.5), ('pedrera', 1.4)]   # el ático
    for piso in range(5):
        desfase = ola(piso * 1.1, 0.9)
        ventana = k % 5 in (1, 2)
        balcon = ventana and (k // 5 + piso) % 2 == 0
        segs += [('pedrera', 1.2 + desfase), ('vidrio' if ventana else 'pedrera', 1.8),
                 ('hierro' if balcon else 'pedrera-sombra', 0.8), ('pedrera', 1.2 - desfase)]
    segs += [('pedrera', 0.8), ('sombra' if k % 4 in (1, 2) else 'pedrera', 3.2)]
    ped.append(', '.join(f'{c} {f(l)}' for c, l in segs if l > 0.01))
mu['1910'].update({
  'nota': 'La Pedrera (Gaudí, 1906–1912), mirada en la foto: la fachada de piedra que ondula; cada piso con sus ventanas oscuras y, en algunos tramos, los balcones de hierro forjado; arriba, el ático con ventanitas, el techo ondulado y las chimeneas; abajo, la planta baja con sus aberturas.',
  'direccion': 'vertical', 'alinear': 'fin', 'alto': 160, 'grosor': 1, 'separacion': 0.3, 'lineas': ped})

# ---------- CCK (fotos Centro Cultural Kirschner/) ----------
# La década la define la Ballena Azul. El edificio se corta a la mitad: la mitad izquierda es la
# fachada medida sobre la foto; en lugar de la mitad derecha, la Ballena Azul con su forma real
# (redondeada, más ancha arriba, con el borde de la terraza encendido) sobre su núcleo de hormigón.
P_, C_, Z = 'cck-piedra', 'cck-columna', 'pizarra'
MITAD = 427
reg = [
  (160, MITAD, 230, 500, P_),
  (180, 355, 190, 232, Z),
  (410, MITAD, 110, 126, Z), (385, MITAD, 126, 150, Z), (370, MITAD, 150, 190, Z), (355, MITAD, 185, 232, P_),
  (160, MITAD, 230, 236, 'piedra'), (160, MITAD, 286, 292, 'piedra'), (160, MITAD, 448, 455, 'piedra'),
]
for x in (200, 240, 285, 330): reg.append((x - 7, x + 8, 200, 226, P_))
for fila_y in ((250, 274), (302, 336), (350, 388), (398, 440)):
    for x in range(180, 345, 30): reg.append((x, x + 14, fila_y[0], fila_y[1], 'vidrio'))
for fila_y in ((302, 336), (350, 388), (398, 440)): reg.append((392, 410, fila_y[0], fila_y[1], 'vidrio'))
for x in (362, 386, 412): reg.append((x - 5, min(x + 5, MITAD), 238, 352, C_))
PUERTAS = (180, 226, 272, 318, 391)
for x in PUERTAS: reg.append((x, x + 28, 478, 500, 'vidrio'))
# La ballena: medida sobre la foto, ancho arriba, se angosta y se redondea abajo.
CX, ARRIBA_B, ABAJO_B, MEDIO_ANCHO = 562, 205, 405, 126   # 260 de ancho por 200 de alto, como en la foto
ADENTRO = 436       # el eje recto del lado de adentro
NUCLEO = 625        # el núcleo, corrido hacia el extremo de afuera
def medio_ancho(y):
    t = (y - ARRIBA_B) / (ABAJO_B - ARRIBA_B)
    if not 0 <= t <= 1: return 0
    forma = (1 - abs(2 * t - 1) ** 5) ** (1 / 5)   # el lado de afuera: esquinas muy redondeadas
    return MEDIO_ANCHO * (1 - 0.14 * t) * (0.55 + 0.45 * forma)   # el de adentro queda recto
FILAS_C = 21   # así la escala vertical es la misma que la horizontal (14 px por unidad)
alto_fila = (500 - 110) / FILAS_C
cck = []
for i, linea in enumerate(por_rectangulos(reg, 160, 695, 110, 500, FILAS_C, 14)):
    y = 110 + (i + 0.5) * alto_fila
    mw = medio_ancho(y)
    extra = []
    if mw > 2:
        tono = 'ballena-luz' if y < ARRIBA_B + alto_fila * 0.8 else ('ballena' if i % 2 == 0 else 'ballena-2')
        # el lado de adentro (hacia el edificio) es recto: todas las líneas arrancan en el mismo eje
        extra.append(((ADENTRO - 160) / 14, (ADENTRO + 2 * mw - 160) / 14, tono))
    elif y > ABAJO_B - 4:
        ancho_nucleo = 24 - (y - ABAJO_B) * 0.06    # el núcleo de hormigón, hacia el extremo de afuera
        extra.append(((NUCLEO - ancho_nucleo - 160) / 14, (NUCLEO + ancho_nucleo - 160) / 14, 'hormigon'))
    # se suma la ballena a la línea de la fachada
    segs, x = [], 0
    for parte in [p.strip() for p in linea.split(',')]:
        c, l = parte.rsplit(' ', 1); l = float(l)
        if c != '-': segs.append((x, x + l, c))
        x += l
    cck.append(tramos(sorted(segs + extra), (695 - 160) / 14))
cck.append(f'piedra {f((695 - 160) / 14)}')
ar['2010'].update({
  'nota': 'Centro Cultural Kirchner (B4FS, 2015): el edificio cortado a la mitad. A la izquierda, la mitad de la fachada del antiguo Palacio de Correos (la cúpula, la mansarda, las columnas, las ventanas y las puertas de arco); a la derecha, en lugar de la otra mitad, la Ballena Azul con su forma real: recta del lado que viene del edificio, redondeada y más ancha arriba del lado de afuera, con el borde de la terraza encendido, sobre su núcleo de hormigón corrido hacia el extremo.',
  'direccion': 'horizontal', 'alto': 190, 'grosor': 1, 'separacion': 0.3, 'lineas': cck,
  'arcos': [{'color': 'vidrio', 'desde': round((x - 160) / 14, 2), 'hasta': round((x + 28 - 160) / 14, 2),
             'base': round((478 - 110) / alto_fila), 'flecha': 1.0, 'relleno': True} for x in PUERTAS]})

# Casa Curutchet: proyectada en 1949, terminada en 1953.
ar['1950']['anio'] = '1953'
ar['1950']['nota'] = ar['1950']['nota'].replace('(Le Corbusier, 1949–1953)', '(Le Corbusier; proyectada en 1949, terminada en 1953)')

s = json.dumps(d, ensure_ascii=False, indent=2)
s = re.sub(r'\{\s*"claro": ("[^"]+"),\s*"oscuro": ("[^"]+")\s*\}', r'{ "claro": \1, "oscuro": \2 }', s)
open(destino, 'w').write(s + '\n')
print('ok')
