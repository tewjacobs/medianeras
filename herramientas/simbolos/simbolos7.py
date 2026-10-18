# Ronda 8: Villa Savoye (bordes exactos), Biblioteca Nacional (idem), Teatro Colón y el
# Guggenheim de Nueva York (Arquitectura orgánica), medidos sobre sus fotos.
# Edita solo esas entradas de www/data/simbolos.json (se corre sobre el archivo actual).
#
# Bordes exactos: los tramos se calculan a partir de las posiciones redondeadas de cada borde
# (no de largos redondeados uno por uno), así el error no se acumula y todas las líneas terminan
# en el mismo punto.
import json, re, sys
destino = sys.argv[1]
d = json.load(open(destino))

def r2(x): return round(x, 2)
def f(x): return '%g' % r2(x)

def tramos(segs, total):
    """segs: (desde, hasta, color), ordenados. Devuelve la línea con huecos, con bordes exactos."""
    out, x = [], 0.0
    total = r2(total)
    for a, b, c in segs:
        a, b = r2(max(a, x)), r2(min(b, total))
        if b - a < 0.01: continue
        if a > x + 0.001: out.append(f'- {f(a - x)}')
        out.append(f'{c} {f(b - a)}'); x = b
    if total - x > 0.001: out.append(f'- {f(total - x)}')
    return ', '.join(out) or f'- {f(total)}'

def dentro(region, x, y):
    if callable(region[0]): return region[0](x, y)
    a, b, ya, yb = region[:4]
    return a <= x < b and ya <= y < yb

def por_regiones(regiones, x0, x1, y0, y1, px_unidad, paso_px=2):
    """Regiones medidas sobre la foto: (x0, x1, y0, y1, color) o (funcion(x, y), color), pintadas
    en orden. Una fila cada px_unidad px, así la escala es la misma en x y en y."""
    filas = round((y1 - y0) / px_unidad)
    alto = (y1 - y0) / filas
    lineas = []
    for i in range(filas):
        y = y0 + (i + 0.5) * alto
        celdas = []
        for c in range(round((x1 - x0) / paso_px)):
            x = x0 + c * paso_px + paso_px / 2
            col = None
            for reg in regiones:
                if dentro(reg, x, y): col = reg[-1]
            celdas.append(col)
        segs, k = [], 0
        while k < len(celdas):
            j = k
            while j < len(celdas) and celdas[j] == celdas[k]: j += 1
            if celdas[k]: segs.append((k * paso_px / px_unidad, j * paso_px / px_unidad, celdas[k]))
            k = j
        lineas.append(tramos(segs, (x1 - x0) / px_unidad))
    return lineas

def triangulo(x0, x1, base, punta):
    """Frontón: base de x0 a x1 en y=base, punta arriba en el centro, en y=punta."""
    cx, mitad = (x0 + x1) / 2, (x1 - x0) / 2
    return lambda x, y: punta <= y < base and abs(x - cx) <= mitad * (y - punta) / (base - punta)

col = d['colores']
col.update({
  'colon-piedra':   {'claro': '#d9c6a2', 'oscuro': '#e2d1b0'},
  'colon-sombra':   {'claro': '#b39b77', 'oscuro': '#bda684'},
  'colon-vidrio':   {'claro': '#3f444b', 'oscuro': '#4a505a'},
  'colon-puerta':   {'claro': '#eceae4', 'oscuro': '#f0eee8'},
  'colon-marquesina': {'claro': '#7bb0a4', 'oscuro': '#8cc0b4'},
  'gug-torre':      {'claro': '#8a4b2e', 'oscuro': '#a35e3c'},
  'gug-base':       {'claro': '#6b3d25', 'oscuro': '#86502f'},
  'gug-base-2':     {'claro': '#4f2c1b', 'oscuro': '#6a3e26'},
  'asfalto':        {'claro': '#4a4a4c', 'oscuro': '#3a3b40'},
  'gug-crema':      {'claro': '#e3d3b2', 'oscuro': '#efe2c6'},
})

# ---------- Moderno: Villa Savoye (foto savoye/, 770 × 385), bordes exactos ----------
B, S, V = 'savoye', 'savoye-sombra', 'savoye-vidrio'
reg = [
  (40, 730, 20, 330, 'savoye-cielo'),
  (170, 328, 38, 97, B), (328, 485, 62, 97, S), (483, 496, 30, 97, B), (497, 600, 30, 97, B),
  (65, 697, 97, 232, B),
  (75, 688, 150, 187, V),
  (65, 697, 232, 242, S),
  (65, 697, 242, 322, 'savoye-arbol'),
  (255, 490, 242, 322, V),
  (40, 730, 322, 350, 'savoye-pasto'),
]
for x in range(115, 688, 40): reg.append((x, x + 4, 150, 187, B))
for x in range(270, 490, 18): reg.append((x, x + 2, 242, 322, S))
for x in (96, 170, 238, 380, 520, 604, 666): reg.append((x, x + 8, 242, 322, B))
d['estilos']['Moderno']['lineas'] = por_regiones(reg, 40, 730, 20, 350, 14)
d['estilos']['Moderno']['alto'] = 160

# ---------- Biblioteca Nacional: los mismos rectángulos, bordes exactos ----------
H_, Sb, Vb, V2 = 'bn-hormigon', 'bn-sombra', 'bn-vidrio', 'bn-vidrio-2'
reg = [
  (186, 710, 50, 68, H_), (186, 710, 68, 126, Vb), (170, 720, 124, 140, H_), (176, 714, 140, 172, Sb),
  (186, 356, 142, 166, H_), (530, 700, 142, 166, H_), (200, 686, 172, 197, V2), (156, 730, 197, 236, H_),
  (176, 710, 236, 250, Sb), (206, 680, 250, 262, Sb), (240, 646, 262, 276, Sb),
  (276, 306, 276, 470, H_), (590, 620, 276, 470, H_), (306, 590, 276, 470, Sb), (336, 540, 282, 410, H_),
  (330, 590, 456, 468, H_), (190, 706, 468, 580, H_), (400, 446, 516, 560, Vb), (540, 586, 516, 560, Vb),
  (140, 760, 580, 596, 'follaje'),
]
for x in range(208, 700, 26): reg.append((x, x + 2, 68, 126, H_))
reg.append((186, 710, 96, 98, H_))
for x in range(222, 680, 24): reg.append((x, x + 2, 172, 197, H_))
d['decadas']['argentina']['1990']['lineas'] = por_regiones(reg, 140, 760, 50, 596, 14)

# ---------- Teatro Colón (foto colon/, 1000 × 714), de frente ----------
P_, Sc, Vc = 'colon-piedra', 'colon-sombra', 'colon-vidrio'
reg = [
  (484, 516, 52, 92, P_),                                     # la chimenea del frontón
  (triangulo(282, 718, 196, 88), P_),                         # el frontón
  (triangulo(300, 700, 190, 104), Sc),                        # su tímpano, en sombra
  (464, 536, 140, 178, Vc),                                   # la ventana del tímpano
  (276, 308, 152, 196, P_), (692, 724, 152, 196, P_),         # los pedestales de las esquinas
  (104, 896, 196, 210, P_),                                   # la cornisa alta
  (110, 890, 210, 300, P_),                                   # el ático
  (triangulo(110, 262, 304, 276), P_), (triangulo(736, 888, 304, 276), P_),   # frontones de los pabellones
  (104, 896, 300, 314, Sc),                                   # la cornisa del piano nobile
  (110, 890, 314, 450, P_),                                   # el piano nobile
  (104, 896, 450, 470, Sc),                                   # la cornisa
  (110, 890, 470, 572, P_),                                   # la planta baja
  (370, 622, 478, 528, 'colon-marquesina'),                   # la marquesina de vidrio
  (380, 612, 528, 572, Sc),                                   # la entrada, en sombra
  (90, 910, 572, 602, Sc),                                    # la escalinata
  (60, 940, 602, 640, 'follaje'),                             # el pasto
]
for a, b in ((165, 220), (397, 453), (471, 524), (544, 597), (776, 831)): reg.append((a, b, 238, 272, Sc))   # relieves
for a, b in ((174, 212), (302, 340), (405, 443), (477, 515), (550, 588), (654, 692), (782, 820)):
    reg.append((a, b, 352, 436, Vc))                         # las ventanas en arco del piano nobile
    reg.append((a + 6, b - 6, 344, 352, Vc))                  # la curva de arriba del arco
for a, b in ((168, 212), (300, 340), (652, 692), (780, 822)): reg.append((a, b, 486, 570, 'colon-puerta'))   # puertas
for x in (134, 150, 228, 244, 282, 362, 454, 530, 618, 708, 750, 766, 844, 860): reg.append((x, x + 6, 314, 450, Sc))   # columnas
reg.append((136, 246, 436, 450, Sc)); reg.append((376, 620, 436, 450, Sc)); reg.append((764, 862, 436, 450, Sc))   # balaustradas
ar = d['decadas']['argentina']['1900']
ar.update({
  'nota': 'Teatro Colón (Tamburini, Meano y Dormal; inaugurado en 1908), de frente, medido sobre la foto: el frontón central con su ventana, la cornisa y el ático con los relieves, los frontones de los dos pabellones, el piano nobile con las columnas y las siete ventanas en arco, las balaustradas, la planta baja con las puertas y la marquesina de vidrio, la escalinata y el pasto.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0, 'alto': 170, 'lineas': por_regiones(reg, 60, 940, 52, 640, 14)})
ar.pop('alinear', None)

# ---------- Arquitectura orgánica: Guggenheim de Nueva York (foto guggenheim new york/, maqueta) ----------
C_, T_ = 'gug-crema', 'gug-torre'
reg = [
  (254, 488, 130, 392, T_),                                   # la torre de atrás
] + [(x, x + 2, 130, 392, 'gug-base') for x in range(272, 488, 22)] + [   # sus juntas, por detrás de la espiral
  (488, 698, 222, 246, T_),                                   # el anexo de atrás
  (triangulo(481, 661, 246, 210), 'vidrio-claro'),            # la cúpula de vidrio, centrada sobre la espiral (eje x 571)
  (420, 722, 246, 302, C_), (434, 712, 302, 312, 'gug-base'),  # la espiral: bandas que se ensanchan hacia arriba
  (436, 712, 312, 338, C_), (440, 708, 338, 347, 'gug-base'),
  (440, 706, 347, 370, C_), (446, 702, 370, 382, 'gug-base'),
  (448, 700, 382, 412, C_),
  (240, 360, 352, 366, C_), (244, 356, 366, 392, 'gug-base'), # la rotonda chica: el borde y las ventanas
  (360, 420, 350, 384, C_),
  (234, 718, 392, 452, C_),                                   # la losa de la base
  (300, 700, 418, 424, 'gug-base'),                           # la línea del letrero
  (120, 880, 452, 476, 'piedra'),                             # la vereda
  (120, 880, 476, 534, 'asfalto'),                            # la calle
]
d['estilos']['Arquitectura orgánica'] = {
  'nota': 'El Guggenheim de Nueva York (Wright, 1943–1959), de frente, medido sobre la foto de la maqueta: la espiral con sus bandas que se ensanchan hacia arriba y las ventanas corridas entre una y otra, la cúpula de vidrio, la rotonda chica a la izquierda, la torre y el anexo de atrás, la losa de la base, la vereda y la calle.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0, 'alto': 150, 'lineas': por_regiones(reg, 120, 880, 130, 534, 7)}

s = json.dumps(d, ensure_ascii=False, indent=2)
s = re.sub(r'\{\s*"claro": ("[^"]+"),\s*"oscuro": ("[^"]+")\s*\}', r'{ "claro": \1, "oscuro": \2 }', s)
open(destino, 'w').write(s + '\n')
print('ok')
