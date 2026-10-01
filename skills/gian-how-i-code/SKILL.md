---
name: gian-how-i-code
description: "Estándar oficial de Gian para implementar, auditar, migrar y consultar features. El núcleo vale en cualquier stack. Usar para contratos API, forms, tables, dialogs, SFC Vue, enums y evaluación guiada de mejoras de stack."
license: Apache-2.0
metadata:
  author: gian
  version: "1.4.14"
---

# gian-how-i-code

Estándar oficial, autocontenido y ejecutable de cómo programa Gian. El núcleo vale en cualquier stack; Laravel, React y Vue son adaptadores documentados. Python, Node y Angular tienen filas en `01`. Funciona como manual humano y contrato de agente.

## Activation Contract

Usar en toda tarea de desarrollo que el workflow carga: crear, editar, alinear, auditar o migrar features; consultar el estándar; contratos API + molde; forms/tables/dialogs; SFC Vue; evaluar mejoras de stack. No queda opcional por no haber dicho “mi estilo”.

No usar como única skill para: explicación genérica de React/Vue/Angular/Laravel/Node sin aplicar el estándar; infra Docker/CI pura; CV/LinkedIn u otros dominios ajenos.

## Hard Rules

- Idioma de hallazgos, propuestas y reportes: **español**.
- No leer todas las `references/` por defecto; usar la matriz de routing.
- No migrar el repo entero en silencio; solo alcance aprobado.
- No instalar deps ni tocar lockfiles/manifests sin OK explícito.
- Auditoría no modifica código ni manifests.
- El conocimiento vive en esta skill; no depender de skills externas como autoridad, **excepto** formato visual PHP → `gian-php-style` y formato visual TS/TSX → `gian-ts-style`.
- El lenguaje no apaga el estándar. Núcleo (nombres, helpers, enums, contratos, errores, display) vale en cualquier stack. Un capítulo de stack solo documenta el adaptador. Ver `01`.
- Vue: `<script setup lang="ts">` inline en el `.vue`. Sin `src`. El script solo declara macros (`defineProps` / `defineEmits` / `defineModel`), imports y la llamada a `composables/useThing.ts`. Computed, handlers, `watch` y llamadas al service no se acumulan ahí. Sin `defineComponent`. `25` es el delta; no reemplaza el núcleo.
- Tests/contratos ejecutables del repo no se rompen para imponer estilo.
- Tests siguen al requisito, no al borrado (`17`). Si el requisito desaparece: borrar el código y sus tests exclusivos; no agregar un test de "ya no existe". Si sigue: conservar o adaptar sus tests. Si la eliminación crea una garantía vigente: probar esa garantía.
- String enum (TS) para conjuntos cerrados; PHP: backed Enum por default, o constantes `public const` en State Machine string-based (`asantibanez`) como fuente única — ver `07`. `Record<Enum, V>` en mappings FE exhaustivos. Membresía 2+: `.includes()` / `in_array(..., true)` / `in (A, B)` en Python, no `=== || ===` — ver `07`.
- Ownership **antes** de declarar `type`/union/enum/mapping: `APP_OWNED` \| `LIBRARY_OWNED` \| `EXTERNAL_GENERATED` \| `UNION LEGÍTIMA` — ver `07`.
- `APP_OWNED` cerrado y nombrado (incl. modos/estados de UI de feature) → string enum por default. `LIBRARY_OWNED` → tipo oficial de la lib; no shadow types.
- Memoización React según `23` (A–E): no ceremonial (A); STYLE_GIAN multi-rama (C) y MRT/`11` (E) sí.
- Styling (adaptador React, `04`/`23`): Tailwind-first cuando existe una utility o un token bridge real equivalente; `cn()` cuando las clases se componen o varían por estado/props runtime; sin constantes locales `*_SX` / `get*Sx`; `sx={(theme) => ({ … theme.palette })}` como escape hatch sin equivalencia limpia; `useTheme()` solo si el theme sale de `sx`. En otro stack, las clases se componen con el mecanismo del framework. No se exige `cn()`, MUI ni `sx`.
- Comentarios `ADAPTAR` solo en templates de `assets/`; eliminarlos al materializar código productivo. Template-only `ADAPTAR` MUST resolverse o quitarse al instanciar; MUST NOT sobrevivir en código de producto.
- Validación user-facing (núcleo): cada regla del borde tiene un mensaje de dominio, y el 422 llega por campo a la UI existente. Cobertura semántica regla→mensaje. En Laravel: FormRequest con `messages()` y, si hace falta, `attributes()`; no se da por terminado solo con `rules()`. En Python: el body model de Pydantic, con un handler de `RequestValidationError` que devuelve el mismo copy. En Node: el schema del handler — ver `01`/`05`/`10`/`14`.
- Display FE: metadata exhaustiva en una propiedad pública `static readonly Record<Enum, Meta>` de `<entity>.helper.ts`; getter de `label` con `i18n.t()` para resolver el locale al leer; `getXMeta(Enum | null | undefined)` como API preferida cuando el consumidor puede recibir ausencia, con `unknownMeta` y resolver privados. El acceso directo al Record queda para enums garantizados o iteración. No ampliar a `string`, usar casts ni fallbacks para ocultar drift. If-chain ad-hoc en el componente con `t()`. Prohibido `*.display.config.ts`, inyectar `TFunction`, `labelKey` diferido — ver `07`/`08`/`15`.
- Contrato de lectura (núcleo): el serializer no dispara queries; las relaciones se cargan antes, sin N+1. En Laravel: `new XResource($this->whenLoaded('rel'))` / `::collection($this->whenLoaded('rels'))`, sin callback `fn() => new X($this->rel)` salvo lógica extra — ver `06`. En Python: `response_model` o un serializer sobre datos ya cargados.
- Mutaciones: IDs de ruta nunca se mezclan con el DTO del body. 1 ID: `(id, data: TDto)`; 2+: `(params, data: TDto)`. El DTO sale de un schema nombrado; en TypeScript ese schema es Zod, en Python un body model de Pydantic. El envelope `*Variables` es del adaptador React Query o Vue Query (`13`). UI no arma FormData — ver `13`/`10`/`23`.
- Campo de formulario (`10`): al tocarlo, nombrar qué representa. La tabla de `10` es ejemplo, no el universo. Se aplica lo que no rechaza un valor que hoy pasa. Lo que puede rechazar datos guardados o cambiar el contrato se propone. El control sigue a la elección, no al gusto. Al crear o editar un campo, evaluar si una ayuda de captura ahorra trabajo, anticipa un problema o muestra la consecuencia. Evaluar es obligatorio. Implementar no: solo si el repo ya tiene lo que esa ayuda necesita, el alcance lo autoriza y no pisa un valor guardado ni una corrección manual. Si falta capacidad, proponer (`19`). No exigir a la vez catálogo, endpoint y debounce.
- Laravel (`05`): antes de crear un archivo, decidir el lugar. No agregarlo a `Support` porque la carpeta ya existe. Config, modelo, enum, helper de un eje ya cohesivo, método privado, fixture, o adaptador si la integración exige o consume la clase (config, factory, contenedor o `new`). No se crea una clase solo para agrupar variables. Una clase existente que solo declara constructor no se borra por eso: mirar consumidores, herencia e invariante. Estar en `Support` es desviación de convención. La gravedad depende del impacto, la frecuencia y el riesgo sustentados por evidencia (`18`, `24`). La Action dueña delimita la transacción. `CustomException` se lanza, no se retorna. No migrar un `Support` existente en silencio.
- Copy visible (`15`): el texto se juzga por audiencia y función, no por una palabra prohibida. Si quien lee no lo entiende, o la frase le pide algo que no puede hacer, no se publica así. Un término del dominio (`API key`, `PDF`, `URL`) se conserva. Al detectar copy ya escrito que le habla al operador, se propone ubicación, texto actual, problema y reemplazo. No se reescribe al tocar. El texto nuevo sale bien desde el inicio. Si se autoriza corregir ese copy, se aplica ese alcance sin volver a pedir permiso.
- Entorno ≠ producto (`01`/`08`/`15`/`17`). `npm run dev`, el test runner, `NODE_ENV`, `import.meta.env`, `APP_ENV` y `APP_DEBUG` no son un modo de producto: la lógica, el copy y las validaciones son los oficiales. Prohibido chip, banner o texto "Test mode" / "Testing mode" (y equivalentes), y prohibido ramificar labels o mensajes por ese entorno. Al tocar un archivo que lo tenga: borrar ese código; si el archivo existe solo para anunciarlo, borrar el archivo. No restylarlo ni dejarlo condicionado. Excepción solo si el contrato ya trae el flag y el requisito de este hilo pide mostrarlo. Auditoría: hallazgo Alto, sin editar.

## Autoridad y precedencia

1. Instrucción explícita del usuario en el hilo.
2. Contratos ejecutables del repo (tests, tipos, schemas, HTTP, migraciones, versiones).
3. Esta skill como estándar objetivo en toda tarea de desarrollo que el workflow carga. No solo cuando el usuario dice “mi estilo”.
4. Convenciones locales del repo (contexto; divergencias = hallazgos).
5. Buenas prácticas genéricas solo como Propuesta.

El molde canónico define la estructura objetivo FE/BE. Multi-tenant solo si aplica.

## Modos

| Modo | Señales | Edita código |
|------|---------|--------------|
| Implementar | crear feature, seguí mi estilo | Sí (alcance nuevo) |
| Auditar (feature) | audita esta feature / este módulo | No |
| Auditar (repositorio completo) | audita todo / el proyecto / el repo / full audit | No |
| Auditar + aplicar | audita y migra / aplica H-00x | Sí (lotes aprobados) |
| Consultar estándar | ¿cómo suelo…?, ¿enum o union? | No |

Alcance **repositorio completo** → protocolo `24` (coverage ledger + gate). Prohibido muestreo como cierre.
## Decision Gates

| Situación | Acción |
|-----------|--------|
| Toca repo | Fase 0 discovery → clasificar → cargar references |
| Repo Vue, Angular, Node, Python u otro stack | Núcleo (`01`, con su fila de stack) + el delta del stack si existe (`25` en Vue). No heredar la API React/MUI que el repo no usa. No saltarse nombres, helpers, enums ni contratos |
| Gap u oportunidad de mejorar stack, tipado, linting o abstracción | Aplicar **Evaluación de mejoras de stack** (`19`); comparar solución actual, mejora interna y librería externa; no instalar sin aprobación |
| Divergencia vs molde | Hallazgo en `18-migrate-audit.md` |
| Hook custom o archivo `use-*` / `use_*` | `04` Naming: camelCase `useX`; rename en alcance; no barrels `<entity>.queries.ts` |
| Variante con store de UI / drawers / fetchers por scope | `20-variants.md` + `09` |
| Tenancy central/tenant | `16-multi-tenant.md` |
| Solo pregunta de estándar | Modo Consultar; citar `references/…` |
| Chip, banner, texto o validación por dev/test ("Test mode", "Testing mode") | Implementar o tocar el archivo: borrar ese código; archivo que solo anuncia el entorno: borrar el archivo. Auditar: hallazgo Alto, no editar (`08`/`15`/`17`) |

## Execution Steps

### Fase 0 — Descubrimiento (antes de diseñar/auditar/editar)

1. Identificar raíz y alcance del repo.
2. Leer AGENTS.md / docs locales relevantes (contexto).
3. Detectar framework, versiones, package manager, deps, estructura, patrones equivalentes, comandos de validación.
4. **Inventario por capacidad** (`02`): fechas, HTTP, errores, server state, forms, i18n. En React, contrastar con QueryClient, RHF y `cn()`. En otro stack, buscar el equivalente; no marcar “ausente” la librería React ni proponer instalarla.
5. Ejemplos de feature:
   - **Implementar** o **Auditar feature:** ≥2 features de referencia equivalentes.
   - **Auditar repositorio completo:** inventario total de features/archivos (`24`) — **no** bastan 2 ejemplos como cierre.
6. Clasificar: Compatible con el estándar | Variante reconocida | Legacy para migración | Patrón desconocido.
7. Cargar solo references necesarias (matriz abajo).

### Por modo

**Implementar:** aplicar molde en alcance nuevo; reportar bloqueos; checklist `03`/`05`/`17`; Evaluación de mejoras de stack si hay evidencia.  
**Auditar (feature):** escanear vs molde; un solo `docs/pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md` en la raíz git del repo auditado (ES); Hallazgos / Propuestas. Si el `.gitignore` de esa raíz no ignora `docs/pattern-audit/`, se agrega esa línea.  
**Auditar (repositorio completo):** `18` + **`24`** (inventario, barridos, gate, disposición); mismo path de reporte; ledger auxiliar solo si hace falta; sin “alineado” sin gate.  
**Auditar + aplicar:** igual + checklist/registro **en el mismo archivo**; solo ítems aprobados; sin installs no aprobados.  
**Consultar:** responder desde references; distinguir Regla / Default / Variante / Excepción / Propuesta; citar ruta.

## Routing de references

| Situación | Leer |
|-----------|------|
| Arranque / índice humano | `00-index`, `01-principles` |
| Toca repo | `02-repository-discovery` (inventario + tooling) |
| Feature FE | `03-feature-mold`, `04-frontend-architecture`, `13-data-fetching`, `23-ts-style-helpers` |
| Repo Vue / `.vue` | Núcleo (`01`, `03`, `04` Naming, `07`, `08`, `14`, `23`) + `25-vue-sfc` |
| Otro stack sin capítulo (Angular, Node, Python) | Núcleo (`01`, filas por stack). El adaptador es la API del framework; no saltar el núcleo |
| Styling MUI/Tailwind / `sx` / `cn()` | `04-frontend-architecture`, `23-ts-style-helpers` |
| Display / labels / estados UI | `07-types-enums-statuses`, `08-display-conventions`, `15-i18n-copy` |
| Test mode / Testing mode / copy o chip condicionado por entorno | `01-principles`, `08-display-conventions`, `15-i18n-copy`, `17-testing-validation` |
| Ownership / enum vs union / shadow MUI / membresía includes | `07-types-enums-statuses` |
| cn / dayjs / utils vs helpers / memoización | `23-ts-style-helpers` |
| Memoización React (`useMemo` / `useCallback` / `memo`) | `23-ts-style-helpers` (A–E) |
| Formato visual TS/TSX (arrows, braces, JSX) | **no esta skill** — cargar `gian-ts-style` |
| Modal / drawer | `09-dialogs-drawers` |
| Forms / schema del body / tipo semántico del campo (RHF + Zod en React) | `10-forms-validation`; máscara, parser o picker → `19-propuestas-stack` |
| Mutations / ruta vs DTO / multipart | `13-data-fetching`, `10-forms-validation`, `23-ts-style-helpers` |
| Validación user-facing / FormRequest `messages` / Pydantic / 422 por campo | `01-principles`, `05-backend-mold`, `10-forms-validation`, `14-errors-feedback` |
| Tablas / filtros | `11-tables-filters` |
| State UI (Zustand, Pinia, etc.) | `12-state-management` |
| Laravel Action/Query/Resource/Request | `05-backend-mold`, `06-api-contracts` |
| Joins / Query Builder / SQL table aliases | `05-backend-mold` (t1/t2, st1 por nivel) |
| Formato visual PHP (indent, braces, guards, arrays) | **no esta skill** — cargar `gian-php-style` |
| Contratos HTTP / envelopes / whenLoaded Resource | `06-api-contracts` |
| Errores / toasts / cliente HTTP compartido + mapper de errores (`apiFetcher` en React) | `14-errors-feedback` |
| i18n / copy / `t()` vs `i18n.t()` | `15-i18n-copy`, `08-display-conventions`, `10-forms-validation` |
| Central/tenant | `16-multi-tenant` |
| Validación comandos | `17-testing-validation` |
| Auditar / migrar (feature) | `18-migrate-audit`, `21-output-contracts` |
| Auditar repositorio completo | `18-migrate-audit`, `24-full-repo-audit`, `21-output-contracts`, `02`, `19` |
| Gap u mejora de stack | `19-propuestas-stack` |
| Repo con patrón dominante distinto del default | `20-variants` |
| Calidad de diseño / traits / límites / refactor cohesión | `22-design-quality` |

## Output Contract

- Implementar: archivos tocados + checklist + propuestas pendientes.
- Auditar (feature): un solo `docs/pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md` en la raíz git del repo auditado (Hallazgos + Propuestas). Si falta, `docs/pattern-audit/` entra al `.gitignore` de esa raíz.  
- Auditar (repo completo): igual + gate/cobertura `24`; sin muestreo; sin “alineado” prematuro.  
- Aplicar: actualizar el mismo archivo (checklist + registro) + validación del repo.  
- Consultar: respuesta con cita `references/<file>.md` §sección.

## References
Ver `references/00-index.md`. Templates en `assets/`. Evals en `evals/`.
