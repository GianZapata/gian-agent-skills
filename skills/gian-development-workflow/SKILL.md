---
name: gian-development-workflow
description: "Router de proceso de desarrollo personal de Gian: clasifica la tarea (feature grande, feature clara multi-step, decisión, bug, trivial, fuera de scope) y decide qué skills de proceso usar (brainstorming, grill-me, writing-plans, systematic-debugging, caveman) y en qué orden, delegando en ellas. NO contiene reglas de código: carga gian-how-i-code como policy cuando la tarea es de desarrollo. Usar cuando se pida diseñar, planificar, implementar, depurar o auditar dentro del workflow de Gian, o decidir qué proceso seguir; cargarla ANTES de tomar decisiones de proceso."
---

# Gian Development Workflow

Router de proceso: decide CÓMO resolver la tarea (qué skills de proceso, en qué orden). NO decide cómo debe quedar el código — eso es `gian-how-i-code` (policy), que este router carga cuando aplica.

## Autoridad

1. Instrucción explícita del usuario (siempre gana).
2. Contratos ejecutables del repo (tests, schemas, versiones reales).
3. `gian-how-i-code` (policy de código).
4. Convenciones locales.
5. Proceso genérico (Superpowers u otras skills de proceso).

## Activación

Cargar cuando la tarea sea de desarrollo dentro del scope de `gian-how-i-code` (PHP, Laravel, React, TypeScript, features, refactors, migraciones, auditorías, contratos API, forms, queries/mutations, tablas, dialogs/drawers, arquitectura) o haya duda sobre qué proceso seguir.

Si la tarea crea, edita, audita o corrige PHP: cargar también `gian-php-style` (formato visual; no duplicar esas reglas aquí). WRITE del hunk. **No correr Pint.** Laravel Boost `pint/core` queda anulado. Los planes no dicen “Pint al final”.

Si la tarea crea o modifica `.ts`/`.tsx` (incl. una feature normal, no solo “format this TS”): **HARD** cargar `gian-react-ts-style` y aplicarla en WRITE sobre código nuevo y el **hunk/función tocada** (SAFE FIX de inconsistencias de ese alcance). No migrar el archivo/repo. Si una corrección puede cambiar semántica: no aplicar; registrar GAP. AUDIT no edita. No duplicar esas reglas aquí.

No cargar para: preguntas generales, Git, Docker/infra pura, textos, debugging ajeno al scope.

## Clasificación de tarea

| Tipo | Señales | Cadena |
|---|---|---|
| Feature grande / cambio de comportamiento | "diseña", "nuevo sistema", "nuevo flujo", requisitos ambiguos, alternativas materiales | policy → brainstorming → (grill solo si decisiones materiales abiertas) → writing-plans → Build |
| Feature clara multi-step | requisitos definidos, múltiples archivos, plan útil | policy → (brainstorming mínimo solo si aporta) → writing-plans → Build |
| Decisión arquitectónica | "decide entre X/Y", tradeoff material, impacto duradero | brainstorming → UN grill (grill-me por defecto; grill-with-docs solo si la decisión amerita ADR) → plan si aplica |
| Bug | fallo, test rojo, 500, error reproducible | policy → systematic-debugging → fix + test |
| Trivial | typo, rename, validación pequeña, cambio mecánico localizado | policy → implementación directa → validación |
| Fuera de scope | Git, infra pura, textos, preguntas generales | nada (ni policy) |

## Bypass (anti-sobreingeniería)

- Bug → NO brainstorming, NO grill, NO writing-plans.
- Trivial → NO brainstorming, NO grill, NO writing-plans, NO systematic-debugging.
- Plan aprobado → NO rediseñar: ejecutar.
- Grill → elegir exactamente una (`grill-me` o `grill-with-docs`); nunca encadenar ambas.
- Plan desde un reporte de auditoría ya existente → `writing-plans`; no re-auditar; el reporte es fuente de verdad.

## Plan (agente plan)

clasificar → cargar policy si desarrollo → brainstorming si aplica → grill si decisiones materiales → writing-plans si multi-step → entregar plan + estado de aprobación. Read-only siempre. Si el plan incluye snippets PHP: siguen `gian-php-style` (no PHPDoc; un parámetro en una línea). Si incluye snippets TS/TSX: siguen `gian-react-ts-style`. No duplicar esas specs aquí. **No incluir Pint como paso final** (Boost `pint/core` queda anulado).

## Build (agente build)

consumir plan aprobado (o alcance aprobado) → cargar policy → Fase 0 + references según routing (lazy) → si toca PHP, WRITE `gian-php-style` en el hunk (**no Pint**) → si toca `.ts`/`.tsx`, WRITE `gian-react-ts-style` en el hunk (HARD; no format-only) → ejecutar por tareas/lotes con todowrite → validaciones reales del repo → revisión independiente según riesgo → cierre con evidencia. Sin plan, o tarea trivial/bug → routing proporcional de esta skill.

## Precedencia y fallback

Este router DELEGA: no reescribe contenido de las process skills ni de la policy. Si una process skill no está disponible o falla, degradar al siguiente nivel (sin writing-plans → lotes con todowrite; sin brainstorming → preguntas directas al usuario). Si `gian-how-i-code` no está disponible, continuar el proceso y señalarlo en el cierre.

## Caveman

Activación manual por trigger del usuario ("caveman", "be brief", "menos tokens"). Aplica a conversación, progress updates, explicaciones y cierres. NO aplica a artefactos: implementation plans, specs, auditorías, reportes técnicos, ADRs, código, errores o temas de seguridad.

## Capacidades futuras (no default)

- `executing-plans`: ejecución con checkpoints en sesión separada — evaluación separada.
- `subagent-driven-development`: ejecución multiagente — evaluación separada (mapping `general` verificado en spike 2026-08-11); actualmente deny en Plan/Build.

## References

- `references/style-activation.md`
