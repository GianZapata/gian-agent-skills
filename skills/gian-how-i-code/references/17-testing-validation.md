# 17 — Testing y validación

Cargar cuando: cerrar Implementar / Aplicar.

## Principio

Usar **comandos del repo** (AGENTS local de validación). No imponer comandos de otro producto.

## El test runner no es un modo de producto

PHPUnit, Pest, Vitest, Jest y `npm run dev` ejecutan la lógica oficial. No crean una UI de "Test mode" ni un mensaje de validación distinto.

Al tocar un archivo de producto que anuncia el runner o el entorno: borrar ese código. No borrar la suite que protege un requisito. Un test no es un chip.

## Patrones frecuentes

| Área | Ejemplo |
|------|---------|
| Frontend con Bun | `bun run lint` desde la app frontend; i18n es↔en si aplica |
| Backend Laravel | tests focalizados + analyse (PHPStan/Psalm) según política |
| Backend Python | `ruff check` y `pytest` focalizados, con el runner del repo (`uv run` si existe) |
| Angular | `ng` o `nx` lint/test del repo |
| No | Suite completa automática en cada nit; `tsc` si el repo lo prohíbe |

## Autoría de tests

Los tests protegen requisitos, no la implementación. Crear o actualizar un test cuando cambia un comportamiento que permanece: contrato, máquina de estados, validación o un bug.

Al eliminar, se decide por el requisito:

- El requisito desaparece: se borra el código y sus tests exclusivos. No se agrega un test que diga "esto ya no existe".
- Cambia la implementación y el requisito sigue: se conservan o adaptan los tests de ese comportamiento.
- La eliminación crea una garantía vigente (dejar de enviar un dato sensible): se prueba esa garantía, en términos del comportamiento.

Limpieza completa en el mismo cambio: tests exclusivos, fixtures, mocks, factories y referencias que quedaron sin uso. La cobertura sigue a los requisitos que quedan.

Al quitar un helper de formato, se borran sus tests. Si el valor que formateaba debe seguir llegando completo y sin redondeo, se conserva la prueba de eso.

No obligar tests artificiales en docs/audit-only.

## Al aplicar migración

Tras cada lote: validación focalizada. Al final: analyse/lint según alcance FE/BE.
