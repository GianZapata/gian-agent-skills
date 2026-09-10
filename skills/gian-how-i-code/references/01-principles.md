# 01 — Principios

Cargar cuando: arranque, conflicto de reglas, modo Consultar sobre “por qué”.

## Reglas de oro

1. **El molde canónico** define la estructura objetivo para features frontend, backend, contratos, formularios, consultas y mutaciones. Usar features CRUD maduras del propio repo como ejemplos de referencia.
2. **Una fuente tipada de verdad** para estados/tipos cerrados (TS string enum `APP_OWNED`; PHP backed Enum o constantes en State Machine string-based — ver `07`). Ownership antes de declarar el contrato.
3. **Negocio en backend Resource/Action**, no recalcular flags en el frontend.
4. **Display inline** (cadena de `if`); no helpers de labels/colores. `useMemo` según `23` A–E (no ceremonial; multi-rama C sí).
5. **Diálogo dueño** de mutación + invalidate; padre solo trigger + entidad + onClose.
6. **YAGNI + migración oportunista**: al tocar, alinear; no refactor masivo no pedido.
7. **Evaluación de mejoras de stack** antes de instalar; mala práctica ≠ “instala una lib”.
8. **dayjs + utils/helpers + memo + styling** (`23`/`04`): `cn()` para condicionales (estático sin `cn` OK); dayjs; utils chicos / helpers clase de área; memo A–E; Tailwind-first / no `*_SX` locales (`04`). Sintaxis TS/TSX → `gian-react-ts-style`.
9. **Formato PHP** no vive aquí: cargar `gian-php-style`. **Formato TS/TSX** no vive aquí: cargar `gian-react-ts-style` (WRITE/FIX corrigen el hunk; AUDIT no edita).

## Qué es obligatorio vs default vs variante

| Nivel | Significado |
|-------|------------|
| Regla | Incumplir = hallazgo Alto/Medio |
| Default | Preferir salvo evidencia de variante |
| Variante | Documentada (p. ej. Zustand para drawers) |
| Excepción | Legacy / OpenAPI generado / texto libre |

## Anti-objetivos

- No diluir esta skill como “notas” o índice de otros documentos.
- No reescribir un producto entero en un cambio pequeño.
- No inventar campos API ni `any` para tapar gaps.
