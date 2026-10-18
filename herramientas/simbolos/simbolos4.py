# Ronda 5: Arroyo, SOMISA y Recoleta con sus fotos; Bilbao y CCTV con volumen por tonos.
# Se corre siempre sobre simbolos-ronda4.json.
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
def pintar(ancho, paso, regla):
    """regla(x) -> color o None, muestreada cada `paso` unidades."""
    return tramos(fundir([regla(c * paso + paso / 2) for c in range(round(ancho / paso))], paso), ancho)

col = d['colores']
col.update({
  'blanco-recoleta': {'claro': '#e0d7c6', 'oscuro': '#f2ede4'},
  'rojo-recoleta': {'claro': '#c0574b', 'oscuro': '#c96558'},
  'somisa-acero':  {'claro': '#2c3442', 'oscuro': '#4a5466'},
  'somisa-vidrio': {'claro': '#4f6f8f', 'oscuro': '#6585a6'},
  'somisa-alero':  {'claro': '#a9b6c4', 'oscuro': '#bcc8d4'},
  'somisa-panel':  {'claro': '#7fb3b8', 'oscuro': '#8fc2c7'},
  'titanio-0': {'claro': '#cfd4d8', 'oscuro': '#e6e9ec'},
  'titanio-1': {'claro': '#aab2b9', 'oscuro': '#c5ccd2'},
  'titanio-2': {'claro': '#868f98', 'oscuro': '#a1aab3'},
  'titanio-3': {'claro': '#636c75', 'oscuro': '#7c8690'},
  'cctv-frente':  {'claro': '#c9d0d6', 'oscuro': '#dde2e6'},
  'cctv-adentro': {'claro': '#9aa5b0', 'oscuro': '#aab4be'},
  'cctv-costado': {'claro': '#3e4652', 'oscuro': '#4b5462'},
  'cctv-luz':     {'claro': '#c9b27a', 'oscuro': '#d8c08a'},
})
ar = d['decadas']['argentina']; mu = d['decadas']['mundo']

# ---------- Casa sobre el Arroyo (foto de frente, casa puente/Screenshot…) ----------
# Medida sobre la foto de frente (px, ancho 900): la caja de x 35 a 878; techo fino, ventana
# corrida con montantes cada ~60 px, banda gruesa de hormigón; abajo, dos pilares anchos y dos
# pares de columnas finas, simétricos; el arco ancho y bajo nace en las orillas (x 160 y 745),
# sube hasta tocar la losa en el centro; abajo, la tierra y el agua en el medio.
U = lambda x: (x - 35) / 14
ANCHO_A = round(U(878), 2)
EJE = ANCHO_A / 2
def simetrico(a, b): return [(a, b), (ANCHO_A - b, ANCHO_A - a)]
PILARES = simetrico(U(143), U(205))
COLUMNAS = simetrico(U(258), U(266)) + simetrico(U(346), U(354))
def bajo_losa(x):
    if any(a <= x < b for a, b in PILARES): return 'hormigon'
    if any(a <= x < b for a, b in COLUMNAS): return 'hormigon'
    return None
ventana = lambda: pintar(ANCHO_A, 0.1, lambda x: 'hormigon' if x < 0.5 or x > ANCHO_A - 0.5 else ('hierro' if (x - 0.5) % 4.3 < 0.3 else 'vidrio'))
arr = ['hormigon %s' % f(ANCHO_A), ventana(), ventana(), ventana(),
       'hormigon %s' % f(ANCHO_A), 'hormigon %s' % f(ANCHO_A),
       pintar(ANCHO_A, 0.1, bajo_losa), pintar(ANCHO_A, 0.1, bajo_losa), pintar(ANCHO_A, 0.1, bajo_losa),
       pintar(ANCHO_A, 0.1, lambda x: 'agua' if abs(x - EJE) < 3.5 else 'tierra'),
       pintar(ANCHO_A, 0.1, lambda x: 'agua' if abs(x - EJE) < 2 else 'follaje')]
paso_a = 1.4
ar['1940'].update({
  'nota': 'Casa sobre el Arroyo (Amancio Williams, 1943–1946), medida sobre la foto de frente: la caja larga con el techo fino, la ventana corrida con sus montantes y la banda gruesa de hormigón; abajo, simétricos, los dos pilares anchos y las columnas finas; el arco ancho y bajo que nace en cada orilla y sube hasta tocar la losa en el centro; la tierra y, en el medio, el arroyo.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0.4, 'lineas': arr,
  'arcos': [{'color': 'hormigon', 'desde': round(U(160), 2), 'hasta': round(ANCHO_A - U(160), 2), 'base': 9,
             'flecha': round(9 * paso_a + 0.5 - (6 * paso_a - 0.4), 2), 'lineas': 1}]})

# ---------- SOMISA (fotos somisa/) ----------
# El frente alto: pilastras de acero oscuro que dividen la fachada en tres paños; en cada piso,
# una franja de vidrio azul con su carpintería y un alero claro; la columna de paneles
# celestes en la esquina; la planta baja retirada en sombra.
ANCHO_S = 20
PILASTRAS = [(0, 0.8), (6.6, 7.4), (13.2, 14), (19.2, 20)]
def en_pilastra(x): return any(a <= x < b for a, b in PILASTRAS)
def vidrio_s(x):
    if en_pilastra(x): return 'somisa-acero'
    if 16.6 <= x < 19.2: return 'somisa-panel'
    return 'somisa-acero' if (x % 1.65) < 0.22 else 'somisa-vidrio'
def alero_s(x): return 'somisa-acero' if en_pilastra(x) else 'somisa-alero'
som = [f'somisa-acero {ANCHO_S}']
for piso in range(11):
    som += [pintar(ANCHO_S, 0.05, alero_s), pintar(ANCHO_S, 0.05, vidrio_s)]
som += [pintar(ANCHO_S, 0.05, lambda x: 'somisa-acero' if en_pilastra(x) else 'sombra')] * 2
ar['1970'].update({
  'nota': 'Edificio SOMISA (Mario Roberto Álvarez, 1966–1977), de frente: todo de acero; las pilastras oscuras dividen la fachada en paños; en cada piso, el vidrio azul con su carpintería y un alero claro; en la esquina, la columna de paneles celestes; la planta baja retirada, en sombra.',
  'direccion': 'horizontal', 'alto': 190, 'grosor': 1, 'separacion': 0.25, 'lineas': som})

# ---------- Centro Cultural Recoleta (foto recoleta/) ----------
# Medido en la foto (px, ancho 30–600): el pabellón central con frontón (x 170–360), las alas con
# balaustrada, las molduras blancas, las ventanas, la marquesina de vidrio en la entrada y,
# a la derecha, el portal con arco.
X = lambda x: (x - 30) / 14.25
ANCHO_R = 40
R, B, V = 'rojo-recoleta', 'blanco-recoleta', 'vidrio'
def frontón(w):
    c = X(265)
    return [(c - w / 2, c - w / 2 + 0.5, B), (c - w / 2 + 0.5, c + w / 2 - 0.5, R), (c + w / 2 - 0.5, c + w / 2, B)]
ventanas_alta = [(125, 155), (190, 225), (245, 280), (305, 335), (375, 405), (465, 500), (565, 590)]
pilastras_r = [175, 232, 290, 345]
def piso_alto(x):
    for a, b in ventanas_alta:
        if X(a) <= x < X(b): return B if (x - X(a) < 0.3 or X(b) - x < 0.3) else V
    if any(X(p) <= x < X(p) + 0.6 for p in pilastras_r): return B
    return R
ventanas_baja = [(60, 90), (125, 155), (190, 215), (310, 335), (380, 405)]
def piso_bajo(x, marquesina=False):
    if marquesina and X(200) <= x < X(310): return V
    if marquesina and X(452) <= x < X(524): return R   # ahí va el arco del portal
    if X(250) <= x < X(285): return V                      # la entrada
    if X(458) <= x < X(518): return V                      # el portal con arco
    if X(452) <= x < X(458) or X(518) <= x < X(524): return B
    if X(238) <= x < X(246) or X(289) <= x < X(297): return B   # columnas de la marquesina
    for a, b in ventanas_baja:
        if X(a) <= x < X(b): return V
    return R
reco = [
  tramos([(X(258), X(272), B)], ANCHO_R),
  tramos(frontón(7), ANCHO_R),
  tramos(frontón(13.4), ANCHO_R),
  tramos([(X(100), X(170), 'balaustre')] + [(X(170), X(360), B)] + [(X(360), X(435), 'balaustre')], ANCHO_R),
  f'{B} {ANCHO_R}',
  pintar(ANCHO_R, 0.1, piso_alto), pintar(ANCHO_R, 0.1, piso_alto), pintar(ANCHO_R, 0.1, piso_alto),
  f'{B} {ANCHO_R}',
  pintar(ANCHO_R, 0.1, lambda x: piso_bajo(x, True)),
  pintar(ANCHO_R, 0.1, piso_bajo), pintar(ANCHO_R, 0.1, piso_bajo), pintar(ANCHO_R, 0.1, piso_bajo),
  f'piedra {ANCHO_R}',
]
reco[3] = reco[3].replace('balaustre', B)
ar['1980'].update({
  'nota': 'Centro Cultural Recoleta (Testa, Bedel y Benedit, 1980), medido sobre la foto: la fachada roja con sus molduras blancas, el pabellón central con el frontón, las balaustradas de las alas, las ventanas enmarcadas, la marquesina de vidrio en la entrada y, a la derecha, el portal con arco.',
  'direccion': 'horizontal', 'alto': 150, 'grosor': 1, 'separacion': 0.3, 'lineas': reco,
  'arcos': [
    {'color': B, 'desde': round(X(452), 2), 'hasta': round(X(524), 2), 'base': 10, 'flecha': 2.0, 'lineas': 1},
    {'color': V, 'desde': round(X(458), 2), 'hasta': round(X(518), 2), 'base': 10, 'flecha': 1.6, 'relleno': True}]})

# ---------- Guggenheim Bilbao: cada pieza curva con su tono ----------
# Piezas medidas sobre la foto (px), dibujadas de atrás hacia adelante: lo de atrás o en
# sombra más oscuro, lo de adelante más claro. Cada pieza: (borde de arriba, borde de abajo, tono).
def interp(puntos, x):
    for (x0, y0), (x1, y1) in zip(puntos, puntos[1:]):
        if x0 <= x <= x1: return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return None
PIEZAS = [  # de atrás hacia adelante
  ([(505, 100), (530, 90), (600, 86), (630, 96), (645, 110)], [(505, 220), (645, 220)], 'titanio-3'),   # la torre de atrás
  ([(640, 152), (690, 148), (735, 160)], [(640, 330), (735, 330)], 'titanio-2'),                       # pétalo de la derecha
  ([(450, 150), (480, 124), (515, 110)], [(450, 330), (515, 330)], 'titanio-2'),                       # pétalo de la izquierda
  ([(500, 128), (560, 118), (640, 128)], [(500, 160), (640, 160)], 'titanio-1'),                       # banda curva alta
  ([(390, 176), (440, 165), (500, 170)], [(390, 330), (500, 330)], 'titanio-2'),                       # la ola de atrás de la sala
  ([(670, 206), (740, 199), (800, 210), (812, 232)], [(670, 330), (812, 330)], 'titanio-1'),            # volumen de la derecha
  ([(85, 178), (200, 205), (300, 214), (400, 190), (480, 190)], [(85, 262), (480, 262)], 'titanio-0'),  # sala: cara iluminada
  ([(85, 262), (480, 262)], [(85, 330), (480, 330)], 'titanio-2'),                                     # sala: parte en sombra
  ([(505, 196), (575, 186), (648, 198)], [(505, 216), (648, 216)], 'titanio-0'),                       # la visera de adelante
]
# La proa de la sala: cada línea empieza un poco más afuera que la de arriba (casi vertical).
proa = lambda y: 85 - (y - 178) * 0.3
gb = []
PX = 6
for i in range(24):
    y = 86 + i * 10.4 + 5
    def regla(u):
        x = 40 + u * 14
        if y >= 322: return 'caliza' if x >= 60 else None
        if 700 <= x <= 790 and y > 282: return 'caliza'
        color = None
        if 492 <= x <= 640 and 216 < y: color = 'vidrio'
        if x < proa(y): return None
        for arriba, abajo, tono in PIEZAS:
            xx = max(x, 85)
            a, b = interp(arriba, xx), interp(abajo, xx)
            if a is not None and b is not None and a < y <= b:
                if tono == 'titanio-2' and color == 'vidrio': continue
                color = tono
        return color
    gb.append(pintar((812 - 40) / 14, PX / 14, regla))
gb += [f'agua {f((812 - 40) / 14)}'] * 2
mu['1990'].update({
  'nota': 'Guggenheim Bilbao (Frank Gehry, 1993–1997), desde la ría: las piezas curvas de titanio superpuestas, cada una con su tono (más claras las de adelante y las iluminadas, más oscuras las de atrás o en sombra): la sala larga con su proa, la ola detrás, los pétalos de la flor, la torre del fondo, la visera sobre el atrio de vidrio y el volumen de la derecha; abajo, la piedra y la ría.',
  'direccion': 'horizontal', 'alto': 170, 'grosor': 1, 'separacion': 0.25, 'lineas': gb})

# ---------- CCTV: el anillo con profundidad ----------
# Caras: el frente iluminado (con la retícula diagonal), las caras de adentro del anillo en un
# tono medio, el costado de la torre derecha y del voladizo en oscuro con ventanas encendidas.
ANCHO_C, FILAS = 32, 26
cc = []
for i in range(FILAS):
    t = i / (FILAS - 1)            # 0 arriba, 1 abajo
    izq = 4.5 * (1 - t)            # borde de afuera de la pierna izquierda: se inclina al subir
    frente_der = 21 - 1.5 * t      # donde termina el frente y empieza el costado oscuro
    der = ANCHO_C - 2.5 * (1 - t)  # borde de afuera del costado
    voladizo = i <= 6
    base = i >= 20
    hueco = None if voladizo or base else (izq + 5.3, frente_der - 2.4)
    def regla(x):
        if x < izq or x > der: return None
        if x >= frente_der:
            # costado oscuro, con filas de ventanas encendidas
            return 'cctv-luz' if (i % 2 == 0 and (x * 2.2) % 1.6 < 0.5) else 'cctv-costado'
        if hueco and hueco[0] <= x < hueco[1]: return None
        if hueco and hueco[1] <= x < hueco[1] + 1.1: return 'cctv-adentro'   # cara interior de la torre derecha
        if i == 7 and hueco is None: return 'cctv-adentro'
        a = (x + i * 0.7) % 3.6
        b = (x - i * 0.7) % 3.6
        return 'cctv-reticula' if a < 0.35 or b < 0.35 else 'cctv-frente'
    linea = pintar(ANCHO_C, 0.2, regla)
    cc.append(linea)
# la cara de abajo del voladizo, vista desde el hueco
cc[7] = pintar(ANCHO_C, 0.2, lambda x: None if x < 4.5 * (1 - 7 / 25) or x > ANCHO_C - 2.5 * (1 - 7 / 25) else
               ('cctv-costado' if x >= 21 - 1.5 * 7 / 25 else ('cctv-adentro' if x >= 4.5 * (1 - 7 / 25) + 5.3 else 'cctv-frente')))
mu['2010'].update({
  'nota': 'Sede de CCTV (OMA, 2004–2012), como en la foto: el anillo con profundidad. El frente iluminado con la retícula diagonal (la pierna izquierda, el basamento y el voladizo), la cara de abajo del voladizo y la cara interior de la torre derecha en un tono medio, y el costado oscuro con sus ventanas encendidas.',
  'direccion': 'horizontal', 'alto': 190, 'grosor': 1, 'separacion': 0.3, 'lineas': cc})

s = json.dumps(d, ensure_ascii=False, indent=2)
s = re.sub(r'\{\s*"claro": ("[^"]+"),\s*"oscuro": ("[^"]+")\s*\}', r'{ "claro": \1, "oscuro": \2 }', s)
open(destino, 'w').write(s + '\n')
print('ok')
