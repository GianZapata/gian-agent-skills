# Vertical spacing

PREFERENCE. Separar secciones con **una** línea en blanco. El orden lo decide `gian-how-i-code` (`04`): dependencias que no leen estado local, estado, hooks que leen ese estado, variables derivadas, funciones, efectos al final, return. Si el edit entra en ese cuerpo, `04` reordena esa función.

WRITE aplica la línea en blanco en el hunk. AUDIT marca FAIL solo si es objetivo: dos secciones pegadas, o dos líneas en blanco seguidas. No recorrer el archivo.

## Juntas

Declaraciones cortas del mismo tipo van seguidas, sin línea en blanco.

```ts
const draft = ref('');
const selectedId = ref('');

const query = computed(() => route.query.q);
const debt = computed(() => parseDebt(route.query.debt));
```

## Separadas

Cada función, `computed` con cuerpo, `watch` o efecto lleva una línea en blanco antes y después.

```ts
const filtered = computed(() => {
  if (!debt.value) return matched;
  return matched.filter((row) => standing(row) === debt.value);
});

const onSearchInput = (event: Event) => {
  draft.value = (event.target as HTMLInputElement).value;
};

watch(query, (value) => {
  draft.value = value;
});
```

Nunca dos líneas en blanco seguidas. Sin comentarios de sección (`// State`, `// Effects`): los prohíbe `comments.md`. El espacio marca la sección.
