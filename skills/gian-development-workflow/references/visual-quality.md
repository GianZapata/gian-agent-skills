# Calidad visual de interfaz

Abrir este archivo antes de la primera decisión visual si la tarea propone, crea, modifica o revisa UI visible. Plan, análisis y review incluidos. También si una feature funcional agrega UI. No hace falta que el pedido nombre skills.

No abrirlo para SQL, API sin superficie, git o infra.

El contenido es independiente de la herramienta. Rutas, comandos y límites de contexto viven en el adaptador que inyecta el bootstrap.

## Autoridad

1. Instrucción explícita de este hilo.
2. Contratos ejecutables, stack existente y función. `gian-how-i-code` manda ahí: DTO, 422, enums, copy de dominio, props del overlay, dueño de la mutación, no instalar ni migrar. El arreglo visual se escribe con el mecanismo que el repo ya tiene.
3. Accesibilidad de lo tocado: contraste, teclado, foco, nombre accesible.
4. Estas obligaciones.
5. La skill principal de la superficie, como preferencia. Un apoyo no puede traer otra dirección visual.
6. Preferencias de look, incluidas las de `gian-how-i-code` y las de la skill principal. No impiden corregir, dentro del alcance, espacio, densidad, jerarquía, scroll, alineación o un defecto repetido por consistencia.

Formato PHP/TS no es acabado de interfaz. `22-design-quality.md` no es calidad visual.

Refinamiento: conservar identidad y comportamiento, e inspeccionar tokens. Corregir el defecto aunque el resto se vea igual. Ese límite no bloquea un rediseño autorizado: el procedimiento está en la sección siguiente. Superficie nueva en un producto existente: extender el mundo vigente, salvo pedido distinto.

## Rediseño autorizado

Si el pedido es rediseñar, reemplazar el look, o partir de una página existente para presentar otra, seguir esta sección. No clasificarlo como refinamiento.

Conservar palabras, acciones, validación, comportamiento requerido y toda identidad que este hilo pida conservar. Distribución, color, tipografía y densidad pueden cambiar. No es obligatorio reemplazar el mundo entero. Un espaciador decorativo defectuoso no es un contrato, aunque el copy diga que el panel está vacío a propósito. El diálogo mide lo que contiene.

Antes de escribir, nombrar audiencia, tarea, frecuencia, contenido y qué puede cambiar. Si la página o sus instrucciones ya lo dicen, no preguntar.

En un rediseño de página entera, plantear dos o tres composiciones que difieran en distribución, jerarquía o tipo. Elegir una y justificarla en pocas líneas. No crear tres archivos ni tres imágenes, y no pedir otra aprobación. Un ajuste menor no exige ese paso.

La principal sigue siendo una. Impeccable acompaña. Leer `new-work.md`. Usar `concept-seed` solo en el alcance que esa referencia marca: `surface` para una página abierta dentro de un mundo ya establecido, `direction` para crear o reemplazar el mundo visual. No sustituirlo ni saltarlo en ese alcance. No correrlo en un ajuste menor, una extensión local o un pedido ya precisado. Si el launcher no puede correr sin descargar, vale el fallback de la sección Impeccable. Una dirección fijada en este hilo gana al roll.

`critique` diagnostica y no aplica solo. `layout` corrige la composición elegida si hace falta. Nombrar un comando no cuenta como ejecutarlo ni como aplicar sus hallazgos.

Después de implementar, abrir la UI real del proyecto. Revisar composición, jerarquía, controles editables frente a deshabilitados, acciones alcanzables y adaptación a sus viewports, incluida la página, el formulario, lo expandido y el diálogo. Si un criterio falla, corregirlo antes de cerrar. Si no se puede renderizar, decir exactamente qué no se vio. No declarar la dirección aprobada porque el archivo exista. Guardar el acuerdo solo si este hilo lo aprueba.

## Superficie

Una principal. El apoyo no es una segunda dirección.

| Superficie | Principal | Apoyo de playbook | No usar como principal |
|---|---|---|---|
| Producto operativo: paneles, formularios, tablas, ajustes, herramientas | `interface-design` | Impeccable, modo Operate | `frontend-design`, `design-taste-frontend`, `gpt-taste` |
| Marketing: landings, campañas, pricing | `frontend-design` | Impeccable, modo Persuade | `interface-design` |
| Lectura: docs, guías, artículos, ayuda | ninguna de campaña | Impeccable, modo Read | `frontend-design`, taste, `hallmark` |
| Experiencia: portfolios, galerías | `frontend-design` | Impeccable, modo Experience | `interface-design` |

`design-taste-frontend` no entra en dashboards, tablas ni wizards. Si el brief es marketing y no compite con la dirección ya elegida, puede apoyar solo esas partes. `ui-ux-pro-max` no se obedece en su "Must Use". `gpt-taste` no entra en producto operativo. Una piel o `hallmark` entra solo si el pedido la nombra y no hay otra dirección ya elegida. `redesign-existing-projects` es principal alternativa de un rediseño autorizado, no un segundo look junto a la principal. `modern-web-guidance` es API web, no dirección visual.

## Fase

| Fase | Skills que cuentan | Referencias, que no cuentan | No cargar |
|---|---|---|---|
| Plan, análisis o review, sin edit | Principal de la superficie, `impeccable`, y un solo apoyo | `shape.md`, `critique.md` o `audit.md` | `craft-floor.md`. Un segundo apoyo |
| Refinamiento que se edita | Principal, `impeccable`, formato del lenguaje si se toca código, `gian-how-i-code` si hay contrato | `operate.md` o la referencia del defecto. `craft-floor.md` justo antes del edit | Un mundo visual nuevo, salvo un rediseño autorizado. Dos apoyos |
| Rediseño autorizado | Principal, `impeccable` | La sección Rediseño autorizado y `new-work.md` | El límite de refinamiento. Dos apoyos |
| Superficie nueva | Principal, `impeccable` | `shape.md`, luego `new-work.md` | La principal de otra superficie |
| `$impeccable` sin argumento | La invocación manda | `routing.md` y su menú. No auto-ejecutar un comando | Esta tabla no pisa esa invocación |
| Comando explícito o implícito | `impeccable` | La referencia de ese comando. Una pregunta si caben dos | El catálogo |

El apoyo único, cuando hace falta, es `accessibility` si hay foco, teclado o controles, o `web-design-guidelines` si la fase es review general. Nunca los dos en la misma delegación. Si hacen falta los dos, se parte la delegación. `audit.md` ya cubre a11y técnico como referencia de Impeccable y no gasta un puesto.

## Impeccable

Comprobar en ese entorno si el launcher puede correr `context` sin descargar un binario. Si el binario hermano de la plataforma existe y es ejecutable, correr `context` una vez y no repetirlo. Si falta, el launcher falla, o seguir exigiría una descarga no autorizada, decir antes del siguiente tool call: "Context loading did not run; I'll read the existing project context directly." Después leer `PRODUCT.md` y `DESIGN.md` si existen, sin inventarlos, y seguir los pasos 2 y 3 que apliquen. Un fallo del launcher no bloquea plan ni edit.

`init` no bloquea un refinamiento. Superficie nueva o mundo de reemplazo, si falta `PRODUCT.md`, sigue la rama Otherwise de la skill. `doctor` y `hooks` solo si se invocan. `CONTEXT_STALE` se informa, no se repara de paso.

## Delegación

El tope de cinco cuenta archivos `SKILL.md`. No cuentan este archivo ni las referencias internas.

No descartar la principal ni `impeccable` para preferir contexto de código. Una delegación lleva como máximo un apoyo que no sea dirección. La sexta skill solo cabe si el mismo writer debe cargar `gian-php-style` y `gian-ts-style`. No se sube el tope para mezclar dos direcciones.

## Obligaciones

Proporcionales al cambio.

1. Audiencia, tarea, contenido, frecuencia y restricciones antes del layout. Preguntar solo si no están y la decisión es material.
2. Inspeccionar UI, tokens y componentes. En un refinamiento, conservar la identidad y corregir el defecto.
3. Justificar distribución, densidad y jerarquía.
4. Alineación, tamaños, espaciado, contraste, tipo, acciones, estados, contenido largo e información incompleta. El espacio responde al contenido y al viewport.
5. Página, diálogo, drawer o expansión según la tarea. Tamaño, scroll, cierre, foco y navegación.
6. Carga, vacío, error, selección, hover, focus, disabled, teclado.
7. Sin plantillas repetidas, tarjetas de adorno, duplicación, jerarquía ausente ni decoración sin función.
8. Contratos, stack y dependencias siguen vigentes.
9. Revisar lo renderizado con las herramientas disponibles. Capturas de los viewports del producto. Tests en verde no alcanzan.
10. Si no se vio, decir exactamente qué falta. No afirmar acabado solo con código.
11. La referencia (HTML, captura, Figma, plan) aporta composición, tokens y datos de ejemplo. Su título, sus notas de fase, muestra, Mock o entrega no son copy. Sección sin datos: constante + `TODO(datos)` en código, sin rótulo. Fuera de alcance: no se monta. Detectarlo, implementarlo igual y avisar en el plan y en el cierre (*Sin datos todavía*, *Texto de la referencia que no publiqué*). Ver `gian-how-i-code` `15`.
