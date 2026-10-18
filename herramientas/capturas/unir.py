# unir.py salida.png nombre1 nombre2 …: pone lado a lado capturas de salida/ (sin .png).
import sys, os
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'salida')
salida, nombres = sys.argv[1], sys.argv[2:]
ims = [Image.open(os.path.join(D, n + '.png')) for n in nombres]
out = Image.new('RGB', (sum(i.width for i in ims), max(i.height for i in ims)), 'white')
x = 0
for im in ims:
    out.paste(im, (x, 0)); x += im.width
out.save(os.path.join(D, salida))
