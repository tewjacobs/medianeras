#!/bin/zsh
# ver.sh <ruta-hash> <nombre.png> [alto] [oscuro]
# Captura la app (http://127.0.0.1:8000) a 500 px de ancho con Chrome headless y la guarda en salida/.
# Con VIRT=1 usa tiempo virtual (capturas estables, pero sin IndexedDB ni imágenes "lazy").
cd "$(dirname "$0")"
mkdir -p salida
P=$(mktemp -d)
H=${3:-1400}
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
  --user-data-dir=$P --window-size=500,$H ${VIRT:+--virtual-time-budget=9000}${VIRT:---timeout=18000} \
  ${4:+--force-dark-mode} --screenshot=salida/$2 "http://127.0.0.1:8000/#$1" >/dev/null 2>&1
rm -rf $P
