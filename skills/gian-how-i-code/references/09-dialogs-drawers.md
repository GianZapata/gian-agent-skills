# 09 — Diálogos y drawers

Cargar cuando: modales, drawers, overlays.

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

Verificación sugerida: ≤5 props en call-site de dialog (señal de aplanado).

## Variante reconocida — store de UI para drawers

Si el repo ya usa un store tipo `createEntityDrawerStore<T>()` / Zustand:

- Respetar el store compartido
- Sigue aplicando: dueño de mutación, no `handle*`, montaje limpio, props `isOpen` + tipo
- No forzar el default de useState encima de la variante

Ver `20-variants.md`.
