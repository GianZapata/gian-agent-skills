# Changelog

## 1.4.0 — 2026-11-23

- `assets/self-check.php`: script de verificación (PHP CLI, `token_get_all`) con el contrato de `gian-ts-style/assets/self-check.mjs`. Sin argumentos revisa los métodos tocados en `git diff HEAD` y los archivos nuevos; `--all` revisa todo; exit 0/1/2 (2 = GAP). Cubre 14 reglas mecánicas. Alineación de `=>`, líneas en blanco, modifiers y `read-group` quedan manuales. `gian-development-workflow` reemplaza `Self-check PHP: manual` por este script.

## 1.3.0 — 2026-10-12

- `read-group` (HARD, `vertical-spacing.md`, `SKILL.md`, audit, overrides): cada lectura abre su grupo y una línea en blanco lo cierra. Su complemento de una línea (ids, historial, `keyBy`) va pegado debajo. Dos lecturas solo van pegadas si la segunda es complemento de la primera. Una lectura multilínea cierra con línea en blanco antes de su complemento; solo el guard que la valida queda pegado. Antes, varias consultas de una línea quedaban pegadas como un solo paso. El ejemplo de "Mismo paso" ya no junta dos lecturas y el de "Cuatro pasos", ahora "Corte por pasos", separa la lectura de etiquetas.

## 1.2.3 — 2026-10-05

- `vertical-spacing`: el orden de los pasos lo decide `gian-how-i-code` `26`. Este archivo solo inserta la línea en blanco.

## 1.2.2 — 2026-10-05

- Corte por pasos (`SKILL.md`, `references/vertical-spacing.md`): al cerrar un paso multilínea, una línea en blanco antes del siguiente. Las sentencias de una línea del mismo paso quedan juntas. No se parte un array ni los argumentos de una llamada. El ejemplo muestra la consulta, el bucle que llena, las reducciones de una línea, el bucle que arma y el `return`. Antes el corte solo era una preferencia en el espaciado vertical, y no se aplicaba.
