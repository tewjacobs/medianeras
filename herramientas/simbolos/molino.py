# Confitería del Molino (Gianotti, 1916–1917): la esquina vista de frente, simétrica sobre su eje,
# con las proporciones de referencias/simbolos/el molino/ (la foto entera y la de la torre). Medido en
# unidades: la aguja con su anillo, el chapitel de pizarra con sus pináculos, la torre con las aspas
# (rectas) y las dos torrecitas, las alas con cuatro pisos de ventanas y balcones, y la confitería.
import sys
from armar import Medida, escribir

M = Medida(0, 44, 0, 1.3)            # 1 px = 1 unidad
FILAS = M.fila(72)
EJE = 22
PI, PZ, SO, V, H, S = 'molino-piedra', 'molino-pizarra', 'molino-sombra', 'vidrio', 'hierro', 'sol'
centrado = lambda c, m, y0, y1: (c, EJE - m, EJE + m, y0, y1)

macizos = [
    centrado(PZ, 0.4, 0, 7),                                  # aguja
    centrado(PZ, 1.8, 7.5, 10.5),                             # linterna
    (PI, 2, 42, 35, 63),                                      # alas
    centrado(PI, 5, 22, 35),                                  # cuerpo de la torre
    (H, 2, 42, 63, 72),                                       # confitería
]
for r in range(M.fila(10.5), M.fila(22)):                     # chapitel: se abre hacia abajo
    y0 = r * M.paso_px
    macizos.append(centrado(PZ, 1.6 + 2.6 * (y0 - 10.5) / 11.5, y0, y0 + 1.3))

zonas = [
    M.zona(PI, EJE - 3.2, EJE + 3.2, 6.5, 8),                                    # anillo
    M.zona(PI, EJE - 0.8, EJE + 0.8, 3, 4.3),                                    # bolita de la aguja
    *[M.zona(V, x - 0.4, x + 0.4, 13, 20) for x in (EJE - 1.2, EJE + 1.2)],      # ventanitas del chapitel
    *[M.zona(PI, x - 0.6, x + 0.6, 17, 22) for x in (EJE - 5, EJE + 5)],         # pináculos
    M.zona(PI, EJE - 5.6, EJE + 5.6, 21, 22.3),                                  # cornisa de la torre
    *[M.zona(PI, x - 1, x + 1, 24, 33) for x in (EJE - 6.6, EJE + 6.6)],         # torrecitas, despegadas
    *[M.zona(PI, x - 0.5, x + 0.5, 33, 34.5) for x in (EJE - 6.6, EJE + 6.6)],
    M.zona(V, EJE - 1.6, EJE + 1.6, 24.5, 31),                                   # ventana detrás de las aspas
    M.zona(H, EJE - 2.4, EJE + 2.4, 31, 32.3, relleno='rayas'),                  # balconcito
    M.zona(H, 2, 42, 33.5, 35, relleno='rayas'),                                 # baranda del techo
    M.zona(PI, 1.5, 42.5, 35, 36.3),                                             # cornisa
    *[M.zona(SO, x - 0.3, x + 0.3, 36.3, 62) for x in (EJE - 4, EJE + 4)],          # bordes de la bahía de la esquina
    *[M.zona(V, x - 1.1, x + 1.1, y, y + 4) for y in (38, 44.5, 51, 57.5) for x in (5.5, 10.5, 15, 29, 33.5, 38.5)],
    *[M.zona(V, EJE - 1.4, EJE + 1.4, y, y + 4) for y in (38, 44.5, 51)],         # ventanas de la bahía
    *[M.zona(H, x - 1.6, x + 1.6, y + 4, y + 5.3, relleno='rayas') for y in (38, 44.5, 51, 57.5) for x in (5.5, 10.5, 15, 29, 33.5, 38.5)],
    *[M.zona(H, EJE - 2.6, EJE + 2.6, y + 4, y + 5.3, relleno='rayas') for y in (38, 44.5, 51)],
    M.zona(V, EJE - 2.2, EJE + 2.2, 57.5, 63),                                   # el arco de la esquina
    M.zona(PI, 1.5, 42.5, 62, 63.3),                                             # marquesina
    *[M.zona(S, x - 1.4, x + 1.4, 65, 70.5) for x in (5.5, 10.5, 15, 29, 33.5, 38.5)],   # vitrales
    M.zona(S, EJE - 2.6, EJE + 2.6, 65, 70.5),
]
rectas = [M.recta(H, EJE - 5.5, 31.5, EJE + 5.5, 22.5), M.recta(H, EJE - 5.5, 22.5, EJE + 5.5, 31.5)]  # aspas
arcos = [M.arco(V, x - 1.1, x + 1.1, M.fila(38) * M.paso_px, 1.1) for x in (5.5, 10.5, 15, 29, 33.5, 38.5)] + \
        [M.arco(V, EJE - 2.2, EJE + 2.2, M.fila(57.5) * M.paso_px, 2.2), M.arco(V, EJE - 1.6, EJE + 1.6, M.fila(24.5) * M.paso_px, 1.6)]

lineas = M.lineas(FILAS, macizos)
escribir(sys.argv[1], 'argentina', '1910', {'separacion': 0.3, 'alto': 210, 'lineas': lineas, 'zonas': zonas, 'rectas': rectas, 'arcos': arcos})
print(len(lineas), 'líneas, ancho', M.ancho)
