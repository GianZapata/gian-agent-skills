# 18 — Auditar y migrar

Cargar cuando: modo Auditar o Auditar + aplicar.

## Alcance de Auditar

| Alcance | Señales del usuario | Protocolo |
|---------|---------------------|-----------|
| **Feature / módulo** | nombra una feature, “audita machines”, un path concreto | Este archivo + references del dominio |
| **Repositorio completo** | “todo”, “el proyecto”, “el repo”, “full audit”, auditoría amplia sin feature | **Obligatorio** `24-full-repo-audit` + este archivo |

**Prohibido** en repositorio completo: cerrar con muestreo de 2 features; concluir “altamente alineado” sin Gate de cobertura (`24`).

Reglas de molde: leer la **versión instalada** de la skill y sus references — no imponer reglas de memoria.

### Scope de una auditoría focalizada

- **FAIL:** la regla aplicable está incumplida y su corrección pertenece al alcance solicitado.
- **GAP:** la regla pertenece al alcance y la corrección cae en uno de estos tres casos, y solo en ellos:
  1. equivalencia no demostrable (p. ej. palette↔utility);
  2. API o slot pública incierta;
  3. token requerido sin bridge.

  Cada GAP indica el caso, la evidencia que falta y qué la resolvería. Cualquier otra regla incumplida dentro del alcance es FAIL.
- **Fuera de alcance:** problema real de otra categoría que la auditoría actual no pretende resolver. En una auditoría de styling, query-key-factory, AbortSignal, CustomTable/MRT o arquitectura del store no son GAP de styling.
- Registrar siempre lo “Fuera de alcance” observado, una línea por caso con `archivo:línea`. No convertirlo en PROP salvo que el usuario haya pedido una auditoría más amplia. No desarrollarlo más allá de esa línea.

## Salida (un solo archivo)

```text
docs/pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md
```

La ruta es relativa a la raíz git del repo auditado, no a un repo padre. Ejemplos de `<alcance>`: `machines`, `entities`, `repo`.

- **Un único** `.md` de auditoría. No carpetas multi-archivo por feature.
- Si ya existe el archivo del mismo alcance/día, **actualizarlo**; no un segundo reporte paralelo.
- Numeración `H-` / `PROP-` **global**.
- Solo en **repo completo**: auxiliar `docs/pattern-audit/YYYY-MM-DD-<alcance>-coverage-ledger.md` (`24`). Usarlo o no es decisión explícita del auditor; se declara en §0 Contexto con el motivo.
- Al escribir, si el `.gitignore` de esa raíz no ignora `docs/pattern-audit/`, se agrega esa línea. Si no hay `.gitignore`, se crea con esa sola línea. Si la entrada ya está, no se duplica. No se ignora `docs/` entero.

Idioma: **español**.

## Conclusión de un caso backend

Cada conclusión es una de cuatro. Buscar una mejora justificada es obligatorio aunque el caso cumpla. No hay cupo mínimo.

| Clase | Cuándo |
|---|---|
| Defecto demostrado | El código incumple una garantía que el contrato ya exige |
| Mejora justificada | Hay evidencia de una oportunidad. No es rutina |
| Decisión pendiente | Una ambigüedad concreta cambia el caso. La ausencia de una regla extra no basta |
| Adecuado | El caso cumple para el contrato y el alcance revisados |

## Estructura del archivo

```markdown
# Auditoría de molde — <alcance>

## 0. Contexto
- Repo / clasificación Fase 0
- Versión de gian-how-i-code cargada
- Alcance: feature | repositorio completo
- References usadas
- Herramientas usadas y no disponibles (ast-grep, Serena, codegraph)
- Coverage-ledger: sí | no, con motivo (solo repo completo)

## 1. Resumen ejecutivo
(Prohibido “altamente alineado” en full-repo sin gate `24`)

## 2. Hallazgos de molde
### Por módulo/feature (cuando la auditoría cubre dos o más features)
### H-001 — …
## 3. Propuestas (PROP-NNN)
## 4. Lotes sugeridos

## 5. Checklist de aplicación          # solo Auditar+aplicar
## 6. Registro de implementación      # solo Auditar+aplicar

# Solo repositorio completo (`24`):
## Inventario / cobertura (resumen)
## Matriz variante
## Tabla por feature
## Categorías sin hallazgos
## Apéndices A–B (o link al coverage-ledger)
## Gate de cobertura
## Disposición + métricas
## Key Learnings
```

### Hallazgo H-NNN (mínimo)

Feature: Severidad, Evidencia (`archivo:línea`), Regla (`references/NN §sección`), Problema, Corrección, Estado.

Cada H cita `references/NN §sección`. Un H sin regla citada no cuenta. Toda categoría revisada sin hallazgos lleva el bloque «Sin hallazgos» de `24` §6.

Repo completo: plantilla enriquecida en `24` (categoría, alcance aislado/repetido/sistemático, impacto, archivos estimados, …).

### PROP

Contrato `19`. Costos/riesgos reales — no “ninguno”; no “garantiza CI” sin evidencia.

## Severidad

| Nivel | Ejemplos |
|-------|----------|
| Alta | N+1, status update a mano, contrato inventado, diálogo rompe datos, falta dayjs / `new Date` sistemático de negocio, falta ErrorMapper/apiFetcher cuando el molde lo exige, chip/banner/copy "Test mode" o validación ramificada por el runtime (`08`), rótulo de referencia, fase o muestra publicado en UI ("Mock", "Próxima fase", "oficial") (`15`), efecto duplicado, dato incoherente o contrato roto por una clase fuera de lugar (`05`), `sometimes` en una key anidada con `required_with` (acepta ítems incompletos), campo obligatorio sin `required` en el Store |
| Media | Display helper (labels/colores), `*Helper` cajón multi-dominio, función local que duplica `DateHelper`/`NumberHelper`/util compartido, keys sueltas, props aplanadas, typed strings vs enum `APP_OWNED`, shadow type `LIBRARY_OWNED`, `useMemo` ceremonial (`23` A; no C/E), constantes `*_SX` / `get*Sx` locales, `sx` de layout/spacing/sizing ordinario, concat/template de `className` condicional, `useTheme()` ceremonial (solo para `sx`), mutation con `onSuccess`/`onError` fijos en el hook, `interface XxxInput` duplicando Zod, `TVariables` híbrido ruta+body, payload anónimo `{ body: string }`, `new FormData()` en dialog/form, IDs de ruta dentro del schema Zod, query sin `*QueryProps`, dayjs crudo pese a módulo configurado, QueryClient por feature, archivo hook kebab/snake `use-*` sistemático (`04`), cadena `=== \|\| ===` de conjunto cerrado sistemático (`07`), loop que inyecta presencia en reglas compartidas, regla redefinida en el Update, trait para el Store/Update de una entidad, `unique` solo en uno de los dos requests |
| Baja | Naming `handle*`, `open` vs `isOpen` (Baja solo en auditoría; en Implementar es HARD y se corrige en el componente tocado, `09`), `entity=`/`data=` vs prop por tipo (`09`), `=== \|\| ===` vs includes/`in_array` aislado (`07`), callback `whenLoaded` innecesario (`06`), archivo hook `use-*`/`use_*` aislado (`04`), copy Title Case, nit de carpeta, mutation sin interface `UseMutationOptions`, mutation sin los 3 genéricos explícitos si el resto (interface + DTO) está bien |

La gravedad depende del impacto, la frecuencia y el riesgo sustentados por evidencia. No hace falta un incidente ya ocurrido para sostener un riesgo. No bajar todo a Baja.

Estar en `Support`, o agrupar variables en una clase, es desviación de convención (`05`). No es un nivel de esta tabla. La gravedad de ese caso sale del impacto, la frecuencia y el riesgo que se puedan sostener.

## Auditar (sin editar)

- No modificar código ni manifests
- Evidencia por `archivo:línea`. Si ast-grep, Serena o codegraph están disponibles, usarlos y registrar cada consulta en el registro de búsquedas. Si no están disponibles, anotarlo en §0 (`02`, `24`)
- Separar Hallazgos vs Propuestas en el **mismo** archivo
- Contrastar inventario FE de `02`
- Si alcance = repo completo → cumplir Gate `24` antes de disposición `complete`

## Auditar + aplicar

1. Actualizar el mismo archivo de auditoría
2. Completar §§5–6 (checklist + registro) en ese archivo
3. Solo H/PROP aprobados por el usuario
4. Validar tras cada lote (`17`)

Orden típico de lotes: diálogos → display/enums → service/hooks/keys → forms → BE Resource/Query.
