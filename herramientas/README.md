# Herramientas (no se publican)

Están fuera de `www/`, así que GitHub Pages no las sube. Sirven para trabajar la gráfica y revisar la app.

## `prueba/`: página de prueba de la gráfica

```sh
herramientas/prueba/servir.sh      # http://127.0.0.1:8001/
```

- `index.html`: cada símbolo que tiene foto de referencia, al lado de su foto, en claro y en oscuro, más la pantalla de carga.
- `todos.html`: todos los símbolos de `simbolos.json`, cargados igual que en la app.
- `equilibrio.html`: todos los íconos de obras en cuadrados (como las tapas), para comparar tamaños y fondos.
- `fondos.html`: fondos para elegir, obra por obra: cada símbolo con su foto y tres colores de fondo, como tapa en claro y en oscuro.
- `marcos.html`: cada símbolo con fondo, con el marco en tinta y con el color invertido de su fondo, para comparar.
- `fotos.html`: cómo entran las fotos en las tapas (enteras o con `encuadre`).
- `completa.html`: la página de prueba completa (logo, estilos, banderas, décadas, materiales, programas, tapas, carga).
- `carga-a.svg.html`: la versión A de la pantalla de carga (molinete escalonado), guardada como alternativa. La B es la de `www/index.html`.

La página usa la app de verdad: `js`, `css`, `data`, `fuentes`, `img` e `index-app.html` son enlaces a `www/`. Las fotos de referencia **no entran al repo**: `servir.sh` crea el enlace `referencias` a `~/medianeras-originales/referencias/simbolos`, y git lo ignora.

## `simbolos/`: armadores de `simbolos.json` (historial)

Son los scripts de Python que dibujaron los símbolos en cada ronda (`simbolos.py` es la primera y `simbolos5.py` la última). Quedan como registro de cómo se midió cada obra sobre su foto.

**La fuente es `www/data/simbolos.json`**, y los cambios nuevos se hacen ahí directamente. Correr un armador pisa el archivo y borra cualquier cambio hecho a mano. Solo las dos últimas rondas se pueden volver a correr:

```sh
cd herramientas/simbolos
python3 simbolos4.py base-ronda4.json /tmp/ronda5.json
python3 simbolos5.py /tmp/ronda5.json ../../www/data/simbolos.json
```

## `capturas/`: capturas de la app con Chrome headless

Con la app levantada en el puerto 8000:

```sh
herramientas/capturas/ver.sh "/arquitecto/frank-lloyd-wright" flw.png        # una vista, tema claro
herramientas/capturas/tanda.sh oscuro "/:inicio" "decada/1950:d1950"         # varias, tema oscuro
python3 herramientas/capturas/unir.py juntas.png inicio-o d1950-o             # lado a lado
```

Las imágenes quedan en `capturas/salida/`, que git ignora. Con `VIRT=1` se usa tiempo virtual: las capturas son estables, pero sin IndexedDB ni imágenes de carga diferida (ver "Problemas conocidos" en `LOG.md`).
