# Medianeras: estado y bitácora

## Qué es

Medianeras es un catálogo personal de obras de arquitectura con un diario de visitas. Es una PWA hecha con HTML, CSS y JavaScript sin frameworks ni compilación, pensada primero para el iPhone, que funciona sin conexión. Se publica en GitHub Pages desde `www/` en cada push a `main` (repo `tewjacobs/medianeras`), con el dominio propio **https://arqivo.com.ar**. Más adelante puede pasar a app nativa con Capacitor.

Se usa como Letterboxd o RYM: un inicio con filas temáticas y una página por arquitecto, estilo, material, programa, lugar, década y año. La estética es de impreso de los 60/70: tapas cuadradas con marco de color y símbolos de líneas paralelas.

## Estado

**20 de octubre de 2026.** La app se publica en https://arqivo.com.ar (dominio propio con https). El nombre definitivo de la app sigue abierto (ver Pendientes).

**18 de octubre de 2026, noche.** Rediseño completo y varias rondas de ajustes visuales, todo publicado.

- Service worker en `v21`.
- Pantalla de carga: skyline "El siglo". Botón de visita: sigue el "+" (la Price Tower quedó para más adelante).

## Cómo retomar

```sh
cd ~/medianeras
git status && git log --oneline -5      # ver dónde quedó
cd www && python3 -m http.server 8000   # la app en http://127.0.0.1:8000/
```

- Para ver los cambios después de tocar la app, subí `VERSION` en `www/sw.js` y recargá dos veces (o tocá "Actualizar" en el aviso).
- Para probar en el iPhone en la misma red: `python3 -m http.server 8000 --bind 0.0.0.0` y abrí `http://<ip-de-la-compu>:8000/`. La ubicación ("Cerca mío") solo anda con https, es decir, en la versión publicada.
- Para publicar, hacé un push a `main`. El workflow `.github/workflows/pages.yml` sube `www/` tal cual y queda en https://arqivo.com.ar.
- Para la página de prueba de la gráfica (símbolos al lado de sus fotos), corré `herramientas/prueba/servir.sh` y abrí `http://127.0.0.1:8001/`. Lee las fotos de referencia de `~/medianeras-originales` con un enlace que no entra al repo.
- Para capturar la app con Chrome headless: `herramientas/capturas/ver.sh` y `tanda.sh`. Detalles en `herramientas/README.md`.

## Qué hay en cada carpeta

| Carpeta / archivo | Qué es |
|---|---|
| `CLAUDE.md`, `LOG.md` | Reglas de trabajo y este registro. Están fuera de `www/`, así que no se publican. |
| `README.md` | Documentación para el usuario: estructura, rutas, cómo cargar obras, perfiles y símbolos. |
| `.github/workflows/pages.yml` | Publica `www/` en GitHub Pages. |
| `herramientas/` | No se publica. `prueba/` es la página de prueba de la gráfica; `simbolos/`, los armadores de `simbolos.json` (historial); `capturas/`, los scripts de capturas. Ver su README. |
| `www/index.html` | La única página. Incluye la pantalla de carga (planta de la Price Tower) y la cabecera. |
| `www/css/estilos.css` | Tokens de color de los dos temas, tipografías y todas las vistas. |
| `www/js/` | `app.js` (rutas), `datos.js` (carga, perfiles, colores, símbolos), `filtros.js`, `filas.js` (filas del inicio), `ui.js` (piezas compartidas), `grafica.js` (logo, símbolos, separadores), `tema.js`. |
| `www/js/vistas/` | Una vista por sección: `inicio`, `obras`, `perfil`, `obra`, `mapa`, `diario`, `listas`, `nueva-visita`. |
| `www/js/plataforma/` | Todo lo que toca el dispositivo (almacén, ubicación, fotos, compartir, preferencias). |
| `www/data/` | `obras.json`, `diario.json`, `listas.json`, `perfiles.json` (optativo), `simbolos.json` (optativo). |
| `www/fuentes/` | Archivo (variable), IBM Plex Mono y Libre Caslon Text, en woff2 y con su licencia OFL. |
| `www/img/` | Fotos del catálogo (`obras/<id>/`) y del diario (`diario/<id>/`). |
| `www/iconos/`, `www/vendor/leaflet/` | Íconos de la app (hechos con el logo) y Leaflet local. |

**No tocar:** `~/medianeras-originales/` es del usuario y es solo de lectura. Tiene las fotos originales (`flatiron/`, `guggenheim/`) y las referencias de símbolos (`referencias/simbolos/<obra>/`). Las referencias son de terceros: sirven solo para mirar y nunca se copian al repo.

## Decisiones tomadas

- **Paletas.**
  - El tema claro es "Another Green World" de Eno: blanco cálido, azul montaña, verde follaje, celeste cielo, arena y el rojo como acento mínimo.
  - El tema oscuro es "Pinback": negro azulado, azul violáceo, verde pino y tierras, con texto blanco.
  - Hay cuatro colores de marco por tema, con nombres fijos (`petroleo`, `follaje`, `cielo`, `mar`) que cambian de valor según el tema.
  - Hay selector de tema (automático, claro u oscuro), guardado en el teléfono.
- **Color del marco.** Sale del `color` de la obra. Si no tiene, del estilo o de su ancestro más cercano en `perfiles.json`. Si tampoco, se calcula un hash estable del estilo raíz.
- **Tipografías.**
  - Solo se usan Archivo, Plex Mono y Caslon, nunca la fuente del sistema.
  - Archivo en ancho normal se parece mucho a Arial, así que las etiquetas y pestañas van condensadas en mayúsculas y los títulos de las tapas, un poco anchos.
- **Logo.**
  - Es la variante 5b·2 "Calm": campo rojo, ventanita de marco negro y dos edificios con su costado en perspectiva roja (sube 2 cada 3), sobre una grilla de 48 × 48 con coordenadas enteras.
  - Con él se hicieron los íconos de la app.
- **Pantalla de carga.** Skyline de Buenos Aires «El siglo» (S3): un edificio por década de la colección Argentina sobre una línea de suelo; cada uno se construye desde abajo, línea por línea. La primera vez que se entra a la app se muestra completa (espera a que termine el skyline; se recuerda con la preferencia `carga-vista`); las siguientes se va apenas cargan los datos. El SVG está inline en `www/index.html` (se regenera con `herramientas/prueba/exportar-skyline.html`). Las versiones de la Price Tower quedaron en `herramientas/prueba/`.
- **Sistema gráfico: flechas** (en `flecha()` de `www/js/ui.js`, para reusar):
  - **F2, escalonada:** rayas apiladas de distinto largo que forman la punta. Va en VER MÁS, la lista de Explorar, Todas las obras y el visor de fotos (dada vuelta para "anterior").
  - **F1, paralela:** tres líneas paralelas; las de afuera doblan y se juntan en la punta. Va en "Cómo llegar".
- **Cabecera y detalles.**
  - Todo en una fila: logo (42 px) y nombre a la izquierda; búsqueda S1 (tres filetes, el del medio rojo en foco) y el botón de tema a la derecha. En el celular la búsqueda está plegada en la lupa.
  - "Todas las obras" es la T2: franja en el rojo de Medianeras (`--logo-rojo`) entre filetes dobles, en los dos temas.
  - Chips y botones secundarios con fondo del color de la familia al 16 % (30 % en oscuro, para que se distingan).
- **Cabecera de la portada en todas las vistas:** logo y "medianeras" (llevan al inicio) y la palabra de la sección (OBRA, ESTILO, MAPA…) en el color de acento. En el celular, la sección va debajo del nombre; desde 600 px, al lado. El nombre de la obra o del perfil va solo en el título de la página y en el de la pestaña del navegador.
- **Por década (inicio):** cada fila con el símbolo de la década en chico (colección Mundo), el nombre y la cantidad en un chip del color de la década. Sin líneas punteadas.
- **Paneles en vez de páginas:** "Ver en el mapa" (desde una obra) abre un mapa en un panel con "Agrandar" a `#/mapa?obra=…`; el botón VISITA y "Registrar visita" abren la nueva visita en un panel (en una obra, viene elegida; en un perfil, sus obras primero). `#/nueva` sigue como página para links y para editar.
- **Compu (desde 900 px):** la ficha de obra y los perfiles llevan arriba dos columnas a la misma altura (tapa e info; texto y símbolo). Debajo, bloques separados por filetes.
- **Ficha de obra.** Arriba, siempre, la tapa, el nombre, los años y arquitectos, y los botones. Pestañas DATOS · UBICACIÓN · FOTOS · PLANOS (las vacías no aparecen). Las visitas van aparte, como reseñas: las 3 más recientes y VER MÁS a `#/obra/<id>/visitas`. Las fotos y planos van en una grilla de miniaturas que abre un visor a pantalla completa, con flechas, gesto y teclado.
- **Símbolos.**
  - Cada perfil tiene un dibujo propio de líneas paralelas, guardado como dato en `simbolos.json`.
  - Se dibujan con el método de `CLAUDE.md`: mirar las referencias, comparar y corregir.
  - Sin símbolo, se muestra el neutro: una línea fina en el color de la familia.
  - Un estilo sin símbolo usa el de su ancestro.
  - Un programa con paréntesis, si no tiene símbolo propio, usa el de la parte anterior al paréntesis.
  - Una obra sin foto muestra el símbolo de su arquitecto o, si no tiene, el de su estilo.
  - Banderas y obras de arquitectos van chicas; estilos y décadas, grandes.
- **Décadas: Argentina y Mundo.**
  - Hay dos colecciones en `simbolos.json` (`decadas.argentina` y `decadas.mundo`), y más adelante una por país.
  - Las páginas `#/decada/…` y `#/anio/…` usan Mundo. La colección de un país aparece en su contexto: con `?pais=Argentina` o desde el perfil de Argentina.
  - La década de 2020 argentina no tiene símbolo y usa el neutro.
  - Los años usan el símbolo de su década, con una tira de diez marcas en la que su año va en rojo.
- **Fotos y derechos.**
  - Las fotos del catálogo son propias del usuario ("Todos los derechos reservados"). Las de ejemplo y los íconos son CC0.
  - Las referencias de símbolos son de terceros y no entran al repo.
  - En las tapas, la foto entra entera y el marco llena lo que sobra. Con el campo optativo `fotos[].encuadre`, se recorta al cuadrado.
  - En la ficha, las fotos van en su proporción original.
- **Perfiles sin obras.** Por ahora no existen: no hay página, link ni entrada en los índices. "Moderno" existe porque sus subestilos tienen obras.
- **Cabecera.** En el celular tiene dos filas (logo o título con el botón de tema; búsqueda con la lupa). Desde 600 px va en una fila. Escribir en la búsqueda lleva a `#/obras` y filtra.
- **Skills de Matt Pocock (`mattpocock/skills`).** Por ahora no se instala ninguna. Si algún día hace falta, la candidata es `diagnosing-bugs`: copiar solo su carpeta a `.claude/skills/` de este repo. Nunca a nivel global, porque en esta compu se trabaja también en otro proyecto.
- **Dominio.** `arqivo.com.ar`, comprado en DonWeb (nameservers `ns1`/`ns2.donweb.com`, no tocarlos). Zona DNS en DonWeb: 4 registros A a `185.199.108.153`, `.109.153`, `.110.153` y `.111.153`, 4 AAAA a `2606:50c0:8000::153` a `8003::153`, y CNAME `www` a `tewjacobs.github.io`. En GitHub: Settings → Pages → Custom domain `arqivo.com.ar` con Enforce HTTPS. Como se publica con el workflow de Actions, no hace falta archivo `CNAME`. `www`, `http` y la dirección vieja (`tewjacobs.github.io/medianeras`) redirigen a `https://arqivo.com.ar`. El certificado es de Let's Encrypt y lo renueva GitHub.
- **Visitas del teléfono.** Se leen de IndexedDB sin bloquear: el inicio y las grillas se pintan enseguida y las filas de visitas se completan después.

## Pendientes

- **Nombre de la app.** "Medianeras" se descartó para el dominio (`medianeras.com.ar` está ocupado) y se compró `arqivo.com.ar`. La app sigue diciendo "Medianeras" hasta decidir. Gustos del usuario que salieron: nombres que hablan de cómo se mira y no de lo que se mira (como Letterboxd), lugares de paso de mediados de siglo (La Guardia, Pan Am), palabras cortas y duras, cosas que suenan a movimiento o antología (Chicago School, números de año) y una melancolía rioplatense (Cortázar, Sur). Propuestas con `.com.ar` libre al 20/10 según whois de NIC: Contrafrente (recomendada), Celosía (segunda), Pared ciega, Planta libre, Escuela del Sur, Usonia, Ochava 96. Ocupados: ochava, medianera, cota, cotacero, cenital, corte, bau, terrazo, vidriera, pulmon. El usuario vuelve con sus elegidas; el próximo paso es mostrarlas en la página de prueba con el logo y las tipografías, en claro y oscuro. No comprar otro dominio antes.
- Price Tower: queda para más adelante (opciones en `herramientas/prueba/price-tower2.html`, a partir de la planta). El botón de visita sigue con el "+". La pantalla de carga actual (molinete) se lee como una esvástica: se reemplaza por el skyline.
- Revisar el `resumen` y la `descripcion` del Guggenheim y el `resumen` del Flatiron (los escribió Claude; reemplazar o corregir).

- Media estrella en los puntajes: hoy se redondea (un 4,5 se ve como 5).
- Probar el ancho de 320 px en un dispositivo real; las capturas automáticas no bajan de 500 px.
- Sumar fotos de referencia para los símbolos que se hicieron sin foto.
- Hay símbolos de materiales y programas sin obras que hoy no se ven en la app (madera, vidrio, etc.), y décadas que no tienen obras.
- La Ballena Azul y el CCTV son las aproximaciones más libres.

## Problemas conocidos

- **Capturas con Chrome headless.**
  - Con `--virtual-time-budget`, IndexedDB no responde: las filas de visitas quedan como esqueleto y las imágenes `loading="lazy"` no cargan.
  - Con `--timeout`, a veces la captura sale con la pantalla de carga a medio desaparecer.
  - Ninguna de las dos cosas pasa en un navegador normal.
- **Chrome de esta Mac en modo oscuro.** Está configurado en oscuro aunque macOS esté en claro, así que el modo automático lo muestra oscuro.
- **Armadores de símbolos.** Están en `herramientas/simbolos/` como historial, pero la fuente es `simbolos.json`: los cambios nuevos se hacen ahí directamente. Volver a correr un armador pisa el archivo.
- **Mapa en oscuro.** Los mosaicos de OpenStreetMap se oscurecen con un filtro CSS y no son mosaicos oscuros propios.

## Bitácora

### 17 de octubre de 2026

- Se aprobó el plan del rediseño (inicio por filas, perfiles, estética impresa), con un punto de control después de la página de prueba de la gráfica.
- **Paso 1:**
  - fuentes propias copiadas a `www/fuentes/`;
  - tokens de color para claro y oscuro;
  - fichas cuadradas ("tapas").
- **Paso 1b:** `grafica.js` y una página de prueba local. Varias rondas de ajustes:
  - Se encontró por qué todo se veía oscuro (el modo de Chrome) y se sumó el selector de tema.
  - Paletas: primero Eno y Jesus Lizard; después claro "Another Green World" y oscuro Pinback, con colores más fuertes.
  - Se sacaron los patrones al azar ("trama" y "círculo rayado").
  - Logo: siete opciones, después tres variantes de 5b; elegida la 5b·2.
  - Pantalla de carga: de la M de arcos a la Price Tower.
  - Nacieron los símbolos por perfil como datos (`simbolos.json`, formato documentado en el README): banderas, Fallingwater, Flatiron, estilos, materiales, programas y una obra por década.

### 18 de octubre de 2026

- **Símbolos:**
  - Se adoptó el método de comparar con las fotos de referencia.
  - Se rehicieron Kavanagh, Banco de Londres, Curutchet, Casa sobre el Arroyo, SOMISA, Recoleta, Puente de la Mujer, Guggenheim Bilbao, 30 St Mary Axe y CCTV.
  - Después, Eames, Stoclet, Paimio, La Pedrera y el CCK con la Ballena Azul.
  - Las décadas se separaron en Argentina y Mundo.
- **Logo y carga:** logo exacto sobre la grilla y pantalla de carga B.
- **Commit de guardado:** `b1025b2`.
- **Pasos 2 a 5:**
  - Datos: perfiles, slugs, jerarquía de estilos, estadísticas de visitas y color por familia.
  - Filtros nuevos: estado y año, con orden y "visitadas".
  - Inicio por filas y grilla en `#/obras`. Los links viejos con filtros redirigen solos.
  - Perfiles e índices, y una ficha de obra con todos los datos como links.
  - Collage en las listas, colores en el mapa e íconos de la app.
  - `perfiles.json` y README.
- **Correcciones:**
  - Los símbolos no mostraban sus colores propios en la app: faltaba registrarlos al cargar los datos.
  - Décadas Mundo y del país según el contexto.
  - Fotos enteras con encuadre optativo; galería en proporción original.
  - Cabecera con búsqueda.
  - Tipografía sin la fuente del sistema y textos chicos más grandes.
  - Alineación en pantallas anchas.
- **Perfiles sin obras:** ya no existen.
- **Commit `0fc5c6c`:** commit y push a `main`.
- **Ronda de la tarde:** Seagram, Villa Savoye (Moderno) y Biblioteca Nacional rehechos con sus fotos; opciones de Price Tower (descartadas por ahora) y del skyline; cabecera de la portada en todas las vistas, décadas con símbolo, ficha y perfiles en dos columnas en la compu, mapa y visita en paneles; ficha con pestañas, visor de fotos, flechas propias. Se sacó la foto 4 del Guggenheim.
- **Última ronda:** descripción de la obra en la cabecera de la ficha (o, si no hay, chips de estilo, década y lugar); bordes exactos en los símbolos medidos (Savoye, Biblioteca); Colón y Guggenheim de Nueva York rehechos con fotos nuevas (`herramientas/simbolos/simbolos7.py`); diario en grilla de entradas compactas con recuadros de color rotando por la paleta (3 por fila en la compu, 2 en tablet, 1 en el celular).
- **Cierre:** Guggenheim (orgánica) con vereda y calle; ficha con `resumen` y descripción completa con "Ver más"; skyline S3 en la pantalla de carga.
- **Cierre del día:** sección "Cómo hablarme" en `CLAUDE.md`; techo de cristal centrado en el Guggenheim (orgánica); la pantalla de carga se ve completa solo la primera vez; commit y push de todo.
- **Organización:**
  - Se crearon `CLAUDE.md` y `LOG.md`.
  - Se revisaron las skills de `mattpocock/skills`. Decisión: no instalar ninguna por ahora (ver Decisiones).
  - La página de prueba, los armadores de símbolos y los scripts de capturas pasaron del scratchpad temporal a `herramientas/`. La página de comparación ahora muestra todos los símbolos con foto y las lee de `~/medianeras-originales`.

### 20 de octubre de 2026

- **Dominio propio:** se conectó `arqivo.com.ar` (DonWeb) a GitHub Pages con https, paso a paso (detalle en Decisiones). Verificado desde la compu: certificado propio, redirecciones de `www`, `http` y la dirección vieja, y manifiesto y service worker accesibles. En el iPhone: "Cerca mío" pidió permiso de ubicación y funcionó. Antes del cambio se revisó que no hubiera visitas sin exportar en el teléfono.
- **Nombre:** primera ronda de ideas a partir de una lista de referencias del usuario (ver Pendientes). Sin decisión todavía.
