# Medianeras: estado y bitácora

## Qué es

Medianeras es un catálogo personal de obras de arquitectura con un diario de visitas. Es una PWA hecha con HTML, CSS y JavaScript sin frameworks ni compilación, pensada primero para el iPhone, que funciona sin conexión. Se publica en GitHub Pages desde `www/` en cada push a `main` (repo `tewjacobs/medianeras`), con el dominio propio **https://arqivo.com.ar**. Más adelante puede pasar a app nativa con Capacitor.

Se usa como Letterboxd o RYM: un inicio con filas temáticas y una página por arquitecto, estilo, material, programa, lugar, década y año. La estética es de impreso de los 60/70: tapas cuadradas con marco de color y símbolos de líneas paralelas.

## Estado

**14 de noviembre de 2026, mediodía.** Subido (`v75`).

**Próxima sesión:**
1. **Fondos de Tudor y Barroco eduardiano** (dibujos aprobados: "perfecto"): opciones en `fondos.html`. Hoy provisorios `tudor-fondo` (crema) y `eduardiano-fondo` (gris verdoso).
2. Seguir puliendo las bases de arqivo (plan del 14/11): ~~1. fuentes~~, ~~2. textos revisados~~, **3. huecos visibles** (símbolos que faltan con carpeta: posmodernismo, neofuturismo, contemporáneo, gótico perpendicular; revisión en el iPhone), 4. carpeta de presentación al final. Cargar obras sin tocar código: solo cuando aparezca alguien concreto.
3. Después **sanskule**; **jagten** (Instagram primero, página quizás después) es la última prioridad.

**14 de noviembre de 2026, madrugada (cierre).** Subido (`v74`, commit 3db962f, publicado en arqivo.com.ar).

**Próxima sesión (14/11, ~10 h): pausa de símbolos; volver a los proyectos futuros, jagten y sanskule.** Idea nueva del usuario sobre arqivo: es muy amplio y lo está armando mucho a su gusto, cuando debería ser "algo de todo para todos". Plan que propone: **seguir puliendo las bases** de lo que ya hay y después **dárselo, vendérselo o colaborar** con alguien que tenga mucho más material y prensa. Conversarlo con él: qué significa "bases pulidas" (lista concreta), qué haría falta para presentarlo (como lo pensado para jagten: idea al 100 %, derechos de fotos, datos verificados) y cómo encaja con jagten y sanskule como proyectos propios.

**Cuando se retomen los símbolos:**
1. (hecho: subido)
2. **Tanda siguiente (de a dos)** con las carpetas que ya están: tudor, barroco eduardiano, posmodernismo (¿el Big Duck suelto en la raíz?), neofuturismo, contemporaneo, gotico perpendicular (`colonial` vacía). **Detalle alto desde la primera versión** (regla nueva en `CLAUDE.md` y memoria): recortar cada zona de la foto, simetría exacta, franjas por tramo.
3. Después: Academicismo e Historicismo; estilos de Buenos Aires que falten; pieles. **En suspenso:** Pintoresquismo, Instagram, logo, iPhone (al final), proyecto sanskule (no arrancar sin pedido).

- **Fondos elegidos:** Art déco **ciruela** (`deco-ciruela`), Italianizante **piedra de lago** (`italia-lago`), Renacimiento francés **lavanda gris** (`renac-lavanda`, el provisorio quedó), Gótico **cielo de Colonia** (`gotico-cielo`; en oscuro el marco y el texto del encabezado van en crema `#f3ead9`, porque el inverso del celeste medio no se leía).
- Ojo con fondos de tono medio en oscuro: el texto del encabezado del perfil usa el color del marco (inverso del fondo); si el fondo es medio, el inverso también y no se lee. Revisar el perfil en la app.

**13 de noviembre de 2026, noche (cierre).** Subido (`v73`, commit c9b180b).

**Próxima sesión, en este orden:**
1. **Art déco e Italianizante aprobados** (13/11 a la noche; la Erba con cornisas, pasamanos y zócalos de las balaustradas en crema bien gris `er-cornisa-g`, también arriba de la torre). Siguen los fondos de los dos (punto 3).
2. **Tanda nueva (de a dos): Renacimiento francés = Alwyn Court** (carpeta `neorenacimiernto frances/`, 4 fotos; es obra del catálogo) **y Gótico = catedral de Colonia** (carpeta `gotico/`: fachada oeste de frente en `Kölner_Dom_-_Westfassade…jpg`). Carpetas nuevas del 13/11 también: tudor, barroco eduardiano, posmodernismo, neofuturismo, contemporaneo, gotico perpendicular (`colonial` vacía; `Big_Duck_2018_01.jpg` suelto en la raíz, ¿Posmodernismo?). Copiar detalles **tal cual**: recortar y ampliar cada zona de la foto antes de dibujar.
3. **Los fondos de los dos son provisorios** (terracota y verde oliva): cuando apruebe los dibujos, proponer opciones en `fondos.html` (ver memoria "fondos después del dibujo").
4. Después: Renacimiento francés (tiene carpeta); el resto espera las fotos que busca el usuario (Gótico, Gótico perpendicular, Colonial, Tudor, Bungalow, Contemporánea, Neofuturismo, Posmodernismo, Barroco eduardiano). Al terminar esos 13, Academicismo e Historicismo; luego estilos de Buenos Aires que falten; luego pieles. **En suspenso:** Pintoresquismo, Instagram, logo (habría que hacer algo, sin apuro), iPhone (va al final).
5. **Proyecto aparte "sanskule" / El lote:** carpeta `~/sanskule?/` (con signo de pregunta en el nombre) con `refs/` (89 fotos de sus referencias) y `contexto/` (`gustos.md` y `el-lote.md`, los textos de su otro chat guardados el 13/11). Idea decidida: herramienta 3D con **modo libre** (su idea: elegir variables) y **modo por encargo** (briefs con cliente, código y voz crítica), sol y sombras. Pendiente: mirar las fotos y leer sus gustos; más adelante armarle un `CLAUDE.md`, contexto y principios para abrirlo en su propio Claude Code. No arrancar sin que lo pida.

- **Nombres decididos (13/11):** esta app es **arqivo** (cambiado en cabecera, título, pantalla de carga, nombre bajo el ícono, pie, aviso de versión y exportación; el logo de lanzas queda por ahora). **jagten** queda para el proyecto de placas de arquitectos (Instagram + página que crece con los comentarios: una foto de la placa y otra de la fachada). **sanskule** para la herramienta 3D. Instagram de arqivo: **@_arqivo** (cargado en `contacto.js`).
- **Media estrella:** los promedios se muestran redondeados a medio (★★★★½), en `estrellas()` de `ui.js`.
- **Textos verificados con Wikipedia:** Flatiron (la punta da a la calle 23; penthouse de 1905 para talleres; Macmillan se fue en 2019; conversión anunciada en octubre de 2023) y Guggenheim (causas de la demora; el "monitor" hoy tiene la colección Thannhauser).
- **Página de comparar:** `?solo=` acepta varias claves separadas por comas y las muestra en grande (420 × 400).

**12 de noviembre de 2026, tarde.** **Sin subir (`v69`)**: el usuario no pidió commit.

**Próxima sesión:**
0. **Primero: el proyecto chico (13/11).** El usuario volvió sobre el alcance: la propuesta A+B de "Alcance: núcleo y cinturón" **no le gustó mucho** (casi no la leyó; el planteo con Lakatos lo armó su chat de IPC, no él). Lo que piensa, en sus palabras: le gusta jagten, pero es mucho trabajo para una persona. Quiere **dejarlo ideado y listo al 100 %** para algún día presentárselo a alguien con fotos de adentro, derechos y contenido, que pueda sumarse (hasta con un acuerdo legal). **Aparte**, quiere una página que pueda hacer **solo, al 100 %, más original y centrada en algo**: arquitectura streamline, casas peculiares, placas de arquitectos en las fachadas de Buenos Aires, un juego o una IA de arquitectura… "algo donde puedas crear, ver, poner en práctica, aprender". Pidió: "pensalo; cuando vuelva leés el log y me decís lo que pensás". Ver "Proyecto chico: lo que pensé" más abajo y presentárselo corto, con recomendación.
1. **Estilo de las pintoresquistas que faltan.** Ya cargadas: Casa Tudor de Florida y Casa de la puerta en arco → **Tudor**; Casa de los arcos → **Bungalow** (estilos nuevos en `perfiles.json`, colores provisorios oliva y teja, descripciones de memoria). Siguen en Pintoresquismo: chalet amarillo, techo empinado, blanca de Olivos y María (propuestas abajo). Después: borrar Pintoresquismo y pasar la casona a "Vasco tradicional" (o a donde corresponda: ninguna casa salió vasca). Abierto: Italianizante, Beaux-Arts y Barroco eduardiano (recomendación: dejarlos como estilos propios).
2. **Símbolos** (punto 3 del plan): Art déco, Italianizante, Renacimiento francés (antes Neorrenacimiento francés), con sus carpetas de referencias.
3. Pieles por estilo; revisar en el iPhone la etiqueta (tocar la P/N de una tarjeta, el bloque de la ficha) y las décadas en grilla.

- **Etiqueta de copia en la app** (diseño D): campo `copia` en `obras.json` (`"pintoresquista"` | `"neo"`), textos en `perfiles.json` → `copias` (`plural`, `ayuda` corta, `descripcion` larga). Es un tipo de perfil más (`copia` en `TIPOS_PERFIL`): la lista de todas está en `#/copia/neo` y `#/copia/pintoresquista`. En la tarjeta (`tarjetaObra` en `ui.js`), la letra a la derecha del nombre; con mouse sube la tarjetita negra con la palabra y el «?», y al pasar por el «?» sale la explicación al costado (un solo `.globo` fijo a la ventana, así no lo corta una fila deslizable; a la izquierda si no entra). Al tocar la letra o el «?» se abre una hoja desde abajo con la explicación y "Ver las N …". Sin mouse, la letra lleva el «?» chiquito. En la ficha (`etiquetaCopia` en `obra.js`), el bloque bajo el nombre abre la explicación con el link.
- **Los neo pasaron a etiqueta:** Neogótico → **Gótico** (Trinity Church, St Luke), Neorrenacimiento francés → **Renacimiento francés** (Alwyn Court), Neocolonial → **Colonial** (las 3 casas de Florida y Olivos), todas con `copia: "neo"`. Los estilos nuevos guardan el color del viejo y ya no cuelgan de Historicismo (que queda solo con Italianizante); Gótico perpendicular ahora cuelga de Gótico. Descripciones nuevas escritas de conocimiento general (no de una fuente puntual).
- Capturas con hover y modo iPhone: script con Chrome por protocolo de depuración (sin extensión), saltea la pantalla de carga con la preferencia `medianeras-carga-vista`. Quedó en el scratchpad de la sesión; si hace falta de nuevo, conviene pasarlo a `herramientas/capturas/`.

**12 de noviembre de 2026 (cierre).** Subido (`v68`, commit 3b80ee1), con todo lo del 11/11.

**Próxima sesión** (desde la cuenta personal: `cd ~/medianeras` y `claude-tew`):
1. **Pasar la etiqueta a la app** (diseño D aprobado, "perfect"; prueba en `herramientas/prueba/etiqueta.html` + `etiqueta.js`, con botón "Simular iPhone"). Marco liso, sin dibujos. En la tarjeta de la grilla: la **P** o la **N** en un cuadradito del color del marco con marquito negro, abajo a la derecha, al lado del nombre (letra del título: Archivo 850, 112 %, mayúscula, `text-box: trim-both cap alphabetic`). En la compu, al pasar el mouse por la tapa sube una tarjetita negra con solo la palabra (PINTORESQUISTA / NEO) y un **?**; al pasar por el **?** se abre una tarjeta **afuera de la tapa**, al costado (a la izquierda en la última columna), con la explicación. En el iPhone: la letra lleva un **?** chiquito en la esquina y se toca; la explicación sale como hoja desde abajo. En la ficha: bloque con la palabra (color del marco, marquito negro) abajo del nombre; al tocarlo se abre la explicación y el link a la lista de todas. Textos aprobados en `etiqueta.js` (`ayuda`); "entre los años 20 y 50" sale de la descripción vieja del estilo, sin verificar.
2. **Datos:** **los "neo" también son etiqueta** (decidido por el usuario): Neogótico → Gótico + neo, Neorrenacimiento francés → Renacimiento francés + neo, Neocolonial → Colonial + neo, etc. Pintoresquismo deja de ser estilo: cada casa con su estilo original + pintoresquista. Proponer el campo (ej. `copia: "pintoresquista" | "neo"`), revisar con el usuario las 7 casas pintoresquistas y las neo una por una, y ver qué hacer con Italianizante, Beaux-Arts y Barroco eduardiano (también son vueltas a estilos viejos). La casona (`casona.py`) pasa a ser el símbolo de "Vasco tradicional".
3. Símbolos (Art déco, Italianizante, Neorrenacimiento francés…) y pieles por estilo, como estaba.
4. Revisar en el iPhone las décadas en grilla y lo pendiente de antes.

- **Décadas del inicio en grilla de tres** (`v68`, elegida la A): `decadas()` en `inicio.js` arma `.decadas-grilla` con una tapa por década (símbolo de Mundo), nombre y cantidad; cada una lleva a su perfil. Tres columnas en el teléfono y `auto-fill` de 120 px desde 600 px. Se sacaron los desplegables y la preferencia `decadas-abiertas` (queda guardada en los teléfonos sin uso).
- **Etiqueta:** se probaron y descartaron op art en el marco (mareaba), fajas en diagonal, esquina cortada, lomo vertical como *69 Love Songs* (quedaba descentrado) e isla en la esquina de la foto.
- Ojo con las capturas: Chrome headless no baja de ~500 px de ancho (a 390 sale cortado) y las fotos `lazy` fuera de pantalla no cargan (usar `--virtual-time-budget`).
- **Cuenta personal:** atajo `claude-tew` en `~/.zshrc` (`CLAUDE_CONFIG_DIR=$HOME/.claude-tew claude`), con ok del usuario. Ya inició sesión con su cuenta. Se copió la memoria del proyecto a `~/.claude-tew/projects/-Users-jacobs-medianeras/memory`. `CLAUDE.md` y `LOG.md` están en el repo y se leen solos.

**11 de noviembre de 2026 (cierre).** **Sin subir (`v67`)**: el usuario no pidió commit.

**Próxima sesión:**
1. **Pintoresquista como etiqueta** (plan aprobado): el estilo Pintoresquismo deja de existir; cada casa copia lleva el estilo original (vasco, tudor, normando, chalet marplatense…) y `pintoresquista: true` en `obras.json`. Etiqueta "PINTORESQUISTA" bien notable en la ficha (junto al nombre) y marquita en la tapa; al tocarla, la lista de todas las pintoresquistas **con un texto breve que explique qué es** (copia en la ciudad de un estilo de campo). La descripción también lo dice. Pasos: (a) 2–3 diseños de la etiqueta en `herramientas/prueba/` y esperar que elija; (b) revisar con el usuario las 7 casas de Pintoresquismo una por una y decidir el estilo de cada una; (c) crear solo los estilos necesarios. **La casona** (`casona.py`) pasa a ser el símbolo de **"Vasco tradicional"** (nombre aprobado; el usuario nota que se parece a las casas de Bután, *Driglam Namzha*). **Abierto:** el usuario duda si los "neo" (Neorrenacimiento francés, Neogótico, Neocolonial…) también deberían ser etiqueta sobre el estilo original (le molesta que una casa racionalista de hoy fuera "neorracionalista"). Retomarlo con ejemplos antes de tocar datos.
2. **Décadas del inicio en grilla:** prueba en `herramientas/prueba/decadas.html` (A grilla de tres, B tira deslizable); falta que elija (recomendación: A). Hoy son desplegables (`decadas()` en `inicio.js`) y ocupan mucha altura; las abiertas se recuerdan en la preferencia `decadas-abiertas`.
3. **Símbolos, tanda siguiente:** Art déco, Italianizante y Neorrenacimiento francés (carpetas ya cargadas en `referencias/simbolos/`). Faltan además Academicismo, Historicismo, Neogótico, Contemporánea, Neofuturismo, Posmodernismo, Neocolonial, Gótico perpendicular, Barroco eduardiano; el usuario va buscando fotos. **Banderas** (3 países): rehacerlas con el sistema nuevo.
4. **Pieles por estilo**, a la par de los símbolos (inspiradas en la arquitectura del estilo, no en discos). Las **tarjetas de familia** de estilos (opción B de `herramientas/prueba/listas.html`) quedan guardadas para cuando haya pieles: cada tarjeta llevaría algo de la piel de su familia (5 familias propuestas: Gótico y neogótico, Historicismos, Art déco, Moderno, Contemporáneo).
5. Pendiente opcional: **miniaturas** de las fotos (copia de ~600 px para grillas: se ve suave con poco zoom en la compu y carga más rápido en el iPhone; hoy 73 MB). El usuario lo dejó afuera por ahora.
6. Revisar en el iPhone todo lo de esta sesión y lo pendiente de antes (círculos de zona, El Planeta, colores de marco).

- **Índice de arquitectos en grilla** (`renderIndice` en `perfil.js`): como la grilla del inicio, cada arquitecto con la tapa de su obra más antigua con foto, nombre y cantidad.
- **Panel de los perfiles** (`resumen` en `perfil.js`): una fila de cuentas ("15 arquitectos · 10 estilos…"); al tocar una se abren sus chips, al volver a tocar se cierran (`.resumen-cuenta`, `.resumen-abierto`). Antes eran todos los chips abiertos.
- **Símbolo de Pintoresquismo = casona de montaña** (`herramientas/simbolos/casona.py`, foto `referencias/simbolos/pintoresquismo/images.jpeg`), aprobado: de frente por el hastial y **simétrica**; techo bajo de tejas sobre tabla oscura, hastial y pisos de entramado denso (pies derechos de 1 cada 3, función `pies()` simétrica desde el eje: sin moiré), dos galerías de balaustres, planta baja de piedra en hiladas con esquinas de sillares, puerta en arco de medio punto, ventanitas a los lados, pasto con matas. Fondo verde de monte (`pintoresquismo-monte`). Quitar las filas vacías de arriba: `recortar()`.
- **Símbolo de Racionalismo = Casas Estudio de Diego Rivera y Frida Kahlo** (Juan O'Gorman, San Ángel; `ogorman.py`, medido sobre `referencias/simbolos/racionalismo/images (2).jpeg`): casa blanca de Diego (techo **plano**, tanques rojos con zunchos, caño), cuerpo blanco del medio con dos ventanas corridas, pilotes y puente con baranda roja fina, cubo azul de Frida con ventanales de muchos cuadros y marco rojo, portón de cuatro hojas, cerco de cactus órgano, farola verde, tezontle moteado, cordón amarillo y vereda. Fondo ocre (`racionalismo-ocre`). El usuario sacó los dientes de sierra y la torre roja: **de frente no se ve lo que está atrás**. Años 1929–1931 solo de la leyenda de una ilustración (no verificados, no cargados). La ilustración guardada en esa carpeta no se copió.
- `vietti.py` (Villa La Roccia, Luigi Vietti, Lago Maggiore) queda como armador sin uso: el usuario la vio más Streamline.
- **Alwyn Court:** se confirmó Neorrenacimiento francés (1907–1909; Wikipedia y la Landmarks Preservation Commission lo describen "en estilo Renacimiento francés" con ornamentación Francisco I: un revival).
- Pruebas nuevas: `herramientas/prueba/listas.html` (listas más cortas), `decadas.html`; `detalle.js` ahora muestra Pintoresquismo y Racionalismo.
- **Lo pixelado de las fotos en la grilla** al alejar el zoom en Chrome: es por achicar fotos de 1600 px a ~150 (ver miniaturas, punto 5).

**10 de noviembre de 2026, segunda parte (cierre).** Subido (`v66`), junto con El Planeta de la primera parte.

**Próxima sesión:**
1. **Pieles por estilo** (idea del usuario, aprobada para probar): cada estilo con su propio diseño fiel (colores, tipografía, bordes, texturas) sobre la misma estructura; las fichas de las obras toman la piel de su estilo, los arquitectos la de su estilo principal; tapas de discos de la época como inspiración, sin copiar. Arrancar con una página de prueba en `herramientas/prueba/` con **Brutalismo y Art déco** (página del estilo + ficha de una obra, claro y oscuro, al lado de cómo se ven hoy) y esperar que elija. Cuidar legibilidad y no sumar muchas fuentes.
2. Símbolos de **Pintoresquismo** y **Racionalismo** (sin carpeta de referencias: pedir o proponer joyas ocultas).
3. Seguir con datos de casas cuando el usuario mande capturas de Google Lens. Pendiente: ¿la foto de Wikimedia "Traditional english-style house in Florida" (Lombardia1, CC BY-SA 4.0) es la Casa Tudor? Casa curva del 4/10 sin dirección.
4. Revisar en el iPhone: círculos de zona en el mapa, El Planeta, colores de marco.

- **Carpeta de originales ordenada** (con ok del usuario; antes era solo lectura): `2024-07 Inglaterra/`, `2026-07 Atlanta/`, `2026-07 Nueva York/` (ahí quedaron `flatiron` y `guggenheim`), `2026 Buenos Aires/` y `Para después/` (Casa San Isidro del arco, sin fotos de afuera; descartadas del 4/10; sin identificar), una subcarpeta por obra. Solo se movieron archivos, sin renombrar; se borró una captura repetida idéntica. `referencias/` intacta. Las fotos se emparejaron con las de la app por huella de imagen. Ojo: las horas de `mdls` están en UTC (restar 3).
- **Casa Pirán** (Pirán 5619, Villa Urquiza; Territorio Mutante: Julia Lazarte y Roman Kruk, 2025; reforma de casa chorizo de los 40; datos de la ficha de Open House BA, https://openhousebsas.org/catalogo/casa-piran/): es la casa "del amarillo", a una cuadra del edificio verde. Sin foto del frente: portada la cocina amarilla.
- Fotos sumadas: 6 de adentro a Casa Villa Urquiza 3, 3 a Edificio Pirán 5672.
- **14 casas de Florida y Olivos** (paseo del 18/10 y Caseros del 23/10). Nombres descriptivos y direcciones "al 2100" porque la altura sale de la ubicación de la foto (OpenStreetMap) y no es exacta; la única leída en la foto es **Santa Rosa 1977** (OSM daba 1991). Estilo y década estimados por la fachada.
- **Casa Stieglitz:** firma en metal "SIEGFRIED STIEGLITZ / MMO" (maestro mayor de obras). Sin datos publicados (dos búsquedas). El usuario cree que es de los 30 y que la hizo un inmigrante alemán para vivir: se puso década 1930 estimada, lo demás no.
- Quedan sin cargar: casa curva del 4/10 (Villa Urquiza, número "60…", falta la dirección), Santa Rosa al 1900 edificio bajo y 11 de Septiembre 1815 (Belgrano), por flojas.
- **Privacidad de casas particulares (`v63`, pedido del usuario):** las viviendas argentinas (menos Edificio Alca y Urquiza 911, que son públicos) llevan `ubicacion.zona: true`, sin `direccion`, con lat/lng redondeadas a 2 decimales; nombres e ids sin dirección (ej. Casa del techo empinado, Casa de la pérgola, Edificio verde de Villa Urquiza), y carpetas y fotos renombradas. En el mapa: círculo celeste de 900 m (`.zona-obra`, `RADIO_ZONA` en `datos.js`); las de la misma zona se juntan en una lista. Sin "Cómo llegar" ni coordenadas en la ficha. Casa Pirán mantiene el nombre oficial de Open House. Ojo: si había visitas registradas en el iPhone a casas con id viejo, quedan como "no está en el catálogo" (no se borran; se puede sumar un alias). El repo guarda las direcciones viejas en la historia: al usuario no le importa.
- **Edificio Alca** (antes Edificio Aristóbulo del Valle 1601): nombre, Frentebril y "terminado entre fines de 1961 y 1962" de un post de Instagram de @leilainfinito y sus comentarios (capturas del usuario), aclarado como no verificado.
- **Investigación:** Instagram, Facebook y Reddit no se pueden leer desde acá (y leer Reddit por otro lado lo frenó el sistema). Funciona mejor que el usuario mande **capturas** de los posts y comentarios, y que haga la búsqueda por imagen con Google Lens.
- **Casa abovedada de La Paternal** (antes Casa Paz Soldán 4780, `v64`): con dirección y punto exactos (el usuario no quiere protegerla: está muy publicada), `modificada`. Descripción armada con ~75 capturas del usuario (Facebook: Buscando a Salamone 2019, Crónicas de la Reina Inquieta 2025, Arquitectura de siempre 2026; Instagram @pablofe70; Reddit): Isla de La Paternal, retiro de 5 m, lote de 21,71 m, 291 m² cubiertos / 188 m² de terreno (registro de parcelas citado en un comentario), sin firma, Salamone descartado, laboratorio y después departamentos (dos comentarios), agregado de chapa arriba, la señora con el mono tití. **Se dejaron afuera** las acusaciones de usurpación y los dichos sobre dueños e inquilinos (gente real, sin verificar). Pendiente opcional: foto de Wikimedia (Roberto Fiadone, CC BY-SA 4.0).
- **Tanda 2 de investigación (`v65`):** Casona italianizante → **Convento de las Hermanas de la Santa Cruz** (monjas suizas), Virrey del Pino 2275/81, con dirección (es institución), atribuido a Guillermo Álvarez (blog arquitectoguillermoalvarez.blogspot.com, por los remates), protección cautelar, Hermana Bernarda. Casa de los ladrillos calados → **Estacionamiento de los ladrillos calados** (TikTok @azulejosencaba), programa Infraestructura. Stieglitz: registros públicos (dateas, Boletín Oficial) dan un Siegfried Stieglitz nacido en 1926 ligado a una constructora familiar → década 1950 estimada; no se publican CUIT, DNI, domicilios ni parientes. Casas de las palmeras: en Street View 2013 era una casa amarilla y de ladrillo con torre mirador, `modificada`. Casa de la celosía: prácticas de Agrimensura FIUBA 2021 con el Distrito X del Consejo de Agrimensura (¿sede? sin confirmar).
- **Resuelto (`v66`):** Casa del balcón curvo → **Casa Cerati** (el usuario confirma que vivió ahí; dato del barrio, sin fuente publicada; aclarado que no es la de Vicente López de 2008). Los lofts de Kurchan son el **Edificio Urquiza 911**: se sumó Juan Kurchan como arquitecto junto a Ferrari Hardoy (comentario de @buenosaires.alpaso). Queda solo lo de la foto de Wikimedia de la Casa Tudor.
- **Pendientes de esta tanda:** (1) "Casa Cerati": el usuario dice que la del balcón curvo es donde vivió Cerati, pero las notas (Los Andes 2024) ubican su última casa en Vicente López, esquina con Hipólito Yrigoyen, de 1937, comprada en 2008; la del balcón curvo está en Florida por la ubicación de la foto. Confirmar antes de nombrarla. (2) Lofts de Juan Kurchan en Vicente López (comentario de @buenosaires.alpaso): falta saber cuál de las casas es. (3) Foto de Wikimedia "Traditional english-style house in Florida" (Lombardia1, CC BY-SA 4.0): confirmar si es la Casa Tudor. El aviso de roomix da 403.
- **Idea de diseño del usuario sobre tapas de discos:** no la contó todavía; pidió dejarla para después y que **se la recuerden siempre**.
- **Estilos sin símbolo propio (14):** Academicismo, Art déco, Historicismo, Neogótico, Neorrenacimiento francés, Contemporánea, Neofuturismo, Posmodernismo, Racionalismo, Pintoresquismo, Neocolonial, Italianizante, Gótico perpendicular, Barroco eduardiano.

**10 de noviembre de 2026.** **Sin subir (`v61`)**: el usuario no pidió commit.
- **Símbolo de Streamline Moderne = Edificio El Planeta** (Atlántida, Uruguay), aprobado ("perfecto"): `herramientas/simbolos/planeta.py`, fotos en `referencias/simbolos/el planeta/`. De frente: punta redonda a la derecha con cuatro cubiertas que vuelan cada vez más al bajar (sombreadas como cilindro, ventanas que se angostan en la curva, barandas de caño), cuarto redondo, plato con baranda, tambor con ojos de buey y faro con ojo; cuerpo largo de balcones con capotas y toldos rojos a rayas, chimeneas y tanque; basamento alto, más ancho en la curva, con líneas de velocidad, entrada con toldos y pilar con ojo; seto, palmera (el usuario la quiere), cartel azul y pasto. Fondo **celeste de la bandera** (`streamline-celeste`), elegido entre cinco (rambla, celeste, Sol de Mayo, yerba, río).
- `herramientas/prueba/detalle.js` ahora muestra El Planeta y una fila de fondos de prueba. Ojo: `registrarColoresSimbolos` **reemplaza** los colores registrados (no suma): para agregar colores de prueba, pasar `{ ...simbolos.colores, ...extra }`.
- Datos de la obra, sin verificar del todo (una búsqueda): hotel impulsado por Natalio Michelizzi, que lo quiso con forma de barco; construido por Pérez Butler y Pagano. **Arquitecto no encontrado.** No es obra del catálogo, solo el símbolo.
- Se habló de cómo distinguir Art déco, Streamline, Racionalismo y Googie, y del "estilo buque".

**Próxima sesión:** revisar en el iPhone el símbolo nuevo y los colores de marco; subir cuando lo pida. Siguen los pendientes de la entrada de abajo (fotos `.jpeg` nuevas, Ateneo, Instagram, hover).

**9 de noviembre de 2026, segunda parte (cierre).** Subido (`v60`), con todo lo de la primera parte.
- **Un color de marco por estilo, en la app** (aprobado en `herramientas/prueba/estilos-color.html`): 19 colores nuevos en `estilos.css` (claro y oscuro), `.marco-*`, `COLORES_MARCO` (`datos.js`) y `COLORES_TEMA` (`grafica.js`); `color` de cada estilo en `perfiles.json`. Moderno sigue en `petroleo` y Arquitectura orgánica en `follaje`; `cielo` y `mar` quedan como colores de tema. Obras sin estilo: `cal` (gris piedra), ya no al azar. Los nombres no pueden chocar con los colores de `simbolos.json` (por eso plomo, carbon, lago, duna, cantera, teja, mostaza, laguna…).
- **Ninguna obra sin estilo:** Casa Urquiza 2299 pasa a **Streamline Moderne** (estilo nuevo, hijo de Art déco, color `laguna`), Peachtree Summit a Moderno tardío (estimado: las fuentes solo dicen "modern") y Casa Villa Urquiza 3 a Arquitectura contemporánea (gris claro `niebla`, pedido del usuario para distinguirla del Brutalismo).
- **Próxima sesión:** hacer el **símbolo de Streamline Moderne** (pedido del usuario; buscar o pedir fotos de referencia y crear la carpeta en `referencias/simbolos/`). Revisar en el iPhone los colores nuevos. Siguen los pendientes de abajo (fotos `.jpeg` nuevas, Daca y Hotel en el iPhone, Ateneo, Instagram, hover).
- Casa Villa Urquiza 3 queda en Contemporánea (el usuario preguntó si era Racionalismo: es una reforma de 2025 de una casa chorizo, no una obra de los años 30 y 40).

**9 de noviembre de 2026.** **Sin subir (`v59`)**: el usuario no pidió commit.
- **Mundo 1980 = Asamblea Nacional de Bangladesh** (`herramientas/simbolos/daca.py`, fotos en `referencias/simbolos/daka/`). De frente y simétrica, a 3 px por línea (curvas parejas): bloques con triángulos (con canto de luz adentro), ojos redondos, ranuras, cilindros sombreados en siete tonos, corona con arcos de medio punto; luz desde la izquierda (lado derecho en sombra, colores `-s`) y juntas de mármol (`-j`). Abajo, **lago con el reflejo** en espejo (colores `-r`, mezcla con el agua) y ondas. Fondo **blanco en claro y negro en oscuro** (`daca-fondo`), elegido por el usuario. "Increíble". Datos verificados: Louis Kahn, inaugurada el 28/1/1982 (el inicio de obra varía según la fuente: 1961, 1962 o 1964; se puso solo 1982).
- **Hotel** rehecho (`hotel.py`), aprobado: celdas de 8 × 8 alternadas como tablero, cada una un tronco de pirámide con biseles y sombra en triángulo abajo; franja de ladrillo, almenas, cartel verde arriba, algunas cortinas corridas, dos pisos de ventanas, columnas y cartel azul. Mantiene `hotel-cola`.
- **15 casas y edificios de barrio cargados** (G20–G31 por hora; G19 es el Vessel). Direcciones de capturas de Street View del usuario; barrios por geocodificación inversa de OpenStreetMap. Nombres "Casa/Edificio <calle número>", sin arquitecto ni año, resumen con lo que se ve en la foto. Edificios (Vivienda colectiva): Aristóbulo del Valle 1601, Urquiza 911 (esquina Segurola), Pirán 5672. **Casa Villa Urquiza 3** (Pje. Talavera 5882): datos de la ficha de Open House BA (Waldman y Andreani Ghiglione, 2025, reforma de casa chorizo); el usuario va a mandar fotos de adentro. Ojo: sus dos fotos tienen la fila de visitantes.
- Casas buscadas en la web por dirección: **ninguna tiene información publicada** (solo avisos inmobiliarios de otras alturas). Se les puso **estilo y década estimados por la fachada** (campo `decada`), y el resumen lo aclara. Estilos nuevos en `perfiles.json`: Racionalismo (de Moderno), Pintoresquismo, Neocolonial e Italianizante (de Historicismo).
- Allen Plaza: portada cambiada a la segunda foto (la primera quedaba muy recortada).
- **El usuario no quiere tanto "azul y amarillo de Boca"** en los marcos (paleta `--petroleo/--follaje/--cielo/--mar`). Página nueva `herramientas/prueba/paleta.html`: la lista de obras de la app con tres paletas (A Tierras, B Otoño, C Piedra y ladrillo), en claro y oscuro. Falta que elija.
- **Edificio Urquiza 911 atribuido a Jorge Ferrari Hardoy** (lo recordó el usuario): el inventario de su archivo en Harvard (GSD) lista "Segurola & General Urquiza (Vicente López)", de fines de los 40 (leído por el buscador; el PDF da 403). Ficha con `arquitectos` y descripción que explica la atribución; década 1940 estimada.
- **Fotos nuevas en `~/medianeras-originales/`: 75 `.jpeg`** (antes no había `.jpeg`; los grupos G0–G32 solo tomaban HEIC/JPG/MOV/png). Por día: 23 del 4/10 (desde las 16:32, justo después de la visita de Open House: probablemente el interior de Casa Villa Urquiza 3), 6 del 5/10, 41 del 18/10, 2 del 22/10 y 3 del 23/10. Ojo: `IMG_0002.HEIC` (4/10, 16:32), usada como Edificio Pirán 5672, es de la misma tanda; confirmar con el usuario que sea Pirán y no parte de la visita.
- Al correr `daca.py` la primera vez se vació `simbolos.json` (el error de abrir para escribir y leer en la misma línea); se recuperó de git y se corrigió.

**Próxima sesión:**
1. **Paletas por estilo (plan aprobado por el usuario, hacer primero):** le gustan todos los colores de `herramientas/prueba/paleta.html` (Hoy, A Tierras, B Otoño, C Piedra y ladrillo) y quiere **un color propio para cada estilo arquitectónico**, en vez de 4 marcos que se repiten (el azul y amarillo "de Boca" no le gusta).
   - a. Pasar de 4 a ~16 colores de marco en `www/css/estilos.css` (claro y oscuro), con nombres de lugar como hoy; ampliar `COLORES_MARCO` en `www/js/datos.js` (y revisar `.marco-*`, `colorValido`, el hash de las obras sin estilo y los usos de `--familia`).
   - b. Asignar en `perfiles.json` un `color` a cada uno de los 19 estilos; los hijos (Brutalismo, Racionalismo, Neogótico…) con un tono de la familia del padre. Obras sin estilo: un color fijo neutro (piedra).
   - c. Mostrar la asignación en una página de prueba (estilo, color, claro y oscuro, y tapas reales) y **esperar que elija/cambie** antes de pasarlo a la app.
   - d. Pasar a la app, capturas en claro y oscuro, subir `VERSION` del service worker.
2. Ordenar las 75 fotos `.jpeg` nuevas (agrupar por hora con `mdls`, contactar al usuario): interior de Casa Villa Urquiza 3 (y elegir portada sin la fila de gente), y ver qué son las del 5, 18, 22 y 23 de octubre.
3. Revisar en el iPhone las casas, Daca y el Hotel; subir cuando lo pida (todo sin commit, `v59`).
4. Lo de antes: verificar datos del Ateneo, Instagram y dominio, hover de "Registrar visita".

**31 de octubre de 2026, cuarta parte (cierre).** Subido (`v58`). Cuatro obras nuevas de Inglaterra con fotos propias (copias de 1600 px **sin metadatos**, con permiso del usuario; los originales quedan intactos):
- **George's Dock Building** (Liverpool, G1): Herbert J. Rowse, 1931–1934, Art déco, piedra Portland, Infraestructura.
- **Catedral de Manchester** (G3, 8 fotos): gótico perpendicular desde 1421, Templo, `modificada`. Arquitecto **J. S. Crowther, aclarado como restaurador** (pedido del usuario). En la portada sale el usuario: se queda. Entra en la década de 1420.
- **Iglesia de St Luke** (Liverpool, G0, 7 fotos): John Foster Sr. y Jr., 1802–1832, Neogótico, bombardeada en 1941, `modificada`; escultura de la tregua de Andy Edwards.
- **50 Newton Street / Hatters** (Manchester, G5): Charles Clegg & Son, 1906–1908, Barroco eduardiano, "Industria (hoy hostel)". Portada: `newton-street-02.jpg`.
- Perfiles nuevos: Rowse, Crowther, los dos Foster, Charles Clegg & Son; estilos Gótico perpendicular y Barroco eduardiano.
- **De memoria, sin verificar:** coordenadas de Manchester, St Luke y Newton Street; piedra arenisca de la catedral y de St Luke; vidas de Rowse y de los Foster.
- Grupos de fotos: se rehacen ordenando por `mdls kMDItemContentCreationDate` y cortando con más de 25 min; dan los mismos G0–G30. Ojo: **no intercambiar fotos manteniendo el nombre** (el navegador y el service worker muestran la vieja): cambiar el orden en `obras.json`.
- `obras.json` tiene formato mixto: agregar obras al final como texto, sin volver a escribir todo el archivo con `json.dumps`.

**Próxima sesión:**
1. Revisar en el iPhone el encabezado nuevo, La Pyramide y las cuatro obras.
2. Las casas de barrio de Buenos Aires (G19–G30) y, después, seguir con símbolos.
3. Esperando al usuario: **Hotel** y **Daca** (Mundo 1980, fotos). Lo de antes: verificar datos del Ateneo, Instagram y dominio, hover de "Registrar visita".

**31 de octubre de 2026, tercera parte.** Subido (`v57`).
- **Encabezado nuevo de los perfiles (variante A) en la app** (`perfil.js`, `ui.js`, `estilos.css`): el cabezal (`.perfil-cabezal`) lleva nombre, datos, categorías, símbolo y flechas sobre la placa del símbolo (`--banda`), con textos y flechas en el color del marco (`--detalle`); el color llega a los bordes de la pantalla (border-image, como el pie). Símbolo grande sin recuadro, recortado a su dibujo, con tope de 380 de alto y 520 de ancho. **Blanco y negro** (tema oscuro adentro, fondo `--franja`): los perfiles sin placa (arquitectos, materiales, ciudades, Mundo 1980) y Brutalismo (lista `EN_BLANCO_Y_NEGRO` en `perfil.js`). Los perfiles sin símbolo propio ya no muestran el neutro (salía como un bloque).
- **La Pyramide con más detalle** (`piramide.py`, aprobada): más resolución (5 filas por piso), aleros de listones con juntas y canto claro, ventanas con parantes y plantas, caja blanca bajo la corona, encofrado y ventanitas en la torre, y en la planta baja **locales** con carteles de color, toldos a rayas, vidrieras y puertas (cada lado con sus carteles).

**Próxima sesión:**
1. Revisar en el iPhone el encabezado nuevo y La Pyramide.
2. Pendiente opcional: chips del cabezal más claros si se ven apagados.
3. Esperando al usuario: **Hotel** (al final) y **Daca** (Mundo 1980, fotos). Lo de antes: verificar datos del Ateneo, Instagram y dominio, hover de "Registrar visita".

**31 de octubre de 2026, segunda parte (cierre).** Subido (`v56`). Las cinco décadas de Mundo que quedaban con el sistema viejo, rehechas con armadores en `herramientas/simbolos/` y aprobadas:
- **1950 Seagram** (`seagram.py`, foto `seagramexrt.webp`): ventanas encendidas calcadas de la foto en tres calideces (naranja, ámbar, amarillo claro), 30 módulos de bronce, faja técnica; planta baja con cielorraso, marquesina, hall con puertas giratorias; plaza **en elevación plana** (canteros como cajas bajas con tulipanes asomando), base marrón. Fondo atardecer.
- **1990 Bilbao** (`bilbao.py`): el que más costó. Calcar no sirvió (camuflaje); quedó **por piezas**: cada cáscara es un polígono medido en px, con caras de tono propio (para que se lean los saltos, no por luz real) y adentro un sombreado de chapa curva en una sola dirección ajustado a la luz de la foto (cuadrados mínimos, sin manchas). Canto claro arriba, juntas finas, líneas finas (PASO 4). La sala larga son **dos "bananas"** cruzadas; los extremos terminan en tandas (torreón de piedra a la izquierda, tambor sobre caja de piedra a la derecha); la visera es una cáscara curva con media luna verde y el vidrio del atrio pegado debajo. Grises, sin dorado. Sin araña (escultura).
- **2000 St Mary Axe** (`smaxe.py`): perfil medido, piel sobre cilindro (una diagonal por malla, seis espirales oscuras), cúpula oscura con la misma trama en gris, sin celeste; tronco más azul.
- **2010 CCTV** (`cctv.py`): de noche, de tres cuartos. Rombos grandes y regulares (dos celdas por fila), hueco sacado de la mancha del cielo con canto parejo, bordes rectos, banda oscura paralela a la izquierda y techo grueso que se junta en punta; basamento en otro tono (mira hacia otro lado).
- **2020 M+** (`mmas.py`, foto real `av_imagen.webp`): torre gris cálido de aletas por módulos con franjitas de luz y medio (como el basamento), ventanas prolijas (no calcadas), patas en V sombreadas, jardín bajo, basamento negro de aletas redondeadas, planta baja baja. Sin césped.
- Borrados los colores viejos sin uso de las cinco. `antes.json` (no va al repo) guarda las versiones anteriores.
- **Página nueva `herramientas/prueba/cabezal.html`:** prueba del encabezado de los perfiles sobre la app real. El usuario eligió la **A**: todo el encabezado (migas, nombre, datos, categorías y flechas) sobre el color de fondo del símbolo, textos y flechas en el color del marco (el inverso), símbolo grande sin recuadro apoyado sobre las flechas (recortado a su dibujo, así los altos como el Seagram crecen). Algunos perfiles en blanco y negro (variante C). **Todavía no está en la app.**

**Próxima sesión:**
1. Revisar en el iPhone lo subido.
2. **Pasar la variante A del encabezado a la app** (`perfil.js` y `estilos.css`): proponer plan antes; decidir qué perfiles van en blanco y negro (los de poco contraste, como Brutalismo azul sobre terracota) y si los símbolos anchos (Museo) llevan tope de tamaño.
3. **Brutalismo (La Pyramide, `piramide.py`): más detalle**, pedido del usuario.
4. Esperando al usuario: **Hotel** (al final) y **Daca** (Mundo 1980, fotos). Lo de antes: verificar datos del Ateneo, Instagram y dominio, hover de "Registrar visita".

**31 de octubre de 2026 (cierre).** Subido (`v55`). Al empezar se subió todo lo del 30 (`v54`). En la sesión, ocho íconos rehechos con armadores nuevos en `herramientas/simbolos/`, todos aprobados:
- **Moderno tardío** (`tenerife.py`): el Auditorio de Tenerife **calcado de la foto** (cada celda toma el color medio de su pedazo; el cielo se inunda desde arriba; seis tonos y moda de vecinos). La franja de abajo, redibujada a mano: ala baja con escalera, muro parejo, boca de la entrada con canto gris del arco, balcón recto y columnas; en oscuro la entrada se prende en dorado (`tt-luz`). Sigue con fondo `au-cielo`. Necesita la foto en `~/medianeras-originales` para correr.
- **Brutalismo** (`piramide.py`): La Pyramide de Abiyán, simétrica en grilla: torre lisa más alta que la corona, corona de parasoles, catorce pisos con alero inclinado, pilotes.
- **Mundo 1970** (`pompidou.py`): caños blancos, cruces de tirantes suaves, escalera mecánica con tramos de igual pendiente y descansos en las vigas (tubo en tres tonos sobre la panza roja) y galerías; escaleras de emergencia de las puntas, un tramo por piso. Usa `rectas` para todo lo inclinado.
- **Mundo 1930** (`paimio.py`): los dos edificios a la misma altura y con paso sutil; terrazas con toldos naranja y verde agua; sombra moteada de los pinos en el pabellón.
- **Moderno** (`savoye.py`): solario curvo, ventana corrida, pilotes de atrás más arriba (perspectiva) y **base de un solo piso, blanca** (el usuario no quiere escalones).
- **Salud** (`infirmary.py`): Royal Infirmary mejorado (no reemplazado): simétrico, juntas, sombras, guardapolvos, cúpulas con tambor, nervios y linterna, pináculos y torrecitas con remate.
- **Mundo 1910** (`pedrera.py`): losas en ondas con sombra, ventanas como huecos redondeados con vidrios **apagados** (azul, celeste gris, oscuro; nada brillante), balcones de hierro en grises como banda con dos hierros ondulados, ático, chimeneas, planta baja en arcos.
- **Mundo 1960** (`congreso.py`): torres con juntas y puentes, cúpula y cuenco sombreados (cuenco playo, curva tendida y base ancha), plataforma, rampa, agua y pasto.
- `armar.py` suma `con_colores` (escribe solo los colores; sirve para las décadas, que se guardan con `escribir`). Ojo: nunca `open(ruta, 'w').write(...open(ruta).read()...)` en una línea: vacía el archivo antes de leerlo (pasó, se recuperó de git).
- Borrados los colores viejos sin uso de todos los rehechos.

**Próxima sesión:**
1. Revisar en el iPhone lo subido hoy.
2. Seguir con las décadas de Mundo con el sistema viejo, de a dos: **Seagram (1950), Bilbao (1990), St Mary Axe (2000), CCTV (2010), M+ (2020)**. Todas tienen carpeta. Si se pide más carácter en las chimeneas de La Pedrera, retocarlas.
3. Esperando al usuario: **Hotel** (al final) y **Daca** (Mundo 1980, fotos). Lo de antes: verificar datos del Ateneo, Instagram y dominio, hover de "Registrar visita".

**30 de octubre de 2026, cuarta parte (cierre).** Subido el 31 de octubre (`v54`), con todo lo de las cuatro partes del 30. Rehechos con armadores nuevos, todos aprobados:
- **Templo** (`herramientas/simbolos/gopuram.py`): gopuram del Meenakshi medido sobre `religioso/images (9).jpeg` (basamento de `images (10)`). Once remates dorados, bóveda con medallones y cabezas en las puntas, nueve pisos con cornisa, pabellones y figuras (paradas y sentadas) entre pilastras, salientes apiladas en vertical y abertura en el eje, basamento de granito con puerta. Sigue con fondo granito rosado. "Increíble".
- **Infraestructura** (`hoian.py`): puente de Hoi An medido sobre `infraestructura/images (15).jpeg`. Techo con tramo central alto, adornos de dragón, galería con postes, faroles y baranda, tablero arqueado con placa, pilas con arcos; el vano del medio hueco (sin vista del canal, pedido del usuario); techitos japoneses sobre los muros rojos. Fondo nuevo **jade de canal** (`infra-jade`).
- **Deportivo** (`monumental.py`): Monumental desde arriba. La banda roja de la bandeja alta costó muchos intentos: salió bien recién al **calcarla de la foto** (captura del usuario) y unir las hojas en una cinta en zigzag que toca el borde de afuera en las esquinas y el anillo en el medio de costados y cabeceras (`ROJO_ADENTRO`/`ROJO_AFUERA`). Pista más ancha con dos líneas de carril, bancos de suplentes de un solo lado. Se deja con pista (como en la foto) y con el **fondo verde de siempre** (`riv-suelo`), decisión del usuario.
- Borrados los colores sin uso: `t-*`, `vi-*`, `hoi-*` y `riv-*` viejos. `antes.json` hoy guarda el Monumental viejo.

**Próxima sesión:**
1. **Salud se queda con el Royal Infirmary** (decisión del usuario); si se rehace, mejorarlo con el sistema nuevo, no reemplazarlo. Seguir con los atrasados de `equilibrio.html`: **Hotel** al final (el usuario no quiere cargar fotos ahora); después Moderno tardío, Brutalismo, Moderno y décadas de Mundo viejas.
2. Revisar en el iPhone y subir todo (commit y push solo cuando lo pida). Verificar los datos del Ateneo.
3. Lo de antes: Asamblea de Bangladesh (esperar fotos), Instagram y dominio, hover de "Registrar visita".

**30 de octubre de 2026, tercera parte (cierre).** **Sin subir (sigue `v54`)**: el usuario no pidió commit. Datos de las cuatro obras del día verificados en la web (Tjibaou: Piano, Numea, 1998; Marina City: Goldberg, Chicago, 1959–1968; Shizuoka: Tange, Ginza, 1967; Nakagin: Kurokawa, Ginza, 1972, demolida en abril de 2022): las notas estaban bien. Rehechos con armadores nuevos (`herramientas/simbolos/`), todos aprobados:
- **Vivienda unifamiliar** (`casa.py`): la victoriana medida sobre `residencial/images.jpeg`. Dos techos (cumbrera plana y uno con pico, con su lima) más la torre cónica; tejuelas en rombos arriba y tablas abajo; saliente azul con pilastras; escalera de frente que gira en diagonal hacia la puerta detrás de un panel calado, con poste y pasamanos; canteros con flores. Fondo **mandarina** (`casa-mandarina`). "La casa está perfecta".
- **Arquitectura orgánica** (`guggenheim.py`): Guggenheim medido sobre fotos reales (`stringio.jpg`), ya no la maqueta. Espiral con sombreado de cilindro, Monitor y losa lisos, blancos en crema. Fondo **rojo Cherokee** (`organica-cherokee`). "Abismal".
- **Beaux-Arts** (`ateneo.py`): nuevo, el **Ateneo Rumano** (Bucarest; datos de memoria: Albert Galleron, 1888, sin verificar). Cúpula con nervios, tambor con ojos de buey redondos, frontón con dentículos y acroteras, pórtico de seis columnas jónicas, alas con techo de chapa, rosetas, sillares y pilastra doble en la punta. Fondo **bordó de palco** (`beaux-bordo`). "Increíble". La Ópera de Hanói se descartó.
- Página `herramientas/prueba/detalle.html` ahora muestra antes y después (lee `herramientas/prueba/antes.json`, que no va al repo; hoy guarda la casa y el Beaux-Arts viejos). Los colores viejos `vi-*` (casa) y los del Beaux-Arts viejo siguen en `simbolos.json` sin uso: borrarlos.

**Próxima sesión:**
1. **Rehacer con el sistema nuevo los íconos atrasados**, de a dos, empezando por abajo de `equilibrio.html`: primero **Templo** (gopuram, carpeta `religioso`) e **Infraestructura** (puente de Hoi An); después **Salud** (preguntar si se mantiene el Royal Infirmary, que parecía palacio; si no, proponer joyas ocultas) y **Deportivo** (Monumental); el **Hotel al final** (el usuario no quiere cargar fotos ahora). Más adelante: Moderno tardío, Brutalismo, Moderno y décadas de Mundo viejas.
2. Revisar en el iPhone y subir todo (commit y push solo cuando lo pida). Verificar los datos del Ateneo.
3. Lo de antes: Asamblea de Bangladesh (Mundo 1980, único sin fondo; esperar fotos), Instagram y dominio, hover de "Registrar visita".

**30 de octubre de 2026, segunda parte (cierre).** **Sin subir (sigue `v54`)**: el usuario se fue sin pedir commit. Cuatro íconos nuevos, aprobados, con armadores en `herramientas/simbolos/`:
- **Cultural** = Centro Cultural Tjibaou (`tjibaou.py`, fotos en `referencias/simbolos/cultura/`): tres cases en líneas verticales, una costilla de cada tres con puntas desparejas, tablillas y aros alineados, piel de adentro, cáscara gris; vistas un poco de costado (cumbre corrida a la derecha, `CORRIDO`). Fondo **araucaria** (`cultural-araucaria`).
- **Vivienda colectiva** = Marina City (`marina.py`): dos torres iguales, pétalos en U que se angostan, borde festoneado, piso de vidrio metido y cochera del mismo ancho, con las columnas bajo las juntas de los pétalos. Fondo **ladrillo de Chicago** (`vivienda-ladrillo`).
- **Oficinas** = Centro de Prensa de Shizuoka (`shizuoka.py`, carpeta `shizuoka`): cilindro en paneles, caño, cajas colgadas a distintas alturas, volumen de piedra con la entrada abajo a la derecha y zócalo. Fondo **papel de diario** (`oficinas-diario`).
- **Metabolismo** (estilo nuevo en `simbolos.json`, ninguna obra lo usa todavía) = Torre de Cápsulas Nakagin (`nakagin.py`, carpeta `nagakin`): cápsulas escalonadas, algunas ciegas, núcleos de óxido de techo inclinado (no flecha), basamento. Fondo **añil** (`metabolismo-anil`).
- `armar.py` suma `Lienzo` (pintar en grilla y sacar líneas) y `guardar` (pone o reemplaza un símbolo en cualquier sección, con sus colores). Los cuatro armadores ya escriben `placa`, `aire` y `marco`: se pueden volver a correr sin perder el fondo.
- Datos de las notas de memoria, sin verificar: Tjibaou (Renzo Piano, Numea), Marina City (Bertrand Goldberg, Chicago), Shizuoka (Kenzo Tange, Tokio), Nakagin (Kisho Kurokawa, Tokio, 1972, demolida en 2022).

**Próxima sesión:**
1. **Revisar en el iPhone y subir** todo lo de hoy (commit y push solo cuando lo pida). Antes, verificar los datos de las cuatro notas.
2. **Fondos que faltan:** Vivienda unifamiliar, Arquitectura orgánica y Beaux-Arts. Gamas usadas hoy: araucaria, ladrillo de Chicago, papel de diario, añil.
3. Lo de antes: Asamblea de Bangladesh (esperar fotos), Instagram y dominio, hover de "Registrar visita"; más adelante Industria, Gobierno, Comercio, Educación; G0–G30.

**30 de octubre de 2026 (cierre).** **Sin subir (`v54`)**: el usuario se fue sin pedir commit. Templo confirmado en granito rosado. **Salud** (Royal Infirmary) con fondo **brezo** (`salud-brezo`). **Museo** rehecho: el **Museo Soumaya** (Ciudad de México), con las fotos de `referencias/simbolos/museo/`, armador `herramientas/simbolos/soumaya.py`. Es un reloj de arena en líneas horizontales con juntas tipo ladrillo (el usuario prefirió esto a la versión vertical, más "escamas"), placas en cinco grises (`so-1` a `so-5`), la lengua de sombra difuminada, un filo claro arriba y el canto de acero abajo. **Sin base** (se probó con zócalo, jardín vertical y vereda; el usuario eligió sin). Fondo **cempasúchil** (`museo-cempasuchil`). Ojo: si se vuelve a correr `soumaya.py`, reescribe la entrada y borra `placa`, `aire` y `marco` (hay que volver a ponerlos). La carpeta `museo` también tiene fotos de la Casa Azul (Frida Kahlo), no usadas.

**Próxima sesión:**
1. **Revisar en el iPhone y subir** (commit y push solo cuando lo pida).
2. **Íconos nuevos, de a dos** (así los quiere el usuario: "dos y dos" son tandas de dos íconos, no dos versiones). Primera tanda: **Cultural** (Centro Cultural Tjibaou, Renzo Piano, Nueva Caledonia) y **Oficinas** (Centro de Prensa de Shizuoka, Kenzo Tange, Tokio). Segunda: **Vivienda colectiva**, probando **Nakagin** (Kurokawa, Tokio) y **Marina City** (Goldberg, Chicago). Datos de memoria, verificar. Esperar las carpetas `cultural`, `oficinas`, `nakagin` y `marina city` en `referencias/simbolos/`. El usuario dijo que el ícono actual de Oficinas, el de Cultural (telón) y el de Vivienda colectiva no le gustan.
3. **Fondos que faltan:** Vivienda unifamiliar, Arquitectura orgánica y Beaux-Arts (y los de los íconos nuevos). Gamas ya usadas, sumar: brezo y cempasúchil. Propuestas que no se eligieron y siguen libres: verde sala, arenisca roja, cobre, musgo, cemento cálido, dorado de sala, verde terciopelo, marfil, damasco, oliva, lavanda gris, rosa mexicano, jade.
4. Lo de antes: Asamblea de Bangladesh (esperar fotos), Instagram y dominio, hover de "Registrar visita"; más adelante Industria, Gobierno, Comercio, Educación; G0–G30.

**28 de octubre de 2026, cuarta parte (cierre).** Subido (`v53`). El usuario revisó en el iPhone lo subido antes y está todo bien. Fondos nuevos con aire y marco invertido: **Brutalismo** laterita (`brut-laterita`), **Hotel** cola, rojo tierra (`hotel-cola`) y **Templo** granito rosado (`templo-granito`). Ojo: para el Templo el usuario escribió "granito azafran"; se aplicó granito rosado (`#d5b8ab`). Preguntarle si quería el azafrán (`#e8a85a` / `#43301a`). **Museo:** sin fondo, porque el usuario quiere un ícono nuevo (hoy es una pared con tres cuadros).

**Próxima sesión:**
1. Confirmar el fondo del Templo (granito o azafrán).
2. **Ícono nuevo de Museo:** pedir carpeta de fotos en `referencias/simbolos/` (una obra de museo, mejor no occidental) y después elegir su fondo.
3. **Más fondos** de a varios en `fondos.html`: Salud, Oficinas, Cultural, Vivienda colectiva y unifamiliar, Moderno, Arquitectura orgánica, Beaux-Arts. Ya usados: laterita, cola, granito rosado y todas las gamas de Argentina y Mundo (ver más abajo).
4. Lo de antes: Asamblea de Bangladesh (esperar fotos), Instagram y dominio, hover de "Registrar visita"; más adelante Industria, Gobierno, Comercio, Educación; G0–G30.

**28 de octubre de 2026, tercera parte.** Subido (`v52`): el **Banco de Londres** (1960s Argentina) se reemplaza por la **Escuela Superior de Comercio Manuel Belgrano** de Córdoba (Bidinost, Chute, Gasó, Lapacó y Meyer; concurso de 1960, construida 1960–1971, inaugurada en 1968, Monumento Histórico Nacional en 2019: verificado en el Decreto 791/2019 y Divisare). Fotos del usuario en `referencias/simbolos/60s argentina/`. Armador `belgrano.py`: techo con canto lleno y cielorraso de madera que se curva a las puntas, columnas que tocan el techo (las de las puntas bajan al piso), bóvedas de luz, a la izquierda el hall vidriado de doble altura y a la derecha el bloque de aulas con la ventana corrida roja, chimenea hasta el piso y muro de piedra. Fondo **arena serrana** (`belg-arena`), elegido por el usuario. En oscuro, el edificio usa los mismos colores que en claro (pedido del usuario; propio `belg-vidrio`). Probó un rojo y un vidrio más suaves y prefirió los fuertes.

**28 de octubre de 2026, segunda sesión (cierre).** Subido lo del cierre anterior en `6f09eba` (`v50`) y lo de esta sesión (`v51`): fondos elegidos para la Confitería del Molino (**caramelo**, `molino-caramelo`) y el CCK (**eucalipto**, `cck-eucalipto`), con aire y marco invertido como los demás. Rehechos con armadores: **Palacio Barolo** (`barolo.py`: el edificio entero, de frente y simétrico: faro, cúpula, cupulitas, arcos góticos, mansardas verdes con ojos de buey, siete pisos con balcones redondos y planta baja con el arco de la entrada) con fondo **noche de faro** (`barolo-faro`), y **Puente de la Mujer** (`puente.py`: el ala es una cuña de bandas que se juntan en la punta y abajo se acuestan en curva sobre el tablero; tirantes casi transparentes perpendiculares al ala; pila; agua marrón del dique) con fondo **malva** (`pm-malva`). Ojo: el ala es casi blanca y sin fondo no se ve en claro (siempre va con su fondo). El usuario aprobó los dos ("el barolo, impecable") y dejó el agua marrón. Gamas ya usadas en Argentina: ladrillo, terracota, óxido, gris plomo, lila, mostaza, pizarra, caramelo, eucalipto, noche de faro, malva.

**Próxima sesión:**
1. Revisar en el iPhone lo subido hoy.
2. **Banco de Londres (1960s Argentina):** elegir reemplazo (el usuario no está seguro del Teatro San Martín) y pedir su carpeta de fotos.
3. **Fondos de programas y estilos** (Brutalismo, Hotel, Templo, Museo, Salud, Oficinas, Cultural, etc.), de a varios en `fondos.html`.
4. Lo de antes: Asamblea de Bangladesh (esperar fotos), Instagram y dominio, hover de "Registrar visita"; más adelante Industria, Gobierno, Comercio, Educación; G0–G30.

**28 de octubre de 2026 (cierre).** **Sin subir (`v50`)**: el usuario se fue antes de pedir commit. En la sesión, con armadores nuevos en `herramientas/simbolos/` y una ayuda común `armar.py` (pasa píxeles de la foto a unidades, pinta filas, zonas, rectas y arcos, y reescribe una sola entrada de `simbolos.json`):
- **Biblioteca Nacional** (`biblioteca.py`): rehecha con líneas y zonas, volumen curvo claro en el hueco oscuro entre los apoyos (rayas verticales), ojos de buey redondos con aro y, con dos fotos nuevas, la azotea (caja con rejillas, tanque amarillo, dos torres, caja baja). Ojos de buey centrados: el usuario los dejó así. Fondo **lila** (`bn-lila`). "Increíble como quedó".
- **Centro Cultural Recoleta** (`recoleta.py`): rehecho en grilla (las aberturas de arriba y abajo sobre los mismos ejes de la foto), más filas y molduras finas; la primera versión le pareció "medio infantil". Fondo **mostaza** (`rec-mostaza`).
- **Teatro Colón** (`colon.py`): frontón con rectas, luneta, columnas simétricas, siete ventanas en arco, relieves iguales, puertas bajo sus ventanas. Fondo **pizarra** (`colon-pizarra`).
- **Confitería del Molino** (`molino.py`, fotos nuevas en `referencias/simbolos/el molino/`): de frente y simétrico; aguja, chapitel de pizarra verdosa, aspas con rectas, torrecitas, cuatro pisos con balcones, confitería con vitrales. Aprobado ("buenísimo").
- **CCK** (`cck.py`): misma idea (mitad Correo y Ballena), con la mitad del Correo medida sobre la foto. Ballena más gris a pedido del usuario. Aprobado.

**Próxima sesión:**
1. **Revisar en el teléfono y subir** lo de hoy (commit y push solo cuando lo pida).
2. **Fondos para el Molino y el CCK** (tres opciones cada uno en `herramientas/prueba/fondos.html`, cambiando `OBRAS` en `fondos.js`). Gamas ya usadas en Argentina: ladrillo, terracota, óxido, gris plomo, lila, mostaza, pizarra. Siguen sin fondo: Barolo, Banco de Londres, Puente de la Mujer, y los programas y estilos.
3. Lo que seguía: Asamblea de Bangladesh (esperar fotos), Banco de Londres (reemplazo), Instagram y dominio, hover de "Registrar visita". Más adelante: Industria, Gobierno, Comercio, Educación; G0–G30.

**27 de octubre de 2026 (cierre).** Subido (`v47`). En la sesión: opción nueva del dibujador, **`zonas`** (rectángulos llenos o con rayas en la otra dirección, encima de las líneas; en `grafica.js` y el README), para mezclar texturas. Rehechos con zonas: **Eames** (galería abierta a la izquierda, más alta), **Bauhaus** (ahora el frente de la entrada: bloque gris lleno, letras, cuatro ventanas iguales rojo oscuro, alero, puerta naranja, anexo que tapa apenas), **Stoclet** (más detalle, simétrico y en grilla) y, un poco, la **Casa sobre el Arroyo** (vidrio oscuro transparente, hormigón y pilares llenos, pasto en rayitas). Armadores en `herramientas/simbolos/` (`eames.py`, `bauhaus.py`, `stoclet.py`). Fondos elegidos: Stoclet ciruela (primero fue verde oliva, pero se confundía con el mármol), Eames arcilla rosada, M+ jardín, Bauhaus ocre dorado, Kavanagh gris plomo cálido, Arroyo ladrillo suave, Curutchet terracota, SOMISA óxido. Página nueva `herramientas/prueba/detalle.html` (símbolo rehecho al lado de su foto; lista `OBRAS` en `detalle.js`); `fondos.js` ahora pone el marco invertido y separa colores por colección.

**Reglas nuevas del usuario:** no todo en líneas horizontales (mezclar verticales y formas llenas, para todos los íconos); simétrico y prolijo cuando el edificio lo amerita (ventanas iguales, grilla).

**Próxima sesión:**
1. **Más fondos** con gamas nuevas (mostaza, lila, ladrillo, malva, óxido): quedan Argentina 1900 (Colón), 1910 (Molino), 1920 (Barolo), 1960 (Banco de Londres), 1980 (Recoleta), 1990 (Biblioteca), 2000 (Puente de la Mujer), 2010 (CCK) y los programas y estilos. Ojo: Paimio, Bilbao y M+ ya son verdes.
2. **Más detalle con zonas:** CCK, Centro Cultural Recoleta, Colón y Biblioteca Nacional.
3. Asamblea de Bangladesh (esperar fotos), Banco de Londres (reemplazo), Instagram y dominio, hover de "Registrar visita". Más adelante: Industria, Gobierno, Comercio, Educación; G0–G30.

**26 de octubre de 2026, tercera sesión (cierre).** Subido (`v46`). En la sesión: arreglos a St Mary Axe (más ancho), Villa Savoye (ventana corrida simétrica, sin cielo ni pasto dibujados, con fondo simple), Kavanagh (simétrico, con escaloncitos y escalón intermedio) y Guggenheim de Nueva York (sin la base de maqueta, rayas de la espiral en diagonal); fondos propios (`placa`) con borde (`aire`) y marco (`marco`) para 12 íconos de obras; cancha dibujada en el Monumental; Tenerife con un celeste más suave. Opciones nuevas del dibujador: `rectas`, `aire` y `marco` (en el README).

**Próxima sesión:**
1. **Confirmado por el usuario:** marcos en el color invertido de su propio fondo (colores `<fondo>-marco`), Monumental con cancha, Savoye con fondo simple y Tenerife más suave. Las banderas no llevan marco.
   **Ojo con los colores de fondo:** dejar de proponer tanto celeste y azul, que ya hay mucho ("me encanta igual, pero no abusemos"). Buscar otras gamas (tierras, verdes, ocres, rosados, grises cálidos).
2. **Asamblea Nacional de Bangladesh** (Louis Kahn, Daca, terminada en 1982; datos de memoria, verificar) reemplaza a la Pirámide del Louvre en los 80 de Mundo: el usuario no pudo cargar fotos todavía. Esperar `referencias/simbolos/daca/` (o el nombre que elija).
3. **Más fondos, de a varios:** quedan sin fondo Mundo 1900 (Stoclet), 1920 (Bauhaus), 1940 (Eames), 2020 (M+), todas las de Argentina y los programas y estilos sin fondo (Brutalismo, Hotel, Templo, Museo, Salud, etc.). Mostrarlos en `herramientas/prueba/fondos.html` (cambiar la lista `OBRAS` de `fondos.js`) con tres colores cada uno, con aire y marco como los elegidos. Elegidos hasta ahora: Brasilia durazno, St Mary Axe gris azulado, CCTV neblina amarilla, Pedrera cielo mediterráneo, Paimio verde pino, Seagram atardecer naranja, Pompidou cielo gris celeste, Bilbao verde monte, Savoye celeste/azul.
4. **Más detalle y más líneas:** Stoclet ("quedó atrasado"), Eames ("perfecta pero con muy poquitas líneas"), CCK, Centro Cultural Recoleta, Colón y Biblioteca Nacional ("medio fea y básica").
5. Banco de Londres (1960s Argentina): reemplazo por decidir; el usuario no está seguro del Teatro San Martín.
6. Instagram y dominio (ver Pendientes). Probar con el mouse el hover amarillo de "Registrar visita".
7. Más adelante: Industria (Battersea), Gobierno (Budapest), Comercio y Educación (carpetas ya listas); G0, G1, G3, G5 y las casas de Buenos Aires (G19–G30). Para revisar: Salud parece más palacio que hospital; Vivienda unifamiliar quizás no occidental.

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

- **Instituto del Mundo Árabe (Jean Nouvel, París, 1987; datos de memoria), guardado para más adelante:** al usuario le pareció muy interesante (la fachada de diafragmas metálicos tipo celosía). No usarlo para los 80 de Mundo (va la Asamblea de Bangladesh); buscarle lugar en otro perfil.
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
- **Armadores de símbolos.** Están en `herramientas/simbolos/`; la fuente es `simbolos.json`. Los viejos (`simbolos*.py`) pisan el archivo entero: no volver a correrlos. Los nuevos (`biblioteca.py`, `recoleta.py`, `colon.py`, `molino.py`, `cck.py`, con `armar.py`; y `eames.py`, `bauhaus.py`, `stoclet.py`) reescriben solo su obra: se corren desde esa carpeta con `python3 <armador>.py ../../www/data/simbolos.json`. Ojo: pisan los retoques hechos a mano en esa obra; `placa`, `aire` y `marco` se conservan.
- **Mapa en oscuro.** Los mosaicos de OpenStreetMap se oscurecen con un filtro CSS y no son mosaicos oscuros propios.

## Proyecto chico: lo que pensé (13/11, para contarle al volver)

Borrador; revisarlo antes de presentarlo y no inventar datos.

- **Jagten grande, en pausa y presentable:** no tirar nada. Más adelante, una carpeta de presentación (qué es, cómo se ve, qué falta, qué necesitaría un socio). Lo ya hecho sirve igual.
- **Recomendación para el proyecto chico: placas de arquitectos de Buenos Aires.** Por qué:
  - Lo puede hacer solo: cada placa es una foto suya desde la vereda; no hay problema de derechos ni de interiores. Ojo con la privacidad de las casas: la placa nombra al arquitecto, no al dueño, pero la ubicación de una casa particular igual va por zona.
  - Es original y finito: se puede "completar" un barrio.
  - Le da sentido literal a **jagten** (la caza): salir a cazar placas.
  - Enseña: cada placa dice quién la hizo, a veces el año, el constructor, el ingeniero; de ahí salen perfiles de arquitectos, tipografías de las placas (bronce, letras de época), mapa y décadas. Resuelve el "arquitecto no encontrado" de las casas de barrio (Stieglitz ya es un caso).
  - Se puede volver juego: álbum de figuritas, mapa con las que faltan, rachas.
  - Reusa lo que ya está hecho (PWA, mapa, perfiles, tapas).
  - A verificar: si ya hay cuentas o sitios que juntan placas de Buenos Aires (creo que hay en Instagram, de memoria); si existen, ver qué haría distinto.
- **Otras, en orden:** (2) Streamline en Buenos Aires: tema acotado y lindo, usa los símbolos, pero hay pocas obras y cuesta clasificar. (3) Juego de "adiviná el estilo o la década" con los símbolos: enseña y es chico, pero sin contenido propio nuevo. (4) IA de arquitectura: la más cara y la menos propia; no la recomiendo para hacer solo.
- **Se pueden combinar:** placas como base, y el juego de adivinar como sección.

## Alcance: núcleo y cinturón (12/11, respuesta para leer)

El usuario se fue antes de leerla y pidió anotarla entera.

### Las casas (antes de lo grande)

- **Casa Tudor de Florida:** de acuerdo, es *mock Tudor* mezclado con la casa "moderna" de ladrillo, amplia y baja, de los 60 a principios de los 80 (garaje ancho, paños vidriados grandes). Pediste "Tudor + las dos etiquetas", pero hoy una obra lleva una sola etiqueta (`copia`), y además no recomiendo sumar "neo". Las etiquetas dicen *qué relación tiene con el estilo* (copia de campo o vuelta de época), y "pintoresquista" ya dice que es copia. Lo de los 70 no es una etiqueta, es **otro estilo mezclado**. Propuesta: estilo Tudor, etiqueta pintoresquista y la mezcla contada en la descripción. Si aparecen más casas mezcladas, recién ahí sumar un campo de "estilo secundario". Ya quedó cargada como Tudor + pintoresquista.
- **Chalet amarillo:** "chalet suburbano" sí le queda como descripción, y coincide con lo que te dije del *pavillon de banlieue* francés (en francés, suburbano). "Neocolonial" no: no tiene nada colonial. Ojo con la fuente: un posteo de Threads sobre casas chilenas sirve como pista, no como dato.
- **Techo empinado:** tus hallazgos lo aclaran. Dos de los tres parecidos son franceses: una villa en Villers-lès-Nancy y otra en Antananarivo (Madagascar fue colonia francesa). Es la **villa francesa de entreguerras**: techo alto regional con cuerpo curvo art déco. Con lo que ya tenemos, la pondría en **Streamline Moderne**, sin etiqueta pintoresquista (no copia una casa de campo) y con el techo contado en la descripción. La de Fisherton (Rosario) es la versión argentina de lo mismo.
- **Casa de los arcos:** la de New Orleans es el mismo tipo. "Bungalow de qué estilo": el bungalow estadounidense es la rama doméstica del **Arts and Crafts**, que allá se llamó *Craftsman*. Algunos, como esa y la tuya, suman ornamento clásico (columnas, escudos). Más adelante se puede crear "Arts and Crafts" como padre de Bungalow. (Zillow dice "Built in 2015" para la de New Orleans; casi seguro es un error del aviso y no un dato.) Ya quedó cargada como Bungalow + pintoresquista.
- **Casa María y Blanca de Olivos:** se quedan en Pintoresquismo por ahora. No pasa nada si una casa queda "a decidir": eso también es parte de acotar (ver abajo).

### 1. Núcleo y cinturón

Estoy de acuerdo con la lectura en términos de Lakatos, con un ajuste. El núcleo no es solo "un diario personal de visitas", sino **"la arquitectura que vi, mirada por mí, con un lenguaje gráfico propio"**. Las tapas de impreso, los símbolos de líneas y los perfiles como Letterboxd no son decoración: son lo más original del proyecto. Y los **símbolos resuelven el problema de los derechos**: una obra sin foto propia puede tener su dibujo propio.

Lo que choca está en el cinturón, como decís: cobertura total, enciclopedia exhaustiva, ubicación exacta, interiores y clasificar todo con precisión de libro.

Una idea de Lakatos que conviene usar: un programa es **progresivo** si los cambios al cinturón abren cosas nuevas, y **regresivo** si solo tapan agujeros. Achicar el alcance es progresivo si de ahí sale algo que antes no se podía hacer (profundidad, un tema propio). Es regresivo si solo sirve para no frustrarse.

### 2. Tres formas de acotar

- **A. Solo lo que visité** (regla de entrada: "si no lo vi en persona, no entra").
  - Se gana: todas las fotos son tuyas, el catálogo es honesto y no hay que cubrir nada.
  - Se pierde: la enciclopedia como consulta; los perfiles de arquitectos y estilos quedan con pocas obras.
- **B. Por territorio: tu recorrido** (Villa Urquiza, Florida, Olivos, Vicente López), más los viajes como sección aparte.
  - Se gana: profundidad real, como un atlas de barrio que se puede completar, con fichas investigadas, décadas y comparaciones.
  - Se pierde: lo famoso queda en "viajes", y las casas particulares (las más interesantes del barrio) son justo las de la privacidad.
- **C. Por tema: la casa de barrio del siglo XX en Buenos Aires** (pintoresquistas, racionalistas, cajón de ladrillo de los 70, mezclas).
  - Se gana: un tema poco documentado, donde lo tuyo aporta algo nuevo, y que va con lo que estudiás.
  - Se pierde: variedad (Nueva York, Inglaterra), y es el tema más difícil de clasificar (el pintoresco que te frustra).

**Recomendación:** A como regla y B como foco. Entra solo lo que viste; crece sobre todo en tu zona; los viajes quedan como lo que son: visitas. C puede ser una lista o una serie dentro de B, no todo el proyecto. Con eso, la parte de enciclopedia sigue, pero como **enciclopedia de lo que vi**: los perfiles de estilo y de arquitecto explican, pero no prometen estar completos.

### 3. Ubicación y fotos con privacidad

- **Ubicación:**
  - Edificios públicos o visitables (iglesias, museos, oficinas, Open House): dirección exacta.
  - Casas particulares: solo el barrio y la zona en el mapa, como ya se hace desde `v63`, con círculo y sin número. No usar el nombre de los dueños; nombres descriptivos ("Casa de los arcos").
- **Fotos:**
  - Exteriores propios, desde la vereda, sin chapas de autos, número de puerta ni personas reconocibles.
  - De otros: solo con licencia abierta (Wikimedia Commons, con crédito, como ya hay una).
  - Lo demás, **link afuera** ("ver fotos en…") y nunca copiado.
  - Sin foto: el símbolo propio.
- **Interiores:** solo en lugares abiertos al público (Open House BA, museos, edificios visitables). Para casas, link a la publicación del estudio o de la revista. No es una falta del proyecto: el diario dice lo que viste, y de una casa privada viste la fachada.
- **Clasificación:** "estilo a decidir" o "mezcla" es una respuesta válida. Mejor eso que inventar.

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

### 26 de octubre de 2026 (tercera sesión)

- Arreglos pedidos: St Mary Axe 18 % más ancho en dos pasos; Villa Savoye con la ventana corrida en 16 paños iguales y, al final, sin cielo ni pasto dibujados (fondo `savoye-fondo`, celeste en claro y azul en oscuro); Kavanagh simétrico (el lado derecho bajaba en dos escalones), con la columna de afuera de cada nivel un escaloncito más baja y un escalón intermedio entre la base y el segundo nivel; Guggenheim de Nueva York sin la tabla de la maqueta y con las tres rayas de la espiral en diagonal, del mismo grosor y a la misma distancia.
- Dibujador (`grafica.js`): `rectas` (bandas inclinadas), `aire` (borde del fondo; el dibujo se achica para hacerle lugar) y `marco` (filete alrededor del fondo). Documentado en el README.
- Fondos elegidos por el usuario en `herramientas/prueba/fondos.html` (página nueva) y marcos comparados en `marcos.html` (nueva). Monumental con la cancha (bordes, mitad, círculo y áreas en `riv-cal`). Tenerife: `au-cielo` claro pasa de `#3f78c4` a `#c3d6ea` ("muy fuerte, no va con la estética").
- 80s Mundo: el Louvre sale. Se propusieron Templo del Loto y HSBC (descartados: se parecen a Tenerife y a SOMISA), después Bangladesh, Portland Building, Hundertwasserhaus e Instituto del Mundo Árabe. Elegida Bangladesh; el Instituto queda guardado (ver Pendientes).

### 28 de octubre de 2026

- Símbolos rehechos con más detalle, cada uno al lado de su foto en `herramientas/prueba/detalle.html`: Biblioteca Nacional (con azotea, de dos fotos nuevas), Centro Cultural Recoleta (dos vueltas: la primera "medio infantil", la segunda en grilla), Teatro Colón (emprolijado), Confitería del Molino (fotos nuevas) y CCK (mitad del Correo medida; Ballena más gris: `ballena` y `ballena-2` desaturados).
- Ayuda común `herramientas/simbolos/armar.py` y un armador por obra. Colores nuevos: `bn-oscuro`, `bn-parasol`, `bn-ambar`, `molino-piedra`, `molino-sombra`, `molino-pizarra`.
- Fondos elegidos en `fondos.html`: Biblioteca lila, Recoleta mostaza, Colón pizarra (con marco del color invertido).
- `sw.js` en `v50`. Nada commiteado.

### 28 de octubre de 2026, cuarta parte

- Fondos para Brutalismo (laterita), Hotel (cola) y Templo (granito rosado), elegidos en `fondos.html` entre tres opciones cada uno. Museo queda sin fondo hasta rehacer su ícono.

### 30 de octubre de 2026

- Fondos: Salud brezo (elegido entre verde sala, arenisca roja y brezo); Oficinas, Cultural y Vivienda colectiva se mostraron pero el usuario prefiere íconos nuevos.
- Museo rehecho como Museo Soumaya (`soumaya.py`), sin base y con fondo cempasúchil (opciones: rosa mexicano, jade, cempasúchil).
- `fondos.js`: las claves de color de prueba ahora cambian los espacios por guiones (con "Vivienda colectiva" salía fondo negro).
- `sw.js` en `v54`. Nada commiteado.

### 30 de octubre de 2026 (tercera parte)

- Fondos elegidos: casa mandarina, Guggenheim rojo Cherokee, Ateneo bordó de palco.
- Armadores nuevos: `casa.py`, `guggenheim.py`, `ateneo.py`. Beaux-Arts pasa a ser el Ateneo Rumano.
- `detalle.js` con antes y después (`antes.json`); `fondos.js` con las opciones del día.
- Datos de Tjibaou, Marina City, Shizuoka y Nakagin verificados. Nada commiteado.

### 13 de noviembre de 2026

- Proyecto chico conversado: placas → jagten (Instagram y página); herramienta 3D "El lote" → sanskule; esta app → arqivo.
- Textos de Guggenheim y Flatiron corregidos contra Wikipedia. Media estrella en los promedios.
- Nombre visible cambiado a arqivo; Instagram @_arqivo.
- Símbolos nuevos: Art déco (`deco.py`, estación Texas & Pacific) e Italianizante (`erba.py`, Villa Erba), con dos rondas de correcciones; quedan pendientes las cúpulas y dos detalles del déco y el óculo de la Erba. Fondos provisorios.
- `comparar.js`: tandas con `?solo=a,b`, en grande.
- Contexto de sanskule guardado en `~/sanskule?/contexto/`.
- `sw.js` en `v72`. Nada commiteado.
- Noche: correcciones del art déco copiando la postal y la foto: linternas (tambor octogonal recto casi del ancho de la torre, ranuras de a pares, cornisita, alero y techo en zigurat bajo; antes cúpula dorada, "de otro estilo"), pináculos bajos y macizos, torre en ladrillo ocre con la tira de ventanitas entre marcos claros que rematan en cascada y el panel alto arriba, pie de torre (`pie_torre`: ventana alta en el eje, líneas claras, paneles oscuros con zigzag; sin marquesina), base con pilastras claras, ventanales de cuadrícula en dos tramos, friso de relieves y marquesina verde en la entrada, pretil con friso de celosía, pilares que terminan en punta, ventanas de arriba con cabeza en punta y bloque escalonado con mástil y bandera de Estados Unidos. Erba: óculo centrado en el eje real de la torre (estaba en x=475 y el eje es 471), dibujado como círculo fila por fila. La foto de la T&P se sumó a `comparar.js`. `sw.js` en `v73`. Nada commiteado.
- Después: bandera del déco del lado derecho del mástil. **Villa Erba rehecha en unidades** (`erba.py`: ayudas `sim`, `eje`, `arco`, `vano`, `frontis_segmento`, `frontis_cartela`, `balaustrada_u`, `mensulas_u`, `estatua`, `maceta`): cada cuerpo simétrico sobre su eje, ventanas parejas con frontis curvo, portón y logia con arcos de medio punto y clave, puertas con frontis partido y cartela, paneles con medallón; terraza con estatuas y macetas, escalinata escalón por escalón con farol, bojes parejos y cerco, muro de sillares con escalera al agua, reflejo y palos de amarre. Las notas adhesivas (Stickies) que vio el usuario en la pantalla no las abrió Claude. Art déco aprobado. Erba: remate distinto en pabellones y cuerpo del medio.

### 14 de noviembre de 2026

- Fondos de Art déco e Italianizante elegidos en `fondos.html` y aplicados (también en `deco.py` y `erba.py`).
- **Renacimiento francés = Alwyn Court** (`alwyn.py`): la esquina de frente y simétrica; para que se lea la esquina, los tramos se angostan al alejarse, ventanas de la torre más angostas a los lados y el lado derecho en sombra suave (colores `-m` en la mitad de la torre, `-s` después, generados con `oscurecer()`); cornisa que vuela con perfil curvo (`MARGEN`, `perfil`), cartelas coronadas, rombos de tres anillos, columnitas, antepechos con medalla y rosetas, cabezales con salamandras, balconcitos y balcón curvo tallado, friso, balaustradas por tramo con dados sobre los pilares, planta baja con toldos, marquesina, faroles y macetas, vereda plana, árboles y semáforo. `espejo()` copia el lado izquierdo al derecho fuera de la torre. Tonos de piedra cercanos entre sí ("que no sea brusco").
- **Gótico = catedral de Colonia** (`colonia.py`, 110 × 248): dos torres de cinco niveles, ventanales con doble moldura, vitrales en rombitos (simétricos en cada ventana), lancetas con arquito y cuadrifolio; gabletes con doble moldura, crochets y rosetón solo en el hueco libre (`libre`); tracería ciega en relieve, contrafuertes con nichos y estatuas, pináculos con crochets, bosque de pináculos (`fialas`), galerías caladas, aguja calada (se ve el fondo), portadas con arquivoltas de estatuas, tímpano en registros, puertas con tachas; faroles de globo. Ojo: `R()` espeja respecto del eje de la fachada, no de cada ventana.
- Regla nueva: símbolos con mucho detalle desde la primera versión (`CLAUDE.md`, paso "Dibujar"; memoria `medianeras-simbolos-detalle-alto`).
- `comparar.js` suma los dos. `sw.js` en `v74`. Nada commiteado.
- **Mediodía (`v75`, subido):** prioridades nuevas: arqivo (pulir bases), después sanskule, jagten al final. **Fuentes en la ficha:** campo `fuentes` en `obras.json` (`[{nombre, url?}]`, 28 obras), fila "Fuentes" al final de la pestaña Datos (`panelDatos` en `obra.js`, `.ficha-fuentes`). **Textos revisados contra Wikipedia** (17 de afuera) y corregidos: Oculus (la claraboya sí se abre cada 11/9, 102 minutos), Catedral de Manchester (Crowther: piedra 1850–1870, murió en 1893 sin terminar; no los pórticos), 50 Newton Street (depósito sobre una fábrica de sombreros quemada en 1906; no Joseph Wood), Flatiron (conversión terminada en 2026), St Luke (sin Insall). Tribeca Synagogue (sitio oficial, Wikipedia, thisispaper: expropiación federal; "llama" es metáfora; sin "la que Breger más defendió") y The Peregrine (CityRealty: mitad de cuadra entre 49 y 50, balcones desde el piso 11; lo de las fotos marcado "a la vista"). Programas: Flatiron "Oficinas (hoy viviendas)", 50 Newton "Depósito (hoy hostel)".
- **Símbolos nuevos:** **Tudor = casa natal de Shakespeare desde el jardín** (`tudor.py`): hastial simétrico con escalones parejos, oriel emplomado, alas largas con techo a cuatro aguas empinado, chimenea saliendo de la cumbrera, malvas rosas. **Barroco eduardiano = Lancaster House, Manchester** (`lancaster.py`): esquina de frente como Alwyn, torre con cúpula, linterna, volutas y balcón, fachadas de ladrillo con fajas (colores parejos, poco contraste, `oscurecer` 0.93), planta baja detallada, torreones con sillares. Los dos en `comparar.js`.
- Capturas en claro: `--blink-settings=preferredColorScheme=1` en Chrome headless (Chrome de esta Mac está en oscuro).

