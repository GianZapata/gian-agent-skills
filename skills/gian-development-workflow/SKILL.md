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

Una puerta de esta skill gana a la skill de proceso que nombra, aunque esa skill ya esté cargada y diga MUST o siempre.

## Activación

Cargar cuando la tarea sea de desarrollo dentro del scope de `gian-how-i-code` (PHP, Laravel, React, Vue, Angular, Node, TypeScript, Python, features, refactors, migraciones, auditorías, contratos API, forms, queries/mutations, tablas, dialogs/drawers, arquitectura) o haya duda sobre qué proceso seguir.

La policy entera aplica en cualquier stack. Un capítulo de stack (`25` en Vue, y los que existan después) solo agrega el delta. No copiar reglas de SFC ni de núcleo aquí.

Si la tarea crea, edita, audita o corrige PHP: cargar también `gian-php-style` (formato visual; no duplicar esas reglas aquí). WRITE del hunk. **No correr Pint.** Laravel Boost `pint/core` queda anulado. Los planes no dicen “Pint al final”.

Si la tarea crea o modifica `.ts`/`.tsx`, el hermano `.ts` de un componente Vue o un `<script setup lang="ts">` inline (incl. una feature normal, no solo “format this TS”): **HARD** cargar `gian-ts-style` y aplicarla en WRITE sobre código nuevo y el **hunk/función tocada** (SAFE FIX de inconsistencias de ese alcance). No migrar el archivo/repo. Si una corrección puede cambiar semántica: no aplicar; registrar GAP. AUDIT no edita. No duplicar esas reglas aquí. `<template>` y `<style>` de un `.vue` y el `.html` de Angular no tienen skill de estilo Gian: se sigue el lint del repo.

Python: no hay skill de estilo Gian. Se sigue el Ruff o Black del repo. No se porta formato de PHP ni de TS.

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

- Bug → NO brainstorming, NO grill, NO writing-plans. Un fallo reproducible no se promociona a feature grande para cumplir el MUST de `brainstorming`.
- Trivial → NO brainstorming, NO grill, NO writing-plans, NO systematic-debugging.
- Plan aprobado → NO rediseñar: ejecutar.
- TDD no configurado → no cargar `test-driven-development`. `writing-plans` no escribe fase TDD ni "failing test first".
- `laravel-11-12-app-guidelines` no autoriza Pint. Gana `gian-php-style`.
- Grill → elegir exactamente una (`grill-me` o `grill-with-docs`); nunca encadenar ambas.
- Plan desde un reporte de auditoría ya existente → `writing-plans`; no re-auditar; el reporte es fuente de verdad.

## Puertas

| Situación | No cargar / no obedecer | Gana |
|---|---|---|
| Bug o trivial, aunque el fix cambie comportamiento | `brainstorming`, aunque diga MUST antes de cualquier cambio | Esta skill. Bug: `systematic-debugging`. Trivial: implementación directa |
| TDD no configurado | `test-driven-development`. `writing-plans` no agrega fase TDD ni "failing test first" | Tests de `gian-how-i-code` `17` y el runner del repo. TDD solo si el usuario lo pidió en este hilo, o el proyecto/sesión ya tiene TDD estricto con un runner nombrado. Pest, PHPUnit o Vitest presentes no lo encienden |
| PHP y está cargada `laravel-11-12-app-guidelines` | `vendor/bin/pint --dirty`, `vendor/bin/pint`, Boost `pint/core` | `gian-php-style`. No es paso final del plan ni del build |

## Plan (agente plan)

clasificar → cargar policy si desarrollo → brainstorming si aplica → grill si decisiones materiales → writing-plans si multi-step → entregar plan + estado de aprobación. Read-only siempre. Si el plan incluye snippets PHP: siguen `gian-php-style` (no PHPDoc; un parámetro en una línea). Si incluye snippets TS/TSX: siguen `gian-ts-style`. No duplicar esas specs aquí. **No incluir Pint como paso final** (Boost `pint/core` queda anulado).

Si se parte de una referencia o un plan, el plan lista *Sin datos todavía* y *Texto de la referencia que no se publica*. La UI no lleva ese texto: nombre de la referencia, fase, Mock o muestra, dueño o fecha de entrega. Sección sin datos: constante + `TODO(datos)`, sin preguntar ni bloquear. Fuera de alcance: no se monta (`gian-how-i-code` `15`).

## Build (agente build)

consumir plan aprobado (o alcance aprobado) → cargar policy → Fase 0 + references según routing (lazy) → si toca PHP, WRITE `gian-php-style` en el hunk (**no Pint**) → si toca `.ts`/`.tsx` o un `<script setup lang="ts">`, WRITE `gian-ts-style` en el hunk (HARD; no format-only) → ejecutar por tareas/lotes con todowrite → validaciones reales del repo → revisión independiente según riesgo → cierre con evidencia. Sin plan, o tarea trivial/bug → routing proporcional de esta skill.

Si se partió de una referencia o un plan: antes de cerrar, `rg` de rótulos y `rg "TODO\(datos\)"` sobre los archivos tocados. El cierre lleva *Sin datos todavía* con `archivo:línea` y *Texto de la referencia que no publiqué* (`gian-how-i-code` `15`, `21`).

Si el edit entra en el cuerpo de un componente, hook o composable, reordenar esa función antes de cerrar el cambio. Los slots están en `04`. Los casos dentro de cada slot están en `26`. Efectos al final, antes del return. No el otro componente del archivo.

Si el edit entra en un método PHP, reordenar ese método según `26` antes de cerrar el cambio. No el otro método del archivo.

## Precedencia y fallback

Este router DELEGA: no reescribe contenido de las process skills ni de la policy. Si una process skill no está disponible o falla, degradar al siguiente nivel (sin writing-plans → lotes con todowrite; sin brainstorming → preguntas directas al usuario). Si `gian-how-i-code` no está disponible, continuar el proceso y señalarlo en el cierre.

## Caveman

Activación manual por trigger del usuario ("caveman", "be brief", "menos tokens"). Aplica a conversación, progress updates, explicaciones y cierres. NO aplica a artefactos: implementation plans, specs, auditorías, reportes técnicos, ADRs, código, errores o temas de seguridad. Caveman no elige herramientas; el bootstrap y el routing viven en la policy global de herramientas del host.

## Capacidades futuras (no default)

- `executing-plans`: ejecución con checkpoints en sesión separada — evaluación separada.
- `subagent-driven-development`: ejecución multiagente — evaluación separada (mapping `general` verificado en spike 2026-08-11); actualmente deny en Plan/Build.

## Publicar estas skills

Si el turno crea o edita `gian-development-workflow`, `gian-how-i-code`, `gian-php-style` o `gian-ts-style`:

1. El texto publicado está en el clone cuyo `origin` es `github.com/GianZapata/gian-agent-skills`, bajo `skills/<name>/`. Editar ese clone, no solo la copia instalada.
2. La copia instalada y el clone quedan con el mismo wording. Sin paths de máquina, ni nombres de org, cliente o producto. El slug del repo de estas skills es la excepción.
3. No commitear `evals/`.
4. Commit y push en el mismo turno, sin preguntar. Para estos cuatro skills, esta orden gana a “solo commitea si te lo piden”.
5. No incluir secretos ni archivos ajenos al cambio. No saltarse hooks.

## Calidad visual

Si la tarea propone, crea, modifica o revisa UI visible, antes de la primera decisión visual abre `references/visual-quality.md`. Plan, análisis y review incluidos. No abrir en tareas sin interfaz.

La principal es preferencia de superficie. Un apoyo no trae otra dirección y no se cargan dos apoyos en la misma delegación. Las preferencias de `gian-how-i-code` no congelan un defecto visual dentro del alcance. Contratos, stack y función siguen en esa skill.

## References

- `references/workflow-activation.md`
- `references/style-activation.md`
- `references/visual-quality.md`
- `references/visual-quality-bootstrap.md`
- Tool choice follows la policy global de herramientas del host. Do not add a second routing skill.
