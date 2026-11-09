# 25 — Vue SFC

Cargar cuando: el repo es Vue, o se crea, edita, audita o consulta un `.vue` o un `composables/use*.ts` de componente.

Este archivo es el **adaptador**. El núcleo sigue vigente (`01`): nombres, helpers de área, enums, contratos, errores, display. No heredar MUI, RHF, `hooks/` ni React Query. Eso no apaga el núcleo.

Los nombres los elige el núcleo (`04` Naming, `23`). La forma del binding (no destructurar por rutina, `import type`, flechas, llaves) es `gian-ts-style`. Una forma de objeto propia es `interface` ahí (`interface-object-shape`), no una regla de este archivo. Conjuntos cerrados y uniones: `07`.

## Script en el .vue

`<script setup lang="ts">` vive en el `.vue`, junto al template y al `<style scoped>`. Sin `src`. El compilador lee ese bloque en el SFC: `defineProps`, `defineEmits` y `defineModel` son macros y no se mueven a un `.ts`.

```vue
<script setup lang="ts">
import { useEntityPage } from '../composables/useEntityPage';

interface EntityPageProps {
  entityId: string;
}

const props = defineProps<EntityPageProps>();
const { label, onConfirm } = useEntityPage(props);
</script>

<template>
  ...
</template>
```

El bloque solo tiene macros, imports de componentes y la llamada al composable. Lo que devuelve queda visible en el template. Sin `export default` y sin `return`.

Prohibido `<script setup src="...">` y `export default defineComponent({ setup() { return {} } })`. Prohibido un `EntityPage.ts` al lado usado como cuerpo del script.

Script vacío, sin imports ni bindings: el bloque no se agrega solo para existir. Un componente que solo declara props y las pinta no gana un composable vacío.

Los componentes que usa el template se importan en ese bloque.

Computed, handlers, `watch` y llamadas al service van a `composables/useEntityPage.ts`: `use` + el componente, camelCase. El composable recibe props, emit o el ref de `defineModel` ya declarados. No llama a `defineProps`, `defineEmits` ni `defineModel`. No se deja esa lógica en el script para «sacarla si crece». No se migra un repo entero por esta regla: aplica a código nuevo y al componente que se toca.

El orden dentro del composable es el de `04`. Los casos dentro de cada slot están en `26`. Si el edit entra en ese cuerpo, se reordena esa función. La línea en blanco entre secciones es `gian-ts-style`.

## Props y emits

La interface se llama `<Componente>Props` / `<Componente>Emits`, igual que en React (`gian-ts-style`, `react-components-jsx`): `HomePage.vue` → `interface HomePageProps`, `defineProps<HomePageProps>()`, `interface HomePageEmits`, `defineEmits<HomePageEmits>()`. Viven en el `<script setup>` del `.vue`. No se exportan a `features/*/interfaces`. El JSON de la API sigue en `<entity>.interface.ts`.

```ts
interface EntityPageProps {
  entityId: string;
}

const props = defineProps<EntityPageProps>();
```

```ts
interface EntityPageEmits {
  confirm: [];
  cancel: [];
}

const emit = defineEmits<EntityPageEmits>();
```

Prohibido `defineProps<{ entityId: string }>()` y `defineEmits<{ confirm: [] }>()`. Prohibido `interface Props` / `interface Emits` sin el nombre del componente.

Sin destructurar: se lee `props.entityId` y se llama `emit('confirm')`. El destructurado reactivo de Vue 3.5 no se usa por rutina: pasar la variable a `watch` o a un composable pide un getter.

Defaults: `withDefaults(defineProps<EntityPageProps>(), { ... })`.

El template usa los nombres que expone `defineProps`. `$props` solo si hay colisión de nombre.

## v-model, overlays y computed

- `defineModel` solo para un `v-model` real (Vue 3.4+). Un overlay sigue con `isOpen` más emit (`09`).
- El overlay dueño de su mutación se monta con `v-if`, no con `v-show` (`09`).
- `computed` sigue los casos A–E de `23`, y vive en el composable. Una `const` derivada de props en `script setup` no es reactiva. A: la expresión va en el template, o en un `computed` del composable si el script la usa. C: `computed` con `if` y early return. D: `v-if` / `v-else-if` en el template.
- `<style scoped>` se queda en el `.vue`, con el template.
- Componentes en PascalCase en el template. Emits en camelCase en `interface <Componente>Emits`.
- `defineSlots` es obligatorio si el componente renderiza un slot con props. `defineExpose` es obligatorio si un padre usa un ref al componente. `generic="T"` cuando una prop, emit o slot depende de un tipo que elige el padre. Sus tipos (`interface <Componente>Slots`, la forma de `T`) son locales, igual que `<Componente>Props`. `generic="T"` va en la etiqueta `<script setup>` del `.vue`.
- Clases condicionales: `:class` con array u objeto (`:class="['flex', { 'font-semibold': isActive }]"`). Prohibido interpolar o concatenar clases (`23`).

```vue
<script setup lang="ts">
import { useEntityPage } from '../composables/useEntityPage';

interface EntityPageProps {
  isLoading: boolean;
}

interface EntityPageEmits {
  searchCleared: [];
}

const props = defineProps<EntityPageProps>();
const emit = defineEmits<EntityPageEmits>();
const search = defineModel<string>('search', { required: true });

const { summary, onClear } = useEntityPage(props, emit, search);
</script>
```

```ts
import { computed, type Ref } from 'vue';
import { useI18n } from 'vue-i18n';

interface UseEntityPageProps {
  isLoading: boolean;
}

interface UseEntityPageEmits {
  (event: 'searchCleared'): void;
}

export const useEntityPage = (
  props: UseEntityPageProps,
  emit: UseEntityPageEmits,
  search: Ref<string>,
) => {
  const { t } = useI18n();

  const summary = computed(() => {
    if (props.isLoading) return t('orders.summary.loading');
    if (search.value) return t('orders.summary.filtered', { search: search.value });
    return t('orders.summary.all');
  });

  const onClear = () => {
    search.value = '';
    emit('searchCleared');
  };

  return { summary, onClear };
};
```

Tipos del composable, forma fija:

- `interface <Composable>Props` (`useEntityPage` → `UseEntityPageProps`) repite el shape de `<Componente>Props`.
- `interface <Composable>Emits` declara una call signature por cada evento de `<Componente>Emits`: `searchCleared: []` → `(event: 'searchCleared'): void`; `select: [id: string]` → `(event: 'select', id: string): void`.
- Prohibido tipar `props` o `emit` del composable con `any`, un genérico anónimo o una firma inline.

## Delta de nombres

Solo cambia la carpeta. El resto es `03` y `04`.

| Pieza | Vue |
|---|---|
| Composables | `composables/useEntityPage.ts` (`use` + componente, camelCase). Nunca `use-thing.ts` ni `hooks/` |
| SFC | `EntityPage.vue`. El script setup va dentro |
| Props / emits | `interface EntityPageProps` / `interface EntityPageEmits`, locales |
| Tipos del composable | `interface UseEntityPageProps` / `interface UseEntityPageEmits` |

El call site llama al método de la clase de área (`DateHelper.formatCalendarDate`). Sin función local que arme fecha, número, dinero o etiqueta. Sin una segunda función al lado de la clase para la misma área.

## i18n

En la vista, `t()` de `useI18n` o `$t`. Fuera de la vista, `i18n.t()` (`15`). No inyectar la función de traducción.

## Styling y datos

Tailwind en el template (`class`) si el repo lo usa. No exigir Tailwind, `cn()`, MUI ni `sx` si el repo no los tiene. Las clases condicionales usan `:class` con array u objeto en cualquier caso. Prohibido interpolar o concatenar clases.

No instalar Vue Router, Pinia ni TanStack Vue Query porque un ejemplo los use. El server state es el cliente de datos que el repo ya tiene (`01`). El service sigue `14`.

## No copiar de un repo de referencia Vue

- `defineComponent` + `return`
- un archivo por función (`get-thing-by-id.ts`). El área sigue en `<entity>.helper.ts`
- `*.response.ts` en lugar de `<entity>.interface.ts`
- barrel `interfaces/index.ts`
- cliente HTTP como default export suelto si el repo ya tiene service
- `$props` cuando el nombre de la prop ya está expuesto

## Checklist

- [ ] Núcleo cargado (`01`); este archivo solo suma el delta
- [ ] `.vue` con `<script setup lang="ts">` inline. Sin `src`. Solo macros, imports y la llamada al composable
- [ ] `interface <Componente>Props` / `interface <Componente>Emits`; sin genérico anónimo ni `interface Props` suelto
- [ ] `const props = defineProps<EntityPageProps>()` y `const emit = defineEmits<EntityPageEmits>()`, sin destructurar
- [ ] Composable con `interface <Composable>Props` (mismo shape) e `interface <Composable>Emits` (call signatures de `<Componente>Emits`)
- [ ] `defineModel` solo para un `v-model` real; overlay con `isOpen` + emit, montado con `v-if`
- [ ] `computed` según A–E de `23`
- [ ] `<style scoped>` en el `.vue`; componentes PascalCase en el template; emits camelCase
- [ ] `defineSlots` si renderiza un slot con props; `defineExpose` si un padre usa un ref; `generic="T"` si el padre elige el tipo; con `interface <Componente>Slots` local
- [ ] Clases condicionales con `:class` array u objeto; sin interpolar ni concatenar
- [ ] Computed, handler, `watch` o llamada al service en `composables/useEntityPage.ts`. El script inline no los contiene
- [ ] Orden del composable según `04`; línea en blanco entre secciones según `gian-ts-style`
- [ ] clase de área (`23`); sin wrapper local ni función suelta de la misma área
- [ ] enums según `07`; forma de objeto según `gian-ts-style`
- [ ] formato del `<script setup>` y de los composables `.ts` según `gian-ts-style`
