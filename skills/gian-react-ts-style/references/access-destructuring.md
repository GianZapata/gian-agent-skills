# Access and destructuring

## Direct property access (PREFERENCE)

`direct-property-access`. No destructurar por rutina:

```ts
const name = user.name;
const email = user.email;
```

No (default):

```ts
const { name, email } = user;
```

No HARD. WRITE en locals nuevos. AUDIT no FAIL corpus. NEVER AUTOFIX masivo.

GAP / no aplicar:

- params de componente/hook (`({ open, onClose }: Props)`)
- `Cell: ({ row: { original } })` — molde `gian-how-i-code` `11`
- alias de query (`query-data-alias`)

## Query data alias (PREFERENCE)

`query-data-alias`.

```ts
const { data: users } = useUsersQuery();
```

No forzar si el caller usa el result entero. WRITE prefiere alias semántico.

## List default `[]` (PREFERENCE)

`list-data-default`. Solo **list** queries donde empty vs pending ya se distinguen:

```ts
const {
  data: users = [],
  isPending,
} = useUsersQuery();
```

No aplicar `= []` mecánicamente.

- list: default `[]` puede tener sentido si `isPending`/`isError` se leen aparte
- **detail**: conservar `undefined`/`null` — no `data: entity = []`

NEVER AUTOFIX si no está claro list vs detail. Ocultar loading con `= []` está prohibido.
