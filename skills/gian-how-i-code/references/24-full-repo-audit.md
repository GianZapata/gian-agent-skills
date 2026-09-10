# 24 — Auditar repositorio completo

Cargar cuando: el usuario pide auditar **todo** / el **proyecto** / el **repo** / full audit / equivalente (`18`).

**Prohibido:** muestreo de 2 features como cierre; concluir “altamente alineado” sin Gate de cobertura.

**Sin cuota mínima de hallazgos.** Profundidad = inventario + búsquedas + categorías sin hallazgos con evidencia + gate.

## 1. Cargar el estándar instalado

1. Leer `gian-how-i-code/SKILL.md` (versión en frontmatter).
2. Registrar en el reporte: versión, references cargadas.
3. Las reglas de queries/mutations/forms/display/… salen de esas references — **no** de memoria ni de un prompt hardcodeado.

## 2. Alcance e inventario

Incluir (si existen): `app/`, `apps/*/src`, `components/`, `features/`, `hooks/`, `lib/`, `stores/`, `types/`, `resources/` (Laravel), tests, configs que afecten arquitectura/TS/ESLint/Query/Next/Firebase/validación.

Excluir por defecto: `node_modules`, `.next`, `dist`, `build`, `coverage`, artefactos generados, cachés, vendor. **Toda exclusión extra** → declarar y justificar.

Inventario reproducible (`git ls-files` o equivalente). Registrar:

- archivos versionados / en alcance / por extensión / por directorio
- features encontradas
- configs y tests
- exclusiones + motivo

Tabla mínima:

| Área | Encontrados | Revisados estructuralmente | Revisados semánticamente | Excluidos |
|------|------------:|---------------------------:|-------------------------:|----------:|

Ningún archivo en alcance puede quedar omitido en silencio. Clasificar cada uno: revisado directo | cubierto por búsqueda estructural | textual | símbolos | excluido justificado.

Auxiliar permitido si el inventario es enorme:

```text
pattern-audit/YYYY-MM-DD-<alcance>-coverage-ledger.md
```

El reporte principal sigue siendo el único `…-auditoria.md` (`18`, `21`).

## 3. Variante del repo

Documentar arquitectura real (HTTP, Firestore realtime, tenancy, drawer store, etc. — `20`).

Matriz:

| Regla del molde | Aplica | No aplica | Adaptación equivalente | Evidencia |
|-----------------|--------|-----------|------------------------|-----------|

“No aplica” no cierra el tema: definir responsabilidad equivalente (p. ej. HTTP service → Firestore service; AbortSignal → unsubscribe; ErrorMapper HTTP → clasificación Firebase).

## 4. Barrido obligatorio (textual + estructural + símbolos)

Combinar `rg`/Grep, **ast-grep** (si hay), **Serena/codegraph** (si hay). Afirmar “usé X” sin filas en el registro de búsquedas **no** cuenta.

Categorías mínimas a cubrir (contrastar con references vigentes):

| Categoría | Reference típica |
|-----------|------------------|
| Mutations | `13` |
| Queries / subscriptions / realtime | `13`, `20` |
| Forms / Zod | `10` |
| Display | `08` |
| Overlays | `09` |
| Fechas / helpers / duplicación | `23` |
| Naming / estilo TS / `cn` | `04`, `23` |
| Enums / tipos cerrados | `07` |
| Errores / feedback | `14` |
| Calidad de diseño | `22` |
| Stack gaps | `19` |

### Patrones orientativos (no son la regla)

La verdad es cada `references/NN`. Ejemplos de búsqueda:

- Fechas: `new Date(`, `Date.now(`, `import dayjs from`, `@/lib/dayjs`, `formatDate`, `toLocaleDateString`
- Mutations: `useMutation`, `UseMutationOptions`, `mutationFn`, `onSuccess`, `invalidateQueries`
- Queries: `useQuery`, `UseQueryOptions`, `queryKey`, `onSnapshot`, `getDocs`
- Forms: `useForm`, `z.object`, `z.infer`, `interface *Input`, `zodResolver`
- Display: `ColorHelper`, `getPrimaryLabel`, ternarios anidados
- Overlays: `*Dialog*`, `*Modal*`, `*Drawer*`
- Naming: `handle[A-Z]`, files `use-*.ts(x)` / `use_*.ts(x)`, `export function`, `className=\``, `as any`
- Errores: `console.error`, `toast.`, `error.message`, `FirebaseError` / `CustomError`

Para **cada** mutation hook / form / overlay relevante: tabla de cumplimiento vs regla **vigente** (no inventar la regla aquí).

## 5. Revisión por feature

Enumera **todas** las carpetas directas de `features/` (u homólogo).

| Feature | Archivos | Queries/realtime | Mutations | Forms | Display | Overlays | Errores | Tipos | Calidad | Estado |
|---------|---------:|------------------|-----------|-------|---------|----------|---------|-------|---------|--------|

Estados: `Revisada, con hallazgos` | `Revisada, sin hallazgos` | `Parcialmente revisada` (bloqueo) | `No aplicable` (motivo).

Prohibido omitir features por “representativas”.

## 6. Categorías sin hallazgos

Obligatorio si no hay H- en esa categoría:

```markdown
### Sin hallazgos — <categoría>
- Archivos cubiertos:
- Features cubiertas:
- Búsquedas ejecutadas:
- Coincidencias revisadas:
- Evidencia representativa:
- Razón para concluir cumplimiento:
```

## 7. Hallazgos (H-NNN)

Plantilla enriquecida (alcance repo):

```markdown
### H-NNN — Título
- Severidad:
- Categoría:
- Features afectadas:
- Alcance: aislado | repetido | sistemático
- Evidencia: `path:línea` (varias si sistemático)
- Regla exacta: `references/…` §…
- Comportamiento actual:
- Problema:
- Impacto:
- Corrección:
- Archivos estimados:
- Dependencias:
- Validación:
- Estado: Pendiente | …
```

Severidad según impacto/frecuencia/riesgo (`18`) — no bajar todo a Baja.

## 8. Propuestas (PROP-NNN)

Contrato `19`. Costos y riesgos **reales**. Prohibido “sin riesgos” / “garantiza CI” sin scripts + pipeline verificados.

## 9. Apéndices

### A — Registro de cobertura (búsquedas)

| ID | Herramienta | Consulta/patrón | Paths | Coincidencias | Revisadas |
|----|-------------|-----------------|-------|--------------:|----------:|

### B — Inventario de archivos

| Archivo | Feature/área | Método | Categorías | Resultado |

(B puede vivir en el coverage-ledger auxiliar.)

## 10. Gate de cobertura

No cerrar como completo hasta:

- [ ] Inventario de todos los archivos en alcance
- [ ] Ningún omitido silencioso
- [ ] Todas las features con estado
- [ ] Mutations / queries-subscriptions / forms / display / overlays cubiertos
- [ ] Fechas-helpers / naming / enums / errores / design quality cubiertos
- [ ] Variante documentada (matriz)
- [ ] Categorías sin hallazgos con evidencia
- [ ] PROP con costos/riesgos reales
- [ ] Registro de búsquedas
- [ ] Sin editar código / manifests / installs / commits

Si un ítem falla → disposición no puede ser `full_repo_audit_complete`.

## 11. Disposición y métricas

Una de:

- `full_repo_audit_complete`
- `full_repo_audit_complete_with_blind_spots`
- `full_repo_audit_blocked`
- `audit_incomplete`

```text
Archivos en alcance:
Archivos cubiertos:
Cobertura:
Features revisadas:
Categorías revisadas:
Búsquedas ejecutadas:
Hallazgos:
Propuestas:
Exclusiones:
```

## 12. Estructura del reporte principal

Además de §§0–4 de `18`, el full-repo incluye (en el mismo `.md` o por referencia al ledger):

- Versión de skill + inventario resumen
- Matriz variante
- Tabla por feature
- Categorías sin hallazgos
- Apéndices A/B (o link al ledger)
- Gate + disposición + métricas
- Key Learnings (3 bullets)
