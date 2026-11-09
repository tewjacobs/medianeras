# Asamblea Nacional de Bangladesh (Louis Kahn, Daca), de frente, medida sobre
# referencias/simbolos/daka/Bangladesh-National-Parliament-1920x1280.jpeg (px de la foto de 1920); el agua, como en
# Asamblea-Nacional-de-Bangladesh-de-Louis-Kahn.jpg.
# Simétrica sobre el eje (x = 900 en la foto), con la luz desde la izquierda: las caras de la izquierda al sol, las de
# la derecha en sombra, los cilindros sombreados como cilindros. De afuera hacia el centro: el bloque con el triángulo
# ancho y la ranura arriba; el bloque con el triángulo alto; la ranura oscura; el bloque con el triángulo alto; la cara
# metida con el ojo redondo; los dos cilindros; el entrante del medio con la puerta. Atrás, la corona octogonal con sus
# arcos. Hormigón con las juntas de mármol blanco. Abajo, el lago con el reflejo del edificio y sus ondas.
# Las curvas (arcos, ojos) se calculan por cuarto de unidad, a 3 px por línea, para que salgan parejas.
# Uso: daca.py <simbolos.json> (pone decadas.mundo.1980).
import sys, math
from armar import Lienzo, escribir, con_colores

EJE, MEDIO, PX = 900, 665, 3                       # eje de la foto, medio ancho dibujado y px por unidad
Y0, SUELO = 486, 812                               # arriba del dibujo y orilla del agua
REFLEJO = 150                                      # px de agua con reflejo
X = lambda px: round((px - (EJE - MEDIO)) / PX * 4) / 4
F = lambda py: round((py - Y0) / PX)
FILAS = F(SUELO) + round(REFLEJO / PX)
JUNTA = 5                                          # una junta horizontal cada 5 líneas (15 px, como en la foto)

l = Lienzo(X(EJE + MEDIO), FILAS)

# --- Colores: cada tono de hormigón tiene su junta (más clara) y su versión en sombra (lado derecho).
def hexa(c): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
def mezcla(a, b, t): return '#' + ''.join(f'{round(x + (y - x) * t):02x}' for x, y in zip(hexa(a), hexa(b)))
AGUA = '#6f8583'
COLORES = {}
def tono(nombre, sol, sombra=None, junta=0.4):
    sombra = sombra or mezcla(sol, '#3a3836', 0.55)
    for n, c in ((nombre, sol), (nombre + '-s', sombra)):
        COLORES[n] = (c, c)
        COLORES[n + '-j'] = (mezcla(c, '#f6f3ec', junta),) * 2

tono('bd-muro', '#d3cab9')                         # caras al frente
tono('bd-cara', '#948d82', '#5a5651', 0.3)         # caras metidas, en sombra propia
tono('bd-corona', '#cbc2b0')
tono('bd-corona2', '#aea594', '#77716a')
tono('bd-corona3', '#958d7e', '#5f5b55', 0.3)
tono('bd-canto', '#ece6d9', '#8a857d', 0)
CILINDRO = ['#f0eadf', '#e2dbcd', '#d1c9b8', '#bdb4a2', '#a49b8a', '#8c8476', '#787164']
for i, c in enumerate(CILINDRO): tono(f'bd-cil{i}', c, c)
for n, c in {'bd-hueco': '#1d1c1d', 'bd-hueco-luz': '#3b3733', 'bd-vidrio': '#39424a', 'bd-marco': '#8a8680',
             'bd-ojo-aro': '#4a4540', 'bd-orilla': '#4b4943', 'bd-agua': AGUA, 'bd-onda': '#9fb2ad',
             'bd-onda-o': '#5d716f'}.items():
    COLORES[n] = (c, c)

def lado(c, izq):
    # El color del lado derecho, en sombra: 'bd-muro' → 'bd-muro-s', 'bd-muro-j' → 'bd-muro-s-j'.
    s = c[:-2] + '-s-j' if c.endswith('-j') else c + '-s'
    return c if izq or s not in COLORES else s

# --- Ayudas en px del eje (d) y de la foto (y), pintando en los dos lados.
def franja(c, d0, d1, y0, y1, solo=None):
    for izq in (True, False):
        if solo and solo != ('izq' if izq else 'der'): continue
        a, b = (EJE - d1, EJE - d0) if izq else (EJE + d0, EJE + d1)
        l.rect(lado(c, izq), X(a), X(b), F(y0), F(y1))

def forma(c, y0, y1, medio_ancho, centro, corrida=0):
    # Fila por fila: medio_ancho(y) en px a la altura del centro de la fila (None o <= 0: nada). `corrida` mueve
    # la forma hacia afuera (+) en los dos lados.
    for f in range(F(y0), F(y1)):
        m = medio_ancho(Y0 + (f + 0.5) * PX)
        if m is None or m <= 0: continue
        for izq in (True, False):
            x = EJE - centro - corrida if izq else EJE + centro + corrida
            l.rect(lado(c, izq), X(x - m), X(x + m), f, f + 1)

def juntas(c, d0, d1, y0, y1, verticales=()):
    # Las juntas de mármol: horizontales cada JUNTA líneas contando desde la orilla, y las verticales pedidas.
    for f in range(F(SUELO) - JUNTA, F(y0), -JUNTA):
        if f < F(y1): franja(c + '-j', d0, d1, Y0 + f * PX, Y0 + (f + 1) * PX)
    for d in verticales:
        for izq in (True, False):
            x = EJE - d if izq else EJE + d
            l.rect(lado(c + '-j', izq), X(x), X(x) + 0.25, F(y0) + 2, F(y1))

def muro(c, d0, d1, y0, verticales=()):
    franja(c, d0, d1, y0, SUELO)
    juntas(c, d0, d1, y0, SUELO, verticales)
    franja('bd-canto', d0, d1, y0, y0 + PX)

def triangulo(d_punta, ancho, y_punta, y_base):
    # Abertura en triángulo con la punta arriba; adentro, pegado al borde de afuera, el canto del muro que recibe luz.
    alto = y_base - y_punta
    forma('bd-hueco', y_punta, y_base, lambda y: ancho / 2 * (y - y_punta) / alto, d_punta)
    for f in range(F(y_punta + alto * 0.15), F(y_base)):
        m = ancho / 2 * (Y0 + (f + 0.5) * PX - y_punta) / alto
        for izq in (True, False):
            borde = X(EJE - d_punta - m) if izq else X(EJE + d_punta + m)
            g = max(0.25, round(m / PX * 0.35 * 4) / 4)
            if izq: l.rect('bd-hueco-luz', borde, borde + g, f, f + 1)
            else: l.rect('bd-hueco-luz', borde - g, borde, f, f + 1)

def circulo(r, yc): return lambda y: math.sqrt(max(0, r * r - (y - yc) ** 2))

# --- La corona, atrás: tambor octogonal (la cara del medio al sol, las de los costados cada vez más en sombra).
for c, d0, d1, top in (('bd-corona', 0, 120, 492), ('bd-corona2', 120, 185, 500), ('bd-corona3', 185, 250, 510)):
    franja(c, d0, d1, top, 575)
    juntas(c, d0, d1, top, 575)
    franja('bd-canto', d0, d1, top, top + PX)
for centro, r, ya in ((75, 40, 548), (218, 22, 558)):   # arcos de medio punto, con un aro de luz
    forma('bd-canto', ya - r - 3, ya + 40, lambda y, r=r, ya=ya: (r + 3) if y > ya else circulo(r + 3, ya)(y), centro)
    forma('bd-hueco', ya - r, ya + 40, lambda y, r=r, ya=ya: r if y > ya else circulo(r, ya)(y), centro)

# --- Los bloques, de afuera hacia adentro.
muro('bd-muro', 510, 635, 608, (540, 600))
for c, d0 in (('bd-cil2', 615), ('bd-cil3', 624), ('bd-cil4', 631)):   # la punta redonda del bloque de afuera
    franja(c, d0, 635, 608, SUELO)
    juntas(c, d0, 635, 608, SUELO)
triangulo(562, 100, 688, 788)
franja('bd-hueco', 558, 566, 618, 682)                     # la ranura sobre el triángulo
muro('bd-muro', 400, 510, 600, (430, 455))
triangulo(486, 42, 630, 745)
franja('bd-hueco', 385, 400, 596, SUELO)                   # la ranura oscura entre bloques
franja('bd-hueco-luz', 397, 400, 596, SUELO)
muro('bd-muro', 260, 385, 584, (290, 380))
triangulo(336, 74, 612, 738)
franja('bd-hueco', 318, 354, 772, SUELO)                   # la puerta bajo el triángulo
muro('bd-cara', 170, 260, 575, (200, 240))                 # la cara metida, con el ojo
forma('bd-ojo-aro', 708, 793, circulo(42, 750.5), 216)
forma('bd-hueco-luz', 712, 789, circulo(38, 750.5), 216)
forma('bd-hueco', 712, 789, circulo(34, 750.5), 216, corrida=-4)   # el fondo del ojo; queda una media luna de luz
franja('bd-cara-s', 170, 182, 575, SUELO, solo='der')      # la sombra de los cilindros sobre la cara metida
franja('bd-cara', 170, 178, 575, SUELO, solo='izq')

# --- Los cilindros: sombreado de cilindro con la luz desde la izquierda, juntas que siguen el tono.
for izq in (True, False):
    a, b = (X(EJE - 175), X(EJE - 30)) if izq else (X(EJE + 30), X(EJE + 175))
    n = round((b - a) * 4)
    for i in range(n):
        t = 2 * (i + 0.5) / n - 1                       # -1 a 1 a lo ancho
        luz = math.cos(math.asin(t) + 0.55)
        k = min(len(CILINDRO) - 1, max(0, round((1 - luz) * 4.2)))
        x = a + i / 4
        l.rect(f'bd-cil{k}', x, x + 0.25, F(540), F(SUELO))
        for f in range(F(SUELO) - JUNTA, F(540), -JUNTA):
            l.rect(f'bd-cil{k}-j', x, x + 0.25, f, f + 1)
    for d in (60, 90, 120, 150):                         # juntas verticales
        x = X(EJE - d if izq else EJE + d)
        l.rect('bd-cil1-j', x, x + 0.25, F(540) + 2, F(SUELO))
    l.rect('bd-canto', a, b, F(540), F(540) + 1)

# --- El entrante del medio, en sombra, con la puerta vidriada.
muro('bd-cara', 0, 30, 548, (15,))
franja('bd-vidrio', 0, 18, 772, SUELO)
franja('bd-marco', 0, 18, 772, 775)
franja('bd-marco', 8, 9, 775, SUELO)

# --- La orilla y el lago con el reflejo: cada línea bajo la orilla copia en espejo la de arriba, mezclada con el
# agua; una línea de cada dos lleva ondas (cortes claros y oscuros) que se alargan hacia abajo.
l.rect('bd-orilla', 0, l.n / 4, F(SUELO) - 1, F(SUELO))
base = F(SUELO)
for k in range(FILAS - base):
    l.c[base + k] = [('bd-agua' if c == '-' else c + '-r') for c in l.c[base - 1 - k]]
for c in list(COLORES):
    COLORES[c + '-r'] = (mezcla(COLORES[c][0], AGUA, 0.5),) * 2
semilla = 7
def azar():
    global semilla
    semilla = (semilla * 1103515245 + 12345) % 2 ** 31
    return semilla / 2 ** 31
for k in range(2, FILAS - base, 2):
    x = azar() * 6
    while x < l.n / 4:
        largo = 1 + azar() * (2 + k / 6)
        l.rect('bd-onda' if azar() < 0.5 else 'bd-onda-o', x, x + largo, base + k, base + k + 1)
        x += largo + 4 + azar() * 14
usados = {c for fila in l.c for c in fila}
COLORES = {k: v for k, v in COLORES.items() if k in usados}

p = {'obra': 'Asamblea Nacional de Bangladesh', 'lugar': 'Daca', 'anio': '1982',
     'nota': ('Asamblea Nacional de Bangladesh (Louis Kahn, Daca, inaugurada en 1982), de frente y simétrica, con la luz '
              'desde la izquierda: los bloques de hormigón con sus aberturas en triángulo, el ojo redondo y las ranuras, '
              'los dos cilindros del medio y, atrás, la corona con sus arcos; las juntas de mármol blanco; abajo, el '
              'lago con el reflejo del edificio y sus ondas.'),
     'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}
p.update(placa='daca-fondo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='daca-fondo-marco')
# Fondo elegido por el usuario: blanco en claro, negro en oscuro; el marco, su color invertido.
COLORES.update({'daca-fondo': ('#f3f0e9', '#151413'), 'daca-fondo-marco': ('#0c0f16', '#eaebec')})
ruta = sys.argv[1]
escribir(ruta, 'mundo', '1980', p, sacar=('grosor', 'alinear'))
texto = con_colores(open(ruta).read(), COLORES, 'bd-|daca-fondo')
open(ruta, 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'], len(COLORES), 'colores')
