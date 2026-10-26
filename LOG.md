# Medianeras: estado y bitácora

## Qué es

Medianeras es un catálogo personal de obras de arquitectura con un diario de visitas. Es una PWA hecha con HTML, CSS y JavaScript sin frameworks ni compilación, pensada primero para el iPhone, que funciona sin conexión. Se publica en GitHub Pages desde `www/` en cada push a `main` (repo `tewjacobs/medianeras`), con el dominio propio **https://arqivo.com.ar**. Más adelante puede pasar a app nativa con Capacitor.

Se usa como Letterboxd o RYM: un inicio con filas temáticas y una página por arquitecto, estilo, material, programa, lugar, década y año. La estética es de impreso de los 60/70: tapas cuadradas con marco de color y símbolos de líneas paralelas.

## Estado

**26 de octubre de 2026, segunda sesión (cierre).** Todo subido en `98c080a` (`v45`). En la sesión: símbolos nuevos de Infraestructura (puente japonés de Hoi An, Vietnam) y Deportivo (Monumental de River, visto desde arriba), los dos con fondo propio (`placa`); regla nueva de **misma superficie** para los íconos cuadrados (tapas sin foto, tira de "todas las obras" y lista "Por década"); página nueva `herramientas/prueba/equilibrio.html` para comparar tamaños y fondos de todos los íconos de obras.

**Próxima sesión:**
1. **Fondos, uno por uno** (decisión del usuario: cada símbolo con un fondo que le quede bien; nada de cielo celeste para todos, porque se parecería a Moderno tardío/Tenerife). Propuesta aceptada para arrancar, de a cuatro y con un par de colores cada uno en la página de prueba: Brasilia (cielo seco rosado del planalto), Pirámide del Louvre (piedra clara del patio), St Mary Axe (gris azulado de la City), CCTV (neblina amarillenta de Pekín). Mirar en `equilibrio.html`.
2. **Arreglos pedidos por el usuario:**
   - St Mary Axe apenas más gordito.
   - Villa Savoye: sacarle el verde del piso de abajo y darle un poco más de perspectiva.
   - Kavanagh: tiene un costado más alto que el otro y en la foto no es así; mirar mejor la imagen.
   - Guggenheim de Nueva York: no tiene que parecer maqueta; sacarle la base (casi sin tocar el resto).
3. **Más detalle y más líneas:** Stoclet ("quedó atrasado"), Eames ("perfecta pero con muy poquitas líneas"), CCK, Centro Cultural Recoleta, Colón y Biblioteca Nacional (la forma está bien, pero "medio fea y básica").
4. **Banco de Londres (1960s Argentina):** al usuario le resulta muy abstracto como ícono. Reemplazo propuesto: **Teatro General San Martín** (Mario Roberto Álvarez, 1960; datos de memoria, verificar). Segunda opción: los pabellones de Ciudad Universitaria. Se le pidió crear `referencias/simbolos/teatro san martin/` con 2 o 3 fotos de la fachada sobre Corrientes; esperar a que avise.
5. Instagram y dominio (ver Pendientes). Probar con el mouse el hover amarillo de "Registrar visita".
6. Más adelante: Industria (Battersea), Gobierno (Budapest), Comercio y Educación (carpetas ya listas); G0 y G5 (Inglaterra), G1, G3 y las casas de Buenos Aires (G19–G30). Para revisar: Salud parece más palacio que hospital; Vivienda unifamiliar quizás no occidental.

**26 de octubre de 2026, cierre.** Todo subido (`v44`). En la sesión: Congreso de Brasil rehecho (1960s Mundo); símbolos nuevos de Salud (Royal Infirmary de Glasgow) y Vivienda unifamiliar (casa victoriana azul de San Francisco, reemplaza a la casita de dibujo). Nueva regla del usuario: los símbolos tienen que ser globales, no todo occidental.

**Próxima sesión:**
1. Más símbolos de programas con carpeta en `referencias/simbolos/`: deportes (Deportivo), fabrica (Industria), estudios:academico (Educación), mercado:shopping (Comercio), infraestructura, politico:parliaments (Gobierno). Proponer referencias de fuera de Europa y EE. UU. si las carpetas lo permiten.
2. Instagram y dominio (ver Pendientes).
3. Probar con el mouse el hover amarillo de "Registrar visita" (claro y oscuro).
4. Más adelante: G0 y G5 (Inglaterra), G1 (torre de ventilación de Liverpool), G3 (Catedral de Manchester) y las casas de Buenos Aires (G19–G30).
5. Para revisar: Salud parece más palacio que hospital (culpa del edificio, dijo el usuario); quizás cambiarlo. Vivienda unifamiliar: quizás pasar a una casa no occidental.

**25 de octubre de 2026, cierre.** Todo subido (`v43`). En la sesión: publicado lo pendiente del 24/10; tapas con la foto centrada (arreglo para Safari: posición absoluta con `--borde`); Alwyn Court con la foto entera de tapa (recortada arriba); símbolos nuevos o rehechos: M+ (2020s Mundo), Templo, Hotel, Brutalismo (La Pyramide) y Moderno tardío (Auditorio de Tenerife); borrados todos los datos de ejemplo (obras, visitas, lista y perfiles; el cartel EJEMPLO queda en el código). Con eso no quedan obras argentinas: el inicio dice "1 país" y Listas está vacía.

**Próxima sesión:**
1. Más símbolos de programas, solo de los que tienen carpeta en `referencias/simbolos/`: deportes, fábrica, hospital, estudios:académico, mercado:shopping, infraestructura, político:parliaments, residencial. Todavía no hay obras con esos programas.
2. Congreso de Brasil (1960s Mundo): rehacer con `referencias/simbolos/brasilia/`.
3. Instagram y dominio (ver Pendientes).
4. Probar con el mouse el hover amarillo de "Registrar visita" (claro y oscuro).
5. Más adelante: G0 y G5 (Inglaterra), G1 (torre de ventilación de Liverpool), G3 (Catedral de Manchester) y las casas de Buenos Aires (G19–G30).

**24 de octubre de 2026, tarde.** Subido en `fe3703b` (`v37`). **Sin subir (`v38`):** 7 obras nuevas de Nueva York (Trinity Church, St. Nicholas, Oculus, Vessel, Alwyn Court, The El Dorado, Ford Foundation) y 2 de Atlanta (Peachtree Summit, 30 Allen Plaza), con sus fotos en `www/img/obras/`; estilos nuevos en `perfiles.json` (Posmodernismo, Neofuturismo bajo Arquitectura contemporánea para Oculus y Vessel, Moderno tardío bajo Moderno); campo optativo `decada` para obras sin años (en `datos.js`, `filas.js`, `vistas/obra.js` y README). El usuario aprobó los resúmenes de Nueva York.

**Atlanta, datos a completar:** Peachtree Summit va sin estilo ni materiales (Wikipedia no los da; a la vista, hormigón y vidrio con escaleras afuera). 30 Allen Plaza: arquitecto MSTSD, 14 pisos, posmoderno, granito y vidrio salen solo de Emporis (cerrado); sin año (comunicado de Southern Company: ocupado en abril de 2006); el usuario eligió dejarlo con `"decada": 2000`. El link de skydb "Southern Company Building" es otro edificio (270 Peachtree, 1961).

**24/10, noche (`v40`, sin subir; el + de los botones rojos y el VISITA de la barra también se ponen amarillos):** Tribeca Synagogue cargada (William N. Breger, terminada en 1967, según Wikipedia y tribecacitizen; hormigón nervurado según thisispaper; "Moderno tardío" lo elegí yo, Wikipedia dice solo "Modernist"; programa nuevo "Sinagoga"). Fotos enderezadas y sin metadatos con un script Swift de ImageIO (`CGImageSourceCreateThumbnailAtIndex` con `WithTransform`). Botones rojos (`boton-primario`): al pasar el mouse, texto en `#f3c96e`, el amarillo de "jagten" en la franja.

Después: The Peregrine (303 East 49th Street; John Klausz, Architects Design Group, 1983; 24 pisos, dato del usuario y CityRealty; Brutalismo según SkyDB): una sola obra con fotos de sus dos torres (5399–5410). Estilo nuevo "Brutalismo" (padre Moderno); la Tribeca Synagogue pasa a Brutalismo (pedido del usuario: brutalista a la vista). Programa "Templo" para iglesias y sinagogas; lista de programas en el README. Descripciones nuevas para todas las obras reales y para los estilos en uso (datos de Wikipedia en inglés, CityRealty y SkyDB). Los arquitectos siguen sin descripción (el usuario dijo que por ahora no).

**Próxima sesión:**
1. Símbolos de programas: el usuario dejó referencias en `referencias/simbolos/` (religioso, deportes, hotel, fabrica, hospital, estudios:academico, mercado:shopping, infraestructura, politico:parliaments, residencial). Gasta bastante: de a pocos. También falta el símbolo propio de Brutalismo (hoy hereda el de Moderno).
2. Congreso de Brasil (década de 1960, Mundo): rehacer el símbolo con las fotos de `referencias/simbolos/brasilia/` (el usuario lo dejó para después).
3. Símbolo de los 2020: el usuario recuerda un edificio "garden algo"; en Mundo es el M+ y en Argentina no hay. No aparece "garden" en el repo ni en las sesiones anteriores.
4. Probar con el mouse el hover amarillo de "Registrar visita" (claro y oscuro).
3. Commit y push cuando lo pida; el usuario aprobó todo lo cargado (El Dorado queda 1929–1931, confirmado por el usuario).
4. Más adelante: G0 y G5 (Inglaterra), G1 (torre de ventilación de Liverpool, confirmada), G3 (Catedral de Manchester, confirmada) y las casas de Buenos Aires (G19–G30, sin nombre: son casas de barrio).

**Fotos sueltas en `~/medianeras-originales/`:** unas 210, sin ubicación en los metadatos. Los grupos G0–G30 salen de ordenarlas por hora (cortes de 25 min). Los scripts para agruparlas y enderezarlas (Swift con ImageIO, aplica la rotación del iPhone) estaban en el scratchpad de la sesión y no quedaron guardados: se rehacen en minutos. Descartadas: G2, G4 y G15 (no son obras), y 6629, 6661 y 6662 (puente y castillo Belvedere del Central Park).

**24 de octubre de 2026.** Todo subido (`v37`): pie de borde a borde, hover ámbar, tapas con marco invertido al pasar el mouse y "todas las obras" más alto con los símbolos de las obras. La cabecera y el pie quedan en la A (vidrio oscuro): al usuario le gustó cómo quedó.

**Próxima sesión:**
1. Probar en el iPhone la barra de arriba con el color de la franja.
2. Mail del proyecto y edificios nuevos (ver la lista de abajo).
3. Para decidir: si "todas las obras" también va de borde a borde en pantallas anchas (hoy queda en 1400 px) y cuántos íconos mostrar cuando haya muchas obras.

**23 de octubre de 2026, cierre.** La app se llama **jagten**, con logo de lanzas (L2) e íconos nuevos: publicado en `e578ac6`. **Sin subir todavía** (service worker en `v33`): Pompidou rehecho; "todas las obras" en minúsculas espaciadas y amarillo, con los datos a la derecha; separadores de lanzas amarillas salpicadas (S1); títulos de sector con tres líneas que bajan en 45° (L2 dada vuelta) y VER MÁS centrado con ellas; botones de sugerir (ocultos hasta tener el mail) y bloque Contacto con Instagram @jagten.arq. El dominio sigue siendo `arqivo.com.ar`; `jagten.com.ar` sin registrar.

**Próxima sesión:**
1. Preguntar si se sube lo que está listo (commit y push).
2. Cargar el Gmail del proyecto en `CONTACTO.mail` (`www/js/contacto.js`) y revisar los botones de sugerir.
3. Edificios nuevos: el usuario cargó muchas fotos. Primero listar qué se reconoce en cada una y que confirme; ir de a tandas (unas 5 obras) por el consumo. No inventar datos.

**23 de octubre de 2026.** La app se llama **Sanskule** (en minúsculas en la marca: "sanskule"), publicado en `5f563ea`. Service worker en `v22`. El dominio sigue siendo `arqivo.com.ar`. Logo nuevo en marcha: finalistas H4 y 1b·2 (ver Pendientes).

**22 de octubre de 2026.** Segunda ronda del nombre: el usuario armó su lista definitiva de palabras (ver Pendientes). Sin cambios en la app.

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
- **Logo (23/10).** L2 "lanzas": las luces encendidas de la mitad de arriba del símbolo del Seagram (década de 1950, Mundo), cada tramo hecho lanza mínima (asta fina y punta de hoja), en ámbar `--logo-luz` sobre vidrio oscuro `--logo-torre`, grilla de 48 × 48. Como Letterboxd, el logo no tiene que hablar de lo que se mira. Los íconos PNG se sacaron con Chrome headless desde `www/iconos/icono.svg`; el maskable va con las lanzas al 78 %. Antes fue la 5b·2 "Calm" (campo rojo y ventanita); sus colores `--logo-*` quedan porque los usan la franja roja y las páginas de prueba.
- **Cabecera y pie (23/10, noche).** Franja de color `--franja` (hoy el vidrio oscuro del logo) arriba y en el pie del inicio, las dos con el tema oscuro adentro (`data-tema`). La barra de estado del iPhone toma `--franja`. El pie, como el de Letterboxd: secciones, redes (solo Instagram con link; TikTok, YouTube y X tenues y sin link; mail cuando haya) y la línea de derechos. Reemplaza al bloque Contacto.
- **Pantalla de carga.** Skyline de Buenos Aires «El siglo» (S3): un edificio por década de la colección Argentina sobre una línea de suelo; cada uno se construye desde abajo, línea por línea. La primera vez que se entra a la app se muestra completa (espera a que termine el skyline; se recuerda con la preferencia `carga-vista`); las siguientes se va apenas cargan los datos. El SVG está inline en `www/index.html` (se regenera con `herramientas/prueba/exportar-skyline.html`). Las versiones de la Price Tower quedaron en `herramientas/prueba/`.
- **Sistema gráfico: flechas** (en `flecha()` de `www/js/ui.js`, para reusar):
  - **F2, escalonada:** rayas apiladas de distinto largo que forman la punta. Va en VER MÁS, la lista de Explorar, Todas las obras y el visor de fotos (dada vuelta para "anterior").
  - **F1, paralela:** tres líneas paralelas; las de afuera doblan y se juntan en la punta. Va en "Cómo llegar".
- **Cabecera y detalles.**
  - Todo en una fila: logo (42 px) y nombre a la izquierda; búsqueda S1 (tres filetes, el del medio rojo en foco) y el botón de tema a la derecha. En el celular la búsqueda está plegada en la lupa.
  - "Todas las obras" es la T2: franja de borde a borde en el ámbar de las lanzas (`--logo-luz`) entre filetes dobles, con el título grande y el resumen a su derecha.
  - Separadores entre bloques (`separador()` en `grafica.js`): lanzas como las del logo, en `--logo-luz`, salpicadas en tres filas, todas a la derecha, cortas y largas según la semilla. Se dibujan al ancho real con un ResizeObserver.
  - Encabezados de fila (`lineaFila()`): tres líneas grises paralelas que bajan en 45° desde arriba, a la derecha del título, y siguen derechas hasta antes de VER MÁS. Reemplazan el filete de 1 px.
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

- **Instagram (@jagten.arq), para después:** planear contenido para subir. Idea del usuario: tener los íconos (símbolos) descargables para subir algunos; hace falta una forma de exportarlos como imagen (PNG cuadrado, claro y oscuro), por ejemplo desde la página de prueba con Chrome headless.
- **Comprar el dominio, para después:** `jagten.com.ar` (libre al 23/10). Ver la mudanza desde `arqivo.com.ar` y exportar visitas antes.
- **Mail del proyecto:** el usuario crea un Gmail; cargarlo en `CONTACTO.mail` de `www/js/contacto.js`. Con `jagten.com.ar`, pasar a `hola@jagten.com.ar` con reenvío gratis (registros MX en la zona de DonWeb, sin tocar nameservers). Más adelante, WhatsApp en el contacto (avisar: deja el número a la vista; mejor uno aparte o Business).
- **Nombre: jagten (23/10, tarde).** Reemplaza a sanskule en todo lo visible. Recordar: *Jagten* es también la película de Vinterberg (2012). Falta registrar `jagten.com.ar` (libre al 23/10) y decidir la mudanza de dominio (ver más abajo lo de exportar visitas antes).
- **Nombre de la app (historial).** "Medianeras" se descartó para el dominio (`medianeras.com.ar` está ocupado) y se compró `arqivo.com.ar`. La app sigue diciendo "Medianeras" hasta decidir. Gustos del usuario que salieron: nombres que hablan de cómo se mira y no de lo que se mira (como Letterboxd), lugares de paso de mediados de siglo (La Guardia, Pan Am), palabras cortas y duras, cosas que suenan a movimiento o antología (Chicago School, números de año) y una melancolía rioplatense (Cortázar, Sur). Propuestas con `.com.ar` libre al 20/10 según whois de NIC: Contrafrente (recomendada), Celosía (segunda), Pared ciega, Planta libre, Escuela del Sur, Usonia, Ochava 96. Ocupados: ochava, medianera, cota, cotacero, cenital, corte, bau, terrazo, vidriera, pulmon. El usuario vuelve con sus elegidas; el próximo paso es mostrarlas en la página de prueba con el logo y las tipografías, en claro y oscuro. No comprar otro dominio antes.
  - **Segunda ronda (22/10).** Nuevos gustos: la época 1900–1960 (Wright, Usonia, googie, mid-century) y cómo suenan el danés, el sueco, el alemán y el holandés, con clase, ni rudo ni infantil (nada tipo "blu" o "kona"). Primero Argentina, después el mundo. No tiene que ser literal. Va en minúsculas, todas las letras parejas, como hoy "medianeras". Su favorita es **jagten** ("la caza" en danés; juega con caza/casa y con buscar en la arquitectura).
  - **Lista definitiva del usuario para buscar la palabra final:** jagten, blik, oteo, lichtval, rear, oak, auster, school, ventum, seeland, wehrmut, neu/neue, brakhage, est, sans, trim, hollow, guard, forum, departures, haze, parsec, strobo, obermann, altc, prins, -der (como final), wilc, orourke, fuses, prekop, park, av, continuum, elementals, showrooms, usonia. Algunas las eligió solo por cómo suenan o se ven.
  - **Notas que se le dieron (de memoria, falta verificar):**
    - *blik*: "mirada" y "chapa" en danés y holandés.
    - *oteo*: mirar desde lo alto para descubrir a lo lejos (RAE).
    - *rear*: *Rear Window*, Hitchcock, 1954.
    - *oak*: Oak Park, la casa y estudio de Wright.
    - *auster*: el viento sur en latín.
    - *ventum*: de *ventus* viene "ventana".
    - *wehrmut*: con "r" evoca la Wehrmacht; *Wehmut* es melancolía y *Wermut*, vermut.
    - *seeland*: la isla de Copenhague.
    - *brakhage*: *Metaphors on Vision*.
    - *lichtval*: cómo entra la luz.
  - **Recomendación de Claude:** jagten, blik, oteo y rear (mirar y buscar).
  - **Recorte (22/10):** jagten, oak, auster, neu/neue, brakhage, sans, parsec, strobo, orourke, fuses, prekop, park, continuum, usonia (segundo recorte; las guardadas del mezclador quedan en el navegador). Para combinarlas está el mezclador: http://127.0.0.1:8001/nombres.html (con `herramientas/prueba/servir.sh`).
  - **Finalistas (23/10):** sanskole / sanskule (invento del usuario: "sans skule", percepción de un ceño, sin escuela), jagten, auster, brakhage, parsec, orourke, prekop, continuum. Se ven juntas en `herramientas/prueba/finalistas.html`.
    - **Verificado (Wiktionary):** *sans* es "sentido" en danés y noruego y "sin" en francés; *skole* es "escuela" en danés y noruego; *skule* es "fruncir el ceño, mirar con enojo" en danés y noruego, y "escuela" solo en nynorsk. *Jagten* es "la caza" y también el título de la película de Vinterberg (2012), que trata de una falsa acusación de abuso infantil.
    - **`.com.ar` (whois NIC, 23/10):** libres sanskole, sanskule, sansskule, jagten, brakhage, parsec, orourke, prekop. Ocupados: auster y continuum.
    - **Lecturas del usuario:** el ceño es la cara que uno pone al mirar un edificio en detalle; "sin escuela" es también no atarse a una sola escuela o estilo.
    - **Recomendación final de Claude: sanskule.** Con esas lecturas tiene las tres capas (sentido/sin, ceño, escuela), y en inglés "skule" se lee como "school".
    - Recomendación anterior: sanskole. Es un invento propio, tiene tres lecturas y el dominio está libre. Brakhage, O'Rourke y Prekop son apellidos de personas reales (Stan Brakhage, Jim O'Rourke, Sam Prekop: de memoria).
  - **Elegida (23/10): sanskule.** Cambiado en lo visible (cabecera, título, pantalla de carga, manifiesto, aviso de versión, exportación, créditos de ejemplo). Los nombres internos de almacenamiento (`medianeras` en IndexedDB, prefijo `medianeras-` en preferencias, cachés del service worker) quedan igual a propósito: cambiarlos borra las visitas y preferencias del teléfono.
  - **Dominio:** `arqivo.com.ar` vence el 19/10/2027. Si se pasa a `sanskule.com.ar`, el teléfono lo toma como otro sitio: las visitas guardadas ahí no se mudan solas (no hay importar), así que antes hay que exportarlas y pasarlas a `diario.json`. Lo de devolver `arqivo` hay que consultarlo con DonWeb. Después, verificar los significados con fuentes, ver si el `.com.ar` está libre (whois de NIC) y mostrar las finalistas en la página de prueba con el logo, en claro y oscuro.
- **Logo (resuelto el 23/10: L2 de lanzas para jagten).** Historial de las rondas para sanskule: el actual habla de medianeras. Primera ronda en `herramientas/prueba/logos.html`: 1a–1c (mirada entrecerrada como ventana corrida), 2a–2b (el ceño; 2b con techo mariposa) y, aparte, P1–P2 (idea del usuario: ojos entrecerrados mirando para arriba con arquitectura encima, en estilo de recorte de papel tipo Saul Bass, inspirado en Prismo de *Hora de aventura*; dibujo propio, no copia). Falta que elija; después se rehacen `logo()` en `grafica.js` y los íconos. Segunda ronda (23/10): descartadas 1a, 1c, 2a y 2b; le gustó 1b (variantes 1b·2 con pupila redonda y 1b·3 en paleta oscura). Su idea, con ciudad más lejana y paleta oscura de amarillos, rojos y negros: P3, P4 y P5, con ojos de lente según sus referencias (`~/medianeras-originales/referencias/estetica/nuevo logo - ojos/`). La paleta Jesus Lizard de la primera ronda no quedó guardada: se usó el amarillo "sol", el rojo del logo, ocre, granate y negro noche. Tercera ronda (23/10): quedan 1b·2 (su favorita de las suyas), P3 y P4 con ojos naranjas más entrecerrados mirando para arriba, sin amarillo; en P3 el cielo pasó a rojo y granate. Descartadas P1 y P5. En P3 decide después si deja la franja de cielo. Después P3/P4 pasaron a solo pupilas naranjas, sin ojo; no lo convencieron. Cuarta ronda (23/10): volver a la idea de la tapa de Calm (campo de color, ventana de marco negro, firma abajo; referencia en `referencias/estetica/`), sin rojo obligatorio, mezclada con op art (Stereolab *Dots and Loops*, *Figure 8*) y edificios: O1 (bóveda de arcos concéntricos), O2 (edificios por desfase de rayas), O3 y O4 (rayas verticales en los edificios). La tapa de Jesus Lizard de las referencias es turquesa, cielo y mar, no amarillo. De la cuarta, le gustó algo la O2. Quinta ronda (23/10), con dos referencias nuevas en `referencias/estetica/` (folleto *Dänemark* con ciudad lejana, y tapa de XSVE *Elevated Minimalism*): H1–H4 (horizonte lejano) y K1–K3 (monograma sk de bloques; K2 con rayas como la O2).
  - **Cierre del 23/10, favoritas del usuario:** **1b·2** (la ventana-ojo), **H4** (cielo y ciudad lejana de Dänemark dentro de la franja, sobre el papel gris de XSVE), y bastante **H1** y **H3**.
    - **H1, a corregir (palabras del usuario):** "la ciudad que no ocupe todo el ancho, sino más lejos y más ancha pero achicala y que llegue hasta la mitad de la pantalla". Interpretación a confirmar: la ciudad más chica y lejana, sin tocar los bordes, y el horizonte subido hasta la mitad del ícono (más campo, menos cielo).
    - **H3, a corregir:** las siluetas dentro de la franja coral no le cierran; probar otras formas.
    - **Sexta ronda (23/10, arriba de todo en `logos.html`, sección "Favoritas"):** 1b·2 y H4 sin cambios; H1·2 (horizonte a la mitad, ciudad más chica y lejos); H3·2 (edificios recortados algo torcidos) y H3·3 (la ciudad de Dänemark en gris sobre el coral).
    - **Finalistas (23/10): H4 y 1b·2.** Próximo paso (24/10): decidir entre las dos (o afinarlas) y después rehacer `logo()` en `grafica.js` y los íconos. Después, rehacer `logo()` en `grafica.js` y los íconos (`www/iconos/`), y revisar cómo se ve el ícono en la cabecera en modo oscuro.
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

### 22 de octubre de 2026

- **Nombre, segunda ronda:**
  - catálogo de palabras de idiomas nórdicos, alemán, holandés, polaco y finés, ordenado por idea (buscar, mirar, luz, amplitud, de paso, piezas de arquitectura, época);
  - análisis de la lista propia del usuario, buscando qué conexión tiene cada palabra con la página;
  - el usuario armó su lista definitiva (ver Pendientes);
  - recortó a 21 palabras y se armó el **mezclador de nombres** en la página de prueba (`herramientas/prueba/nombres.html`): sumar y recortar palabras, mezclas al azar, vista con el logo en claro y oscuro, y guardadas (quedan en el navegador de la compu).
- **23/10:** finalistas, significados verificados, whois y página `finalistas.html`. Elegido **sanskule** y cambiado en la app; commit y push `5f563ea`. Logo nuevo: cinco rondas en `herramientas/prueba/logos.html` (ventana-ojo, ojos y ciudad, Calm + op art, horizonte lejano, letras sk). El usuario creó la cuenta @_sanskule y registra `sanskule.com.ar` el 24/10.
- Sin cambios en la app.
- **23/10, tarde:** logos para jagten: Savoye con lanzas (J1–J8, queda J4 en la página de prueba), y luego las luces del Seagram hechas lanzas (L1–L3). Elegida **L2**. Nombre cambiado a jagten en la app, logo L2 en `grafica.js` e íconos rehechos; `sw.js` en `v23`. Commit y push `e578ac6`. Después, "Todas las obras" en ámbar y separadores de lanzas (`v24`). Pompidou (década de 1970, Mundo) rehecho con las fotos nuevas: de frente, 58 líneas, escalera mecánica en zigzag con panza roja; colores nuevos `pompidou-interior`, `pompidou-tubo`, `pompidou-pasarela`; sumado a `comparar.js`. Opciones de texto en `todas.html` (`v25`).
- **23/10, cierre:** separadores en varias rondas (sándwich de lanzas, con y sin loma, más gruesas) hasta elegir en `herramientas/prueba/separadores.html` la S1 (lanzas amarillas salpicadas) para separar bloques y la L2 dada vuelta para los títulos de sector (`lineaFila()` en `grafica.js`, reemplaza el filete). Los separadores se dibujan en píxeles al ancho real con un ResizeObserver: antes se estiraban y se cortaban en pantallas anchas. "todas las obras" en la opción E, con 10 px más de aire a la izquierda y los datos uno por renglón en el celular. VER MÁS centrado con las líneas. Sugerencias por mail y Contacto (`www/js/contacto.js`, sumado a `APP` en `sw.js`). Se le explicó que el dominio no trae mail: para `@jagten.com.ar` hace falta reenvío (gratis) o casilla (paga). Todo verificado con capturas en claro y oscuro; sin commit (`v33`).
- **23/10, noche:** commit y push `bc6a86a`. Arreglado el "null" que aparecía debajo de "todas las obras" (el botón de sugerir oculto se escribía como texto; el inicio ahora usa `agregar()`), `v34`. Pie de página nuevo (`pieDePagina()` en `contacto.js`, íconos de redes en `ui.js`) y cabecera del mismo color; opciones de color en `herramientas/prueba/franjas.html`. Verificado con capturas en claro y oscuro; sin probar en el iPhone. La captura de Letterboxd no estaba en `referencias/estetica/`: se hizo de memoria. Sin commit (`v35`).

### 24 de octubre de 2026

- Pie de página de borde a borde y hasta abajo de todo (con `border-image`, sin correr la página): en pantallas anchas quedaba como una isla.
- Al pasar el mouse, todo lo que se toca se pone ámbar (`--realce`, más oscuro en claro), como el celeste de Letterboxd. Las tapas suman un marco por dentro del color invertido al de su marco (`rgb(from …)`). Solo con mouse (`hover: hover`).
- "todas las obras": sin las lanzas de arriba, más alto (132 px) y con los símbolos de las obras en chiquito (debajo del título en el celular, al costado desde 900 px). Si varias obras comparten dibujo, va una sola vez. El símbolo neutro casi no se ve, pero el usuario prefirió dejarlo.
- Verificado con capturas en claro, oscuro y a 1600 px; el hover no se puede capturar, lo probó el usuario. Commit y push (`v37`).
- **Edificios nuevos, primera tanda:** fotos agrupadas por fecha y hora, reconocidas en hojas de miniaturas y confirmadas por el usuario. Cargadas 6 obras de Nueva York con datos verificados en Wikipedia (materiales de Trinity y del Oculus en HDC y Architectural Record); estilos nuevos: Historicismo (Neogótico, Neorrenacimiento francés), Art déco y Arquitectura contemporánea. Fotos a 1600 px, derechas y sin metadatos. Verificado con capturas (inicio, obras, ficha en oscuro). Sin commit.
- **Atlanta (G7):** con una captura de Street View del usuario se identificaron Peachtree Summit (Toombs, Amisano and Wells, 1974–1975, datos de Wikipedia) y 30 Allen Plaza, sede de Southern Company (datos de Emporis). Coordenadas de OpenStreetMap. Fotos: 6 y 2, preparadas con `preparar.swift` (ImageIO: endereza, 1600 px, sin metadatos; quedó en el scratchpad). Verificado con capturas de las dos fichas. Sin commit.
- **Tarde:** 30 Allen Plaza con década 2000 (campo `decada` nuevo), Oculus y Vessel pasan a Neofuturismo, y Ford Foundation cargada (Wikipedia: Roche y Dinkeloo, 1964–1967, moderno tardío; 7 fotos). Verificado con capturas (ficha de Ford y de Allen Plaza, `#/decada/2000`, `#/estilo/neofuturismo`). `sw.js` en `v38`. Sin commit.

### 25 de octubre de 2026

- Commit y push de lo pendiente (obras de Nueva York y Atlanta, estilos, descripciones, hover amarillo). Se había colado `www/js/.DS_Store`: sacado del repo y `.DS_Store` sumado a `.gitignore`.
- **Tapas:** en el iPhone las fotos verticales quedaban sin borde abajo (Safari no resuelve el 100 % de alto dentro de un `aspect-ratio`). Ahora la imagen va en posición absoluta con `inset: var(--borde)`; las variantes cambian `--borde` en vez de `padding`. Verificado en Chrome con una página temporal; el usuario lo vio bien en el iPhone.
- **Alwyn Court:** primera foto la del edificio entero, recortada un 13 % arriba (PIL; `sips -c` con `--cropOffset` no recorta bien).
- **Color de los marcos:** el usuario preguntó el criterio (sale del estilo, 4 colores para 6 familias). Se le propuso por época; prefirió dejarlo como está y balancear con más estilos.
- **Símbolos** (todos comparados con su foto en `herramientas/prueba/`, claro y oscuro; `comparar.js` ahora muestra también programas):
  - M+ (2020s Mundo): torre gris azulada con toques de terracota, casi del ancho del basamento, 15 franjas; basamento negro de 4 líneas. El "garden algo" del usuario era probablemente el jardín de la terraza del M+.
  - Templo: gopuram del Meenakshi de Madurai (nueve pisos de figuras de colores, bóveda y remates).
  - Hotel: Hôtel de l'Indépendance de Dakar (celdas en punta, franja de ladrillo, cornisa almenada).
  - Brutalismo: primero se hizo con fotos de la Tribeca Synagogue sin carpeta (el usuario lo corrigió: solo símbolos con carpeta de referencias); rehecho con La Pyramide de Abiyán.
  - Moderno tardío: Auditorio de Tenerife (Calatrava), rebanadas horizontales calculadas con curvas sobre la foto desde el mar, con placa de cielo (de noche en oscuro). Corrección del usuario: el medio son dos velas que suben hacia la derecha, no una cúpula. Aviso dado: suele clasificarse cerca del neofuturismo.
- Racionalismo, cuando haya obras, va bajo Moderno y hereda la Villa Savoye.
- **Ejemplos borrados:** 3 obras, 3 visitas, la lista, "Racionalismo (ejemplo)", "Brutalismo (ejemplo)", "Art déco (ejemplo)" y sus imágenes; README actualizado. Verificado con capturas del inicio y de Listas. `sw.js` en `v43`.

### 26 de octubre de 2026

- **Congreso de Brasil (1960s Mundo)** rehecho sobre la foto frontal de `brasilia/`: torres altas con el puente vidriado, cúpula y cuenco redondeados (44 líneas de torre, grosor 0.8), edificio bajo vidriado con columnas, rampa, espejo de agua y pasto. Colores `br-*`.
- **Salud** (carpeta `hospital/`): Royal Infirmary de Glasgow. La primera versión parecía oriental (cúpulas escalonadas y pabellón bajo); rehecha con torres redondas desde el piso, tambor con aberturas, cúpula de media naranja con punta, frente largo con cornisa oscura. Colores `gl-*`.
- **Vivienda unifamiliar** (carpeta `residencial/`): pasó por tres versiones. La del reel era del hotel Coconut Lagoon (Kumarakom, Kerala), sin foto entera; después una casa de barrio del usuario (fotos HEIC, Chrome no las muestra: abrir la prueba en Safari); quedó una victoriana azul de San Francisco (`images.jpeg`): techo de atrás claro, triángulo intermedio que llega a los costados, torre cónica oscura; frisos rojos y blancos, saliente simétrica de tres ventanas, puerta de dos hojas. Colores `vi-*`. En la carpeta siguen también las fotos de antes.
- Generadores de las partituras: scripts de Python en el scratchpad (miden sobre la foto y escriben las líneas); no se guardaron, se rehacen rápido.
- `comparar.js` suma Brasilia, Salud y Vivienda unifamiliar. `sw.js` en `v44`.

### 26 de octubre de 2026 (segunda sesión)

- **Infraestructura** (carpeta `infraestructura/`): puente japonés de Hoi An, de frente, medido sobre la foto cuadrada (`images (15).jpeg`). Techo de tejas con canales, friso rojo y blanco y guarda de puntos azules en el alero, dragones, galería con postes, faroles y baranda, tablero arqueado, arcos y agua con el reflejo de las pilas. Correcciones del usuario: agua abajo y más detalle en el techo; en claro los grises mareaban (se resolvió con placa de cielo `hoi-cielo`, noche azul en oscuro); los huecos entre pilas van sin pintar, para que se vea el fondo. Colores `hoi-*`.
- **Deportivo** (carpeta `deportes/`): Monumental de River **visto desde arriba** (se avisó que se sale de la regla de vista frontal: de frente un estadio no se reconoce). Óvalo, banda roja, anillo oscuro, pista y cancha. Correcciones: más grada en proporción a la cancha y la pista; la banda roja se lee de la foto cenital (convertida con `sips` a jpg, en el scratchpad) y, como solo el cuarto de arriba a la derecha salía completo, se usa en espejo para los cuatro. Fondo verde de barrio (`riv-suelo`). Colores `riv-*`. La foto cenital está en `comparar.js`.
- **Misma superficie:** `simbolo()` en `grafica.js` acepta `superficie` (0 a 1): el dibujo ocupa esa parte del área útil, sin pasarse del borde, y reemplaza a `escala`. Se usa con 0.42 en las tapas (`ui.js`), en la tira de "todas las obras" y en "Por década" (`vistas/inicio.js`). Motivo: el Templo se veía chico al lado de La Pyramide, y CCTV mucho más grande que M+. Verificado con captura del inicio en claro; falta mirarlo en oscuro y en el iPhone.
- **`herramientas/prueba/equilibrio.html`:** todos los íconos de obras en cuadrados, en claro y oscuro, con tres tamaños (como hoy, misma superficie, mismo alto) y tres fondos (como hoy, cielo, placa neutra). El usuario eligió misma superficie y descartó el cielo para todos.
- Generadores: `armar.py` en el scratchpad (no se guardó, como en la sesión anterior).
