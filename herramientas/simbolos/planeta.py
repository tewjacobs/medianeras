# Edificio El Planeta (Atlántida, Uruguay), de frente, dibujado sobre referencias/simbolos/el planeta/: el "barco"
# del Streamline. A la derecha, la punta redonda con las cubiertas que se escalonan hacia adentro al subir (sombreadas
# como cilindro, luz desde la izquierda), ventanas que se angostan en la curva y barandas de caño en lo que queda al
# aire; arriba, el cuarto redondo, el plato y el faro con su ojo. A la izquierda, el cuerpo largo: cada piso es una faja
# de balcón y un muro metido con ventanas iguales, capotas claras y algún toldo a rayas; chimeneas y tanques en la
# azotea. Abajo, el basamento, más ancho que las cubiertas en la curva, con líneas de velocidad, la entrada de toldos y
# el pilar con ojo; el seto, la palmera, el cartel azul y el pasto.
# Uso: planeta.py <simbolos.json> (pone estilos."Streamline Moderne").
import sys
from armar import Lienzo, guardar

LARGO, FILAS = 162, 96
C = 104                                              # eje de la punta redonda (faro, plato, cuarto)
SOMBRAS = ('pl-s1', 'pl-s2', 'pl-s3')                # de la luz a la sombra, hacia la punta redonda
VENTANAS = list(range(12, LARGO, 7))                 # la misma grilla en todos los pisos

def redondo(l, a, b, f0, f1, cola=6, recorte=None):
    # Un volumen redondeado a la derecha (y apenas a la izquierda): claro, con la punta en sombra que se oscurece.
    recorte = recorte or {}
    for f in range(f0, f1):
        m = recorte.get(f - f0, recorte.get(f - f1, 0))
        l.rect('pl-blanco', a + m / 2, b - m, f, f + 1)
        paso = cola / len(SOMBRAS)
        for k, c in enumerate(SOMBRAS):
            x = b - cola + k * paso
            l.rect(c, x, min(x + paso, b - m), f, f + 1)

def faja(l, a, b, f):
    # La faja de un balcón (tres filas): canto de arriba, frente y panza en sombra; redondeada en las puntas.
    redondo(l, a, b, f, f + 3, cola=10, recorte={0: 1.5, -1: 1})
    l.rect('pl-canto', a + 0.75, b - 10, f, f + 1)                    # canto de arriba, con luz
    l.rect('pl-bajo', a + 0.5, b - 1.5, f + 2, f + 3)

def baranda(l, a, b, f):
    # Baranda de caño sobre una cubierta: el caño (fila f) y los parantes (fila f+1).
    l.rect('pl-cano', a, b, f, f + 1)
    x = a
    while x < b:
        l.rect('pl-cano', x, x + 0.25, f + 1, f + 2)
        x += 2

def ventana(l, x, f0, f1, ancho=3):
    l.rect('pl-vidrio', x, x + ancho, f0, f1)
    if ancho >= 2: l.rect('pl-marco', x + ancho / 2, x + ancho / 2 + 0.25, f0, f1)   # el parante del medio
    l.rect('pl-reflejo', x, x + min(1, ancho), f0, f0 + 1)                             # reflejo del cielo arriba

def piso(l, f, derecha, toldos):
    # El muro metido de un piso (siete filas): en sombra, con ventanas iguales, capotas y toldos a rayas;
    # en la curva, ventanas cada vez más angostas.
    redondo(l, 9, derecha, f, f + 7, cola=8)
    l.rect('pl-muro', 9, derecha - 8, f, f + 7)
    l.rect('pl-bajo', 9, derecha - 1, f, f + 1)                       # sombra de la faja de arriba
    for i, x in enumerate(VENTANAS):
        if x + 4 > derecha - 8: break
        ventana(l, x, f + 3, f + 7)
        if i in toldos:                                                # toldo a rayas
            for k in range(16):
                l.rect('pl-rojo' if k % 2 == 0 else 'pl-lona', x - 0.5 + k * 0.25, x - 0.25 + k * 0.25, f + 1, f + 3)
            l.rect('pl-rojo', x - 0.5, x + 3.5, f + 3, f + 4)
        else:                                                          # capota clara, en arco
            l.rect('pl-capota', x + 0.25, x + 2.75, f + 1, f + 2)
            l.rect('pl-capota', x - 0.5, x + 3.5, f + 2, f + 3)
            l.rect('pl-capota-s', x - 0.5, x + 3.5, f + 3, f + 4)
    for dx, ancho in ((7, 2.25), (4, 1.25), (2, 0.5)):                # en la curva
        ventana(l, derecha - dx, f + 3, f + 7, ancho)

def version():
    l = Lienzo(LARGO, FILAS)
    # El faro: cubo con remate, el ojo redondo, sobre un caño alto.
    l.rect('pl-blanco', C - 1.5, C + 1.5, 0, 1); l.rect('pl-s2', C + 0.75, C + 1.5, 0, 1)
    l.rect('pl-blanco', C - 3.5, C + 3.5, 1, 7)
    l.rect('pl-s1', C + 2, C + 3.5, 1, 7)
    l.rect('pl-s3', C - 3.5, C + 3.5, 6, 7)
    l.rect('pl-ojo', C - 1.5, C + 1.5, 2, 6)
    for f in (2, 5):                                                   # el ojo, redondeado
        l.rect('pl-blanco', C - 1.5, C - 1, f, f + 1); l.rect('pl-blanco', C + 1, C + 1.5, f, f + 1)
    l.rect('pl-blanco', C - 1.5, C + 1.5, 7, 14)
    l.rect('pl-s2', C + 0.75, C + 1.5, 7, 14)
    # El plato, con baranda, y el tambor que lo sostiene.
    baranda(l, C - 11.5, C + 11.5, 12)
    l.rect('pl-blanco', C - 1.5, C + 1.5, 12, 14); l.rect('pl-s2', C + 0.75, C + 1.5, 12, 14)
    redondo(l, C - 13, C + 13, 14, 18, cola=8, recorte={0: 1.5, -1: 1.5})
    l.rect('pl-canto', C - 12, C + 5, 14, 15)
    l.rect('pl-bajo', C - 12, C + 11.5, 17, 18)
    redondo(l, C - 7, C + 7, 18, 22, cola=5)
    l.rect('pl-bajo', C - 7, C + 6.5, 18, 19)
    for x in (C - 4, C + 1):
        l.rect('pl-ojo', x, x + 1.5, 20, 21)                         # ojos de buey del tambor
    # El cuarto redondo de arriba, con baranda en su techo y ventanas.
    baranda(l, C - 15.5, C - 7.5, 20); baranda(l, C + 7.5, C + 15.5, 20)
    redondo(l, C - 17, C + 17, 22, 30, cola=10)
    l.rect('pl-bajo', C - 17, C + 16, 22, 23)
    for x in (C - 14, C - 8, C - 2, C + 4):
        ventana(l, x, 24, 28)
    ventana(l, C + 9, 24, 28, 2); ventana(l, C + 12.5, 24, 28, 1)
    # La azotea del cuerpo largo: chimeneas, tanques con tapa redonda y baranda a lo largo.
    for x, a, alto in ((14, 3, 5), (28, 2, 4), (44, 3, 5), (64, 2, 4), (76, 3, 5)):
        l.rect('pl-blanco', x, x + a, 30 - alto, 30)
        l.rect('pl-s2', x + a - 0.75, x + a, 30 - alto, 30)
        l.rect('pl-s3', x - 0.25, x + a + 0.25, 30 - alto, 30 - alto + 1)
    for x in (52,):                                                    # tanque de agua
        l.rect('pl-blanco', x + 1, x + 5, 25, 26)
        l.rect('pl-blanco', x, x + 6, 26, 30)
        l.rect('pl-s2', x + 4.5, x + 6, 25, 30)
    baranda(l, 9.5, C - 17.5, 28); baranda(l, C + 17.5, C + 21.5, 28)
    # Cuatro pisos: faja de balcón y muro metido; cada cubierta sale más que la de arriba, muy volada en la punta.
    faja(l, 8, C + 23, 30)
    for f, der_faja, toldos in ((33, C + 27, {1, 7, 11}), (43, C + 31, {4, 9}), (53, C + 35, {1, 6, 12}),
                                (63, C + 39, {3, 8, 10})):
        der_muro = der_faja - 12
        piso(l, f, der_muro, toldos)
        baranda(l, der_muro + 0.5, der_faja - 2, f + 5)
        faja(l, 8, der_faja, f + 7)
    # El basamento: muro claro con la punta redonda grande, más ancha que las cubiertas, con líneas de velocidad,
    # ventanas (más angostas en la curva) y la entrada con sus toldos y el pilar con ojo.
    B = C + 54
    redondo(l, 9, B, 73, 92, cola=24, recorte={0: 1.5, 1: 0.5})
    l.rect('pl-bajo', 9, C + 38, 73, 74)
    for f in (75, 77):
        l.rect('pl-s1', 9, B - 24, f, f + 1)
        l.rect('pl-s3', B - 24, B - 1, f, f + 1)
    for x in (12, 19, 72, 79, 86, 93, 100, 107, 114, 121):
        ventana(l, x, 80, 87)
    for x, ancho in ((B - 22, 4), (B - 15, 3), (B - 9, 2), (B - 4.5, 1)):
        ventana(l, x, 80, 87, ancho)
    for a, b in ((38, 48), (50, 60)):                                  # la entrada: dos toldos a rayas y puertas
        for k in range(round((b - a) * 4)):
            l.rect('pl-rojo' if (k // 2) % 2 == 0 else 'pl-lona', a + k * 0.25, a + (k + 1) * 0.25, 80, 83)
        l.rect('pl-rojo', a, b, 83, 84)
        l.rect('pl-vidrio', a + 2, b - 2, 85, 92)
        l.rect('pl-marco', (a + b) / 2 - 0.25, (a + b) / 2 + 0.25, 85, 92)
    l.rect('pl-zocalo', 9, B - 1, 91, 92)
    # El seto, el pilar con ojo, la palmera, el cartel azul y el pasto.
    for a, b in ((0, 34), (64, LARGO)):
        l.rect('pl-seto', a, b, 88, 93)
        for x in range(int(a), int(b), 3): l.rect('pl-seto-o', x, x + 1, 88, 89)
    l.rect('pl-blanco', 31, 36, 82, 86); l.rect('pl-s2', 35, 36, 82, 86)   # pilar de la entrada, como un faro chico
    l.rect('pl-ojo', 32.5, 34.5, 83, 85)
    l.rect('pl-blanco', 32, 35, 86, 93); l.rect('pl-s2', 34.25, 35, 86, 93)
    l.rect('pl-poste', B - 18, B - 17.5, 84, 93); l.rect('pl-poste', B - 10, B - 9.5, 84, 93)
    l.rect('pl-cartel', B - 19, B - 8.5, 82, 85)
    l.rect('pl-lona', B - 17.5, B - 10, 83, 84)
    P = 84
    l.rect('pl-tronco', P - 0.75, P + 0.75, 64, 93)
    l.rect('pl-tronco-o', P, P + 0.75, 64, 93)
    HOJAS = [(61, -1.5, 1.5, 'pl-hoja'), (62, -5, -1, 'pl-hoja'), (62, 1, 5, 'pl-hoja'),
             (63, -9, -3, 'pl-hoja'), (63, -1, 1, 'pl-hoja-o'), (63, 3, 9, 'pl-hoja'),
             (64, -12, -6, 'pl-hoja'), (64, -4, 4, 'pl-hoja-o'), (64, 6, 12, 'pl-hoja'),
             (65, -14, -9, 'pl-hoja-o'), (65, -7, -2, 'pl-hoja'), (65, 2, 7, 'pl-hoja'), (65, 9, 14, 'pl-hoja-o'),
             (66, -15, -12, 'pl-hoja-o'), (66, -9, -5, 'pl-hoja-o'), (66, -1, 1, 'pl-hoja-o'), (66, 5, 9, 'pl-hoja-o'), (66, 12, 15, 'pl-hoja-o'),
             (67, -16, -14, 'pl-hoja-o'), (67, -10, -8, 'pl-hoja-o'), (67, 8, 10, 'pl-hoja-o'), (67, 14, 16, 'pl-hoja-o'),
             (68, -11, -10, 'pl-hoja-o'), (68, 10, 11, 'pl-hoja-o')]
    for f, a, b, c in HOJAS:
        l.rect(c, P + a, P + b, f, f + 1)
    l.rect('pl-pasto', 0, LARGO, 93, FILAS)
    l.rect('pl-pasto-o', 0, LARGO, 93, 94)
    return {'nota': ('El Edificio El Planeta (Atlántida, Uruguay), el hotel con forma de barco, de frente: la punta redonda '
                     'con las cubiertas muy voladas y escalonadas, ventanas que se angostan en la curva y barandas de caño; '
                     'el cuarto redondo, el plato y el faro con su ojo; el cuerpo largo de balcones con capotas y toldos a '
                     'rayas, chimeneas y tanque en la azotea; el basamento, más ancho en la curva, con líneas de velocidad, '
                     'la entrada y el pilar con ojo; el seto, la palmera, el cartel azul y el pasto.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': LARGO, 'lineas': l.lineas()}

COLORES = {
    'pl-blanco': ('#f4e6df', '#f4e6df'), 'pl-s1': ('#e8d5cd', '#e8d5cd'), 'pl-s2': ('#d6bfb6', '#d6bfb6'),
    'pl-s3': ('#bfa59c', '#bfa59c'), 'pl-bajo': ('#b39890', '#b39890'), 'pl-muro': ('#dfc9c0', '#dfc9c0'),
    'pl-canto': ('#fbf3ee', '#fbf3ee'), 'pl-reflejo': ('#5d6d78', '#5d6d78'),
    'pl-vidrio': ('#2e3538', '#2e3538'), 'pl-marco': ('#6b6461', '#6b6461'), 'pl-cano': ('#9a908c', '#9a908c'),
    'pl-ojo': ('#30363b', '#30363b'), 'pl-rojo': ('#b8383a', '#b8383a'), 'pl-lona': ('#f5efe9', '#f5efe9'),
    'pl-capota': ('#f6ece7', '#f6ece7'), 'pl-capota-s': ('#cdb3aa', '#cdb3aa'), 'pl-zocalo': ('#a88c84', '#a88c84'),
    'pl-seto': ('#3f5b31', '#3f5b31'), 'pl-seto-o': ('#30482a', '#30482a'), 'pl-tronco': ('#8a7156', '#8a7156'),
    'pl-tronco-o': ('#6a5440', '#6a5440'), 'pl-hoja': ('#4f7236', '#4f7236'), 'pl-hoja-o': ('#3a5829', '#3a5829'),
    'pl-poste': ('#7d8487', '#7d8487'), 'pl-cartel': ('#2f5fa0', '#2f5fa0'),
    'pl-pasto': ('#7f9a48', '#6f8a3e'), 'pl-pasto-o': ('#6a843c', '#5c7634'),
    'streamline-celeste': ('#6f9fcf', '#1d3550'), 'streamline-celeste-marco': ('#1f2a44', '#f4e1d8'),
}

p = version()
p.update(placa='streamline-celeste', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10,
         marco='streamline-celeste-marco')
guardar(sys.argv[1], 'estilos', 'Streamline Moderne', p, COLORES, 'pl-|streamline-')
print(len(p['lineas']), 'líneas, largo', p['largo'])
