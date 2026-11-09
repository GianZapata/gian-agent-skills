# 16 — Multi-tenant (obligatorio si el repo tiene tenancy)

Cargar cuando: tenancy, central vs tenant, stancl, fetchers por scope.

## Cuándo aplica

Solo si el repo tiene tenancy o el usuario lo pide. No asumir en apps single-tenant. Si el repo tiene tenancy, todo este archivo es HARD.

## Reglas (HARD con tenancy)

- **Central DB:** identidad, catálogo compartido, metadata canónica, pagos de plataforma
- **Tenant DB:** operación diaria del tenant
- IDs snapshot (`central_*_id`); Central gana en divergencia canónica
- Prohibido: relaciones Eloquent cross-DB; FKs entre central y tenant

## Frontend

- Fetchers distintos por scope (central vs tenant vs Sanctum)
- Cada pieza nueva vive en un namespace o carpeta de contexto: Central | Shared | Tenant

## Checklist

- [ ] Pieza nueva declara contexto
- [ ] Fetcher correcto
- [ ] No filtrar autoridad canónica al tenant
- [ ] Jobs y colas inicializan el tenant antes de leer o escribir
- [ ] Keys de caché y paths de storage llevan el tenant
- [ ] Tests cubren cada contexto tocado (Central, Shared, Tenant)
