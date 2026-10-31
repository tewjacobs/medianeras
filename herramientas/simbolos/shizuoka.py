# Centro de Prensa y Radiodifusión de Shizuoka (Kenzo Tange, Tokio), medido sobre referencias/simbolos/shizuoka/
# metalocus_..._32-32.jpg, achicada a la mitad (1 unidad = 10 px). Líneas horizontales sin separación: el cilindro
# del núcleo en paneles verticales que se angostan hacia los bordes (luz de la izquierda), el caño de arriba y las
# cajas de oficinas colgadas a los dos lados, a distintas alturas, con sus losas y el vidrio partido por montantes.
# Uso: shizuoka.py <simbolos.json> (reescribe programas.Oficinas).
import math, sys
from armar import Lienzo, guardar

X = lambda px: (px - 63) / 10 + 4             # px de la foto achicada a unidades
F = lambda py: round((py - 30) / 10) + 2      # px a fila (dos filas arriba para el caño)
N0, N1, PIE = X(63), X(162), F(785)           # núcleo
PANELES = 40                                  # paneles en toda la vuelta del cilindro

# Cajas: desde, hasta (x en px) y los bordes de sus pisos (y en px).
CAJAS = [
    (28, 147, [180, 240, 295, 350]),          # arriba a la izquierda, tres pisos
    (150, 205, [240, 295, 350]),              # arriba a la derecha, dos
    (28, 147, [440, 495, 550, 610]),          # abajo a la izquierda, tres
    (150, 232, [390, 440, 490, 540, 590, 640, 690]),   # abajo a la derecha, seis
]

def tono(x):                                  # panel según el ángulo del cilindro
    r = (N1 - N0) / 2
    luz = math.cos(math.asin(max(-1, min(1, (x - (N0 + r)) / r))) + 0.6)
    return 'sz-1' if luz > 0.8 else 'sz-2' if luz > 0.3 else 'sz-3'

def version():
    l = Lienzo(X(240), PIE + 1)
    r, cx = (N1 - N0) / 2, (N0 + N1) / 2
    bordes = [cx + r * math.sin(-math.pi / 2 + k * 2 * math.pi / PANELES) for k in range(PANELES // 2 + 1)]
    for a, b in zip(bordes, bordes[1:]):      # el cilindro, panel por panel
        l.rect(tono((a + b) / 2), a, b, 3, PIE)
        l.rect('sz-junta', b - 0.125, b + 0.125, 3, PIE)
    l.rect('sz-2', N0 + 1, N1 - 1, 2, 3)      # el remate redondeado
    l.rect('sz-tubo', X(127), X(135), 0, 2)
    for f in (F(370), F(420), F(720)):        # ojos de buey del núcleo, entre las cajas
        l.rect('sz-ojo', cx - 0.5, cx + 0.5, f, f + 1)
    for x0, x1, pisos in CAJAS:
        a, b = X(x0), X(x1)
        l.rect('sz-caja', a, b, F(pisos[0]), F(pisos[-1]) + 1)
        for p0, p1 in zip(pisos, pisos[1:]):
            l.rect('sz-losa', a, b, F(p0), F(p0) + 1)
            x = a + 0.5
            while x + 1 <= b - 0.5:          # vidrio entre montantes
                l.rect('sz-vidrio', x + 0.25, x + 1, F(p0) + 1, F(p1))
                l.rect('sz-cielo', x + 0.25, x + 1, F(p0) + 1, F(p0) + 2)   # el reflejo de arriba
                x += 1
        l.rect('sz-losa', a, b, F(pisos[-1]), F(pisos[-1]) + 1)
    # Abajo a la derecha, bajo las cajas: el volumen de piedra con la entrada vidriada junto al tubo, y el zócalo.
    l.rect('sz-piedra', X(150), X(232), F(690) + 1, PIE)
    l.rect('sz-vidrio', N1, X(190), F(705), PIE)
    for x in (X(170), X(180)):
        l.rect('sz-marco', x, x + 0.25, F(705), PIE)
    l.rect('sz-puerta', X(200), X(215), F(745), PIE)
    l.rect('sz-zocalo', X(20), X(240), PIE, PIE + 1)
    lineas = l.lineas()
    return {'nota': ('El Centro de Prensa de Shizuoka (Kenzo Tange, Tokio), de frente: el cilindro del núcleo en paneles '
                     'oscuros, con su caño arriba y algunos ojos de buey, y las cajas de oficinas colgadas a los dos lados, '
                     'a distintas alturas, con vidrio entre montantes; abajo, la entrada en un volumen de piedra y el zócalo.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': lineas}

COLORES = {
    'sz-1': ('#6f6762', '#6f6762'), 'sz-2': ('#57504b', '#57504b'), 'sz-3': ('#423c38', '#423c38'),
    'sz-junta': ('#2e2926', '#2e2926'), 'sz-caja': ('#3a3532', '#3a3532'), 'sz-losa': ('#625b56', '#625b56'),
    'sz-vidrio': ('#3d4e5b', '#3d4e5b'), 'sz-cielo': ('#7f97a8', '#7f97a8'), 'sz-tubo': ('#a3a4a5', '#a3a4a5'), 'sz-ojo': ('#1d1a18', '#1d1a18'),
    'sz-piedra': ('#cbbba4', '#cbbba4'), 'sz-marco': ('#8a9196', '#8a9196'), 'sz-puerta': ('#6b5d4e', '#6b5d4e'),
    'sz-zocalo': ('#d9d2c6', '#d9d2c6'),
}

p = version()
p.update(placa='oficinas-diario', aire=round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10, marco='oficinas-diario-marco')
COLORES.update({'oficinas-diario': ('#e6dcc6', '#38342b'), 'oficinas-diario-marco': ('#192339', '#c7cbd4')})
guardar(sys.argv[1], 'programas', 'Oficinas', p, COLORES, 'sz-|oficinas-diario')
print(len(p['lineas']), 'líneas, largo', p['largo'])
