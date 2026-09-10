# 13 — Data fetching (TanStack React Query)

Cargar cuando: services, hooks query/mutation, query keys, invalidación, opciones de caché.

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

### Hook de mutation (regla)

1. Crear **siempre** una interface que extiende `UseMutationOptions<TData, TError, TVariables>` (genéricos ahí).
2. `TVariables` / DTO = tipo inferido del Zod schema (`10`), no una `interface XxxInput` paralela.
3. El hook recibe `options?: ThatInterface`.
4. Dentro: **solo** `mutationFn` + `...options`. No hardcodear `onSuccess` / `onError` / invalidate en el hook.

```ts
interface UseCreateEntityMutationOptions extends UseMutationOptions<
  MutationResponse<Entity>,
  CustomError,
  EntityDto // z.infer<typeof entitySchema>
> {}

export const useCreateEntity = (
  options?: UseCreateEntityMutationOptions,
) =>
  useMutation({
    mutationFn: EntityService.create,
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

**Anti-patrones del hook:** meter `onSuccess`/`onError` fijos dentro del hook; tipar la mutation solo con un `Props` genérico sin extender `UseMutationOptions<…>`.

## 5. Services

```ts
export class EntityService extends SharedService {
  static findAll = async (
    options: EntityParams,
    signal?: AbortSignal,
  ) =>
    SharedService.findAll(apiFetcher, '/entities', options, { signal });
  // ADAPTAR: si SharedService/fetcher usa otra firma, reenviar signal igual
  // mutaciones: try/catch + ErrorMapper.throwMappedError
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

- [ ] Variables del `queryFn` están en la key
- [ ] QueryClient central reutilizado (no uno por feature)
- [ ] Query: interface `*QueryProps` con `Omit<UseQueryOptions…, 'queryKey' | 'queryFn'>`
- [ ] Mutation: interface `Use*MutationOptions` + solo `mutationFn` en el hook; toast/invalidate en el caller
- [ ] `TVariables` desde Zod (`z.infer`), no interface Input paralela
- [ ] Invalidación vía store (`_def` / `queryKey`), no strings
- [ ] Params tipados y normalizados
- [ ] Sin duplicar server state fuera de Query
- [ ] PROP de ESLint Query solo con evidencia
