# Callbacks and handlers

Solo React (JSX). En Vue, Angular y Node no aplica.

## Direct reference (HARD)

`direct-handler-reference`. Wrapper que solo llama a una función → referencia directa.

```tsx
<Button onClick={onClose} />
```

No:

```tsx
<Button onClick={() => onClose()} />
```

SAFE FIX cuando la función declara 0 parámetros, o parámetros idénticos a los que pasa la prop. Si la función acepta un parámetro opcional que el evento llenaría (`onClose(reason?)`), se conserva el wrapper. Bind parcial (`() => onSelect(user.id)`) → `inline-argument-handler`.

## Inline argument handler (HARD)

`inline-argument-handler`. Un handler con argumentos que se usa una sola vez en JSX va inline:

```tsx
<Button onClick={() => selectUser(user.id)} />
```

No:

```tsx
const selectCurrentUser = () => selectUser(user.id);

<Button onClick={selectCurrentUser} />
```

WRITE: inline. FIX/AUDIT en el alcance: `const x = () => f(a)` con un único uso, y ese uso es JSX → inline.

## No ceremonial extraction (HARD)

`no-ceremonial-handler-extraction`. Un handler que se usa una sola vez en JSX va inline, aunque tenga varias statements:

```tsx
onClick={() => {
  reset();
  onClose();
}}
```

Se extrae a `const` solo si cumple uno de estos criterios, lista cerrada:

- se usa en 2 o más sitios;
- se pasa a algo que no es JSX (array de deps, `export`, un test).

WRITE no crea `const onCancel` fuera de esa lista. FIX/AUDIT en el alcance: un handler nombrado que no cumple la lista → inline.
