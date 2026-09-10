# 17 — Testing y validación

Cargar cuando: cerrar Implementar / Aplicar.

## Principio

Usar **comandos del repo** (AGENTS local de validación). No imponer comandos de otro producto.

## Patrones frecuentes

| Área | Ejemplo |
|------|---------|
| Frontend con Bun | `bun run lint` desde la app frontend; i18n es↔en si aplica |
| Backend Laravel | tests focalizados + analyse (PHPStan/Psalm) según política |
| No | Suite completa automática en cada nit; `tsc` si el repo lo prohíbe |

## Autoría de tests

Crear/actualizar cuando cambie comportamiento observable, contrato, SM, validación, bug.  
No obligar tests artificiales en docs/audit-only.

## Al aplicar migración

Tras cada lote: validación focalizada. Al final: analyse/lint según alcance FE/BE.
