# Vertical spacing

PREFERENCE. Separar secciones con **una** línea en blanco. Los slots los decide `gian-how-i-code` (`04`). Los casos dentro de cada slot, y el orden de una función plana, los decide `26`. Si el edit entra en ese cuerpo, `04` y `26` reordenan esa función. Esta reference solo inserta la línea en blanco.

WRITE aplica la línea en blanco en el hunk. AUDIT marca FAIL solo si es objetivo: dos secciones pegadas, o dos líneas en blanco seguidas. No recorrer el archivo.

## Juntas

Declaraciones cortas del mismo tipo van seguidas, sin línea en blanco, salvo dos lecturas (`read-group`, abajo).

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

## Una lectura, un grupo (HARD)

`read-group`. Cada lectura abre su propio grupo. Su complemento va pegado debajo. Una línea en blanco cierra el grupo. Dos lecturas solo van pegadas si la segunda es complemento de la primera, aunque cada una quepa en una línea. Gana a la regla que junta declaraciones cortas del mismo slot.

Lectura: lo que trae datos de una fuente.

- En un componente, hook o composable: cada query (`useQuery`, `useSuspenseQuery`, `useXQuery`, el composable que trae datos).
- En una función plana: cada `await` que trae datos de un service, repositorio, `fetch` o cliente HTTP (`get`, `list`, `find`).

Un write no es lectura. Una mutation de un componente: las de una línea van juntas entre ellas, en su grupo. Un `await` que escribe (`post`, `patch`, `put`, `delete`, `save`) es efecto (`gian-how-i-code` `26`).

Complemento: la sentencia de una línea justo debajo que solo lee esa lectura y existe para completarla: sus ids, su `Map` por id, su detalle cuyo nombre deriva del de la lectura. Otra entidad es otra lectura y abre su grupo. Una línea que combina dos lecturas es una derivada y abre su grupo. En un componente, la derivada barata (`?? []`) vive en el slot de derivadas de `gian-how-i-code` `04`, no como complemento.

Si la lectura es multilínea, la línea en blanco va al cerrarla. Su complemento queda en su propio grupo. Única excepción: el guard que la valida se queda pegado (`gian-how-i-code` `26`).

```tsx
const invoice = useInvoiceQuery(id);

const payments = usePaymentsQuery(id);

const pay = usePayInvoice(id);
const cancel = useCancelInvoice(id);
```

```ts
export const loadDashboard = async (from: string, to: string) => {
  const range = { from, to };

  const orders = await orderService.list(range);
  const orderIds = orders.map((order) => order.id);

  const invoices = await invoiceService.list({ orderIds });

  const customers = await customerService.list(range);
  const customerById = new Map(customers.map((customer) => [customer.id, customer]));

  return buildDashboard(orders, invoices, customerById);
};
```

No:

```ts
const orders = await orderService.list(range);
const orderIds = orders.map((order) => order.id);
const invoices = await invoiceService.list({ orderIds });
const customers = await customerService.list(range);
```

WRITE lo aplica en la función tocada. AUDIT: FAIL si dos lecturas van pegadas y la segunda no es complemento de la primera. Si no es claro que una línea sea lectura o complemento: GAP, sin FAIL.
