# Puente japonés de Hoi An (Vietnam), para Infraestructura, medido sobre referencias/simbolos/infraestructura/images (15).jpeg
# (447 px de ancho), de frente y simétrico sobre el eje x = 220. Líneas horizontales sin separación: los adornos de
# la cumbrera, el techo de tejas con el tramo del medio más alto y las puntas levantadas, la galería oscura con sus
# postes, faroles y baranda, el tablero de piedra apenas arqueado con la placa, las pilas con sus arcos y el canal,
# entre los muros rojos de las orillas.
# Uso: hoian.py <simbolos.json> (pone programas.Infraestructura).
import sys, math
from armar import Lienzo, guardar

EJE = 220
X = lambda px: round((px - 8) / 3 * 4) / 4        # px a unidades (3 px = 1)
F = lambda py: round((py - 134) / 3)               # px a fila

def sim(l, color, x0, x1, f0, f1):
    # Pinta un rectángulo y su espejo respecto del eje (x0 < x1 del lado izquierdo, en px).
    l.rect(color, X(x0), X(x1), f0, f1)
    l.rect(color, X(2 * EJE - x1), X(2 * EJE - x0), f0, f1)

def y_fila(f): return 134 + f * 3 + 1.5

def adorno(l, cx, ancho, y0, y1):
    # Dragón o llama de la cumbrera: lomo ancho abajo y tres puntas que suben (la del medio, más alta).
    f0, f1 = F(y0), F(y1)
    l.rect('ha-adorno', X(cx - ancho / 2), X(cx + ancho / 2), f1 - 2, f1)
    for k, alto in ((-1, 0.6), (0, 1), (1, 0.6)):
        px = cx + k * ancho / 3
        fa = f1 - 2 - round((f1 - 2 - f0) * alto)
        for f in range(fa, f1 - 2):
            t = (f - fa + 1) / (f1 - 2 - fa)
            w = ancho / 7 * t + 1
            l.rect('ha-adorno', X(px - w), X(px + w), f, f + 1)
        l.rect('ha-adorno', X(px + 2), X(px + 4), fa + 1, fa + 2)        # rulo

def alero(x):
    # Borde de abajo de las tejas: más alto en el medio, cae hacia las puntas.
    return 205 + 11 * (abs(x - EJE) / 150) ** 1.5

def tablero(x):
    # Borde de arriba del tablero: apenas arqueado.
    return 256 + 8 * ((x - EJE) / 150) ** 2

def version():
    l = Lienzo(X(432), F(378))
    # Muros rojos de las orillas, con su techito gris.
    sim(l, 'ha-muro', 24, 74, F(222), F(318))
    sim(l, 'ha-muro-o', 24, 74, F(292), F(318))
    # Techito japonés sobre cada muro: cumbrera con calado, tejas con juntas, alero gris y puntas levantadas.
    sim(l, 'ha-cumbre', 30, 70, F(196), F(202))
    for x in range(33, 68, 6): sim(l, 'ha-calado', x, x + 3, F(198), F(200))
    for f in range(F(202), F(219)):
        y = y_fila(f)
        x0 = 30 - (y - 202) * 0.6
        for x in range(int(x0), 74):
            junta = (x + (3 if (int(y) // 6) % 2 else 0)) % 6 < 2
            sim(l, 'ha-teja-o' if junta else 'ha-teja', x, x + 1, f, f + 1)
    sim(l, 'ha-cumbre', 18, 74, F(219), F(223))
    sim(l, 'ha-calado', 14, 20, F(210), F(222))
    sim(l, 'ha-calado', 11, 17, F(210), F(213))
    sim(l, 'ha-calado', 26, 32, F(188), F(202))
    sim(l, 'ha-calado', 23, 29, F(188), F(191))
    adorno(l, 50, 22, 186, 196)
    adorno(l, 390, 22, 186, 196)
    # Canal: orillas de piedra, pasto y el agua con reflejos.
    sim(l, 'ha-orilla', 20, 92, F(318), F(352))
    for f in range(F(318), F(352)):
        for x in range(20 + (f % 2) * 8, 92, 16): sim(l, 'ha-orilla-o', x, x + 2, f, f + 1)
    sim(l, 'ha-pasto', 20, 112, F(352), F(360))
    l.rect('ha-agua', X(92), X(348), F(318), F(378))
    sim(l, 'ha-orilla', 20, 70, F(360), F(378))
    sim(l, 'ha-agua', 70, 112, F(360), F(378))
    # Techo: tejas naranjas con las juntas oscuras en vertical, tramo del medio más alto.
    for f in range(F(170), F(218)):
        y = y_fila(f)
        borde = 168 if y < 184 else 72 - (y - 184) * 0.12
        for x in range(int(borde), int(2 * EJE - borde), 1):
            if y > alero(x): continue
            junta = (x - EJE + (3 if (int(y) // 6) % 2 else 0)) % 6 < 2
            c = 'ha-teja-o' if junta else 'ha-teja'
            if y > alero(x) - 3: c = 'ha-cumbre'
            l.rect(c, X(x), X(x + 1), f, f + 1)
    # Cumbreras: el tramo alto y los dos laterales, con calado claro y las puntas levantadas.
    l.rect('ha-cumbre', X(172), X(268), F(164), F(173))
    for x in range(176, 266, 6): l.rect('ha-calado', X(x), X(x + 3), F(167), F(170))
    sim(l, 'ha-cumbre', 80, 168, F(176), F(185))
    for x in range(84, 164, 6): sim(l, 'ha-calado', x, x + 3, F(179), F(182))
    for x0, y0 in ((166, 152), (74, 166)):
        sim(l, 'ha-calado', x0, x0 + 6, F(y0), F(y0 + 18))
        sim(l, 'ha-calado', x0 - 3, x0 + 3, F(y0), F(y0 + 4))
    # Adornos sobre las cumbreras: tres en el tramo alto, uno largo en cada lateral.
    for cx in (186, EJE, 254): adorno(l, cx, 22, 146, 164)
    adorno(l, 100, 34, 160, 177); adorno(l, 340, 34, 160, 177)
    # Galería: oscura, con la viga, los postes y sus faroles redondos.
    for f in range(F(205), F(262)):
        y = y_fila(f)
        for x in range(72, 2 * EJE - 72):
            if y > alero(x): l.rect('ha-sombra', X(x), X(x + 1), f, f + 1)
    sim(l, 'ha-viga', 72, 220, F(222), F(226))
    sim(l, 'ha-viga', 72, 220, F(236), F(238))
    for x in (114, 164):
        sim(l, 'ha-poste', x - 3, x + 3, F(226), F(262))
        for f in range(F(224), F(236)):
            t = (y_fila(f) - 230) / 6
            w = 5 * math.sqrt(max(0, 1 - t * t))
            sim(l, 'ha-farol', x - w, x + w, f, f + 1)
    # Baranda: pasamanos y tablillas.
    sim(l, 'ha-baranda', 72, 220, F(242), F(245))
    for x in range(74, 218, 5):
        if not any(abs(x - p) < 5 for p in (114, 164)): sim(l, 'ha-baranda', x, x + 2, F(245), F(262))
    # Tablero de piedra arqueado, con el canto oscuro y la placa del medio.
    for f in range(F(250), F(292)):
        y = y_fila(f)
        for x in range(70, 2 * EJE - 70):
            t = tablero(x)
            if t <= y < t + 26: l.rect('ha-piedra-o' if y > t + 21 else 'ha-piedra', X(x), X(x + 1), f, f + 1)
    l.rect('ha-placa', X(192), X(248), F(262), F(267))
    # Pilas y arcos: huecos oscuros con arco redondo, el del medio más ancho y con el canal al fondo.
    sim(l, 'ha-pila', 72, 220, F(282), F(358))
    for f in range(F(282), F(358)):
        if f % 3 == 0: sim(l, 'ha-pila-o', 72, 220, f, f + 1)
    for x0, x1 in ((82, 105), (127, 155)):
        r = (x1 - x0) / 2
        cx = (x0 + x1) / 2
        for f in range(F(288), F(358)):
            y = y_fila(f)
            alto = 288 + r * 0.7
            w = r if y >= alto else r * math.sqrt(max(0, 1 - ((alto - y) / (r * 0.7)) ** 2))
            sim(l, 'ha-hueco', cx - w, cx + w, f, f + 1)
    # El vano del medio: recto bajo el tablero y hueco; abajo, el agua con reflejos.
    l.rect('ha-hueco', X(180), X(260), F(284), F(358))
    for f in range(F(358), F(378)):
        if f % 2: l.rect('ha-reflejo', X(200), X(240), f, f + 1)
    return {'nota': ('El puente japonés de Hoi An (Vietnam), de frente: los adornos de la cumbrera, el techo de tejas '
                     'naranjas con el tramo del medio más alto y las puntas levantadas, la galería oscura con sus postes, '
                     'faroles y baranda, el tablero de piedra apenas arqueado y las pilas con sus arcos sobre el canal, '
                     'entre los muros rojos de las orillas.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'ha-teja': ('#c8703f', '#c8703f'), 'ha-teja-o': ('#8a4a2c', '#8a4a2c'), 'ha-cumbre': ('#6c767a', '#6c767a'),
    'ha-calado': ('#d9d6cc', '#d9d6cc'), 'ha-adorno': ('#3f6e78', '#4f8590'), 'ha-sombra': ('#2a2420', '#2a2420'),
    'ha-viga': ('#5e3f2c', '#5e3f2c'), 'ha-poste': ('#6b4a36', '#6b4a36'), 'ha-farol': ('#ece6d6', '#ece6d6'),
    'ha-baranda': ('#a29a8c', '#a29a8c'), 'ha-piedra': ('#9aa09a', '#9aa09a'), 'ha-piedra-o': ('#62665f', '#62665f'),
    'ha-placa': ('#6e3a2a', '#6e3a2a'), 'ha-pila': ('#5a5e57', '#5a5e57'), 'ha-pila-o': ('#464943', '#464943'),
    'ha-hueco': ('#1f2220', '#1f2220'), 'ha-agua': ('#2e3b2e', '#2e3b2e'),
    'ha-reflejo': ('#55683f', '#55683f'), 'ha-muro': ('#9b2f2a', '#9b2f2a'), 'ha-muro-o': ('#77231f', '#77231f'),
    'ha-orilla': ('#7a7466', '#7a7466'), 'ha-orilla-o': ('#5a5549', '#5a5549'), 'ha-pasto': ('#7d8a4a', '#7d8a4a'),
}

p = version()
p.update(placa='infra-jade', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='infra-jade-marco')
COLORES.update({'infra-jade': ('#9fb58e', '#1c2a1e'), 'infra-jade-marco': ('#604a71', '#e3d5e1')})
guardar(sys.argv[1], 'programas', 'Infraestructura', p, COLORES, 'ha-|infra-jade')
print(len(p['lineas']), 'líneas, largo', p['largo'])
