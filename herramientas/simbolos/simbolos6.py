# Ronda 7: Moderno (Villa Savoye) y Biblioteca Nacional, medidos sobre sus fotos nuevas.
# Edita solo esas dos entradas de www/data/simbolos.json (se corre sobre el archivo actual).
import json, re, sys
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
def por_rectangulos(regiones, x0, x1, y0, y1, filas, px_unidad, paso_px=2):
    """Regiones (x0, x1, y0, y1, color) medidas sobre la foto, pintadas en orden; una línea por fila."""
    lineas, alto = [], (y1 - y0) / filas
    for i in range(filas):
        y = y0 + (i + 0.5) * alto
        celdas = []
        for c in range(int((x1 - x0) / paso_px)):
            x = x0 + c * paso_px + paso_px / 2
            col = None
            for a, b, ya, yb, cc in regiones:
                if a <= x < b and ya <= y < yb: col = cc
            celdas.append(col)
        segs, k = [], 0
        while k < len(celdas):
            j = k
            while j < len(celdas) and celdas[j] == celdas[k]: j += 1
            if celdas[k]: segs.append((k * paso_px / px_unidad, j * paso_px / px_unidad, celdas[k]))
            k = j
        lineas.append(tramos(segs, (x1 - x0) / px_unidad))
    return lineas

d['colores'].update({
  'savoye':        {'claro': '#f4f2ec', 'oscuro': '#ece9e1'},
  'savoye-sombra': {'claro': '#c9c6bd', 'oscuro': '#a9a69e'},
  'savoye-cielo':  {'claro': '#7fb2d9', 'oscuro': '#4f7397'},
  'savoye-vidrio': {'claro': '#22252a', 'oscuro': '#22252a'},
  'savoye-pasto':  {'claro': '#5d9a3f', 'oscuro': '#4f8a3a'},
  'savoye-arbol':  {'claro': '#2f4a2c', 'oscuro': '#2a3f28'},
  'bn-hormigon':   {'claro': '#b9ad98', 'oscuro': '#cbbfa9'},
  'bn-sombra':     {'claro': '#857b6b', 'oscuro': '#8d8372'},
  'bn-vidrio':     {'claro': '#3a5f8f', 'oscuro': '#5f84b4'},
  'bn-vidrio-2':   {'claro': '#8fa6b8', 'oscuro': '#a9bccb'},
})

# ---------- Moderno: Villa Savoye (foto savoye/, 770 × 385), de frente ----------
B, S, V = 'savoye', 'savoye-sombra', 'savoye-vidrio'
reg = [
  (40, 730, 20, 330, 'savoye-cielo'),                                 # el cielo, como placa
  (170, 328, 38, 97, B), (328, 485, 62, 97, S), (483, 496, 30, 97, B), (497, 600, 30, 97, B),   # el solario
  (330, 380, 66, 73, S),                                              # la abertura del muro del solario
  (65, 697, 97, 232, B),                                              # la caja
  (75, 688, 150, 187, V),                                             # la ventana corrida
  (65, 697, 232, 242, S),                                             # la sombra bajo la caja
  (65, 697, 242, 322, 'savoye-arbol'),                                # bajo la caja se ven los árboles
  (255, 490, 242, 322, V),                                            # el vidrio curvo de la planta baja
  (40, 730, 322, 345, 'savoye-pasto'),
]
for x in range(115, 688, 40): reg.append((x, x + 3, 150, 187, B))    # parantes de la ventana
for x in range(270, 490, 18): reg.append((x, x + 2, 242, 322, S))     # parantes del vidrio curvo
for x in (95, 170, 237, 380, 520, 603, 665): reg.append((x, x + 9, 242, 322, B))   # los pilotis
sav = por_rectangulos(reg, 40, 730, 20, 345, round((345 - 20) / 14), 14)   # una fila cada 14 px: misma escala en x y en y
d['estilos']['Moderno'] = {
  'nota': 'La Villa Savoye (Le Corbusier, 1928–1931), de frente, medida sobre la foto: el solario con sus dos volúmenes curvos arriba, la caja blanca con la ventana corrida, la planta baja retirada con el vidrio curvo, los pilotis y el pasto; detrás, el cielo.',
  'direccion': 'horizontal', 'alto': 160, 'grosor': 1, 'separacion': 0, 'lineas': sav}

# ---------- Biblioteca Nacional (foto bibliotecanacionalcnm, 1631 × 1080 → 900 px), de frente ----------
H_, Sb, Vb, V2 = 'bn-hormigon', 'bn-sombra', 'bn-vidrio', 'bn-vidrio-2'
reg = [
  (185, 710, 50, 68, H_),                                             # el remate
  (185, 710, 68, 126, Vb),                                            # la grilla de vidrio de arriba
  (170, 720, 124, 140, H_),                                           # la losa
  (175, 718, 140, 172, Sb),                                           # el piso en sombra
  (185, 355, 142, 166, H_), (525, 698, 142, 166, H_),                # los parasoles que vuelan
  (200, 680, 172, 197, V2),                                           # la banda de vidrio de la sala
  (155, 728, 197, 236, H_),                                           # la gran losa
  (175, 710, 236, 250, Sb), (205, 680, 250, 262, Sb), (240, 640, 262, 276, Sb),   # las vigas que se angostan
  (275, 305, 276, 470, H_), (590, 615, 276, 470, H_),                # los dos apoyos de los costados
  (305, 590, 276, 470, Sb),                                           # el fondo en sombra
  (335, 540, 282, 410, H_),                                           # el volumen curvo del centro
  (330, 590, 455, 468, H_),                                           # la baranda
  (190, 690, 468, 580, H_),                                           # el basamento
  (400, 445, 515, 560, Vb), (540, 585, 515, 560, Vb),                # las dos ventanas redondas
  (140, 760, 580, 596, 'follaje'),
]
for x in range(207, 700, 26): reg.append((x, x + 2, 68, 126, H_))    # parantes de la grilla de arriba
reg.append((185, 710, 96, 98, H_))
for x in range(222, 680, 24): reg.append((x, x + 2, 172, 197, H_))
bn = por_rectangulos(reg, 140, 760, 50, 596, round((596 - 50) / 14), 14)
ar = d['decadas']['argentina']['1990']
ar.update({
  'nota': 'Biblioteca Nacional (Testa, Bullrich y Cazzaniga; proyecto de 1962, inaugurada en 1992), de frente, medida sobre la foto: la caja de lectura con la grilla de vidrio, los parasoles que vuelan, la banda de vidrio, la gran losa y las vigas que se angostan, los apoyos de los costados, el volumen curvo del centro y el basamento con sus dos ventanas redondas.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0, 'alto': 170, 'lineas': bn})

s = json.dumps(d, ensure_ascii=False, indent=2)
s = re.sub(r'\{\s*"claro": ("[^"]+"),\s*"oscuro": ("[^"]+")\s*\}', r'{ "claro": \1, "oscuro": \2 }', s)
open(destino, 'w').write(s + '\n')
print('ok')
