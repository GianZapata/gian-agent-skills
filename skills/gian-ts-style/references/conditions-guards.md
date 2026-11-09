# Conditions and guards

## Single-statement-if (HARD)

`single-statement-if`. Un `if` **standalone** (sin `else` / `else if` en esa statement) con **exactamente una** statement aprobada:

- el `if` completo cabe en una línea física tras Prettier → sin `{}`;
- el `if` ocupa varias líneas → con `{}`.

Aprobadas, lista cerrada: `return`; `throw`; call; `await` call; optional call (`a?.b()`); assignment; `++` / `--`; `continue`; `break`.

Conservan `{}`: `yield`, declaraciones (`const` / `let`) y cualquier statement fuera de la lista.

```ts
if (!entity) return null;

if (!enabled) return;

if (!id) throw new Error('Entity id is required');

if (enabled) refresh();

if (shouldSync) await sync();

if (user) name = user.name;

if (isValid) attempts++;
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

### Multilínea → llaves

Si la statement no cabe en la línea del `if`, lleva llaves. Vale igual que en `gian-php-style`.

```tsx
if (!contract) return null;

if (!contract) {
  return (
    <EmptyState
      title={t('contracts:empty.title')}
      description={t('contracts:empty.description')}
    />
  );
}

if (!entity) {
  throw new DomainError(
    'Entity is required before continuing',
    context,
  );
}
```

No:

```tsx
if (!contract) return (
  <EmptyState title={t('contracts:empty.title')} />
);

if (!entity)
  throw new DomainError('Entity is required before continuing', context);
```

`for` / `for…of` / `while` no siguen esta regla. Prettier y el repo deciden sus llaves.

WRITE/FIX: SAFE FIX en las dos direcciones (quitar `{}` de una línea, añadir `{}` a multilínea) si el `if` es standalone y el cuerpo no contiene otro `if`. AUDIT: FAIL en las dos direcciones.

### Dangling-else / association (NEVER AUTOFIX)

1. El `if` tiene `else` o `else if` → no usar el SAFE FIX de standalone (ver `compact-if-else`).
2. El cuerpo contiene otro `if` → no quitar braces.
3. Un `else` hermano se asocia a este `if` vía braces → no quitar braces.

Estos tres casos se reportan `GAP single-statement-if archivo:línea — <caso>`.

## Compact if/else (HARD)

`compact-if-else`. Aplicar cuando se cumplen todos:

- dos ramas: `if` y `else`, sin `else if`;
- cada rama tiene una statement aprobada que cabe en una línea;
- ninguna rama contiene `if`;
- sin comentarios entre `if` y `else`.

```ts
if (enabled) start();
else stop();
```

No:

```ts
if (enabled) {
  start();
} else {
  stop();
}
```

Si una rama no cumple, la regla no aplica: llaves en las dos ramas (`} else {`). No es FAIL.

WRITE/FIX/AUDIT: aplicar con los criterios de arriba. Un `if` anidado con `else` es GAP (`principles.md` § NEVER AUTOFIX).

## Guard clauses (HARD)

`guard-clause-over-nesting`. Un `if` sin `else` cuyo único contenido es otro `if` sin `else`, y que es la última statement de la función → guard clauses.

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

WRITE: aplicar siempre. FIX y AUDIT: aplicar en el alcance, salvo esta lista cerrada, que se reporta `GAP guard-clause-over-nesting archivo:línea — <caso>`:

- `else` en cualquier nivel;
- bindings del bloque externo usados después;
- side effects en la condición que se invierte;
- el `if` está dentro de un loop;
- el `if` decide un árbol JSX;
- mutations de estado (`setX`, `ref.value =`) dentro del bloque.
