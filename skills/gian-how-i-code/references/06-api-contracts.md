# 06 — Contratos API

Cargar cuando: Resource↔TS, envelopes, QueryBuilder, Form Requests, anti-patrones de contrato.

## Principio

El frontend **refleja** el contrato; no lo adivina. Interfaces = JSON del Resource. DTOs mutación = Form Requests.

## Shapes conceptuales

```ts
type ReadResponse<T> = T | { data: T };
type PaginationResponse<T> = { data: T[]; meta?: unknown; links?: unknown };
type MutationResponse<T> = { message: string; data: T };
```

Adaptar a convención del proyecto; ser consistente (unwrap vs envelope).

| Endpoint | Backend | Response típica |
|----------|---------|-----------------|
| GET collection | Query + Resource collection | PaginationResponse si pagina |
| GET show | Query detail + Resource | ReadResponse |
| POST | StoreRequest + Action + Resource | MutationResponse 201 |
| PUT/PATCH | UpdateRequest + Action + Resource | MutationResponse 200 |
| DELETE | DeleteAction | Según política proyecto (204 / message / id) |

## QueryBuilder

- `AllowedInclude` / `AllowedFilter` / `AllowedSort` explícitos
- Params FE = allowlists reales
- Counts: `withCount` forzado si filtra/ordena; include count si solo display opcional

## Resources

- `whenLoaded()` → campo opcional/nullable en TS
- Relación → Resource (HARD): pasar `whenLoaded` al constructor (Laravel omite si es `MissingValue`). Colección: `::collection($this->whenLoaded('rels'))`.
- No inventar datos ni fallbacks mentirosos (`code ?? \`X-${id}\``)
- No exponer `pivot` crudo; aplanar campos documentados
- Clasificar relaciones: public_api / internal / sensitive

```php
'city' => new CityResource($this->whenLoaded('city')),
'items' => ItemResource::collection($this->whenLoaded('items')),
```

No:

```php
'client' => $this->whenLoaded(
    'client',
    fn() => new ClientResource($this->client)
),
```

KEEP el callback si hay lógica extra (recurso distinto, default, map). KEEP `whenLoaded()` sin Resource (escalar).

AUDIT: FAIL. WRITE/FIX: SAFE en el Resource tocado; no barrer el repo.

## Anti-patrones

- Campos inventados en FE o Resource
- `any` en responses/DTOs
- Includes no permitidos usados como si existieran
- Recalcular en FE lo que debe ir en Resource
- Relaciones cross-DB en multi-tenant

## Params de lectura

```ts
export interface EntityParams {
  include?: Array<'…'>;
  filter?: { … };
  sort?: Array<'…'>;
  page?: number;
  perPage?: number;
}
```

## Cadena a validar

```text
Route → Controller → FormRequest → Action/Query → Resource
→ interface/DTO → service → hook → query key / invalidation
```
