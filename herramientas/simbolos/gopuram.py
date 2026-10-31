# Gopuram del templo Meenakshi (Madurai), para Templo, medido sobre referencias/simbolos/religioso/images (9).jpeg
# (495 px de ancho; la torre y la bóveda) y, para el basamento de piedra, images (10).jpeg pasada a la misma escala.
# De frente y simétrico sobre el eje x = 257. Líneas horizontales sin separación: los remates dorados, la bóveda de
# cañón con sus cabezas en las puntas y los medallones, nueve pisos que se angostan hacia arriba (cada uno con su
# cornisa, la fila de pabellones y las figuras de colores entre pilastras, con la abertura oscura en el medio) y el
# basamento de granito con la puerta.
# Uso: gopuram.py <simbolos.json> (pone programas.Templo).
import sys, math
from armar import Lienzo, guardar

EJE = 257
X = lambda px: round((px - 30) / 4 * 4) / 4        # px a unidades (4 px = 1)
F = lambda py: round((py - 30) / 4)                # px a fila

def sim(l, color, x0, x1, f0, f1):
    # Pinta un rectángulo y su espejo respecto del eje (x0 < x1 del lado izquierdo, en px).
    l.rect(color, X(x0), X(x1), f0, f1)
    l.rect(color, X(2 * EJE - x1), X(2 * EJE - x0), f0, f1)

def medio(py):
    # Medio ancho de la torre a la altura py: de 125 px arriba (y = 118) a 222 px abajo (y = 600).
    return 125 + (py - 118) / (600 - 118) * 97

FIGURAS = ('gp-rosa', 'gp-ocre', 'gp-verde', 'gp-crema', 'gp-azul', 'gp-rojo')

def piso(l, n, y0, y1):
    # Un piso de y0 a y1: cornisa, fila de pabellones y figuras entre pilastras; abertura oscura en el medio.
    w = medio((y0 + y1) / 2)
    f0, f1 = F(y0), F(y1)
    l.rect('gp-turquesa', X(EJE - w), X(EJE + w), f0, f1)
    # Cornisa saliente: canto claro, sombra debajo.
    l.rect('gp-crema', X(EJE - w - 5), X(EJE + w + 5), f0, f0 + 1)
    l.rect('gp-ocre', X(EJE - w - 4), X(EJE + w + 4), f0 + 1, f0 + 2)
    l.rect('gp-sombra', X(EJE - w), X(EJE + w), f0 + 2, f0 + 3)
    # Pabellones (cupulitas) sobre la cornisa: bloques rosa y turquesa alternados, de a 12 px desde el eje.
    k = 0
    while 6 + 12 * k + 8 <= w:
        x = EJE + 6 + 12 * k
        c = 'gp-rosa' if k % 2 else 'gp-verde'
        sim(l, c, 2 * EJE - x - 8, 2 * EJE - x, f0 + 3, f0 + 5)
        sim(l, 'gp-oro', 2 * EJE - x - 5, 2 * EJE - x - 3, f0 + 3, f0 + 4)
        k += 1
    l.rect('gp-azul', X(EJE - w), X(EJE + w), f0 + 5, f0 + 6)
    # Figuras entre pilastras: nichos de 12 px (pilastra de 3 px y figura con cabeza, cuerpo y peana).
    a, b = f0 + 6, f1 - 1
    k = 0
    while 6 + 12 * k + 12 <= w + 2:
        x = EJE + 6 + 12 * k                                         # borde izquierdo del nicho, lado derecho
        sim(l, 'gp-azul', 2 * EJE - x - 3, 2 * EJE - x, a, b)          # pilastra
        sim(l, 'gp-nicho', 2 * EJE - x - 12, 2 * EJE - x - 3, a, b)    # fondo del nicho
        c = FIGURAS[(k + n) % len(FIGURAS)]
        h = a + 1 + (k + n) % 2                                       # alternan paradas y sentadas
        sim(l, c, 2 * EJE - x - 9, 2 * EJE - x - 6, h, h + 1)          # cabeza
        sim(l, c, 2 * EJE - x - 11, 2 * EJE - x - 4, h + 1, b - 1)     # cuerpo
        sim(l, 'gp-ocre', 2 * EJE - x - 12, 2 * EJE - x - 3, b - 1, b) # peana
        k += 1
    l.rect('gp-turquesa', X(EJE - w), X(EJE + w), f1 - 1, f1)
    # Salientes que se apilan piso sobre piso (a 66 y 150 px del eje): marco ocre, techito rosa y nicho oscuro.
    for d in (66, 150):
        if d + 12 > w: continue
        sim(l, 'gp-ocre', EJE - d - 11, EJE - d + 11, f0 + 3, b)
        sim(l, 'gp-rosa', EJE - d - 7, EJE - d + 7, f0 + 3, f0 + 4)
        sim(l, 'gp-rosa', EJE - d - 9, EJE - d + 9, f0 + 4, f0 + 6)
        sim(l, 'gp-turquesa', EJE - d - 8, EJE - d + 8, f0 + 6, b - 1)
        sim(l, 'gp-sombra', EJE - d - 4, EJE - d + 4, f0 + 7, b - 1)
        sim(l, FIGURAS[(n + d // 66) % len(FIGURAS)], EJE - d - 2, EJE - d + 2, f0 + 8, b - 1)
    # El eje: pilastras doradas y la abertura oscura (en los pisos de abajo, más alta).
    l.rect('gp-oro', X(EJE - 9), X(EJE + 9), a, b)
    l.rect('gp-sombra', X(EJE - 5), X(EJE + 5), a + (1 if n < 4 else 2), b)

def version():
    l = Lienzo(X(490), F(670))
    # Remates dorados (kalasam): once, de 16.5 px, con punta, bulbo y collar.
    for i in range(11):
        cx = 175 + i * 16.5
        l.rect('gp-oro', X(cx) - 0.25, X(cx) + 0.25, F(38), F(46))
        l.rect('gp-oro', X(cx - 3), X(cx + 3), F(46), F(58))
        l.rect('gp-oro-o', X(cx), X(cx + 3), F(46), F(58))
        l.rect('gp-oro-o', X(cx - 4), X(cx + 4), F(58), F(62))
        l.rect('gp-oro', X(cx - 2), X(cx + 2), F(62), F(70))
    # Bóveda de cañón: cumbrera turquesa, cara rosada con rombos, friso verde abajo.
    l.rect('gp-turquesa', X(140), X(374), F(66), F(72))
    for f in range(F(72), F(100)):
        l.rect('gp-boveda', X(140), X(374), f, f + 1)
        for x in range(140 + (f % 2) * 6, 374, 12):
            l.rect('gp-boveda-o', X(x), X(x + 4), f, f + 1)
    l.rect('gp-verde', X(140), X(374), F(100), F(112))
    l.rect('gp-crema', X(132), X(382), F(112), F(118))
    # Medallones (kudu): uno grande en el medio y dos chicos, aro dorado con el centro oscuro.
    for cx, r in ((EJE, 18), (EJE - 70, 12), (EJE + 70, 12)):
        f0, f1 = F(80 - (r - 12)), F(112)
        for f in range(f0, f1):
            t = (f + 0.5 - f0) / (f1 - f0)
            wr = r * math.sqrt(max(0.15, 1 - (1 - t) ** 2))
            l.rect('gp-oro', X(cx - wr), X(cx + wr), f, f + 1)
            if f0 < f < f1 - 1: l.rect('gp-sombra', X(cx - wr) + 1, X(cx + wr) - 1, f, f + 1)
    # Cabezas en las puntas: cuerno azul que sube por fuera y cara verde con ojo.
    for f in range(F(50), F(118)):
        y = 30 + f * 4
        w = 10 + (y - 50) * 0.18
        sim(l, 'gp-azul', 124, 124 + w, f, f + 1)
    sim(l, 'gp-verde', 128, 146, F(76), F(108))
    sim(l, 'gp-rojo', 134, 140, F(84), F(92))
    sim(l, 'gp-oro', 120, 128, F(96), F(118))
    # Los nueve pisos: más bajos arriba (44 px) que abajo (62 px).
    y = 118
    for n in range(9):
        alto = 44 + n * 18 / 8
        piso(l, 8 - n, y, y + alto)
        y += alto
    # Basamento de granito: cornisa, muro con pilastras, puerta con marco y zócalo con dos escalones.
    w = medio(600) - 6
    l.rect('gp-piedra-l', X(EJE - w - 4), X(EJE + w + 4), F(600), F(608))
    l.rect('gp-piedra-o', X(EJE - w), X(EJE + w), F(608), F(612))
    l.rect('gp-piedra', X(EJE - w), X(EJE + w), F(612), F(654))
    for x in range(int(EJE - w) + 6, EJE - 30, 24):
        sim(l, 'gp-piedra-l', x, x + 8, F(612), F(654))
        sim(l, 'gp-piedra-o', x + 8, x + 10, F(612), F(654))
    l.rect('gp-ocre', X(EJE - 24), X(EJE + 24), F(596), F(654))
    l.rect('gp-puerta', X(EJE - 18), X(EJE + 18), F(602), F(654))
    l.rect('gp-madera', X(EJE - 12), X(EJE + 12), F(620), F(654))
    l.rect('gp-puerta', X(EJE) - 0.25, X(EJE) + 0.25, F(620), F(654))
    l.rect('gp-piedra-o', X(EJE - w - 4), X(EJE + w + 4), F(654), F(662))
    l.rect('gp-piedra-l', X(EJE - w - 8), X(EJE + w + 8), F(662), F(670))
    return {'nota': ('Una torre de entrada de templo (gopuram), la del Meenakshi de Madurai, de frente: los remates dorados, '
                     'la bóveda de cañón con sus medallones y las cabezas de las puntas; nueve pisos que se angostan hacia arriba, '
                     'cada uno con su cornisa, la fila de pabellones y las figuras de colores entre pilastras, con la abertura '
                     'oscura en el eje; abajo, el basamento de granito con la puerta.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'gp-turquesa': ('#2f9a95', '#2f9a95'), 'gp-azul': ('#2d6aa8', '#2d6aa8'), 'gp-verde': ('#4f9348', '#4f9348'),
    'gp-rosa': ('#d77a78', '#d77a78'), 'gp-rojo': ('#b3423a', '#b3423a'), 'gp-ocre': ('#d4a03e', '#d4a03e'),
    'gp-crema': ('#ecdcb4', '#ecdcb4'), 'gp-nicho': ('#1f3f5c', '#1f3f5c'), 'gp-sombra': ('#25232b', '#25232b'),
    'gp-oro': ('#e6b53a', '#e6b53a'), 'gp-oro-o': ('#b5862a', '#b5862a'),
    'gp-boveda': ('#b7756a', '#b7756a'), 'gp-boveda-o': ('#94564e', '#94564e'),
    'gp-piedra': ('#b2a68f', '#b2a68f'), 'gp-piedra-l': ('#cbc0aa', '#cbc0aa'), 'gp-piedra-o': ('#8c8170', '#8c8170'),
    'gp-puerta': ('#231f1d', '#231f1d'), 'gp-madera': ('#6b4024', '#6b4024'),
}

p = version()
p.update(placa='templo-granito', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='templo-granito-marco')
guardar(sys.argv[1], 'programas', 'Templo', p, COLORES, 'gp-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
