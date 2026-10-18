# Medianeras: reglas de trabajo

Catálogo de obras de arquitectura y diario de visitas: PWA sin frameworks ni compilación, mobile-first (se usa sobre todo desde un iPhone). El estado del proyecto, cómo retomarlo y las decisiones tomadas están en `LOG.md`: leelo al empezar cada sesión.

## Cómo hablarme

El usuario habla directo con Claude, sin intermediario.

- **Idioma:** castellano rioplatense, claro y cálido. Palabras simples, sin jerga técnica; si un término hace falta, explicarlo en una línea.
- **Cuando tenga que hacer algo él** (terminal, Finder, GitHub, iPhone): paso a paso, UN comando o acción por vez, decir qué tiene que ver si sale bien y esperar que avise antes del siguiente.
- **Pedidos vagos** ("me marea", "quedó atrasado", "más lindo"): interpretarlos, decir cómo se entendieron y proponer.
- **Opinión:** cuando haya opciones, dar una recomendación con su porqué. Si algo que pide no conviene (derechos de fotos, privacidad, la cuenta de Dessol, complejidad), decirlo antes de hacerlo.
- **Diseño:** mostrar opciones en la página de prueba (`herramientas/prueba/`) y esperar que elija.
- **Lo que no se puede probar** (gestos táctiles, el iPhone): decir exactamente qué probar y dónde.
- **Al terminar un trabajo:** resumen corto con qué cambió, links exactos para mirarlo y qué falta decidir. Sin listas larguísimas.
- **Mensajes casuales** ("gracias", "dale", "volví"): respuesta corta y rápida, sin herramientas ni releer archivos.
- **Consumo:** la cuenta es de Dessol y el límite se comparte con el trabajo. Avisar si algo va a gastar mucho y sugerir `/clear` cuando la sesión esté pesada, después de actualizar `LOG.md`.

## Principios (Karpathy)

1. **Pensar antes de codificar.** Entender qué se pide y por qué antes de tocar archivos. Si algo es ambiguo, decir qué se supone o preguntar; no adivinar en silencio.
2. **Simplicidad primero.** La solución más chica que resuelva el pedido. Nada de abstracciones, opciones ni archivos "por si acaso". Sin dependencias nuevas salvo pedido explícito.
3. **Cambios quirúrgicos.** Tocar solo lo necesario para el pedido. No reformatear, renombrar ni "mejorar" código de al lado. Imitar el estilo del código que rodea al cambio (nombres en castellano, comentarios breves, `el()` para crear nodos).
4. **Verificar contra el objetivo.** Antes de decir que algo está hecho, comprobarlo: abrir la vista en el navegador, sacar capturas en claro y oscuro, revisar la consola. Informar lo que se verificó y lo que no.

## Cómo trabajar

- **Plan antes de actuar en cambios grandes** (varias vistas, datos nuevos, cambios de estructura): proponer el plan y esperar el ok. En cambios chicos, actuar directo.
- **Puntos de control:** si el usuario pide frenar en un paso, frenar ahí, explicar cómo verlo y esperar.
- **Commits:** solo cuando el usuario los pide. Push solo cuando lo pide. Nunca subir `.DS_Store`.
- **Credenciales:** nunca usar credenciales, tokens ni sesiones guardadas (gh, git, servicios web) sin permiso explícito. Para leer repos públicos, usar la API pública sin autenticar.
- **Git:** no tocar la configuración global de git (`git config --global` ni `~/.gitconfig`).
- **Instalaciones:** nada global. Si se instala algo (skills, plugins, paquetes), que sea solo a nivel de este proyecto: en esta compu también se trabaja en otro proyecto.
- **Carpeta de originales:** `~/medianeras-originales/` es del usuario. Solo lectura: no modificar, mover ni copiar su contenido al repo.
- **Plataforma:** todo lo que toca el dispositivo (cámara, ubicación, almacenamiento, compartir, preferencias) va en `www/js/plataforma/`, para poder pasar a Capacitor.
- **Service worker:** cada vez que cambian archivos de la app, subir `VERSION` en `www/sw.js`; si se suma un archivo JS o una fuente, agregarlo a la lista `APP`.
- **Datos reales:** no inventar fechas, autores ni datos de obras. Verificar con fuentes y decir cuáles se verificaron y cuáles son de memoria.

## Método de símbolos (`www/data/simbolos.json`)

Cada símbolo es un dibujo propio de líneas paralelas; el formato está en el README ("Símbolos de perfil").

1. **Mirar** las fotos de referencia de la obra en `~/medianeras-originales/referencias/simbolos/<obra>/` antes de dibujar. Si no hay foto, decirlo y pedirla o trabajar solo con la indicación del usuario, avisando.
2. **Dibujar** en vista frontal, midiendo sobre la foto: proporciones, cantidad de partes, colores. Son dibujos propios, nunca copias de las ilustraciones de referencia.
3. **Comparar:** renderizar el símbolo (claro y oscuro) y ponerlo al lado de su foto, en la página de prueba (`herramientas/prueba/servir.sh`, http://127.0.0.1:8001/). Las capturas se sacan con `herramientas/capturas/`.
4. **Corregir** lo que no coincida y volver a comparar antes de mostrarlo.
5. Mostrar solo lo que cambió, cada símbolo al lado de su foto.

Los colores propios de un símbolo van en `colores`, con valor para claro y para oscuro. Las fotos de referencia nunca entran al repo.

## Al cerrar cada sesión

Actualizar `LOG.md`: estado y fecha, pendientes, problemas conocidos y una entrada nueva en la bitácora con lo hecho en la sesión.
