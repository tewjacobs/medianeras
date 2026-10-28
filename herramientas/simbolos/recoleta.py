# Centro Cultural Recoleta (Testa, Bedel y Benedit, 1980), medido en píxeles sobre
# referencias/simbolos/recoleta/cultu reco.jpg (600 × 375). Muro rojo en filas finas; molduras, pilastras,
# balaustradas (rayas), ventanas, marquesina y el portal con arco en zonas; el frontón con rectas.
# Las aberturas de arriba y de abajo caen sobre los mismos ejes (medidos en la foto).
import sys
from armar import Medida, escribir

M = Medida(40, 598, 12, 8.1)
FILAS = M.fila(286) + 1
R, B, V, P = 'rojo-recoleta', 'blanco-recoleta', 'vidrio', 'piedra'
EJE = 264                                       # eje del pabellón
EJES = [140, 206, 264, 322, 392, 485, 579]      # ventanas de arriba

macizos = [
    (R, 45, 598, 100, 272),                     # muro
    (R, 440, 598, 90, 100),                     # parte derecha, más alta
    (R, 170, 358, 80, 100),                     # pabellón
    (P, 45, 598, 272, 287),                     # zócalo
]
for r in range(M.fila(36), M.fila(80)):         # frontón por filas, por dentro de sus cornisas
    y0 = M.y0 + r * M.paso_px
    m = 104 * (y0 - 34) / 47
    if m > 0: macizos.append((R, EJE - m, EJE + m, y0, y0 + M.paso_px))

ventana = lambda c, y0, y1, a=15: [M.zona(B, c - a - 3, c + a + 3, y0 - 3, y1), M.zona(V, c - a, c + a, y0, y1)]
zonas = [
    M.zona(B, 45, 440, 96, 102), M.zona(B, 440, 598, 86, 92),                  # cornisas
    *[M.zona(B, a, b, 88, 96, relleno='rayas') for a, b in ((100, 170), (358, 436))],   # balaustradas
    M.zona(B, 165, 363, 78, 86),                                               # base del frontón
    M.zona(B, EJE - 7, EJE + 7, 52, 66),                                       # escudo
    M.zona(B, EJE - 4, EJE + 4, 16, 36),                                       # remate
    *[M.zona(B, x - 4, x + 4, 102, 182) for x in (177, 235, 293, 351)],        # pilastras del pabellón
    *[M.zona(B, x - 4, x + 4, 92, 272) for x in (440, 538)],                   # pilastras de la derecha
    M.zona(B, 536, 540, 40, 92),                                               # aguja de la torrecita
    *[c for x in EJES for c in ventana(x, 120, 174)],                          # ventanas de arriba, iguales
    *[M.zona(B, x - 22, x + 22, 108, 114) for x in (206, 264, 322)],           # sus cornisitas en el pabellón
    M.zona(B, 45, 598, 182, 190),                                              # moldura del medio
    *[c for x in (74, 140, 392, 579) for c in ventana(x, 222, 266, 13)],       # planta baja
    *[M.zona(V, x - 14, x + 14, 210, 272) for x in (206, 322)],                # puertas
    M.zona(V, EJE - 18, EJE + 18, 206, 272),                                   # entrada
    *[M.zona(B, x - 4, x + 4, 196, 272) for x in (235, 293)],                  # columnas de la marquesina
    M.zona(V, 196, 332, 190, 198),                                             # marquesina
    M.zona(B, 450, 520, 192, 272),                                             # portal
    M.zona(V, 461, 509, 214, 272),
]
rectas = [M.recta(B, 160, 81, EJE, 34), M.recta(B, EJE, 34, 368, 81)]       # cornisas del frontón
arcos = [M.arco(V, 461, 509, M.y0 + M.fila(214) * M.paso_px, 13)]              # el arco del portal

lineas = M.lineas(FILAS, macizos)
escribir(sys.argv[1], 'argentina', '1980', {'separacion': 0.3, 'lineas': lineas, 'zonas': zonas, 'rectas': rectas, 'arcos': arcos})
print(len(lineas), 'líneas, ancho', M.ancho)
