# Escuela Superior de Comercio Manuel Belgrano, Córdoba (Bidinost, Chute, Gasó, Lapacó y Meyer; concurso
# de 1960, construida entre 1960 y 1971). Medida sobre referencias/simbolos/60s argentina/Belgrano_por_fuera_027.jpg
# (de frente, 20 px por unidad): el gran techo de hormigón con su canto y el cielorraso que se curva hacia
# las puntas, las columnas finas (rayas verticales), las bóvedas iluminadas bajo el techo; a la izquierda el
# hall vidriado de doble altura (foto del atardecer, Screenshot…Bauhasaurus), a la derecha el bloque de aulas
# con la ventana corrida de marcos rojos y la planta baja en sombra; la chimenea y el muro de piedra.
import sys
from armar import Medida, escribir

M = Medida(160, 1805, 418, 26)
FILAS = M.fila(964)
HO, MA, SO, RO, LU, V, P1, P2 = ('belg-hormigon', 'belg-madera', 'belg-sombra', 'belg-rojo', 'belg-luz',
                                  'belg-vidrio', 'belg-piedra', 'belg-piedra-2')
HALL = 1000                                                   # donde termina el hall y empieza el bloque de aulas
COLUMNAS = [210 + 102.6 * k for k in range(16)]

def cielorraso(y0, y1):
    # El techo es más grueso en el medio: debajo del canto, cada fila llega menos lejos hacia las puntas.
    hondo = (y0 - 601) / 40                                   # 0 arriba, 1 abajo
    corte = 260 * hondo ** 1.4
    return (MA, 160 + corte, 1805 - corte, y0, y1)

def arranque(x):
    # Donde termina el techo sobre la columna: en las puntas, el cielorraso ya subió.
    c = cielorraso(627, 653)
    return 627 if c[1] <= x <= c[2] else 601                  # entra en la última fila del techo: sin aire

macizos = [
    (SO, 240, HALL, 712, 900),                                # el hall, en sombra
    (HO, HALL, 1700, 712, 900),                               # el bloque de aulas
    (HO, 160, 1805, 575, 601),                                # canto del techo
    *[cielorraso(y, y + 26) for y in (601, 627)],
    (P1, 160, 1805, 900, 926), (P2, 160, 1805, 926, 952),     # muro de piedra
]

zonas = [
    M.zona(HO, 160, 1805, 575, 601),                                             # canto, lleno
    # Columnas iguales, desde el techo: apoyan en el bloque de aulas o, fuera de él, bajan hasta el piso.
    M.zona(V, 240, HALL - 10, 712, 900, relleno='rayas', fondo=SO),             # vidrio del hall
    M.zona(HO, 240, HALL, 795, 810),                                             # entrepiso del hall
    *[{**M.zona(HO, x - 7, x + 7, arranque(x), 712 if HALL < x < 1700 else 900), 'hasta': M.u(x - 7) + 0.75} for x in COLUMNAS],
    M.zona(RO, HALL + 70, 1700, 735, 775, relleno='rayas', fondo=V),             # ventana corrida
    M.zona(SO, HALL, 1700, 820, 900),                                            # planta baja en sombra
    *[M.zona(V, x, x + 140, 840, 885, relleno='rayas', fondo=SO) for x in (1060, 1300, 1500)],
    M.zona(HO, 1578, 1622, 418, 900), M.zona(SO, 1610, 1622, 430, 900),          # chimenea, llena, hasta el piso
]
arcos = [M.arco(LU, a + 22, b - 22, 712, 24) for a, b in zip(COLUMNAS, COLUMNAS[1:]) if 400 < a < 1500]

lineas = M.lineas(FILAS, macizos)
escribir(sys.argv[1], 'argentina', '1960', {
    'obra': 'Escuela Superior de Comercio Manuel Belgrano', 'lugar': 'Córdoba', 'anio': '1960–1971',
    'nota': 'Escuela Superior de Comercio Manuel Belgrano (Bidinost, Chute, Gasó, Lapacó y Meyer; concurso de 1960, '
            'construida entre 1960 y 1971), de frente desde el río Suquía: un único techo de hormigón que vuela sobre '
            'columnas finas, con las bóvedas iluminadas debajo, el volumen de aulas con su ventana corrida, la chimenea '
            'al costado y el muro de piedra.',
    'direccion': 'horizontal', 'separacion': 0.3, 'alto': 110, 'lineas': lineas, 'zonas': zonas, 'arcos': arcos})
print(len(lineas), 'líneas, ancho', M.ancho)
