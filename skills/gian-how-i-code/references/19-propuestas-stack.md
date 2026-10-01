# 19 — Evaluación de mejoras de stack

Cargar cuando: gap, complejidad, dependencia potencial, mejora no molde-estricto, oportunidad positiva.

## Capacidad canónica

**Evaluación de mejoras de stack** — aplica durante **Implementar** y **Auditar** cuando exista evidencia de:

- una capacidad faltante;
- una dependencia instalada pero subutilizada;
- código manual sustituible por una abstracción madura;
- una mejora de configuración, linting, tipado o arquitectura;
- una oportunidad para simplificar o hacer más segura una implementación.

No es obligatorio producir una propuesta en cada tarea. Si el stack actual ya resuelve adecuadamente el problema, registrar `No requiere cambio` o no crear una PROP.

Una ayuda de captura (`10`) que falta se propone nombrando solo la capacidad que ella necesita: utilidad local, catálogo, endpoint o debounce. No se piden los cuatro si basta uno. No se instala sin OK.

## Decision Gate (obligatorio)

1. Detectar una necesidad concreta.  
2. Demostrarla con evidencia del código.  
3. Verificar dependencias y versiones actuales (`package.json` / `composer.json` / `pyproject.toml` / lockfiles, `uv.lock` incluido).  
4. Buscar una capacidad equivalente ya instalada o wrapper local.  
5. Comparar: solución con stack actual | mejora interna sin dependencia | librería/herramienta externa.  
6. Consultar documentación oficial (no versiones de memoria).  
7. Explicar beneficios y costos.  
8. Recomendar una opción.  
9. Esperar autorización explícita antes de instalar o modificar manifests.  
10. Tras aprobación: instalar con el package manager real → integrar → tests → validaciones → documentar la decisión.

## Clasificación

| Tipo | Significado |
|------|------------|
| Librería faltante | Capacidad necesaria no está en el repo |
| Librería instalada pero subutilizada | Existe pero el código no la aprovecha |
| Abstracción interna faltante | Falta helper/store/wrapper del propio estándar |
| Mejora de configuración | Ajuste de tooling/config |
| Mejora de linting | p. ej. `@tanstack/eslint-plugin-query` |
| Mejora de tipado | Enums, Params tipados, quitar casts |
| Complejidad innecesariamente manual | Wizard, máquina de estados o tabla a mano. También máscara, parser o picker de moneda, decimal por locale, fecha con rangos o zona, u hora con intervalos, cuando una librería madura ya lo cubre (`10`) |
| Sustitución no recomendable | Cambiar lib por moda sin ganancia |
| Oportunidad futura no prioritaria | Diferir |
| No requiere cambio | Stack actual suficiente |

## Reglas

1. Verificar manifests y abstracciones **antes** de proponer.  
2. No versiones de memoria.  
3. Mala práctica corregible con stack existente ≠ propuesta de install (preferir Hallazgo H-).  
4. Preferir el stack canónico de este estándar cuando cubra el caso.  
5. **Nunca instalar sin OK.**  
6. Auditoría no toca manifests.  
7. El comando de instalación se muestra como propuesta; no se ejecuta hasta aprobación.
8. **Costos y riesgos reales** — prohibido “Costos y riesgos: Ninguno”. Incluir migración, API change, fragmentación de caché, esfuerzo de adopción, etc.
9. **No afirmar que algo “garantiza CI”** salvo evidencia: plugin/reglas en ESLint, script de lint, y job de CI que lo ejecute. Si falta alguno, decirlo.
10. Migrar query keys / invalidaciones: evaluar riesgo de cambiar identidades de caché y plan incremental.

## Dependencias FE canónicas esperadas

Contrastar con el inventario por capacidad de `02`. Presente pero mal usado → Hallazgo (subutilización), no reinstalar.

El adaptador React de abajo es el esperado **cuando el repo es React**. En Vue, Angular u otro stack, la ausencia de TanStack Query, RHF, MUI o `cn()` no es PROP de instalarlos. Se pide el equivalente de esa capacidad en el stack (`01`). dayjs y el mapper de errores sí se esperan en cualquier cliente TS. En un backend Python no se proponen libs JS: las fechas van en un módulo con datetimes aware (`01`). El cliente HTTP es uno compartido más `SharedService`: `apiFetcher` donde el repo lo elige. En Angular es `HttpClient` más un interceptor, porque el framework lo impone (`LIBRARY_OWNED`). No se pide axios ahí.

| Capacidad | Adaptador React |
|-----------|-----------------|
| Server state + keys | TanStack Query + `query-key-factory` / `mergeQueryKeys` (o híbrido documentado) |
| Forms + UI | RHF + Zod + i18n + MUI/Tailwind/`cn` (`04`, `10`, `15`) |
| **dayjs** + módulo configurado | Fechas de negocio (`23`). Cualquier cliente TS |
| Cliente HTTP compartido + `SharedService` | HTTP único (`14`). `apiFetcher` en el adaptador React. En Angular, `HttpClient` + interceptor; no pedir axios |
| `CustomError` + `ErrorMapper` | Errores traducidos (`14`). Cualquier cliente TS |
| `QueryClient` central | Defaults compartidos (`13`). Solo si el server state es React Query |
| Realtime (Echo/Reverb) | **Solo si** el producto lo necesita — no stack mínimo |

- dayjs ausente en un cliente TS → PROP **Librería faltante** (Alta) + hallazgo `new Date` si aplica.
- dayjs presente, imports crudos / sin módulo → PROP **Abstracción interna** o Hallazgo.
- React Query sin store de keys / invalidaciones con arrays sueltos → subutilización o abstracción interna.
- axios ad-hoc / sin ErrorMapper → Hallazgo + PROP de abstracción.
- Repo Vue/Angular sin React Query, RHF o MUI → no PROP. Cumplir la responsabilidad con el equivalente del stack.
## Contrato PROP-NNN

```markdown
### PROP-001 — [Título]
- Tipo: (ver clasificación)
- Severidad: Alta | Media | Baja
- Problema observado:
- Evidencia:
- Capacidad necesaria:
- Solución con stack actual:
- Librería o herramienta propuesta:
- Ya existe en el repositorio: Sí | No
- Alternativas:
- Beneficios:
- Costos y riesgos:
- Impacto arquitectónico:
- Archivos o capas afectadas:
- Comando de instalación: (propuesta; no ejecutar)
- Plan de integración:
- Plan de migración:
- Tests requeridos:
- Validaciones requeridas:
- Requiere instalación: Sí | No
- Requiere aprobación: Sí
- Estado: Propuesta | Aprobada | Rechazada | Aplicada
```

## Ejemplos de cuándo proponer

- Falta TanStack Query y hay fetch en `useEffect`.
- Query-key-factory instalado pero keys manuales + invalidate con arrays sueltos → **subutilizada**.
- Catálogos sin `staleTime` y refetch agresivo → tipado/config, no lib nueva.
- Wizard de 8 pasos sin máquina de estados y el dominio es SM → evaluar lib o patrón interno.
- Campo de moneda, decimal por locale, fecha con rangos o zona, u hora con intervalos: no escribir la máscara, el parser ni el picker. Usar el componente o wrapper del repo. Si no existe, PROP de una librería del framework de ese repo (`10`). No instalar sin OK. Mientras tanto, el campo queda con el tipo y la validación de `10`.

## Ejemplos de cuándo no proponer

- El repo ya resuelve bien con SharedService + Query.
- Sustituir MUI por otra UI lib por preferencia.
- Instalar “la última moda” sin evidencia de dolor.
- Instalar TanStack Query, RHF o MUI en un repo que no es React. Cumplir la capacidad con el equivalente del stack (`01`).
- Proponer dayjs, Zod u otra lib JS en un backend Python.
- Una máscara, un parser o un picker escritos a mano para moneda, decimal por locale, fecha u hora. Ahí la propuesta es el componente del repo o una librería del framework (`10`), no el parser propio.

## Preferencias canónicas (sin pin de versión)

| Caso | Preferir |
|------|----------|
| Server state (React) | TanStack Query |
| Query key factory | `@lukemorales/query-key-factory` si ya es el patrón; si no, evaluar |
| Lint Query | `@tanstack/eslint-plugin-query` con evidencia, solo si hay React Query |
| Forms (React) | RHF + Zod. En otro stack, el form del stack. Un schema nombrado es la fuente del DTO; Zod es ese schema en TypeScript |
| Query HTTP Laravel | Spatie QueryBuilder |
| SM | paquete de state machines ya en repo o el canónico del estándar |
| UI (React) | MUI + Tailwind |
| Tenancy multi-DB | stancl/tenancy si el producto lo requiere |

Si el repo ya eligió otra lib equivalente → variante, no reinstall.
