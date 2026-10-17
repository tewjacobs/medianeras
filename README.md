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
    │   ├── exportar.js           arma el ZIP con las visitas del teléfono
    │   ├── vistas/               una por sección (inicio, mapa, obra, diario, listas, nueva-visita)
    │   ├── plataforma/           todo lo que toca el dispositivo (ver Capacitor)
    │   └── lib/zip.js            generador de ZIP sin dependencias
    ├── vendor/leaflet/           Leaflet 1.9.4 (copia local, sin CDN)
    ├── iconos/
    ├── data/                     obras.json, diario.json, listas.json
    └── img/
        ├── obras/<id-de-obra>/   fotos del catálogo
        └── diario/<id-de-visita>/ fotos propias de las visitas
```

Rutas de la app: `#/` (obras), `#/mapa`, `#/obra/<id>`, `#/diario`, `#/listas`, `#/lista/<id>`, `#/nueva`.
Los filtros quedan en la dirección (por ejemplo `#/?pais=Argentina&decada=1950`), así que se pueden guardar o compartir.

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
| `ejemplo` | `true` muestra el cartel EJEMPLO. No lo pongas en obras reales | no |

Los filtros (década, estilo, material, arquitecto, programa, país → provincia → partido/ciudad → barrio) se arman solos con lo que haya en los datos: no hay que tocar código para sumar un país o un barrio nuevo.

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
