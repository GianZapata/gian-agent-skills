# Access and destructuring

## Direct property access (HARD)

`direct-property-access`. `const { a } = obj` sobre un objeto local o un parámetro que no es de componente → acceso directo `obj.a`.

```ts
const name = user.name;
const email = user.email;
```

No:

```ts
const { name, email } = user;
```

Excepciones, lista cerrada (se desestructura, no FAIL):

- props del componente (`FC<InvoiceDrawerProps> = ({ isOpen, onClose })`) y parámetros de un hook
- resultado de un hook `useX()` (`const { t } = useTranslation()`, `const { id } = useParams()`)
- tuplas (`const [search, setSearch] = useState('')`)
- `...rest`
- `Cell: ({ row: { original } })` — molde `gian-how-i-code` `11`
- alias de query (`query-data-alias`)

WRITE/FIX/AUDIT en el alcance. Si `obj` se reasigna o se muta entre la desestructuración y el uso, el acceso directo cambiaría el valor leído → `GAP direct-property-access archivo:línea — objeto mutado después de desestructurar`.

Vue: `interface HomePageProps` / `interface HomePageEmits`, y `const props = defineProps<HomePageProps>()` / `const emit = defineEmits<HomePageEmits>()`, sin desestructurar. `Props` / `Emits` a secas es error. El GAP de props de componente es solo de React.

## Query data alias (HARD)

`query-data-alias`. Si del resultado de la query solo se leen `.data` y flags (`isPending`, `isError`, `isFetching`) → alias semántico:

```ts
const { data: users, isPending } = useUsersQuery();
```

No:

```ts
const usersQuery = useUsersQuery();

const users = usersQuery.data;
```

Excepción: el result entero se pasa a otra función o componente. Ahí se conserva `const usersQuery = useUsersQuery()`.

## List default `[]` (HARD)

`list-data-default`. `data` es `T[]` y se leen `isPending` o `isError` del mismo hook → `data: x = []` obligatorio:

```ts
const {
  data: users = [],
  isPending,
} = useUsersQuery();
```

- detail o tipo no array: nunca `= []`. Se conserva `undefined` / `null`.
- `T[]` sin leer `isPending` ni `isError`: sin `= []`. Ocultar el loading con `= []` está prohibido.
