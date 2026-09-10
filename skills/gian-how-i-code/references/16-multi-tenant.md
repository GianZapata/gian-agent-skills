# 16 — Multi-tenant (opcional)

Cargar cuando: tenancy, central vs tenant, stancl, fetchers por scope.

## Cuándo aplica

Solo si el repo tiene tenancy o el usuario lo pide. No asumir en apps single-tenant.

## Modelo típico

- **Central DB:** identidad, catálogo compartido, metadata canónica, pagos de plataforma
- **Tenant DB:** operación diaria del tenant
- IDs snapshot (`central_*_id`); Central gana en divergencia canónica
- Prohibido: relaciones Eloquent cross-DB; FKs entre central y tenant

## Frontend

- Fetchers distintos por scope (central vs tenant vs Sanctum)
- Contextos en código/namespaces: Central | Shared | Tenant

## Checklist

- [ ] Pieza nueva declara contexto
- [ ] Fetcher correcto
- [ ] No filtrar autoridad canónica al tenant
