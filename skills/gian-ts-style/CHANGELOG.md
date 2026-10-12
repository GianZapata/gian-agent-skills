# Changelog

## 2.6.0 — 2026-10-12

- `self-check.mjs` marca FAIL (antes GAP o nada): `enum-ownership` (unión de strings propia; detecta cuando repite un enum que ya existe, resolviendo los imports con el `tsconfig` del repo), `library-shadow-type` (unión de colores, variants, sizes o severities de MUI), `named-interface` (objeto inline con 2+ campos), `interface-object-shape`, `display-meta-location` (Record o copy de opciones en un `.tsx`) y `parallel-meta` (dos Records por la misma key).
- `types-imports.md`: §Named interface y §Library and enum types. `SKILL.md`: línea de tipos en Hard Rules.

## 2.5.0 — 2026-10-12

- `assets/self-check.mjs` (nuevo): verificador con el parser de TypeScript del repo. Revisa las funciones tocadas en `git diff HEAD` (o `--all`): `slot-order`, `vertical-spacing`, `read-group`, `guard-glue`, `single-statement-if`, `arrow-implicit-return`, `classname-cn`, `boolean-prop-shorthand`, `fragment-shorthand`, `self-closing-jsx`, `handler-naming`, `data-hook-location`, `no-local-style-constants`, `comments-noise`; GAP para `enum-ownership` y bloques repetidos. WRITE y FIX no cierran sin su salida. Antes el cierre pedía un `self-check.sh` que no existía.
- `vertical-spacing` pasa a HARD con lista cerrada de secciones: dos slots distintos nunca van pegados; una sentencia multilínea cierra con línea en blanco; función, efecto o `useMemo` con cuerpo llevan blanco antes y después; derivadas agrupadas por fuente. Nuevo § Dentro de un bloque: pasos de `26` y `guard-glue` (el guard queda pegado a su lectura). Ejemplo React y ejemplo "No".
- La línea de `SKILL.md` ya no dice "del mismo tipo": nombra los slots de `04`, para que funcione sin abrir la reference.

## 2.4.0 — 2026-10-12

- `read-group` (HARD, `vertical-spacing.md`, `SKILL.md`, audit): cada lectura (query en un componente, hook o composable; `await` que trae datos en una función plana; un `await` que escribe es efecto) abre su grupo y una línea en blanco lo cierra. Su complemento de una línea (ids, `Map` por id) va pegado debajo. Dos lecturas solo van pegadas si la segunda es complemento de la primera. Las mutations de una línea siguen juntas entre ellas. Una lectura multilínea cierra con línea en blanco antes de su complemento; solo el guard que la valida queda pegado.

## 2.3.0 — 2026-10-09

- `react-component-fc-props`: la interface se llama `<Componente>Props` (`HomePage` → `HomePageProps`). `Props` a secas, una abreviatura o el nombre de otro componente es error; FIX la renombra en el componente tocado. Cada componente del archivo tiene la suya. El ejemplo de drawer usa `isOpen` (`gian-how-i-code` `09`).

## 2.2.0 — 2026-10-09

- `classname-cn` (HARD, solo React): en el hunk tocado, `className` con template literal, `+`, ternario, join o prop `className` se escribe con el `cn` del repo. No se crea otro ni se importa `clsx`/`twMerge` directo. `rg` de cierre sobre los `.tsx` tocados. GAP si el repo no tiene `cn`. Tailwind vs `sx` y las constantes de styling siguen en `gian-how-i-code` `04`/`23`.

## 2.1.0 — 2026-10-09

- `react-component-fc-props` (HARD, solo React): props en `interface Props` local y componente `export const X: FC<Props> = ({ … }) => { return … }`; sin props, `FC`. `import type { FC }`, no `React.FC`. Aplica al componente nuevo o tocado. GAP en genérico, `forwardRef`, `memo` con comparador y lint que prohíbe `FC`. Reemplaza el GAP match-file.

## 2.0.2 — 2026-10-05

- `vertical-spacing`: los slots siguen en `04`. Los casos dentro de cada slot, y el orden de una función plana, los decide `26`. Esta reference solo inserta la línea en blanco.

## 2.0.1 — 2026-10-05

- `vertical-spacing`: la cita del orden sigue a `04`. Efectos al final. Si el edit entra en el cuerpo, `04` reordena esa función. La línea en blanco sigue en el hunk.

## 2.0.0 — 2026-09-30

- Renombrada desde `gian-react-ts-style`. El núcleo es TypeScript y vale en React, Vue, Angular y Node. JSX queda como sección solo React.
- `vertical-spacing`: una línea en blanco entre secciones. Declaraciones cortas del mismo tipo juntas. Sin comentarios de sección.

## 1.1.0 — 2026-09-30

- Alcance: cualquier stack TS. Vue (hermano `.ts` y `<script setup lang="ts">`) sin reglas JSX ni `react-component-*`; Angular: clases, decoradores y DI son GAP o `LIBRARY_OWNED`; Node: funciones libres con `exported-arrow-default`, clases Nest/Express GAP. `.js`/`.jsx`/`.mjs`/`.cjs` fuera.
- `access-destructuring`: Vue usa `const props = defineProps<Props>()` y `const emit = defineEmits<Emits>()` sin destructurar.
- `derived-multi-branch`: solo define la forma (cadena de `if` con `return`). `useMemo`/`computed` lo decide `gian-how-i-code` `23`.
- `prettier-eslint-boundary`: no pelear ni instalar `eslint-plugin-vue` ni `@angular-eslint`.

## 1.0.1 — 2026-08-17

- Description: visual-format work vs consult-only architecture/policy. No change to WRITE/AUDIT/FIX rules.

## 1.0.0 — 2026-08-13

- Skill canónica de sintaxis/estilo TS/TSX. Autoridad visual; no arquitectura (`gian-how-i-code`).
- Modos WRITE / AUDIT / FIX espejo de `gian-php-style`: WRITE/FIX corrigen el hunk; AUDIT no edita.
- SAFE FIX vs AST-SENSITIVE (gate) vs NEVER AUTOFIX/GAP.
- Prettier manda wrapping mecánico. No instalar ni reconfigurar ESLint.
