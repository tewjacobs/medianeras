# Medianeras

Un Letterboxd de arquitectura: catálogo de obras + diario personal de visitas + listas temáticas.

Es una app web estática (HTML, CSS y JavaScript sin frameworks ni compilación), pensada para usarse desde el iPhone e instalarse en la pantalla de inicio. Funciona sin conexión para lo que ya se vio, y permite registrar visitas desde el teléfono.

> Las 3 obras, las entradas del diario y la lista que vienen cargadas son **de ejemplo** (ficticias, marcadas con `"ejemplo": true` y la palabra EJEMPLO). Borralas cuando cargues las tuyas.

## Contenido

- [Estructura](#estructura)
- [Ver el sitio en la compu](#ver-el-sitio-en-la-compu)
- [Publicar en GitHub Pages](#publicar-en-github-pages)
- [Usarlo en el iPhone](#usarlo-en-el-iphone)
- [Cargar una obra nueva](#cargar-una-obra-nueva)
- [Diario y listas](#diario-y-listas)
- [Sumar al repo las visitas cargadas desde el teléfono](#sumar-al-repo-las-visitas-cargadas-desde-el-teléfono)
- [Actualizar la app (service worker)](#actualizar-la-app-service-worker)
- [Camino a app nativa (Capacitor)](#camino-a-app-nativa-capacitor)

## Estructura

```
medianeras/
├── README.md
├── .github/workflows/pages.yml   publica www/ en GitHub Pages
└── www/                          ← todo el sitio
    ├── index.html                única página; las secciones son rutas #/…
    ├── manifest.webmanifest      datos para instalarla como app
    ├── sw.js                     service worker (funcionamiento sin conexión)
    ├── css/estilos.css
    ├── js/
    │   ├── app.js                router, pestañas, registro del service worker
    │   ├── datos.js              carga de los JSON y funciones de formato
    │   ├── filtros.js            filtros generados desde los datos
    │   ├── ui.js                 piezas de interfaz compartidas
    │   ├── grafica.js            logo, símbolos de perfil y patrones de líneas (SVG)
    │   ├── tema.js               claro / oscuro / automático
    │   ├── exportar.js           arma el ZIP con las visitas del teléfono
    │   ├── filas.js              las filas del inicio (de dónde salen sus obras y adónde lleva VER MÁS)
    │   ├── vistas/               una por sección (inicio, obras, perfil, mapa, obra, diario, listas, nueva-visita)
    │   ├── plataforma/           todo lo que toca el dispositivo (ver Capacitor)
    │   └── lib/zip.js            generador de ZIP sin dependencias
    ├── vendor/leaflet/           Leaflet 1.9.4 (copia local, sin CDN)
    ├── fuentes/                  Archivo, IBM Plex Mono y Libre Caslon Text (woff2 + licencias OFL)
    ├── iconos/
    ├── data/                     obras.json, diario.json, listas.json, perfiles.json, simbolos.json
    └── img/
        ├── obras/<id-de-obra>/   fotos del catálogo
        └── diario/<id-de-visita>/ fotos propias de las visitas
```

Rutas de la app:

| Ruta | Qué es |
|---|---|
| `#/` | inicio: filas temáticas (visitadas, agregadas, mejor puntuadas, de un arquitecto/a, por década) |
| `#/obras` | todas las obras, con buscador, filtros y orden |
| `#/arquitecto/<slug>`, `#/estilo/…`, `#/material/…`, `#/programa/…`, `#/estado/…`, `#/pais/…`, `#/provincia/…`, `#/ciudad/…`, `#/barrio/…`, `#/decada/1950`, `#/anio/1959` | perfil: símbolo, datos, descripción, resumen y sus obras |
| `#/arquitectos`, `#/estilos`, `#/materiales`, `#/programas`, `#/paises`, `#/decadas`, `#/anios`… | índice de cada tipo (los estilos, como árbol) |
| `#/obra/<id>`, `#/mapa`, `#/diario`, `#/listas`, `#/lista/<id>`, `#/nueva` | ficha, mapa, diario, listas y nueva visita |

El slug es el nombre en minúsculas, sin tildes y con guiones: "Frank Lloyd Wright" → `frank-lloyd-wright`.
Los filtros y el orden quedan en la dirección (por ejemplo `#/obras?pais=Argentina&decada=1950&orden=anio`), así que se pueden guardar o compartir. Los links viejos con filtros en el inicio (`#/?pais=Argentina`) llevan solos a `#/obras`.

## Ver el sitio en la compu

Hace falta un servidor local porque el navegador no deja leer los JSON abriendo `index.html` con doble clic. Con Python (viene en macOS):

```sh
cd www
python3 -m http.server 8000
```

Abrí <http://localhost:8000>. Para cortar el servidor: `Ctrl + C`.

Para verlo como en el celular: en Chrome o Safari abrí las herramientas de desarrollo y activá la vista de dispositivo (iPhone).

## Publicar en GitHub Pages

1. Subí el repo a GitHub.
2. En el repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Cada `git push` a `main` publica la carpeta `www/` (el workflow está en `.github/workflows/pages.yml`). La dirección queda como `https://<usuario>.github.io/<repo>/`.

## Usarlo en el iPhone

La ubicación ("Cerca mío") y el modo sin conexión necesitan `https`, así que en el teléfono usá la versión publicada en GitHub Pages:

1. Abrí la dirección en **Safari**.
2. Tocá **Compartir → Agregar a inicio**.
3. Abrila desde el ícono: se ve a pantalla completa, como una app.

Las secciones y fotos que ya abriste quedan disponibles sin conexión. Del mapa se guardan solo los mosaicos que ya viste (hasta unos 500), respetando la política de uso de OpenStreetMap.

### Checklist de prueba en el iPhone

- [ ] Se instala con "Agregar a inicio" y abre sin barra de Safari, con el ícono correcto.
- [ ] La barra de pestañas no queda tapada por la barra de inicio del iPhone.
- [ ] Filtros: país → provincia → partido → barrio se van habilitando en cascada.
- [ ] Mapa: arranca en zona norte; "Cerca mío" pide permiso y muestra las obras cercanas.
- [ ] Nueva visita: sacar una foto con la cámara y elegir otra de la fototeca.
- [ ] La visita aparece en el Diario y en la ficha con "Solo en este teléfono".
- [ ] Exportar → Compartir → Guardar en Archivos: el ZIP abre y tiene `diario-nuevas.json` y las fotos.
- [ ] En modo avión, la app abre y muestra lo ya visto.

## Cargar una obra nueva

Todo se hace editando `www/data/obras.json`.

1. **Elegí un id** (slug): minúsculas, sin tildes ni espacios, con guiones. Ej.: `casa-curutchet`. Tiene que ser único y no cambiarlo después (lo usan el diario y las listas).
2. **Fotos**: creá la carpeta `www/img/obras/<id>/` y poné ahí las fotos (`1.jpg`, `2.jpg`…). Conviene achicarlas a ~1600 px de lado.
   - Si son de [Wikimedia Commons](https://commons.wikimedia.org), en la página de la foto está el autor y la licencia (CC BY-SA 4.0, CC0, etc.). Poné el link a esa página en `fuente`.
   - Si son tuyas: `"autor": "<tu nombre>"` y la licencia que quieras darles.
3. **Coordenadas**: en [openstreetmap.org](https://www.openstreetmap.org) hacé clic derecho sobre el edificio → **Mostrar dirección**; a la izquierda aparecen latitud y longitud. (En Google Maps: clic derecho → el primer renglón son las coordenadas.)
4. **Agregá el objeto** al array de `obras.json` (cuidado con las comas entre obras):

```json
{
  "id": "nombre-de-la-obra",
  "nombre": "Nombre de la obra",
  "otros_nombres": [],
  "arquitectos": ["Nombre Apellido", "Nombre Apellido"],
  "anio_proyecto": 1950,
  "anio_finalizacion": 1955,
  "estilo": "Estilo",
  "materiales": ["Material 1", "Material 2"],
  "programa": "Uso",
  "estado": "existente",
  "ubicacion": {
    "pais": "Argentina",
    "provincia": "Ciudad Autónoma de Buenos Aires",
    "ciudad": "Buenos Aires",
    "barrio": "Barrio",
    "direccion": "Calle y número",
    "lat": -34.5,
    "lng": -58.4
  },
  "descripcion": "Texto breve.",
  "fotos": [
    {
      "archivo": "img/obras/nombre-de-la-obra/1.jpg",
      "autor": "Autor de la foto",
      "licencia": "CC BY-SA 4.0",
      "fuente": "https://commons.wikimedia.org/wiki/File:..."
    }
  ]
}
```

(Es una plantilla: reemplazá cada valor por datos verificados de la obra.)

5. **Validá el JSON** antes de subir (si hay un error, avisa la línea):

```sh
python3 -m json.tool www/data/obras.json > /dev/null && echo "JSON OK"
```

6. Recargá el sitio local y revisá la ficha. Si un `obra_id` del diario o de las listas no existe, aparece un aviso en la consola del navegador.

### Detalle de los campos

| Campo | Qué va | Obligatorio |
|---|---|---|
| `id` | slug único | sí |
| `nombre` | nombre principal | sí |
| `otros_nombres` | lista de nombres alternativos | no (`[]`) |
| `arquitectos` | lista; se usan tal cual para el filtro, así que escribí cada nombre siempre igual | no |
| `anio_proyecto`, `anio_finalizacion` | números o `null`. La década sale de la finalización (o del proyecto si no hay) | no |
| `estilo`, `programa` | texto; el filtro agrupa por texto exacto | no |
| `materiales` | lista | no |
| `estado` | `existente`, `demolida` o `modificada` | sí |
| `ubicacion.pais` … `barrio` | niveles genéricos: `provincia` = provincia / estado / región; `ciudad` = partido / ciudad / municipio; `barrio` = barrio / localidad. Sirve para cualquier país | no, pero sin país no entra en el filtro de ubicación |
| `ubicacion.lat`, `lng` | números decimales; sin ellos la obra no aparece en el mapa | no |
| `fotos` | lista; la primera es la portada | no (`[]`) |
| `resumen` | una o dos líneas, debajo de los botones de la ficha. Con "Ver más" se reemplaza por `descripcion` | no |
| `planos` | lista de planos (planta, corte, vista) con los mismos campos que `fotos` (`archivo`, `autor`, `licencia`, `fuente`), más `tipo` ("Planta", "Corte"…) y `pie`. Si no hay, la pestaña PLANOS no aparece | no |
| `fotos[].encuadre` | cómo se ve la portada en la tapa cuadrada. Sin encuadre, la foto entra entera y el color del marco llena lo que sobra. Con `"centro"`, `"arriba"`, `"abajo"`, `"izquierda"`, `"derecha"` o una posición como `"50% 30%"`, se recorta al cuadrado mostrando esa parte. En la ficha, las fotos siempre se ven enteras | no |
| `ejemplo` | `true` muestra el cartel EJEMPLO. No lo pongas en obras reales | no |
| `agregada` | fecha `AAAA-MM-DD` en que se sumó al catálogo, para "Agregadas recientemente". Si falta, vale el orden del archivo (la última es la más nueva) | no |
| `color` | fuerza el color del marco: `petroleo`, `follaje`, `cielo` o `mar` (si no, sale del estilo; ver Perfiles) | no |

Los filtros (década, año, estilo, material, arquitecto, programa, estado, país → provincia → partido/ciudad → barrio) se arman solos con lo que haya en los datos: no hay que tocar código para sumar un país o un barrio nuevo.

## Perfiles (`data/perfiles.json`)

Cada arquitecto, estilo, material, lugar, década o año tiene su página, armada con las obras. `data/perfiles.json` es optativo y suma lo que las obras no dicen: si falta o está vacío, todo funciona igual. Las claves son el nombre exacto tal como aparece en `obras.json`:

```json
{
  "arquitectos": {
    "Frank Lloyd Wright": { "nacimiento": 1867, "muerte": 1959, "pais": "Estados Unidos", "descripcion": "…" }
  },
  "estilos": {
    "Moderno": { "color": "petroleo", "descripcion": "…" },
    "Arquitectura orgánica": { "padre": "Moderno", "color": "follaje", "descripcion": "…" },
    "Racionalismo (ejemplo)": { "padre": "Moderno" }
  },
  "materiales": {}, "programas": {}, "paises": {}, "decadas": {}, "anios": {}
}
```

- **Arquitectos**: `nacimiento`, `muerte`, `fundacion` (para estudios), `pais` y `descripcion`. Se muestra lo que haya.
- **Jerarquía de estilos**: `padre` arma el árbol (`ESTILOS › Moderno › Racionalismo`). Un estilo puede existir solo acá, sin obras propias, como "Moderno": su página muestra las obras de todos sus descendientes, y filtrar por él también. Si un `padre` no existe o hay un ciclo, la consola lo avisa.
- **Color del marco**: el `color` de un estilo lo heredan sus descendientes que no tengan uno propio, así una familia comparte color. Sin color, se calcula uno estable desde el nombre del estilo raíz.
- **Descripción**: cualquier perfil puede tener `descripcion`. Si no tiene, la página se arma solo con las obras.

## Símbolos de perfil (`data/simbolos.json`)

Cada perfil (país, arquitecto, estilo, material…) puede tener un **símbolo**: un dibujo de líneas paralelas donde lo que cuenta es el color de cada línea y el punto exacto donde cambia de color. No es código: es una "partitura" que se escribe a mano en `data/simbolos.json`.

El archivo tiene una sección `colores` y una sección por tipo de perfil (`paises`, `arquitectos`, `estilos`, `materiales`, `programas`, `decadas`…). La clave es el nombre exacto tal como aparece en `obras.json`. Las décadas van agrupadas por colección (`decadas.argentina`, `decadas.mundo`, y más adelante una por país) y la clave es el año con que empieza cada una (`"1950"`):

```json
{
  "colores": {
    "celeste": { "claro": "#6cb0e3", "oscuro": "#79b7e6" },
    "sol":     { "claro": "#f2b318", "oscuro": "#eaae2b" }
  },
  "paises": {
    "Argentina": {
      "nota": "Bandera: dos celestes, dos blancas con el sol en el centro, dos celestes.",
      "direccion": "horizontal",
      "placa": "noche",
      "escala": 0.55,
      "grosor": 1,
      "separacion": 0.8,
      "lineas": [
        "celeste 18",
        "celeste 18",
        "blanco 7, sol 4, blanco 7",
        "blanco 7, sol 4, blanco 7",
        "celeste 18",
        "celeste 18"
      ]
    }
  }
}
```

**Cada línea** es un texto con **tramos** `color largo`, separados por comas, que se dibujan en orden: de izquierda a derecha si la dirección es horizontal (y las líneas se apilan de arriba hacia abajo), o de arriba hacia abajo si es vertical (y las líneas van de izquierda a derecha).

| Escritura | Qué hace |
|---|---|
| `celeste 40` | un tramo celeste de largo 40 |
| `blanco 17, sol 6, blanco 17` | tres tramos seguidos: el sol queda en el centro |
| `- 4` | un tramo vacío de largo 4 (se ve el fondo) |
| `(fachada 1, vidrio 0.6) x12` | repite el grupo 12 veces |
| `… celeste 40 …` | los `…` (o `...`) estiran el primer o el último tramo hasta el borde de la banda |

Los largos son relativos: no son píxeles. El dibujo se escala entero para entrar en la banda, así que solo importa la proporción entre los largos, el `grosor` de cada línea y la `separacion` entre líneas.

**Opciones del símbolo** (todas optativas salvo `lineas`):

| Campo | Valores | Por defecto |
|---|---|---|
| `direccion` | `horizontal` o `vertical` | `horizontal` |
| `grosor` | ancho de cada línea, en las mismas unidades que los largos | `1` |
| `separacion` | espacio entre una línea y la siguiente | `1` |
| `alinear` | dónde arrancan las líneas más cortas: `inicio`, `centro` o `fin` | `inicio` |
| `fondo` | color del fondo de toda la banda | `papel` |
| `placa` | color de un rectángulo justo detrás del dibujo (las banderas lo usan para que se vea el blanco) | ninguna |
| `escala` | achica el dibujo dentro de la banda: `1` es lo más grande que entra, `0.55` algo más de la mitad | `1` |
| `alto` | alto de la banda en píxeles (los verticales suelen necesitar más) | `132` |
| `largo` | largo total fijo, para que varias partituras compartan escala | el de la línea más larga |
| `nota` | descripción en palabras de lo que representa (no se dibuja) | |
| `arcos` | líneas curvas paralelas para lo que no se puede dibujar recto, como el arco de un puente (ver abajo) | ninguno |
| `obra`, `lugar`, `anio` | solo en `decadas`: qué obra representa a la década, dónde está y su fecha | |

**Colores.** Se puede usar cualquiera de la paleta de la app, que cambia sola con el tema (`tinta`, `papel`, `papel-2`, `tenue`, `filete`, `rojo`, `petroleo`, `follaje`, `cielo`, `mar`), o uno propio definido en `colores`, con su valor para el tema claro y para el oscuro. Si se usa un color que no existe, la consola lo avisa y el tramo sale en el color del texto.

**Arcos.** Cada arco es `{ "color", "desde", "hasta", "base", "flecha", "lineas" }`, en las mismas unidades que los tramos: va de `desde` a `hasta`, apoya en la línea número `base` (contando desde 0) y sube `flecha`. Con `"lineas": 2` se dibujan dos arcos paralelos, uno dentro del otro. Ejemplo: la Casa sobre el Arroyo, en `decadas.argentina.1940`. Con `"relleno": true` el arco es una figura llena (la parte de arriba de un portal) que apoya en el borde de arriba de la línea `base`; ejemplo: el portal de la Recoleta, en `decadas.argentina.1980`.

**Sin símbolo.** Un perfil que no tiene símbolo muestra una sola línea fina en el color de su familia. Un estilo sin símbolo usa el de su ancestro más cercano que tenga; un programa como "Oficinas (en conversión a viviendas)", si no tiene uno propio, usa el de lo que está antes del paréntesis ("Oficinas"). La década de 2020 argentina, por ahora, no tiene símbolo y usa el neutro.

**Obras sin foto.** La tapa muestra el símbolo de su arquitecto/a o, si no tiene, el de su estilo; si tampoco, el neutro.

**Décadas y años.** Cada década tiene el símbolo de una obra característica de esa época, en dos colecciones: `argentina` (la que usa la app; por ejemplo, 1930 → Edificio Kavanagh) y `mundo` (por ejemplo, 1960 → Congreso Nacional de Brasilia). Los años no se cargan: usan el símbolo de su década y, debajo, diez marcas, una por año, con la de ese año en rojo.

**Materiales y programas** dibujan lo que representan: el aparejo del ladrillo, las tablas y tensores del hormigón visto, las vetas de la madera; una sala con cuadros para Museo, una torre de muro cortina para Oficinas.

**Tamaño.** Los estilos y las décadas van grandes; las banderas y las obras de arquitectos van más chicas (`escala` menor) y con poco entorno.

**Para pedir un símbolo nuevo** alcanza con describirlo en estos términos: cuántas líneas, en qué dirección y dónde cambia cada una de color. Por ejemplo: "Uruguay: nueve líneas horizontales, blancas y azules alternadas; en las cinco de arriba, a la izquierda, un sol amarillo que crece hasta la del medio y vuelve a achicarse".

## Diario y listas

**`www/data/diario.json`** — una entrada por visita (una obra puede tener varias):

```json
{
  "id": "2026-03-14-nombre-de-la-obra",
  "obra_id": "nombre-de-la-obra",
  "fecha": "2026-03-14",
  "nota": "Texto libre. Los saltos de línea se respetan (\n).",
  "puntaje": 4,
  "fotos": [{ "archivo": "img/diario/2026-03-14-nombre-de-la-obra/1.jpg", "pie": "Hall de entrada" }]
}
```

`puntaje` es de 1 a 5, o `null` para no puntuar.

**`www/data/listas.json`**:

```json
{
  "id": "nombre-de-la-lista",
  "titulo": "Título de la lista",
  "descripcion": "Para qué es la lista.",
  "obras": ["nombre-de-la-obra", "otra-obra"]
}
```

Las obras se muestran en el orden del array.

## Sumar al repo las visitas cargadas desde el teléfono

Las visitas que cargás con el botón **+** quedan guardadas **solo en ese teléfono** (en el almacenamiento de la app) hasta que las exportes.

1. En el teléfono: **Diario → Exportar visitas → Compartir** (o **Descargar**). Guardá el ZIP en Archivos / iCloud Drive, o mandátelo por AirDrop o mail.
2. En la compu, descomprimí el ZIP **dentro de `www/`**: las fotos quedan en `www/img/diario/<id>/`.
3. Abrí `diario-nuevas.json`, copiá las entradas y pegalas dentro del array de `www/data/diario.json`.
4. Borrá `diario-nuevas.json` y `LEEME.txt`, validá con `python3 -m json.tool www/data/diario.json`, y hacé commit y push.
5. Cuando el teléfono vea esas visitas publicadas, el Diario te ofrece **borrar las copias del teléfono**.

> **Importante:** Safari puede borrar los datos de sitios que no se usan por varias semanas. Instalada en la pantalla de inicio es más estable, pero exportá seguido para no perder nada.

Limitación actual: solo se pueden registrar visitas a obras que ya están en el catálogo.

## Actualizar la app (service worker)

El service worker guarda una copia de la app en el teléfono para que abra sin conexión. Cuando cambies HTML, CSS o JS:

1. Subí la versión en `www/sw.js` (`const VERSION = 'v2'`, `'v3'`…).
2. Si agregaste un archivo JS nuevo, sumalo a la lista `APP` en el mismo archivo.

Los cambios en `data/*.json` y en las fotos **no** necesitan cambiar la versión: los datos se piden a la red cada vez (y se usa la copia guardada si no hay conexión), y las fotos se actualizan solas en segundo plano.

Al detectar una versión nueva, la app muestra el aviso "Hay una versión nueva" con el botón **Actualizar**.

## Camino a app nativa (Capacitor)

El código está organizado para empaquetarlo con [Capacitor](https://capacitorjs.com) sin rehacerlo:

- `www/` es la carpeta que Capacitor usa por defecto (`webDir`).
- Todo es local (sin CDN) y con rutas relativas, y la navegación es por `#/…`, que funciona igual dentro de la app nativa.
- Lo que toca el dispositivo está aislado en `www/js/plataforma/`. Para la versión nativa se reemplaza el interior de esas funciones manteniendo sus nombres:

| Archivo | Hoy (web) | En Capacitor |
|---|---|---|
| `almacen.js` | IndexedDB | puede quedar igual, o pasar a `@capacitor/filesystem` |
| `ubicacion.js` | `navigator.geolocation` | `@capacitor/geolocation` |
| `fotos.js` | `<input type="file">` + achicado con canvas | `@capacitor/camera` (`pickImages` / `getPhoto`) |
| `compartir.js` | Web Share / descarga | `@capacitor/filesystem` + `@capacitor/share` |

- El service worker no se registra dentro de la app nativa (`app.js` lo detecta con `Capacitor.isNativePlatform()`).

Pasos aproximados cuando llegue el momento (requiere Node.js y Xcode): `npm init -y`, `npm install @capacitor/core @capacitor/cli @capacitor/ios`, `npx cap init Medianeras ar.medianeras.app --web-dir www`, `npx cap add ios`, `npx cap open ios`.

## Créditos

- Mapa: [Leaflet](https://leafletjs.com) (BSD-2) con mosaicos de [OpenStreetMap](https://www.openstreetmap.org/copyright) (© colaboradores de OpenStreetMap, ODbL).
- Las imágenes de ejemplo y los íconos son propios del proyecto (CC0).
