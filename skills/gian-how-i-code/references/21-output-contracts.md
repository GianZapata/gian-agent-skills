# 21 — Contratos de salida

Cargar cuando: cerrar un modo; formato de reportes.

## Implementar

- Lista de archivos creados/modificados
- Checklist molde FE/BE
- Propuestas abiertas (PROP) si las hay
- Validación ejecutada o motivo
- Si toca formularios o validación user-facing: no declarar done sin el completion gate de `05` (`rules` / `messages` / copy / cobertura semántica / attributes si aplica / 422 BE / consumo FE)

## Auditar — feature / módulo

- Un solo archivo: `pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md`
- Español: Contexto, Resumen, Hallazgos, Propuestas, Lotes
- Sin cambios de código
- Sin carpetas multi-archivo por feature

## Auditar — repositorio completo

- Mismo path canónico (`…-repo-auditoria.md` o `<alcance>=repo`)
- Protocolo `24`: inventario, matriz variante, tabla por feature, categorías sin hallazgos con evidencia, registro de búsquedas, Gate, disposición
- Auxiliar opcional: `pattern-audit/YYYY-MM-DD-<alcance>-coverage-ledger.md`
- **Prohibido** concluir “altamente alineado” / cierre completo sin Gate
- **Prohibido** muestreo de pocas features como auditoría completa
- Sin cuota mínima de hallazgos
- PROP con costos/riesgos reales (`19`)

## Auditar + aplicar

- El **mismo** archivo, actualizado
- Secciones Checklist de aplicación + Registro de implementación dentro del archivo
- Validación por lote documentada en §6

## Consultar estándar

- Respuesta en español
- Etiqueta: Regla | Default | Variante | Excepción | Propuesta
- Cita: `references/<archivo>.md` y sección

## Compatible con writing-plans

El único `pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md` es fuente válida para `writing-plans` (no re-auditar). El coverage-ledger es soporte, no reemplazo del reporte.
