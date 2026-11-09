# 21 — Contratos de salida

Cargar cuando: cerrar un modo; formato de reportes.

## Implementar

Cierre obligatorio de toda implementación, también en bug y trivial. Sin este cierre la tarea no está terminada. Cada punto va siempre; si no hubo casos, el punto dice «ninguno».

1. **Archivos**: creados y modificados.
2. **References leídas**: cada `NN` de esta skill y cada skill de estilo cargada (`gian-ts-style`, `gian-php-style`), más `visual-quality.md` si hubo UI.
3. **Reglas aplicadas**: por reference, las reglas aplicadas en la unidad de `01` §Unidad que se alinea al tocar. Cada GAP con `archivo:línea` y su caso.
4. **Self-check de estilo**: por cada lenguaje tocado. TS: la salida de `node <ruta de gian-ts-style>/assets/self-check.mjs`, con su última línea tal cual (`Self-check TS: 0 pendientes` o GAP). PHP: `Self-check PHP: manual` y las reglas de gian-php-style revisadas en el método tocado (igual que gian-development-workflow §Self-check).
5. **Validación**: cada comando corrido con su resultado. Solo valen dos motivos para no correr uno: «el repo no tiene el comando» o «falla por causa ajena al cambio», con la salida citada. Falta de tiempo no es motivo.
6. **Funciones reordenadas** (`26`): cada función con `archivo:línea`, y cada GAP de orden con su motivo (efecto, lock, transacción, TDZ, hooks).
7. **PROP**: «PROP: ninguna» o la lista.
8. **Referencia o plan**: si se partió de uno, el bloque de `15` (*Sin datos todavía* / *Texto de la referencia que no publiqué*) con el `rg` corrido. Sin casos, cada lista dice «ninguno» y cita el `rg`.
9. **Copy cambiado** (`15`): cada texto visible corregido, original → nuevo. Cada coincidencia conservada como término de dominio, con `archivo:línea`.
10. **Campos de formulario** (`10`): por cada campo creado o editado, la ayuda evaluada, aplicada / propuesta / descartada, y el motivo en una línea.
11. **Formularios o validación user-facing**: el completion gate de `05` marcado punto por punto (`rules` / `messages` / copy / cobertura semántica / `attributes()` cuando un mensaje interpola `:attribute` con un nombre de columna o clave interna / 422 BE / consumo FE).
12. **Verificación visual**: con UI, los viewports capturados y cada contenedor visto (`visual-quality.md`), y lo que no se vio, nombrado. Sin UI: «sin UI».

Formato breve de ejemplo:

```text
Archivos: features/invoices/components/InvoiceDrawer.tsx, app/Actions/PayInvoice.php
References: 01, 03, 04, 09, 13, 26; gian-ts-style; gian-php-style; visual-quality.md
Reglas: 09 isOpen + entidad tipada (InvoiceDrawer.tsx:12); 13 ruta ≠ body (usePayInvoice.ts:8)
GAP: ninguno
Self-check TS: 0 pendientes
Self-check PHP: manual — brace-same-line, laravel-validation-rule-array (PayInvoice.php:18)
Validación: npm run typecheck → ok; npm run lint → ok; php artisan test --filter=PayInvoice → 4 passed
Reordenadas: InvoiceDrawer.tsx:20 (InvoiceDrawer)
PROP: ninguna
Referencia o plan: no se partió de uno
Copy: "Pago registrado correctamente!" → "Pago registrado" (es.json:41)
Campos: note — ayuda evaluada: contador de caracteres; descartada: el campo no tiene límite
Gate 05: rules ✔ messages ✔ attributes ✔ 422 ✔ consumo FE ✔
Visual: 375/768/1440, drawer abierto y cerrado; sin pendientes
```

## Auditar — feature / módulo

- Un solo archivo: `docs/pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md`, en la raíz git del repo auditado. Si el `.gitignore` de esa raíz no ignora `docs/pattern-audit/`, se agrega esa línea (`18`).
- Español: Contexto, Resumen, Hallazgos, Propuestas, Lotes
- Sin cambios de código
- Sin carpetas multi-archivo por feature

## Auditar — repositorio completo

- Mismo path canónico (`…-repo-auditoria.md` o `<alcance>=repo`)
- Protocolo `24`: inventario, matriz variante, tabla por feature, categorías sin hallazgos con evidencia, registro de búsquedas, Gate, disposición
- Auxiliar opcional: `docs/pattern-audit/YYYY-MM-DD-<alcance>-coverage-ledger.md`
- **Prohibido** concluir “altamente alineado” / cierre completo sin Gate
- **Prohibido** muestreo de pocas features como auditoría completa
- Sin cuota mínima de hallazgos
- PROP con costos/riesgos reales (`19`)

## Auditar + aplicar

- El **mismo** archivo, actualizado
- Secciones Checklist de aplicación + Registro de implementación dentro del archivo
- Validación por lote documentada en `18` §6

## Consultar estándar

- Respuesta en español
- Etiqueta: Regla | Default | Variante | Excepción | Propuesta
- Cita: `references/<archivo>.md` y sección

## Compatible con writing-plans

El único `docs/pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md` es fuente válida para `writing-plans` (no re-auditar). El coverage-ledger es soporte, no reemplazo del reporte.
