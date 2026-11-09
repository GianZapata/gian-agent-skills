# 17 — Testing y validación

Cargar cuando: cerrar Implementar / Aplicar.

## Principio

Usar **comandos del repo** (AGENTS local de validación). No imponer comandos de otro producto.

Si el repo no documenta comandos: leer los scripts de `package.json`, `composer.json` y `pyproject.toml`, y correr lint, typecheck y tests focalizados. Si no existe ninguno, el cierre lo dice así: «el repo no tiene comandos de lint, typecheck ni tests».

Cada validación se reporta en el cierre con el comando y su resultado (`21`). Solo valen dos motivos para no correr un comando: «el repo no tiene el comando» o «falla por causa ajena al cambio», con la salida citada.

## El test runner no es un modo de producto

PHPUnit, Pest, Vitest, Jest y `npm run dev` ejecutan la lógica oficial. No crean una UI de "Test mode" ni un mensaje de validación distinto.

Al tocar un archivo de producto que anuncia el runner o el entorno: borrar ese código. No borrar la suite que protege un requisito. Un test no es un chip.

## Patrones frecuentes

| Área | Ejemplo |
|------|---------|
| Frontend con Bun | `bun run lint` desde la app frontend; paridad de todos los locales al tocar locales (`15`) |
| Frontend TS (cualquier stack) | Typecheck obligatorio: `tsc --noEmit`, `vue-tsc --noEmit` o el script del repo |
| Backend Laravel | Tests focalizados + PHPStan/Psalm sobre los archivos tocados si el repo los tiene configurados |
| Backend Python | `ruff check` y `pytest` focalizados, con el runner del repo (`uv run` si existe) |
| Angular | `ng` o `nx` lint/test del repo |
| No | Suite completa automática en cada nit; `tsc` si el repo lo prohíbe |

## Autoría de tests

Los tests protegen requisitos, no la implementación. Crear o actualizar un test es obligatorio ante:

- comportamiento nuevo (feature, endpoint);
- cambio de contrato;
- máquina de estados;
- validación;
- autorización o permisos;
- scoping de tenant (`16`);
- un bug.

Al eliminar, se decide por el requisito:

- El requisito desaparece: se borra el código y sus tests exclusivos. No se agrega un test que diga "esto ya no existe".
- Cambia la implementación y el requisito sigue: se conservan o adaptan los tests de ese comportamiento.
- La eliminación crea una garantía vigente (dejar de enviar un dato sensible): se prueba esa garantía, en términos del comportamiento.

Limpieza completa en el mismo cambio: tests exclusivos, fixtures, mocks, factories y referencias que quedaron sin uso. La cobertura sigue a los requisitos que quedan.

Al quitar un helper de formato, se borran sus tests. Si el valor que formateaba debe seguir llegando completo y sin redondeo, se conserva la prueba de eso.

No obligar tests artificiales en docs/audit-only.

## Al aplicar migración

Tras cada lote: validación focalizada. Al final: lint y typecheck de cada lado tocado (FE, BE o ambos), más PHPStan/Psalm si el repo los tiene configurados. El cierre registra cada comando y su resultado.
