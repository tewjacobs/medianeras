# Ronda 4: símbolos rehechos mirando las fotos de referencia. Reescribe solo esas entradas.
import json, re, sys, math
destino = sys.argv[1]
d = json.load(open(destino))

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
    """celdas: lista de colores (o None) cada `paso` unidades -> segmentos."""
    segs, i = [], 0
    while i < len(celdas):
        j = i
        while j < len(celdas) and celdas[j] == celdas[i]: j += 1
        if celdas[i]: segs.append((i * paso, j * paso, celdas[i]))
        i = j
    return segs

def vertical_desde_abajo(segs_abajo, alto):
    """segs (desde, hasta, color) medidos desde la vereda -> texto de arriba hacia abajo."""
    invertidos = sorted(((alto - b, alto - a, c) for a, b, c in segs_abajo))
    return tramos(invertidos, alto).lstrip()

col = d['colores']
col.update({
  'kava':         {'claro': '#b4ada1', 'oscuro': '#d9d4ca'},
  'kava-sombra':  {'claro': '#857e73', 'oscuro': '#9f998f'},
  'kava-vidrio':  {'claro': '#4a4843', 'oscuro': '#565a66'},
  'banco-vidrio': {'claro': '#536e69', 'oscuro': '#6c8a84'},
  'sombra':       {'claro': '#3b3a37', 'oscuro': '#2a2c33'},
  'vidrio-claro': {'claro': '#9fb6bb', 'oscuro': '#a9c1c6'},
  'vidrio-verde': {'claro': '#7ea69c', 'oscuro': '#8db3a9'},
  'puerta':       {'claro': '#c46a2e', 'oscuro': '#d07a3c'},
  'reja':         {'claro': '#3a3936', 'oscuro': '#6b6e78'},
  'vidrio-azul':  {'claro': '#3d5f8a', 'oscuro': '#5677a3'},
  'acero-azul':   {'claro': '#7d92ad', 'oscuro': '#9fb2ca'},
  'rojo-recoleta': {'claro': '#a63d2c', 'oscuro': '#bb4c38'},
  'tejas':        {'claro': '#6e2a1f', 'oscuro': '#8a3a2b'},
  'puente':       {'claro': '#8d939b', 'oscuro': '#ebe8e1'},
  'tensor':       {'claro': '#c4c7cc', 'oscuro': '#5f636c'},
  'titanio-2':    {'claro': '#7b858f', 'oscuro': '#9aa3ac'},
  'vidrio-gk':    {'claro': '#2e3d4c', 'oscuro': '#33475b'},
  'cctv':         {'claro': '#b9c3cc', 'oscuro': '#c9d2da'},
  'cctv-reticula': {'claro': '#3d4650', 'oscuro': '#4d5866'},
})
ar = d['decadas']['argentina']; mu = d['decadas']['mundo']

# ---------- Kavanagh (frente): cuerpo curvo a la izquierda, torre central, escalonado ----------
# Medido sobre el dibujo de referencia: 26 columnas; alturas en unidades (torre = 40).
PISO = 1.8
def zona_ventanas(a, b, muro, ventana):
    segs, y = [], a
    while y < b - 0.01:
        segs.append((y, min(b, y + PISO - 0.7), muro))
        segs.append((min(b, y + PISO - 0.7), min(b, y + PISO), ventana))
        y += PISO
    return segs
def kav_col(k):
    # (desde, hasta, tipo) por volumen, desde la vereda
    vol = []
    # alturas medidas sobre el dibujo (torre = 56): ala izquierda 0,53 · cuerpo medio 0,77 ·
    # ala derecha 0,46 y su último escalón 0,32 · la torre remata en dos escalones
    if k <= 3: vol.append((0, 29.5, 'curva'))
    elif k <= 10: vol.append((0, 29.5, 'ala'))
    if 6 <= k <= 18: vol.append((29.5 if k <= 10 else 0, 43, 'medio'))
    if 8 <= k <= 15: vol.append((43, {8: 52, 15: 52, 9: 54, 14: 54}.get(k, 56), 'torre'))
    if 19 <= k <= 23: vol.append((0, 26, 'ala'))
    if k >= 24: vol.append((0, 18, 'ala'))
    return vol
kav = []
for k in range(26):
    segs = [(0, 1.5, 'piedra')]
    for a, b, tipo in kav_col(k):
        a = max(a, 1.5)
        if tipo == 'curva':
            # el cuerpo curvo: bandas horizontales de ventanas, más oscuro hacia el borde
            muro = ['kava-sombra', 'kava-sombra', 'kava', 'kava'][k]
            segs += zona_ventanas(a, b - 0.6, muro, 'kava-vidrio') + [(b - 0.6, b, 'kava-sombra')]
        else:
            liso = k % 2 == 1 if tipo != 'torre' else k in (8, 11, 12, 15)
            muro = 'kava' if tipo != 'medio' or k % 4 else 'kava-sombra'
            if liso: segs.append((a, b - 0.6, muro))
            else: segs += zona_ventanas(a, b - 0.6, muro, 'kava-vidrio')
            segs.append((b - 0.6, b, 'kava-sombra'))  # la cornisa de cada retiro
    alto = max(b for _, b, _ in segs)
    kav.append(vertical_desde_abajo(segs, alto))
ar['1930'].update({
  'nota': 'Edificio Kavanagh (Sánchez, Lagos y de la Torre, 1934–1936), de frente: el cuerpo curvo a la izquierda con sus ventanas en bandas, el volumen que se escalona hacia los costados, la torre central con su remate y el basamento.',
  'direccion': 'vertical', 'alinear': 'fin', 'alto': 230, 'grosor': 1, 'separacion': 0.3, 'lineas': kav})
ar['1930'].pop('escala', None)

# ---------- Banco de Londres (frente sobre Reconquista) ----------
# En la foto: los pilares de hormigón son más anchos que las ranuras de vidrio, con agujeros
# ovalados; en la esquina, el gran volumen macizo vuela sobre una sombra con vigas.
bl = []
ALTO_BL = 30
for k in range(31):
    segs = [(0, 2, 'sombra')]  # planta baja retirada
    if k <= 9:
        segs += [(2, 14, 'banco-vidrio')]
        for y in (14, 15, 16): segs += [(y, y + 0.5, 'sombra'), (y + 0.5, y + 1, 'hormigon' if y < 16 else 'sombra')]
        segs += [(17, ALTO_BL, 'hormigon')]
    else:
        j = (k - 10) % 3
        if j == 2:
            segs += [(2, ALTO_BL - 1.5, 'banco-vidrio'), (ALTO_BL - 1.5, ALTO_BL, 'hormigon')]
        else:
            pilar = (k - 10) // 3
            alturas = [7, 14, 21] if pilar % 2 == 0 else [10.5, 17.5, 24]
            agujeros = [(y + (0.3 if j else 0), y + (2.2 if j else 2.5), 'sombra') for y in alturas]
            partes, y0 = [], 2
            for a, b, c in agujeros:
                partes += [(y0, a, 'hormigon'), (a, b, c)]; y0 = b
            partes.append((y0, ALTO_BL, 'hormigon'))
            segs += partes
    bl.append(vertical_desde_abajo(segs, ALTO_BL))
ar['1960'].update({
  'nota': 'Banco de Londres (Clorindo Testa con SEPRA, 1959–1966), llevado a una vista de frente: a la izquierda, la esquina con el gran volumen de hormigón que vuela sobre la sombra de sus vigas; a la derecha, los pilares anchos de la fachada con sus agujeros ovalados y las ranuras de vidrio verdoso entre ellos.',
  'direccion': 'vertical', 'alto': 170, 'grosor': 1, 'separacion': 0.3, 'lineas': bl})

# ---------- Casa Curutchet (frente) ----------
# Medida sobre la foto: 30 unidades de ancho. Montantes del marco y columnas en estas posiciones.
MONT = [2.3, 9, 15.4, 22.1, 28.6]
def marco(relleno, desde=2.3, hasta=29):
    segs = []
    for a, b in zip(MONT, MONT[1:]):
        segs += [(a, a + 0.5, 'revoque'), (a + 0.5, b, relleno)]
    segs.append((MONT[-1], MONT[-1] + 0.5, 'revoque'))
    return segs
def columnas(*xs): return [(x, x + 0.7, 'revoque') for x in xs]
cur = [
  tramos([(8.3, 30, 'revoque')], 30),                                          # losa-parasol
  tramos(columnas(14.2, 27.4), 30), tramos(columnas(14.2, 27.4), 30), tramos(columnas(14.2, 27.4), 30),
  tramos([(2.3, 28.6, 'revoque')], 30),                                       # viga de la terraza
  tramos(sorted([(13, 14.2, 'follaje'), (14.9, 17, 'follaje')] + [(x, x + 0.5, 'revoque') for x in MONT]), 30),
  tramos(sorted([(12.6, 14.2, 'follaje'), (14.9, 17.4, 'follaje')] + [(x, x + 0.5, 'revoque') for x in MONT]), 30),
  tramos(marco('reja'), 30), tramos(marco('reja'), 30),                         # barandas
  'revoque 30',
  tramos([(0, 2.3, 'vidrio-claro')] + marco('vidrio-claro') + [(29.1, 30, 'vidrio-claro')], 30),
  tramos([(0, 2.3, 'vidrio-claro')] + marco('vidrio-claro') + [(29.1, 30, 'vidrio-claro')], 30),
  'revoque 30',
  tramos([(0, 2.3, 'vidrio-verde')] + marco('vidrio-verde') + [(29.1, 30, 'vidrio-verde')], 30),
  tramos([(0, 2.3, 'vidrio-verde')] + marco('vidrio-verde') + [(29.1, 30, 'vidrio-verde')], 30),
  'revoque 30',
]
pb = lambda reja: tramos(sorted(columnas(0.9, 14.2, 22.8) + [(5, 5.6, 'revoque'), (6.2, 8.8, 'puerta'), (9.4, 10, 'revoque')]
                               + ([(10, 14.2, 'reja'), (14.9, 22.8, 'reja'), (23.5, 28.8, 'reja')] if reja else [])), 30)
cur += [pb(False), pb(False), pb(True), pb(True), 'piedra 30']
ar['1950'].update({
  'nota': 'Casa Curutchet (Le Corbusier, 1949–1953), de frente: la losa-parasol arriba sobre dos columnas finas, la terraza abierta con el álamo detrás, las barandas, los dos pisos de parasoles con su vidrio, y la planta baja con los pilotes, la puerta naranja y la reja.',
  'direccion': 'horizontal', 'alto': 200, 'grosor': 1, 'separacion': 0.45, 'lineas': cur})

# ---------- Casa sobre el Arroyo: arco más bajo y apoyado en la tierra ----------
arroyo = ['hormigon 30', 'hormigon 1, vidrio 28, hormigon 1', 'hormigon 30', '- 30', '- 30',
          'follaje 5, - 20, follaje 5', 'follaje 7, agua 16, follaje 7', 'follaje 9, agua 12, follaje 9']
paso = 1.6
ar['1940'].update({'lineas': arroyo,
  'nota': 'Casa sobre el Arroyo (Amancio Williams, 1943–1946): la caja con su ventana corrida, apoyada sobre un arco de hormigón bajo que salta el arroyo y apoya sus dos extremos en la tierra de cada orilla.',
  'arcos': [{'color': 'hormigon', 'desde': 2, 'hasta': 28, 'base': 5, 'flecha': round(5 * paso + 0.5 - (2 * paso + 1), 2), 'lineas': 2}]})

# ---------- SOMISA: más azulado ----------
ar['1970']['lineas'] = [l.replace('acero', 'acero-azul').replace('vidrio', 'vidrio-azul') for l in ar['1970']['lineas']]

# ---------- Recoleta: roja ----------
ar['1980']['lineas'] = [l.replace('revoque', 'rojo-recoleta').replace('ladrillo', 'tejas') for l in ar['1980']['lineas']]
ar['1980']['nota'] = 'Centro Cultural Recoleta (Testa, Bedel y Benedit, 1980): el antiguo convento reciclado, con sus muros rojos, el techo de tejas y la galería de arcos.'

# ---------- Puente de la Mujer: un solo mástil inclinado y los tirantes al tablero ----------
# Líneas horizontales: el mástil es una diagonal que nace en la pila y sube hacia la derecha,
# más grueso abajo; debajo de él, los tirantes en arpa hasta el tablero.
pm = []
ANCHO_PM, ARRIBA = 46, 16
for i in range(ARRIBA):
    t = (ARRIBA - 1 - i) / (ARRIBA - 1)        # 0 en el tablero, 1 en la punta
    xm = 12 + t * 24
    grueso = 4.2 - 3.4 * t
    segs = [(xm, xm + grueso, 'puente')]
    if i >= 2 and i % 3 == 2: segs.append((xm + grueso + 0.6, 36.5, 'tensor'))  # pocos tirantes, finos
    pm.append(tramos(segs, ANCHO_PM))
pm += ['puente 46', tramos([(0, 12, 'agua'), (12.6, 15.8, 'puente'), (16.4, 46, 'agua')], 46),
       tramos([(0, 12, 'agua'), (12.9, 15.5, 'puente'), (16.4, 46, 'agua')], 46), 'agua 46']
ar['2000'].update({
  'nota': 'Puente de la Mujer (Santiago Calatrava, 1998–2001): un solo mástil blanco que nace sobre la pila y sube inclinado, afinándose hasta la punta; debajo de él, los tirantes en arpa que bajan al tablero, y el agua del dique.',
  'direccion': 'horizontal', 'alto': 150, 'grosor': 1, 'separacion': 0.35, 'lineas': pm})

# ---------- Guggenheim Bilbao (desde la ría) ----------
# Silueta medida sobre la foto (píxeles): la sala larga con su proa a la izquierda y la ola
# del techo, la "flor" de piezas curvas en el centro, el volumen de la derecha.
def interp(puntos, x):
    for (x0, y0), (x1, y1) in zip(puntos, puntos[1:]):
        if x0 <= x <= x1: return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return None
SALA = [(85, 178), (200, 205), (300, 214), (400, 176), (470, 165), (500, 172)]
FLOR = [(450, 152), (480, 124), (510, 96), (560, 87), (610, 92), (640, 102), (655, 150), (700, 150), (735, 162)]
DERECHA = [(670, 206), (740, 200), (800, 210), (812, 232)]
gb = []
PX = 7
for i in range(21):
    y = 88 + i * 11.5 + 5
    celdas = []
    for c in range(int((812 - 60) / PX)):
        x = 60 + c * PX + PX / 2
        color = None
        if 322 <= y: color = 'caliza'
        elif 490 <= x <= 640 and y > 215: color = 'vidrio'
        elif 700 <= x <= 790 and y > 282: color = 'caliza'
        elif (t := interp(FLOR, x)) is not None and y > t: color = 'titanio' if (i // 3) % 2 == 0 else 'titanio-2'
        elif (t := interp(DERECHA, x)) is not None and y > t: color = 'titanio-2'
        elif (t := interp(SALA, x)) is not None and y > t: color = 'titanio' if y < 262 else 'titanio-2'
        celdas.append(color)
    gb.append(tramos(fundir(celdas, PX / 14), (812 - 60) / 14))
gb += [f'agua {f((812 - 60) / 14)}'] * 2
mu['1990'].update({
  'nota': 'Guggenheim Bilbao (Frank Gehry, 1993–1997), desde la ría: la sala larga a la izquierda, con su proa y el techo de titanio que ondula; en el centro, las piezas curvas que se apilan como una flor sobre el atrio de vidrio; a la derecha, el volumen más bajo y el bloque de piedra; abajo, el basamento y el agua.',
  'direccion': 'horizontal', 'alto': 170, 'grosor': 1, 'separacion': 0.25, 'lineas': gb})

# ---------- 30 St Mary Axe: 180 m de alto por 56 m de diámetro máximo ----------
WMAX = 10
ALTO_GK = WMAX * 180 / 56
N = 24
paso_gk = ALTO_GK / N
gk = []
for i in range(N):
    z = 1 - (i + 0.5) / N   # 0 = vereda, 1 = punta
    if z > 0.4: w = WMAX * math.sqrt(max(0, 1 - ((z - 0.4) / 0.6) ** 2))
    else: w = WMAX * (0.875 + 0.125 * z / 0.4)
    w = max(w, 0.8)
    celdas = []
    pasos = max(1, round(w / 0.25))
    for c in range(pasos):
        x = c / pasos
        fase = (x + i * 0.04) % (1 / 3)
        celdas.append('vidrio-gk' if fase < 0.12 else 'reflejo')
    segs = fundir(celdas, w / pasos)
    gk.append(', '.join(f'{c} {f(b - a)}' for a, b, c in segs))
mu['2000'].update({
  'nota': '30 St Mary Axe (Foster + Partners, 2001–2004): 180 m de alto por 56 m de diámetro en su parte más ancha, un poco por debajo de la mitad; se angosta apenas hacia la vereda y cierra en punta arriba. Las franjas de vidrio oscuro giran en espiral.',
  'direccion': 'horizontal', 'alinear': 'centro', 'alto': 200, 'grosor': 1, 'separacion': round(paso_gk - 1, 3), 'lineas': gk})

# ---------- CCTV (como en la foto): dos torres inclinadas unidas arriba y abajo ----------
ANCHO_CC, FILAS = 30, 22
cc = []
for i in range(FILAS):
    t = i / (FILAS - 1)   # 0 = arriba, 1 = abajo
    afuera_izq = 4.5 * (1 - t)            # las torres se inclinan hacia adentro al subir
    afuera_der = ANCHO_CC - 3.5 * (1 - t)
    hueco = None
    if 5 <= i <= 17:
        u = (i - 5) / 12
        hueco = (10.5 - 1.5 * u, 19.5 + 1.2 * u)
    celdas = []
    paso_c = 0.25
    for c in range(int(ANCHO_CC / paso_c)):
        x = c * paso_c + paso_c / 2
        if x < afuera_izq or x > afuera_der or (hueco and hueco[0] < x < hueco[1]): celdas.append(None); continue
        a = (x + i * 0.75) % 4
        b = (x - i * 0.75) % 4
        celdas.append('cctv-reticula' if a < 0.45 or b < 0.45 else 'cctv')
    cc.append(tramos(fundir(celdas, paso_c), ANCHO_CC))
mu['2010'].update({
  'nota': 'Sede de CCTV (OMA, 2004–2012), como en la foto: dos torres que se inclinan una hacia la otra y se unen arriba en el voladizo y abajo en el basamento, formando un anillo con el hueco en el medio; toda la fachada con la retícula diagonal.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0.3, 'lineas': cc})

s = json.dumps(d, ensure_ascii=False, indent=2)
s = re.sub(r'\{\s*"claro": ("[^"]+"),\s*"oscuro": ("[^"]+")\s*\}', r'{ "claro": \1, "oscuro": \2 }', s)
open(destino, 'w').write(s + '\n')
print('ok')
