# 20 — Variantes técnicas

Cargar cuando: el repo tiene un patrón dominante distinto del default del estándar.

## Clasificación

Tras Fase 0, si hay patrón dominante distinto del default, documentarlo en el reporte y **seguir la variante** en Implementar (no pelear).

## Variante reconocida — store de UI + fetchers por scope

| Tema | Default del estándar | Variante |
|------|----------------------|----------|
| Overlays | useState + montaje condicional | `createEntityDrawerStore` / Zustand |
| Service | `extends SharedService` | Clase static + fetcher por scope |
| Fetchers | un `apiFetcher` | fetchers central / tenant / Sanctum por scope |
| Folders | `components/`, `hooks/`, … | + `pages/`, `stores/` |
| Tenancy | N/A | Central/Tenant (`16`) |

Siguen aplicando: display cadena de `if` (`08`; `useMemo` según `23` A–E), no `handle*`, diálogo dueño de mutación (options en caller), query-keys central (o híbrido documentado), enums/`07` ownership, i18n flat, Controllers→Actions→Resources.

## Otras variantes / opcionales

- **App profile / feature flags por marca o producto:** si el repo ya tiene config de perfil (features on/off, rutas bloqueadas), **respetarla** al implementar o auditar; no exigir profile en todo proyecto.
- **Realtime (Echo / Reverb / Pusher):** opcional. Detectar en Fase 0; si hay env/keys de realtime sin cliente, o necesidad de WS sin stack → PROP (`19`), no instalar por defecto.
- **MRT localization:** solo si el repo usa Material React Table (`11`).

## Regla

En **Implementar** sobre variante reconocida: extender el patrón local.  
En **Auditar** hacia el molde canónico: reportar divergencias; migrar solo si el usuario aprueba lotes (puede incluir migrar drawers useState↔Zustand conscientemente).
