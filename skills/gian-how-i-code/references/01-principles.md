# 01 — Principios

Cargar cuando: arranque, conflicto de reglas, modo Consultar sobre “por qué”, o un stack que no es React.

## Reglas de oro

1. **El molde canónico** define la estructura objetivo para features frontend, backend, contratos, formularios, consultas y mutaciones. Usar features CRUD maduras del propio repo como ejemplos de referencia.
2. **Una fuente tipada de verdad** para estados/tipos cerrados (TS string enum `APP_OWNED`; PHP backed Enum o constantes en State Machine string-based — ver `07`). Ownership antes de declarar el contrato.
3. **Negocio en el contrato de lectura** (Laravel: Resource/Action), no recalcular flags en el cliente. El cliente refleja el contrato; no lo adivina.
4. **Display:** metadata exhaustiva de un enum `APP_OWNED` en el entity helper (`static readonly Record`, `08`). Display ad-hoc de un componente: cadena de `if` inline. En React, `useMemo` según `23` A–E (no ceremonial; multi-rama C sí).
5. **Diálogo dueño** de mutación + invalidate; padre solo trigger + entidad + onClose. En React el montaje es `{isOpen && user && (`; en otro stack, el overlay equivalente. La propiedad no cambia.
6. **YAGNI + migración oportunista**: al tocar, alinear; no refactor masivo no pedido. No escribir un capítulo de stack (Angular, Node, Python, …) sin un repo real.
7. **Evaluación de mejoras de stack** antes de instalar; mala práctica ≠ “instala una lib”.
8. **Fechas, helpers y estilo** (`23`/`04`): dayjs vía el módulo del repo; utils chicos / helpers clase de área; alias claros, no opacos. En el adaptador React: `cn()` para clases que varían, Tailwind-first, sin `*_SX` locales, memo A–E. Sintaxis TS/TSX → `gian-ts-style`.
9. **Formato PHP** no vive aquí: cargar `gian-php-style`. **Formato TS/TSX** no vive aquí: cargar `gian-ts-style` (WRITE/FIX corrigen el hunk; AUDIT no edita).
10. **Ruta ≠ body.** IDs de URL no se mezclan con el DTO. Firmas y `TVariables` en `13`; schema en `10`.
11. **El lenguaje no apaga el estándar.** Núcleo y adaptador, abajo. Una API de React que el stack no tiene no es permiso para saltarse la responsabilidad.
12. **El entorno no es un modo de producto.** `npm run dev`, el test runner y las variables de entorno ejecutan la lógica oficial. No condicionar copy, chips ni validaciones al runtime. Al tocarlo, borrarlo (`08`/`15`/`17`).

## Núcleo y adaptador

El núcleo vale en React, Vue, Angular, Node o el que siga. Un capítulo de stack (`25` y los que existan después) solo documenta el delta del adaptador. No reescribe nombres, helpers, enums ni contratos.

| Capa | Qué decide |
|------|------------|
| Núcleo | Nombres del dominio; helpers de área en clase; enums y ownership (`07`); contratos (`06`); ruta ≠ body (`13` §4); errores (`14`); display (`08`); i18n sin inyectar `TFunction` (`15`); diseño (`22`); fechas, alias, utils vs helpers (`23`); capas (`03`/`05`). Diálogo dueño de su mutación. Server state sin duplicar en otro store. DTO desde el schema, no un `interface *Input` paralelo. |
| Adaptador | Vista, primitivo de estado, cliente de datos, forms, estructura que pide el CLI. |

Lo que el framework impone (`script setup`, `@Component`, DI, `*.component.ts`) es `LIBRARY_OWNED` (`07`): se usa y no se pelea. Lo que el framework deja libre lo decide el núcleo.

El nombre de archivo que exige la guía oficial del framework es `LIBRARY_OWNED` (`user-list.component.ts` en Angular). Clases, métodos, variables y helpers siguen `04` Naming.

Si una regla del núcleo está escrita con una API que este stack no tiene, “no aplica” no cierra el tema (`24` §3, en todo modo, no solo en auditoría de repo). Se cumple la responsabilidad con el equivalente del stack. No se instala la librería React para tapar el hueco (`19`).

| Responsabilidad | Adaptador React | Equivalente |
|-----------------|-----------------|-------------|
| Server state | TanStack Query | El cliente de datos del stack. No duplicar en un store de UI |
| Form y DTO | RHF + Zod | El form del stack. Un schema nombrado es la fuente del DTO; no un `interface` paralelo. Zod es ese schema en TypeScript |
| i18n en la vista | `t()` de `useTranslation` | El helper del framework (`15`). Fuera de la vista, `i18n.t()` |
| Vista | TSX | Lo que impone el framework |
| Estado local | `useState` | El primitivo del framework |
| Clases | `className` + `cn()` | `class` si no hay `cn()`. No exigir `cn()` |
| Carpeta de estado de UI | `hooks/` | `composables/` en Vue. El archivo sigue `useThing.ts` |

| Responsabilidad | Laravel | Python | Node |
|-----------------|---------|--------|------|
| Validación en el borde | FormRequest (`05`) | Body model de Pydantic, separado de los path params; `RequestValidationError` → 422 por campo con copy de dominio | Schema del handler |
| Caso de uso | Action | Service | Service |
| Contrato de lectura | Resource (`06`) | `response_model` o serializer | Serializer o mapper |
| Enum y estado | Backed enum + state machine (`07`) | `StrEnum` + mapa de transiciones | Enum TS + mapa de transiciones |
| Membresía | `in_array(..., true)` | `in (A, B)` | `.includes()` |
| Fechas | Carbon | Un módulo con datetimes aware | dayjs |
| Helper de área | Clase | Clase | Clase |
| Nombre de archivo | PSR-4 | snake_case; PEP 8 lo impone el lenguaje | El del repo |

El snake_case de Python es `LIBRARY_OWNED`, igual que el kebab de Angular. El dominio del nombre sigue `04` Naming.

Solo filas. No escribir un capítulo de Node, Python o Angular sin un repo real (`#6`).

## Qué es obligatorio vs default vs variante

| Nivel | Significado |
|-------|------------|
| Regla | Incumplir = hallazgo Alto/Medio |
| Default | Preferir salvo evidencia de variante reconocida (`20`) |
| Variante | Documentada en `20` (p. ej. Zustand para drawers) |
| Excepción | Legacy / OpenAPI generado / texto libre |

Un patrón local que no está en `20` no es variante. Otra tecnología para la misma capacidad es adaptador (`24` §3). Un patrón que rompe una regla de núcleo es legacy.

## Anti-objetivos

- No diluir esta skill como “notas” o índice de otros documentos.
- No reescribir un producto entero en un cambio pequeño.
- No inventar campos API ni `any` para tapar gaps.
- No anunciar el entorno en la UI ni ramificar el producto por dev/test.
