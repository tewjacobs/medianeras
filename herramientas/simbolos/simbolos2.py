# Ronda 3 de símbolos: décadas en dos colecciones, orgánica = Guggenheim, materiales y programas.
# Ayuda de una sola vez; la fuente es www/data/simbolos.json.
import json, re, sys, math
destino = sys.argv[1]
d = json.load(open(destino))

def f(x): return '%g' % round(x, 2)

def tramos(segs, total):
    """segs: (desde, hasta, color) ordenados y sin solapes -> texto de línea con huecos."""
    out, x = [], 0
    for a, b, c in segs:
        if b - a < 0.01: continue
        if a > x + 0.005: out.append(f'- {f(a - x)}')
        out.append(f'{c} {f(b - a)}'); x = b
    if total - x > 0.005: out.append(f'- {f(total - x)}')
    return ', '.join(out) or f'- {f(total)}'

def suma(linea):
    t = re.sub(r'^(…)|(…)$', '', linea.strip())
    t = re.sub(r'\(([^()]*)\)\s*x\s*(\d+)', lambda m: ','.join([m.group(1)] * int(m.group(2))), t)
    return sum(float(p.split()[1]) for p in t.split(',') if p.strip())

def misma_medida(nombre, lineas, total):
    for l in lineas:
        if abs(suma(l) - total) > 0.02: raise SystemExit(f'{nombre}: "{l}" suma {suma(l)} y no {total}')
    return lineas

def ventanas(n, muro, vano, color_muro='marmol', color_vano='vidrio', borde=None):
    borde = muro if borde is None else borde
    return f'{color_muro} {f(borde)}, ({color_vano} {f(vano)}, {color_muro} {f(muro)}) x{n - 1}, {color_vano} {f(vano)}, {color_muro} {f(borde)}'

col = d['colores']
col.update({
  'seagram':  {'claro': '#303137', 'oscuro': '#303137'},
  'bronce':   {'claro': '#c07f45', 'oscuro': '#c07f45'},
  'crema':    {'claro': '#d3c5a4', 'oscuro': '#e8e0cc'},
  'revoque':  {'claro': '#d6ccb9', 'oscuro': '#e3dccf'},
  'titanio':  {'claro': '#98a2ab', 'oscuro': '#c3cad1'},
  'madera-clara': {'claro': '#b98a5c', 'oscuro': '#d0a77c'},
  'caliza':   {'claro': '#cbbd9a', 'oscuro': '#d8ccb0'},
  'caliza-2': {'claro': '#b9aa86', 'oscuro': '#c6b996'},
  'terracota':   {'claro': '#b8643f', 'oscuro': '#c9784f'},
  'terracota-2': {'claro': '#a35634', 'oscuro': '#b46744'},
  'telon':    {'claro': '#a8322a', 'oscuro': '#c2483c'},
  'pliegue':  {'claro': '#86251f', 'oscuro': '#9e382e'},
  'hierro':   {'claro': '#24221f', 'oscuro': '#41434c'},
  'barra':    {'claro': '#3b3a37', 'oscuro': '#4a4f5c'},
})
viejas = d.pop('decadas')
if 'argentina' in viejas:
    viejas_ar, viejas_mu = viejas['argentina'], viejas['mundo']
else:
    viejas_ar = viejas_mu = viejas

def decada(obra, lugar, anio, nota, **partitura):
    return {'obra': obra, 'lugar': lugar, 'anio': anio, 'nota': nota, **partitura}

ar, mu = {}, {}

# ================= ARGENTINA =================
ar['1900'] = viejas_ar['1900']

molino = ['madera 1', 'madera 1', 'madera 13', 'madera 1', 'madera 1',
          'pizarra 3', 'pizarra 4', 'marmol 6', 'marmol 2, vidrio 2, marmol 2', 'marmol 8',
          'marmol 20'] + [ventanas(6, 1.5, 1.5, borde=1.75)] * 4 + [ventanas(6, 1.5, 1.5, color_vano='sol', borde=1.75), 'piedra 22']
ar['1910'] = decada('Confitería del Molino', 'Buenos Aires', '1916–1917',
  'Confitería del Molino (Francesco Gianotti; la confitería abrió en 1916 y el edificio se terminó en 1917): la esquina art nouveau con su torre, la cúpula y las aspas del molino arriba; abajo, los vitrales encendidos de la confitería.',
  direccion='horizontal', alinear='centro', grosor=1, separacion=0.5, lineas=molino)

barolo = ['sol 1', 'sol 2.4', 'pizarra 2', 'marmol 3', 'marmol 4', 'marmol 5', 'marmol 6',
          ventanas(2, 1.2, 1.4, borde=1.1)] + [ventanas(3, 1.2, 1.2, borde=1.5)] * 4 + ['marmol 12'] + \
         [ventanas(7, 1.3, 1.2, borde=1.6)] * 7 + ['marmol 20', 'piedra 22']
ar['1920'] = decada('Palacio Barolo', 'Buenos Aires', '1919–1923',
  'Palacio Barolo (Mario Palanti, 1919–1923): el cuerpo de oficinas, la torre que se angosta en escalones, la cúpula y, arriba de todo, el faro encendido.',
  direccion='horizontal', alinear='centro', grosor=1, separacion=0.5, lineas=barolo)

alt_k = [6, 6, 6, 10, 10, 10, 14, 14, 14, 19, 19, 24, 29, 29, 24, 19, 19, 14, 14, 10, 10, 6]
kav = []
for h in alt_k:
    corona = 'hormigon 1.5, ' if h == 29 else ''
    kav.append(f'{corona}hormigon 0.6, (vidrio 0.35, hormigon 0.65) x{h}, piedra 2.5')
ar['1930'] = decada('Edificio Kavanagh', 'Buenos Aires', '1934–1936',
  'Edificio Kavanagh (Sánchez, Lagos y de la Torre, 1934–1936): la torre angosta con su remate, los retiros en bloque hacia los costados, las filas de ventanas y el basamento.',
  direccion='vertical', alinear='fin', alto=190, grosor=1, separacion=0.3, lineas=kav)

arroyo = ['hormigon 30', 'hormigon 1, vidrio 28, hormigon 1', 'hormigon 30',
          '- 30', '- 30', '- 30', '- 30',
          'follaje 3, - 24, follaje 3', 'follaje 6, agua 18, follaje 6', 'follaje 8, agua 14, follaje 8']
misma_medida('Casa sobre el Arroyo', arroyo, 30)
paso = 1.6
ar['1940'] = decada('Casa sobre el Arroyo', 'Mar del Plata', '1943–1946',
  'Casa sobre el Arroyo (Amancio Williams, 1943–1946): la caja con su ventana corrida, apoyada sobre un arco de hormigón que salta el arroyo de una orilla a la otra.',
  direccion='horizontal', grosor=1, separacion=0.6, lineas=arroyo,
  arcos=[{'color': 'hormigon', 'desde': 2.5, 'hasta': 27.5, 'base': 7, 'flecha': round(7 * paso + 0.5 - (2 * paso + 1), 2), 'lineas': 2}])

curu = ['hormigon 30', '(hormigon 0.6, vidrio 2.4) x10', 'hormigon 30', '(hormigon 0.6, vidrio 2.4) x10', 'hormigon 30',
        'hormigon 1, - 10, follaje 7, - 11, hormigon 1', 'hormigon 1, - 11, follaje 5, - 12, hormigon 1',
        'hormigon 1, - 13, madera 1, - 14, hormigon 1', 'piedra 30']
misma_medida('Curutchet', curu, 30)
ar['1950'] = decada('Casa Curutchet', 'La Plata', '1949–1953',
  'Casa Curutchet (Le Corbusier, 1949–1953): la grilla de parasoles de hormigón, los pilotes y el álamo que crece en el medio de la casa.',
  direccion='horizontal', grosor=1, separacion=0.55, lineas=curu)

bl = []
for k in range(17):
    if k % 2 == 0: bl.append('hormigon 28')
    else:
        a = 2 + 1.5 * math.sin(k * 0.8)
        bl.append(f'hormigon {f(a)}, vidrio 6, hormigon 2, vidrio 7, hormigon 2, vidrio 6, hormigon {f(5 - a)}')
misma_medida('Banco de Londres', bl, 28)
ar['1960'] = decada('Banco de Londres y América del Sud', 'Buenos Aires', '1959–1966',
  'Banco de Londres (Clorindo Testa con SEPRA, 1959–1966): los grandes pilares de hormigón de la fachada y, entre ellos, los vidrios recortados por las placas que suben desparejas.',
  direccion='vertical', grosor=1, separacion=0.5, lineas=bl)

somisa = []
for piso in range(12):
    somisa.append('acero 20.5' if piso % 2 == 0 else '(acero 0.5, vidrio 2) x8, acero 0.5')
somisa += ['acero 20.5', '- 2, vidrio 16.5, - 2', '- 2, vidrio 16.5, - 2']
misma_medida('SOMISA', somisa, 20.5)
ar['1970'] = decada('Edificio SOMISA', 'Buenos Aires', '1966–1977',
  'Edificio SOMISA (Mario Roberto Álvarez, 1966–1977): todo de acero soldado, la fachada como una grilla de perfiles y vidrio sobre la planta baja retirada.',
  direccion='horizontal', grosor=1, separacion=0.4, lineas=somisa)

reco = ['ladrillo 30', 'revoque 30', 'revoque 30',
        tramos([(x, x + 3, 'vidrio') for x in (2.5, 8.5, 14.5, 20.5)] + [(26.5, 28, 'revoque')], 30).replace('- ', 'revoque ').replace('revoque 2.5', 'revoque 2.5', 1)]
fila = ', '.join(['revoque 4.5'] + sum([['vidrio 3', 'revoque 3'] for _ in range(4)], [])[:-1] + ['revoque 4.5'])
reco = misma_medida('Recoleta', ['ladrillo 30', 'revoque 30', 'revoque 30', 'revoque 30', fila, fila, fila, 'revoque 30', 'piedra 30'], 30)
reco = [l for l in reco]
ar['1980'] = decada('Centro Cultural Recoleta', 'Buenos Aires', '1980',
  'Centro Cultural Recoleta (Testa, Bedel y Benedit, 1980): el antiguo convento reciclado, con el techo de tejas y la galería de arcos sobre los muros blancos.',
  direccion='horizontal', grosor=1, separacion=0.5, lineas=reco,
  arcos=[{'color': 'vidrio', 'desde': 4.5 + 6 * i, 'hasta': 7.5 + 6 * i, 'base': 4, 'flecha': 1.6, 'lineas': 1} for i in range(4)])

ar['1990'] = viejas_ar['1990']

puente = ['hormigon 30, tinta 1.2, agua 3']
for k in range(1, 16):
    puente.append(f'acero {f(27 - k * 1.7)}, tinta 1.2, agua 3')
puente += ['tinta 1.2, agua 3'] * 3
ar['2000'] = decada('Puente de la Mujer', 'Buenos Aires', '1998–2001',
  'Puente de la Mujer (Santiago Calatrava, 1998–2001): el mástil y los tensores que bajan en arpa hasta el tablero, sobre el agua del dique de Puerto Madero.',
  direccion='vertical', alinear='fin', alto=150, grosor=1, separacion=0.55, lineas=puente)

cck = ['pizarra 20', 'pizarra 24', 'marmol 28',
       ventanas(9, 1.6, 1.3, borde=0.65), 'marmol 4, azul 20, marmol 4', 'marmol 3, azul 22, marmol 3',
       'marmol 3, azul 22, marmol 3', 'marmol 4, azul 20, marmol 4', ventanas(9, 1.6, 1.3, borde=0.65), 'marmol 28', 'piedra 30']
ar['2010'] = decada('Centro Cultural Kirchner', 'Buenos Aires', '2015',
  'Centro Cultural Kirchner (B4FS, 2015): el antiguo Palacio de Correos con su mansarda y, en el centro, la Ballena Azul, la sala de conciertos que ocupa el corazón del edificio.',
  direccion='horizontal', alinear='centro', grosor=1, separacion=0.5, lineas=cck)

# ================= MUNDO =================
st = ['- 11, bronce 2, - 17', '- 10, bronce 4, - 16'] + ['- 10, bronce 0.5, marmol 3, bronce 0.5, - 16'] * 3 + \
     ['bronce 30', 'bronce 0.5, (marmol 2.4, vidrio 1.2) x8, marmol 0.2, bronce 0.5', 'bronce 0.5, marmol 29, bronce 0.5',
      'bronce 0.5, (marmol 2.4, vidrio 1.2) x8, marmol 0.2, bronce 0.5', 'bronce 30', 'follaje 30']
misma_medida('Stoclet', st, 30)
mu['1900'] = decada('Palacio Stoclet', 'Bruselas', '1905–1911',
  'Palacio Stoclet (Josef Hoffmann, 1905–1911): los volúmenes blancos con todos los bordes marcados en bronce y la torre escalonada, corrida hacia un costado.',
  direccion='horizontal', grosor=1, separacion=0.55, lineas=st)

ped = []
for k in range(30):
    partes = []
    techo = 2.2 + 1.3 * math.sin(k * 0.42)
    partes.append(f'marmol {f(techo)}')
    for piso in range(6):
        a = 3.0 + 0.9 * math.sin(k * 0.38 + piso * 1.1)
        partes += [f'hierro 0.6', f'marmol {f(a)}']
    partes.append('piedra 3')
    ped.append(', '.join(partes))
mu['1910'] = decada('Casa Milà (La Pedrera)', 'Barcelona', '1906–1912',
  'La Pedrera (Gaudí, 1906–1912): la fachada de piedra que ondula; los balcones de hierro forjado son los tramos negros, que suben y bajan de una línea a la otra.',
  direccion='vertical', alinear='fin', grosor=1, separacion=0.35, lineas=ped)

mu['1920'] = viejas_mu['1920']

pai = ['revoque 30']
for _ in range(5): pai += ['(revoque 0.5, vidrio 2.5) x10', 'revoque 30']
pai += ['- 20, sol 6, - 4', '- 1, vidrio 28, - 1', 'follaje 30']
misma_medida('Paimio', pai, 30)
mu['1930'] = decada('Sanatorio de Paimio', 'Paimio, Finlandia', '1929–1933',
  'Sanatorio de Paimio (Alvar Aalto, 1929–1933): el pabellón blanco de los pacientes con sus ventanas corridas, la marquesina amarilla de la entrada y el bosque alrededor.',
  direccion='horizontal', grosor=1, separacion=0.5, lineas=pai)

def eames(colores, anchos):
    partes = ['hierro 0.4']
    for c, w in zip(colores, anchos): partes += [f'{c} {f(w)}', 'hierro 0.4']
    return ', '.join(partes)
anchos = [3, 3, 2, 3, 3, 2, 3, 3, 2, 3]
arriba = ['vidrio', 'rojo', 'revoque', 'vidrio', 'azul', 'vidrio', 'revoque', 'hierro', 'vidrio', 'rojo']
abajo = ['revoque', 'vidrio', 'vidrio', 'azul', 'revoque', 'rojo', 'vidrio', 'vidrio', 'revoque', 'vidrio']
total = sum(anchos) + 0.4 * 11
eam = [f'hierro {f(total)}'] + [eames(arriba, anchos)] * 3 + [f'hierro {f(total)}'] + [eames(abajo, anchos)] * 3 + [f'hierro {f(total)}', f'follaje {f(total)}']
misma_medida('Eames', eam, total)
mu['1940'] = decada('Casa Eames', 'Los Ángeles', '1949',
  'Casa Eames (Charles y Ray Eames, 1949): la estructura fina de acero negro y los paneles de colores, vidrio, blanco, rojo y azul, en dos pisos.',
  direccion='horizontal', grosor=1, separacion=0.45, lineas=eam)

sg = ['seagram 24'] * 10
sg[5] = 'seagram 18, bronce 6'; sg[9] = 'seagram 18, bronce 6'
mu['1950'] = decada('Seagram Building', 'Nueva York', '1954–1958',
  'Seagram Building (Mies van der Rohe y Philip Johnson, 1954–1958): los perfiles verticales oscuros, casi todos en sombra; dos se encienden abajo en bronce. Igual en los dos temas.',
  direccion='vertical', grosor=1, separacion=1.2, lineas=sg)

mu['1960'] = viejas_mu['1960']

ciclo = ['acero', 'azul', 'acero', 'verde', 'acero', 'sol', 'acero', 'azul', 'verde', 'acero']
pomp = []
for k in range(32):
    c = ciclo[k % len(ciclo)]
    if 3 <= k <= 28:
        y = 11.5 - (k - 3) * 0.42
        pomp.append(f'{c} {f(y)}, rojo 1.4, {c} {f(16 - y - 1.4)}')
    else:
        pomp.append(f'{c} 16')
misma_medida('Pompidou', pomp, 16)
mu['1970'] = decada('Centro Pompidou', 'París', '1971–1977',
  'Centro Pompidou (Piano, Rogers y Franchini, 1971–1977): la fachada larga de estructura gris con los conductos de colores (azul el aire, verde el agua, amarillo la electricidad) y la escalera mecánica roja en diagonal.',
  direccion='vertical', grosor=1, separacion=0.4, lineas=pomp)

mu['1980'] = viejas_mu['1980']

bil = []
for i in range(14):
    segs = []
    c1, w1 = 7 + 1.5 * math.sin(i * 0.5), 5 + 3 * math.sin(i * 0.45 + 0.3)
    c2, w2 = 18 + 2 * math.sin(i * 0.4 + 1), 7 + 4 * math.sin(i * 0.35 + 1.2)
    c3, w3 = 28 + 1.2 * math.cos(i * 0.6), 4 + 2.5 * math.cos(i * 0.5 + 0.4)
    for c, w, color in [(c1, w1, 'titanio'), (c2, w2, 'vidrio' if i % 4 == 1 else 'titanio'), (c3, w3, 'titanio')]:
        if w > 0.6: segs.append((max(0, c - w / 2), min(34, c + w / 2), color))
    if i < 9: segs.append((35, 36.6, 'caliza'))
    segs.sort()
    limpio, fin = [], 0
    for a, b, c in segs:
        a = max(a, fin + 0.4) if limpio else a
        if b - a > 0.3: limpio.append((a, b, c)); fin = b
    bil.append(tramos(limpio, 37))
bil += ['agua 37', 'agua 37']
mu['1990'] = decada('Museo Guggenheim Bilbao', 'Bilbao', '1993–1997',
  'Guggenheim Bilbao (Frank Gehry, 1993–1997): las formas de titanio que se curvan, con algún paño de vidrio, la torre de piedra a la derecha y la ría abajo.',
  direccion='horizontal', grosor=1, separacion=0.45, lineas=bil)

gk = []
n_l = 24
for k in range(n_l):
    t = k / (n_l - 1)
    w = 8 * min(1, (t / 0.5) ** 0.5) if t < 0.5 else 8 - (t - 0.5) / 0.5 * 1.6
    w = max(w, 1.2)
    p = ((k * 0.13) % 1) * w
    a, b = p, min(p + w * 0.25, w)
    segs = [(0, a, 'reflejo'), (a, b, 'vidrio'), (b, w, 'reflejo')]
    gk.append(', '.join(f'{c} {f(y - x)}' for x, y, c in segs if y - x > 0.05))
mu['2000'] = decada('30 St Mary Axe', 'Londres', '2001–2004',
  '30 St Mary Axe (Foster + Partners, 2001–2004): el perfil de bala, esbelto, en líneas horizontales, con la franja de vidrio oscuro que gira en espiral.',
  direccion='horizontal', alinear='centro', alto=190, grosor=1, separacion=0.3, lineas=gk)

cctv = []
def diag(a, b, i):
    segs, x, k = [], a, 0
    while x < b - 0.05:
        w = 1.6 + 0.6 * math.sin(i * 0.9 + k)
        segs.append((x, min(b, x + w), 'vidrio' if k % 2 == 0 else 'acero')); x += w; k += 1
    return segs
for i in range(5): cctv.append(tramos(diag(4, 34, i), 34))
for i in range(5, 17):
    s_ = i - 5
    ia = 4 + s_ * 0.22; da = 22 - s_ * 0.22
    cctv.append(tramos(diag(ia, ia + 7, i) + diag(da, da + 7, i), 34))
for i in range(17, 20): cctv.append(tramos(diag(0, 32, i), 34))
mu['2010'] = decada('Sede de CCTV', 'Pekín', '2004–2012',
  'Sede de CCTV (OMA, 2004–2012): las dos torres inclinadas que se unen arriba en un voladizo y abajo en el basamento, formando un anillo, con la trama irregular de la fachada.',
  direccion='horizontal', grosor=1, separacion=0.45, lineas=cctv)

mu['2020'] = viejas_mu['2020']
d['decadas'] = {'argentina': ar, 'mundo': mu}

# ================= ESTILO: ORGÁNICA = GUGGENHEIM =================
gug = []
bandas = [22, 20, 18, 16]
for j, w in enumerate(bandas):
    for fila in range(3):
        color = 'vidrio' if fila == 2 else 'crema'
        ww = w - 1.5 if color == 'vidrio' else w
        segs = [(20 - ww / 2, 20 + ww / 2, color)]
        r = len(gug)
        if 6 <= r <= 11: segs.insert(0, (1, 7, 'crema' if r % 3 != 2 else 'vidrio'))
        gug.append(tramos(segs, 34))
gug += [tramos([(1, 7, 'crema'), (9, 31, 'vidrio')], 34), 'piedra 34']
d['estilos']['Arquitectura orgánica'] = {
  'nota': 'El Guggenheim de Nueva York (Wright, 1943–1959): la espiral de hormigón que se ensancha hacia arriba, banda por banda, con la ventana corrida entre una y otra; a la izquierda, la rotonda chica.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0.45, 'lineas': gug}

# ================= MATERIALES =================
mat = {}
fa = '(ladrillo 3.6, - 0.4) x7, ladrillo 3.6, - 0.4'
fb = 'ladrillo 1.8, - 0.4, (ladrillo 3.6, - 0.4) x7, ladrillo 1.8'
mat['Ladrillo'] = {'nota': 'Aparejo a soga: cada hilada corrida media pieza respecto de la anterior; las juntas son los huecos.',
  'direccion': 'horizontal', 'escala': 0.8, 'grosor': 1, 'separacion': 0.4, 'lineas': misma_medida('Ladrillo', [fa, fb] * 4, 32)}
mat['Hormigón armado'] = {'nota': 'El hormigón con las barras de acero en corte, en una grilla regular.',
  'direccion': 'horizontal', 'escala': 0.8, 'grosor': 1, 'separacion': 0.3,
  'lineas': misma_medida('Hormigón armado', ['hormigon 31.8', '(hormigon 3, barra 0.6) x8, hormigon 3'] * 4 + ['hormigon 31.8'], 31.8)}
tablas = ['hormigon 32', '(hormigon 3.7, barra 0.6, hormigon 3.7) x4', 'hormigon 32', 'hormigon 32']
mat['Hormigón visto'] = {'nota': 'Las tablas del encofrado (una línea cada una) y, cada tanto, los agujeros de los tensores.',
  'direccion': 'horizontal', 'escala': 0.8, 'grosor': 1, 'separacion': 0.2, 'lineas': misma_medida('Hormigón visto', tablas * 2 + ['hormigon 32'], 32)}
vetas = []
for i in range(11):
    nudo = 3.5 * math.exp(-((i - 5) ** 2) / 6)
    a = 13 - nudo; b = 2 * nudo + 1.5 + 0.8 * math.sin(i)
    vetas.append(f'madera {f(a)}, madera-clara {f(b)}, madera {f(32 - a - b)}' if i % 2 else f'madera-clara {f(a + 2)}, madera {f(b + 1)}, madera-clara {f(32 - a - b - 3)}')
mat['Madera'] = {'nota': 'Las vetas en dos tonos, que se abren alrededor de un nudo.',
  'direccion': 'horizontal', 'escala': 0.8, 'grosor': 1, 'separacion': 0.15, 'lineas': misma_medida('Madera', vetas, 32)}
vid = []
for i in range(10):
    lineas_ = []
    for pano in range(2):
        x = 1 + i * 0.9 + pano * 0.6
        lineas_.append(f'reflejo {f(x)}, espuma 1.4, reflejo {f(14 - x - 1.4)}')
    vid.append(', - 1, '.join(lineas_))
mat['Vidrio'] = {'nota': 'Dos paños de vidrio con el reflejo que los cruza en diagonal; la carpintería es el corte del medio.',
  'direccion': 'horizontal', 'escala': 0.8, 'grosor': 1, 'separacion': 0.3, 'lineas': misma_medida('Vidrio', vid, 29)}
ac = []
alas = 2; alma = 5
for fila in range(alas + alma + alas):
    es_ala = fila < alas or fila >= alas + alma
    segs = [(x, x + 6, 'acero') if es_ala else (x + 2.6, x + 3.4, 'acero') for x in (0, 9, 18)]
    ac.append(tramos(segs, 24))
mat['Acero'] = {'nota': 'Tres perfiles doble T en corte: las alas arriba y abajo, el alma en el medio.',
  'direccion': 'horizontal', 'escala': 0.8, 'grosor': 1, 'separacion': 0.25, 'lineas': ac}
hiladas = [[6, 5, 7, 4, 6], [4, 7, 5, 6, 6], [5, 6, 6, 5, 6], [7, 4, 6, 7, 4], [5, 6, 5, 6, 6]]
pc = []
for i, h in enumerate(hiladas):
    partes = []
    for j, w in enumerate(h):
        partes.append(f'{"caliza" if (i + j) % 3 else "caliza-2"} {f(w - 0.4)}')
    linea = ', - 0.4, '.join(partes)
    pc += [linea, linea]
mat['Piedra caliza'] = {'nota': 'Sillares de caliza en hiladas de dos líneas, con piezas de largos distintos y juntas finas.',
  'direccion': 'horizontal', 'escala': 0.8, 'grosor': 1, 'separacion': 0.2, 'lineas': misma_medida('Piedra caliza', pc, 27.6)}
tc = []
for i in range(9):
    c1, c2 = ('terracota', 'terracota-2') if i % 2 else ('terracota-2', 'terracota')
    corr = 0.9 if i % 2 else 0
    tc.append(f'{c1} {f(1.5 + corr)}, ' + ', '.join([f'- 0.3, {c2 if k % 2 else c1} 1.5' for k in range(15)]) + (f', - 0.3, {c1} {f(1.5 - corr)}' if 1.5 - corr > 0 else ''))
mat['Terracota'] = {'nota': 'Piezas chicas de terracota esmaltada en dos tonos, corridas media pieza de una hilada a la otra.',
  'direccion': 'horizontal', 'escala': 0.8, 'grosor': 1, 'separacion': 0.3, 'lineas': tc}
d['materiales'] = mat

# ================= PROGRAMAS =================
pro = {}
def cuadro(x0, x1, color, fila, f0, f1):
    if fila == f0 or fila == f1: return [(x0, x1, 'tinta')]
    if f0 < fila < f1: return [(x0, x0 + 0.5, 'tinta'), (x0 + 0.5, x1 - 0.5, color), (x1 - 0.5, x1, 'tinta')]
    return []
mus = []
for fila in range(8):
    segs = cuadro(2, 9, 'cielo', fila, 1, 6) + cuadro(12, 22, 'sol', fila, 0, 7) + cuadro(25, 30, 'rojo', fila, 2, 5)
    mus.append(tramos(segs, 32))
mus += ['- 32', 'madera 32']
pro['Museo'] = {'nota': 'Una pared de sala con tres cuadros de tamaños distintos, colgados a la misma altura de centro, y el piso de madera.',
  'direccion': 'horizontal', 'escala': 0.8, 'grosor': 1, 'separacion': 0.5, 'lineas': mus}
casa = ['ladrillo 2', 'ladrillo 5', 'ladrillo 8', 'ladrillo 11', 'ladrillo 14', 'ladrillo 17',
        'revoque 2, vidrio 4, revoque 4, madera 2.5, revoque 1.5', 'revoque 2, vidrio 4, revoque 4, madera 2.5, revoque 1.5',
        'revoque 10, madera 2.5, revoque 1.5', 'follaje 20']
pro['Vivienda unifamiliar'] = {'nota': 'La casa de dibujo de chico: techo a dos aguas de tejas, una ventana, la puerta y el pasto.',
  'direccion': 'horizontal', 'alinear': 'centro', 'escala': 0.8, 'grosor': 1, 'separacion': 0.4, 'lineas': casa}
vc = []
for piso in range(7):
    vc += ['hormigon 22.6', '(revoque 0.6, vidrio 2.2, revoque 0.6, follaje 1) x5, revoque 0.6' if piso % 2 else '(revoque 0.6, vidrio 2.2, revoque 0.6, madera 1) x5, revoque 0.6']
vc += ['hormigon 22.6', '- 2, vidrio 18.6, - 2']
pro['Vivienda colectiva'] = {'nota': 'Un bloque de departamentos: losas, ventanas y balcones, unos con plantas y otros con persianas de madera.',
  'direccion': 'horizontal', 'escala': 0.8, 'grosor': 1, 'separacion': 0.3, 'lineas': misma_medida('Vivienda colectiva', vc, 22.6)}
of = []
for piso in range(18):
    of.append('acero 10.3' if piso % 2 == 0 else '(acero 0.3, vidrio 1.7) x5, acero 0.3')
of += ['acero 10.3', '- 1, vidrio 8.3, - 1']
pro['Oficinas'] = {'nota': 'Una torre de oficinas con muro cortina: franjas de vidrio entre antepechos de acero.',
  'direccion': 'horizontal', 'alto': 170, 'escala': 0.85, 'grosor': 1, 'separacion': 0.25, 'lineas': of}
tel = []
for k in range(21):
    if 6 <= k <= 14: tel.append('telon 3, vidrio 14, madera 2')
    else: tel.append(f'{"telon" if k % 2 == 0 else "pliegue"} {f(17 + 2 * math.cos((k if k < 6 else 20 - k) * 0.5))}, madera 2')
pro['Cultural'] = {'nota': 'Un escenario: el telón rojo abierto a los costados, con sus pliegues, el fondo oscuro y las tablas.',
  'direccion': 'vertical', 'alinear': 'fin', 'escala': 0.8, 'grosor': 1, 'separacion': 0.3, 'lineas': tel}
d['programas'] = pro

s = json.dumps(d, ensure_ascii=False, indent=2)
s = re.sub(r'\{\s*"claro": ("[^"]+"),\s*"oscuro": ("[^"]+")\s*\}', r'{ "claro": \1, "oscuro": \2 }', s)
open(destino, 'w').write(s + '\n')
print('ok', 'AR', list(ar), 'MUNDO', list(mu))
