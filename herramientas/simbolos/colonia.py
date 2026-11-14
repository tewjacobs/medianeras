# Catedral de Colonia, fachada oeste de frente y simétrica, medida en px sobre
# referencias/simbolos/gotico/Kölner_Dom_-_Westfassade_2022_ohne_Gerüst-0968_b.jpg (agrandada a 660 de ancho:
# frente de x 108 a 548, base en y 1010, puntas en y 30); los niveles, de catedral-de-colonia-alemania…webp.
# Dos torres de cinco niveles: planta baja (portada de la torre y ventanal de afuera), dos ventanales por torre,
# un ventanal grande con su gablete, el campanario con su ventana y las agujas de las esquinas, y la aguja calada
# con crochets y la flor arriba. En el medio la portada grande con el tímpano dorado, el ventanal de la nave y el
# piñón con la cruz. Contrafuertes con pináculos en cada nivel. Luz desde la izquierda.
# Uso: colonia.py <simbolos.json> (pone estilos."Gótico").
import sys
from armar import Lienzo, guardar

S = 0.25                                  # unidades por px de la foto agrandada
LARGO = round(440 * S)                    # 110
CX = LARGO / 2
FILAS = round(980 * S) + 3                # hasta la base, más la plaza
TC = -30                                  # eje de la torre izquierda, desde el eje de la fachada

def q(x): return round(x * 4) / 4

def R(l, c, a, b, f0, f1):
    # Rectángulo de a a b (desde el eje) y su espejo.
    a, b = q(a), q(b)
    l.rect(c, CX + a, CX + b, f0, f1)
    l.rect(c, CX - b, CX - a, f0, f1)

def T(l, c, a, b, f0, f1): R(l, c, TC + a, TC + b, f0, f1)          # desde el eje de la torre

def aguja(l, c, cx, w, f_base, f_punta):
    # Triángulo lleno de medio ancho w en f_base hasta la punta en f_punta.
    n = f_base - f_punta
    for k in range(n):
        hw = q(w * (k + 1) / n)
        R(l, c, cx - hw, cx + hw, f_punta + k, f_punta + k + 1)

def pinaculo(l, cx, w, f_base, f_punta):
    aguja(l, 'ko-piedra', cx, w, f_base, f_punta)
    R(l, 'ko-piedra-c', cx - w, cx - w + 0.5, f_base, f_base + 2)
    R(l, 'ko-piedra-c', cx - 0.25, cx + 0.25, f_punta - 1, f_punta)     # florón

def gablete(l, cx, w, f_base, f_punta, relleno='ko-piedra', libre=None):
    # Gablete simétrico: doble moldura en los dos cantos (borde claro y la línea en sombra adentro),
    # crochets parejos y florón. `libre`: filas libres arriba (sin la cabeza del ventanal) para el rosetón.
    n = f_base - f_punta
    for k in range(n):
        hw = q(w * (k + 1) / n)
        f = f_punta + k
        R(l, relleno, cx - hw, cx + hw, f, f + 1)
        R(l, 'ko-piedra-c', cx - hw, cx - hw + 0.5, f, f + 1)
        R(l, 'ko-piedra-c', cx + hw - 0.5, cx + hw, f, f + 1)
        if hw > 1.5:
            R(l, 'ko-piedra-o', cx - hw + 0.5, cx - hw + 0.75, f, f + 1)
            R(l, 'ko-piedra-o', cx + hw - 0.75, cx + hw - 0.5, f, f + 1)
        if k % 3 == 1 and hw > 1:                                      # crochets
            R(l, 'ko-piedra-c', cx - hw - 0.5, cx - hw, f, f + 1)
            R(l, 'ko-piedra-c', cx + hw, cx + hw + 0.5, f, f + 1)
    R(l, 'ko-piedra-c', cx - 0.25, cx + 0.25, f_punta - 3, f_punta)       # florón en cruz
    R(l, 'ko-piedra-c', cx - 1, cx + 1, f_punta - 2, f_punta - 1)
    libre = n if libre is None else libre
    if libre >= 8:                                                      # rosetón en el hueco de arriba
        r = q(min(w * 0.4, (libre - 3) / 2))
        if r >= 1.5: cuadrifolio(l, cx, f_punta + round(libre * 0.55), r, 'ko-piedra-o')
    if n >= 26:                                                         # arquería ciega escalonada
        for d in (-0.5, -0.25, 0, 0.25, 0.5):
            x = cx + q(w * d)
            f0 = f_punta + round(n * (0.62 + abs(d) * 0.5))
            R(l, 'ko-piedra-o', x - 0.5, x + 0.5, f0 + 1, f_base)
            R(l, 'ko-piedra-c', x - 0.25, x + 0.25, f0, f0 + 1)

def cuadrifolio(l, cx, fc, r, hueco):
    # Aro de tracería con cuatro lóbulos redondos calados adentro (arriba, abajo y a los lados).
    def disco(c, x, f, rr):
        for k in range(-round(rr), round(rr) + 1):
            hw = q(max(0, rr * rr - k * k) ** 0.5)
            if hw > 0: R(l, c, x - hw, x + hw, f + k, f + k + 1)
    disco('ko-traceria', cx, fc, r)
    d, rl = r * 0.42, max(0.5, r * 0.42)
    for dx, df in ((0, -d), (0, d), (-d, 0), (d, 0)):
        disco(hueco, cx + q(dx), fc + round(df), rl)
    R(l, 'ko-traceria', cx - 0.25, cx + 0.25, fc, fc + 1)

def rosa(l, cx, fc, r):
    cuadrifolio(l, cx, fc, r, 'ko-piedra-o')

def ojiva(w, k):
    # Medio ancho de un arco apuntado (de tercio) a k filas por encima del arranque.
    v = 4 * w * w - k * k
    return q(v ** 0.5 - w) if v > 0 else 0

def ventanal(l, cx, w, f0, f1, parteluces=2):
    # Ventanal apuntado completo: dos molduras alrededor (clara y en sombra), vidrio con vitrales de tonos
    # apagados en rombos, parteluces con sus arquitos apuntados, cuadrifolio en la cabeza, barras de hierro
    # y el alféizar abajo. Simétrico.
    alto = round(3 ** 0.5 * w)
    def forma(c, ext, a, b):
        # La silueta del ventanal agrandada `ext` unidades, de la fila a a la b.
        for k in range(alto):
            hw = ojiva(w, alto - k)
            if hw > 0 and a <= f0 + k < b: R(l, c, cx - hw - ext, cx + hw + ext, f0 + k, f0 + k + 1)
        R(l, c, cx - w - ext, cx + w + ext, max(a, f0 + alto), b)
    forma('ko-piedra-c', 1, f0 - 1, f1)
    forma('ko-piedra-o', 0.75, f0 - 1, f1)
    forma('ko-marco', 0.5, f0, f1)
    forma('ko-vidrio', 0, f0, f1)
    # Vitrales: rombitos de color sobre el vidrio oscuro.
    for f in range(f0 + 1, f1 - 1):
        hw = ojiva(w, alto - (f - f0)) if f < f0 + alto else w
        fila = f - f0
        d = 0.5 + (fila // 2) % 2 * 0.5                                # rombitos: cada dos filas se corren medio
        while d < hw - 0.25:
            c = ('ko-vitral-a', 'ko-vitral-r', 'ko-vitral-a', 'ko-vitral-o')[(round(d * 2) + fila // 2) % 4]
            R(l, c, cx + d - 0.25, cx + d, f, f + 1)                   # las dos mitades del ventanal
            R(l, c, cx - d, cx - d + 0.25, f, f + 1)
            d += 1
    if parteluces:
        paso = 2 * w / (parteluces + 1)
        for i in range(1, parteluces + 1):
            x = cx - w + q(paso * i)
            R(l, 'ko-traceria', x - 0.25, x + 0.25, f0 + alto, f1)
        r = q(w * 0.5)
        fc = f0 + round(alto * 0.6)
        if r >= 1.5: cuadrifolio(l, cx, fc, r, 'ko-vidrio')
        pl = paso / 2 - 0.25                                           # cada lanceta con su arquito apuntado
        hl = max(1, round(3 ** 0.5 * pl))
        for i in range(parteluces + 1):
            xl = cx - w + q(paso * (i + 0.5))
            for k in range(hl):
                hw = ojiva(pl, hl - k)
                f = f0 + alto + k
                if hw < pl:
                    R(l, 'ko-traceria', xl - pl - 0.25, xl - hw, f, f + 1)
                    R(l, 'ko-traceria', xl + hw, xl + pl + 0.25, f, f + 1)
            R(l, 'ko-traceria', xl - pl, xl + pl, f0 + alto - 1, f0 + alto)
            for f in range(f0 + alto + hl + 4, f1 - 2, 5):             # barras de hierro
                R(l, 'ko-marco', xl - pl + 0.25, xl + pl - 0.25, f, f + 1)
    R(l, 'ko-piedra-c', cx - w - 1, cx + w + 1, f1 - 1, f1)             # alféizar

def ventanal_g(l, cx, w, f0, f1, alto_gablete, parteluces):
    # Ventanal con su gablete: el triángulo arranca donde arranca el arco y lo envuelve.
    alto = round(3 ** 0.5 * w)
    f = f0 + alto
    gablete(l, cx, w + 2, f, f - alto_gablete, libre=alto_gablete - alto - 2)
    ventanal(l, cx, w, f0, f1, parteluces)

def contrafuerte(l, cx, w, f0, f1, punta):
    # Contrafuerte de medio ancho w de f0 a f1 con canto claro, nichos y pináculo arriba hasta `punta`.
    R(l, 'ko-piedra', cx - w, cx + w, f0, f1)
    R(l, 'ko-piedra-c', cx - w, cx - w + 0.75, f0, f1)
    R(l, 'ko-piedra-o', cx + w - 0.75, cx + w, f0, f1)
    for f in range(f0 + 3, f1 - 6, 9):                                 # nichos con su estatua y doselete
        R(l, 'ko-piedra-o', cx - 0.75, cx + 0.75, f + 1, f + 6)
        R(l, 'ko-piedra-c', cx - 0.25, cx + 0.25, f - 1, f + 1)
        R(l, 'ko-estatua', cx - 0.25, cx + 0.25, f + 2, f + 3)
        R(l, 'ko-estatua', cx - 0.5, cx + 0.5, f + 3, f + 6)
        R(l, 'ko-piedra-c', cx - 0.75, cx + 0.75, f + 6, f + 7)
    pinaculo(l, cx, w, f0, punta)
    for f in range(punta + 2, f0, 2):                                  # crochets del pináculo
        hw = q(w * (f - punta) / (f0 - punta))
        R(l, 'ko-piedra-c', cx - hw - 0.25, cx - hw, f, f + 1)
        R(l, 'ko-piedra-o', cx + hw, cx + hw + 0.25, f, f + 1)

def galeria(l, a, b, f):
    # Galería calada: pasamanos y arquitos con el hueco oscuro.
    R(l, 'ko-piedra-c', a, b, f, f + 1)
    x = a + 0.25
    while x + 0.75 <= b:
        R(l, 'ko-piedra-o', x + 0.25, x + 0.5, f + 1, f + 2)
        R(l, 'ko-piedra-o', x, x + 0.75, f + 2, f + 3)
        x += 1.25
    R(l, 'ko-piedra-c', a, b, f + 3, f + 4)

def paneles(l, a, b, f0, f1):
    # Tracería ciega: paneles en relieve (varilla con luz y su sombra), cada uno con cabeza apuntada,
    # trébol y travesaño cada 12 filas.
    paso, x = 2.5, a + 0.75
    while x + paso <= b + 0.01:
        R(l, 'ko-piedra-c', x, x + 0.25, f0, f1)
        R(l, 'ko-piedra-o', x + 0.25, x + 0.5, f0, f1)
        m = q(x + 0.5 + (paso - 0.5) / 2)
        for f in range(f0 + 2, f1 - 4, 12):
            R(l, 'ko-piedra-c', m - 0.25, m, f, f + 1)
            R(l, 'ko-piedra-o', m, m + 0.25, f, f + 1)
            R(l, 'ko-piedra-c', m - 0.75, m - 0.5, f + 1, f + 2)
            R(l, 'ko-piedra-o', m + 0.5, m + 0.75, f + 1, f + 2)
            R(l, 'ko-piedra-c', m - 1, m - 0.75, f + 2, f + 3)
            R(l, 'ko-piedra-o', m + 0.75, m + 1, f + 2, f + 3)
            R(l, 'ko-piedra-o', m - 0.25, m + 0.25, f + 1, f + 3)        # trébol
            R(l, 'ko-piedra-c', x + 0.5, x + paso, f + 4, f + 5)         # travesaño
        x += paso

def fialas(l, a, b, f, alto, paso=2.5):
    # Bosque de pináculos finos sobre una cornisa, de a a b (desde el eje), con su florón.
    x = a + paso / 2
    while x <= b - paso / 2 + 0.01:
        pinaculo(l, q(x), 0.75, f, f - alto)
        x += paso

def version():
    l = Lienzo(LARGO, FILAS)
    BASE = FILAS - 3
    # Filas de cada nivel, de la foto: y 860, 690, 510, 380 → filas 208, 165, 120, 88.
    N1, N2, N3, N4 = 208, 165, 120, 88

    # Cuerpo de las torres, nivel por nivel (más angostas al subir).
    T(l, 'ko-piedra', -24, 24, N2, BASE)
    T(l, 'ko-piedra', -22, 22, N3, N2)
    T(l, 'ko-piedra', -17, 17, N4, N3)
    paneles(l, TC - 24 + CX - CX, TC + 24, N2, BASE)
    paneles(l, TC - 22, TC + 22, N3, N2)
    paneles(l, TC - 17, TC + 17, N4, N3)
    R(l, 'ko-piedra', -6, 6, N2, BASE)                                 # cuerpo del medio

    # Aguja calada: crochets en los cantos, bandas de tracería y la flor arriba.
    f_punta, f_base, w = 4, N4, 11
    n = f_base - f_punta
    for k in range(n):
        hw = q(w * (k + 1) / n)
        f = f_punta + k
        T(l, 'ko-piedra', -hw, hw, f, f + 1)
        if hw > 2:
            T(l, 'ko-piedra-o', -hw + 1, hw - 1, f, f + 1)
            if k % 6 in (2, 3, 4) and hw > 3:                          # huecos calados entre nervios: se ve el fondo
                bordes = [-hw + 1, -hw / 2, 0, hw / 2, hw - 1]
                for x0, x1 in zip(bordes, bordes[1:]):
                    m, w2 = (x0 + x1) / 2, (x1 - x0) / 2 - (0.75 if k % 6 != 3 else 0.5)
                    if (k // 6) % 2: m, w2 = m, w2 - 0.25                # filas alternadas, huecos un poco distintos
                    if w2 > 0.2: T(l, '-', q(m - w2), q(m + w2), f, f + 1)
            if k % 6 in (0, 1):
                T(l, 'ko-piedra', -hw + 1, hw - 1, f, f + 1)
            if k % 6 == 0:
                T(l, 'ko-piedra-c', -hw + 1, hw - 1, f, f + 1)
            for x in (-hw / 2, 0, hw / 2):
                T(l, 'ko-piedra', x - 0.25, x + 0.25, f, f + 1)
        T(l, 'ko-piedra-c', -hw, -hw + 0.5, f, f + 1)
        if k % 4 == 2 and hw > 1:
            T(l, 'ko-piedra-c', -hw - 0.5, -hw, f, f + 1)
            T(l, 'ko-piedra-o', hw, hw + 0.5, f, f + 1)
    T(l, 'ko-piedra-c', -1.5, 1.5, 1, 2)                               # flor
    T(l, 'ko-piedra-c', -0.5, 0.5, 0, 4)
    T(l, 'ko-piedra-c', -1, 1, 2, 3)

    # Campanario: ventana alta con gablete, agujas de las esquinas, pináculos en el arranque de la aguja.
    ventanal_g(l, TC, 4.5, N4 + 3, N3 - 3, 22, 1)
    for s in (-1, 1):
        contrafuerte(l, TC + s * 15.5, 1.75, N4, N3, N4 - 18)
        pinaculo(l, TC + s * 9.5, 1.25, N4 + 1, N4 - 10)

    # Tercer nivel: ventanal grande con gablete; contrafuertes de esquina con pináculos.
    ventanal_g(l, TC, 7, N3 + 3, N2 - 3, 28, 3)
    for x in (-20, 20):
        contrafuerte(l, TC + x, 2, N3, N2, N3 - 12)
    for x in (-12.5, 12.5):
        pinaculo(l, TC + x, 1.25, N3 + 2, N3 - 6)

    # Piñón de la nave entre las torres, con la cruz.
    gablete(l, 0, 8, N2, N2 - 34)
    ventanal(l, 0, 2.5, N2 - 22, N2 - 4, parteluces=1)
    R(l, 'ko-piedra-c', -0.25, 0.25, N2 - 41, N2 - 35)                 # cruz
    R(l, 'ko-piedra-c', -1.25, 1.25, N2 - 39, N2 - 38)

    # Segundo nivel: dos ventanales por torre y el ventanal grande de la nave.
    for x in (-11, 11):
        ventanal_g(l, TC + x, 5.5, N2 + 3, N1 - 3, 20, 2)
    ventanal_g(l, 0, 5, N2 + 3, N1 - 3, 20, 3)

    # Planta baja: ventanal de afuera y portada de la torre; la portada grande en el medio.
    ventanal_g(l, TC - 11, 5, N1 + 5, BASE - 2, 16, 2)
    for cx, w in ((TC + 11, 5.5), (0, 6)):
        alto = round(3 ** 0.5 * w)
        gablete(l, cx, w + 2.5, N1 + 6 + alto, N1 - 6)
        fa = N1 + 6
        ft = fa + alto                                                 # arranque de los arcos
        # Arquivoltas: molduras y filas de estatuas bajo doseletes, que bajan por las jambas.
        for dw, c in ((3, 'ko-piedra-c'), (2.25, 'est'), (1.5, 'ko-piedra'), (0.75, 'est'), (0, 'ko-oro')):
            ar = round(3 ** 0.5 * (w + dw))
            for k in range(ar):
                hw = ojiva(w + dw, ar - k)
                if hw <= 0: continue
                f = ft - ar + k
                col = c if c != 'est' else ('ko-marco' if k % 3 == 2 else 'ko-estatua')
                R(l, col, cx - hw, cx + hw, f, f + 1)
            for f in range(ft, BASE):
                col = c if c != 'est' else ('ko-piedra-c' if (f - ft) % 7 == 0 else 'ko-piedra-o' if (f - ft) % 7 == 6 else 'ko-estatua')
                R(l, col, cx - w - dw, cx - w - dw + 0.75, f, f + 1) if dw else None
                if dw: R(l, col, cx + w + dw - 0.75, cx + w + dw, f, f + 1)
        # Tímpano: tres registros de figuras y la figura grande en la punta.
        for f0r in (ft - 5, ft - 1, ft + 3):
            R(l, 'ko-oro-o', cx - w, cx + w, f0r - 1, f0r)
            x = cx - w + 0.5
            while x < cx + w - 0.5:
                R(l, 'ko-oro-c', x, x + 0.5, f0r + 1, f0r + 3)            # cuerpos
                R(l, 'ko-oro-c', x + 0.125 - 0.125, x + 0.5, f0r, f0r + 1) if False else R(l, 'ko-oro-c', x, x + 0.25, f0r, f0r + 1)
                x += 1
        mf = ft - round(alto * 0.75)
        R(l, 'ko-oro-o', cx - 1.25, cx + 1.25, mf - 1, mf + 4)            # mandorla
        R(l, 'ko-oro-c', cx - 0.75, cx + 0.75, mf, mf + 4)
        R(l, 'ko-oro-o', cx - 0.25, cx + 0.25, mf - 1, mf)
        # Dintel, puertas de dos hojas con tachas y el parteluz con su estatua y doselete.
        R(l, 'ko-piedra-c', cx - w, cx + w, ft + 6, ft + 7)
        R(l, 'ko-puerta', cx - w, cx + w, ft + 7, BASE)
        for f in range(ft + 8, BASE, 2):
            x = cx - w + 0.5
            while x < cx + w - 0.25:
                R(l, 'ko-puerta-l', x, x + 0.25, f, f + 1)
                x += 1
        R(l, 'ko-piedra', cx - 0.75, cx + 0.75, ft + 7, BASE)
        R(l, 'ko-piedra-c', cx - 1, cx + 1, ft + 7, ft + 8)
        R(l, 'ko-estatua', cx - 0.25, cx + 0.25, ft + 8, ft + 9)
        R(l, 'ko-estatua', cx - 0.5, cx + 0.5, ft + 9, ft + 14)
        R(l, 'ko-piedra-o', cx - 0.75, cx + 0.75, ft + 14, ft + 15)
        for s in (-1, 1):                                              # pináculos a los lados del gablete
            pinaculo(l, cx + s * (w + 3.75), 0.75, ft - 2, ft - 14)

    # Contrafuertes de abajo: tres por torre, con pináculos que suben al nivel de arriba.
    for x in (-21.5, 0, 21.5):
        contrafuerte(l, TC + x, 2.5, N1, BASE, N1 - 8)
        contrafuerte(l, TC + x, 2.25, N2, N1, N2 - 8)

    # Cornisas entre niveles.
    for f, w in ((N1, 24), (N2, 24), (N3, 22)):
        T(l, 'ko-piedra-c', -w, w, f, f + 1)
    R(l, 'ko-piedra-c', -6, 6, N1, N1 + 1)
    for f, w in ((N2 - 4, 24), (N3 - 4, 22), (N4 - 4, 17)):           # galerías caladas arriba de cada nivel
        galeria(l, TC - w, TC + w, f)
    galeria(l, -6, 6, N2 - 4)
    fialas(l, TC - 22, TC - 17.5, N3 - 4, 7, 2)                         # retiro del campanario
    fialas(l, TC + 17.5, TC + 22, N3 - 4, 7, 2)
    fialas(l, TC - 16.5, TC - 12, N4 - 4, 6, 2)                         # arranque de la aguja
    fialas(l, TC + 12, TC + 16.5, N4 - 4, 6, 2)
    for x in (-30, 30):                                                # faroles de globo de la plaza
        l.rect('ko-farol', CX + x - 0.25, CX + x + 0.25, BASE - 15, BASE)
        l.rect('ko-farol', CX + x - 1.5, CX + x + 1.5, BASE - 15, BASE - 14)
        for d in (-1.5, 0, 1.5):
            l.rect('ko-globo', CX + x + d - 0.5, CX + x + d + 0.5, BASE - 17, BASE - 15)

    # Plaza.
    l.rect('ko-plaza', 0, LARGO, BASE, BASE + 2)
    l.rect('ko-plaza-o', 0, LARGO, BASE + 2, BASE + 3)
    return {'nota': 'La catedral de Colonia, fachada oeste de frente: las dos torres con sus ventanales apuntados, '
                    'gabletes y contrafuertes con pináculos, el campanario, las agujas caladas con crochets y su '
                    'flor, el piñón de la nave con la cruz y las tres portadas con el tímpano dorado.',
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

COLORES = {
    'ko-piedra': ('#4b4540', '#4b4540'), 'ko-piedra-c': ('#7a7166', '#7a7166'), 'ko-piedra-o': ('#2e2a27', '#2e2a27'),
    'ko-marco': ('#625a51', '#625a51'), 'ko-vidrio': ('#1f2229', '#1f2229'), 'ko-traceria': ('#8a8072', '#8a8072'),
    'ko-oro': ('#b0935e', '#b0935e'), 'ko-oro-o': ('#8a7044', '#8a7044'), 'ko-oro-c': ('#d3b97f', '#d3b97f'), 'ko-vitral-a': ('#2f3a5c', '#2f3a5c'), 'ko-vitral-r': ('#5a2e34', '#5a2e34'), 'ko-vitral-o': ('#6a5a34', '#6a5a34'), 'ko-puerta': ('#2a221e', '#2a221e'),
    'ko-puerta-l': ('#3b302a', '#3b302a'), 'ko-estatua': ('#9a8f80', '#9a8f80'),
    'ko-farol': ('#2b2b2b', '#2b2b2b'), 'ko-globo': ('#f1ead8', '#f1ead8'),
    'ko-plaza': ('#bdb6aa', '#77726b'), 'ko-plaza-o': ('#9b958a', '#5c5853'),
    'gotico-cielo': ('#a9c0d4', '#5f7891'), 'gotico-cielo-marco': ('#563f2b', '#f3ead9'),
}

p = version()
p.update(placa='gotico-cielo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
         marco='gotico-cielo-marco')
guardar(sys.argv[1], 'estilos', 'Gótico', p, COLORES, 'ko-|gotico-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
