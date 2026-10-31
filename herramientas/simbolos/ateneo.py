# Ateneo Rumano (Bucarest), para Beaux-Arts, medido sobre referencias/simbolos/ateneo rumano/images (2).jpeg
# (554 px de ancho; el pórtico y la cúpula) y, para las alas, romanian-athenaeum-bucharest-RO.jpg pasada a la misma
# escala. De frente y simétrico sobre el eje x = 272. Líneas horizontales sin separación: la aguja, la corona y la
# cúpula gris con sus nervios, el tambor con ojos de buey, el frontón, la cornisa con la inscripción, el pórtico de
# seis columnas jónicas con medallones y tres puertas de madera, las alas con sus rosetas y la escalinata.
# Uso: ateneo.py <simbolos.json> (pone estilos.Beaux-Arts).
import sys, math
from armar import Lienzo, guardar

EJE = 272
X = lambda px: round((px + 47) / 4 * 4) / 4        # px a unidades (4 px = 1)
F = lambda py: round((py - 48) / 4)                # px a fila

def sim(l, color, x0, x1, f0, f1):
    # Pinta un rectángulo y su espejo respecto del eje.
    l.rect(color, X(x0), X(x1), f0, f1)
    l.rect(color, X(2 * EJE - x1), X(2 * EJE - x0), f0, f1)

def columna(l, cx):
    l.rect('at-capitel-o', X(cx - 14), X(cx + 14), F(318), F(322))      # capitel con volutas
    l.rect('at-piedra', X(cx - 11), X(cx + 11), F(322), F(330))
    l.rect('at-capitel-o', X(cx - 14), X(cx - 10), F(322), F(330))
    l.rect('at-capitel-o', X(cx + 10), X(cx + 14), F(322), F(330))
    for x0, x1, c in ((-9, -6, 'at-sombra'), (-6, 1, 'at-luz'), (1, 5, 'at-piedra'), (5, 9, 'at-sombra')):
        l.rect(c, X(cx + x0), X(cx + x1), F(330), F(466))               # fuste redondo
    for x in (-4, 0, 3):                                                # estrías
        l.rect('at-sombra', X(cx + x), X(cx + x) + 0.25, F(334), F(462))
    l.rect('at-piedra', X(cx - 12), X(cx + 12), F(466), F(472))         # basa

def version():
    l = Lienzo(X(592), F(490))
    # La aguja, la linterna y la corona.
    l.rect('at-domo-o', X(EJE - 2), X(EJE + 2), F(50), F(80))
    l.rect('at-domo-l', X(EJE - 10), X(EJE + 10), F(80), F(100))
    l.rect('at-domo-o', X(EJE - 10), X(EJE + 10), F(92), F(96))
    for f in range(F(100), F(140)):                                     # la corona: ensancha hacia abajo con remates
        y = 48 + f * 4
        w = 22 + (y - 100) * 0.8
        l.rect('at-domo-o' if f % 3 == 0 else 'at-domo-l', X(EJE - w), X(EJE + w), f, f + 1)
    # La cúpula: media elipse gris con nervios.
    for f in range(F(140), F(186)):
        y = 48 + f * 4
        w = 140 * math.sqrt(max(0, 1 - ((186 - y) / 50) ** 2))
        w = max(w, 52)
        l.rect('at-domo', X(EJE - w), X(EJE + w), f, f + 1)
        l.rect('at-domo-o', X(EJE + w * 0.55), X(EJE + w), f, f + 1)
        for k in (0, 0.38, 0.71, 0.92):
            for s in (-1, 1):
                l.rect('at-domo-l' if s < 0 else 'at-domo-o', X(EJE + s * k * w) - 0.25, X(EJE + s * k * w) + 0.25, f, f + 1)
    # El tambor con su cornisa, pilastras y ojos de buey.
    l.rect('at-sombra', X(112), X(432), F(186), F(192))
    l.rect('at-piedra', X(112), X(432), F(192), F(200))
    l.rect('at-piedra', X(120), X(424), F(200), F(284))
    l.rect('at-sombra', X(120), X(134), F(200), F(284))
    l.rect('at-sombra', X(410), X(424), F(200), F(284))
    for dx, ancho in ((0, 30), (52, 28), (100, 20), (132, 10)):
        for s in ((1,) if dx == 0 else (-1, 1)):
            cx = EJE + s * dx
            f0, f1 = F(204), F(240)
            for f in range(f0, f1):                                 # redondo: aro de piedra y vidrio
                t = (f + 0.5 - (f0 + f1) / 2) / ((f1 - f0) / 2)
                w = ancho / 2 * math.sqrt(max(0, 1 - t * t))
                l.rect('at-capitel-o', X(cx - w), X(cx + w), f, f + 1)
                if f not in (f0, f1 - 1): l.rect('at-vidrio', X(cx - w) + 0.5, X(cx + w) - 0.5, f, f + 1)
    for dx in (26, 76, 118):                                            # pilastras entre los ojos
        sim(l, 'at-luz', EJE + dx - 3, EJE + dx + 3, F(200), F(284))
    # Frontón: la cornisa inclinada clara con su sombra, los dentículos, el tímpano y la ventanita con marco.
    for f in range(F(225), F(284)):
        y = 48 + f * 4
        w = (y - 225) / (284 - 225) * 164
        l.rect('at-luz', X(EJE - w), X(EJE + w), f, f + 1)
        if w > 10: l.rect('at-sombra', X(EJE - w + 7), X(EJE + w - 7), f, f + 1)
        if w > 18:
            d = 'at-luz' if f % 2 else 'at-capitel-o'
            l.rect(d, X(EJE - w + 10), X(EJE - w + 13), f, f + 1)
            l.rect(d, X(EJE + w - 13), X(EJE + w - 10), f, f + 1)
        if w > 24: l.rect('at-timpano', X(EJE - w + 16), X(EJE + w - 16), f, f + 1)
    l.rect('at-luz', X(EJE - 7), X(EJE + 7), F(262), F(278))
    l.rect('at-capitel-o', X(EJE - 4), X(EJE + 4), F(265), F(275))
    for x in (106, 438):                                                # acroteras en las puntas y arriba
        l.rect('at-capitel-o', X(x - 5), X(x + 5), F(268), F(282))
        l.rect('at-capitel-o', X(x - 3), X(x + 3), F(262), F(268))
    # Cornisa, friso con la inscripción y arquitrabe.
    l.rect('at-sombra', X(104), X(440), F(282), F(290))
    for i, x in enumerate(range(108, 436, 4)):                          # dentículos bajo la cornisa
        l.rect('at-luz' if i % 2 else 'at-capitel-o', X(x), X(x + 4), F(288), F(290))
    l.rect('at-piedra', X(108), X(436), F(290), F(312))
    l.rect('at-sombra', X(195), X(349), F(295), F(307))
    l.rect('at-luz', X(197), X(347), F(298), F(304))
    for i, x in enumerate(range(204, 340, 6)):
        if i % 6 != 5: l.rect('at-letra', X(x), X(x + 3), F(299), F(303))
    l.rect('at-sombra', X(108), X(436), F(312), F(318))
    # Alas: el techo de chapa a cuatro aguas que asoma, la cornisa saliente con su friso de dentículos, el ático
    # con tres rosetas entre pilastras, la faja, los capiteles con guirnalda y abajo cuatro pilastras con sillares,
    # cartelas y zócalo; en la punta, una pilastra doble que cierra el ala.
    for f in range(F(288), F(310)):
        y = 48 + f * 4
        k = (310 - y) / 22
        sim(l, 'at-domo' if f % 2 else 'at-domo-l', -30 + 40 * k, 100, f, f + 1)
    sim(l, 'at-luz', -46, 108, F(310), F(316))
    sim(l, 'at-sombra', -44, 106, F(316), F(320))
    sim(l, 'at-piedra', -40, 106, F(320), F(478))
    for i, x in enumerate(range(-40, 106, 4)):
        sim(l, 'at-luz' if i % 2 else 'at-capitel-o', x, x + 4, F(324), F(328))
    sim(l, 'at-sombra', -40, 106, F(332), F(336))
    for cx in (-40, 8, 56, 98):                                        # pilastras del ático
        sim(l, 'at-luz', cx, cx + 8, F(336), F(378))
    for cx in (-12, 32, 76):
        sim(l, 'at-piedra', cx - 13, cx + 13, F(343), F(373))
        sim(l, 'at-reja', cx - 11, cx + 11, F(345), F(371))            # roseta: reja oscura en estrella
        sim(l, 'at-piedra', cx - 11, cx + 11, F(345), F(347))
        sim(l, 'at-piedra', cx - 11, cx + 11, F(369), F(371))
        sim(l, 'at-piedra', cx - 11, cx - 9, F(345), F(371))
        sim(l, 'at-piedra', cx + 9, cx + 11, F(345), F(371))
        for r in range(F(347), F(369)):                                # la X de la reja
            t = (r - F(347) + 0.5) / (F(369) - F(347))
            sim(l, 'at-piedra', cx - 9 + 18 * t - 2, cx - 9 + 18 * t + 2, r, r + 1)
            sim(l, 'at-piedra', cx + 9 - 18 * t - 2, cx + 9 - 18 * t + 2, r, r + 1)
    sim(l, 'at-luz', -44, 106, F(378), F(382))
    sim(l, 'at-sombra', -42, 106, F(382), F(386))
    for i, x in enumerate(range(-40, 106, 6)):                          # guirnalda de los capiteles
        sim(l, 'at-capitel-o' if i % 2 else 'at-panel', x, x + 6, F(388), F(394))
    for f in range(F(398), F(470), 3):                                  # sillares
        sim(l, 'at-panel', -40, 106, f, f + 1)
    for cx in (-40, 8, 56, 98):
        sim(l, 'at-luz', cx, cx + 8, F(386), F(470))
        sim(l, 'at-piedra', cx - 1, cx + 9, F(386), F(392))
    for cx in (-16, 32, 77):                                            # cartelas
        sim(l, 'at-capitel-o', cx - 7, cx + 7, F(410), F(414))
        sim(l, 'at-capitel-o', cx - 4, cx + 4, F(414), F(420))
    sim(l, 'at-sombra', -44, -38, F(310), F(478))                       # la punta: pilastra doble
    sim(l, 'at-luz', -38, -30, F(336), F(470))
    sim(l, 'at-sombra', -44, 106, F(470), F(474))
    sim(l, 'at-luz', -46, 108, F(474), F(478))
    # Los tramos de unión, con su ventana alta.
    sim(l, 'at-piedra', 104, 122, F(300), F(478))
    sim(l, 'at-vidrio', 109, 119, F(342), F(440))
    # El pórtico: muro en sombra, medallones dorados y tres puertas de madera.
    l.rect('at-muro', X(120), X(424), F(318), F(472))
    for dx in (0, 52, 104):
        for s in ((1,) if dx == 0 else (-1, 1)):
            cx = EJE + s * dx
            l.rect('at-oro', X(cx - 7), X(cx + 7), F(347), F(349))
            l.rect('at-oro', X(cx - 9), X(cx + 9), F(349), F(363))
            l.rect('at-oro', X(cx - 7), X(cx + 7), F(363), F(365))
            l.rect('at-bronce', X(cx - 4), X(cx + 4), F(351), F(361))
    for cx in (EJE - 50, EJE, EJE + 50):
        l.rect('at-piedra', X(cx - 17), X(cx + 17), F(388), F(472))
        l.rect('at-vidrio', X(cx - 13), X(cx + 13), F(394), F(418))
        l.rect('at-madera', X(cx - 13), X(cx + 13), F(418), F(472))
        l.rect('at-madera-o', X(cx) - 0.25, X(cx) + 0.25, F(418), F(472))
    for cx in (142, 194, 246):
        columna(l, cx)
        columna(l, 2 * EJE - cx)
    # Escalinata.
    for i, f in enumerate(range(F(472), F(490))):
        l.rect('at-sombra' if i % 2 else 'at-luz', X(-40), X(584), f, f + 1)
    return {'nota': ('El Ateneo Rumano (Bucarest), de frente y simétrico: la aguja, la corona y la cúpula gris con sus nervios; '
                     'el tambor con ojos de buey; el frontón y la cornisa con la inscripción; el pórtico de seis columnas jónicas '
                     'con medallones dorados y tres puertas de madera; a los lados, las alas con sus rosetas, y la escalinata.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'at-piedra': ('#ecdcc4', '#ecdcc4'), 'at-luz': ('#f7ecdb', '#f7ecdb'), 'at-sombra': ('#cdb699', '#cdb699'),
    'at-muro': ('#c9b08f', '#c9b08f'), 'at-capitel-o': ('#b39b7c', '#b39b7c'), 'at-panel': ('#e3d0b5', '#e3d0b5'), 'at-timpano': ('#e6d4ba', '#e6d4ba'),
    'at-reja': ('#6d5c48', '#6d5c48'), 'at-vidrio': ('#3e4a52', '#3e4a52'), 'at-letra': ('#9c8466', '#9c8466'),
    'at-domo': ('#68717b', '#68717b'), 'at-domo-o': ('#4a525b', '#4a525b'), 'at-domo-l': ('#8d969f', '#8d969f'),
    'at-oro': ('#c9a04f', '#c9a04f'), 'at-bronce': ('#6e5532', '#6e5532'),
    'at-madera': ('#9a5a2a', '#9a5a2a'), 'at-madera-o': ('#4a2a14', '#4a2a14'),
}

p = version()
p.update(placa='beaux-bordo', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='beaux-bordo-marco')
COLORES.update({'beaux-bordo': ('#6e2a35', '#2a1015'), 'beaux-bordo-marco': ('#91d5ca', '#d5efea')})
guardar(sys.argv[1], 'estilos', 'Beaux-Arts', p, COLORES, 'at-|beaux-bordo')
print(len(p['lineas']), 'líneas, largo', p['largo'])
