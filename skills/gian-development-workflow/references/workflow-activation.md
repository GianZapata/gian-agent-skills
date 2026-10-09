# Gian development workflow activation

Pegar el bloque `gian-development-workflow-bootstrap` en el always-on de cada harness, junto al de estilo. No es un include: los agentes no lo siguen salvo que esté inyectado.

La calidad visual no va dentro de ese bloque. Su bootstrap está en `references/visual-quality-bootstrap.md`. El adaptador lo inyecta fuera de las regiones `gentle-ai:*`.

El bloque obliga a abrir los archivos. Recordar la skill no cuenta. Nombrarla no cuenta. No copiar aquí el molde de `gian-how-i-code`.

```markdown
<!-- gian-development-workflow-bootstrap -->
## Gian development workflow

En trabajo de desarrollo dentro del scope (PHP, Laravel, React, Vue, Angular, Node, TypeScript, Python, features, refactors, auditorías, contratos, forms, queries, tablas, dialogs), seguir `gian-development-workflow` y `gian-how-i-code` es obligatorio. Es la forma de trabajo.

Antes del primer edit, abrir y leer estos archivos. Recordar la skill no cuenta. Nombrarla no cuenta.

- `gian-development-workflow` `SKILL.md`, y clasificar la tarea con esa tabla.
- `gian-how-i-code` `SKILL.md`.
- Cada reference que la matriz de routing de esa skill marca para esta tarea.

Esas references se aplican. Saltarse una regla porque el cambio parece pequeño, porque el repo ya diverge, o porque la skill ya se usó en otro turno, no está permitido.

La matriz decide qué references aplican. No se leen todas en cada turno. No se copia el molde en este bloque.

Fuera de scope (git, Docker/infra pura, preguntas generales): no se carga.
<!-- /gian-development-workflow-bootstrap -->
```
