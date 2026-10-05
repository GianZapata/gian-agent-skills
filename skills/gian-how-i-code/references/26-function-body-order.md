# 26 — Orden dentro de la función

Cargar cuando: el edit entra en un método PHP, en una función plana `.ts`, o en el cuerpo de un componente, hook o composable y hace falta resolver el orden dentro de un slot. Los siete slots de ese cuerpo están en `04`. Esta reference no los copia.

La línea en blanco entre pasos es formato: `gian-php-style` o `gian-ts-style`.

## Alcance

Entra la función que el edit toca: método PHP público o privado, componente, hook, composable, o función plana de un módulo `.ts`. Se mueven bloques de primer nivel.

El otro método o el otro componente del archivo queda como está. Imports, la interface de props y el orden de los miembros de la clase quedan fuera. Un closure, el callback de `map` / `filter` / `array_map`, y un arrow de una expresión son el algoritmo de esa línea: su cuerpo no se reordena.

Si mover un bloque cambiaría el comportamiento, no se mueve y queda GAP. Cubre un efecto cuyo lugar importa, un lock, una transacción que no se puede partir, un temporal dead zone y las rules of hooks. No se mete un guard dentro de un efecto para forzar el orden.

## PHP y función plana

El mismo orden por rol vale para un método PHP y para una función plana `.ts` que no es componente, hook ni composable. La dependencia de datos gana al rol: una lectura que un guard necesita se queda pegada encima de ese guard.

1. Normalizar la entrada: trim, cast, default. Las de una línea del mismo paso van juntas.
2. Guards: `return` / `throw` tempranos, y `continue` dentro de un bucle. El orden es invalidez, ausencia, conflicto, precondición. El camino feliz queda al nivel del método.
3. Cargar. Las lecturas consecutivas que no se necesitan entre sí son el mismo paso. La que usa el resultado de la anterior va debajo. Una query no sube por encima del id que usa.
4. Decidir: `match`, `if` / `else` que elige un valor. Un anidado profundo se queda, o se extrae a un método privado. No se reordenan sus ramas.
5. Derivar: mapas, reducciones y transforms de lo cargado.
6. Efecto: writes, eventos, jobs. Un write no queda arriba del guard que lo habría saltado.
7. `return` del camino feliz.

```php
$invoice = $this->invoices->find($id);
$payments = $this->payments->forInvoice($id);

$customer = $this->customers->find($invoice->customerId);
```

`$invoice` y `$payments` solo usan `$id`, así que van juntas. `$customer` usa `$invoice`, así que baja.

La transacción envuelve el efecto. Los guards y la lectura que decide entrar quedan afuera. Si el lock exige que esa lectura viva adentro, la sección crítica se queda entera adentro.

`try` / `catch` se queda alrededor de lo que puede fallar. `match` y `switch` son un solo paso. Sus casos siguen el orden del dominio.

Un bucle de tres líneas que acumula se queda junto. Si el cuerpo del bucle es un procedimiento con guards y trabajo, y el edit entra ahí, usa estos mismos roles.

```php
public function handle(int $id): Invoice {
    if ($id <= 0) throw new InvalidArgumentException('Invoice id is required.');

    $invoice = $this->invoices->find($id);
    if ($invoice === null) throw new ModelNotFoundException();
    if ($invoice->isPaid()) throw new ConflictException('Invoice is already paid.');

    $invoice->markPaid();
    $this->invoices->save($invoice);

    return $invoice;
}
```

## React, hook y composable

Los slots son los de `04`. Aquí solo el orden dentro de cada uno.

- Dependencias que no leen estado local: router y route, luego stores, luego clientes.
- Estado: primero ids y lo que sale de la ruta, luego el input del usuario, luego el chrome (`open`, tab). Un par `search` / `setSearch` es una declaración. El orden en que el resto del cuerpo los lee gana al alfabético.
- Hooks que leen ese estado: queries que el render necesita, luego mutations, luego el resto. El que consume a otro va debajo. Ninguno debajo de un `return` ni de un efecto.
- Derivadas: cada `const` debajo de lo que lee. Las baratas (`?? []`, un boolean) siguen juntas y en una línea. Un `useMemo` de varias ramas (`23`, caso C) es un solo bloque.
- Funciones: helpers que los handlers llaman, luego handlers en el orden en que el JSX los lee. El handler que solo usa un efecto queda inmediatamente arriba de ese efecto, en el slot de funciones. Extraer un handler ceremonial, o envolver una referencia directa, lo decide `gian-ts-style`.
- Efectos: al final del cuerpo, antes de cualquier `return`. Varios efectos siguen el orden en que se declaró el estado que leen. Primero los que sincronizan datos, después DOM o título, después el ciclo de vida (`onMounted`).
- Returns tempranos del componente, después de todos los hooks: loading, error, vacío, y el return principal.

```tsx
export const InvoicePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [note, setNote] = useState('');

  const invoice = useInvoiceQuery(id);
  const pay = usePayInvoiceMutation();

  const rows = invoice.data?.lines ?? [];

  const openLine = (lineId: string) => {
    navigate(`/invoices/${id}/lines/${lineId}`);
  };

  const onPay = () => {
    pay.mutate({ id, note });
  };

  useEffect(() => {
    document.title = invoice.data?.number ?? 'Factura';
  }, [invoice.data?.number]);

  if (invoice.isLoading) return <Skeleton />;
  if (invoice.isError) return <ErrorState />;

  return <InvoiceView rows={rows} onOpen={openLine} onPay={onPay} />;
};
```

## Fuera de este contrato

Orden de imports, de miembros de clase, de hijos JSX y de clases de Tailwind. Tampoco un sort alfabético de handlers o de propiedades.

## Aplicar

WRITE reordena la función tocada cuando el movimiento conserva el comportamiento. AUDIT marca FAIL solo si el bloque está en un rol o slot equivocado y moverlo no cambia comportamiento: un `useEffect` arriba de un `useState`, un write arriba de un guard que no lo lee, un `return` en medio de los hooks. El límite dudoso queda GAP.
