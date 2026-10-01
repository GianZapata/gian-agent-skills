# 09 — Diálogos y drawers

Cargar cuando: modales, drawers, overlays.

## Alcance

- **Núcleo:** componente aparte; el overlay es dueño de la mutación; props `isOpen` + entidad por tipo + `onClose`; prohibido `open`, `entity=` y `data=`; la UI no arma `FormData`.
- **Adaptador React:** montaje `{isOpen && user && (`, `invalidateQueries` y el hook de mutation. En otro stack, el primitivo de overlay equivalente cumple las mismas props y la misma propiedad.
- **Angular:** el componente que se abre con `MatDialog` recibe la entidad por `MAT_DIALOG_DATA`, es dueño de la mutación y devuelve el resultado por `afterClosed`.
- **Vue:** el overlay se monta con `v-if`, no con `v-show`, para que se desmonte (`25`).

## Default canónico

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

3. Varios overlays en el mismo padre: un boolean por diálogo (`isOpenPassword`, `isOpenEdit`) + una entidad seleccionada. El JSX sigue el mismo molde: `{isOpenPassword && user && (`.
4. Props HARD: `isOpen` (no `open`); entidad por tipo (`user={user}`, `salesOrder={salesOrder}`); `onClose`. Prohibido `entity=` / `data=`. `onSuccess` solo si no es refrescar datos.
5. Diálogo es **dueño** de form interno, mutación e `invalidateQueries`.
6. Pasa `onSuccess` / `onError` (y demás) como **options** al hook de mutation (`13`): el hook solo fija `mutationFn`.
7. Dato de otro endpoint (no include) → prop hermano; verificar Query allowlist.
8. El overlay solo envía **DTO**. Prohibido `new FormData()`, formatear Dayjs/Date a string o armar multipart en el dialog. `mutate(data)` o `mutate({ params, data })` según `13`. Serialización en el service (`23`).
9. No perder lo escrito al cerrar con cambios pendientes: advertir. Borrador o autoguardado solo si el flujo largo ya lo tiene, o se propone (`10`). Un error de envío no borra la captura.

### Anti-patrones

| Mal | Bien |
|-----|------|
| Drawer siempre montado | Montar condicional |
| Solo ID como señal de apertura | Entidad + `isOpen` |
| Estado del form en el padre | Estado en el diálogo |
| `onConfirm` de acción desde el padre | Mutación dentro |
| Aplanar 8 props de relaciones | Pasar entidad con includes |
| `open={…}` | `isOpen={…}` |
| `entity={…}` / `data={…}` | Prop del tipo: `user={user}` |
| `new FormData()` / `append` en el dialog | `mutate(data)` y el service serializa |

Verificación sugerida: ≤5 props en call-site de dialog (señal de aplanado).

## Variante reconocida — store de UI para drawers

Si el repo ya usa un store tipo `createEntityDrawerStore<T>()` / Zustand:

- Respetar el store compartido
- Sigue aplicando: dueño de mutación, no `handle*`, montaje limpio, props `isOpen` + tipo
- No forzar el default de useState encima de la variante

Ver `20-variants.md`.
