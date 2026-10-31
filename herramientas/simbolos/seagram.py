# Seagram Building (Mies van der Rohe y Philip Johnson), de frente, medido sobre referencias/simbolos/seagram/
# seagramexrt.webp (425 px de ancho, al anochecer). Líneas horizontales sin separación: la torre de 30 módulos con sus
# montantes de bronce, cada piso en dos filas (vidrio y antepecho); las ventanas encendidas calcadas de la foto (cada
# vidrio toma el brillo de su pedazo: apagado, tenue o prendido); arriba, la faja de los pisos técnicos con rejillas; abajo,
# las columnas de la planta baja, el hall vidriado bajo su marquesina, la plaza con los dos canteros y la escalinata.
# Uso: seagram.py <simbolos.json> (pone decadas.mundo.1950). Necesita la foto en ~/medianeras-originales.
import sys, os
from PIL import Image
from armar import Lienzo, escribir, con_colores

FOTO = os.path.expanduser('~/medianeras-originales/referencias/simbolos/seagram/seagramexrt.webp')
TX0, MOD = 116, 6.5                  # borde izquierdo de la torre y px por módulo
PY0, PISO, PISOS = 163, 14.11, 37    # vidrio del primer piso de oficinas, px por piso
MODS, L = 30, 7                      # módulos de frente y margen de plaza a cada lado
TEC = 8                              # filas de la faja técnica
F0 = TEC + 1                         # primera fila de pisos
BAJA = F0 + PISOS * 2                # planta baja
PLAZA = BAJA + 6
FIN = PLAZA + 5

def vidrios():
    # El tono de cada vidrio: su brillo (apagado, tenue o prendido) y, si está prendido, su calidez (verde sobre rojo).
    im = Image.open(FOTO).convert('RGB')
    out = []
    for k in range(PISOS):
        fila = []
        for m in range(MODS):
            x, y = TX0 + m * MOD, PY0 + k * PISO
            v = sorted(im.crop((int(x + 1), round(y + 1), int(x + MOD - 1), round(y + 8))).getdata(), key=sum)
            r, g, b = v[len(v) * 9 // 10]
            l, calor = (r + g + b) / 3, g / max(1, r)
            fila.append('sg-vidrio' if l <= 75 else 'sg-tenue' if l <= 125 else
                        'sg-calida' if calor < 0.76 else 'sg-luz' if calor < 0.87 else 'sg-clara')
        out.append(fila)
    return out

def version():
    l = Lienzo(L * 2 + MODS + 0.25, FIN)
    T = lambda x: L + x
    # La faja técnica: oscura, con una rejilla por módulo, y el canto de arriba.
    l.rect('sg-tecnico', T(0), T(MODS + 0.25), 0, F0)
    for m in range(MODS + 1):
        l.rect('sg-rejilla', T(m), T(m + 0.25), 1, F0)
    l.rect('sg-bronce', T(0), T(MODS + 0.25), 0, 1)
    # Los pisos: vidrio según el brillo de la foto y antepecho; un montante por módulo.
    for k, fila in enumerate(vidrios()):
        f = F0 + k * 2
        for m, c in enumerate(fila):
            l.rect(c, T(m + 0.25), T(m + 1), f, f + 1)
        l.rect('sg-antepecho', T(0), T(MODS + 0.25), f + 1, f + 2)
        for m in range(MODS + 1):
            l.rect('sg-bronce', T(m), T(m + 0.25), f, f + 2)
    # Planta baja: el cielorraso encendido; en los tres vanos del medio, la marquesina blanca y el hall vidriado con
    # montantes y puertas giratorias; en los de las puntas, el fondo en penumbra con el piso iluminado; las columnas.
    W = T(MODS + 0.25)
    l.rect('sg-cielorraso', T(0), W, BAJA, BAJA + 1)
    l.rect('sg-penumbra', T(0), W, BAJA + 1, PLAZA)
    l.rect('sg-hall', T(0), W, PLAZA - 1, PLAZA)
    l.rect('sg-hall', T(6), T(24.25), BAJA + 2, PLAZA)
    for x in range(8, 24, 2):
        l.rect('sg-bronce', T(x - 0.25), T(x), BAJA + 2, PLAZA)
    for x in (10.5, 14.5, 18.5):                                       # las puertas giratorias
        l.rect('sg-puerta', T(x), T(x + 1.5), BAJA + 3, PLAZA)
        l.rect('sg-bronce', T(x + 0.5), T(x + 1), BAJA + 3, PLAZA)
    l.rect('sg-marquesina', T(5.75), T(24.5), BAJA + 1, BAJA + 2)
    l.rect('sg-sombra', T(6), T(24.25), BAJA + 2, BAJA + 3)
    for x in (0, 6, 12, 18, 24, 30):
        l.rect('sg-columna', T(x - 0.25), T(x + 0.5), BAJA, PLAZA)
    # La plaza en elevación: los canteros a los lados son cajas bajas de mármol con el cerco verde y los tulipanes
    # asomando; la plataforma de granito con el reflejo cálido del hall, su canto en sombra y los dos escalones.
    N = l.n / 4
    for a, b in ((0.5, L - 0.5), (N - L + 0.5, N - 0.5)):
        for i, x in enumerate(range(round(a * 4), round(b * 4))):
            k = (i * 7) % 11
            l.rect('sg-flor-o' if k < 3 else 'sg-flor-c' if k < 5 else 'sg-flor', x / 4, x / 4 + 0.25, PLAZA - 2, PLAZA - 1)
        l.rect('sg-cerco', a, b, PLAZA - 1, PLAZA)
    l.rect('sg-plaza', 0, N, PLAZA, PLAZA + 2)
    l.rect('sg-reflejo', T(2), T(MODS - 1.75), PLAZA, PLAZA + 1)
    for a, b in ((0.5, L - 0.5), (N - L + 0.5, N - 0.5)):
        l.rect('sg-borde', a, b, PLAZA, PLAZA + 2)
    l.rect('sg-junta', 0, N, PLAZA + 2, PLAZA + 3)
    l.rect('sg-escalon-c', 0, N, PLAZA + 3, PLAZA + 4)
    l.rect('sg-escalon', 0, N, PLAZA + 4, FIN)
    return {'nota': ('Seagram Building (Mies van der Rohe y Philip Johnson, 1954–1958), de frente al anochecer, con las '
                     'ventanas encendidas calcadas de la foto: la torre de treinta módulos con sus montantes de bronce y '
                     'antepechos oscuros, la faja de los pisos técnicos con rejillas arriba, las columnas de la planta baja, '
                     'el hall vidriado bajo su marquesina, la plaza de granito con los dos canteros y la escalinata.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': l.n / 4, 'lineas': l.lineas()}

COLORES = {
    'sg-tecnico': ('#1f1b17', '#1f1b17'), 'sg-rejilla': ('#4a3f33', '#4a3f33'), 'sg-bronce': ('#5a4630', '#5a4630'),
    'sg-antepecho': ('#2a221b', '#2a221b'), 'sg-vidrio': ('#36332f', '#36332f'), 'sg-tenue': ('#9a6a2c', '#9a6a2c'),
    'sg-calida': ('#e8873a', '#e8873a'), 'sg-luz': ('#f0a944', '#f0a944'), 'sg-clara': ('#f5c868', '#f5c868'),
    'sg-cielorraso': ('#f2c27a', '#f2c27a'), 'sg-penumbra': ('#6a4426', '#6a4426'), 'sg-hall': ('#e8a456', '#e8a456'),
    'sg-puerta': ('#f6d9a0', '#f6d9a0'), 'sg-marquesina': ('#f3eee4', '#f3eee4'), 'sg-sombra': ('#8a5a2e', '#8a5a2e'),
    'sg-columna': ('#2a221b', '#2a221b'), 'sg-plaza': ('#8c6f58', '#8c6f58'), 'sg-junta': ('#7c604b', '#7c604b'),
    'sg-reflejo': ('#a87e58', '#a87e58'), 'sg-borde': ('#d8ccba', '#d8ccba'),
    'sg-cerco': ('#46602f', '#46602f'), 'sg-flor': ('#e0b545', '#e0b545'), 'sg-flor-o': ('#c98a2c', '#c98a2c'),
    'sg-flor-c': ('#f2d77a', '#f2d77a'), 'sg-escalon-c': ('#9e8068', '#9e8068'), 'sg-escalon': ('#654c3a', '#654c3a'),
}

ruta = sys.argv[1]
p = version()
p['aire'] = round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10
escribir(ruta, 'mundo', '1950', p, sacar=('grosor', 'alto', 'arcos', 'rectas', 'zonas'))
texto = con_colores(open(ruta).read(), COLORES, 'sg-')
open(ruta, 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'])
