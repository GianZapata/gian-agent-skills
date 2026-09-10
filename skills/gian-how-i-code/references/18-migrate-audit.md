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
- **GAP:** la regla pertenece al alcance, pero no puede resolverse de forma segura con la evidencia actual (por ejemplo, equivalencia palette↔utility no demostrable, slot público incierto o token requerido sin bridge).
- **Fuera de alcance:** problema real de otra categoría que la auditoría actual no pretende resolver. En una auditoría de styling, query-key-factory, AbortSignal, CustomTable/MRT o arquitectura del store no son GAP de styling.
- Registrar “Fuera de alcance” solo cuando sea útil; no convertirlo automáticamente en PROP salvo que el usuario haya pedido una auditoría más amplia ni inflar el reporte con deuda lateral no solicitada.

## Salida (un solo archivo)

```text
pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md
```

Ejemplos de `<alcance>`: `machines`, `entities`, `repo`.

- **Un único** `.md` de auditoría. No carpetas multi-archivo por feature.
- Si ya existe el archivo del mismo alcance/día, **actualizarlo**; no un segundo reporte paralelo.
- Numeración `H-` / `PROP-` **global**.
- Solo en **repo completo**: auxiliar opcional `pattern-audit/YYYY-MM-DD-<alcance>-coverage-ledger.md` si el inventario de archivos es inmanejable (`24`).

Idioma: **español**.

## Estructura del archivo

```markdown
# Auditoría de molde — <alcance>

## 0. Contexto
- Repo / clasificación Fase 0
- Versión de gian-how-i-code cargada
- Alcance: feature | repositorio completo
- References usadas

## 1. Resumen ejecutivo
(Prohibido “altamente alineado” en full-repo sin gate `24`)

## 2. Hallazgos de molde
### Por módulo/feature (si el alcance es amplio)
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

Feature: Severidad, Evidencia, Regla, Problema, Corrección, Estado.

Repo completo: plantilla enriquecida en `24` (categoría, alcance aislado/repetido/sistemático, impacto, archivos estimados, …).

### PROP

Contrato `19`. Costos/riesgos reales — no “ninguno”; no “garantiza CI” sin evidencia.

## Severidad

| Nivel | Ejemplos |
|-------|----------|
| Alta | N+1, status update a mano, contrato inventado, diálogo rompe datos, falta dayjs / `new Date` sistemático de negocio, falta ErrorMapper/apiFetcher cuando el molde lo exige |
| Media | Display helper (labels/colores), `*Helper` cajón multi-dominio, función local que duplica `DateHelper`/`NumberHelper`/util compartido, keys sueltas, props aplanadas, typed strings vs enum `APP_OWNED`, shadow type `LIBRARY_OWNED`, `useMemo` ceremonial (`23` A; no C/E), constantes `*_SX` / `get*Sx` locales, `sx` de layout/spacing/sizing ordinario, concat/template de `className` condicional, `useTheme()` ceremonial (solo para `sx`), mutation con `onSuccess`/`onError` fijos en el hook, `interface XxxInput` duplicando Zod, query sin `*QueryProps`, dayjs crudo pese a módulo configurado, QueryClient por feature, archivo hook kebab/snake `use-*` sistemático (`04`), cadena `=== \|\| ===` de conjunto cerrado sistemático (`07`) |
| Baja | Naming `handle*`, `open` vs `isOpen`, `entity=`/`data=` vs prop por tipo (`09`), `=== \|\| ===` vs includes/`in_array` aislado (`07`), callback `whenLoaded` innecesario (`06`), archivo hook `use-*`/`use_*` aislado (`04`), copy Title Case, nit de carpeta, mutation sin interface `UseMutationOptions` |

Considerar impacto, frecuencia y si el patrón es **sistemático** — no bajar todo a Baja.

## Auditar (sin editar)

- No modificar código ni manifests
- Evidencia por archivo/línea (preferir ast-grep / símbolos cuando estén disponibles — ver `02` / `24`)
- Separar Hallazgos vs Propuestas en el **mismo** archivo
- Contrastar inventario FE de `02`
- Si alcance = repo completo → cumplir Gate `24` antes de disposición `complete`

## Auditar + aplicar

1. Actualizar el mismo archivo de auditoría
2. Completar §§5–6 (checklist + registro) en ese archivo
3. Solo H/PROP aprobados por el usuario
4. Validar tras cada lote (`17`)

Orden típico de lotes: diálogos → display/enums → service/hooks/keys → forms → BE Resource/Query.
