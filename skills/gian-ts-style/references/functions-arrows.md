# Functions and arrows

## Exported arrow default (HARD)

`exported-arrow-default`. Obligatorio: toda función de módulo, exportada o no, y toda function expression se escriben como `const x = (…) =>`.

```ts
export const getUser = () => UserService.get();

const toLabel = (user: User) => user.name;
```

No:

```ts
export function getUser() {
  return UserService.get();
}

function toLabel(user: User) {
  return user.name;
}

const toLabel = function (user: User) {
  return user.name;
};
```

`export default function X` → `const` + `export default` aparte:

```tsx
export const SettingsPage: FC = () => {
  return <SettingsLayout />;
};

export default SettingsPage;
```

No:

```tsx
export default function SettingsPage() {
  return <SettingsLayout />;
}
```

WRITE/FIX: convertir en el alcance. AUDIT: FAIL.

Excepciones, lista cerrada (se conserva `function`, no FAIL):

- overloads TypeScript (`function parse(x: string): A; function parse(x: number): B;`)
- generadores `function*`
- función que usa `this`
- función llamada a nivel de módulo antes de su definición

Nada más es excepción. El estilo del archivo no lo es.

Class methods: la forma (method o arrow field, `static async getAll()`) es GAP y la decide el molde de `gian-how-i-code`. El cuerpo de cada método cumple todas las reglas de esta skill.
`export function cn` de shadcn o de código generado → GAP.

## Implicit return (HARD) — no-component

`arrow-implicit-return`. Body con una sola expresión → sin `{}` ni `return`. También un body cuya única statement es una llamada sin `return` (`f()`, `await f()`, `a?.b()`): `() => { store.reset(); }` → `() => store.reset()`. Un body cuya única statement es una asignación conserva el block.

```ts
const loadUser = () => UserService.load();

const ids = users.map((user) => user.id);

const toOption = (user: User) => ({
  label: user.name,
  value: user.id,
});

const resetFilters = () => filtersStore.reset();
```

No:

```ts
const loadUser = () => {
  return UserService.load();
};

const ids = users.map((user) => {
  return user.id;
});

const resetFilters = () => {
  filtersStore.reset();
};
```

Object literal: paréntesis `({ })`. Varias statements → block body.

Excepción cerrada, se conserva el block: callback de `useEffect`, `useLayoutEffect` o `forEach` con una sola expression statement cuya expresión no devuelve `void` (por ejemplo, una llamada que devuelve una `Promise`). El implicit return la convertiría en el valor de retorno del callback.

```tsx
useEffect(() => {
  refetch();
}, [refetch]);
```

SAFE FIX. No aplica a componentes PascalCase (`react-component-explicit-return`).

Callbacks: `.map`, `.filter`, `queryFn`, `mutationFn`, `Cell`, `Header` y los helpers camelCase `renderX` → implicit si son una expresión (incluido JSX). `renderX` camelCase no es componente ni GAP.
