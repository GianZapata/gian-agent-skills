# 00 — Índice del estándar

Cargar cuando: arranque humano, modo Consultar, orientación general.

| # | Archivo | Tema |
|---|---------|------|
| 01 | `01-principles.md` | Principios; núcleo y adaptador (el lenguaje no apaga el estándar); filas por stack (Laravel, Python, Node) |
| 02 | `02-repository-discovery.md` | Fase 0 |
| 03 | `03-feature-mold.md` | Molde de carpetas FE; checklist núcleo y adaptador React |
| 04 | `04-frontend-architecture.md` | Naming (núcleo); arquitectura FE y styling MUI+Tailwind (adaptador React) |
| 05 | `05-backend-mold.md` | Molde Laravel (adaptador); FormRequest `rules`/`messages`/`attributes` |
| 06 | `06-api-contracts.md` | Contratos HTTP; whenLoaded → Resource ctor (adaptador Laravel) |
| 07 | `07-types-enums-statuses.md` | Enums, ownership, membresía includes / in_array / in |
| 08 | `08-display-conventions.md` | Display inline **o** `static readonly Record` con labels dinámicos en helper |
| 09 | `09-dialogs-drawers.md` | Diálogos / drawers; dueño de mutación; montaje condicional |
| 10 | `10-forms-validation.md` | Forms; DTO = schema nombrado del body; tipo semántico del campo; 422 por campo; adaptador RHF+Zod |
| 11 | `11-tables-filters.md` | Tablas y filtros |
| 12 | `12-state-management.md` | Estado cliente |
| 13 | `13-data-fetching.md` | Data fetching: núcleo ruta ≠ body; adaptador TanStack Query (keys, TVariables) |
| 14 | `14-errors-feedback.md` | Errores, cliente HTTP compartido y toasts |
| 15 | `15-i18n-copy.md` | i18n y copy |
| 16 | `16-multi-tenant.md` | Multi-tenant |
| 17 | `17-testing-validation.md` | Validación |
| 18 | `18-migrate-audit.md` | Auditoría / migración |
| 19 | `19-propuestas-stack.md` | Evaluación de mejoras de stack |
| 20 | `20-variants.md` | Variantes técnicas |
| 21 | `21-output-contracts.md` | Formatos de salida |
| 22 | `22-design-quality.md` | Traits, SOLID operacional, Clean Code |
| 23 | `23-ts-style-helpers.md` | cn, dayjs, memoización A–E, utils vs helpers, FormDataHelper |
| 24 | `24-full-repo-audit.md` | Auditar repositorio completo (coverage ledger / gate) |
| 25 | `25-vue-sfc.md` | Delta Vue: script setup inline, `Props` / `Emits`, `defineModel`, overlays con `v-if`, `composables/`. No reemplaza el núcleo |

Formato visual PHP: skill `gian-php-style`. Formato visual TS/TSX: skill `gian-ts-style`. Ninguno es un capítulo de esta skill.
