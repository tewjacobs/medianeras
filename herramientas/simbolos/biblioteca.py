# Biblioteca Nacional (Testa, Bullrich y Cazzaniga; 1962–1992), de frente, medida en píxeles sobre
# referencias/simbolos/biblioteca nacional/bibliotecanacionalcnm.jpg (1631 × 1080), con el eje en x 805.
# Hormigón en filas; vidrios, parasoles, volumen curvo, apoyos (rayas verticales) y ojos de buey en zonas.
# Simétrica salvo la cajita del costado derecho, que es así en la obra.
import json, sys

CX, PX, Y0, PASO_PX = 805, 20.6, -39, 26.8    # filas de 1 unidad con 0,3 de separación; 5 filas para la azotea
MEDIO = 520                                   # la losa grande, lo más ancho
ANCHO = round(2 * MEDIO / PX * 4) / 4
u = lambda dx: round((dx + MEDIO) / PX * 4) / 4          # dx: distancia al eje, en px
fila = lambda y: round((y - Y0) / PASO_PX)
FILAS = fila(1045) + 1                                    # la última es el pasto

def hormigon(y):
    # Tramos llenos de la fila que pasa por y (centro de la fila): [(medio ancho en px, color)].
    if y < 95: return 0, '-'                               # azotea: todo en zonas
    if y < 318: return 470, 'bn-hormigon'                  # caja de lectura (los vidrios van en zonas)
    if y < 352: return 510, 'bn-hormigon'                  # balcón de la banda de vidrio
    if y < 475: return 520, 'bn-hormigon'                  # la losa
    if y < 640:                                           # vigas que se angostan hacia los apoyos
        m = 520 - (y - 475) / 165 * 220
        return m, 'bn-hormigon' if fila(y) % 2 else 'bn-sombra'
    if y < 850: return 300, 'bn-sombra'                    # entre apoyos: el interior en sombra
    if y < 890: return 255, 'bn-hormigon'                  # plataforma
    return 330, 'bn-hormigon'                              # basamento

def linea(r):
    if r == FILAS - 1: return f'follaje {ANCHO:g}'
    m, color = hormigon(Y0 + r * PASO_PX + PX / 2)
    a, b = u(-m), u(m)
    return ', '.join(f'{c} {round(l, 2):g}' for c, l in (('-', a), (color, b - a), ('-', ANCHO - b)) if l > 0)

def z(color, x0, x1, y0, y1, **o):
    a = fila(y0); b = max(a, fila(y1) - 1)
    return {'color': color, 'desde': u(x0), 'hasta': u(x1), 'primera': a, 'ultima': b, **o}
par = lambda color, x0, x1, y0, y1, **o: [z(color, -x1, -x0, y0, y1, **o), z(color, x0, x1, y0, y1, **o)]

zonas = [
    # Azotea, medida sobre las dos fotos nuevas (de frente y aérea): caja con rejillas, tanque amarillo
    # acostado, las dos torres que se abren abajo y la caja baja entre ellas. No es simétrica.
    z('bn-hormigon', -360, -215, -12, 95), z('bn-oscuro', -345, -285, -12, 41),
    z('bn-sombra', 5, 115, 15, 95),
    *[c for x0 in (-145, 125) for c in (
        z('bn-hormigon', x0, x0 + 125, -39, 95), z('bn-hormigon', x0 - 12, x0 + 137, 41, 95),
        z('bn-oscuro', x0 + 50, x0 + 75, 68, 95))],
    z('bn-ambar', -390, -150, 41, 95),
    z('bn-vidrio', -465, 465, 125, 228),                                         # caja de vidrio
    *[z('bn-hormigon', x - 4, x + 4, 125, 228) for x in [-465 + k * 930 / 12 for k in range(1, 12)]],
    *[z('bn-sombra', -470 + k * 940 / 6 + 50, -470 + (k + 1) * 940 / 6 - 50, 228, 255) for k in range(6)],  # borde dentado
    *par('bn-oscuro', 175, 465, 255, 282),                                       # vidrio detrás de los parasoles
    *par('bn-parasol', 150, 455, 282, 309),                                      # parasoles
    z('bn-vidrio-2', -430, 430, 336, 363),                                       # banda de vidrio
    *[z('bn-hormigon', x - 3, x + 3, 336, 363) for x in [-430 + k * 860 / 20 for k in range(1, 20)]],
    z('bn-oscuro', -245, 245, 470, 850),                                         # el hueco entre los apoyos
    *par('bn-ambar', 225, 245, 560, 820),                                        # paneles amarillos del fondo
    *par('bn-hormigon', 245, 300, 520, 850, relleno='rayas', fondo='bn-sombra'),  # apoyos
    *[z('bn-sombra', -225, 225, y, y + 27) for y in (765,)],                     # viga bajo el volumen
    z('bn-hormigon', -215, 215, 818, 845),                                       # baranda
    z('bn-hormigon', 175, 210, 640, 690),                                        # cuello y cajita del costado
    z('bn-hormigon', 205, 285, 615, 700),
    z('bn-vidrio-2', 225, 265, 640, 670),
    # Volumen curvo: esquinas de abajo bien redondeadas.
    z('bn-parasol', -185, 185, 520, 680),
    z('bn-parasol', -172, 172, 520, 707),                                        # (empiezan arriba: sin ranuras)
    z('bn-parasol', -150, 150, 520, 734),
    # Ojos de buey del basamento, con su aro de color.
    *[c for x in (-125, 125) for c in (
        z('bn-vidrio', x - 34, x + 34, 905, 1013), z('bn-vidrio', x - 46, x + 46, 932, 986),
        z('bn-oscuro', x - 24, x + 24, 905, 1013), z('bn-oscuro', x - 36, x + 36, 932, 986))],
]

ruta = sys.argv[1]
texto = open(ruta).read()
i = texto.index('"1990": {', texto.index('"argentina"', texto.index('"decadas"')))
a = texto.index('"lineas": [', i); b = texto.index(']', a) + 1
lista = lambda nombre, cosas: f'"{nombre}": [\n' + ',\n'.join(' ' * 10 + json.dumps(c, ensure_ascii=False) for c in cosas) + '\n' + ' ' * 8 + ']'
if texto[b:].startswith(',\n        "zonas": ['): b = texto.index(']', b + 5) + 1
texto = texto[:a] + lista('lineas', lineas := [linea(r) for r in range(FILAS)]) + ',\n        ' + lista('zonas', zonas) + texto[b:]
texto = texto[:i] + texto[i:a].replace('"separacion": 0,', '"separacion": 0.3,') + texto[a:]
open(ruta, 'w').write(texto)
json.loads(texto)
print(len(lineas), 'líneas, ancho', ANCHO)
