# Workspace bootstrap

Prepara la raíz del proyecto para el toolchain del agente. Es la regla para proyectos nuevos y para los que nunca se prepararon.

## Raíz del proyecto

La raíz es la carpeta workspace, no cada sub-repo:

- Una carpeta sin `.git` que agrupa repos (`tienda/` con `tienda-client/` y `tienda-back/`) es la raíz cuando ya está marcada (`.engram/config.json`, `.codegraph/` o un `*.code-workspace`) o cuando la mayoría de sus repos llevan su nombre como prefijo.
- Un submódulo pertenece a su superproyecto.
- Un repo suelto es su propia raíz.
- Una carpeta de categoría (que solo agrupa proyectos sin relación) no es raíz.

## Qué prepara

En la raíz, y solo lo que falta:

| Paso | Resultado |
| --- | --- |
| Engram | `.engram/config.json` con `project_name` = nombre de la carpeta raíz, y un alias de cada sub-repo hacia ese proyecto |
| CodeGraph | `codegraph init --yes` en segundo plano, con el log en `.codegraph-init.log` |
| Skill registry | `.atl/skill-registry.md` |
| Editor | `.vscode/settings.json` con un repo por carpeta, búsquedas sin `vendor/`/`node_modules/` y lint por sub-repo. Una configuración existente no se sobrescribe |
| Git | `.codegraph/ .engram/ .atl/ .serena/ graphify-out/` en el ignore global de git. Los `.gitignore` de los repos no se editan, solo se reporta lo que falte |

Nunca instala dependencias, nunca corre onboarding de Serena y nunca actualiza ni reindexa CodeGraph.

## Cuándo correrlo

- Si el host tiene un hook de inicio de sesión que lo ejecuta, no hagas nada.
- Si no lo tiene, antes del primer edit de una tarea de desarrollo: cuando a la raíz le falta `.engram/`, `.codegraph/` o `.atl/skill-registry.md`, corre una vez

```bash
python3 scripts/workspace-bootstrap.py <cwd> --apply
```

con la ruta relativa a esta skill. Sin `--apply` solo reporta.

- `--all <dir>` reporta todas las raíces bajo `<dir>`. Con `--apply` las prepara todas. Úsalo solo cuando lo pidan.

## Hook

`scripts/workspace-hook.py` lee el JSON de inicio de sesión del host (`{"cwd": ...}`), corre el bootstrap con `--apply` e imprime un recordatorio de la raíz y de esta skill. Fuera de un workspace no imprime nada. Su registro en cada host es configuración de la máquina y no vive en esta skill.
