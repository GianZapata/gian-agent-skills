# 09 — Diálogos y drawers

Cargar cuando: modales, drawers, overlays.

## Alcance

- **Núcleo:** componente aparte; el overlay es dueño de la mutación; props `isOpen` + entidad con el nombre de su tipo + `onClose` (punto 4); la UI no arma `FormData`.
- **Adaptador React:** montaje `{isOpen && user && (` (creación: `{isOpenCreate && (`), `invalidateQueries` y el hook de mutation. En otro stack, el primitivo de overlay equivalente cumple las mismas props y la misma propiedad.
- **Angular:** el componente que se abre con `MatDialog` recibe la entidad por `MAT_DIALOG_DATA`, es dueño de la mutación y devuelve el resultado por `afterClosed`.
- **Vue:** el overlay se monta con `v-if`, no con `v-show`, para que se desmonte (`25`).

## Regla

HARD. Solo la reemplaza la variante de `20` (§Variante reconocida abajo).

1. Componente aparte.
2. Montar al abrir (un overlay):

```tsx
{isOpen && user && (
  <UserPasswordDrawer
    isOpen={isOpen}
    user={user}
    onClose={onClose}
  />
)}
```

   Diálogo de creación: sin entidad y sin prop de entidad.

```tsx
{isOpenCreate && (
  <UserCreateDialog
    isOpen={isOpenCreate}
    onClose={onCloseCreate}
  />
)}
```

3. Varios overlays en el mismo padre: un boolean `isOpen<X>` por diálogo (`isOpenPassword`, `isOpenEdit`) + la entidad. El JSX sigue el mismo molde: `{isOpenPassword && user && (`. Un enum de "qué diálogo está abierto" no es el patrón (`DialogKind` de `07` es solo un ejemplo de enum).
4. Props HARD:
   - Apertura: MUST `isOpen`. Prohibidos `open`, `visible`, `show`, `isVisible`.
   - Entidad: MUST el nombre de su tipo en camelCase (`user={user}`, `salesOrder={salesOrder}`). Prohibidos `entity`, `data`, `item`, `record`, `row`, `selected`, `value`.
   - Cierre: MUST `onClose`. Prohibidos `onCancel` y pasar `setOpen` como cierre.
   - `onSuccess` del padre solo para lo que no es refrescar datos. Refrescar es del diálogo (punto 5).
5. Diálogo es **dueño** de form interno, mutación e `invalidateQueries`.
6. Pasa `onSuccess` / `onError` (y demás) como **options** al hook de mutation (`13`): el hook solo fija `mutationFn`.
7. Dato de otro endpoint (no include) → prop hermano; verificar Query allowlist.
8. El overlay solo envía **DTO**. Prohibido `new FormData()`, formatear Dayjs/Date a string o armar multipart en el dialog. `mutate(data)` o `mutate({ params, data })` según `13`. Serialización en el service (`23`).
9. Cerrar con `isDirty` MUST abrir una confirmación con el componente de confirmación del repo. Borrador o autoguardado solo si la feature ya lo tiene; si no, PROP (`10`). Un error de envío no borra la captura.

### Anti-patrones

| Mal | Bien |
|-----|------|
| Drawer siempre montado | Montar condicional |
| Solo ID como señal de apertura | Entidad + `isOpen` |
| Estado del form en el padre | Estado en el diálogo |
| `onConfirm` de acción desde el padre | Mutación dentro |
| Aplanar 8 props de relaciones | Pasar entidad con includes |
| `open` / `visible` / `show` / `isVisible` | `isOpen={…}` |
| `entity` / `data` / `item` / `record` / `row` / `selected` / `value` | Prop del tipo: `user={user}` |
| `onCancel` / `setOpen` como cierre | `onClose` |
| `useState<DialogKind \| null>` para elegir qué diálogo abre | Un boolean `isOpen<X>` por diálogo |
| Cerrar con `isDirty` sin confirmar | Confirmación del repo |
| `new FormData()` / `append` en el dialog | `mutate(data)` y el service serializa |

Más de 5 props en el call-site de un dialog MUST reportarse como aplanado.

## Variante reconocida — store de UI para drawers

Si el repo ya usa un store tipo `createEntityDrawerStore<T>()` / Zustand:

- Respetar el store compartido
- Sigue aplicando: dueño de mutación, no `handle*`, montaje limpio, props `isOpen` + tipo
- No se migra la variante a `useState`

Ver `20-variants.md`.
