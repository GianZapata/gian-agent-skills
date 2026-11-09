# Comments

## comments-noise (HARD)

Código autoexplicativo: nombres, no comentarios. WRITE no emite `//`, `/* */`, `/** */` (JSDoc) ni `{/* */}` en JSX. Tampoco un "why". Si el usuario pide un comentario en el hilo, gana esa instrucción.

FIX conserva un comentario existente solo si está en esta lista cerrada:

- referencia a un ticket, issue o bug externo (id o URL);
- workaround de una librería, con nombre y versión;
- requisito legal o de negocio que el código no puede expresar;
- directives (abajo).

Todo lo demás se borra: narración, JSDoc que repite la firma, comentarios de sección, código comentado.

| Sitio | WRITE | FIX (alcance) | AUDIT |
|---|---|---|---|
| JSDoc ceremonial / que narra la firma | no emitir | borrar | FAIL |
| `//` o `{/* */}` que narra el código (`return the user`, `get data`) | no emitir | borrar | FAIL |
| Comentario de sección (`// State`, `{/* Header */}`) | no emitir | borrar | FAIL |
| Código comentado | no emitir | borrar | FAIL |
| Comentario de la lista cerrada | no emitir | **conservar** | no FAIL |
| `TODO` / `FIXME` / `HACK` | no emitir, salvo `TODO(datos)` (`gian-how-i-code` `15`) | conservar solo con ticket o `TODO(datos)`; el resto se borra | FAIL sin ticket ni `TODO(datos)` |
| Directives | no emitir | **conservar** | no FAIL |

Los `{/* */}` de JSX siguen la misma tabla.

`jsdoc-no-default` está subsumido en este ID (como `comments-phpdoc` en PHP).

## Directives (NEVER strip)

No son comentarios de estilo. Lista cerrada, se conservan exactamente:

- `@ts-expect-error` / `@ts-ignore` / `@ts-nocheck`
- `eslint-disable` / `eslint-disable-next-line` / `eslint-enable`
- `prettier-ignore`
- triple-slash `/// <reference … />`
- pragmas de bundler (`webpackChunkName`, `@vite-ignore`)
- generated markers (`@generated`, headers de codegen)
- licenses / copyright file headers

WRITE no añade directives. Fuera de esta lista no hay excepción.

Los `// BEFORE` / `// AFTER` de evals de esta skill son marcadores de fixture, no estilo de producción.
