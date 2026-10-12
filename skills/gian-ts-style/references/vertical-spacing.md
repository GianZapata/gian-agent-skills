# Vertical spacing

## vertical-spacing (HARD)

`vertical-spacing`. Separar secciones con **una** línea en blanco. Los slots los decide `gian-how-i-code` (`04`). El orden dentro de cada slot, y el de una función plana, lo decide `26`. Si el edit entra en ese cuerpo, `04` y `26` reordenan esa función. Esta reference solo inserta la línea en blanco.

Sección, lista cerrada:

- cada grupo de declaraciones de una línea del mismo slot de `04` (dependencias, estado, hooks que leen estado, derivadas, funciones de una línea);
- cada sentencia multilínea (una `const` que ocupa varias líneas, una llamada que Prettier parte);
- cada función con block body;
- cada `computed` / `useMemo` / `useCallback` con block body;
- cada `watch` / `useEffect` / `useLayoutEffect` / `onMounted`;
- cada lectura con su complemento (`read-group`, abajo);
- el grupo de returns tempranos de una línea;
- el `return` final.

Reglas:

- Dos slots distintos de `04` nunca van pegados, aunque las dos líneas sean cortas.
- Las declaraciones de una línea del mismo slot van seguidas, sin línea en blanco, salvo dos lecturas (`read-group`).
- Una sentencia multilínea cierra con una línea en blanco. La siguiente no se le pega.
- Una función, efecto, `useMemo` o `computed` con cuerpo lleva una línea en blanco antes y después.
- En el slot de derivadas, las que leen la misma fuente van juntas. Al cambiar de fuente (`indicators.occupancy` → `indicators.arrears`), una línea en blanco.
- Nunca dos líneas en blanco seguidas.
- Sin comentarios de sección (`// State`, `// Effects`): los prohíbe `comments.md`. El espacio marca la sección.

## Dentro de un bloque (HARD)

El cuerpo de un handler, `useMemo`, efecto, callback o función plana con varios pasos sigue los pasos de `gian-how-i-code` `26`: normalizar, guards, cargar, decidir, derivar, efecto, `return`. Una línea en blanco entre pasos. Una sentencia multilínea cierra con línea en blanco.

`guard-glue`. La lectura que un guard necesita queda pegada encima de ese guard. El blanco va después del guard.

```ts
const areaNumber = (value: string | null): number | null => {
  if (value === null || value === '') return null;

  const number = Number(value);
  if (!Number.isFinite(number)) return null;

  return number;
};
```

No:

```ts
const number = Number(value);

if (!Number.isFinite(number)) return null;
```

En el cuerpo de un componente esto no aplica: los returns tempranos son su propio slot (`04`) y van separados.

## React

```tsx
export const InvoicePage: FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [note, setNote] = useState('');
  const [isOpen, setIsOpen] = useState(false);

  const { data: invoice, isPending } = useInvoiceQuery(id);

  const payInvoice = usePayInvoiceMutation(id);

  const rows = invoice?.lines ?? [];
  const canPay = invoice?.status === InvoiceStatus.Pending;

  const total = rows.reduce(
    (sum, row) => sum + row.amount,
    0,
  );

  const formatAmount = (value: number) => formatCurrency(value, invoice?.currency);

  useEffect(() => {
    document.title = invoice?.number ?? 'Factura';
  }, [invoice?.number]);

  if (isPending) return <Skeleton />;
  if (!invoice) return <EmptyState />;

  return (
    <InvoiceView
      rows={rows}
      note={note}
      isOpen={isOpen}
      canPay={canPay}
      total={formatAmount(total)}
      onOpenLine={(lineId) => navigate(`/invoices/${id}/lines/${lineId}`)}
      onNoteChange={setNote}
      onToggle={() => setIsOpen(!isOpen)}
      onPay={() => payInvoice.mutate({ note })}
    />
  );
};
```

No:

```tsx
const navigate = useNavigate();
const { data: tenant } = useTenantInfo();
const periodRef = useRef<HTMLDivElement>(null);
const [period, setPeriod] = useState(Period.Month);
const rows = invoice?.lines ?? [];
const occupancyRate = indicators?.occupancy.rate
  ? rate(indicators.occupancy.rate)
  : null;
const cohortShare = cohortMxn?.percent ? rate(cohortMxn.percent) : null;
const openBand = () => {
  onOpen(bucket);
};
```

Ahí la query va pegada a las dependencias, el `useRef` queda fuera del slot de estado, una derivada multilínea se pega a la siguiente y el handler se pega a las derivadas.

## Vue

```ts
const route = useRoute();

const draft = ref('');
const selectedId = ref('');

const query = computed(() => route.query.q);
const debt = computed(() => parseDebt(route.query.debt));

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

## Aplicar

WRITE y FIX aplican estas reglas en la función tocada y cierran con `assets/self-check.mjs` (`SKILL.md` § Self-check). AUDIT: FAIL si dos secciones van pegadas, si una sentencia multilínea no cierra con línea en blanco, si el guard se separa de su lectura, si dos lecturas van pegadas y la segunda no es complemento, o si hay dos líneas en blanco seguidas. La agrupación de derivadas por fuente la aplica el agente; si es dudosa, GAP.
