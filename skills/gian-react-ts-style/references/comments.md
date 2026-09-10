# Comments

## comments-noise (HARD WRITE)

Código autoexplicativo: nombres, no comentarios. WRITE no emite `//`, `/* */`, ni `/** */` (JSDoc). Si el usuario pide un comentario en el hilo, gana esa instrucción.

Incluso un “why” se prefiere eliminar si el código/abstracción puede hacer explícita la intención.

| Sitio | WRITE | FIX (hunk pedido) | AUDIT |
|---|---|---|---|
| JSDoc ceremonial / que narra la firma | no emitir | borrar | FAIL |
| `//` que narra el código (`return the user`, `get data`) | no emitir | borrar | FAIL |
| why no-obvio intra-cuerpo | no añadir | **conservar** | no FAIL (GAP si dudoso) |
| Directives (abajo) | no inventar | **conservar** | no FAIL |

`jsdoc-no-default` está subsumido en este ID (como `comments-phpdoc` en PHP).

## NEVER strip (tooling / contrato)

No son “comentarios de estilo”. Conservar exactamente:

- `@ts-expect-error` / `@ts-ignore` / `@ts-nocheck`
- `eslint-disable` / `eslint-disable-next-line` (con causa legítima)
- `prettier-ignore`
- pragmas de bundler (`webpackChunkName`, vite)
- generated markers (`@generated`, codegen headers)
- licenses / copyright file headers

No inventar más excepciones sin evidencia.

Los `// BEFORE` / `// AFTER` de evals de esta skill son marcadores de fixture, no estilo de producción.
