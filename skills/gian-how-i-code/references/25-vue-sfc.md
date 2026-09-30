# 25 — Vue SFC

Cargar cuando: el repo es Vue, o se crea, edita, audita o consulta un `.vue` o su `.ts` hermano.

Este archivo es el **adaptador**. El núcleo sigue vigente (`01`): nombres, helpers de área, enums, contratos, errores, display. No heredar MUI, RHF, `hooks/` ni React Query. Eso no apaga el núcleo.

Los nombres los elige el núcleo (`04` Naming, `23`). La forma del binding (no destructurar por rutina, `import type`, flechas, llaves) es `gian-react-ts-style`. Una forma de objeto propia es `interface` ahí (`interface-object-shape`), no una regla de este archivo. Conjuntos cerrados y uniones: `07`.

## SFC partido

SFC con lógica: el `.vue` conserva el template y el style. El script vive en un hermano con el mismo basename PascalCase.

```vue
<script setup lang="ts" src="./EntityPage.ts"></script>

<template>
  ...
</template>
```

El `.ts` es el cuerpo de `script setup`: imports, `defineProps` / `defineEmits`, composables y computeds. Esos bindings quedan visibles en el template. Sin `export default` y sin `return`.

El atributo `setup` es obligatorio. Prohibido el hermano como `export default defineComponent({ setup() { return {} } })`.

Script vacío, sin imports ni bindings: no gana archivo.

Los componentes que usa el template se importan en el `.ts`.

## Props y emits

`interface Props` e `interface Emits` viven en el `.ts` del componente. No se exportan a `features/*/interfaces`. El JSON de la API sigue en `<entity>.interface.ts`.

```ts
interface Props {
  entityId: string;
}

const props = defineProps<Props>();
```

```ts
interface Emits {
  confirm: [];
  cancel: [];
}

const emit = defineEmits<Emits>();
```

Prohibido `defineProps<{ entityId: string }>()` y `defineEmits<{ confirm: [] }>()`.

Defaults: `withDefaults(defineProps<Props>(), { ... })`.

El template usa los nombres que expone `defineProps`. `$props` solo si hay colisión de nombre.

## Delta de nombres

Solo cambia la carpeta. El resto es `03` y `04`.

| Pieza | Vue |
|---|---|
| Composables | `composables/useThing.ts` (camelCase). Nunca `use-thing.ts` ni `hooks/` |
| SFC | `EntityPage.vue` + `EntityPage.ts` |
| Props / emits | `interface Props` / `interface Emits`, locales |

El call site llama al método de la clase de área (`DateHelper.formatCalendarDate`). Sin función local que arme fecha, número, dinero o etiqueta. Sin una segunda función al lado de la clase para la misma área.

## i18n

En la vista, el helper de `vue-i18n`. Fuera de la vista, `i18n.t()` (`15`). No inyectar la función de traducción.

## Styling y datos

Tailwind en el template (`class`) si el repo lo usa. No exigir Tailwind, `cn()`, MUI ni `sx` si el repo no los tiene.

No instalar Vue Router, Pinia ni TanStack Vue Query porque un ejemplo los use. El server state es el cliente de datos que el repo ya tiene (`01`). El service sigue `14`.

## No copiar de un repo de referencia Vue

- `defineComponent` + `return` en el hermano
- un archivo por función (`get-thing-by-id.ts`). El área sigue en `<entity>.helper.ts`
- `*.response.ts` en lugar de `<entity>.interface.ts`
- barrel `interfaces/index.ts`
- cliente HTTP como default export suelto si el repo ya tiene service
- `$props` cuando el nombre de la prop ya está expuesto

## Checklist

- [ ] Núcleo cargado (`01`); este archivo solo suma el delta
- [ ] `.vue` con `<script setup lang="ts" src="./Nombre.ts">` si hay lógica
- [ ] `interface Props` / `interface Emits`; sin genérico anónimo
- [ ] `composables/useThing.ts`
- [ ] clase de área (`23`); sin wrapper local ni función suelta de la misma área
- [ ] enums según `07`; forma de objeto según `gian-react-ts-style`
- [ ] formato del `.ts` según `gian-react-ts-style`
