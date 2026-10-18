#!/bin/sh
# Levanta la página de prueba de la gráfica en http://127.0.0.1:8001/
# Usa la app de www/ (enlaces js, css, data…) y lee las fotos de referencia de
# ~/medianeras-originales, que no entran al repo: el enlace "referencias" se crea acá.
cd "$(dirname "$0")"
[ -e referencias ] || ln -s "$HOME/medianeras-originales/referencias/simbolos" referencias
exec python3 -m http.server 8001 --bind 127.0.0.1
