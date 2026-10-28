# Puente de la Mujer (Calatrava, 1998–2001), medido sobre referencias/simbolos/puente de la mujer/mujer.jpg
# (10 px por unidad). El ala es una cuña: bandas inclinadas que se juntan en la punta; donde nace, cada
# banda dobla en curva y se acuesta sobre el tablero (la de arriba más lejos, la de abajo sobre la pila). Los tirantes
# son tiras casi transparentes, perpendiculares al ala, que bajan al tablero. Abajo, la pila y el agua del dique.
import sys
from armar import Medida, escribir

M = Medida(0, 800, 50, 13)
FILAS = M.fila(505)
B, SO, TI, A, A2 = 'pm-blanco', 'pm-sombra', 'pm-tirante', 'pm-agua', 'pm-agua-2'
PUNTA = (665, 55)
arriba = lambda x: 55 + (660 - x) * 0.70                      # borde de arriba del ala, recto hasta x = 330
abajo = lambda x: 58 + (665 - x) * 0.91                       # borde de abajo
NACE = 330

macizos = [
    (B, 0, 800, 401, 414),                                    # tablero
    (SO, 0, 800, 414, 427),
    *[(c, 0, 800, y, y + 13) for c, y in ((A, 440), (A2, 453), (A, 466), (A2, 479), (A, 492))],   # agua
    (B, 252, 308, 427, 479),                                  # pila
    (B, 262, 298, 479, 492),
]

# Tirantes: de un punto del borde de abajo, perpendiculares al ala (bajan 1.25 por cada px a la derecha).
tirantes = [M.recta(TI, x, abajo(x), x + (401 - abajo(x)) / 1.25, 401) for x in range(350, 600, 24)]
# El ala: veinticinco bandas (se pisan, sin huecos) desde x = 330, repartidas entre los dos bordes, que terminan juntas en la punta.
n = 25
ala = [M.recta(B, NACE - 3, y0 + 2, PUNTA[0], PUNTA[1] + 4 * k / (n - 1))
       for k in range(n) for y0 in [arriba(NACE) + k * (abajo(NACE) - arriba(NACE) - 10) / (n - 1)]]
# Donde nace el ala: cada banda sigue en curva (Bézier, en tramos rectos) hasta acostarse sobre el tablero.
def doblez(y0, x_fin, y_fin=394, tramos=10):
    dx = NACE - x_fin
    p = [(NACE, y0), (NACE - 0.45 * dx, min(y_fin, y0 + 0.45 * dx * 0.70)), (x_fin + 0.45 * dx, y_fin), (x_fin, y_fin)]
    punto = lambda t: tuple(sum(c * q[i] for c, q in zip(((1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3), p)) for i in (0, 1))
    pts = [punto(k / tramos) for k in range(tramos + 1)]
    return [M.recta(B, b[0] - 1.5, b[1], a[0] + 1.5, a[1]) for a, b in zip(pts, pts[1:])]   # se pisan: sin costuras
pie = [r for k in range(n) for r in doblez(arriba(NACE) + k * (abajo(NACE) - arriba(NACE) - 10) / (n - 1), 290 * k / (n - 1) - 0)]
zonas = [M.zona(SO, 290, 308, 427, 492)]                      # sombra de la pila

lineas = M.lineas(FILAS, macizos)
escribir(sys.argv[1], 'argentina', '2000', {'separacion': 0.3, 'lineas': lineas, 'zonas': zonas, 'rectas': tirantes + pie + ala})
print(len(lineas), 'líneas, ancho', M.ancho)
