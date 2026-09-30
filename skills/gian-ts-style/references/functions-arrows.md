# Functions and arrows

## Exported arrow default (HARD)

`exported-arrow-default`. Preferir:

```ts
export const getUser = () => UserService.get();
```

No:

```ts
export function getUser() {
  return UserService.get();
}
```

WRITE/FIX: convertir `export function` → `export const` arrow cuando no hay excepción.

Excepciones (KEEP, no FAIL):

- overloads TypeScript (`function parse(x: string): A; function parse(x: number): B;`)
- hoisting real necesario
- API de framework que exige `function`

Class methods (`static async getAll()`) → GAP; molde `gian-how-i-code`.
`export function cn` shadcn/generated → GAP.

## Implicit return (HARD) — no-component

`arrow-implicit-return`. Una sola expresión → sin `{}` ni `return`.

```ts
const loadUser = () => UserService.load();

const ids = users.map((user) => user.id);

const toOption = (user: User) => ({
  label: user.name,
  value: user.id,
});
```

No:

```ts
const loadUser = () => {
  return UserService.load();
};

const ids = users.map((user) => {
  return user.id;
});
```

Object literal: paréntesis `({ })`. Varias statements → block body.

SAFE FIX. No aplica a componentes PascalCase (`react-component-explicit-return`).

Callbacks: `.map`, `.filter`, `queryFn`, `mutationFn`, `Cell`, `Header`, camelCase `renderX` → implicit si una expresión (incl. JSX).

## When `function` is justified

Solo las excepciones de arriba. No usar `function` por gusto local del archivo.
