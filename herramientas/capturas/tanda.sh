#!/bin/zsh
# tanda.sh claro|oscuro ruta:nombre ... — captura varias vistas, una por una.
# Ejemplo: ./tanda.sh oscuro "/:inicio" "arquitecto/frank-lloyd-wright:flw"
cd "$(dirname "$0")"
tema=$1; shift
for r in "$@"; do
  if [ "$tema" = oscuro ]; then ./ver.sh "/${r%%:*}" "${r##*:}-o.png" 1500 oscuro; else ./ver.sh "/${r%%:*}" "${r##*:}-c.png" 1500; fi
done
