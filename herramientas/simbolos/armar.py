# Ayudas para los armadores medidos en píxeles sobre una foto (recoleta.py, colon.py).
# Una Medida pasa px de la foto a unidades del símbolo: filas de 1 con `sep` de separación.
import json, re

class Medida:
    def __init__(self, x0, x1, y0, paso_px, sep=0.3):
        self.x0, self.x1, self.y0, self.paso_px, self.sep = x0, x1, y0, paso_px, sep
        self.px = paso_px / (1 + sep)                         # px por unidad, igual en las dos direcciones
        self.ancho = self.u(x1)

    def u(self, x): return round((x - self.x0) / self.px * 4) / 4
    def fila(self, y): return round((y - self.y0) / self.paso_px)

    def lineas(self, filas, macizos):
        # macizos: [(color, x0, x1, y0, y1)] en px, pintados en orden; cada fila toma lo que pasa por su centro.
        out = []
        for r in range(filas):
            y = self.y0 + r * self.paso_px + self.px / 2
            sobre = [m for m in macizos if m[3] <= y < m[4]]
            cortes = sorted({0, self.ancho, *[self.u(x) for m in sobre for x in m[1:3]]})
            tramos = []
            for a, b in zip(cortes, cortes[1:]):
                if b <= a or a < 0 or b > self.ancho: continue
                c = '-'
                for m in sobre:
                    if self.u(m[1]) <= a and b <= self.u(m[2]): c = m[0]
                if tramos and tramos[-1][0] == c: tramos[-1][1] += b - a
                else: tramos.append([c, b - a])
            out.append(', '.join(f'{c} {round(l, 2):g}' for c, l in tramos))
        return out

    def zona(self, color, x0, x1, y0, y1, **o):
        a = self.fila(y0); b = max(a, self.fila(y1) - 1)
        return {'color': color, 'desde': self.u(x0), 'hasta': self.u(x1), 'primera': a, 'ultima': b, **o}

    def recta(self, color, xa, ya, xb, yb):
        # Banda inclinada de (xa, ya) a (xb, yb), con el borde de arriba sobre esa línea.
        return {'color': color, 'desde': self.u(xa), 'hasta': self.u(xb),
                'base': round(((ya + yb) / 2 - self.y0) / self.paso_px, 2), 'subida': round((ya - yb) / self.px, 2)}

    def arco(self, color, x0, x1, y_apoyo, alto_px):
        # Arco lleno que apoya en y_apoyo y sube alto_px.
        return {'color': color, 'desde': self.u(x0), 'hasta': self.u(x1),
                'base': round((y_apoyo - self.y0) / self.paso_px, 2), 'flecha': round(alto_px / self.px, 2), 'relleno': True}

def escribir(ruta, coleccion, clave, cambios, sacar=()):
    # Reescribe la entrada de decadas[coleccion][clave] con sus claves de siempre más `cambios`.
    texto = open(ruta).read()
    i = texto.index(f'"{clave}": {{', texto.index(f'"{coleccion}"', texto.index('"decadas"')))
    a = texto.index('{', i); prof, b, dentro = 0, a, False
    while True:                                                # fin de la entrada (llaves fuera de textos)
        ch = texto[b]
        if ch == '"' and texto[b - 1] != '\\': dentro = not dentro
        elif not dentro and ch == '{': prof += 1
        elif not dentro and ch == '}':
            prof -= 1
            if prof == 0: break
        b += 1
    entrada = json.loads(texto[a:b + 1])
    for k in sacar: entrada.pop(k, None)
    entrada.update(cambios)
    def valor(v):
        if isinstance(v, list): return '[\n' + ',\n'.join(' ' * 10 + json.dumps(c, ensure_ascii=False) for c in v) + '\n' + ' ' * 8 + ']'
        return json.dumps(v, ensure_ascii=False)
    nuevo = '{\n' + ',\n'.join(f'        "{k}": {valor(v)}' for k, v in entrada.items()) + '\n      }'
    texto = texto[:a] + nuevo + texto[b + 1:]
    json.loads(texto)
    open(ruta, 'w').write(texto)

class Lienzo:
    # Una grilla de colores: filas = líneas, columnas de 0.25 a lo largo. Se pinta en orden (lo último queda arriba).
    def __init__(self, largo, filas):
        self.n = round(largo * 4)
        self.c = [['-'] * self.n for _ in range(filas)]

    def rect(self, color, x0, x1, f0, f1):
        # De x0 a x1 (unidades) y de la fila f0 a la f1 sin incluirla.
        for f in range(max(0, f0), min(len(self.c), f1)):
            for i in range(max(0, round(x0 * 4)), min(self.n, round(x1 * 4))): self.c[f][i] = color

    def lineas(self):
        out = []
        for fila in self.c:
            tramos = []
            for col in fila:
                if tramos and tramos[-1][0] == col: tramos[-1][1] += 0.25
                else: tramos.append([col, 0.25])
            while tramos and tramos[-1][0] == '-': tramos.pop()
            out.append(', '.join(f'{c} {l:g}' for c, l in tramos) or '- 0.25')
        return out

def guardar(ruta, seccion, clave, entrada, colores, prefijo):
    # Pone (o reemplaza) seccion[clave] con `entrada` y los colores propios que empiezan con `prefijo`
    # (una expresión: 'sz-|oficinas-diario').
    texto = open(ruta).read()
    texto = re.sub(rf'    "(?:{prefijo})[^"]*": \{{[^}}]*\}},\n', '', texto)
    i = texto.index('"colores": {') + len('"colores": {\n')
    texto = texto[:i] + ''.join(f'    "{k}": {{ "claro": "{v[0]}", "oscuro": "{v[1]}" }},\n' for k, v in colores.items()) + texto[i:]
    nuevo = (f'    "{clave}": {{\n' + ',\n'.join(
        f'      "{k}": ' + ('[\n' + ',\n'.join(f'        {json.dumps(l, ensure_ascii=False)}' for l in v) + '\n      ]'
                            if k == 'lineas' else json.dumps(v, ensure_ascii=False)) for k, v in entrada.items()) + '\n    }')
    s = texto.index(f'  "{seccion}": {{')
    fin = texto.index('\n  }', s)
    if f'    "{clave}": {{' in texto[s:fin]:
        a = texto.index(f'    "{clave}": {{', s)
        b = texto.index('\n    }', a) + len('\n    }')
        texto = texto[:a] + nuevo + texto[b:]
    else:
        texto = texto[:fin] + ',\n' + nuevo + texto[fin:]
    json.loads(texto)
    open(ruta, 'w').write(texto)
