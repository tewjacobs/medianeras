# Hôtel de l'Indépendance (Dakar), de frente, sobre las fotos de referencias/simbolos/hotel/ (la de la calle y la de
# frente, 72_big.jpg). La fachada de celdas alternadas como un tablero: cada celda, una abertura honda con su marco de
# biseles (arriba con luz, a los costados medio, abajo en sombra) y las sombras en triángulo entre celdas; el borde de
# la derecha dentado por las celdas que asoman. A la izquierda, la franja de ladrillo con el canto de las celdas del
# costado. Arriba, la cornisa almenada; abajo, los dos pisos de ventanas con sus cajones y las columnas de la planta
# baja, con el local en sombra detrás.
# Uso: hotel.py <simbolos.json> (pone programas.Hotel).
import sys
from armar import Lienzo, guardar

H, V = 8, 5                 # medio paso de las celdas a lo ancho (unidades) y alto de cada fila de celdas (líneas)
COLUMNAS, FILAS = 7, 21     # medias columnas de la cara y filas de celdas
COSTADO, LADRILLO = 4, 10   # canto de las celdas del costado y franja de ladrillo
X0 = COSTADO + LADRILLO     # donde empieza la cara de las celdas
ANCHO = X0 + COLUMNAS * H + 4
ALMENAS, CELDAS = 0, 6      # primera fila de las almenas y de las celdas
PISOS = CELDAS + FILAS * V + 3
PILOTES = PISOS + 14
FIN = PILOTES + 22

l = Lienzo(ANCHO, FIN + 1)

def celda(x, f, vidrio='ho-vidrio'):
    # Una celda de 8 x 8 vista de frente: un marco en tronco de pirámide (cuatro biseles: luz arriba, medio a la
    # izquierda, sombra a la derecha y abajo) alrededor de la abertura honda de 4 x 4, con el vidrio en el fondo.
    for r in range(8):
        for i in range(32):
            u, v = (i + 0.5) / 4, r + 0.5
            if 2 <= u < 6 and 2 <= v < 6:
                c = vidrio if 2.75 <= u < 5.25 and v >= 3 else 'ho-hueco'
            else:
                c = min((v, 'ho-bisel-luz'), (u, 'ho-bisel'), (8 - u, 'ho-bisel-s'), (8 - v, 'ho-bisel-s2'))[1]
            l.rect(c, x + i / 4, x + (i + 1) / 4, f + r, f + r + 1)

# El hormigón de la cara y las celdas, de arriba hacia abajo (las de abajo tapan el pie de las de arriba).
l.rect('ho-crema', X0, X0 + COLUMNAS * H, CELDAS, PISOS)
for r in range(FILAS):
    f = CELDAS + r * V
    for k in range(r % 2, COLUMNAS + 1, 2):
        x = X0 + k * H - H / 2
        if x + H > ANCHO: continue
        n = (r * 73 + k * 151 + r * k * 37) % 13                     # algunas ventanas con la cortina corrida, salteadas
        celda(x, f, 'ho-cortina' if n == 2 else 'ho-cortina-clara' if n in (5, 9) else 'ho-vidrio')
        # La sombra que tira la celda en el hueco de abajo: un triángulo con la punta hacia abajo.
        if x >= X0:
            l.rect('ho-tri', x + 1, x + H - 1, f + 8, f + 9)
            l.rect('ho-tri', x + 2.5, x + H - 2.5, f + 9, f + 10)
# La cara de la izquierda de la primera media celda queda cortada por el ladrillo.
l.rect('ho-ladrillo', COSTADO, X0, ALMENAS + 3, PILOTES)
for f in range(CELDAS, PILOTES, 3):
    l.rect('ho-ladrillo-j', COSTADO, X0, f, f + 1)
l.rect('ho-ladrillo-s', X0 - 1, X0, ALMENAS + 3, PILOTES)
# El canto de las celdas del costado: dientes que asoman a la izquierda del ladrillo.
for r in range(FILAS):
    f = CELDAS + r * V
    l.rect('ho-bisel', 0 if r % 2 else 1.5, COSTADO, f, f + 3)
    l.rect('ho-bisel-s2', 0 if r % 2 else 1.5, COSTADO, f + 3, f + 4)

# El cartel verde arriba de la franja de ladrillo, con las letras claras.
l.rect('ho-cartel', COSTADO - 1, X0 + 1, ALMENAS, ALMENAS + 4)
l.rect('ho-cartel-s', COSTADO - 1, X0 + 1, ALMENAS + 3, ALMENAS + 4)
for i in range(5):
    l.rect('ho-letra', COSTADO + 0.5 + i * 2, COSTADO + 1.5 + i * 2, ALMENAS + 1, ALMENAS + 3)

# La cornisa almenada: una almena sobre cada media columna, con su remate.
for k in range(COLUMNAS + 1):
    x = X0 + k * H - 1.25
    if x + 2.5 > ANCHO: break
    l.rect('ho-crema', max(X0, x), x + 2.5, ALMENAS, CELDAS)
    l.rect('ho-bisel-s', x + 1.75, x + 2.5, ALMENAS + 1, CELDAS)
l.rect('ho-bisel-luz', X0, X0 + COLUMNAS * H, CELDAS - 1, CELDAS)

# Los dos pisos de ventanas, con los cajones de las ventanas entre pilastras.
l.rect('ho-crema', COSTADO, ANCHO - 1, PISOS, PILOTES)
for piso in (PISOS + 1, PISOS + 7):
    for k in range(COLUMNAS):
        x = X0 + k * H
        l.rect('ho-hueco', x + 1, x + H - 1, piso, piso + 4)
        l.rect('ho-vidrio-claro', x + 1.5, x + H - 1.5, piso + 1, piso + 4)
        l.rect('ho-bisel-s2', x + 0.75, x + H - 0.75, piso + 4, piso + 5)
l.rect('ho-bisel-s', COSTADO, ANCHO - 1, PILOTES - 2, PILOTES)

# La planta baja: el local en sombra y las columnas, con su capitel; la vereda.
l.rect('ho-local', COSTADO, ANCHO - 1, PILOTES, FIN)
for k in range(COLUMNAS + 1):
    x = X0 + k * H - 1 if k else X0 - 1
    x = min(x, ANCHO - 3)
    l.rect('ho-columna', x, x + 2, PILOTES, FIN)
    l.rect('ho-bisel-s', x + 1.25, x + 2, PILOTES, FIN)
    l.rect('ho-crema', x - 0.5, x + 2.5, PILOTES, PILOTES + 1)
for k in range(COLUMNAS):
    x = X0 + k * H
    l.rect('ho-vidriera', x + 1.5, x + H - 2.5, PILOTES + 9, FIN)
# El cartel azul del hotel entre dos columnas, con su letrero claro.
l.rect('ho-azul', X0 + 3 * H + 1.5, X0 + 5 * H - 1.5, PILOTES + 4, PILOTES + 7)
l.rect('ho-letra', X0 + 3 * H + 3, X0 + 5 * H - 3, PILOTES + 5, PILOTES + 6)
l.rect('ho-vereda', 0, ANCHO, FIN, FIN + 1)

COLORES = {
    'ho-crema': ('#ddcdb6', '#ddcdb6'), 'ho-bisel-luz': ('#f0e5d4', '#f0e5d4'), 'ho-bisel': ('#cdb99e', '#cdb99e'),
    'ho-bisel-s': ('#b29c80', '#b29c80'), 'ho-bisel-s2': ('#9a8366', '#9a8366'), 'ho-hueco': ('#2b2321', '#2b2321'),
    'ho-vidrio': ('#3f3a38', '#3f3a38'), 'ho-tri': ('#5b3c31', '#5b3c31'),
    'ho-ladrillo': ('#7b4a3c', '#7b4a3c'), 'ho-ladrillo-j': ('#6c3f33', '#6c3f33'), 'ho-ladrillo-s': ('#5d362c', '#5d362c'),
    'ho-vidrio-claro': ('#55606a', '#55606a'), 'ho-local': ('#3a3331', '#3a3331'), 'ho-columna': ('#e4d7c4', '#e4d7c4'),
    'ho-vidriera': ('#4d5a62', '#4d5a62'), 'ho-vereda': ('#a99d8c', '#a99d8c'),
    'ho-cortina': ('#b5874f', '#b5874f'), 'ho-cortina-clara': ('#cfc3ad', '#cfc3ad'),
    'ho-cartel': ('#2f6b4f', '#2f6b4f'), 'ho-cartel-s': ('#24523d', '#24523d'), 'ho-letra': ('#eef0e6', '#eef0e6'),
    'ho-azul': ('#3d86b5', '#3d86b5'),
}

p = {'nota': ("El Hôtel de l'Indépendance de Dakar, de frente: la fachada de celdas alternadas como un tablero, cada una "
              'una abertura honda con su marco de biseles (luz arriba, sombra abajo) y las sombras en triángulo entre '
              'celdas; a la izquierda, la franja de ladrillo con el canto de las celdas del costado; arriba, la cornisa '
              'almenada y el cartel verde; algunas ventanas con la cortina corrida; abajo, los dos pisos de ventanas y las columnas de la planta baja con el cartel azul.'),
     'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}
p.update(placa='hotel-cola', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='hotel-cola-marco')
guardar(sys.argv[1], 'programas', 'Hotel', p, COLORES, 'ho-|h-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
