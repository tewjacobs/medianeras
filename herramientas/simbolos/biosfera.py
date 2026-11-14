# Biosfera de Montreal (Buckminster Fuller, pabellón de Estados Unidos en la Expo 67), de frente desde el estanque.
# Medida en px sobre referencias/simbolos/neofuturismo/images (8).jpeg (447 × 447); las plataformas y lo de
# abajo, con biosfera-de-montreal-1536x1152.jpg. Esfera de centro (220, 225) y radio 180, cortada por el muro.
# La malla es transparente: atrás la cara lejana, más apagada; adelante la cercana, clara, con el aro del
# borde fino y parejo. Adentro, tenue, las plataformas escalonadas de la Expo: losas con panza de vigas,
# barandas de vidrio, la torre blanca, el núcleo de la derecha, columnas y la escalera de reticulado.
# Abajo: el cerco de enredadera con los equipos blancos arriba, el paseo con tres
# paneles de marco gris (más chicos los de atrás) y láminas color papel antiguo, el pabellón blanco; los árboles de la isla y
# el estanque quieto con el globo color papel antiguo flotando.
# Uso: biosfera.py <simbolos.json> (pone estilos."Neofuturismo").
import sys, math
from armar import Lienzo, guardar

S = 0.3
X0, X1, Y0, Y1 = 0, 447, 38, 384
CX, CY, R = 220, 225, 180
AGUA = 352                                 # borde del estanque
LARGO = round((X1 - X0) * S)
FILAS = round((Y1 - Y0) * S)
LINEAS = 12.5                              # líneas de la malla de cada lado del centro

def q(x): return round(x * 4) / 4
def ux(px): return q((px - X0) * S)
def fy(py): return round((py - Y0) * S)
def py(f): return Y0 + (f + 0.5) / S

def P(l, c, x0, x1, y0, y1):
    l.rect(c, ux(x0), ux(x1), fy(y0), max(fy(y0) + 1, fy(y1)))

def cuerda(y):
    # Medio ancho de la esfera a la altura y (px), 0 afuera.
    d = R * R - (y - CY) ** 2
    return math.sqrt(d) if d > 0 else 0

# Las tres familias de barras: una horizontal y dos a 60°. Cada familia son planos paralelos que cortan la
# esfera; de frente son rectas, más juntas hacia el borde (asin). Las horizontales que se juntan a menos de
# tres líneas se saltean, así la punta no se empasta. La cara de atrás es la misma malla corrida media barra.
DIAG = (math.cos(math.radians(30)), math.sin(math.radians(30)))

def malla(l, corrida, color, hasta_y, horizontales=True, aro=True):
    def t(x, y, k):
        u, v = (x - CX) / R, (y - CY) / R
        p = u * DIAG[0] * (1 if k == 1 else -1) + v * DIAG[1]
        return math.asin(max(-1, min(1, p))) / (math.pi / 2) * LINEAS + corrida
    filas_h = set()
    if horizontales:
        for lado in (1, -1):
            ultima = None
            for n in range(0, int(LINEAS) + 1):
                y = CY + lado * R * math.sin(n / LINEAS * math.pi / 2)
                if cuerda(y) < R * 0.4: break                    # cerca de la punta, sin horizontales
                f = fy(y)
                if ultima is None or abs(f - ultima) >= 3:
                    filas_h.add(f)
                    ultima = f
    d = 0.2 / S                                                  # medio ancho extra de las diagonales, en px
    for f in range(0, fy(hasta_y)):
        yc = py(f)
        h = cuerda(yc)
        if h == 0: continue
        h_arriba = cuerda(yc - 0.5 / S)
        for i in range(l.n):
            xa, xb = X0 + i * 0.25 / S, X0 + (i + 1) * 0.25 / S
            dx = abs((xa + xb) / 2 - CX)
            if dx > h: continue
            if not aro and dx > h - 1.2 / S: continue           # la cara de atrás llega hasta el aro
            if aro and dx > min(h_arriba, h - 0.8 / S):          # el aro: une el borde de esta fila con el de arriba
                l.c[f][i] = 'bi-acero'
                continue
            hay = f in filas_h
            for k in (1, 2):
                a, b = t(xa - d, yc, k), t(xb + d, yc, k)
                if math.floor(min(a, b)) != math.floor(max(a, b)): hay = True
            if hay: l.c[f][i] = color

class Azar:
    # Números de mentira pero siempre iguales, para que el dibujo no cambie entre corridas.
    def __init__(self, semilla): self.s = semilla
    def __call__(self):
        self.s = (self.s * 1103515245 + 12345) % 2 ** 31
        return self.s / 2 ** 31

def version():
    l = Lienzo(LARGO, FILAS)

    # La cara de atrás de la malla, vista a través.
    malla(l, 0.5, 'bi-acero-o', 345, horizontales=False, aro=False)

    # Adentro, tenue. El pabellón de abajo, con sus ventanales.
    P(l, 'bi-gris-c', 112, 252, 300, 344)
    P(l, 'bi-losa', 112, 252, 300, 303)
    for x in range(118, 250, 12):
        P(l, 'bi-vidrio', x, x + 8, 308, 338)
        P(l, 'bi-vidrio-c', x, x + 8, 308, 311)
    # La plataforma baja.
    P(l, 'bi-losa', 100, 252, 288, 293)
    P(l, 'bi-bajo', 104, 248, 293, 299)
    # Columnas blancas y el núcleo de la derecha.
    for x in (248, 266, 322, 340):
        P(l, 'bi-blanco', x, x + 3.5, 240, 344)
        P(l, 'bi-gris-c', x + 2.5, x + 3.5, 240, 344)
    P(l, 'bi-blanco', 304, 318, 228, 344)
    P(l, 'bi-gris-c', 314, 318, 228, 344)
    for y in range(238, 330, 14):
        P(l, 'bi-vidrio', 306, 313, y, y + 4)
    # La escalera de reticulado: dos montantes y las cruces de cada tramo.
    for f in range(fy(262), fy(344)):
        k = f - fy(262)
        l.rect('bi-gris', ux(276), ux(277.5), f, f + 1)
        l.rect('bi-gris', ux(294.5), ux(296), f, f + 1)
        if k % 6 == 0: l.rect('bi-gris', ux(276), ux(296), f, f + 1)
        x = (k % 6) * 0.9
        l.rect('bi-gris', ux(276) + x, ux(276) + x + 0.5, f, f + 1)
        l.rect('bi-gris', ux(296) - x - 0.5, ux(296) - x, f, f + 1)
    # Las tres plataformas escalonadas: losa clara, baranda de vidrio con su pasamanos, y la panza de
    # vigas que se angosta abajo.
    for x0, x1, y0, panza, vuelo in ((100, 205, 250, 12, 10), (150, 334, 238, 20, 24), (258, 358, 222, 15, 28)):
        P(l, 'bi-vidrio-c', x0 + 2, x1 - 2, y0 - 6, y0)
        P(l, 'bi-gris', x0 + 2, x1 - 2, y0 - 7, y0 - 6)
        P(l, 'bi-losa', x0, x1, y0, y0 + 4)
        for f in range(fy(y0 + 4), fy(y0 + 4 + panza)):
            t = (py(f) - y0 - 4) / panza
            a, b = ux(x0 + vuelo * t), ux(x1 - vuelo * t)
            l.rect('bi-bajo', a, b, f, f + 1)
            x = a + 1.5
            while x < b - 1:                                     # las vigas, cada 1.5
                l.rect('bi-bajo-c', x, x + 0.25, f, f + 1)
                x += 1.5
            l.rect('bi-bajo-o', a, a + 0.5, f, f + 1)
    # El cuarto vidriado de arriba a la derecha, con su techo curvo blanco.
    P(l, 'bi-vidrio', 270, 322, 208, 222)
    P(l, 'bi-vidrio-c', 270, 322, 208, 211)
    for x in range(274, 322, 8):
        P(l, 'bi-blanco', x, x + 1.5, 208, 222)
    for f in range(fy(198), fy(209)):
        t = (py(f) - 198) / 11
        l.rect('bi-blanco', ux(296 - 27 * math.sqrt(max(0, t))), ux(296 + 27 * math.sqrt(max(0, t))), f, f + 1)
    # La torre de los ascensores, blanca con su sombra y fajas de ventanas, y la bandera.
    P(l, 'bi-blanco', 198, 226, 204, 344)
    P(l, 'bi-gris-c', 219, 226, 204, 344)
    for y in range(214, 330, 14):
        P(l, 'bi-vidrio', 202, 216, y, y + 4)
    P(l, 'bi-gris', 196, 228, 200, 205)
    P(l, 'bi-gris', 211, 212.5, 172, 200)
    P(l, 'bi-rojo', 212.5, 222, 172, 180)
    P(l, 'bi-blanco', 215.5, 219, 173, 179)

    # La cara de adelante de la malla.
    malla(l, 0, 'bi-acero', 345)

    # Árboles: tronco y ramas, y una copa hecha de muchos manojos de hojas, cada uno con luz arriba a la
    # izquierda y sombra abajo a la derecha; los de abajo y la derecha de la copa, más oscuros.
    def arbol(cx, base, alto, ancho, semilla, ramas=True):
        az = Azar(semilla)
        top = base - alto
        P(l, 'bi-tronco', cx - ancho * 0.05, cx + ancho * 0.05, top + alto * 0.45, base)
        if ramas:
            for dx, y0 in ((-0.3, 0.5), (0.28, 0.45), (-0.15, 0.3), (0.2, 0.3)):
                for f in range(fy(top + alto * y0), fy(top + alto * 0.65)):
                    t = (py(f) - top - alto * y0) / (alto * (0.65 - y0))
                    x = cx + dx * ancho * (1 - t)
                    l.rect('bi-tronco', ux(x) - 0.25, ux(x) + 0.25, f, f + 1)
        ccx, ccy, rx, ry = cx, top + alto * 0.36, ancho / 2, alto * 0.36
        manojos = []
        for _ in range(70):
            a, r = az() * 2 * math.pi, math.sqrt(az())
            x, y = ccx + math.cos(a) * r * rx * 0.85, ccy + math.sin(a) * r * ry * 0.85
            manojos.append((y, x, 5 + az() * 6))
        for y, x, r in sorted(manojos):
            pos = ((x - ccx) / rx + (y - ccy) / ry) / 2            # -1 arriba a la izquierda, 1 abajo a la derecha
            base_c = 'bi-hoja-o' if pos > 0.35 else 'bi-hoja'
            for f in range(fy(y - r), fy(y + r) + 1):
                d = r * r - (py(f) - y) ** 2
                if d <= 0: continue
                hh = math.sqrt(d)
                for i in range(round(ux(x - hh) * 4), round(ux(x + hh) * 4)):
                    if not 0 <= i < l.n: continue
                    xx = X0 + (i + 0.5) * 0.25 / S
                    luz = ((xx - x) + (py(f) - y)) / r
                    c = 'bi-hoja-c' if luz < -0.6 and pos < 0.5 else 'bi-hoja-oo' if luz > 0.7 else base_c
                    l.c[f][i] = c
    arbol(52, AGUA, 168, 118, 7)
    arbol(104, AGUA, 92, 52, 3, ramas=False)
    arbol(430, 330, 62, 38, 5, ramas=False)

    # El cerco de enredadera, alto: muchos manojos de hojas con luz arriba a la izquierda, más oscuro abajo,
    # el borde de arriba hecho de los mismos manojos; los equipos blancos asoman arriba.
    az = Azar(11)
    HX0, HX1, HY0, HY1 = 262, 394, 304, AGUA - 2
    def adentro(x, y):
        # Un rectángulo de esquinas redondeadas (radio 12): el contorno del cerco.
        cx, cy = min(max(x, HX0 + 12), HX1 - 12), max(y, HY0 + 12)
        return HX0 <= x <= HX1 and y >= HY0 and math.hypot(x - cx, y - cy) <= 12
    P(l, 'bi-hoja-o', HX0 + 5, HX1 - 5, HY0 + 8, HY1)              # el fondo, metido, así el borde lo hacen las hojas
    manojos = []
    while len(manojos) < 230:
        x, y = HX0 + az() * (HX1 - HX0), HY0 + az() * (HY1 - HY0)
        if adentro(x, y): manojos.append((y, x, 2.5 + az() * 3))
    for y, x, r in sorted(manojos):
        abajo = (y - HY0) / (HY1 - HY0)
        for f in range(fy(y - r), fy(y + r) + 1):
            d = r * r - (py(f) - y) ** 2
            if d <= 0 or py(f) >= AGUA - 2: continue
            h = math.sqrt(d)
            for i in range(round(ux(x - h) * 4), round(ux(x + h) * 4)):
                xx = X0 + (i + 0.5) * 0.25 / S
                luz = ((xx - x) + (py(f) - y)) / r
                c = 'bi-hoja-c' if luz < -0.7 and abajo < 0.6 else 'bi-hoja-oo' if luz > 0.6 or abajo > 0.85 else 'bi-hoja' if abajo < 0.5 else 'bi-hoja-o'
                l.c[f][i] = c
    # El equipo de aire arriba del cerco: caja blanca con rejillas y el costado en sombra.
    P(l, 'bi-blanco', 296, 322, 294, 305)
    P(l, 'bi-gris-c', 318, 322, 294, 305)
    for y in range(296, 304, 2):
        P(l, 'bi-gris-c', 298, 316, y, y + 0.8)
    # El pabellón blanco de la derecha: pretil con su remate, la sombra que hace, paños de la fachada,
    # el ventanal con marco oscuro, parteluces y reflejos, el zócalo y su equipo en el techo.
    P(l, 'bi-blanco', 403, 425, 298, 309)                          # el equipo del techo
    P(l, 'bi-gris-c', 421, 425, 298, 309)
    for y in range(300, 308, 2):
        P(l, 'bi-gris-c', 405, 419, y, y + 0.8)
    P(l, 'bi-blanco', 394, X1, 309, 344)
    P(l, 'bi-blanco-c', 392, X1, 307, 310)                         # el remate del pretil
    P(l, 'bi-gris-c', 394, X1, 310, 312)                           # su sombra
    for x in (420,):
        P(l, 'bi-blanco-s', x, x + 0.8, 312, 340)                  # junta de los paños
    P(l, 'bi-blanco-s', 394, 397, 312, 344)                        # la esquina, en sombra
    P(l, 'bi-gris', 402, 442, 320, 338)                            # el ventanal
    for k in range(4):
        a = 403.5 + k * 9.5
        P(l, 'bi-vidrio', a, a + 8, 321.5, 336.5)
        P(l, 'bi-vidrio-c', a, a + 8, 321.5, 324)
        for f in range(fy(324), fy(336.5)):                         # reflejo en diagonal
            x = ux(a) + (f - fy(324)) * 0.5 + 0.5
            if x + 0.5 <= ux(a + 8): l.rect('bi-vidrio-c', x, x + 0.5, f, f + 1)
    P(l, 'bi-blanco-c', 401, 443, 338, 339.5)                      # el antepecho
    P(l, 'bi-gris-c', 394, X1, 340, 344)                           # el zócalo

    # El paseo del borde del estanque y, a lo largo, la fila de paneles de la exposición, separados como en
    # un pasillo: marco gris alto, y adentro una lámina color papel antiguo con su imagen sepia y el epígrafe.
    P(l, 'bi-paseo', X0, X1, 344, AGUA - 2)
    P(l, 'bi-paseo-o', X0, X1, 344, 345.5)
    for x in range(18, 447, 20):
        P(l, 'bi-paseo-o', x, x + 1, 345.5, AGUA - 2)              # juntas de las losas
    # Tres paneles, más chicos los de atrás para que se lea el pasillo. Marco biselado (luz arriba y a la
    # izquierda, sombra abajo y a la derecha), el costado en sombra, la lámina color papel antiguo con una foto
    # vieja (cielo claro, horizonte, un edificio oscuro) y su epígrafe, las patas con sus pies y la sombra.
    for x0, alto, base in ((280, 20, 347), (322, 25, 348.5), (368, 31, 350)):
        ancho, y0 = alto * 0.55, base - 5 - alto
        x1, y1 = x0 + ancho, base - 5
        P(l, 'bi-sombra', x0 + 3, x1 + 7, base - 1.5, base)                # sombra en el piso
        P(l, 'bi-marco-o', x1, x1 + 2.5, y0 + 1.5, y1)                     # el costado
        P(l, 'bi-marco', x0, x1, y0, y1)
        P(l, 'bi-marco-c', x0, x0 + 1.2, y0, y1)
        P(l, 'bi-marco-c', x0, x1, y0, y0 + 1.2)
        P(l, 'bi-marco-o', x0, x1, y1 - 1.2, y1)
        m = alto * 0.12
        a, b, c0, c1 = x0 + m, x1 - m, y0 + m, y1 - m
        P(l, 'bi-marco-o', a - 0.8, b + 0.8, c0 - 0.8, c0)                 # la sombra del marco sobre la lámina
        P(l, 'bi-papel', a, b, c0, c1)
        fh = c0 + (c1 - c0) * 0.62                                          # la foto, arriba
        P(l, 'bi-papel-l', a + 1, b - 1, c0 + 1, fh)
        P(l, 'bi-papel-o', a + 1, b - 1, c0 + (fh - c0) * 0.55, fh)        # la tierra
        P(l, 'bi-papel-oo', a + (b - a) * 0.35, a + (b - a) * 0.6, c0 + (fh - c0) * 0.25, fh)   # el edificio
        P(l, 'bi-papel-o', a + 1, b - 1.5, fh + 2, fh + 3)                  # el epígrafe
        P(l, 'bi-papel-l', a + 1, b - 3, fh + 4.5, fh + 5.5)
        for px in (x0 + 1.5, x1 - 3.5):                                     # las patas y sus pies
            P(l, 'bi-marco-o', px, px + 2, y1, base)
            P(l, 'bi-marco-o', px - 1.5, px + 3.5, base - 1, base)
    P(l, 'bi-borde', X0, X1, AGUA - 2, AGUA + 4)                  # el borde de piedra del estanque

    # El estanque, quieto, con unas pocas líneas de luz.
    P(l, 'bi-agua', X0, X1, AGUA + 4, Y1)
    for y, x0, x1 in ((364, 150, 300), (375, 40, 180), (375, 260, 420)):
        P(l, 'bi-agua-c', x0, x1, y, y + 2.5)
    # El globo flotando: un mundo color papel antiguo con sombreado suave de esfera (luz arriba a la izquierda),
    # América, Europa y África en sepia, el ecuador y un meridiano finos, un brillo; su sombra en el agua.
    GX, GY, GR = 228, 344, 17
    TIERRA = ((-75, 40, 28, 16), (-62, -12, 13, 26), (18, 48, 16, 10), (20, 2, 18, 24))   # lon, lat, radios
    P(l, 'bi-agua-o', GX - 14, GX + 18, GY + 15, GY + 19)
    for f in range(fy(GY - GR), fy(GY + GR) + 1):
        y = py(f)
        if GR * GR - (y - GY) ** 2 <= 0: continue
        h = math.sqrt(GR * GR - (y - GY) ** 2)
        for i in range(round(ux(GX - h) * 4), round(ux(GX + h) * 4)):
            x = X0 + (i + 0.5) * 0.25 / S
            u, v = (x - GX) / GR, (y - GY) / GR
            z = math.sqrt(max(0, 1 - u * u - v * v))
            lon = math.degrees(math.atan2(u, z)) - 25                     # mira al Atlántico
            lat = -math.degrees(math.asin(max(-1, min(1, v))))
            luz = (-u * 0.55 - v * 0.6 + z * 0.6)                         # luz arriba a la izquierda
            tierra = any(((lon - a) / ra) ** 2 + ((lat - b) / rb) ** 2 < 1 for a, b, ra, rb in TIERRA)
            if tierra: c = 'bi-papel-o' if luz > 0.45 else 'bi-papel-oo'
            else: c = 'bi-papel-c' if luz > 0.85 else 'bi-papel' if luz > 0.45 else 'bi-papel-s' if luz > 0.1 else 'bi-papel-l'
            if not tierra and (abs(lat) < 2.5 or abs(lon + 25) < 2.5): c = 'bi-papel-l' if luz > 0.3 else 'bi-papel-o'
            if z < 0.25: c = 'bi-papel-oo' if tierra else 'bi-papel-o'      # el borde, que se oscurece
            l.c[f][i] = c
    for f in range(fy(GY - 9.5), fy(GY - 4.5)):                          # el brillo
        d = 6.25 - (py(f) - GY + 7) ** 2
        if d > 0: P(l, 'bi-papel-c', GX - 6 - math.sqrt(d), GX - 6 + math.sqrt(d), py(f), py(f) + 0.1)

    return {'nota': 'La Biosfera de Montreal (Buckminster Fuller, Expo 67) desde el estanque: la esfera '
                    'geodésica transparente, con su cara de atrás vista a través, las plataformas escalonadas '
                    'de adentro, los árboles de la isla, los paneles y el globo color papel '
                    'antiguo flotando en el estanque.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

COLORES = {
    'bi-acero': ('#f6f7f6', '#e9ecec'), 'bi-acero-o': ('#aab5a6', '#5d6862'),
    'bi-blanco': ('#e3e2dc', '#d4d3cd'), 'bi-gris': ('#7d8285', '#7d8285'), 'bi-gris-c': ('#b9bcbc', '#a9acac'),
    'bi-losa': ('#d2d2ce', '#c2c2be'), 'bi-bajo': ('#5d6368', '#4f555a'), 'bi-bajo-c': ('#73797e', '#656b70'),
    'bi-bajo-o': ('#4a4f53', '#3f4447'),
    'bi-vidrio': ('#5a6b76', '#4d5e69'), 'bi-vidrio-c': ('#a9bcc4', '#8fa2aa'),
    'bi-rojo': ('#c8312c', '#c8312c'), 'bi-hierro': ('#3a3c3e', '#3a3c3e'),
    'bi-hoja': ('#3f6a33', '#3a6030'), 'bi-hoja-o': ('#2f5228', '#2a4924'), 'bi-hoja-oo': ('#223d1d', '#1e361a'),
    'bi-hoja-c': ('#5f8a42', '#55793c'),
    'bi-tronco': ('#4a3b2e', '#4a3b2e'),
    'bi-blanco-c': ('#f1f0eb', '#e2e1dc'), 'bi-blanco-s': ('#cfcec8', '#c0bfb9'),
    'bi-marco': ('#8a8c8c', '#7c7e7e'), 'bi-marco-c': ('#a9abab', '#9a9c9c'), 'bi-sombra': ('#a8a191', '#7f796d'), 'bi-marco-o': ('#6a6c6d', '#5e6061'),
    'bi-papel': ('#e9dfc4', '#ddd2b6'), 'bi-papel-o': ('#b9a47c', '#ad9870'), 'bi-papel-oo': ('#8c7552', '#806a48'),
    'bi-papel-l': ('#c9b892', '#bdac86'), 'bi-papel-s': ('#cbbd9c', '#bfb190'), 'bi-papel-c': ('#f4ecd8', '#e8e0cc'),
    'bi-paseo': ('#cfc8b8', '#a39d90'), 'bi-paseo-o': ('#b3ac9c', '#8a8478'),
    'bi-borde': ('#c7c2b6', '#9f9a8f'),
    'bi-agua': ('#3f5357', '#26343a'), 'bi-agua-o': ('#2c3d42', '#1b272c'), 'bi-agua-c': ('#90a4a6', '#64787c'),
    'neo-pizarra': ('#5f6f7d', '#1f262d'), 'neo-pizarra-marco': ('#f3ead9', '#e0d9d2'),
}

if __name__ == '__main__':
    p = version()
    p.update(placa='neo-pizarra', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
             marco='neo-pizarra-marco')
    guardar(sys.argv[1], 'estilos', 'Neofuturismo', p, COLORES, 'bi-|neo-')
    print(len(p['lineas']), 'líneas, largo', p['largo'])
