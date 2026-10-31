# Casa victoriana de San Francisco (Vivienda unifamiliar), medida sobre referencias/simbolos/residencial/images.jpeg
# (437 px de ancho), de frente. Líneas horizontales sin separación: los dos techos de tejas, uno de cumbrera plana y otro con pico, y la torre cónica
# con remate, la chimenea, el alero, el friso rojo y blanco, la planta alta de tejuelas azules (en rombos) con la
# ventana y el balcón a la izquierda y la ventana saliente de tres paños a la derecha, los frontones, la guirnalda,
# la planta baja de tablas azules con el ventanal, la ventanita y la saliente, los paneles, el basamento con la
# escalera y los canteros.
# Uso: casa.py <simbolos.json> (pone programas.Vivienda unifamiliar).
import sys
from armar import Lienzo, guardar

X = lambda px: round((px - 35) / 4 * 4) / 4        # px a unidades (4 px = 1)
F = lambda py: round((py - 10) / 4)                # px a fila

def triangulo(l, color, x0, x1, y_pico, y_base, x_pico=None, hilada=None):
    # Triángulo lleno: un pico arriba y la base abajo, fila por fila (con `hilada`, una fila de ese color cada cuatro).
    xp = (x0 + x1) / 2 if x_pico is None else x_pico
    f0, f1 = F(y_pico), F(y_base)
    for f in range(f0, f1):
        t = (f - f0 + 1) / (f1 - f0)
        l.rect(hilada if hilada and f % 4 == 0 else color, X(xp - (xp - x0) * t), X(xp + (x1 - xp) * t), f, f + 1)

def ventana(l, x0, x1, y0, y1, hojas=1):
    # Marco blanco, vidrio oscuro y el travesaño de la guillotina.
    l.rect('cv-blanco', X(x0), X(x1), F(y0), F(y1))
    l.rect('cv-vidrio', X(x0) + 0.75, X(x1) - 0.75, F(y0) + 1, F(y1) - 1)
    l.rect('cv-blanco', X(x0), X(x1), (F(y0) + F(y1)) // 2, (F(y0) + F(y1)) // 2 + 1)
    for k in range(1, hojas):
        x = X(x0 + (x1 - x0) * k / hojas)
        l.rect('cv-blanco', x - 0.25, x + 0.25, F(y0), F(y1))

def tejuelas(l, x0, x1, y0, y1):
    # Tejuelas en rombos: filas que alternan el tono, corridas medio paso.
    for f in range(F(y0), F(y1)):
        l.rect('cv-azul', X(x0), X(x1), f, f + 1)
        x = X(x0) + (0.75 if f % 2 else 0)
        while x < X(x1):
            l.rect('cv-azul-o', x, min(x + 0.5, X(x1)), f, f + 1)
            x += 1.5

def tablas(l, x0, x1, y0, y1):
    # Tablas horizontales: una fila oscura cada tres.
    for f in range(F(y0), F(y1)):
        l.rect('cv-azul-o' if f % 3 == 2 else 'cv-azul', X(x0), X(x1), f, f + 1)

def friso(l, x0, x1, y0, y1, paso):
    # Friso rojo con roleos blancos.
    l.rect('cv-rojo', X(x0), X(x1), F(y0), F(y1))
    x = X(x0) + paso / 2
    for f in range(F(y0) + 1, F(y1) - 1):
        xx = x + (0.5 if f % 2 else 0)
        while xx + 1 < X(x1):
            l.rect('cv-blanco', xx, xx + 1, f, f + 1)
            xx += paso

def version():
    l = Lienzo(X(400), F(622))
    # Techos: dos a la izquierda (uno de cumbrera plana con su remate y, delante, uno a cuatro aguas con pico y un
    # piquito al costado), la chimenea y la torre cónica con su aguja.
    l.rect('cv-ladrillo', X(330), X(352), F(95), F(150))
    l.rect('cv-techo-o', X(93), X(97), F(55), F(77))
    for f in range(F(77), F(172)):                              # el de cumbrera plana
        y = 10 + f * 4
        izq = 92 if y < 140 else 92 - (y - 140) / 32 * 50
        l.rect('cv-techo-o' if f % 4 == 0 else 'cv-techo', X(izq), X(260), f, f + 1)
    triangulo(l, 'cv-techo-2', 215, 255, 58, 90, x_pico=233, hilada='cv-techo-o')   # el piquito
    for f in range(F(47), F(172)):                              # el del pico, con su lima oscura a la izquierda
        y = 10 + f * 4
        borde = 92 if y < 140 else 92 - (y - 140) / 32 * 50          # no pasarse del borde del otro techo
        izq, der = max(212 - (y - 47) * 1.23, borde), 212 + (y - 47) * 1.5
        l.rect('cv-techo-o' if f % 4 == 0 else 'cv-techo-2', X(izq), X(der), f, f + 1)
        l.rect('cv-techo-o', X(izq), X(izq) + 0.5, f, f + 1)
    triangulo(l, 'cv-techo-l', 212, 370, 50, 172, x_pico=289, hilada='cv-techo-o')
    for f in range(F(50), F(172)):                              # el borde izquierdo del cono
        x = 289 - (289 - 212) * (f - F(50) + 1) / (F(172) - F(50))
        l.rect('cv-techo-o', X(x), X(x) + 0.5, f, f + 1)
    l.rect('cv-blanco', X(287), X(291), F(18), F(52))           # la aguja
    l.rect('cv-blanco', X(285), X(293), F(30), F(36))
    # Alero y friso.
    l.rect('cv-azul-o', X(45), X(395), F(172), F(186))
    friso(l, 55, 362, 186, 212, 2.5)
    # Planta alta: tejuelas, ventana y balcón a la izquierda, saliente de tres paños a la derecha.
    tejuelas(l, 58, 362, 212, 322)
    ventana(l, 88, 142, 216, 305)
    for x0, x1 in ((220, 228), (258, 268), (312, 322), (352, 362)):  # pilastras de la saliente
        l.rect('cv-blanco', X(x0), X(x1), F(212), F(322))
    for x0, x1 in ((228, 258), (268, 312), (322, 352)):
        ventana(l, x0, x1, 220, 305)
    l.rect('cv-blanco', X(62), X(156), F(298), F(302))          # el balcón: pasamanos, balaustres y piso
    for px in range(66, 156, 6):
        l.rect('cv-blanco', X(px), X(px) + 0.5, F(302), F(318))
    l.rect('cv-blanco', X(60), X(158), F(318), F(322))
    # Faja con los dos frontones y la guirnalda roja.
    l.rect('cv-azul-o', X(56), X(364), F(322), F(338))
    for x0, x1 in ((70, 152), (246, 336)):
        triangulo(l, 'cv-blanco', x0, x1, 310, 336)
        triangulo(l, 'cv-ocre', x0 + 14, x1 - 14, 318, 333)
    l.rect('cv-blanco', X(56), X(364), F(336), F(344))
    friso(l, 62, 156, 344, 360, 3)
    friso(l, 218, 358, 344, 360, 3)
    l.rect('cv-azul', X(156), X(218), F(344), F(360))
    # Planta baja: tablas azules, ventanal a la izquierda con la puerta de madera adentro, ventanita y saliente.
    tablas(l, 58, 362, 360, 498)
    l.rect('cv-blanco', X(62), X(156), F(360), F(478))
    l.rect('cv-madera', X(74), X(146), F(368), F(470))
    for px in (88, 110, 132):
        l.rect('cv-madera-o', X(px), X(px) + 1, F(395), F(468))
    l.rect('cv-blanco', X(74), X(146), F(390), F(392))
    l.rect('cv-blanco', X(170), X(210), F(372), F(422))
    l.rect('cv-vidrio', X(174), X(206), F(376), F(418))
    for x0, x1 in ((218, 226), (258, 268), (312, 322), (354, 362)):
        l.rect('cv-blanco', X(x0), X(x1), F(360), F(478))
    for x0, x1 in ((226, 258), (268, 312), (322, 354)):
        ventana(l, x0, x1, 366, 470)
    # Paneles bajo las ventanas, con el rombo.
    for x0, x1 in ((62, 156), (218, 362)):
        l.rect('cv-azul-o', X(x0), X(x1), F(478), F(498))
        l.rect('cv-blanco', X(x0) + 1, X(x1) - 1, F(482), F(494))
        l.rect('cv-azul', X(x0) + 1.5, X(x1) - 1.5, F(483), F(493))
    l.rect('cv-ocre', X(105), X(113), F(484), F(492))
    l.rect('cv-blanco', X(56), X(364), F(498), F(504))
    # Basamento oscuro con la escalera al medio y los canteros a los lados.
    l.rect('cv-base', X(58), X(362), F(504), F(580))
    # La escalera: un tramo de frente abajo y, arriba, el tramo que gira hacia la puerta, de costado, tapado por el
    # panel calado azul con la baranda negra encima; el poste, la baranda de la derecha y los dos escalones de la vereda.
    for f in range(F(500), F(588)):
        y = 10 + f * 4
        d = 150 + (y - 500)                                      # la diagonal del tramo de arriba
        if y < 545:
            l.rect('cv-escalon-o' if f % 3 == 2 else 'cv-escalon', X(d), X(d + 14), f, f + 1)
        l.rect('cv-celosia', X(150), X(min(d, 192)), f, f + 1)
        if y < 545: l.rect('cv-hierro', X(d) - 0.25, X(d) + 0.5, f, f + 1)
    for f in range(F(542), F(588)):
        k = (f - F(542)) % 3
        l.rect(('cv-escalon-l', 'cv-escalon', 'cv-escalon-o')[k], X(194), X(256), f, f + 1)
    l.rect('cv-hierro', X(189), X(193), F(490), F(588))         # el poste
    for f in range(F(452), F(492)):                              # y su pasamanos, que sube en diagonal hasta la puerta
        x = 191 - (490 - (10 + f * 4))
        l.rect('cv-hierro', X(x) - 0.25, X(x) + 0.75, f, f + 1)
    l.rect('cv-hierro', X(256), X(261), F(535), F(588))         # la baranda de la derecha
    l.rect('cv-base', X(40), X(400), F(586), F(598))           # el murete de los canteros
    l.rect('cv-arena', X(184), X(264), F(598), F(610))
    l.rect('cv-arena-o', X(170), X(278), F(610), F(622))
    # Canteros con matas que suben y bajan: hortensias blancas a la izquierda, flores rojas y rosas a la derecha.
    import math
    for x0, x1, flores in ((45, 148, ('cv-flor', 'cv-flor', 'cv-flor-r')), (266, 400, ('cv-flor-r', 'cv-flor-p', 'cv-flor-r'))):
        x = x0
        while x < x1:
            alto = 540 + 9 * math.sin(x / 11) + 3 * math.sin(x / 5)
            l.rect('cv-verde', X(x), X(x + 2), F(alto), F(586))
            l.rect('cv-verde-o', X(x), X(x + 2), F(alto) + 4, F(586))
            x += 2
        for i, px in enumerate(range(x0 + 4, x1 - 8, 13)):      # ramilletes redondos
            py = 552 + 9 * math.sin(px / 11)
            c = flores[i % 3]
            l.rect(c, X(px) + 0.5, X(px + 8) - 0.5, F(py), F(py) + 1)
            l.rect(c, X(px), X(px + 8), F(py) + 1, F(py) + 4)
            l.rect(c, X(px) + 0.5, X(px + 8) - 0.5, F(py) + 4, F(py) + 5)
    return {'nota': ('Una casa victoriana de San Francisco, de frente: los dos techos de tejas, uno de cumbrera plana y otro con pico, y la torre cónica con su '
                     'aguja, la chimenea, el alero y el friso rojo con roleos blancos; la planta alta de tejuelas azules con la '
                     'ventana y el balcón de un lado y la saliente de tres paños del otro; los frontones y la guirnalda; la '
                     'planta baja de tablas azules con el ventanal de la puerta de madera; el basamento con la escalera que sube de frente y gira hacia la puerta detrás de un panel calado, y los canteros con flores.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'cv-azul': ('#3f5f8f', '#3f5f8f'), 'cv-azul-o': ('#2c4268', '#2c4268'), 'cv-blanco': ('#ece7dc', '#ece7dc'),
    'cv-vidrio': ('#cdbf9c', '#cdbf9c'), 'cv-rojo': ('#9a2a35', '#9a2a35'), 'cv-ocre': ('#c9a45c', '#c9a45c'),
    'cv-techo': ('#7a5a44', '#7a5a44'), 'cv-techo-o': ('#5e4434', '#5e4434'), 'cv-techo-l': ('#8f6d52', '#8f6d52'), 'cv-techo-2': ('#84624a', '#84624a'),
    'cv-ladrillo': ('#8a4a36', '#8a4a36'), 'cv-madera': ('#7a4a2a', '#7a4a2a'), 'cv-madera-o': ('#4e2e1a', '#4e2e1a'),
    'cv-base': ('#2a3a57', '#2a3a57'), 'cv-escalon': ('#d6cdbb', '#d6cdbb'), 'cv-escalon-o': ('#a49b8a', '#a49b8a'), 'cv-hierro': ('#1d2230', '#1d2230'),
    'cv-arena': ('#c4a676', '#c4a676'), 'cv-escalon-l': ('#e8e1d2', '#e8e1d2'), 'cv-verde': ('#4a7a3f', '#4a7a3f'), 'cv-verde-o': ('#2f5530', '#2f5530'),
    'cv-flor': ('#efeaf0', '#efeaf0'), 'cv-flor-r': ('#c43a4c', '#c43a4c'), 'cv-flor-p': ('#e58aa6', '#e58aa6'),
    'cv-celosia': ('#34507e', '#34507e'), 'cv-arena-o': ('#a88d62', '#a88d62'),
}

p = version()
p.update(placa='casa-mandarina', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='casa-mandarina-marco')
COLORES.update({'casa-mandarina': ('#e8955a', '#40220f'), 'casa-mandarina-marco': ('#176aa5', '#bfddf0')})
guardar(sys.argv[1], 'programas', 'Vivienda unifamiliar', p, COLORES, 'cv-|casa-mandarina')
print(len(p['lineas']), 'líneas, largo', p['largo'])
