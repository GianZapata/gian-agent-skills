# 13 — Data fetching: núcleo ruta ≠ body; adaptador TanStack Query

Cargar cuando: services, hooks query/mutation, query keys, invalidación, opciones de caché, IDs de ruta vs DTO, `TVariables`.

## Alcance

- **Núcleo:** ruta ≠ body, firmas del service `(id, data)` o `(params, data)`, y el DTO sale de un schema nombrado. No invalidar sin filtro. La UI no arma `FormData`. La cancelación es la del stack: `AbortSignal`, o `takeUntilDestroyed`/unsubscribe en RxJS. Vale aunque el cliente de datos no sea React Query.
- **Adaptador React:** QueryClient, query-key-factory, `useQuery` / `useMutation`, el envelope `*Variables` (§4) y el resto de este archivo. El envelope existe en React Query o Vue Query; no es núcleo.

## 1. Responsabilidad

| Tipo | Herramienta |
|------|-------------|
| Server state | TanStack React Query |
| UI local | `useState` / URL |
| Form | RHF |
| Global cliente no-servidor | Solo si justificado (auth session UI, tema) |

No duplicar en Zustand/Context datos que ya están (o deberían estar) en la caché de Query.

## 1b. QueryClient (defaults canónicos)

Reutilizar el **cliente central** del repo (`getQueryClient` / provider único). No crear `new QueryClient()` por feature.

Defaults orientativos (adaptar al proyecto si ya difieren de forma consciente):

| Opción | Default sugerido |
|--------|------------------|
| `refetchOnWindowFocus` | `false` |
| `mutations.retry` | `false` |
| `queries.retry` | no reintentar 4xx / 401 (usar `ErrorMapper` para clasificar) |
| `staleTime` | corto (p. ej. ~30s) salvo catálogos |

Si falta un QueryClient compartido o cada ruta instancia el suyo → Hallazgo / PROP de abstracción (`19`).

## 2. Query keys — reglas canónicas

Las keys deben ser:

- **arrays** en el nivel superior;
- **deterministas** y **serializables** (`JSON.stringify`-safe);
- **semánticamente únicas** para los datos consultados;
- **estables** (mismo input → misma key);
- **completas**: toda variable usada por el `queryFn` que cambie el resultado va en la key;
- **jerárquicas** para invalidación dirigida.

### Organización (default del estándar)

**Store central** con `@lukemorales/query-key-factory` + `mergeQueryKeys` (p. ej. `lib/query-keys.ts`).

```ts
queries.entities.list(options).queryKey
queries.entities.list._def          // todas las variantes de list
queries.entities.detail(id).queryKey
queries.entities._def               // dominio completo
```

- No keys preventivas
- No strings sueltos en `invalidateQueries`
- Hooks no inventan keys ad-hoc si el store central existe

**Variante de escala (híbrida):** cada feature declara keys y un índice las combina con `mergeQueryKeys`. Usar solo si el store central se vuelve inmantenible; documentar en el reporte.

**No default:** un archivo `*.keys.ts` por feature sin índice común (dificulta invalidación cross-feature).

### Forma de list / detail

```ts
// Preferir Params tipados por feature — no Record<string, unknown> | object
// EntityId: un solo tipo por feature (default number; string si UUID)
type EntityId = number;

list: (params?: EntityListParams) => ({
  queryKey: [normalizeListParams(params)],
}),
detail: (id: EntityId, params?: EntityDetailParams) => ({
  queryKey: params ? [id, params] : [id],
}),
```

**Normalización:** `list()` y `list({})` no deben producir keys distintas si significan “sin filtros”. Normalizar params vacíos antes de armar la key.

**Anti-patrón / workaround a evitar como default:**

```ts
type EntityParams = Record<string, unknown> | object; // tipado inútil
const emptyEntityListKey = [] as unknown as [EntityParams];
queryKey: params ? [params] : emptyEntityListKey
```

Ese patrón intenta satisfacer firmas de tuplas de query-key-factory. Antes de copiarlo:

1. Verificar versión instalada de `@lukemorales/query-key-factory`.
2. Preferir definición estática (`list: null`) cuando no hay params.
3. O normalizar siempre a un objeto serializable.
4. Tipar `Params` por feature, no un union abierto.

**Ids:** elegir `string` **o** `number` de forma consistente con el contrato API. No usar `string | number` en firmas materializadas; el template usa `type EntityId = number` por defecto (cambiar a `string` si el contrato es UUID).

## 3. Queries

Siempre crear una **interface de props** que extiende `Omit<UseQueryOptions<…>, 'queryKey' | 'queryFn'>` y añade los params de la feature. El hook fija `queryKey` / `queryFn` y hace `...rest`.

```ts
export interface EntitiesQueryProps extends Omit<
  UseQueryOptions<PaginationResponse<Entity>, CustomError>,
  'queryKey' | 'queryFn'
> {
  options?: EntityListParams;
}

export const useEntitiesQuery = ({
  options = {},
  ...rest
}: EntitiesQueryProps) =>
  useQuery({
    queryKey: queries.entities.list(options).queryKey,
    queryFn: ({ signal }) => EntityService.findAll(options, signal),
    placeholderData: keepPreviousData, // si aplica
    ...rest,
  });
```

Error: `CustomError` (o el del proyecto).

### Cuándo evaluar opciones

| Opción | Cuándo |
|--------|--------|
| `enabled` | Dependencias seriales (id/padre aún no listo) |
| `staleTime` / `gcTime` | Catálogos poco variables |
| `select` | Derivar vista sin otra query |
| `placeholderData` / `initialData` | Transiciones de lista sin flash |
| `retry` | Redes flaky; no en 4xx de negocio |
| `AbortSignal` | Cancelar fetch al desmontar / key change — reenviar al service/fetcher |
| `queryOptions` / prefetch | Loaders, rutas, reutilizar la misma definición |
| Infinite | Listas cursor/page infinitas reales |

No imponer todas las opciones en cada query.

## 4. Mutations e invalidación

### Separación ruta vs DTO (HARD)

Los identificadores de la URL no se mezclan con el payload. Un objeto plano `{ parentId, id, body }` contamina capas: `parentId`/`id` son contexto de ruta; `body` es el DTO.

**Service**

| IDs de ruta | Firma |
|-------------|--------|
| 0 (colección, create raíz) | `(data: TDto)` |
| 1 | `(id: EntityId, data: TDto)` |
| 2+ | `(params: { parentId: EntityId; id: EntityId }, data: TDto)` |
| Acción sin body (delete / cancel / send) | `(id: EntityId)` |

```ts
static updateNested = async (
  params: { parentId: EntityId; id: EntityId },
  data: UpdateNestedDto,
): Promise<MutationResponse<Entity>> => {
  try {
    const response = await apiFetcher.patch<MutationResponse<Entity>>(
      `/parents/${params.parentId}/entities/${params.id}`,
      data,
    );

    return response.data;
  } catch (error) {
    ErrorMapper.throwMappedError(error);
  }
};

static registerPayment = async (
  paymentId: EntityId,
  data: RegisterPaymentDto,
): Promise<MutationResponse<Payment>> => {
  try {
    const response = await apiFetcher.post(
      `/payments/${paymentId}/register`,
      FormDataHelper.toFormData(data),
    );

    return response.data;
  } catch (error) {
    ErrorMapper.throwMappedError(error);
  }
};
```

`FormDataHelper` solo si el endpoint es multipart (`23`). JSON usa el objeto `data` tal cual.

**`TVariables` (React Query)** — el DTO sigue saliendo de Zod (`10`). El envelope **no** es un DTO: se nombra `*Variables`, no `*Dto` / `*Input`.

| Cuándo se conocen los IDs | Hook | `TVariables` | `mutate` |
|---------------------------|------|--------------|----------|
| Acción sin body | `useDeleteEntity()` | `EntityId` | `mutate(id)` |
| 1 ID conocido al llamar el hook (dialog de un registro) | `useRegisterPayment(paymentId)` | `RegisterPaymentDto` | `mutate(data)` |
| 1 ID solo en mutate-time (p. ej. tras un create) | `usePrepareChild()` | `{ parentId: EntityId; data: PrepareChildDto }` | `mutate({ parentId, data })` |
| 2+ IDs | `useUpdateNested()` | `{ params: { parentId: EntityId; id: EntityId }; data: UpdateNestedDto }` | `mutate({ params, data })` |

Prohibido: `{ parentId, id, body }` / meter path params dentro del schema Zod. `params` en el envelope **solo** si hay 2+ IDs.

**Genéricos:** declarar siempre `useMutation<TData, CustomError, TVariables>`. `TError` = `CustomError` (o el del repo).

### Hook de mutation (regla)

1. Crear **siempre** una interface que extiende `UseMutationOptions<TData, TError, TVariables>` (genéricos ahí).
2. El **DTO** (`data`) = `z.infer` del schema (`10`). `TVariables` es ese DTO **o** el envelope de la tabla de §4 (nunca un `*Input` paralelo ni un híbrido ruta+body).
3. El hook recibe `options?: ThatInterface`.
4. Dentro: **solo** `mutationFn` + `...options`. No hardcodear `onSuccess` / `onError` / invalidate en el hook.

```ts
interface UseCreateEntityMutationOptions extends UseMutationOptions<
  MutationResponse<Entity>,
  CustomError,
  EntityDto
> {}

export const useCreateEntity = (
  options?: UseCreateEntityMutationOptions,
) =>
  useMutation<MutationResponse<Entity>, CustomError, EntityDto>({
    mutationFn: EntityService.create,
    ...options,
  });

export interface UpdateNestedVariables {
  params: { parentId: EntityId; id: EntityId };
  data: UpdateNestedDto;
}

interface UseUpdateNestedMutationOptions extends UseMutationOptions<
  MutationResponse<Entity>,
  CustomError,
  UpdateNestedVariables
> {}

export const useUpdateNested = (
  options?: UseUpdateNestedMutationOptions,
) =>
  useMutation<MutationResponse<Entity>, CustomError, UpdateNestedVariables>({
    mutationFn: ({ params, data }) => EntityService.updateNested(params, data),
    ...options,
  });

export const useRegisterPayment = (
  paymentId: EntityId,
  options?: UseMutationOptions<
    MutationResponse<Payment>,
    CustomError,
    RegisterPaymentDto
  >,
) =>
  useMutation<MutationResponse<Payment>, CustomError, RegisterPaymentDto>({
    mutationFn: (data) => EntityService.registerPayment(paymentId, data),
    ...options,
  });
```

### Caller (diálogo / página dueña)

Ahí van toast + invalidate:

```ts
const { mutate } = useCreateEntity({
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: queries.entities.list._def });
  },
  onError: (error) => {
    toast.error(ErrorMapper.getTranslatedMessage(error));
  },
});
```

```ts
queryClient.invalidateQueries({ queryKey: queries.entities.list._def });
queryClient.invalidateQueries({ queryKey: queries.entities.detail(id).queryKey });
// todos los detalles: queries.entities.detail._def
```

| Acción | Invalidación típica |
|--------|---------------------|
| create | `list._def` (+ métricas) |
| update | `detail(id).queryKey` + `list._def` |
| delete | `list._def` + remove/`detail._def` según caso |
| acción de dominio | keys de datos realmente afectados (puede ser cross-feature) |

**Prohibido como default:** `queryClient.invalidateQueries()` sin filtro.

**`setQueryData` / optimistic:** solo cuando UX lo exige y hay rollback claro; no convertir toda mutation en optimistic.

**Anti-patrones del hook:** meter `onSuccess`/`onError` fijos dentro del hook; tipar la mutation solo con un `Props` genérico sin extender `UseMutationOptions<…>`; aplanar IDs de ruta con campos del body; `TVariables` anónimo `{ body: string }`.

## 5. Services

```ts
export class EntityService extends SharedService {
  static findAll = async (
    options: EntityParams,
    signal?: AbortSignal,
  ) =>
    SharedService.findAll(apiFetcher, '/entities', options, { signal });
  // ADAPTAR: si SharedService/fetcher usa otra firma, reenviar signal igual
  // mutaciones: try/catch + ErrorMapper.throwMappedError; firmas §4
}
```

Variante: clase static + fetcher por scope (central/tenant) — ver `20`.

## 6. Linting y herramientas (como PROP, no auto-install)

Evaluar `@tanstack/eslint-plugin-query` si:

- TanStack Query ya está en el repo;
- el plugin **no** está instalado;
- hay evidencia de keys incompletas / QueryClient inestable / deps omitidas.

Reglas útiles: exhaustive-deps, stable-query-client, no-unstable-deps, prefer-query-options (según docs oficiales de la versión del repo).

Devtools: útil en dev; no es dependencia de producción obligatoria.

## 7. Checklist rápido

### Núcleo (cualquier stack)

- [ ] DTO desde un schema nombrado; no interface Input paralela (`10`)
- [ ] Ruta ≠ body: service `(id, data)` o `(params, data)` (§4)
- [ ] Multipart: service llama `FormDataHelper`; UI no arma FormData (`23`/`09`)
- [ ] Invalidación dirigida; nunca sin filtro
- [ ] Params tipados y normalizados
- [ ] Sin duplicar server state en un store de UI
- [ ] Cancelación del stack reenviada al service (`AbortSignal`, o `takeUntilDestroyed`/unsubscribe)

### Adaptador React

- [ ] Variables del `queryFn` están en la key
- [ ] QueryClient central reutilizado (no uno por feature)
- [ ] Query: interface `*QueryProps` con `Omit<UseQueryOptions…, 'queryKey' | 'queryFn'>`
- [ ] Mutation: interface `Use*MutationOptions` + solo `mutationFn` en el hook; toast/invalidate en el caller
- [ ] DTO con `z.infer`; `TVariables` = DTO o envelope `*Variables` según la tabla de §4
- [ ] `useMutation<TData, CustomError, TVariables>` con los 3 genéricos
- [ ] Invalidación vía store (`_def` / `queryKey`), no strings
- [ ] PROP de ESLint Query solo con evidencia
