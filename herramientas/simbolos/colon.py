# Teatro Colón (Tamburini, Meano y Dormal; inaugurado en 1908), de frente, medido en píxeles sobre
# referencias/simbolos/colon/Fachada_del_Teatro_Colón… (achicada a 1600 × 1143). Piedra en filas;
# cornisas con dentículos y balaustradas (rayas), relieves, columnas, ventanas en arco, puertas y
# marquesina en zonas; el frontón grande y los dos chicos con rectas. Simétrico.
import sys
from armar import Medida, escribir

M = Medida(160, 1440, 85, 24.3)
FILAS = M.fila(1000) + 1
P, S, V, PU, MQ = 'colon-piedra', 'colon-sombra', 'colon-vidrio', 'colon-puerta', 'colon-marquesina'
EJE = 800
espejo = lambda x0, x1: [(x0, x1), (2 * EJE - x1, 2 * EJE - x0)]

macizos = [
    (P, 165, 1435, 335, 925),                                 # cuerpo
    (P, 160, 1440, 315, 335),                                 # cornisa, que vuela
    (P, 420, 1180, 300, 315),                                 # ático del centro
    *[(P, a, b, 245, 300) for a, b in espejo(445, 495)],      # remates del frontón
    *[(P, a, b, 295, 315) for a, b in espejo(175, 425)],      # áticos de los costados
    (S, 165, 1435, 925, 960),                                 # escalinata
    ('follaje', 160, 1440, 960, 1001),                        # pasto
]
for r in range(M.fila(150), M.fila(300)):                     # frontón por filas, por dentro de sus cornisas
    y0 = M.y0 + r * M.paso_px
    m = 375 * (y0 - 150) / 150
    if m > 0: macizos.append((P, EJE - m, EJE + m, y0, y0 + M.paso_px))
apoyo = lambda y: M.y0 + M.fila(y) * M.paso_px               # borde de arriba de la fila de y

ventanas = [310, 513, 680, 800, 920, 1087, 1290]
zonas = [
    M.zona(S, 160, 1440, 315, 335, relleno='rayas', fondo=P),                       # cornisa con dentículos
    M.zona(S, 420, 1180, 300, 312),
    M.zona(P, 780, 820, 85, 150),                                                   # remate de la punta
    *[M.zona(S, c - 40, c + 40, 395, 430) for c in (307, 680, 800, 920, 1293)],     # relieves del ático, iguales
    *[M.zona(S, c - 18, c + 18, 395, 430) for c in (513, 1087)],                    # medallones
    M.zona(S, 160, 1440, 482, 500, relleno='rayas', fondo=P),                       # cornisa del piso noble
    *[M.zona(S, c + d - 7, c + d + 7, 530, 715) for c in (310, 1290) for d in (-96, -72, 72, 96)],  # columnas
    *[M.zona(S, x - 7, x + 7, 530, 715) for c in (452, 585, 612, 740) for x in (c, 2 * EJE - c)],
    *[M.zona(V, c - 29, c + 29, 588, 700) for c in ventanas],                       # ventanas en arco
    *[M.zona(S, c - 45, c + 45, 700, 722, relleno='rayas') for c in (310, 513, 1087, 1290)],  # balcones
    M.zona(S, 597, 1003, 700, 722, relleno='rayas'),
    M.zona(S, 160, 1440, 735, 752),                                                 # cornisa de planta baja
    *[M.zona(PU, c - 29, c + 29, 775, 925) for c in (310, 513, 1087, 1290)],        # puertas, bajo sus ventanas
    M.zona(V, 597, 1003, 830, 925),                                                 # entrada
    M.zona(MQ, 595, 1005, 775, 835),                                                # marquesina
]
rectas = [M.recta(S, 425, 312, EJE, 145), M.recta(S, EJE, 145, 1175, 312),          # frontón grande
          *[r for c in (310, 1290) for r in (M.recta(S, c - 120, 478, c, 432), M.recta(S, c, 432, c + 120, 478))]]
arcos = [M.arco(V, c - 29, c + 29, apoyo(588), 28) for c in ventanas] + [M.arco(V, 745, 855, apoyo(290), 48)]   # y la luneta

lineas = M.lineas(FILAS, macizos)
escribir(sys.argv[1], 'argentina', '1900', {'separacion': 0.3, 'lineas': lineas, 'zonas': zonas, 'rectas': rectas, 'arcos': arcos})
print(len(lineas), 'líneas, ancho', M.ancho)
