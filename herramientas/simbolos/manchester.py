# Catedral de Manchester, el lado sur, en elevación.
# Medida en px sobre referencias/simbolos/gotico perpendicular/3_IMG_6851_3__…jpg (1200 × 865).
# A la izquierda la torre oeste: contrafuertes en las esquinas con retallos, parapeto calado con almenas y
# pináculos (simétricos desde el eje), campanario de dos luces con tablillas bajo un arco conopial con
# tracería ciega, el reloj y el ventanal bajo. Después el pórtico sur: puerta en arco de varias roscas,
# friso tallado, dos ventanitas y su parapeto con pináculos. La nave en seis tramos iguales: ventanales
# perpendiculares (parantes rectos hasta el arco, travesaño con arquitos), contrafuertes con pináculos,
# el triforio y el parapeto calado con almenas; la torrecilla de la escalera. Sillería de arenisca con
# hollín en los huecos. Abajo, las losas mojadas del atrio, dos pedestales y el pasto.
# Sombreado con luz arriba a la izquierda: caras de la izquierda con luz, sombra a la derecha de lo que
# sobresale, debajo de cornisas y adentro de los huecos (el lado de la izquierda y arriba).
# Uso: manchester.py <simbolos.json> (pone estilos."Gótico perpendicular").
import sys, math
from armar import Lienzo, guardar, con_sombras

S = 0.24                                   # unidades por px
X0, X1, Y0, Y1 = 50, 935, 58, 760
SUELO = 712
LARGO = round((X1 - X0) * S)
FILAS = round((Y1 - Y0) * S)
EJE_T = 162                                # eje de la torre
EJE_P = 314                                # eje del pórtico
NAVE = (400, 920)                          # de la torre... al final de la nave
TRAMOS = 6

def q(x): return round(x * 4) / 4
def ux(px): return q((px - X0) * S)
def fy(py): return round((py - Y0) * S)

def P(l, c, x0, x1, y0, y1):
    l.rect(c, ux(x0), ux(x1), fy(y0), max(fy(y0) + 1, fy(y1)))

def U(l, c, cu, wu, f0, f1):
    # Rectángulo centrado en cu (unidades) de ancho wu: así lo simétrico queda igual a los dos lados.
    w = q(wu / 2)
    l.rect(c, cu - w, cu + w, f0, f1)

def sillar(l, a, b, f0, f1, c='mc-piedra'):
    # Sillería prolija: hiladas de tres filas (dos de piedra y la junta) y juntas verticales cada 4,
    # trabadas media pieza por hilada.
    l.rect(c, a, b, f0, f1)
    for f in range(f0, f1):
        k = f - f0
        if k % 3 == 2: l.rect('mc-junta', a, b, f, f + 1)
        else:
            x = a + (2 if (k // 3) % 2 else 0)
            while x < b:
                l.rect('mc-junta', x, x + 0.25, f, f + 1)
                x += 4

def arco_ancho(w, h, H):
    # Medio ancho de un arco apuntado de luz w y flecha H, a la altura h sobre el arranque: arranca
    # vertical y llega a la punta con ángulo (se lee en punta aun en pocas filas).
    if h >= H: return 0
    return w / 2 * (1 - (h / H) ** 2.2)

def hueco_apuntado(l, c, cu, w, f_arr, flecha, f_fondo):
    # Rellena con c un hueco apuntado centrado en cu (unidades): arranque en la fila f_arr.
    for f in range(f_arr - flecha, f_fondo):
        h = f_arr - f - 0.5
        hw = w / 2 if h <= 0 else arco_ancho(w, h, flecha)
        hw = q(hw)
        if hw > 0: l.rect(c, cu - hw, cu + hw, f, f + 1)

def arco_linea(l, c, cu, w, f_arr, flecha, grueso=0.25):
    # Solo el contorno de un arco apuntado (los dos bordes), para la tracería.
    for f in range(f_arr - flecha, f_arr + 1):
        h = f_arr - f - 0.5
        hw = q(w / 2 if h <= 0 else arco_ancho(w, h, flecha))
        if hw <= 0: continue
        l.rect(c, cu - hw, cu - hw + grueso, f, f + 1)
        l.rect(c, cu + hw - grueso, cu + hw, f, f + 1)
    l.rect(c, cu - 0.125, cu + 0.125, f_arr - flecha, f_arr - flecha + 1)

def ventanal(l, cx, ancho, arranque, fondo, luces=5, flecha=None):
    # Ventanal perpendicular: goterón fino y moldura con luz, derrame (izquierda en sombra, derecha con
    # luz), vidrio emplomado gris claro, parantes rectos hasta el arco y en la cabeza la tracería: arquitos
    # sobre cada luz, dos arcos que agrupan las luces de los costados y paneles rectos hasta la punta.
    cu, w = ux(cx), q(ancho * S)
    fa, ff = fy(arranque), fy(fondo)
    fl = flecha if flecha is not None else round(w * 0.7)
    hueco_apuntado(l, 'mc-derrame', cu, w, fa, fl, ff)                   # derrame
    arco_linea(l, 'mc-piedra-c', cu, w + 1, fa, fl + 1, 0.5)             # moldura con luz, siguiendo el arco
    arco_linea(l, 'mc-hollin', cu, w + 1.5, fa, fl + 2, 0.25)            # goterón fino
    for s in (-1, 1): l.rect('mc-piedra-c' if s < 0 else 'mc-piedra', cu + s * (w / 2 + 0.25) - 0.25, cu + s * (w / 2 + 0.25) + 0.25, fa, ff)
    l.rect('mc-piedra-c', cu + w / 2 - 0.75, cu + w / 2 - 0.25, fa - 1, ff)
    vi = w - 1.5
    c0 = cu - 0.25
    hueco_apuntado(l, 'mc-vidrio', c0, vi, fa, fl - 2, ff - 1)
    for f in range(fa - fl, ff - 1):                                     # emplomado: rombitos de luz
        for i in range(round((c0 - vi / 2) * 4), round((c0 + vi / 2) * 4)):
            if l.c[f][i] == 'mc-vidrio' and (i + 2 * f) % 6 == 0: l.c[f][i] = 'mc-vidrio-c'
    paso = vi / luces
    xs = [q(c0 - vi / 2 + k * paso) for k in range(luces + 1)]
    for x in xs[1:-1]:                                                   # parantes hasta el arco
        for f in range(fa - fl, ff - 1):
            if l.c[f][round(x * 4)] in ('mc-vidrio', 'mc-vidrio-c'): l.rect('mc-traceria', x - 0.125, x + 0.125, f, f + 1)
    ft = fa + round((ff - fa) * 0.45)                                    # travesaño con arquitos
    l.rect('mc-traceria', c0 - vi / 2, c0 + vi / 2, ft, ft + 1)
    for a, b in zip(xs, xs[1:]):
        arco_linea(l, 'mc-traceria', (a + b) / 2, b - a, ft + 2, 2)
        arco_linea(l, 'mc-traceria', (a + b) / 2, b - a, fa + 1, 2)      # y sobre cada luz, en el arranque
    if luces >= 4:                                                       # dos arcos que agrupan los costados
        for a, b in ((xs[0], xs[2]), (xs[-3], xs[-1])):
            arco_linea(l, 'mc-traceria', (a + b) / 2, b - a, fa - 2, round((b - a) * 0.75))
    # alféizar con luz arriba y sombra abajo
    l.rect('mc-piedra-c', cu - w / 2 - 0.5, cu + w / 2 + 0.5, ff, ff + 1)
    l.rect('mc-sombra', cu - w / 2 - 0.5, cu + w / 2 + 0.5, ff + 1, ff + 2)

def remate_nave(l, a, b, tramo):
    # El remate de la nave en tres pisos, como en la foto: almenas con ranuras arriba; el claristorio con
    # tres ventanitas en arco por tramo; el parapeto del pasillo con tableros calados sueltos (un
    # cuadrifolio en cada uno) entre postes; la cornisa con su sombra.
    A, B = ux(a), ux(b)
    f0 = fy(448)
    # almenas sobre la albardilla
    l.rect('mc-piedra', A, B, f0 + 3, f0 + 5)
    l.rect('mc-piedra-c', A, B, f0 + 3, f0 + 4)
    x = A
    while x < B:
        e = min(B, x + 3.5)
        l.rect('mc-piedra', x, e, f0, f0 + 3)
        l.rect('mc-piedra-c', x, e, f0, f0 + 1)
        l.rect('mc-piedra-o', e - 0.25, e, f0 + 1, f0 + 3)
        m = q((x + e) / 2)
        l.rect('-', m - 0.5, m - 0.25, f0 + 1, f0 + 3)
        l.rect('-', m + 0.25, m + 0.5, f0 + 1, f0 + 3)
        x += 5.5
    # el claristorio
    l.rect('mc-sombra', A, B, f0 + 5, f0 + 6)
    for k in range(TRAMOS):
        cx = a + tramo * (k + 0.5)
        for j in (-1, 0, 1):
            ventanal(l, cx + j * 22, 18, 476, 490, luces=2, flecha=3)
    # el parapeto del pasillo: tableros sueltos
    g0, g1 = fy(492), fy(516)
    l.rect('mc-piedra', A, B, g0, g1)
    l.rect('mc-piedra-c', A, B, g0, g0 + 1)
    for k in range(TRAMOS):
        x0 = ux(a + tramo * k) + 2
        x1 = ux(a + tramo * (k + 1)) - 2
        n = 4
        p = (x1 - x0) / n
        for j in range(n):
            u = q(x0 + j * p + 0.5)
            v = q(x0 + (j + 1) * p - 0.5)
            l.rect('mc-hollin', u, v, g0 + 1, g1 - 1)
            mc = q((u + v) / 2)
            mf = (g0 + g1) // 2
            l.rect('mc-traceria', mc - 1, mc + 1, mf, mf + 1)                # el cuadrifolio: una cruz
            l.rect('mc-traceria', mc - 0.25, mc + 0.25, g0 + 2, g1 - 2)
            l.rect('mc-traceria', u, u + 0.25, g0 + 1, g1 - 1)               # el marco del tablero
            l.rect('mc-piedra-o', v - 0.25, v, g0 + 1, g1 - 1)
    l.rect('mc-piedra-c', A, B, g1 - 1, g1)
    l.rect('mc-hollin', A, B, g1, g1 + 1)

def reloj(l, cu, fc, rc):
    # Reloj redondo: aro de piedra con luz, anillo oscuro, esfera blanca, los números romanos como
    # marquitas en una corona y las agujas a las 10:20, como en la foto.
    for f in range(fc - round(rc) - 3, fc + round(rc) + 3):
        dy = f + 0.5 - fc
        for c, r in (('mc-piedra-c', rc + 2), ('mc-hollin', rc + 1), ('mc-esfera', rc + 0.25)):
            if abs(dy) < r:
                w = q((r * r - dy * dy) ** 0.5)
                l.rect(c, cu - w, cu + w, f, f + 1)
    for ang in range(12):
        a = ang * math.pi / 6
        for rr in (rc - 0.5, rc - 1.25):
            x = cu + rr * math.sin(a)
            f = math.floor(fc - rr * math.cos(a))
            l.rect('mc-hierro', q(x) - 0.25, q(x) + 0.25, f, f + 1)
    for grados, largo, c in ((310, rc * 0.5, 'mc-hierro'), (120, rc * 0.8, 'mc-hierro')):
        a = math.radians(grados)
        for k in range(1, 9):
            r = largo * k / 8
            x = cu + r * math.sin(a)
            f = math.floor(fc - r * math.cos(a))
            l.rect(c, q(x) - 0.25, q(x) + 0.25, f, f + 1)
    l.rect('mc-hierro', cu - 0.25, cu + 0.25, fc - 1, fc)

def campanario(l, cu):
    # Dos luces altas en punta con tablillas, separadas por el parante, bajo un arco con tracería: dos
    # arquitos con su trébol y un rombo en la punta; el goterón con su conopio y la flor.
    w = q(66 * S)
    fa, ff, fl = fy(262), fy(356), round(q(66 * S) * 0.62)
    hueco_apuntado(l, 'mc-hollin', cu, w + 1, fa, fl + 1, ff)
    hueco_apuntado(l, 'mc-piedra-c', cu, w + 0.5, fa, fl, ff)
    hueco_apuntado(l, 'mc-derrame', cu, w - 0.5, fa, fl - 1, ff)
    lw = q((w - 2.5) / 2)
    for s in (-1, 1):
        x = cu + s * (lw / 2 + 0.5)
        hueco_apuntado(l, 'mc-vidrio', x, lw, fy(282), round(lw * 0.7), ff - 1)
        for f in range(fy(286), ff - 1, 2):
            l.rect('mc-tablilla', x - lw / 2, x + lw / 2, f, f + 1)
        arco_linea(l, 'mc-traceria', x, lw + 0.5, fy(282) - round(lw * 0.7) - 1, round(lw * 0.6))
        l.rect('mc-traceria', x - 0.5, x + 0.5, fy(270), fy(270) + 1)          # el trébol
        l.rect('mc-traceria', x - 0.25, x + 0.25, fy(270) - 1, fy(270) + 2)
    l.rect('mc-traceria', cu - 0.25, cu + 0.25, fa - fl + 3, ff)               # el parante del medio
    f = fa - fl + 2                                                            # el rombo de la punta
    for d, wd in ((0, 0.25), (1, 0.75), (2, 0.25)):
        l.rect('mc-traceria', cu - wd, cu + wd, f + d, f + d + 1)
    for k in range(5):                                                         # el conopio y la flor
        l.rect('mc-piedra-c', cu - 0.25 - k * 0.25, cu + 0.25 + k * 0.25, fa - fl - 5 + k, fa - fl - 4 + k)
    l.rect('mc-piedra-c', cu - 0.25, cu + 0.25, fa - fl - 7, fa - fl - 5)
    l.rect('mc-piedra-c', cu - w / 2 - 1, cu + w / 2 + 1, ff, ff + 1)

def contrafuerte(l, cx, ancho, tope, fondo, retallos=2):
    # Contrafuerte con retallos (cada tramo un poco más angosto arriba), cara de luz y sombra a la derecha.
    cu = ux(cx)
    f0, f1 = fy(tope), fy(fondo)
    n = retallos + 1
    for k in range(n):
        fa = f0 + (f1 - f0) * k // n
        fb = f0 + (f1 - f0) * (k + 1) // n
        w = q(ancho * S * (0.7 + 0.3 * (k + 1) / n))
        sillar(l, cu - w / 2, cu + w / 2, fa, fb)
        l.rect('mc-piedra-c', cu - w / 2, cu - w / 2 + 0.5, fa, fb)
        l.rect('mc-piedra-o', cu + w / 2 - 0.75, cu + w / 2, fa, fb)
        l.rect('mc-sombra', cu + w / 2, cu + w / 2 + 0.5, fa + 1, fb)          # sombra sobre el muro
        l.rect('mc-piedra-c', cu - w / 2 - 0.25, cu + w / 2 + 0.25, fa, fa + 1)  # el talud con luz

def pinaculo(l, cx, punta, base, ancho, cruz=False):
    # Pináculo: fuste con su cara de luz y el panel calado, la aguja fina que se afina con ganchos
    # (crochets) a los dos lados, y la flor arriba.
    cu, w = ux(cx), q(ancho * S)
    fp, fb = fy(punta), fy(base)
    alto = fb - fp
    fuste = fp + round(alto * 0.55)
    U(l, 'mc-piedra', cu, w, fuste, fb)
    l.rect('mc-piedra-c', cu - w / 2, cu - w / 2 + 0.5, fuste, fb)
    l.rect('mc-piedra-o', cu + w / 2 - 0.5, cu + w / 2, fuste, fb)
    if w >= 2: U(l, 'mc-hollin', cu, q(w * 0.4), fuste + 1, fb - 1)       # el panel calado del fuste
    U(l, 'mc-piedra-c', cu, w + 0.5, fuste, fuste + 1)                     # la cornisita
    for f in range(fp + 1, fuste):
        t = (f - fp) / max(1, fuste - fp)
        hw = q(max(0.25, w / 2 * t * 0.8))
        l.rect('mc-piedra', cu - hw, cu + hw, f, f + 1)
        if hw > 0.25: l.rect('mc-piedra-c', cu - hw, cu, f, f + 1)
        if (f - fp) % 2 == 0 and f > fp + 1:                                # crochets
            l.rect('mc-piedra-c', cu - hw - 0.5, cu - hw, f, f + 1)
            l.rect('mc-piedra-o', cu + hw, cu + hw + 0.5, f, f + 1)
    if cruz:
        U(l, 'mc-piedra-o', cu, 0.5, fp - 3, fp + 1)
        U(l, 'mc-piedra-o', cu, 1.5, fp - 2, fp - 1)
    else:                                                                    # la flor: un botón con su tallo
        U(l, 'mc-piedra-c', cu, 1, fp - 1, fp + 1)
        U(l, 'mc-piedra', cu, 0.5, fp - 2, fp - 1)

def parapeto(l, a, b, f0, f1, almena=4, hueco=2):
    # Parapeto calado: almenas altas con dos ranuritas que dejan ver el cielo; debajo, una banda de
    # tableros calados (cuadrifolios en hollín con su cruz de piedra) y la cornisa con su sombra.
    fa = f0 + 3                                                              # pie de las almenas
    l.rect('mc-piedra', a, b, fa, f1)
    l.rect('mc-piedra-c', a, b, fa, fa + 1)                                  # la albardilla con luz
    x = a + 0.5
    while x + 2 <= b - 0.5:                                                  # los tableros calados
        l.rect('mc-hollin', x, x + 1.75, fa + 2, f1 - 2)
        l.rect('mc-traceria', x + 0.75, x + 1, fa + 2, f1 - 2)
        for f in range(fa + 2, f1 - 2, 2): l.rect('mc-traceria', x, x + 1.75, f, f + 1) if (f - fa) % 4 == 0 else None
        x += 2.25
    l.rect('mc-piedra-c', a, b, f1 - 2, f1 - 1)                              # la cornisa
    l.rect('mc-sombra', a, b, f1 - 1, f1)
    x = a
    while x < b:                                                             # almenas
        e = min(b, x + almena)
        l.rect('mc-piedra', x, e, f0, fa)
        l.rect('mc-piedra-c', x, e, f0, f0 + 1)
        l.rect('mc-piedra-o', e - 0.25, e, f0 + 1, fa)
        if almena >= 3:
            m = q((x + e) / 2)
            for d in (-0.75, 0.5):
                l.rect('-', m + d, m + d + 0.25, f0 + 1, fa - 0)
        x += almena + hueco

def torrecilla(l, cx, tope, base):
    # La torrecilla de la escalera: tambor de tableros, almenas con pinaculitos en las esquinas y la aguja.
    cu = ux(cx)
    w = q(40 * S)
    sillar(l, cu - w / 2, cu + w / 2, fy(tope), fy(base))
    tableros(l, cu, w - 2, fy(tope) + 3, fy(base) - 1, paso=2, alto=6)
    l.rect('mc-piedra-c', cu - w / 2, cu - w / 2 + 0.75, fy(tope), fy(base))
    l.rect('mc-piedra-o', cu + w / 2 - 1, cu + w / 2, fy(tope), fy(base))
    parapeto(l, cu - w / 2 - 0.5, cu + w / 2 + 0.5, fy(tope) - 6, fy(tope) + 1, almena=2.5, hueco=1.25)
    for s in (-1, 1): pinaculo(l, cx + s * 20, tope - 30, tope - 18, 6)
    pinaculo(l, cx, tope - 62, tope - 20, 14)

def tableros(l, cu, ancho, f0, f1, paso=2.5, alto=12):
    # Tracería ciega: paneles altos de cabeza apuntada, parejos desde el eje (lo perpendicular en el muro).
    n = int(ancho / 2 / paso)
    for k in range(-n, n + 1):
        x = cu + k * paso
        l.rect('mc-hollin', x - 0.25, x, f0, f1)                             # el parante: sombra a la derecha
        l.rect('mc-piedra-c', x, x + 0.25, f0, f1)
    for f in range(f0, f1 - 2, alto):                                        # cabezas de los paneles
        for k in range(-n, n):
            x = cu + k * paso
            l.rect('mc-piedra-c', x, x + paso, f, f + 1)
            l.rect('mc-hollin', x + 0.5, x + paso - 0.5, f + 1, f + 2)
            l.rect('mc-hollin', x + 0.25, x + 0.5, f + 2, f + 3)
            l.rect('mc-hollin', x + paso - 0.75, x + paso - 0.5, f + 2, f + 3)

def gastar(l, f_alta):
    # El desgaste de la arenisca: hollín debajo de cada saliente (cornisas, albardillas, alféizares) que
    # se corre hacia abajo en chorreaduras continuas de distinto largo, los cantos oscurecidos junto a las
    # sombras, y toda la parte alta (parapetos, pináculos) más negra, pareja, como en la foto.
    PIEDRA = ('mc-piedra', 'mc-piedra-c', 'mc-junta', 'mc-traceria')
    SALIENTE = ('mc-sombra', 'mc-hollin')
    alto, ancho = len(l.c), l.n
    nuevo = [fila[:] for fila in l.c]
    for i in range(ancho):
        racha = 99
        h = (i // 2 * 37 + 11) % 13                                         # chorreaduras de media unidad
        goteo = (3, 7, 1, 10, 2, 5, 1, 14, 2, 4, 1, 8, 3)[h]
        tope = f_alta + (0, 4, -2, 9, 1, -3, 6, 2, 12, -1, 3, 7, 0)[h]       # el borde de lo negro, desparejo
        for f in range(alto):
            c = l.c[f][i]
            if c in SALIENTE: racha = 0; continue
            if c not in PIEDRA: racha = 99; continue
            racha += 1
            if racha <= 1: nuevo[f][i] = c + '-g'
            elif racha <= 1 + goteo: nuevo[f][i] = c + ('-g' if f < tope and goteo > 4 else '-s')
            elif f < tope: nuevo[f][i] = c + '-s'
    for f in range(alto):                                                    # cantos junto a las sombras
        for i in range(1, ancho):
            if l.c[f][i - 1] in ('mc-piedra-o', 'mc-derrame') and nuevo[f][i] in PIEDRA: nuevo[f][i] += '-s'
    l.c = nuevo

def friso(l, a, b, f0, f1, k=0):
    # Friso tallado: una hilera de cuadrifolios (rombitos de luz sobre hollín) entre dos listeles.
    l.rect('mc-hollin', a, b, f0, f1)
    l.rect('mc-piedra-c', a, b, f0, f0 + 1)
    x = a + 0.5 + (0.75 if k % 2 else 0)
    m = (f0 + f1) // 2
    while x + 1.25 <= b:
        l.rect('mc-piedra-c', x + 0.25, x + 1, m, m + 1)
        if f1 - f0 > 3:
            l.rect('mc-piedra', x + 0.5, x + 0.75, m - 1, m)
            l.rect('mc-piedra-o', x + 0.5, x + 0.75, m + 1, m + 2)
        x += 1.5

def version():
    l = Lienzo(LARGO, FILAS)

    # La nave: muro de sillería, el parapeto calado alto y seis tramos iguales.
    a, b = NAVE
    sillar(l, ux(a), ux(b), fy(452), fy(SUELO))
    P(l, 'mc-hollin', a, b, 518, 522)                                    # el cordón bajo el parapeto
    P(l, 'mc-sombra', a, b, 522, 528)
    tramo = (b - a) / TRAMOS
    for k in range(TRAMOS):
        ventanal(l, a + tramo * (k + 0.5), 56, 566, 668)
    P(l, 'mc-piedra-c', a, b, 688, 692)                                  # zócalo con su talud
    P(l, 'mc-piedra-o', a, b, 692, SUELO)
    for k in range(TRAMOS + 1):
        contrafuerte(l, a + tramo * k, 24, 470, SUELO)
    remate_nave(l, a, b, tramo)
    for k in range(TRAMOS + 1):                                          # pares de pináculos en cada contrafuerte
        x = a + tramo * k
        pinaculo(l, x - 9, 414, 466, 9)
        pinaculo(l, x + 9, 424, 466, 9)
    torrecilla(l, a + tramo * 2, 420, 520)

    # El pórtico sur, como en la foto: simétrico desde su eje.
    cu = ux(EJE_P)
    PW = q(112 * S)
    sillar(l, cu - PW / 2, cu + PW / 2, fy(470), fy(SUELO))
    l.rect('mc-sombra', cu + PW / 2 + 2.5, cu + PW / 2 + 3.5, fy(470), fy(SUELO))   # su sombra sobre la nave
    parapeto(l, cu - PW / 2, cu + PW / 2, fy(428), fy(474), almena=4, hueco=2.5)
    tableros(l, cu, PW - 2, fy(477), fy(499), paso=2, alto=11)          # la banda de nichos
    U(l, 'mc-piedra-c', cu, PW, fy(499), fy(499) + 1)
    for s in (-1, 1):                                                   # dos ventanas con su moldura recta
        x = EJE_P + s * 27
        xu = ux(x)
        ventanal(l, x, 24, 516, 556, luces=2)
        l.rect('mc-hollin', xu - 3.75, xu + 3.75, fy(506), fy(506) + 1)
        for e in (-3.75, 3.5): l.rect('mc-hollin', xu + e, xu + e + 0.25, fy(506), fy(516))
    hueco_apuntado(l, 'mc-hollin', cu, 2, fy(518), 2, fy(552))          # el nicho del medio y su figura
    U(l, 'mc-piedra-c', cu, 0.75, fy(526), fy(550))
    U(l, 'mc-piedra-c', cu, 0.5, fy(522), fy(526))
    U(l, 'mc-piedra-c', cu, PW, fy(560), fy(560) + 1)                   # los dos frisos
    friso(l, cu - PW / 2 + 0.5, cu + PW / 2 - 0.5, fy(565), fy(581), 0)
    friso(l, cu - PW / 2 + 0.5, cu + PW / 2 - 0.5, fy(583), fy(599), 1)
    # la puerta: arco de varias roscas dentro de un marco recto, con las enjutas talladas
    fr0, fr1 = fy(602), fy(645)
    l.rect('mc-piedra-c', cu - q(51 * S), cu + q(51 * S), fr0, fr0 + 1)
    l.rect('mc-hollin', cu - q(51 * S), cu + q(51 * S), fr0 + 1, fr0 + 2)
    for e in (-1, 1): U(l, 'mc-hollin', cu + e * q(50 * S), 0.5, fr0, fr1)
    for f in range(fr0 + 2, fr1):                                       # tracería de las enjutas
        for x in range(round((cu - q(48 * S)) * 4), round((cu + q(48 * S)) * 4)):
            if (x + 2 * f) % 6 == 0: l.rect('mc-piedra-o', x / 4, x / 4 + 0.25, f, f + 1)
    for c, w in (('mc-hollin', 94), ('mc-piedra-c', 88), ('mc-piedra', 82), ('mc-hollin', 77),
                 ('mc-piedra-c', 72), ('mc-piedra-o', 67), ('mc-derrame', 62)):
        hueco_apuntado(l, c, cu, q(w * S), fy(642), round(q(w * S) * 0.42), fy(SUELO))
    hueco_apuntado(l, 'mc-puerta', cu + 0.25, q(56 * S), fy(642), round(q(56 * S) * 0.42) - 1, fy(SUELO))
    U(l, 'mc-hollin', cu + 0.25, 0.5, fy(632), fy(SUELO))
    for j in (-4, -2, 2, 4):
        U(l, 'mc-puerta-c', cu + 0.25 + j, 0.25, fy(652), fy(SUELO))
    for e in (-1, 1.5): U(l, 'mc-hierro', cu + e, 0.5, fy(676), fy(678))
    # contrafuertes del pórtico con sus manojos de pináculos, y la cruz del medio
    for s in (-1, 1):
        x = EJE_P + s * 67
        contrafuerte(l, x, 22, 440, SUELO, retallos=3)
        pinaculo(l, x, 362, 444, 18)
        pinaculo(l, x - 9, 404, 444, 6)
        pinaculo(l, x + 9, 404, 444, 6)
    pinaculo(l, EJE_P, 380, 432, 9, cruz=True)

    # La torre, simétrica desde su eje salvo el cuerpo bajo, que sigue la foto.
    cu = ux(EJE_T)
    TW = q(150 * S)
    sillar(l, cu - TW / 2, cu + TW / 2, fy(176), fy(SUELO))
    for y in (176, 365, 470):                                            # cordones entre cuerpos
        U(l, 'mc-piedra-c', cu, TW + 1, fy(y), fy(y) + 1)
        U(l, 'mc-hollin', cu, TW, fy(y) + 1, fy(y) + 2)
        U(l, 'mc-sombra', cu, TW, fy(y) + 2, fy(y) + 3)
    # campanario: tracería ciega, el arco con su conopio y las dos luces con tablillas
    tableros(l, cu, TW - 3, fy(188), fy(362), paso=3, alto=20)
    campanario(l, cu)
    U(l, 'mc-piedra-c', cu, TW - 4, fy(356), fy(356) + 1)               # el alféizar
    # el reloj, redondo en su aro
    reloj(l, cu, fy(410), q(20 * S))
    tableros(l, cu, TW - 3, fy(436), fy(466), alto=10)
    # el cuerpo bajo, como en la foto: el balconcito almenado con sus pináculos, el caño de bajada,
    # el ventanal de tres luces corrido a la derecha y el nicho con su figura en el contrafuerte.
    parapeto(l, ux(141), ux(216), fy(476), fy(516), almena=3, hueco=2)
    pinaculo(l, 152, 440, 486, 8)
    pinaculo(l, 186, 452, 486, 6)
    ventanal(l, 194, 42, 568, 656, luces=3)
    P(l, 'mc-hierro', 150, 153, 516, SUELO)
    for y in range(540, SUELO, 40): P(l, 'mc-hierro', 148, 155, y, y + 3)
    for s in (-1, 1):
        contrafuerte(l, EJE_T + s * 84, 34, 150, SUELO, retallos=4)
    x = ux(EJE_T - 84)
    hueco_apuntado(l, 'mc-hollin', x, 2.5, fy(520), 2, fy(556))
    l.rect('mc-piedra-c', x - 0.5, x + 0.5, fy(524), fy(554))
    l.rect('mc-piedra-c', x - 1.5, x + 1.5, fy(556), fy(558))
    parapeto(l, cu - TW / 2 - 1, cu + TW / 2 + 1, fy(134), fy(180), almena=3, hueco=1.75)
    for s in (-1, 1):
        pinaculo(l, EJE_T + s * 84, 66, 150, 26)
        pinaculo(l, EJE_T + s * 62, 86, 140, 12)
    pinaculo(l, EJE_T, 100, 140, 12)
    l.sombra(cu + TW / 2 + 1, cu + TW / 2 + 3.5, fy(140), fy(470), ('mc-piedra', 'mc-junta', 'mc-piedra-c'))

    gastar(l, fy(530))

    # Abajo: losas mojadas del atrio con reflejos, dos pedestales tallados, el pasto delante de la nave.
    P(l, 'mc-losa', X0, 400, SUELO, Y1)
    P(l, 'mc-pasto', 400, X1, SUELO, Y1)
    for f in range(fy(SUELO), FILAS):
        k = f - fy(SUELO)
        x = ux(X0) + (k // 3 % 2) * 2.5
        while x < ux(400):
            if k % 3 == 2: l.rect('mc-losa-o', x, x + 5, f, f + 1)
            else:
                l.rect('mc-losa-o', x, x + 0.25, f, f + 1)
                if (round(x * 4) + k) % 7 == 0: l.rect('mc-losa-c', x + 0.75, x + 2.5, f, f + 1)
            x += 5
        x = ux(400) + (k % 2) * 0.75
        while x < ux(X1):
            l.rect('mc-pasto-c', x, x + 0.5, f, f + 1)
            x += 1.75
    P(l, 'mc-piedra-o', 400, X1, SUELO, SUELO + 4)
    for x in (96, 394):
        cu = ux(x)
        U(l, 'mc-piedra-c', cu, 7, fy(688), fy(692))
        U(l, 'mc-hollin', cu, 6.5, fy(692), fy(696))
        U(l, 'mc-piedra', cu, 5, fy(696), fy(744))
        l.rect('mc-piedra-c', cu - 2.5, cu - 1.75, fy(696), fy(744))
        l.rect('mc-piedra-o', cu + 1.75, cu + 2.5, fy(696), fy(744))
        U(l, 'mc-hollin', cu, 3, fy(704), fy(732))
        U(l, 'mc-piedra-o', cu, 1.5, fy(712), fy(724))
        U(l, 'mc-piedra-c', cu, 6.5, fy(744), fy(748))

    return {'nota': 'La catedral de Manchester, el lado sur: la torre con sus pináculos, el campanario y el '
                    'reloj, el pórtico con la puerta en arco dentro de su marco y los frisos tallados, y la nave '
                    'con los ventanales perpendiculares, contrafuertes, el parapeto calado y los pináculos; '
                    'arenisca negra de hollín debajo de cada saliente.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

PIEDRA = ('mc-piedra', 'mc-piedra-c', 'mc-junta', 'mc-traceria')
SOMBREABLES = ('mc-piedra', 'mc-piedra-c', 'mc-junta', 'mc-hollin', 'mc-traceria')
COLORES = {
    'mc-piedra': ('#b59b74', '#a68e6a'), 'mc-piedra-c': ('#d2bb94', '#c0aa86'), 'mc-piedra-o': ('#8c7556', '#7e694d'),
    'mc-junta': ('#a99070', '#9a8466'), 'mc-sombra': ('#6f5c45', '#64533e'), 'mc-hollin': ('#45392e', '#3f342a'),
    'mc-derrame': ('#5c4c3b', '#544535'), 'mc-traceria': ('#a8916d', '#9a8564'),
    'mc-vidrio': ('#47515b', '#3f4851'), 'mc-vidrio-c': ('#7a8590', '#6c7782'),
    'mc-tablilla': ('#6a5a48', '#5e5040'), 'mc-oro': ('#c9a443', '#b8963d'),
    'mc-esfera': ('#f1efe8', '#e2e0d8'), 'mc-esfera-o': ('#c9c4b6', '#bab5a8'), 'mc-hierro': ('#2a2622', '#2a2622'),
    'mc-puerta': ('#2a201a', '#251c17'), 'mc-puerta-c': ('#46362a', '#3f3126'),
    'mc-losa': ('#7d7468', '#5f574d'), 'mc-losa-o': ('#5c554c', '#47413a'), 'mc-losa-c': ('#a8a196', '#7c766c'),
    'mc-pasto': ('#5f8a3a', '#4c702e'), 'mc-pasto-c': ('#72a046', '#5c8239'),
    'perpendicular-fondo': ('#d7d3c7', '#2b2a27'), 'perpendicular-fondo-marco': ('#5a4c3c', '#e1dccd'),
}
con_sombras(COLORES, SOMBREABLES)
con_sombras(COLORES, PIEDRA, 0.6, '-g')

if __name__ == '__main__':
    p = version()
    p.update(placa='perpendicular-fondo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
             marco='perpendicular-fondo-marco')
    guardar(sys.argv[1], 'estilos', 'Gótico perpendicular', p, COLORES, 'mc-|perpendicular-')
    print(len(p['lineas']), 'líneas, largo', p['largo'])
