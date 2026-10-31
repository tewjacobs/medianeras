# Sede de CCTV (OMA), de noche y de tres cuartos como en referencias/simbolos/CCTV/china.png (400 px), con las caras
# medidas en px de la foto. Líneas horizontales sin separación: la cara del frente iluminada (la U invertida del
# voladizo, las dos piernas y el basamento) con la retícula diagonal de acero, más tupida abajo, donde carga más, y
# detrás las losas, los montantes y algunas ventanas cálidas; el hueco del medio vacío, con su esquina ochavada; las
# caras oscuras con las ventanas encendidas calcadas de la foto (prendidas o tenues), a la derecha y a la
# izquierda, que se juntan arriba en el voladizo; abajo, la explanada.
# Uso: cctv.py <simbolos.json> (pone decadas.mundo.2010). Necesita la foto en ~/medianeras-originales.
import sys, os
from PIL import Image
from armar import escribir, con_colores

FOTO = os.path.expanduser('~/medianeras-originales/referencias/simbolos/CCTV/china.png')
X0, X1, Y0, Y1, PASO = 52, 334, 0, 332, 3.5
# El borde izquierdo del frente iluminado, medido de arriba abajo.
BORDE = [(147, 58), (115, 105), (77, 331)]                          # dos tramos rectos: la esquina y la pierna
FRENTE = [(147, 58), (255, 97), (270, 154), (286, 231), (301, 331)] + BORDE[:0:-1]
# El hueco, sacado de la foto (la mancha del cielo): arriba, paralelo al borde del voladizo; la esquina izquierda
# ochavada y los costados que se abren hacia abajo.
HUECO = [(176, 111), (222, 128), (243, 270), (140, 270), (157, 140)]

def paralela(linea, d):
    # La misma línea corrida `d` px hacia afuera (a la izquierda de su sentido de avance).
    out = []
    for i, (x, y) in enumerate(linea):
        a, b = linea[max(0, i - 1)], linea[min(len(linea) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = (dx * dx + dy * dy) ** 0.5
        out.append((x + dy / n * d, y - dx / n * d))
    return out

# Lo oscuro que rodea el frente: a la izquierda, una banda pareja y paralela al borde; arriba, el voladizo, que se
# angosta hacia la derecha (más empinado que el frente); a la derecha, el costado de la torre.
# El techo, grueso, y la banda izquierda siguen derecho hasta encontrarse en una punta (sin escalón).
OSCURO = [(155, 14), (303, 80), (330, 331)] + paralela(BORDE, -16)[:0:-1]

def adentro(x, y, pol):
    d = False
    for (xa, ya), (xb, yb) in zip(pol, pol[1:] + pol[:1]):
        if (ya > y) != (yb > y) and x < xa + (y - ya) * (xb - xa) / (yb - ya): d = not d
    return d

def cerca(x, y, pol, d):
    # Si el punto está a menos de `d` px del borde del polígono (para el canto parejo alrededor del hueco).
    for (xa, ya), (xb, yb) in zip(pol, pol[1:] + pol[:1]):
        dx, dy = xb - xa, yb - ya
        k = max(0, min(1, ((x - xa) * dx + (y - ya) * dy) / (dx * dx + dy * dy)))
        if (x - xa - k * dx) ** 2 + (y - ya - k * dy) ** 2 < d * d: return True
    return False

def reticula(c, f, y):
    # Las diagonales de acero, contadas en celdas: corren dos celdas por fila, así los escalones son todos iguales.
    # Más separadas arriba, más tupidas en las piernas bajas y el basamento.
    paso = 32 if y < 150 else 28 if y < 240 else 24
    return (c + 2 * f) % paso < 2 or (c - 2 * f) % paso < 2

def version():
    W, H = int((X1 - X0) / (PASO / 4)), int((Y1 - Y0) / PASO)
    foto = Image.open(FOTO).convert('L').crop((X0, Y0, X1, Y1)).resize((W, H), Image.BOX).load()
    xy = lambda c, f: (X0 + (c + 0.5) * PASO / 4, Y0 + (f + 0.5) * PASO)
    grid = [['-'] * W for _ in range(H)]
    for f in range(H):
        for c in range(W):
            x, y = xy(c, f)
            if adentro(x, y, HUECO): continue
            if adentro(x, y, FRENTE):
                abajo = y > 270                                           # el basamento mira hacia otro lado: otro tono
                if cerca(x, y, HUECO, 3.2):
                    grid[f][c] = 'cc-canto'                                # el borde del hueco, liso y parejo
                elif reticula(c, f, y): grid[f][c] = 'cc-acero'
                elif f % 3 == 0: grid[f][c] = 'cc-piso'                     # detrás de la retícula: losas y ventanas
                elif f % 3 == 1 and c % 6 == 0: grid[f][c] = 'cc-montante'
                elif f % 3 == 1 and (c // 12 + f // 3) % 4 == 0: grid[f][c] = 'cc-luz'
                else: grid[f][c] = 'cc-base' if abajo else 'cc-frente'
            elif adentro(x, y, OSCURO):
                v = foto[c, f]
                grid[f][c] = 'cc-ventana' if v > 105 else 'cc-tenue' if v > 70 else 'cc-costado'
    # Las ventanas, en fajas de piso: una fila prendida y la siguiente de losa.
    for f in range(1, H, 2):
        grid[f] = ['cc-costado' if k in ('cc-ventana', 'cc-tenue') else k for k in grid[f]]
    grid += [['cc-explanada'] * W, ['cc-explanada-o'] * W]
    lineas = []
    for fila in grid:
        tramos = []
        for col in fila:
            if tramos and tramos[-1][0] == col: tramos[-1][1] += 0.25
            else: tramos.append([col, 0.25])
        while tramos and tramos[-1][0] == '-': tramos.pop()
        lineas.append(', '.join(f'{c} {l:g}' for c, l in tramos) or '- 0.25')
    return {'nota': ('Sede de CCTV (OMA, 2004–2012), de noche y de tres cuartos como en la foto: la cara del frente '
                     'iluminada (el voladizo, las dos piernas inclinadas y el basamento) con la retícula diagonal de acero, '
                     'más tupida abajo, donde carga más; el hueco del medio; la cara oscura del costado con sus ventanas '
                     'encendidas en fajas de piso; abajo, la explanada.'),
            'direccion': 'horizontal', 'separacion': 0, 'largo': W / 4, 'lineas': lineas}

COLORES = {
    'cc-frente': ('#ebe4ee', '#ebe4ee'), 'cc-piso': ('#cdc3d6', '#cdc3d6'), 'cc-montante': ('#bdb2c8', '#bdb2c8'),
    'cc-luz': ('#f3dfb4', '#f3dfb4'), 'cc-canto': ('#d8cfe0', '#d8cfe0'), 'cc-base': ('#d9d0e2', '#d9d0e2'), 'cc-acero': ('#6a6180', '#6a6180'),
    'cc-costado': ('#1d1e2b', '#1d1e2b'), 'cc-ventana': ('#e8c36a', '#e8c36a'), 'cc-tenue': ('#7d6c45', '#7d6c45'),
'cc-explanada': ('#8a8496', '#8a8496'), 'cc-explanada-o': ('#4a4658', '#4a4658'),
}

ruta = sys.argv[1]
p = version()
p['aire'] = round((1.5 + 0.06 * max(p['largo'], len(p['lineas']))) * 10) / 10
escribir(ruta, 'mundo', '2010', p, sacar=('grosor', 'alto', 'alinear', 'arcos', 'rectas', 'zonas'))
texto = con_colores(open(ruta).read(), COLORES, 'cc-')
open(ruta, 'w').write(texto)
print(len(p['lineas']), 'líneas, largo', p['largo'])
