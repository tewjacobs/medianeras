# Centro Cultural Kirchner (B4FS, 2015): el edificio cortado a la mitad. A la izquierda, la mitad del
# Palacio de Correos medida en píxeles sobre referencias/simbolos/Centro Cultural Kirschner/
# Buenos_Aires_Centrum_Kirchner.jpg (achicada a 1400 de ancho), con el eje en x 700: mansarda con
# buhardillas, cúpula con el reloj, columnas, ventanas y arcos. A la derecha, en lugar de la otra mitad,
# la Ballena Azul (de la foto de adentro): recta del lado del edificio, redondeada y más ancha arriba,
# con el borde de la terraza encendido, sobre su núcleo de hormigón.
import sys
from armar import Medida, escribir

M = Medida(245, 1155, 165, 16)
FILAS = M.fila(812) + 1
EJE = 700
P, C, PZ, V, H = 'cck-piedra', 'cck-columna', 'pizarra', 'vidrio', 'hormigon'
B1, B2, BL = 'ballena', 'ballena-2', 'ballena-luz'

macizos = [
    (P, 245, EJE, 355, 812),                     # cuerpo
    (PZ, 262, 555, 292, 345),                    # mansarda del ala
    (P, 555, EJE, 330, 355),                     # ático del centro
    (P, 650, EJE, 195, 330),                     # pabellón del reloj
    (H, 900, 980, 650, 812),                     # núcleo de la ballena
]
for r in range(M.fila(185), M.fila(330)):        # cúpula: se abre hacia abajo
    y0 = M.y0 + r * M.paso_px
    m = 90 + 50 * min(1, max(0, y0 - 185) / 105) ** 0.5             # hombro redondeado
    macizos.append((PZ, EJE - m, 650, y0, y0 + M.paso_px))
# Ballena: borde de afuera redondeado (y, x), lado del edificio recto con la panza redondeada abajo.
afuera = [(300, 1075), (318, 1108), (345, 1122), (420, 1124), (500, 1112), (560, 1088), (605, 1050), (632, 1000), (648, 940)]
def borde(y, pares):
    for (ya, xa), (yb, xb) in zip(pares, pares[1:]):
        if ya <= y <= yb: return xa + (xb - xa) * (y - ya) / (yb - ya)
for r in range(M.fila(300), M.fila(650)):
    y0 = M.y0 + r * M.paso_px; y = y0 + M.paso_px / 2
    x0 = 712 if y < 605 else borde(y, [(605, 714), (632, 735), (648, 790)]) or 790
    macizos.append((B1 if r % 2 else B2, x0, borde(y, afuera) or 940, y0, y0 + M.paso_px))

ventana = lambda x, y0, y1, a=13: M.zona(V, x - a, x + a, y0, y1)
alas = (320, 385, 450, 515)
zonas = [
    M.zona(P, 245, EJE, 345, 360),                                            # cornisa
    *[M.zona(P, x - 14, x + 14, 312, 345) for x in (325, 390, 455, 518)],     # buhardillas
    *[M.zona(V, x - 6, x + 6, 322, 345) for x in (325, 390, 455, 518)],
    M.zona(PZ, 655, EJE, 205, 230),                                           # techo del pabellón
    M.zona(C, 676, EJE, 228, 256),                                            # reloj (medio)
    *[ventana(x, 380, 410) for x in alas],                                    # ventanas del ala, por piso
    *[ventana(x, 448, 478) for x in alas],
    *[ventana(x, 505, 540) for x in alas],
    M.zona(P, 245, EJE, 548, 556),                                            # moldura
    *[ventana(x, 570, 598) for x in alas],
    *[ventana(x, 625, 680) for x in alas],
    *[M.zona(C, x - 9, x + 9, 372, 548) for x in (565, 595, 655, 680)],       # columnas del centro
    *[ventana(x, 395, 425, 10) for x in (620,)],
    *[ventana(x, 478, 545, 12) for x in (622,)],
    ventana(EJE - 4, 478, 545, 12),
    *[ventana(x, 595, 680, 14) for x in (628, EJE - 4)],
    M.zona(P, 245, EJE, 688, 700),                                            # base del piano nobile
    *[M.zona(V, x - 20, x + 20, 742, 812) for x in (302, 373, 445, 513, 628)],   # arcos de planta baja
    M.zona(V, EJE - 20, EJE, 742, 812),
    M.zona(BL, 712, 1080, 290, 302),                                          # terraza encendida
]
apoyo = lambda y: M.y0 + M.fila(y) * M.paso_px
arcos = [M.arco(V, x - 20, x + 20, apoyo(742), 20) for x in (302, 373, 445, 513, 628)] + \
        [M.arco(V, x - 13, x + 13, apoyo(625), 13) for x in alas]

lineas = M.lineas(FILAS, macizos)
escribir(sys.argv[1], 'argentina', '2010', {'lineas': lineas, 'zonas': zonas, 'arcos': arcos}, sacar=('alinear',))
print(len(lineas), 'líneas, ancho', M.ancho)
