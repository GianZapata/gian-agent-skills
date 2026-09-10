# Conditions and guards

## Single-statement-if (HARD)

`single-statement-if`. Si un `if` **standalone** (sin `else` / `else if` en esa statement) contiene **exactamente una** statement aprobada: omitir `{}`.

Aprobadas: `return`; `throw`; call; assignment; `continue`; `break`.

```ts
if (!entity) return null;

if (!enabled) return;

if (!id) throw new Error('Entity id is required');

if (enabled) refresh();

if (user) name = user.name;
```

No:

```ts
if (!entity) {
  return null;
}
```

Varias statements → braces.

```ts
if (!user) {
  logMissing();
  return null;
}
```

WRITE/FIX: SAFE FIX si standalone + una aprobada + sin `if` anidado en el cuerpo.

### Lines ≠ statements

`single-statement-multiline` es **cláusula** de esta regla, no otro ID. Wrapping de Prettier no convierte una statement en varias.

```tsx
if (!entity) return (
  <EmptyState
    title="Sin entidad"
    description="Selecciona una entidad"
  />
);

if (!entity) throw new DomainError(
  'Entity is required before continuing',
  context,
);
```

AST-SENSITIVE: aplicar si sigue siendo una statement. No añadir braces porque el wrap ocupa varias líneas.

### Dangling-else / association (NEVER AUTOFIX)

1. El `if` tiene `else` o `else if` → no usar el SAFE FIX de standalone (ver `compact-if-else`).
2. El cuerpo contiene otro `if` → no quitar braces.
3. Un `else` hermano se asocia a este `if` vía braces → no quitar braces.
4. Si el árbol de control diferiría → skip FIX; GAP.

## Compact if/else (PREFERENCE)

`compact-if-else`. Una statement aprobada por branch, **ningún** branch contiene `if`, no `else if`, no comments entre `if`/`else`:

```ts
if (enabled) start();
else stop();
```

AST-SENSITIVE. AUDIT FAIL solo caso plano demostrable. FIX NEVER si nesting / else-if / 3+ branches / JSX association dudosa.

```text
GAP — no corregido automáticamente:
posible cambio de asociación/semántica
```

## Guard clauses (PREFERENCE)

`guard-clause-over-nesting`. WRITE en código nuevo:

```ts
if (!user) return;
if (!user.active) return;

refresh();
```

No:

```ts
if (user) {
  if (user.active) {
    refresh();
  }
}
```

FIX NEVER AUTOFIX si: `else` en cualquier nivel; bindings del bloque externo usados después; side effects en la condición invertida; loops; JSX tree; mutations de estado. AUDIT no FAIL legado ambiguo.
