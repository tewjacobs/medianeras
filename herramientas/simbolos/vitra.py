# VitraHaus (Herzog & de Meuron, Weil am Rhein), en elevación.
# Medida en px sobre referencias/simbolos/contemporaneo/images (6).jpeg (764 × 401), la foto más de frente.
# Casitas de dos aguas apiladas: cuatro muestran el hastial vidriado (A arriba, B adelante, C volada a la
# derecha, D atrás a la izquierda) y las demás se ven de costado, con el faldón como una banda.
# Cada hastial es simétrico con la misma pendiente: borde de chapa oscuro, marco blanco, tres paños con un
# travesaño; arriba cortinas claras y abajo el interior con muebles. Muros de revoque antracita; abajo,
# vidriado y listones en la planta baja, el pasto con flores azules y dos arbolitos.
# Sombreado con luz arriba a la izquierda: cantos de la izquierda con luz, sombra debajo de lo que vuela y
# en la cara de adentro de los marcos.
# Uso: vitra.py <simbolos.json> (pone estilos."Arquitectura contemporánea").
import sys, math
from armar import Lienzo, guardar, con_sombras

S = 0.28                                   # unidades por px
X0, X1, Y0, Y1 = 0, 690, -14, 432
SUELO = 400
LARGO = round((X1 - X0) * S)
FILAS = round((Y1 - Y0) * S)
PENDIENTE = 0.66                           # alto del hastial / medio ancho, igual en todas las casas

def q(x): return round(x * 4) / 4
def ux(px): return q((px - X0) * S)
def fy(py): return round((py - Y0) * S)
def py(f): return Y0 + (f + 0.5) / S

def P(l, c, x0, x1, y0, y1):
    l.rect(c, ux(x0), ux(x1), fy(y0), max(fy(y0) + 1, fy(y1)))

def pentagono(l, c, cu, mu, cumbre, fondo):
    # Hastial lleno, simétrico desde cu (unidades): medio ancho mu (unidades), punta en la fila `cumbre`.
    for f in range(max(0, cumbre), fondo):
        w = min(mu, q((f + 0.5 - cumbre) / PENDIENTE))
        if w > 0: l.rect(c, cu - w, cu + w, f, f + 1)

def bordes(l, c, cu, mu, cumbre, hasta, lado, ancho=0.5):
    # La cara de un lado del hastial (lado -1 izquierda, 1 derecha), `ancho` unidades hacia adentro.
    for f in range(max(0, cumbre), hasta):
        w = min(mu, q((f + 0.5 - cumbre) / PENDIENTE))
        if w <= 0: continue
        if lado < 0: l.rect(c, cu - w, cu - w + ancho, f, f + 1)
        else: l.rect(c, cu + w - ancho, cu + w, f, f + 1)

# Interiores: lo que se ve abajo de cada hastial (posiciones en tercios del ancho de adentro).
def silla(l, x, f, c):
    # Silla de cáscara: el asiento con su respaldo y dos patas finas.
    l.rect(c, x, x + 0.5, f - 3, f - 1)
    l.rect(c, x, x + 2, f - 1, f)
    l.rect(c + '-o', x + 0.5, x + 2, f, f + 1)
    l.rect('vt-hierro', x + 0.25, x + 0.5, f + 1, f + 3)
    l.rect('vt-hierro', x + 1.5, x + 1.75, f + 1, f + 3)

def mesa(l, x, f, largo):
    l.rect('vt-mesa', x, x + largo, f, f + 1)
    l.rect('vt-mesa-o', x, x + largo, f + 1, f + 2)
    l.rect('vt-hierro', x + 0.5, x + 0.75, f + 2, f + 4)
    l.rect('vt-hierro', x + largo - 0.75, x + largo - 0.5, f + 2, f + 4)

def lampara(l, x, f0, f1, c='vt-lampara'):
    l.rect('vt-hierro', x, x + 0.25, f0, f1)
    l.rect(c, x - 1, x + 1.25, f1, f1 + 1)
    l.rect(c, x - 1.5, x + 1.75, f1 + 1, f1 + 2)
    l.rect('vt-luz', x - 0.75, x + 1, f1 + 2, f1 + 3)

def estante(l, a, b, f):
    # Estante en la pared del fondo con cosas de colores.
    l.rect('vt-mesa-o', a, b, f, f + 1)
    cosas = ('vt-amarillo', 'vt-azul', 'vt-rojo', 'vt-verde', 'vt-mesa')
    x, k = a + 0.5, 0
    while x + 1 < b:
        alto = 1 + (k % 2)
        l.rect(cosas[k % len(cosas)], x, x + 0.75, f - alto, f)
        x += 1.5 + (k % 3) * 0.5
        k += 1

def muebles_en(l, a, b, f_techo, f_piso, muebles):
    # Los muebles parados en la fila f_piso, repartidos en tercios de a..b; las lámparas cuelgan de f_techo.
    t = (b - a) / 3
    f1 = f_piso
    for m, *v in muebles:
        x = q(a + v[0] * t)
        if m == 'silla': silla(l, x, f1 - 3, v[1])
        elif m == 'mesa': mesa(l, x, f1 - 4, q(v[1] * t))
        elif m == 'lampara': lampara(l, x, f_techo, f_techo + v[1], *v[2:])
        elif m == 'estante': estante(l, x, q(a + v[1] * t), f1 - v[2])
        elif m == 'sillon':
            l.rect(v[1], x, x + 4, f1 - 3, f1 - 1)
            l.rect(v[1] + '-o', x, x + 4, f1 - 1, f1)
            l.rect(v[1], x - 0.5, x, f1 - 4, f1)
            l.rect(v[1] + '-o', x + 4, x + 4.5, f1 - 4, f1)
        elif m == 'planta':
            l.rect('vt-maceta', x, x + 1.5, f1 - 2, f1)
            for k, (d0, d1) in enumerate(((0.5, 1), (-0.5, 2), (0, 1.75), (-1, 2.25))):
                l.rect('vt-hoja' if k % 2 else 'vt-hoja-c', x + d0, x + d1, f1 - 3 - k, f1 - 2 - k)

def casa(l, cx, ancho, eave, fondo, travesano, muebles, hondo=40, volada=False, lado=1):
    # Hastial vidriado que se lee como una habitación: chapa, borde oscuro y marco blanco; adentro el
    # cielorraso a dos aguas (la mitad con luz y la otra en sombra), las paredes de los costados, la pared
    # del fondo con su punta, el piso de madera que viene hacia adelante, los muebles y las cortinas
    # recogidas a los lados. Tres paños con el travesaño y la losa del piso abajo.
    cu, mu = ux(cx), q(ancho * S / 2)
    alto = round(mu * PENDIENTE)                                 # filas del hastial
    f_alero, f_fondo, f_trav = fy(eave), fy(fondo), fy(travesano)
    cumbre = f_alero - alto
    # el cuerpo que se va hacia atrás, a la derecha: el faldón de la derecha (en sombra) con la cumbrera
    # derecha hasta el fondo, y el costado; si vuela, la panza en sombra.
    dx = q(hondo * S)
    # lado 1: se va hacia atrás por la derecha (faldón en sombra); -1: por la izquierda (faldón con luz)
    techo = 'vt-techo' if lado > 0 else 'vt-techo-l'
    for f in range(cumbre - 1, f_fondo + 1):
        w = min(mu + 0.75, q((f + 0.5 - cumbre + 1) / PENDIENTE))
        if f <= f_alero:
            a = cu + w if lado > 0 else cu - w - dx
            l.rect(techo, a, a + dx, f, f + 1)
            l.rect('vt-borde' if lado > 0 else 'vt-chapa-c', (a + dx - 0.25) if lado > 0 else a, (a + dx) if lado > 0 else a + 0.25, f, f + 1)
        else:
            a = cu + mu if lado > 0 else cu - mu - dx
            l.rect('vt-lado-m' if lado > 0 else 'vt-muro', a, a + dx, f, f + 1)
    a = cu if lado > 0 else cu - dx
    l.rect('vt-chapa-c', a, a + dx, cumbre - 1, cumbre)                         # la cumbrera, con luz
    a = cu + mu if lado > 0 else cu - mu - dx - 0.75
    l.rect('vt-borde', a, a + dx + 0.75, f_alero + 1, f_alero + 2)             # el alero
    l.sombra(a, a + dx + 0.75, f_alero + 2, f_alero + 3, SOMBREABLES)
    if volada: l.rect('vt-bajo', cu - mu - (dx if lado < 0 else 0), cu + mu + (dx if lado > 0 else 0), f_fondo, f_fondo + 2)
    pentagono(l, 'vt-chapa', cu, mu + 0.75, cumbre - 1, f_alero + 1)  # el canto del techo, que vuela
    bordes(l, 'vt-chapa-c', cu, mu + 0.75, cumbre - 1, f_alero + 1, -1, 0.75)
    pentagono(l, 'vt-borde', cu, mu, cumbre, f_fondo)
    pentagono(l, 'vt-perfil', cu, mu - 1, cumbre + 2, f_fondo - 1)
    vi = mu - 1.5                                                # el vidrio
    c0, f_vid = cumbre + 3, f_fondo - 1                          # punta y pie del vidrio
    # la pared del fondo: un hastial más chico, más abajo; el piso entre las dos
    mb = q(vi * 0.62)
    f_piso = f_vid - max(2, round((vi - mb) * 0.35))            # donde apoya la pared del fondo
    cb = f_piso - round((f_vid - c0) * 0.72)
    eb = cb + round(mb * PENDIENTE)
    for f in range(c0, f_vid):
        wo = min(vi, q((f + 0.5 - c0) / PENDIENTE))
        if wo <= 0: continue
        if f >= f_piso:                                           # el piso, de tablas
            l.rect('vt-piso' if (f - f_piso) % 2 else 'vt-piso-o', cu - wo, cu + wo, f, f + 1)
            continue
        wb = min(mb, q((f + 0.5 - cb) / PENDIENTE)) if f >= cb else 0
        techo = f < eb
        l.rect('vt-cielo-c' if techo else 'vt-lado-c', cu - wo, cu - wb, f, f + 1)   # izquierda
        l.rect('vt-cielo-o' if techo else 'vt-lado-o', cu + wb, cu + wo, f, f + 1)   # derecha, en sombra
        if wb > 0: l.rect('vt-pared', cu - wb, cu + wb, f, f + 1)
        else: l.rect('vt-cumbrera', cu - 0.25, cu + 0.25, f, f + 1)             # la viga de la cumbre
    l.rect('vt-pared-o', cu - mb, cu + mb, f_piso - 1, f_piso)                  # el zócalo del fondo
    muebles_en(l, cu - mb, cu + mb, eb - 1, f_piso + 1, muebles)
    # que se lea vidrio: arriba la cortina translúcida con sus pliegues, abajo el adentro apenas
    # insinuado detrás del reflejo, y dos franjas de brillo en diagonal.
    for f in range(c0, f_vid):
        wo = min(vi, q((f + 0.5 - c0) / PENDIENTE))
        for i in range(round((cu - wo) * 4), round((cu + wo) * 4)):
            x = i / 4 - cu
            if f < f_trav:
                p = round((x + 50) * 4) % 12
                l.c[f][i] = 'vt-velo-o' if p in (0, 1) else 'vt-velo'
                if f == f_trav - 1 and round((x + 50) * 4) % 4 < 2: l.c[f][i] = 'vt-velo-o'   # el volado
            else:
                d = (i / 4 + (f - f_trav) * 1.0) % 18
                l.c[f][i] = 'vt-reflejo' if d < 1 else l.c[f][i] + '-v'
    # la cara de adentro del marco, en sombra: a la derecha y debajo del canto de arriba
    bordes(l, 'vt-perfil-s', cu, mu - 1, cumbre + 2, f_alero + 1, 1, 0.5)
    l.rect('vt-perfil-s', cu + vi, cu + mu - 1, f_alero, f_vid)
    # parantes en tercios de punta a piso, el travesaño y el travesaño chico de la punta
    tt = q(2 * vi / 3)
    for x in (cu - vi + tt, cu + vi - tt):
        for f in range(c0, f_vid):
            w = q((f + 0.5 - c0) / PENDIENTE)
            if abs(x - cu) <= w: l.rect('vt-perfil', x - 0.25, x + 0.25, f, f + 1)
        l.rect('vt-perfil-s', x + 0.25, x + 0.5, f_trav + 1, f_vid)
    l.rect('vt-perfil', cu - vi, cu + vi, f_trav, f_trav + 1)
    fp = c0 + round(tt * PENDIENTE * 0.8)
    w = q((fp + 0.5 - c0) / PENDIENTE)
    l.rect('vt-perfil', cu - w, cu + w, fp, fp + 1)
    # la losa del piso, que asoma con su canto de luz
    l.rect('vt-borde', cu - mu, cu + mu, f_fondo - 1, f_fondo + 1)
    l.rect('vt-chapa-c', cu - mu, cu + mu, f_fondo - 1, f_fondo)
    return cu, mu, f_fondo + 1

def costado(l, x0, x1, techo, muro, fondo, claro=False, volada=False):
    # Casa vista de costado: el faldón es un plano liso del mismo material, con los extremos en diagonal
    # (las aristas que bajan de la cumbrera a la casa: la de la izquierda con luz), la cumbrera con un hilo
    # de luz, el canto del alero, la sombra debajo y el muro parejo. Si vuela, la panza en sombra.
    c = 'vt-muro-c' if claro else 'vt-muro'
    fa, fb = fy(techo), fy(muro)
    for f in range(fa, fb):
        t = (f + 0.5 - fa) / max(1, fb - fa)                    # 0 en la cumbrera, 1 en el alero
        e = q((1 - t) * (fb - fa) * 0.9)                         # cuánto se mete la arista arriba
        a, b = ux(x0) - 1 + e, ux(x1) + 1 - e
        l.rect('vt-techo', a, b, f, f + 1)
        l.rect('vt-chapa-c', a, a + 0.5, f, f + 1)              # arista de la izquierda, con luz
        l.rect('vt-borde', b - 0.5, b, f, f + 1)                # arista de la derecha
    e = q((fb - fa) * 0.9)
    l.rect('vt-chapa-c', ux(x0) - 1 + e, ux(x1) + 1 - e, fa, fa + 1)   # la cumbrera
    l.rect('vt-borde', ux(x0) - 1, ux(x1) + 1, fb - 1, fb)               # el canto del alero
    P(l, c, x0, x1, muro, fondo)
    l.sombra(ux(x0), ux(x1), fb, fb + 1, SOMBREABLES)               # sombra del alero
    l.sombra(ux(x1) - 0.75, ux(x1), fb, fy(fondo), SOMBREABLES)    # el canto de la derecha
    if volada: l.rect('vt-bajo', ux(x0), ux(x1), fy(fondo) - 1, fy(fondo))

def faldon(l, xa, ya, xb, yb, grueso):
    # Techo que se aleja en diagonal (de otra casa que va hacia atrás): banda inclinada con el borde de luz.
    fa, fb = fy(ya), fy(yb)
    for i in range(round(ux(xa) * 4), round(ux(xb) * 4)):
        x = i / 4
        t = (x - ux(xa)) / max(0.25, ux(xb) - ux(xa))
        f = round(fa + (fb - fa) * t)
        l.rect('vt-chapa-c', x, x + 0.25, f, f + 1)
        l.rect('vt-techo', x, x + 0.25, f + 1, f + round(grueso * S))
        l.rect('vt-borde', x, x + 0.25, f + round(grueso * S), f + round(grueso * S) + 1)

def tablones(l, x0, x1, y0, y1):
    # Revestimiento de tablones horizontales de madera: cada tablón de dos filas con su tono, el canto de
    # abajo en sombra y las juntas de punta trabadas.
    a, b = ux(x0), ux(x1)
    tonos = ('vt-liston', 'vt-liston-c', 'vt-liston-m', 'vt-liston', 'vt-liston-c')
    for k, f in enumerate(range(fy(y0), fy(y1), 2)):
        l.rect(tonos[k * 3 % 5], a, b, f, f + 1)
        l.rect('vt-liston-o', a, b, f + 1, f + 2)
        x = a + (k * 7 % 11) + 2
        while x < b:
            l.rect('vt-liston-o', x, x + 0.25, f, f + 1)
            x += 13
    l.sombra(a, a + 0.75, fy(y0), fy(y1), ('vt-liston', 'vt-liston-c', 'vt-liston-m', 'vt-liston-o'))

def arbol(l, x, alto, r):
    # Árbol más real: tronco que se afina con dos ramas que suben, la copa hecha de varias matas
    # irregulares (luz arriba a la izquierda, sombra abajo a la derecha), hojas sueltas en el borde y
    # huecos por donde se ve el fondo.
    cu, fc = ux(x), fy(alto)
    piso = fy(SUELO) + 1
    for f in range(fc, piso):
        w = 0.5 if f < fc + r else 0.75
        l.rect('vt-tronco', cu, cu + w, f, f + 1)
    for k in range(4):                                         # dos ramas
        l.rect('vt-tronco', cu - 0.5 - k * 0.5, cu - k * 0.5, fc + 6 - k, fc + 7 - k)
        l.rect('vt-tronco', cu + 0.75 + k * 0.5, cu + 1.25 + k * 0.5, fc + 5 - k, fc + 6 - k)
    matas = ((0, -0.2, 1.0), (-0.9, 0.25, 0.7), (0.95, 0.15, 0.75), (-0.35, -0.85, 0.6), (0.5, -0.7, 0.65),
             (0.1, 0.55, 0.6))
    for f in range(fc - 2 * r, fc + r + 2):
        for i in range(round((cu - 2.5 * r) * 4), round((cu + 2.5 * r) * 4)):
            xx = (i / 4 - cu) / (1.25 * r)
            yy = (f + 0.5 - fc) / r
            dentro = None
            for mx, my, mr in matas:
                d = ((xx - mx) ** 2 + (yy - my) ** 2) / (mr * mr)
                if d < 1 and (dentro is None or d < dentro[0]): dentro = (d, mx, my, mr)
            if dentro is None: continue
            d, mx, my, mr = dentro
            h = (i * 7 + f * 13) % 17
            if d > 0.8 and h < 6: continue                         # el borde, mordido
            if h == 3 and d < 0.6: continue                        # huequitos
            luz = (xx - mx) / mr + (yy - my) / mr                  # hacia abajo a la derecha, sombra
            c = 'vt-hoja-c' if luz < -0.5 else 'vt-hoja-o' if luz > 0.5 else 'vt-hoja'
            if h in (5, 11): c = 'vt-hoja-c' if luz < 0.2 else 'vt-hoja'
            if yy > 0.6 and h % 4 == 0: c = 'vt-hoja-oo'
            if 0 <= f < len(l.c) and 0 <= i < l.n: l.c[f][i] = c

SOMBREABLES = ('vt-muro', 'vt-muro-c', 'vt-chapa', 'vt-chapa-c', 'vt-cortina', 'vt-cortina-o', 'vt-pared',
               'vt-piso', 'vt-perfil', 'vt-vidrio', 'vt-vidrio-c', 'vt-liston', 'vt-liston-c', 'vt-liston-m', 'vt-liston-o', 'vt-muro-p', 'vt-muro-c-p', 'vt-muro-f', 'vt-junta', 'vt-techo', 'vt-techo-l', 'vt-lado-m', 'vt-ladrillo', 'vt-ladrillo-o', 'vt-puerta', 'vt-puerta-o', 'vt-mesa', 'vt-borde')

# Las casitas en 3D: cada una es un prisma con el perfil de dos aguas (la punta vidriada adelante y el
# cuerpo que se va hacia atrás), girado en planta. Se mira de frente y un poco desde arriba (CABEZA), en
# proyección paralela; cada cara toma su gris según cómo le da la luz (arriba a la izquierda y de frente),
# y un z-buffer resuelve qué tapa a qué. La cara de adelante lleva el ventanal: marco, parantes,
# travesaño, cortina arriba y el interior cálido abajo.
CABEZA = math.radians(0.5)
SP, CP = math.sin(CABEZA), math.cos(CABEZA)
LUZ = (-0.55, 0.7, -0.45)
GRISES = ('vt-g1', 'vt-g2', 'vt-g3', 'vt-g4', 'vt-g5', 'vt-g6')

def pantalla(p):
    # (x, y, z) del mundo → (x, alto) en la pantalla; z crece hacia el fondo.
    return p[0], p[1] * CP + p[2] * SP

def resta(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def punto(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cruz(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def unidad(a):
    n = math.sqrt(punto(a, a)); return (a[0] / n, a[1] / n, a[2] / n)

VISTA = (0, -SP, CP)                                   # hacia dónde mira el ojo

def adentro(px, py, poli):
    d = False
    j = len(poli) - 1
    for i in range(len(poli)):
        xi, yi = poli[i]; xj, yj = poli[j]
        if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi: d = not d
        j = i
    return d

def cara(l, zb, vs, pintar, ident=None):
    # Rasteriza una cara plana (vértices del mundo, en orden) con z-buffer; pintar(Q) da el color del
    # punto Q del mundo.
    n = unidad(cruz(resta(vs[1], vs[0]), resta(vs[2], vs[0])))
    nd = punto(n, VISTA)
    if abs(nd) < 1e-6: return
    poli = [pantalla(v) for v in vs]
    xs = [p[0] for p in poli]; ys = [p[1] for p in poli]
    i0, i1 = max(0, math.floor(min(xs) * 4)), min(l.n, math.ceil(max(xs) * 4))
    f0, f1 = max(0, math.floor((FILAS - max(ys)) * 4)), min(len(l.c) * 4, math.ceil((FILAS - min(ys)) * 4))
    for sf in range(f0, f1):                               # cuatro submuestras por fila, para suavizar
        sy = FILAS - (sf + 0.5) / 4
        for i in range(i0, i1):
            sx = (i + 0.5) / 4
            if not adentro(sx, sy, poli): continue
            o = (sx, sy * CP, sy * SP)                       # el punto de la pantalla, en el mundo
            t = punto(n, resta(vs[0], o)) / nd
            if t >= zb[sf][i]: continue
            Q = (o[0] + t * VISTA[0], o[1] + t * VISTA[1], o[2] + t * VISTA[2])
            zb[sf][i] = t
            SUBC[sf][i] = pintar(Q)
            SUBI[sf][i] = ident

def gris(n, techo=False):
    b = punto(n, unidad(LUZ))
    k = max(0, min(5, round((b + 0.6) / 1.5 * 5)))
    return GRISES[k] if not techo else GRISES[max(0, k - 1)]

def casita(l, zb, x, fila, z, gira, esc, largo, vidrio=True, interior=(), ancho=1.0, entrada=False, planta=0, puerta=False):
    # x, fila: dónde cae en la pantalla el pie del medio de la punta; z: qué tan al fondo; gira: grados
    # que mira hacia la derecha (en planta); esc: tamaño; largo: el cuerpo hacia atrás.
    W, H, R = 46 * esc * ancho, 25 * esc, 15.5 * esc * ancho
    if planta: H, R = planta, 0.01                        # caja de techo plano (la planta baja)
    y = ((FILAS - fila) - z * SP) / CP
    a = math.radians(gira)
    U = (math.cos(a), 0, math.sin(a))                         # a lo ancho de la punta
    Wd = (-math.sin(a), 0, math.cos(a))                       # hacia atrás
    P0 = (x, y, z)
    def L(u, v, w): return (P0[0] + u * U[0] + w * Wd[0], P0[1] + v, P0[2] + u * U[2] + w * Wd[2])
    perfil = [(-W / 2, 0), (W / 2, 0), (W / 2, H), (0, H + R), (-W / 2, H)]
    fr = [L(u, v, 0) for u, v in perfil]
    bk = [L(u, v, largo) for u, v in perfil]
    centro = L(0, H / 2, largo / 2)
    def orientada(vs):
        n = unidad(cruz(resta(vs[1], vs[0]), resta(vs[2], vs[0])))
        c = tuple(sum(v[k] for v in vs) / len(vs) for k in range(3))
        if punto(n, resta(c, centro)) < 0: vs = vs[::-1]; n = (-n[0], -n[1], -n[2])
        return vs, n
    caras = []
    for k in range(5):                                         # costados, faldones y piso
        j = (k + 1) % 5
        vs, n = orientada([fr[k], fr[j], bk[j], bk[k]])
        techo = k in (2, 3)
        caras.append((vs, (lambda c: lambda Q: c)(gris(n, techo))))
    vs, n = orientada(bk[:])
    caras.append((vs, (lambda c: lambda Q: c)(gris(n))))
    vs, n = orientada(fr[:])
    if vidrio:
        def ventanal(Q):
            d = resta(Q, P0)
            u, v = punto(d, U), d[1]
            m = min(v, W / 2 - abs(u), (H + R * (1 - abs(u) / (W / 2)) - v) * 0.85)
            if m < 0.9: return 'vt-borde'
            if m < 1.6: return 'vt-perfil'
            wi = W / 2 - 1.6
            if planta:                                         # vidriado de la planta baja con la escalera
                if abs(v - H * 0.7) < 0.4: return 'vt-perfil'
                k = (u + wi) / (2 * wi / 6)
                if abs(k - round(k)) * (2 * wi / 6) < 0.25: return 'vt-perfil'
                e = (u + wi) * 0.45 + 0.5                      # la escalera sube hacia la derecha
                if 0 < v - e + 1.2 < 1.2 and (u * 2) % 3 < 1.6: return 'vt-escalera'
                if 0 < v - e + 2.4 < 1.2: return 'vt-escalera-o'
                if v > H * 0.7: return 'vt-vidrio-c'
                return 'vt-vidrio' if v > H * 0.35 else 'vt-vidrio-o'
            if entrada:                                        # la entrada: luz cálida y puertas de vidrio altas
                vp = H * 0.78                                  # alto de las puertas
                if abs(v - vp) < 0.45: return 'vt-perfil'
                if v < vp:
                    paso = 2 * wi / 4
                    k = (u + wi) / paso
                    if abs(k - round(k)) * paso < 0.3: return 'vt-perfil'      # los marcos de las puertas
                    if abs(k - round(k) - 0.5) * paso < 0.15 and abs(v - vp * 0.45) < 1: return 'vt-hierro'  # manijas
                    if v < 0.8: return 'vt-piso'
                    return 'vt-luz-c' if v > vp * 0.6 else 'vt-calido-c'
                f = (v - vp) / (H + R - vp)
                return 'vt-luz' if f < 0.35 else 'vt-luz-c' if f < 0.75 else 'vt-calido-c'
            vt = H * 0.42
            if abs(abs(u) - wi / 3) < 0.3 or abs(v - vt) < 0.45: return 'vt-perfil'
            if v > vt:                                         # la persiana, lisa y translúcida
                return 'vt-velo-c' if v > H + R * 0.35 else 'vt-velo'
            if (u + v * 0.9) % 16 < 0.5: return 'vt-reflejo'
            if v < 2.2: return 'vt-piso-v' if v > 1.6 else 'vt-piso'
            for u0, u1, h, c in interior:                      # muebles y lámparas
                if u0 * W / 2 <= u <= u1 * W / 2 and v < 1.6 + h: return c
            return 'vt-calido-c' if v > vt - 2 else 'vt-calido'
        caras.append((vs, ventanal))
    elif puerta:                                               # punta ciega con una puerta de chapa
        base = gris(n)
        def ciega(Q):
            d = resta(Q, P0)
            u, v = punto(d, U), d[1]
            if W * 0.08 <= u <= W * 0.3 and v < H * 0.72:
                if u < W * 0.08 + 0.5 or u > W * 0.3 - 0.5 or v > H * 0.72 - 0.6: return 'vt-g1'
                return 'vt-g6' if abs(u - W * 0.26) < 0.3 and abs(v - H * 0.35) < 0.6 else 'vt-g3'
            return base
        caras.append((vs, ciega))
    else:
        caras.append((vs, (lambda c: lambda Q: c)(gris(n))))
    for k, (vs, pintar) in enumerate(caras):
        if punto(unidad(cruz(resta(vs[1], vs[0]), resta(vs[2], vs[0]))), VISTA) < 0:
            cara(l, zb, vs, pintar, (id(caras), k, pintar.__name__ == 'ventanal'))

IDS, SUBC, SUBI, MEZCLAS = [], [], [], {}

def mezcla(c1, c2, k):
    # Un color intermedio entre c1 (k cuartos) y c2: se registra y se calcula al guardar.
    if c1 == c2: return c1
    nombre = f'vt-m{len(MEZCLAS)}'
    for n, v in MEZCLAS.items():
        if v == (c1, c2, k): return n
    MEZCLAS[nombre] = (c1, c2, k)
    return nombre

def casitas(l):
    filas = len(l.c)
    zb = [[1e9] * l.n for _ in range(filas * 4)]
    SUBC[:] = [[None] * l.n for _ in range(filas * 4)]
    SUBI[:] = [[None] * l.n for _ in range(filas * 4)]
    IDS[:] = [[None] * l.n for _ in range(filas)]
    # Medidas sobre la foto de noche (contemporaneo/images (2).jpeg): x = (px − 80) · 0.42, fila = (py − 140) · 0.42 + 4.
    # La escondida: mira a la derecha (70°), detrás de la grande; asoma solo una tira de su vidrio y su
    # cuerpo largo sale flotando arriba a la izquierda.
    casita(l, zb, 128, 41, 70, 70, 0.52, 100, interior=((-0.5, 0.5, 2, 'vt-rojo'),))
    # La grande, arriba: de frente.
    casita(l, zb, 93, 53, 30, 0, 1.05, 60, interior=((-0.7, -0.45, 3, 'vt-rojo'), (0.4, 0.6, 2.5, 'vt-amarillo'),
                                                  (-0.2, 0.25, 1.2, 'vt-mesa')))
    # La larga de la izquierda: mira a la izquierda (−45°), punta chica, el cuerpo largo hacia la derecha.
    casita(l, zb, 16, 83, 60, -45, 0.6, 150, interior=((-0.3, 0.1, 2.5, 'vt-verde'),))
    # La entrada, entre la larga y la del medio: mira a la izquierda, apoyada en el piso, vidrio hasta abajo.
    casita(l, zb, 60, 115, 40, -55, 0.85, 22, entrada=True)
    # La del medio: mira a la izquierda (−35°); su faldón derecho cae grande hacia la derecha.
    casita(l, zb, 87, 101, 10, -35, 1.04, 45, interior=((-0.6, -0.4, 2.5, 'vt-verde'), (0.3, 0.5, 2.5, 'vt-rojo'),
                                                    (-0.25, 0.2, 1.2, 'vt-mesa')))
    # Abajo a la derecha, la casa baja: mira a la derecha, su faldón grande baja hacia la derecha y su
    # punta es una pared ciega con una puerta; el cuerpo se va hacia atrás por debajo de la del medio.
    casita(l, zb, 150, 116, 20, 45, 0.78, 70, vidrio=False, puerta=True, planta=19)
    # Debajo de la del medio, la planta baja vidriada, con el mismo giro.
    casita(l, zb, 87, 117, 10, -35, 1.04, 30, planta=15)
    # La volada de la derecha: mira a la derecha (50°), su cuerpo se va hacia atrás por la izquierda.
    casita(l, zb, 149, 74, 15, 50, 0.88, 127, interior=((-0.5, -0.1, 1.5, 'vt-rojo'), (0.4, 0.55, 3, 'vt-hoja')))
    # componer: cada celda toma su cara de la mayoría de las submuestras; en los bordes (submuestras de
    # caras distintas, o cara y fondo) un color intermedio según cuánto cubre cada una.
    MIXTA = set()
    for f in range(filas):
        for i in range(l.n):
            ms = [(SUBI[f * 4 + s][i], SUBC[f * 4 + s][i]) for s in range(4)]
            cuenta = {}
            for a, c in ms: cuenta[a] = cuenta.get(a, 0) + 1
            orden = sorted(cuenta.items(), key=lambda x: -x[1])
            a, k = orden[0]
            c = next(cc for aa, cc in ms[1:] + ms[:1] if aa == a)
            if a is None: c = l.c[f][i]
            IDS[f][i] = a
            if len(orden) > 1 and not (a and a[2]) and not (orden[1][0] and orden[1][0][2]):
                b = orden[1][0]
                c2 = next(cc for aa, cc in ms if aa == b) if b is not None else l.c[f][i]
                l.c[f][i] = mezcla(c, c2, k)
                MIXTA.add((f, i))
            else:
                l.c[f][i] = c
                cs = [cc for aa, cc in ms if aa == a]
                if a and a[2] and len(set(cs)) > 1 and 'vt-borde' in cs:   # el marco de la punta, suavizado
                    otra = next(cc for cc in cs if cc != 'vt-borde')
                    l.c[f][i] = mezcla('vt-borde', otra, cs.count('vt-borde'))
    # prolijidad: las astillas (una cara de menos de una unidad de ancho o de una fila de alto, entre la
    # misma cara a los dos lados) toman la cara vecina
    for f in range(len(l.c)):
        i = 0
        while i < l.n:
            j = i
            while j < l.n and IDS[f][j] == IDS[f][i]: j += 1
            if 0 < i and j < l.n and j - i < 4 and IDS[f][i - 1] == IDS[f][j] and IDS[f][i - 1] is not None:
                for k in range(i, j): IDS[f][k], l.c[f][k] = IDS[f][i - 1], l.c[f][i - 1]
            i = j
    for f in range(1, len(l.c) - 1):
        for i in range(l.n):
            a, b = IDS[f - 1][i], IDS[f + 1][i]
            if a is not None and a == b and IDS[f][i] != a: IDS[f][i], l.c[f][i] = a, l.c[f - 1][i]
    # aristas: donde se tocan dos caras de muro (no en los vidrios), una línea oscura fina; solo en los
    # bordes rectos (horizontales o verticales): en los inclinados queda el suavizado.
    def g(f, i): return IDS[f][i] if 0 <= f < filas and 0 <= i < l.n else 'x'
    for f in range(1, filas - 1):
        for i in range(1, l.n - 1):
            a = IDS[f][i]
            if a is None or a[2] or (f, i) in MIXTA: continue
            b = g(f - 1, i)
            if b is not None and b != a and not b[2] and g(f - 1, i - 1) == b and g(f - 1, i + 1) == b \
                    and g(f, i - 1) == a and g(f, i + 1) == a:
                l.c[f][i] = 'vt-g1'; continue
            b = g(f, i - 1)
            if b is not None and b != a and not b[2] and g(f - 1, i - 1) == b and g(f + 1, i - 1) == b \
                    and g(f - 1, i) == a and g(f + 1, i) == a:
                l.c[f][i] = 'vt-g1'

def version():
    l = Lienzo(LARGO, FILAS)

    # Atrás, abajo: muro en sombra para que no queden huecos entre la planta baja y las casitas.
    P(l, 'vt-muro-f', 22, 646, 230, SUELO)
    # la larga de la izquierda apoya en una base de tablones
    tablones(l, 22, 170, 332, SUELO)
    P(l, 'vt-borde', 22, 170, 329, 332)
    # más a la derecha, otra baja revestida de tablones
    P(l, 'vt-g2', 596, 690, 290, 300)
    P(l, 'vt-g5', 596, 690, 290, 292)
    tablones(l, 600, 690, 300, SUELO)
    casitas(l)

    # Abajo: el zócalo, el sendero de pedregullo y el pasto con lirios azules y dos arbolitos.
    P(l, 'vt-borde', 0, 690, SUELO - 2, SUELO)
    P(l, 'vt-pasto', 0, 690, SUELO, Y1)
    P(l, 'vt-sendero', 300, 470, SUELO + 6, SUELO + 14)
    for f in range(fy(SUELO) + 1, FILAS):
        x = (f % 3) * 0.75
        while x < LARGO:
            l.rect('vt-pasto-c', x, x + 0.5, f, f + 1)
            x += 2.25
    for k, x in enumerate(range(10, 680, 17)):
        if 300 <= x <= 470: continue
        f = fy(SUELO) + 1 + k % 4
        l.rect('vt-lirio', ux(x), ux(x) + 0.75, f, f + 1)
        l.rect('vt-hoja', ux(x) + 0.25, ux(x) + 0.5, f + 1, f + 3)
    arbol(l, 616, 300, 8)
    return {'nota': 'La VitraHaus de Herzog & de Meuron en Weil am Rhein: casitas de dos aguas apiladas y '
                    'voladas, de revoque antracita, con los hastiales vidriados y sus persianas.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

COLORES = {
    'vt-muro': ('#4a4746', '#4a4746'), 'vt-muro-c': ('#5a5755', '#5a5755'),
    'vt-muro-p': ('#555250', '#555250'), 'vt-muro-c-p': ('#646160', '#646160'),
    'vt-chapa': ('#2e2c2c', '#2e2c2c'), 'vt-chapa-c': ('#5f5c5a', '#5f5c5a'),
    'vt-borde': ('#262424', '#262424'), 'vt-perfil': ('#eef0ee', '#e2e4e2'),
    'vt-cortina': ('#dfe5e3', '#d3d9d7'), 'vt-cortina-o': ('#c9d1cf', '#bdc5c3'),
    'vt-techo': ('#363433', '#363433'), 'vt-bajo': ('#1f1d1d', '#1f1d1d'),
    'vt-escalera': ('#3a4a4a', '#334242'), 'vt-escalera-o': ('#263232', '#212b2b'),
    'vt-vidrio-o': ('#3f5555', '#364a4a'), 'vt-ladrillo': ('#a2553a', '#8d4a33'), 'vt-ladrillo-o': ('#7d3f2b', '#6c3726'),
    'vt-puerta': ('#4f4c4b', '#4f4c4b'), 'vt-puerta-o': ('#3a3837', '#3a3837'),
    'vt-techo-l': ('#4a4847', '#4a4847'),
    'vt-g1': ('#1f1e1e', '#1f1e1e'), 'vt-g2': ('#2a2828', '#2a2828'), 'vt-g3': ('#343231', '#343231'),
    'vt-g4': ('#403e3d', '#403e3d'), 'vt-g5': ('#4d4a49', '#4d4a49'), 'vt-g6': ('#5c5957', '#5c5957'),
    'vt-calido': ('#d9a66a', '#c9965c'), 'vt-calido-c': ('#f0c98c', '#e2b97c'), 'vt-piso-v': ('#8a6440', '#7c5838'),
    'vt-velo-c': ('#eef1ef', '#e0e3e1'), 'vt-liston-c': ('#9c7a58', '#8a6b4c'), 'vt-liston-m': ('#76583e', '#684d36'),
    'vt-hoja-oo': ('#2c4a1f', '#27411b'),
    'vt-luz-c': ('#ffd99a', '#f5cc88'),
    'vt-lado-m': ('#3c3a39', '#3c3a39'),
    'vt-muro-f': ('#3a3837', '#3a3837'), 'vt-junta': ('#3d3b3a', '#3d3b3a'),
    'vt-cielo-c': ('#f3efe6', '#e6e1d6'), 'vt-cielo-o': ('#cfc8bb', '#c0b9ac'), 'vt-cumbrera': ('#b5ad9f', '#a69e90'),
    'vt-lado-c': ('#e2d6c4', '#d3c7b5'), 'vt-lado-o': ('#bfb19c', '#b0a28d'),
    'vt-pared': ('#d8c6aa', '#c9b79b'), 'vt-pared-o': ('#9f8670', '#8f7864'),
    'vt-piso': ('#a8875e', '#987a55'), 'vt-piso-o': ('#7e6545', '#715a3d'),
    'vt-mesa': ('#f4f1ea', '#e6e3dc'), 'vt-mesa-o': ('#b9b2a4', '#a9a294'), 'vt-hierro': ('#2a2828', '#2a2828'),
    'vt-lampara': ('#2f2d2c', '#2f2d2c'), 'vt-lampara-r': ('#c8432e', '#c8432e'), 'vt-luz': ('#ffe7a6', '#ffe7a6'),
    'vt-rojo': ('#c8432e', '#c8432e'), 'vt-rojo-o': ('#932f20', '#932f20'),
    'vt-amarillo': ('#e3b437', '#e3b437'), 'vt-amarillo-o': ('#b08824', '#b08824'),
    'vt-azul': ('#3d5e8c', '#3d5e8c'), 'vt-azul-o': ('#2b4466', '#2b4466'),
    'vt-verde': ('#5d8a5a', '#5d8a5a'), 'vt-verde-o': ('#436641', '#436641'),
    'vt-maceta': ('#e8e4dc', '#d8d4cc'),
    'vt-vidrio': ('#4d6262', '#425555'), 'vt-vidrio-c': ('#8fa9a7', '#7c9694'),
    'vt-liston': ('#8a6a4c', '#7a5c40'), 'vt-liston-o': ('#4e3b2b', '#45342a'),
    'vt-pasto': ('#6f8c3e', '#58712f'), 'vt-pasto-c': ('#80a04a', '#678238'),
    'vt-sendero': ('#cfc6b4', '#a8a090'), 'vt-lirio': ('#6a6fc4', '#6a6fc4'),
    'vt-hoja': ('#4f7a34', '#456b2d'), 'vt-hoja-c': ('#6e9a45', '#5f873b'), 'vt-hoja-o': ('#3a5c27', '#324f22'),
    'vt-tronco': ('#5a4636', '#5a4636'),
    'contemporanea-fondo': ('#d8cdb6', '#2f2b25'), 'contemporanea-fondo-marco': ('#4a4746', '#e2d9c6'),
}
con_sombras(COLORES, SOMBREABLES)
def velar(h, k=0.35, v='#a7b4b4'):
    return '#' + ''.join(f'{round(int(h[i:i + 2], 16) * (1 - k) + int(v[i:i + 2], 16) * k):02x}' for i in (1, 3, 5))
COLORES.update({c + '-v': tuple(velar(x) for x in v) for c, v in list(COLORES.items()) if c.startswith('vt-')})
COLORES.update({'vt-velo': ('#dde3e1', '#cfd5d3'), 'vt-velo-o': ('#d6dbd9', '#c9cecc'),
                'vt-reflejo': ('#d3dcdd', '#c3cccd')})
COLORES['vt-perfil-s'] = ('#a9b0b0', '#9aa0a0')

if __name__ == '__main__':
    p = version()
    def hexmix(h1, h2, k):
        return '#' + ''.join(f'{round(int(h1[i:i + 2], 16) * k / 4 + int(h2[i:i + 2], 16) * (4 - k) / 4):02x}' for i in (1, 3, 5))
    for n, (c1, c2, k) in MEZCLAS.items():
        v1 = COLORES['contemporanea-fondo' if c1 == '-' else c1]
        v2 = COLORES['contemporanea-fondo' if c2 == '-' else c2]
        COLORES[n] = tuple(hexmix(v1[j], v2[j], k) for j in range(2))
    p.update(placa='contemporanea-fondo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
             marco='contemporanea-fondo-marco')
    guardar(sys.argv[1], 'estilos', 'Arquitectura contemporánea', p, COLORES, 'vt-|contemporanea-')
    print(len(p['lineas']), 'líneas, largo', p['largo'])
