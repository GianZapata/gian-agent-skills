# 20 — Variantes técnicas

Cargar cuando: el repo tiene un patrón distinto del default y hay que decidir si es variante reconocida o legacy.

## Clasificación

El default del estándar es obligatorio. Solo lo reemplaza una variante de la lista de este archivo, con evidencia en el repo (`archivo:línea`). Incumplir el default sin variante es hallazgo Medio. La variante se documenta en el reporte y se extiende en Implementar.

Un patrón dominante que no está en la lista no es variante. Hay dos casos, y no se mezclan:

- **Adaptador.** Otra tecnología para la misma capacidad: Firestore en lugar de HTTP, realtime, o el cliente de datos del stack. Es adaptador solo si cambia la tecnología y hay evidencia de que la responsabilidad equivalente se cumple (fila de la matriz `24` §3 con `archivo:línea`). Sin esa evidencia, es legacy. Con evidencia, se documenta, se cumple la responsabilidad con el equivalente (`01`) y no se migra a la librería React.
- **Legacy.** Un patrón que rompe una regla de núcleo: `defineComponent` + `return`, funciones sueltas de área, mapas de metadata en paralelo, un `interface *Input` junto al schema. El código nuevo sigue el estándar. El viejo es hallazgo (`02`: legacy para migración). No se convierte en la regla.

## Variante reconocida — store de UI + fetchers por scope

| Tema | Default del estándar | Variante |
|------|----------------------|----------|
| Overlays | useState + montaje condicional | `createEntityDrawerStore` / Zustand |
| Service | `extends SharedService` | Clase static + fetcher por scope |
| Fetchers | un `apiFetcher` | fetchers central / tenant / Sanctum por scope |
| Folders | `components/`, `hooks/`, … | + `pages/`, `stores/` |
| Tenancy | N/A | Central/Tenant (`16`) |

Siguen aplicando: display (`08`), no `handle*`, diálogo dueño de mutación (options en caller), query-keys central (o híbrido documentado), enums/`07` ownership, i18n flat, Controllers→Actions→Resources.

## Adaptador reconocido — Vue

No es una variante que reemplace el estándar. Es el delta de vista (`25`). Detectar Vue en Fase 0, cargar el núcleo (`01`) y sumar `25`. No clasificar el repo como patrón desconocido ni migrarlo a React.

| Tema | Adaptador React | Vue (`25`) |
|------|-----------------|------------|
| Vista | TSX | `.vue` con script setup inline |
| Carpeta de estado de UI | `hooks/` | `composables/` |
| Server state | React Query | El cliente de datos que el repo ya usa |
| Store de overlays (variante) | Zustand | Pinia o provide/inject si ya existen (12) |

El núcleo no se sustituye: naming (`04`), helpers de área (`23`), enums (`07`), contratos, errores y display.

## Variantes condicionales: obligatorias cuando el repo las tiene

- **App profile / feature flags por marca o producto:** si el repo ya tiene config de perfil (features on/off, rutas bloqueadas), **respetarla** al implementar o auditar. No exigir profile en un proyecto que no lo tiene.
- **Realtime (Echo / Reverb / Pusher):** detectar en Fase 0. Si el repo lo tiene, se sigue. Si hay env/keys de realtime sin cliente, o necesidad de WS sin stack → PROP (`19`). No instalar sin OK.
- **MRT localization:** solo si el repo usa Material React Table (`11`).

## Regla

En **Implementar** sobre variante reconocida: extender el patrón local.  
En **Auditar** hacia el molde canónico: reportar divergencias; migrar solo si el usuario aprueba lotes (puede incluir migrar drawers useState↔Zustand conscientemente).
