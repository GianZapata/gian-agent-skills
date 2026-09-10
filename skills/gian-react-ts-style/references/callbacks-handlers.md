# Callbacks and handlers

## Direct reference (HARD)

`direct-handler-reference`. Si la función ya tiene la firma correcta:

```tsx
<Button onClick={onClose} />
```

No:

```tsx
<Button onClick={() => onClose()} />
```

SAFE FIX cuando: cero argumentos extra; no se ignora el evento a propósito; no hay bind parcial.

## Inline argument handler (PREFERENCE)

`inline-argument-handler`. Si necesita argumentos:

```tsx
<Button onClick={() => selectUser(user.id)} />
```

No extraer automáticamente `const selectCurrentUser = () => selectUser(user.id)` solo para pasarla al JSX.

WRITE: inline. AUDIT no FAIL extracción existente si el nombre aporta. NEVER AUTOFIX extracción ni inline-ización de named handlers reutilizados.

## No ceremonial extraction (PREFERENCE)

`no-ceremonial-handler-extraction`. Multi-statement local y claro → inline:

```tsx
onClick={() => {
  reset();
  onClose();
}}
```

Extraer solo si: reuso; nombre semántico valioso; cuerpo complejo; testing/API; legibilidad claramente mejor.

WRITE no inventa `const onCancel` ceremoniales. AUDIT no FAIL handlers nombrados existentes.
