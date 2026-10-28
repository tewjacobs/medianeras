# Palacio Barolo (Palanti, 1919–1923): de frente y simétrico sobre el eje de la torre, con las
# proporciones de referencias/simbolos/barolo/ (sobre todo la foto desde arriba, 16 px por unidad).
# De arriba abajo: aguja, faro encendido, cúpula con nervios, tambor, escalones con cupulitas, los
# pisos de la torre (ventanas en arco, balcón corrido, arcos góticos) y, a los costados, las mansardas
# verdes con nervios de piedra, ojos de buey y ventanas en arco. Debajo (foto de frente, Palacio-Barolo-1024x802),
# siete pisos con balcones redondos, la franja de ventanales y la planta baja con el arco de la entrada.
import sys
from armar import Medida, escribir

M = Medida(0, 44, 0, 1.3)
FILAS = M.fila(148.4)
EJE = 22
PI, SO, VE, V, S = 'barolo-piedra', 'barolo-sombra', 'barolo-verde', 'vidrio', 'sol'
centrado = lambda c, m, y0, y1: (c, EJE - m, EJE + m, y0, y1)
pares = lambda d: (EJE - d, EJE + d)
filas_de = lambda y0, y1: [(r * M.paso_px, r * M.paso_px + M.paso_px) for r in range(M.fila(y0), M.fila(y1))]

macizos = [
    centrado(SO, 0.3, 0, 7.5),                                # aguja
    centrado(PI, 1.4, 7.5, 8.75),                             # tapita del faro
    centrado(SO, 2.7, 8.75, 13.4),                            # faro
    centrado(PI, 5.6, 19.1, 26.25),                           # tambor
    centrado(PI, 11.9, 33.75, 45.9),                          # pisos altos de la torre
    centrado(SO, 19, 72, 76.25),                              # terrazas a los costados de la torre
]
for a, b in filas_de(13.4, 19.1):                             # cúpula: se abre hacia abajo
    macizos.append(centrado(PI, 2.8 + 2.6 * (max(0, a - 13.4) / 5.7) ** 0.5, a, b))
for a, b in filas_de(26.25, 33.75):                           # escalones que bajan del tambor
    macizos.append(centrado(PI, 6.2 + 2.8 * (a - 26.25) / 7.5, a, b))
for a, b in filas_de(76.25, 93.75):                           # mansardas: el borde de afuera se curva
    afuera = 20.5 + 1.5 * min(1, max(0, a - 76.25) / 6) ** 0.5
    macizos.append(centrado(VE, afuera, a, b))
macizos += [
    centrado(PI, 11.25, 45.9, 100.6),                         # el cuerpo de la torre
    centrado(PI, 22, 93.75, 148.4),                           # el cuerpo de abajo
]

ventana = lambda x, y0, y1, m: [M.zona(V, x - m, x + m, y0, y1)]
en_arco = lambda x, y0, y1, m, c=V: [M.zona(c, x - m, x + m, y0, y1)]
techo = lambda x, y, m, c=V: M.arco(c, x - m, x + m, M.fila(y) * M.paso_px, m)
BAHIAS = (13.1, 16.7, 20.2)                                   # centros de las bahías de cada mansarda
PISOS = [100.9 + 4.6 * k for k in range(7)]

zonas = [
    M.zona(S, EJE - 2, EJE + 2, 9.3, 12.9, relleno='rayas', fondo=V),             # la luz del faro
    *[M.zona(SO, x - 0.15, x + 0.15, 15, 19.1) for x in (*pares(1.6), *pares(3.4))],   # nervios de la cúpula
    M.zona(PI, EJE - 6.2, EJE + 6.2, 19.1, 20.3),                                  # cornisa del tambor
    *[z for x in (EJE, *pares(3)) for z in ventana(x, 21.8, 24.6, 0.5)],
    *[M.zona(SO, x - 0.4, x + 0.4, 27, 33.75) for x in (*pares(4.2), *pares(6.8))],  # contrafuertes
    *[M.zona(PI, x - 1.3, x + 1.3, 31.2, 33.75) for x in pares(9.6)],              # tambores de las cupulitas
    *[z for x in (*pares(2), *pares(6)) for z in en_arco(x, 35, 37.6, 0.9)],
    M.zona(PI, EJE - 12.5, EJE + 12.5, 38.1, 39.4),                                # cornisa
    M.zona(SO, EJE - 12.5, EJE + 12.5, 39.4, 40.2),
    *[z for x in (*pares(2), *pares(6), *pares(9.6)) for z in ventana(x, 40.6, 43, 0.9)],
    M.zona(PI, EJE - 13.6, EJE + 13.6, 43.4, 45.9),                                # balcón corrido
    M.zona(SO, EJE - 13.2, EJE + 13.2, 44.2, 45.4, relleno='rayas'),
    *en_arco(EJE, 48.4, 54, 2.4), *[z for x in pares(6.5) for z in en_arco(x, 49, 54, 1.3)],
    M.zona(PI, EJE - 12, EJE + 12, 54, 55.6), M.zona(SO, EJE - 12, EJE + 12, 55.6, 56.5),
    *[z for x in (EJE, *pares(3.5), *pares(7.5)) for z in ventana(x, 57, 59.6, 0.6)],
    # Arcos góticos: el hueco en sombra y la ventana adentro.
    M.zona(SO, EJE - 3.6, EJE + 3.6, 63.5, 71.6), *en_arco(EJE, 65.4, 71.6, 2.2),
    *[z for x in pares(7.8) for z in (M.zona(SO, x - 1.8, x + 1.8, 65.4, 71.6), *en_arco(x, 66.8, 71.6, 1))],
    *[M.zona(PI, x - 1.6, x + 1.6, 66.2, 67.4) for x in pares(11.6)],              # balconcitos salientes
    M.zona(PI, EJE - 11.8, EJE + 11.8, 71.6, 72.9),
    *[z for x in (EJE, *pares(3.5), *pares(7.5)) for z in ventana(x, 73.4, 75.6, 0.9)],
    M.zona(SO, EJE - 11.8, EJE + 11.8, 75.8, 76.9, relleno='rayas'),
    # Pisos de la torre, entre las mansardas.
    *[z for y in (77.6, 81.9, 86.2, 90.5) for x in (EJE, *pares(3.4), *pares(7.4)) for z in ventana(x, y, y + 2.8, 0.9)],
    *[M.zona(SO, x - 1.5, x + 1.5, y + 2.8, y + 3.7, relleno='rayas') for y in (77.6, 81.9, 86.2, 90.5) for x in pares(7.4)],
    # Mansardas: nervios de piedra, ojos de buey (aro de piedra) y ventanas en arco.
    *[M.zona(PI, x - 0.25, x + 0.25, 77, 93.75) for d in (14.9, 18.45) for x in pares(d)],
    *[M.zona(PI, x - 0.3, x + 0.3, 80, 93.75) for x in (0.3, 43.7)],
    *[c for d in BAHIAS for x in pares(d) for c in (
        M.zona(PI, x - 0.9, x + 0.9, 77.9, 80.5), M.zona(PI, x - 1.2, x + 1.2, 78.5, 79.9),
        M.zona(V, x - 0.5, x + 0.5, 78.5, 79.9))],
    *[M.zona(V, x - 0.8, x + 0.8, y + 0.3, y + 3) for d in BAHIAS for x in pares(d) for y in (82.6, 87.6)],
    # Arcada debajo de las mansardas.
    M.zona(SO, 0, 44, 93.75, 94.9, relleno='rayas'),
    *[z for d in BAHIAS for x in pares(d) for z in en_arco(x, 96.4, 99.2, 1.1)],
    *[z for x in (EJE, *pares(3.4), *pares(7.4)) for z in ventana(x, 95.6, 99.2, 0.9)],
    M.zona(SO, 0, 44, 99.4, 100.6),
    # Siete pisos: ventanas sobre los mismos ejes y balcones redondos en los bordes de la torre y en las puntas.
    *[z for y in PISOS for x in (EJE, *pares(3.4), *pares(7.4), *[e for d in BAHIAS for e in pares(d)]) for z in ventana(x, y + 0.6, y + 3.4, 0.8)],
    *[z for y in PISOS for x in (*pares(11.25), *pares(20.8)) for z in (
        M.zona(PI, x - 1.8, x + 1.8, y + 3.4, y + 4.7), M.zona(SO, x - 1.6, x + 1.6, y + 3.4, y + 4.7, relleno='rayas'),
        M.zona(SO, x - 1.1, x + 1.1, y + 4.7, y + 5.4))],
    *[M.zona(SO, x - 0.2, x + 0.2, 100.6, 133.2) for x in pares(11.25)],                 # bordes de la torre
    # Balcón corrido y franja de ventanales.
    M.zona(PI, 0, 44, 133.2, 134.5), M.zona(SO, 0, 44, 134.5, 135.8, relleno='rayas'),
    *[c for d in BAHIAS for x in pares(d) for c in (
        M.zona(V, x - 1.4, x + 1.4, 136.6, 142.4, relleno='rayas', fondo=SO),)],
    M.zona(PI, 0, 44, 142.6, 143.8),
    # Planta baja: vidrieras, el arco de la entrada con su lámpara y sus pilares.
    *[M.zona(V, x - 1.5, x + 1.5, 144.4, 148.4) for d in BAHIAS for x in pares(d)],
    M.zona(SO, EJE - 9.6, EJE + 9.6, 137.8, 148.4), M.zona(V, EJE - 8.4, EJE + 8.4, 137.8, 148.4, relleno='rayas', fondo=SO),
    M.zona(S, EJE - 0.6, EJE + 0.6, 138.4, 141),
    *[M.zona(PI, x - 1, x + 1, 137.8, 148.4) for x in pares(10.4)],
]
arcos = [
    *[M.arco(PI, x - 1.3, x + 1.3, M.fila(31.2) * M.paso_px, 1.6) for x in pares(9.6)],   # cupulitas
    *[techo(x, 35, 0.9) for x in (*pares(2), *pares(6))],
    techo(EJE, 48.4, 2.4), *[techo(x, 49, 1.3) for x in pares(6.5)],
    M.arco(SO, EJE - 3.6, EJE + 3.6, M.fila(63.5) * M.paso_px, 4.2),             # punta gótica
    M.arco(V, EJE - 2.2, EJE + 2.2, M.fila(65.4) * M.paso_px, 2.8),
    *[a for x in pares(7.8) for a in (M.arco(SO, x - 1.8, x + 1.8, M.fila(65.4) * M.paso_px, 2.2),
                                      M.arco(V, x - 1, x + 1, M.fila(66.8) * M.paso_px, 1.3))],
    *[techo(x, y + 0.3, 0.8) for d in BAHIAS for x in pares(d) for y in (82.6, 87.6)],
    *[techo(x, 96.4, 1.1) for d in BAHIAS for x in pares(d)],
    M.arco(SO, EJE - 9.6, EJE + 9.6, M.fila(137.8) * M.paso_px, 9.6),           # arco de la entrada
    M.arco(V, EJE - 8.4, EJE + 8.4, M.fila(137.8) * M.paso_px, 8.4),
]

lineas = M.lineas(FILAS, macizos)
escribir(sys.argv[1], 'argentina', '1920', {'separacion': 0.3, 'alto': 280, 'lineas': lineas, 'zonas': zonas, 'arcos': arcos})
print(len(lineas), 'líneas, ancho', M.ancho)
