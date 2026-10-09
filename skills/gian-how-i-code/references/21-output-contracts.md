# 21 — Contratos de salida

Cargar cuando: cerrar un modo; formato de reportes.

## Implementar

- Lista de archivos creados/modificados
- Checklist molde FE/BE
- Propuestas abiertas (PROP) si las hay
- Si se partió de una referencia o un plan: *Sin datos todavía* con `archivo:línea` de cada `TODO(datos)` (desde `rg`), y *Texto de la referencia que no publiqué* (original → qué se hizo). Va aunque nadie lo pida. Si no hubo casos, no se agrega (`15`)
- Validación ejecutada o motivo
- Si toca formularios o validación user-facing: no declarar done sin el completion gate de `05` (`rules` / `messages` / copy / cobertura semántica / attributes si aplica / 422 BE / consumo FE)

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
