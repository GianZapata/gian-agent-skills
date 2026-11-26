# 33 — Moldes frontend compartidos

Cargar cuando: se toca `src/shared`, `schemas/shared`, o un archivo de este kit (`DateHelper`, `FormHelper`, `FormDataHelper`, `HumanFormatsHelper`, `NumberHelper`, `createEmailSchema`, `useExport`, `error-response`).

Estas piezas se copian entre paneles. Una copia se queda atrás (sin el método nuevo, o sin el test) y un fix no llega a las demás. Regla general (HARD): si el eje ya existe, se extiende esa clase. No se crea otra. Si la copia divergió, el delta se reporta; no se reescribe el otro repo sin pedirlo. Extraer un paquete es PROP (`19`).

## 1. Dos familias, sin mezclarlas

- Paneles (React + TanStack Router). La copia de métodos es `fortezza-panel-admin`. Los tests que esa copia no trajo siguen siendo obligatorios y viven en `elcaba-panel-admin`.
- Next. De ese árbol solo se toma el schema de correo (§2). `entity-query` / `entity-mutation` y un helper que muta el DOM (`e: any`) no son molde.

No se mezclan las dos familias en una tarea.

## 2. Correo (HARD)

`createEmailSchema({ requiredMessage, invalidMessage, maxLength, lengthMessage, lowercase })` sobre un patrón único, con `trim`. Los mensajes los pone quien llama. `lowercase` es opcional.

Prohibido un schema compartido que nombre el producto (`nombre@elcaba.com`, `nombre@fortezza.test`). El ejemplo neutro es `nombre@ejemplo.com`.

El test viaja al lado (`email.schema.test.ts`). Acepta espacios alrededor, `+`, apóstrofe y guion. Rechaza vacío, acento, punto doble, punto al inicio y dominio con guion bajo. El valor parseado es el `trim`. Si varios schemas usan la factory, un caso comprueba que siguen aceptando y que el mensaje es el del caller. No se copia la tabla de casos en cada schema.

En Laravel el mismo campo lleva un mensaje por regla (`32` §7), no uno genérico.

## 3. Kit de paneles

Helpers: `date`, `form`, `form-data`, `human-formats`, `number`, `parser`, `phone`, `sort`, `query-invalidation`, `with-availability-default`. Schemas: `human-name`, `phone`, `strong-password`, `password-with-confirmation`, `entity-id`. También `useExport`, `error-response.interface`, `table.interface`, `create-table-store`, `route.util`.

`BrandMark` y `payment-brands` son del producto: no se portan.

Antes de crear un helper en `shared/`, buscar el eje (`23`). Si existe, se extiende. Un método que solo está en la copia nueva (`HumanFormatsHelper.fileSize`, `humanReadableCompactMoney`, `NumberHelper.fixedDecimal`) se reporta como faltante en las copias viejas.

Cambiar el tipo de id (`number` o string, `entity-id.schema`) es la adaptación permitida, y se declara. No es un helper nuevo.

## 4. Tests

Cada archivo del kit lleva el test al lado (`form.helper.test.ts` junto a `form.helper.ts`). Vitest, `describe` por comportamiento. Copiar la pieza y dejar el test es Media si el archivo se toca, Baja si solo se audita.

Un método nuevo no cierra sin el caso que fija su salida. La forma de `trimOnBlur`: llama `onChange` con el valor limpio, y no lo llama si ya estaba limpio.

El resto de cuándo hace falta un test está en `17`.
