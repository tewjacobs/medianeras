# Arma www/data/simbolos.json (ayuda de una sola vez; el JSON es la fuente).
import json, re, sys
destino = sys.argv[1]
d = json.load(open(destino))

def f(x): return '%g' % round(x, 2)

def tramos(segs, total):
    """segs: lista de (desde, hasta, color) ordenada y sin solapes -> texto de línea."""
    out, x = [], 0
    for a, b, c in segs:
        if a > x + 1e-9: out.append(f'- {f(a - x)}')
        out.append(f'{c} {f(b - a)}'); x = b
    if total - x > 1e-9: out.append(f'- {f(total - x)}')
    return ', '.join(out)

def suma(linea):
    t = re.sub(r'^(…)|(…)$', '', linea.strip())
    t = re.sub(r'\(([^()]*)\)\s*x\s*(\d+)', lambda m: ','.join([m.group(1)] * int(m.group(2))), t)
    return sum(float(p.split()[1]) for p in t.split(',') if p.strip())

def misma_medida(nombre, lineas, total):
    for l in lineas:
        if abs(suma(l) - total) > 0.01: raise SystemExit(f'{nombre}: "{l}" suma {suma(l)} y no {total}')

col = d['colores']
col.update({
  'pizarra':  {'claro': '#56687a', 'oscuro': '#8a9bad'},
  'ladrillo': {'claro': '#9c5a3a', 'oscuro': '#b8714c'},
  'acero':    {'claro': '#8b9096', 'oscuro': '#b4b9c0'},
  'hormigon': {'claro': '#a39d93', 'oscuro': '#dcd8d0'},
  'brise':    {'claro': '#6d8fa6', 'oscuro': '#86a6bd'},
  'azulejo':  {'claro': '#2f60b5', 'oscuro': '#5a82d0'},
  'verde':    {'claro': '#3d8a4f', 'oscuro': '#4fa063'},
  'bronce':   {'claro': '#8a6a45', 'oscuro': '#c07f45'},
  'gris-bosco': {'claro': '#55524d', 'oscuro': '#8f8b84'},
  'verde-m':  {'claro': '#3e5f52', 'oscuro': '#6f9585'},
  'pantalla': {'claro': '#9fc0cc', 'oscuro': '#b8d4de'},
  'reflejo':  {'claro': '#86b9d6', 'oscuro': '#8fbfdc'},
})

# ---- Banderas: compactas, sobre una placa ----
d['paises'] = {
  'Argentina': {
    'nota': 'Bandera: dos celestes, dos blancas con el sol amarillo en el centro, dos celestes.',
    'direccion': 'horizontal', 'placa': 'noche', 'escala': 0.55, 'grosor': 1, 'separacion': 0.8,
    'lineas': ['celeste 18', 'celeste 18', 'blanco 7, sol 4, blanco 7', 'blanco 7, sol 4, blanco 7', 'celeste 18', 'celeste 18'],
  },
  'Estados Unidos': {
    'nota': 'Bandera: rayas rojas y blancas; arriba a la izquierda el cantón azul, con las estrellas como cortes blancos en zigzag.',
    'direccion': 'horizontal', 'placa': 'noche', 'escala': 0.55, 'grosor': 1, 'separacion': 0.5,
    'lineas': [
      'azul-eeuu 1.25, (blanco 0.75, azul-eeuu 1.5) x3, blanco 0.75, azul-eeuu 1.25, rojo-eeuu 14',
      'azul-eeuu 2, (blanco 0.75, azul-eeuu 1.5) x2, blanco 0.75, azul-eeuu 2.75, blanco 14',
      'azul-eeuu 1.25, (blanco 0.75, azul-eeuu 1.5) x3, blanco 0.75, azul-eeuu 1.25, rojo-eeuu 14',
      'azul-eeuu 2, (blanco 0.75, azul-eeuu 1.5) x2, blanco 0.75, azul-eeuu 2.75, blanco 14',
      'azul-eeuu 1.25, (blanco 0.75, azul-eeuu 1.5) x3, blanco 0.75, azul-eeuu 1.25, rojo-eeuu 14',
      'blanco 24', 'rojo-eeuu 24', 'blanco 24', 'rojo-eeuu 24'],
  },
  'Uruguay': {
    'nota': 'Bandera: nueve franjas blancas y azules; en el cantón blanco, el sol de mayo, que crece y se achica de línea a línea.',
    'direccion': 'horizontal', 'placa': 'noche', 'escala': 0.55, 'grosor': 1, 'separacion': 0.5,
    'lineas': [
      'blanco 3.25, sol 1.5, blanco 19.25',
      'blanco 2.5, sol 3, blanco 2.5, azul 16',
      'blanco 2.25, sol 3.5, blanco 18.25',
      'blanco 2.5, sol 3, blanco 2.5, azul 16',
      'blanco 3.25, sol 1.5, blanco 19.25',
      'azul 24', 'blanco 24', 'azul 24', 'blanco 24'],
  },
}
for k, v in d['paises'].items():
    misma_medida(k, v['lineas'], v['lineas'][0] and suma(v['lineas'][0]))

# ---- Obras emblemáticas de arquitectos: compactas, con poco entorno ----
fw = [
  'follaje 2, - 11, piedra 2.5, - 6.5, follaje 2',
  'follaje 3, - 4, terraza 9, piedra 2.5, terraza 2, - 1.5, follaje 2',
  'follaje 2, - 5, (rojo 0.5, vidrio 1.5) x4, piedra 2.5, - 6.5',
  'follaje 1, - 1, terraza 14, piedra 2.5, terraza 4, - 1.5',
  '- 3, (rojo 0.5, vidrio 1.5) x5, rojo 0.5, piedra 2.5, - 8',
  'terraza 20, piedra 2.5, - 1.5',
  '- 6, piedra 1.5, - 7, piedra 2.5, - 7',
  'agua 6, piedra 1.5, agua 7, piedra 2.5, agua 7',
  'agua 8, espuma 3, agua 5, espuma 2, agua 6',
  'agua 9, espuma 2, agua 13',
]
misma_medida('Fallingwater', fw, 24)
d['arquitectos']['Frank Lloyd Wright'] = {
  'nota': 'Fallingwater de frente: la torre de piedra, las terrazas de hormigón ocre, las ventanas con marcos rojo Cherokee, un poco de verde a los costados y, abajo, el agua con la cascada.',
  'direccion': 'horizontal', 'escala': 0.72, 'grosor': 1, 'separacion': 0.55, 'lineas': fw,
}
fl = [f'piedra 1.5, (fachada 1, vidrio 0.6) x{12 - abs(i - 3)}, fachada 0.8, piedra 2.5' for i in range(7)]
d['arquitectos']['D. H. Burnham & Company'] = {
  'nota': 'El Flatiron desde la punta: líneas verticales apoyadas en la vereda, la del centro (la proa) más alta y las de los costados un poco más bajas por la perspectiva. Arriba la cornisa de piedra, después las filas de ventanas y abajo el basamento.',
  'direccion': 'vertical', 'alinear': 'fin', 'alto': 150, 'escala': 0.8, 'grosor': 1, 'separacion': 0.45, 'lineas': fl,
}

# ---- Décadas: una obra (o un estilo) característica de cada una ----
dec = {}

# 1900 · Teatro Colón (Buenos Aires, 1908)
colon = ['pizarra 12', 'pizarra 18', 'marmol 30',
         '(marmol 2, vidrio 1.5) x8, marmol 2',
         'marmol 30',
         '(marmol 1.25, vidrio 2.25) x8, marmol 2',
         '(marmol 1.25, vidrio 2.25) x8, marmol 2',
         'marmol 30', '(marmol 2, vidrio 1.5) x8, marmol 2', 'piedra 34']
dec['1900'] = {'obra': 'Teatro Colón', 'lugar': 'Buenos Aires', 'anio': '1908',
  'nota': 'Teatro Colón (Buenos Aires, inaugurado en 1908): la mansarda de pizarra, la fachada de piedra con sus ventanas y columnas, y la escalinata.',
  'direccion': 'horizontal', 'alinear': 'centro', 'grosor': 1, 'separacion': 0.6, 'lineas': colon}

# 1910 · Fábrica Fagus (Alfeld, 1911–1913)
fagus = ['ladrillo 30',
         '(ladrillo 1, vidrio 3) x6, vidrio 6', '(ladrillo 1, acero 3) x6, acero 6',
         '(ladrillo 1, vidrio 3) x6, vidrio 6', '(ladrillo 1, acero 3) x6, acero 6',
         '(ladrillo 1, vidrio 3) x6, vidrio 6',
         'ladrillo 30', 'ladrillo 30']
misma_medida('Fagus', fagus, 30)
dec['1910'] = {'obra': 'Fábrica Fagus', 'lugar': 'Alfeld, Alemania', 'anio': '1911–1913',
  'nota': 'Fábrica Fagus (Gropius y Meyer, 1911–1913): el muro cortina entre pilares de ladrillo y la esquina toda de vidrio, sin columna.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0.55, 'lineas': fagus}

# 1920 · Bauhaus Dessau (1925–1926)
bau = ['hormigon 30', 'hormigon 30',
       '(vidrio 2.2, reflejo 0.5) x11, vidrio 0.3',
       '(vidrio 2.2, acero 0.5) x11, vidrio 0.3',
       '(vidrio 2.2, reflejo 0.5) x11, vidrio 0.3',
       '(vidrio 2.2, acero 0.5) x11, vidrio 0.3',
       'hormigon 30', '- 2, vidrio 26, - 2']
misma_medida('Bauhaus', bau, 30)
dec['1920'] = {'obra': 'Bauhaus', 'lugar': 'Dessau, Alemania', 'anio': '1925–1926',
  'nota': 'Bauhaus de Dessau (Gropius, 1925–1926): el ala de talleres con el muro cortina de vidrio entre la losa blanca de arriba y el basamento retirado.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0.55, 'lineas': bau}

# 1930 · Edificio Kavanagh (Buenos Aires, 1934–1936)
alturas = [5, 5, 9, 9, 13, 13, 21, 21, 13, 13, 9, 9, 5, 5]
kav = [f'hormigon 1.2, (vidrio 0.5, hormigon 0.9) x{h}' for h in alturas]
dec['1930'] = {'obra': 'Edificio Kavanagh', 'lugar': 'Buenos Aires', 'anio': '1934–1936',
  'nota': 'Edificio Kavanagh (Sánchez, Lagos y de la Torre, 1934–1936): la torre angosta y los retiros en bloque que bajan hacia los costados, como en el art déco, en líneas verticales apoyadas en la calle.',
  'direccion': 'vertical', 'alinear': 'fin', 'alto': 150, 'grosor': 1, 'separacion': 0.5, 'lineas': kav}

# 1940 · Ministerio de Educación y Salud, Río de Janeiro (1936–1945)
mes = ['hormigon 26'] + ['hormigon 1, brise 24, hormigon 1'] * 7 + ['hormigon 26',
       tramos([(1, 2, 'hormigon'), (6, 7, 'hormigon'), (8.5, 17.5, 'azulejo'), (19, 20, 'hormigon'), (24, 25, 'hormigon')], 26),
       tramos([(1, 2, 'hormigon'), (6, 7, 'hormigon'), (8.5, 17.5, 'azulejo'), (19, 20, 'hormigon'), (24, 25, 'hormigon')], 26)]
misma_medida('MES', mes, 26)
dec['1940'] = {'obra': 'Ministerio de Educación y Salud', 'lugar': 'Río de Janeiro', 'anio': '1936–1945',
  'nota': 'Ministerio de Educación y Salud de Río (Lúcio Costa, Niemeyer y equipo, con Le Corbusier, 1936–1945): el bloque con los brise-soleil, los pilotes y, abajo, el muro de azulejos azules.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0.5, 'lineas': mes}

# 1950 · Seagram (la que salió del gráfico y quedó)
seagram = ['filete 24'] * 10
seagram[5] = 'filete 18, cielo 6'
seagram[9] = 'filete 18, cielo 6'
dec['1950'] = {'obra': 'Seagram Building', 'lugar': 'Nueva York', 'anio': '1954–1958',
  'nota': 'Seagram Building (Mies van der Rohe y Philip Johnson, 1954–1958): los perfiles verticales de bronce, casi todos en sombra; dos se encienden abajo.',
  'direccion': 'vertical', 'grosor': 1, 'separacion': 1.2, 'lineas': seagram}

# 1960 · Congreso Nacional, Brasilia (1958–1960)
cong = []
torres = [(18, 19.6, 'hormigon'), (20.4, 22, 'hormigon')]
cupula = {4: 3, 5: 6.5, 6: 9, 7: 10.5}
cuenco = {4: 14, 5: 11.5, 6: 8, 7: 4}
for fila in range(8):
    segs = list(torres)
    if fila in cupula: segs.insert(0, (9 - cupula[fila] / 2, 9 + cupula[fila] / 2, 'hormigon'))
    if fila in cuenco: segs.append((31 - cuenco[fila] / 2, 31 + cuenco[fila] / 2, 'hormigon'))
    cong.append(tramos(segs, 40))
cong += ['hormigon 40', 'agua 40', 'agua 40']
misma_medida('Congreso', cong, 40)
dec['1960'] = {'obra': 'Congreso Nacional', 'lugar': 'Brasilia', 'anio': '1958–1960',
  'nota': 'Congreso Nacional de Brasilia (Niemeyer, 1958–1960): las dos torres en el centro, la cúpula del Senado a la izquierda, el cuenco de la Cámara a la derecha, la explanada y el espejo de agua.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0.6, 'lineas': cong}

# 1970 · Centro Pompidou (París, 1971–1977)
tubos = ['azul', 'azul', 'verde', 'sol', 'acero', 'azul', 'verde', 'verde', 'sol', 'acero', 'azul', 'verde', 'sol', 'azul']
pomp = []
for k, c in enumerate(tubos):
    if 2 <= k <= 11:
        y = 19 - (k - 2) * 1.8
        pomp.append(f'{c} {f(y)}, rojo 2, {c} {f(24 - y - 2)}')
    else:
        pomp.append(f'{c} 24')
misma_medida('Pompidou', pomp, 24)
dec['1970'] = {'obra': 'Centro Pompidou', 'lugar': 'París', 'anio': '1971–1977',
  'nota': 'Centro Pompidou (Piano, Rogers y Franchini, 1971–1977): los conductos de colores en vertical (azul el aire, verde el agua, amarillo la electricidad) y la escalera mecánica roja que los cruza en diagonal.',
  'direccion': 'vertical', 'grosor': 1, 'separacion': 0.6, 'lineas': pomp}

# 1980 · Pirámide del Louvre (París, 1989)
pir = [f'(reflejo 1.6, acero 0.4) x{k}' for k in range(1, 11)] + ['piedra 26']
dec['1980'] = {'obra': 'Pirámide del Louvre', 'lugar': 'París', 'anio': '1989',
  'nota': 'Pirámide del Louvre (I. M. Pei, 1989): líneas cada vez más largas, de vidrio con su trama de acero, sobre el patio de piedra.',
  'direccion': 'horizontal', 'alinear': 'centro', 'grosor': 1, 'separacion': 0.5, 'lineas': pir}

# 1990 · Biblioteca Nacional (Buenos Aires, inaugurada en 1992)
bn = ['hormigon 30', 'hormigon 2, (vidrio 2, hormigon 1) x8, hormigon 4', 'hormigon 30',
      'hormigon 2, (vidrio 2, hormigon 1) x8, hormigon 4', '- 4, hormigon 22, - 4',
      tramos([(6, 8, 'hormigon'), (12, 14, 'hormigon'), (16, 18, 'hormigon'), (22, 24, 'hormigon')], 30),
      tramos([(6, 8, 'hormigon'), (12, 14, 'hormigon'), (16, 18, 'hormigon'), (22, 24, 'hormigon')], 30),
      tramos([(6, 8, 'hormigon'), (12, 14, 'hormigon'), (16, 18, 'hormigon'), (22, 24, 'hormigon')], 30),
      'follaje 30']
misma_medida('Biblioteca Nacional', bn, 30)
dec['1990'] = {'obra': 'Biblioteca Nacional Mariano Moreno', 'lugar': 'Buenos Aires', 'anio': '1962–1992',
  'nota': 'Biblioteca Nacional (Testa, Bullrich y Cazzaniga; proyecto de 1962, inaugurada en 1992): el gran volumen de hormigón levantado sobre cuatro apoyos, encima de la plaza.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0.55, 'lineas': bn}

# 2000 · 30 St Mary Axe (Londres, 2003–2004)
perfil = [4, 8, 11, 13, 14, 14.5, 14.5, 14, 13, 12, 10.5, 9]
gk = []
for k, w in enumerate(perfil):
    # una franja oscura que gira: su posición se corre en cada línea
    p = ((k * 0.17) % 1) * w
    a, b = p, min(p + w * 0.22, w)
    segs = [(0, a, 'reflejo'), (a, b, 'vidrio'), (b, w, 'reflejo')]
    segs = [s for s in segs if s[1] - s[0] > 0.05]
    gk.append(', '.join(f'{c} {f(y - x)}' for x, y, c in segs))
dec['2000'] = {'obra': '30 St Mary Axe', 'lugar': 'Londres', 'anio': '2001–2004',
  'nota': '30 St Mary Axe (Foster + Partners, 2001–2004): el perfil de bala en líneas horizontales y la franja de vidrio oscuro que gira en espiral.',
  'direccion': 'horizontal', 'alinear': 'centro', 'grosor': 1, 'separacion': 0.45, 'lineas': gk}

# 2010 · Bosque Vertical (Milán, 2014)
bosco = []
for fila in range(16):
    a = tramos([(0, 10, 'gris-bosco')], 10)
    verdes = [(x, x + 1.6, 'follaje') for x in ([0.6, 4.4, 8] if fila % 2 == 0 else [2.4, 6.2])]
    torre_a = tramos([(0, verdes[0][0], 'gris-bosco')] + sum([[v, (v[1], (verdes[i + 1][0] if i + 1 < len(verdes) else 10), 'gris-bosco')] for i, v in enumerate(verdes)], []), 10)
    if fila >= 5:
        vb = [(x, x + 1.4, 'follaje') for x in ([0.5, 4, 7] if fila % 2 else [2.2, 5.6])]
        torre_b = sum([[v, (v[1], (vb[i + 1][0] if i + 1 < len(vb) else 9), 'gris-bosco')] for i, v in enumerate(vb)], [])
        torre_b = [(0, vb[0][0], 'gris-bosco')] + torre_b
        linea = torre_a + ', - 3, ' + tramos([(x0, x1, c) for x0, x1, c in torre_b if x1 - x0 > 0.01], 9)
    else:
        linea = torre_a
    bosco.append(re.sub(r'(?:, )?\S+ 0(?=,|$)', '', linea))
bosco.append('piedra 22')
dec['2010'] = {'obra': 'Bosque Vertical', 'lugar': 'Milán', 'anio': '2009–2014',
  'nota': 'Bosque Vertical (Stefano Boeri, 2009–2014): las dos torres de distinta altura, con los balcones plantados que alternan de un piso a otro.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0.45, 'lineas': bosco}

# 2020 · M+ (Hong Kong, 2021)
mmas = ['verde-m 22', 'pantalla 22', 'verde-m 22', 'pantalla 22', 'verde-m 22', 'pantalla 22', 'verde-m 22']
mmas = [f'- 9, {l}, - 9' for l in mmas] + ['hormigon 40', 'hormigon 40',
        tramos([(3, 5, 'hormigon'), (35, 37, 'hormigon')], 40), 'agua 40']
misma_medida('M+', mmas, 40)
dec['2020'] = {'obra': 'M+', 'lugar': 'Hong Kong', 'anio': '2021',
  'nota': 'Museo M+ (Herzog & de Meuron, 2021): la T invertida, con la torre plana de fachada-pantalla sobre el basamento horizontal, frente a la bahía.',
  'direccion': 'horizontal', 'grosor': 1, 'separacion': 0.5, 'lineas': mmas}

d['decadas'] = dec

s = json.dumps(d, ensure_ascii=False, indent=2)
s = re.sub(r'\{\s*"claro": ("[^"]+"),\s*"oscuro": ("[^"]+")\s*\}', r'{ "claro": \1, "oscuro": \2 }', s)
open(destino, 'w').write(s + '\n')
print('ok', list(dec))
