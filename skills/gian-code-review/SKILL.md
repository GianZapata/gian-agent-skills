---
name: gian-code-review
description: "Gian's own read-only code review over a diff (branch, PR, or work in progress). Runs independent lenses in parallel: security and dependencies, bugs, transactions and data integrity, design (SOLID / clean code), current library practices via Context7, gian-how-i-code conformance, and stale docs. Runs alongside RDD native review, never replaces it."
license: Apache-2.0
metadata:
  author: gian
  version: "1.0.0"
when-to-use: "Review a diff before a pull request; 'revisa el diff', 'code review', 'review since X', 'audita este PR'. Not for writing code, not for style-only checks (use the style self-checks), not for full-repo audits (gian-how-i-code 24)."
---

# gian-code-review

Review propia sobre un diff. **Solo lectura**: no edita, no commitea, no abre PR. Entrega hallazgos; el usuario decide qué se corrige.

## Relación con RDD

Independiente de la review nativa (`gentle-ai review`). No pide consentimiento, no crea lineage ni receipt, no cuenta como aprobación de entrega. Si RDD está activo, corren las dos; esta no salta ni sustituye la nativa.

## Entrada

1. **Base**: la que el usuario nombre (commit, rama, tag). Si no nombra: `git merge-base HEAD <rama por defecto>`; si no hay rama por defecto, `HEAD` (trabajo sin commitear). Anunciar la base elegida.
2. **Diff**: `git diff <base>` más archivos sin trackear. Excluir lockfiles del análisis de lógica, no de la lente de dependencias.
3. **Contexto del repo**: Fase 0 de `gian-how-i-code` `02` en versión corta: manifests, stack, verificador declarado. Memoria primero (`project/conventions`, `project/decisions` en Engram) si está disponible.
4. **Spec**: si el usuario o el feature doc (`odd/tasks/*.md`) trae requisitos, pasarlos a la lente de bugs.

## Lentes

Detalle de cada una en `references/lenses.md`. Cada lente recibe el mismo diff, la base y las rutas de las skills que aplican.

| # | Lente | Corre cuando |
|---|-------|--------------|
| L1 | Seguridad y dependencias | Siempre. `composer audit` / `npm audit --omit=dev` solo si cambió un manifest o lockfile |
| L2 | Bugs y regresiones | Siempre |
| L3 | Transacciones e integridad de datos | El diff toca escrituras, migraciones, jobs, pagos o estado |
| L4 | Diseño (SOLID, clean code) | Siempre; criterio de `gian-how-i-code` `22` |
| L5 | Prácticas actuales de librerías | El diff usa API de una librería externa; consultar Context7, nunca memoria |
| L6 | Conformidad con `gian-how-i-code` | Siempre; solo las references que la matriz marca para lo tocado |
| L7 | Docs desactualizadas | El diff cambia comando, opción, endpoint, config, env o contrato |

Estilo visual no es una lente: se corre `gian-php-style/assets/self-check.php` y `gian-ts-style/assets/self-check.mjs` sobre el diff y se pega la última línea de cada uno.

## Ejecución

1. Resolver base, diff y lentes aplicables; anunciar cuáles corren y cuáles no, con motivo.
2. Si el host tiene subagentes, una lente por subagente, **todas en el mismo turno**, solo lectura. Si no, en secuencia. Diff de más de ~1500 líneas: partir por área y avisar.
3. Cada lente devuelve hallazgos con el formato de `assets/report-template.md`. Sin evidencia `path:line` no hay hallazgo.
4. Consolidar: deduplicar (mismo `path:line` y misma causa → uno, con todas las lentes que lo vieron), ordenar por severidad.
5. Verificar cada BLOCKER y MAJOR leyendo el código en el padre. Lo que no se sostiene baja a INFO o se descarta, y se dice.

## Severidad

- **BLOCKER**: rompe en producción, pierde o expone datos, vulnerabilidad explotable, regresión de una spec pedida.
- **MAJOR**: bug probable en un caso real, falta de transacción o idempotencia, contrato roto, dependencia con CVE alta.
- **MINOR**: diseño, conformidad, docs, mantenibilidad.
- **INFO**: observación sin acción obligatoria; preexistente fuera del diff.

Hallazgos en código que el diff no tocó van como **preexistentes**, aparte, nunca como BLOCKER del cambio.

## Output Contract

Formato de `assets/report-template.md`: base y diff revisados, lentes corridas/omitidas, hallazgos por severidad, preexistentes, líneas de self-check, veredicto (`listo para PR` / `corregir antes de PR` / `no evaluable`) y la siguiente acción sugerida. Sin parches salvo que el usuario los pida.

## References

- `references/lenses.md`
- `assets/report-template.md`
- `gian-how-i-code` `02`, `17`, `18`, `22`, `27`, `28`, `29`
