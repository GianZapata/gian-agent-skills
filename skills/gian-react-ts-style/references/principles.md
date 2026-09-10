# Principles

## Layers

1. **BASELINE** — TypeScript/React razonable cuando esta skill no especifica. No vender preferencias de Gian como best practice universal.
2. **PREFERENCE** — estilo deliberado. Audit FAIL sólo si es objetivamente determinable.
3. **HARD / OVERRIDE** — STYLE_GIAN estructural (braces, arrow body, JSX shape, import type).
4. **NEUTRAL / PRETTIER_OWNED** — indent, quotes, semi, trailing comma, printWidth, JSX wrap, `arrowParens`. MUST NOT FAIL. MUST NOT rewrite-only.
5. **GAP** — semántica dudosa o heurística frágil. MUST NOT FAIL. NEVER AUTOFIX.

## Precedence

```text
explicit user instruction
  > HARD gian-react-ts-style
  > repo ESLint/Prettier already active
  > PREFERENCE gian-react-ts-style
  > recommended baseline
```

## Operational modes (HARD)

Igual que `gian-php-style`. La skill **corrige** cuando está autorizada a editar; no se limita a observar.

```text
WRITE
→ código nuevo y hunk/función tocada salen conformes
→ SAFE FIX de inconsistencias dentro de ese alcance
→ no recorrer el archivo ni el repo

AUDIT
→ detecta y reporta; no edita

FIX
→ corrige inconsistencias existentes seguras
→ omite transformaciones semánticamente dudosas (GAP)
```

Una tarea normal (“agrega un filtro a esta tabla”) que edita `.ts`/`.tsx` es **WRITE**, no un format opcional.

## Scope of mutation

- Aplicar al código **nuevo** y al **hunk/función que la tarea ya está modificando**.
- Si alrededor del hunk hay un `if (!user) { return null; }` y esa región entra en el cambio, compactarla.
- No reformatear el resto de `users-table.tsx` ni el repositorio.

## FIX safety classes

- **SAFE FIX** — transformación estructural 1:1, sin cambio de asociación de control ni de runtime:
  - arrow `{ return expr; }` → implicit (no-component)
  - map callback `{ return x; }` → implicit
  - `disabled={true}` → `disabled`
  - `<Fragment>` sin props → `<>`
  - empty JSX → self-closing
  - type-only import → `import type`
  - `onClick={() => onClose()}` → `onClick={onClose}` (firma 1:1, cero args extra)
  - `if` standalone + una statement aprobada → quitar `{}`
- **AST-SENSITIVE** — corregible **solo** con gate:
  - `compact-if-else` plano
  - single-statement multilínea (JSX/throw wrap)
  - ternary `: null` → `&&` boolean-safe
  - nested ternary → forma derivada
  - `type` object shape propio → `interface`
- **NEVER AUTOFIX / GAP**:
  - nested `if` con `else`
  - dangling-else
  - guard-clause rewrite con side effects / bindings / JSX tree
  - prop spread de entity/DTO
  - `= []` donde `undefined` tiene semántica (detail query)
  - comentario why no-obvio
  - `renderFoo` camelCase ambiguo componente vs helper
  - `React.FC` vs props explícitas
  - wrap que Prettier reimprime

Al omitir: reportar `GAP — no corregido automáticamente: posible cambio de asociación/semántica`.

## Visual principle

```text
short + readable → inline
long/structured → multiline
multiline geometry → Prettier
statements vs lines → statements (AST)
```

No usar 80/100/120 como umbral de esta skill.

## Out of scope

Arquitectura, ownership de tipos, enums, React Query, RHF/Zod, UI/UX, selección de librerías → `gian-how-i-code`.
Class methods `static async foo()` vs class field arrows → molde `03`/`13`, GAP aquí.
`export function cn` de shadcn/generated → GAP.
