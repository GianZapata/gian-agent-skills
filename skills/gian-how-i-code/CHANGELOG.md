# Changelog

## 1.4.52 — 2026-11-25

- Nueva `31-form-controls-ux`: matriz dato × número de opciones × contexto (formulario de página, dialog/drawer, barra de filtros, edición inline), ayudas ágiles con su disparador (slug autogenerado con check en vivo contra un endpoint existente, dominio con adornment y preview, dinero/unidades, default visible desde migración → modelo/FormRequest → seeder → supuesto, máscaras, fechas con presets y min/max), aplicar en un formulario nuevo vs PROP en uno existente, componente ausente → `19` sin instalar, severidad de auditoría.
- `10`: la tabla de controles y la preferencia de picker se mueven a `31`; un widget existente que no encaja se propone, no se ignora.
- `24` categoría «Control de formulario / ayudas ágiles»; `30` §2 apunta a `31`.
- Evals: audit +5 (53), implementation +1 (75).

## 1.4.51 — 2026-11-25

- Evals: `impl-drop-ceremonial-usememo` contradecía el caso C (`displayFile` tiene 3 ramas). Ahora usa un `useMemo` ceremonial real (una expresión sin ramas); `displayFile` pasa al nuevo `impl-keep-case-c-usememo`, que espera conservar `useMemo<DisplayFile | null>`.

## 1.4.50 — 2026-11-25

- `23` Memoización: el caso C incluye el booleano que junta 3+ partes con `&&` / `||` (`useMemo<boolean>` + `if`, ejemplo `showClearLogo`). Revierte la regla de 1.4.49 «booleano de 3+ partes → `const` con nombre por parte»: fila de §Lógica en JSX, bloque Mal/Bien y severidad.
- `23`: todo `useMemo` lleva genérico explícito (`useMemo<T>`) para que TypeScript marque la rama que no devuelve `T`; ejemplos C actualizados; severidad Media.
- `23` §Copy que repite un valor: se separa valor de frase; el valor configurable sale a constante, el copy puro queda inline (ejemplo `logoStatusHint`).
- `SKILL.md`: líneas Memo y Composición alineadas.
- Evals: `audit-long-boolean-condition` reescrito; nuevos `audit-usememo-missing-generic`, `audit-hint-hardcoded-config`.

## 1.4.49 — 2026-11-25

- `23` §Contraste con el backend (HARD, Implementar + Auditar): todo valor de regla del servidor que la UI muestra o valida se corrobora contra FormRequest/config/enum de la API con `archivo:línea` o «sin verificar»; paridad campo a campo, enums exhaustivos, defaults iguales, una sola fuente exportada con comentario de fuente; alinear a una regla que el backend ya aplica no es PROP; filas de severidad Alta/Media.
- `23` §Lógica en JSX: booleano de 3+ partes → `const` con nombre por parte; `useMemo` (C) queda para 3+ ramas.
- `21`: línea `Contraste backend` en el cierre de Implementar y Auditar. Punteros en `06`, `07` (checklist 6), `10`, `24` §4.1 (columna Fuente backend).
- Evals `impl-upload-limits-from-backend`, `audit-ui-values-vs-backend`, `audit-long-boolean-condition`, `audit-enum-parity-backend`, `audit-default-drift-backend`.

## 1.4.48 — 2026-11-25

- `13` §Pasar una query a un componente: si un componente usa 2+ piezas de la misma query, recibe el objeto completo (`UseQueryResult<T, CustomError>`, sin `Pick`); el padre elige el objeto una vez en vez de repetir el ternario por pieza; excepción para componentes genéricos de `shared/`. rg de auditoría, hallazgo Media, ítem de checklist, puntero en `04` §Composición y Hard Rule en `SKILL.md`.
- Evals `impl-pass-whole-query`, `audit-split-query-props`.

## 1.4.47 — 2026-11-25

- `23` §URLs blob: descarga con `FileHelper.download`, preview con `useObjectUrl` (crea al cambiar, revoca en cleanup); prohibido `createObjectURL`/`revokeObjectURL` a mano o URL en `useState` + efecto propio. rg de auditoría, fila de severidad Media y Hard Rule en `SKILL.md`.
- Evals `impl-blob-preview-hook`, `audit-manual-object-urls`.

## 1.4.46 — 2026-11-25

- `12` §Efectos: un efecto solo sincroniza con algo externo; tabla de reemplazos (derivado en render, reset con `{isOpen && <X />}` o `key`, reset o aviso en el handler, sin props token para disparar resets). Severidad Media y rg de auditoría.
- `23` §Casts que apagan el tipado: `as any`, `as unknown as` y `as never` prohibidos; corrección en el origen; forms con `useForm<z.input, unknown, z.output>`; excepción con comentario. Fila de severidad Media y puntero desde `10` §Stack.
- Hard Rules «Efectos» y «Casts» en `SKILL.md`. Evals `impl-effect-reset-by-mount`, `impl-form-resolver-no-cast`, `audit-effects-and-casts`.

## 1.4.45 — 2026-11-25

- `04` §Carpeta del componente gana «Dónde vive cada subcomponente» (carpeta del ancestro común más cercano, árbol completo, lo público fuera; ejemplo `components/layouts`) y «Funciones de un árbol de componentes» (privada en el padre con props, sin `.util.ts`; archivo de componente solo exporta componentes; función que devuelve JSX → componente). Dos filas de severidad, puntero desde `23` §Funciones locales y línea en la Hard Rule «Composición».
- Evals `impl-subcomponent-common-ancestor`, `impl-tree-function-no-util`, `audit-loose-layout-children`.

## 1.4.44 — 2026-11-25

- `04` §Carpeta del componente: al tocar un archivo, si el cambio lo deja con 2+ componentes privados, pasa a carpeta en el mismo cambio aunque los otros no sean tuyos (límite: ese archivo; vale también en `components/layouts` y `components/shared`). Fila de severidad Media y línea en la Hard Rule «Composición».
- Eval `impl-touched-file-folder`.

## 1.4.43 — 2026-11-25

- `07` §Checklist al declarar gana el punto 5: un valor de una entidad de otra feature usa el enum y el meta de la feature dueña (`ContractHelper.statusMeta`) y el payload se tipa con ese enum; prohibido el Record de labels local, `Record<string, string>` o cast; si la API devuelve otro conjunto, se verifica en la API antes de crear un enum propio. Fila de hallazgo en §Hallazgos típicos y línea en la Hard Rule de ownership.
- Evals `impl-cross-feature-status-meta` y `audit-cross-feature-status-labels`.

## 1.4.42 — 2026-11-25

- Nueva `30-screen-audit`: auditoría por pantalla en 7 pasos (quién y para qué, cada elemento contra la pregunta, lenguaje, acciones coherentes, densidad y jerarquía, estados, visto en vivo), severidades y formato de hallazgo con «visto en vivo / leído, no visto».
- Hard Rule «Pantalla coherente» y fila de routing en `SKILL.md`; punteros en `11` §Tablas resumen y `15` §Copy; `24` gana categoría «Pantallas» (por pantalla) y su línea de cobertura; `00-index` fila 30.
- Evals `screen-audit-action-coherence`, `screen-audit-technical-term`, `screen-audit-table-density`.

## 1.4.41 — 2026-11-25

- `24` gana §4.1 «Comparación entre archivos»: Pasada 1 arma cuatro tablas (constantes, enums y labels, funciones locales agrupadas por nombre y propósito, constantes sin consumidores); Pasada 2 compara cada archivo contra ellas, con un hallazgo por grupo de funciones duplicadas. §4.2 «Cobertura por eje»: barrido textual y lectura se reportan por separado; una cifra que los mezcla es `audit_incomplete`. Gate actualizado.
- `23` §Valores: el drift se corrige a un solo valor (el usuario decide cuál; follow-up cruzado con la API; datos guardados no se migran); constante sin consumidores → borrar (Baja). §Duplicación: misma función local en 2+ archivos sin helper previo = Media.
- Evals `audit-cross-file-local-functions`, `audit-coverage-per-axis`, `audit-drift-single-value`.

## 1.4.40 — 2026-11-25

- `23` §Duplicación gana «Formato inline»: `toFixed`, `toLocaleString`, `Intl.*Format`, bytes→MB, porcentaje o dinero escritos directo en el componente van al helper del eje (`NumberHelper`, `HumanFormatsHelper`, `DateHelper`); si falta el método, se agrega. Sin helper del eje, se crea en `shared/helpers` con 2+ archivos. Locale y moneda no van en el call site. Filas de severidad, línea en la Hard Rule «Valores» y eval `audit-inline-formatting`.

## 1.4.39 — 2026-11-25

- `23` gana §Valores (Auditar + Implementar): buscar con `rg` antes de declarar; un valor sale del archivo si ya existe, si se usa en 2+ archivos o si es configuración de negocio; orden de ubicación (helper de eje > constantes globales > `features/<f>/constants/`); drift entre fuentes = Alta; un conjunto cerrado repetido va a enum (`07`); el copy que repite un valor se interpola; una función del eje de un helper existente va al helper. Constante de UI de un solo archivo y placeholders: permitidos.
- `23` gana §Lógica en JSX: derivación repetida → helper; expresión larga → `const` (A/B); `useMemo` solo para 3+ ramas o condición de 3+ partes (C), nunca para concatenar.
- `04` gana §Composición: un `.map` con lógica pasa a componente; un bloque JSX repetido 2+ veces pasa a componente con prop de variante; un componente con 3+ secciones se divide; con 2+ subcomponentes privados se crea la carpeta `<Comp>/<Comp>.tsx` sin `index.ts`. `04` regla 4 ahora remite a esta sección. `25` checklist la cita.
- `SKILL.md`: Hard Rules «Valores» y «Composición», y fila de routing. Evals `audit-duplicated-constants-drift`, `audit-component-composition`, `impl-reuse-existing-constant`, `impl-map-row-component`.

## 1.4.38 — 2026-11-24

- `15`: un texto visible de un spec, plan o ticket que el usuario no dictó es una propuesta; pasa por el `rg` de vocabulario al escribirse y al implementarse, y el cierre avisa del cambio. BAD/GOOD genérico.
- `gian-development-workflow` `visual-quality` obligación 12: cada acción muestra su efecto donde el usuario mira (scroll y foco, o no se pone); al arreglar «no pasa nada» se reproduce antes.
- `tools/run-behavior.py`: evals de comportamiento (Grok CLI, cursor-agent, claude) que editan un worktree desechable y califican el diff.

## 1.4.37 — 2026-11-24

- `10`: fila para identificadores con formato fijo (RFC, CURP, CLABE, código postal): string, normalización del valor real, `maxLength` y regex en un campo nuevo (PROP en uno existente), formato visible fuera del placeholder.
- `10`: tabla de control según el número de opciones y fuente del combobox (componente y endpoint del repo; sin ellos, propuesta, no ruta inventada).
- `10` y `21`: una línea por campo antes del edit, y el cierre reporta control, normalización y ayuda.

## 1.4.36 — 2026-11-24

- `15` gana «Vocabulario de arquitectura»: `central`, `tenant`, base de datos, CRUD, módulo y similares no se publican, ni siquiera si vienen del prompt. El término es el que el producto ya usa, sin tabla fija. Incluye BAD/GOOD y un `rg` que solo juzga strings visibles. `21` punto 9 lo cita.
- `10`: excepción para radio cards en un formulario nuevo con 2 a 4 opciones que traen datos que comparar.

## 1.4.35 — 2026-11-18

- Revisión de diseño en Implementar (`22`, `21`, `SKILL.md`): se lee cada archivo tocado completo. Un Alto en lo escrito o tocado se corrige antes de cerrar; lo de fuera se reporta con propuesta. Dos apariciones del mismo bloque son hallazgo (Media si es lógica o regla, Baja si es forma). Nueva sección de dirección de dependencias (Controller, Action, Resource, modelo; componente, helper). El cierre gana el punto 13, Diseño, y `22` entra siempre en References.
- `22` ya no dice «no extraer por una sola duplicación accidental», y `23` registra esa coincidencia como Baja con propuesta.
- `how-i-code` carga por sí misma `gian-php-style` y `gian-ts-style` cuando el cambio escribe PHP o TS. Antes lo hacía el bootstrap del harness.

## 1.4.34 — 2026-11-09

- `05` §Historial de estados: API real de `asantibanez/laravel-eloquent-state-machines` verificada contra el README (`was`, `timesWas`, `whenWas`, `snapshotWhen`, `snapshotsWhen`, `history()` + scopes, `getCustomProperty`, `responsible`, `whereHas{Field}` + scopes, `changedAttributes*`). Prohibido inventar métodos, consultar `state_histories` a mano o pasar strings literales en lugar de constantes de la SM. `postponeTransitionTo` / `hasPendingTransitions` quedan fuera del historial. Checklist BE y routing en `SKILL.md`.

## 1.4.33 — 2026-10-26

- Store y Update de una entidad (`05`): reglas y mensajes en una base abstracta `<Entity>Request`; Store y Update solo implementan `presence()`. Prohibido el loop que inyecta `sometimes`/`required` y el trait para ese par. `unique` vive una vez, con `->ignore($this->route('<param>'))`. Una key anidada no lleva `sometimes`.
- Un bloque de reglas reutilizado por entidades distintas: trait en `app/Traits/Requests/`, sin `rules()` ni `$this->route()`.
- `18`: Alta si `sometimes` cae en una key anidada con `required_with`, o si el Store deja un obligatorio sin `required`. Media si hay loop de presencia, regla redefinida, trait de ese par, o `unique` solo en uno.
- Templates `assets/backend/`: llaves en la misma línea, `handle` en la Action, `use` en lugar de FQCN, y marcadores ADAPTAR como `//`. Requests: `EntityRequest`, `StoreEntityRequest` y `UpdateEntityRequest`.
- `21` §Implementar: el self-check de TS es la última línea de `self-check.mjs`; PHP es `Self-check PHP: manual` más las reglas revisadas en el método tocado.

## 1.4.32 — 2026-10-12

- `26`: la lectura queda inmediatamente arriba del guard. En PHP van pegadas. En TS, un `const`/`let`/`var` de una línea lleva línea en blanco antes de la sentencia siguiente si no es otra declaración.

## 1.4.31 — 2026-10-12

- `26` §Alcance: el self-check revisa esta misma unidad. El detalle queda en `gian-ts-style` `vertical-spacing.md` §Aplicar.

## 1.4.30 — 2026-10-12

- `23` caso C: también un ternario cuya condición junta 3+ partes con `&&` / `||`, aunque tenga dos resultados. `useMemo` + `if` + early return es obligatorio en componente y hook (Vue: `computed`). Ejemplo `orderMessage`. B queda para dos resultados con una condición de 1 o 2 partes. Lo verifica `gian-ts-style` `self-check.mjs`.

## 1.4.29 — 2026-10-12

- `07` §Checklist al declarar (HARD): antes de un `type`, unión, enum, `Record` o constante de opciones, buscar el enum que ya existe en la feature; conjunto propio → string enum; valores de MUI → `XProps['prop']`; varios datos por miembro → una `static readonly Record<Enum, Meta>` en el helper con su interface; objeto inline 2+ campos → interface. Lo verifica `gian-ts-style` `self-check.mjs`.
- Routing: `07` y `08` se cargan siempre que el edit declara un tipo, unión, enum, interface, `Record` o constante de opciones, aunque la tarea no hable de tipos.

## 1.4.28 — 2026-10-12

- `04` §Orden: los slots nombran `useContext`, `useTranslation` y `useQueryClient` (dependencias), `useReducer` y `useForm` (estado), y `useWatch`, `useFieldArray` y `useFormState` (hooks que leen estado). La derivada que un hook recibe como argumento va justo arriba de él y es la única que sube. La línea en blanco entre slots es HARD y la verifica `gian-ts-style` `assets/self-check.mjs`.

## 1.4.27 — 2026-10-12

- `26` §Cargar: las lecturas que no se necesitan entre sí ya no son "el mismo paso" pegado. Cada lectura es su grupo visual; la línea en blanco la pone `read-group` de `gian-php-style` 1.3.0 / `gian-ts-style` 2.4.0. Los ejemplos PHP y React de `26` separan cada lectura.

## 1.4.26 — 2026-10-09

- `no-local-style-constants` (`04`, `23`, `SKILL.md`): también cubre los strings de clases (`const cardClass = '…'`). Las clases van inline con `cn()`; si el bloque se repite, se extrae un componente. Template literal, concatenación, ternario o join en `className` → el `cn()` del repo. La mecánica por hunk vive en `gian-ts-style` 2.2.0 (`classname-cn`).

## 1.4.25 — 2026-10-09

- Ejemplos de componente en `04` y `26` anotados con `FC`, como exige `gian-ts-style` 2.1.0.

## 1.4.24 — 2026-10-09

- Detectar y avisar (`15`, `21`, `SKILL.md`, workflow, `visual-quality`): la falta de datos no bloquea ni se pregunta. Se implementa con una constante y `TODO(datos)`, y el plan y el cierre listan *Sin datos todavía* (con `archivo:línea`) y *Texto de la referencia que no publiqué*, aunque nadie lo pida. Antes de cerrar, `rg` de rótulos sobre los archivos tocados.

## 1.4.23 — 2026-10-09

- Referencia ≠ producto (`15`, `08`, `18`, `SKILL.md`, workflow, `visual-quality`): el nombre de la referencia, la fase, "Mock", "Muestra" y las notas de entrega no se publican. El título nombra la tarea. Sección sin datos: constante + `TODO:` en código, nada visible. Lo que está fuera de alcance no se monta.

## 1.4.22 — 2026-10-05

- Valor fijo de prueba (`15`, `01`, `SKILL.md`): un teléfono, correo, id o URL fijo que no es el del registro va en el request, el dial o la config. La pantalla no anuncia el desvío ni el guion de la prueba. Al tocarlo se quita el aviso; el cableado se queda.

## 1.4.21 — 2026-10-05

- Carga (`26`): las lecturas consecutivas que no se necesitan entre sí son el mismo paso. La que usa el resultado de la anterior va debajo.
- Cierre React (`gian-development-workflow`): el cuerpo de un componente, hook o composable se reordena con los slots de `04` y los casos de cada slot en `26`.

## 1.4.20 — 2026-10-05

- Orden dentro de la función (`26`, `04`, `05`, `25`, `SKILL.md`): un método PHP y una función plana siguen el rol (normalizar, guards, cargar, decidir, derivar, efecto, return). En un componente, hook o composable los slots siguen en `04` y los casos de cada slot en `26`. Si el edit entra en esa función, se reordena. El otro método o el otro componente no.

## 1.4.19 — 2026-10-05

- Orden del cuerpo (`04`, `SKILL.md`): dependencias que no leen estado local, estado, hooks que leen ese estado, variables derivadas, funciones, efectos al final, return. Si el edit entra en ese cuerpo, se reordena esa función. No el archivo ni el otro componente.
- Carga con forma (`04`, `15`, `SKILL.md`): si la espera ocupa el lugar de una tarjeta, lista, ficha o gráfica, el placeholder es un skeleton. El párrafo «Cargando…» no.

## 1.4.17 — 2026-10-02

- Superficie de captura (`10`, `15`, `14`, `05`, `SKILL.md`): que el sistema compruebe, calcule o limite no autoriza publicarlo. El éxito y el estado normal no se anuncian. Si hace falta señalar, es un icono, y no siempre. El fallo que hay que corregir sí lleva el mensaje. Sin botón de comprobar si el campo ya consulta, sin segundo envío al lado de Guardar, sin título que repite la única etiqueta, sin descargo de lo que Guardar no hace.

## 1.4.16 — 2026-10-01

- Caso de uso backend (`05`, `SKILL.md`, `24`, `18`): la Action garantiza el caso al crear, modificar o auditar, aunque tenga una línea. El flujo es FormRequest antes del Controller. `render()` no revierte escrituras. Cuatro conclusiones, sin cupo mínimo. La ausencia de una regla extra no es decisión pendiente por sí sola.

## 1.4.15 — 2026-10-01

- Copy (`15`, `14`, `SKILL.md`): el copy de operador se corrige por defecto y después se informa. Solo se propone, sin editar, si el usuario pidió solo analizar o no modificar archivos. Un término de dominio se conserva.

## 1.4.14 — 2026-10-01

- Copy (`15`, `14`, `SKILL.md`): se juzga por audiencia y función, no por palabra prohibida. Un término de dominio se conserva. El copy de operador ya escrito se propone, no se reescribe al tocar. No se inventa causa ni plazo. “Más tarde” no es el mensaje de todo error.
- Idioma (`05`, `14`): mensajes visibles en el idioma soportado del usuario y el fallback del proyecto. `code`, status y claves de campo quedan estables.
- `18`: “Convención” sale de la tabla de severidad. La gravedad depende del impacto, la frecuencia y el riesgo sustentados por evidencia.

## 1.4.13 — 2026-10-01

- Copy visible (`15`, `14`): título, descripción, vacío, error, toast y ayuda le hablan a quien usa el producto. No nombran API, servidor ni piden operarlo. Al tocarlo, se reescribe.

## 1.4.12 — 2026-10-01

- Ayudas de captura (`10`): evaluar es obligatorio; implementar no. Local y asíncrona se separan. Cada ayuda declara solo lo que necesita. La corrección manual gana, y se señala si dejó de ser coherente. El dominio del email puede ir en minúsculas; la parte local es decisión de producto.
- `05`: no se borra una clase solo porque declara constructor. Adaptador si la integración la exige, no solo si hay `new`. `Support` es convención, no Alta automático (`18`).
- Transacción y error (`05`): dueño de la operación, savepoint en la misma conexión, `throw` para revertir, `CustomException` se lanza, reintento de deadlock se conserva hasta agotarlo, idempotencia operable, colisión al guardar, efectos externos por flujo.

## 1.4.11 — 2026-10-01

- Laravel (`05`): antes de crear el archivo se decide el lugar. No se agrega a `Support` porque la carpeta ya existe. Config, modelo, enum, helper estático, adaptador de paquete, método privado o fixture. Prohibida una clase cuyo único miembro es el constructor.

## 1.4.10 — 2026-10-01

- Laravel (`05`): si el repo ya tiene `Support`, no es el molde y una feature nueva no agrega archivos ahí. La forma a copiar es Action `handle`, método privado en la Query, y helper estático en `Helpers`. Prohibido un `readonly` cuyo cuerpo es solo el constructor. No migrar el `Support` existente en silencio.

## 1.4.9 — 2026-10-01

- Laravel (`05`): prohibido `Support` y prohibida una clase cuyo único miembro es el constructor. Un valor o un arreglo va a un método privado del dueño; `private static` si no usa `$this`. Un helper nuevo solo si ese eje se reutiliza o ya existe. Al tocarla, se borra.

## 1.4.8 — 2026-10-01

- Campo de formulario (`10`): la tabla es ejemplo, no el universo. Cualquier campo se trata por lo que representa. Se aplica la normalización sin pérdida; lo que rechaza datos guardados o cambia el contrato se propone. El control sigue a la elección: dos opciones exclusivas son un radio, no cards; muchas opciones usan el autocomplete del repo, o se propone.

## 1.4.7 — 2026-10-01

- Entorno ≠ producto (`01`, `08`, `15`, `17`). `npm run dev` y el test runner no son un modo. Prohibido chip, banner o copy "Test mode" / "Testing mode", y prohibido ramificar validaciones por el runtime. Al tocar ese código, se borra; si el archivo existe solo para anunciarlo, se borra el archivo. Excepción solo si el contrato ya trae el flag y el requisito pide mostrarlo.

## 1.4.6 — 2026-10-01

- Campo de formulario (`10`): el tipo y la validación siguen lo que el campo representa. Se aplica `type`, `inputmode`, `autocomplete` y la normalización sin pérdida. Nombre sin dígitos, rangos y topes que puedan rechazar datos guardados se proponen. La misma regla va en el schema del form y en el borde.
- Campo complejo (`10`, `19`): moneda, decimal por locale, fecha con rangos o zona, hora con intervalos. Se usa el componente del repo. Si no existe, se propone una librería del framework. No se escribe la máscara a mano ni se instala sin OK.

## 1.4.5 — 2026-10-01

- Tests (`17`): siguen al requisito, no al borrado. Si el requisito desaparece, se borran el código y sus tests exclusivos, sin un test de "ya no existe". Si sigue, se conservan o adaptan. Si la eliminación crea una garantía vigente, se prueba esa garantía. La limpieza incluye fixtures, mocks y factories sin uso.

## 1.4.4 — 2026-09-30

- Orden dentro de un composable, hook o componente (`04`): dependencias, estado, derivados, funciones, efectos, ciclo de vida, return. Dependencias y estado van separados.
- El formato visual TypeScript pasa a llamarse `gian-ts-style`. La línea en blanco entre secciones vive ahí.

## 1.4.3 — 2026-09-30

- Auditoría: el reporte vive en `docs/pattern-audit/` de la raíz git del repo auditado. Si esa carpeta no está en el `.gitignore` de esa raíz, se agrega. No se ignora `docs/` entero.

## 1.4.2 — 2026-09-30

- Vue (`25`): si hay computed, handler, `watch` o llamada al service, vive en `composables/useThing.ts`. El script inline solo declara macros, imports y la llamada. El `.vue` no acumula esa lógica.

## 1.4.1 — 2026-09-30

- Vue (`25`): `<script setup lang="ts">` inline en el `.vue`. Sin `src`. Las macros no se mueven a un `.ts`. La lógica extraída va a `composables/useThing.ts`. La extracción pasa a ser obligatoria en 1.4.2.
- Supersede el SFC partido `<script setup lang="ts" src="./Nombre.ts">` de 1.3.0.

## 1.4.0 — 2026-09-30

- Hard rules del núcleo partidas: styling, validación user-facing y contrato de lectura son adaptadores. El schema nombrado es el núcleo; Zod lo es solo en TypeScript.
- `01`: filas de Python sin capítulo (body de Pydantic ≠ path, 422 por campo, `StrEnum`, `in`, datetimes aware, PEP 8 snake_case).
- Equivalentes Angular y Vue: MatDialog, `v-if`, Pinia, HttpClient, tabla de i18n, `defineModel`, `computed` A–E.
- `05` y `06` quedan declarados como adaptadores de Laravel.

## 1.3.2 — 2026-09-30

- `25`: ejemplos genéricos (`EntityPage`, `entityId`, `confirm` / `cancel`). Tailwind solo si el repo lo usa.
- `20`: adaptador (otra tecnología, misma capacidad) distinto de legacy (rompe el núcleo). Alineado con `24` §3.
- `01`: filas de backend sin capítulo nuevo. El DTO sale de un schema nombrado; Zod es ese schema en TypeScript. El nombre de archivo que impone el framework es `LIBRARY_OWNED`.
- `19`: cliente HTTP por capacidad. En Angular, `HttpClient` + interceptor; no pedir axios.
- `13` y la hard rule de mutaciones: el envelope `*Variables` queda en el adaptador de React Query o Vue Query. El DTO sale de un schema nombrado.

## 1.3.1 — 2026-09-30

- El lenguaje no apaga el estándar (`01`). Núcleo (nombres, helpers de área, enums, contratos, errores, display) vale en cualquier stack. Un capítulo de stack solo documenta el adaptador. Lo que el framework impone es `LIBRARY_OWNED`.
- “No aplica” no cierra la responsabilidad: se cumple con el equivalente del stack, en todo modo, no solo en la auditoría de repo (`24` §3).
- Fase 0 y `19` inventarían capacidades. En un repo que no es React, no se propone instalar TanStack Query, RHF ni MUI.
- `20`: solo se sigue una variante de la lista. Un patrón local no reconocido es legacy, no molde.
- `01` #4 y `04` quedan alineados con `08`: metadata del enum en el entity helper; ad-hoc inline.
- `25` es delta. Se quita `formatMoney` como ejemplo. Un archivo por función no es un helper de área.

## 1.3.0 — 2026-09-30

- Vue (`25`): SFC con lógica en `<script setup lang="ts" src="./Nombre.ts">`; `interface Props` / `interface Emits` locales; `composables/` en lugar de `hooks/`. Prohibido `defineComponent` y el genérico anónimo de `defineProps`. Reemplazado en 1.4.1: el script setup va inline, sin `src`.
- El stack React de `04`/`13` no se hereda. Naming sigue en esta skill; el formato del `.ts` hermano sigue en `gian-react-ts-style`.

## 1.2.14 — 2026-09-17

- Mutaciones (`13`): HARD ruta ≠ body. Service `(id, data)` o `(params, data)`; `TVariables` DTO / `{ id, data }` / `{ params, data }` / `EntityId`.
- DTOs (`10`): schema Zod nombrado = body HTTP; prohibido anónimo e IDs de ruta en el schema.
- UI (`09`) no serializa multipart; `FormDataHelper` shared (`23`) solo si el endpoint es multipart (Laravel `null` → `""`).
- Templates de service/mutation/schema + helper/tests. Evals `impl-mutation-route-vs-dto`, `impl-mutation-bind-id-at-hook`, `impl-named-dto-not-anonymous`, `audit-hybrid-mutation-vars`.

## 1.2.13 — 2026-09-15

- Metadata nullable (`07`/`08`/`15`): `getXMeta(Enum | null | undefined)` es el resolver canónico para componentes; `unknownMeta` y `getMeta` son privados.
- Supersede el consumo directo `Helper.statusMeta[status]` de 1.2.12 cuando el valor puede llegar ausente: ahí manda `getXMeta`.
- El `Record<Enum, Meta>` público se conserva para valores garantizados e iteración; los resolvers no aceptan `string`, casts ni fallbacks para ocultar drift.
- `unknownMeta.label` usa getter cuando el copy es dinámico para no congelar el locale.

## 1.2.12 — 2026-09-15

- Metadata de enums (`07`/`08`): un único mapa público `static readonly Record<Enum, Meta>` en el entity helper; no métodos que reconstruyen el Record.
- i18n (`15`): getters de `label` ejecutan `i18n.t()` al leer para que el cambio de locale no deje traducciones congeladas.
- Consumo normal directo `Helper.statusMeta[status]` o spread al componente, sin método, `?.`, `??` ni fallback para enums cerrados.
- Nullable, contratos externos y legacy se validan, normalizan o ramifican por separado sin debilitar el Record canónico.
- Checklists `03`/`23` y evals de implementación/auditoría alineados con exhaustividad, locale dinámico, consumo directo y fronteras desconocidas.

## 1.2.11 — 2026-09-10

- Resources (`06`): `new XResource($this->whenLoaded('rel'))` y `::collection($this->whenLoaded('rels'))`. Prohibido callback `whenLoaded(..., fn() => new X($this->rel))` salvo lógica extra.
- `05` apunta a `06`. Evals: `impl-whenloaded-resource-ctor`, `audit-whenloaded-callback`.

## 1.2.10 — 2026-09-09

- Membresía HARD (`07`): 2+ `===`/`!==` del mismo identificador contra un conjunto cerrado → `.includes()` (TS) / `in_array(..., true)` (PHP). Una sola comparación sigue `===`.
- `05` SM apunta a `07`. Evals: `impl-status-membership-includes`, `impl-php-status-in-array`, `audit-status-or-chain`.

## 1.2.9 — 2026-09-08

- Diálogos (`09`): montaje canónico `{isOpen && user && (`; props `isOpen` + entidad por tipo (`user={user}`). Prohibido `open`, `entity=`, `data=`.
- Varios overlays: un boolean por diálogo; el JSX sigue el mismo molde. `03` checklist alineado.
- Evals: `impl-dialog-mount-typed-props`, `audit-dialog-entity-open`.

## 1.2.8 — 2026-09-08

- Display / i18n HARD (`08`/`15`/`07`/`10`): Record de enum en `<entity>.helper.ts` con `i18n.t()` al leer; if-chain ad-hoc en el componente con `t()`.
- Prohibido `*.display.config.ts`, inyectar `TFunction` (`getXConfig(t)`, `createXSchema(t)`), `labelKey` diferido, mappings de color/icon/key en paralelo.
- Audits locales del repo no ganan al molde. `03`/`23`: el entity helper puede exponer el Record; no hay archivo display extra.
- Evals: `impl-reject-display-config-t-inject`, `impl-enum-meta-in-helper`, `audit-display-config-tfunction`, `audit-labelkey-indirection`.

## 1.2.7 — 2026-08-25

- HARD naming de hooks custom (`04`): archivo, directorio 1:1, export e import camelCase `useDashboard`; nunca `use-dashboard` / `use_dashboard`. Implementar: rename en alcance. Auditar: Hallazgo.
- No aplica a barrels `<entity>.queries.ts` / `<entity>.mutations.ts`.
- Evals: `impl-hook-file-camelcase`, `impl-hook-kebab-rename`, `impl-keep-query-barrel`, `audit-hook-kebab-file`.

## 1.2.6 — 2026-08-14

- HARD User-Facing Validation Contracts (`05` autoridad; `10`/`14` consumen 422): no terminar un FormRequest solo con `rules()`.
- Cobertura semántica regla→mensaje (no `count(rules) === count(messages)`). `attributes()` solo si `:attribute` o el copy lo necesita.
- UI: mapear 422 por campo según el patrón del repo; preservar el mensaje human-facing del backend; no sustituir por genérico ni crear ErrorMapper nuevo.
- Evals: `impl-formrequest-user-facing`, `impl-422-show-backend-messages`, `audit-formrequest-rules-only`.

## 1.2.5 — 2026-08-14

- `04`: Tailwind-first no autoriza `bg-[#…]` / `text-[#…]` si el token vive en `theme.palette`; no inventar nombres de `slotProps`.
- Evals negativos: conservar `sx` theme-aware, `useTheme()` en lógica JS, y `slotProps.className` frente a `'& .Mui…'` de layout.
- `04`/`23`: `cn()` depende de la composición real de clases; estado/props runtime con clases variables usa `cn()`, mientras un `className` idéntico permanece estático aunque MUI cambie `variant`/`color`.
- `04`: gate de tokens verificados; si el bridge MUI→Tailwind ya expone una equivalencia real, Tailwind-first también aplica a colores/tokens. `sx(theme)` queda como hatch cuando no existe equivalencia limpia o la API MUI lo requiere.
- `18`: auditorías focalizadas distinguen FAIL/GAP de “Fuera de alcance” y no convierten deuda lateral en PROP automáticamente.
- Evals positivos/negativos contra sobre-aplicación y sub-aplicación de `cn()`, bridges Tailwind, `sx(theme)`, `useTheme()` y scope de auditoría.

## 1.2.4 — 2026-08-14

- Styling FE (`04` HARD `no-local-style-constants`): Tailwind-first; `className` estático sin `cn()`; `cn()` solo composición; `sx` escape hatch; `sx={(theme) => theme.palette.*}` en vez de `useTheme()` ceremonial; `slotProps.className` antes de `'& .Mui…'`.
- `23`: mecánica de `cn()` alineada; concatenación, `*_SX` locales, `sx` de layout y `useTheme()` huérfano = Media. Clase estática sin `cn()` permitida.
- No vive en `gian-react-ts-style`.

## 1.2.3 — 2026-08-13

- Formato visual TS/TSX sale de esta skill: `gian-react-ts-style` (WRITE/FIX corrigen hunk; AUDIT no edita).
- `23` ya no gobierna arrows/expresión corta; conserva `cn()`, dayjs, utils vs helpers y memoización **A–E** (ceremonial A prohibido; multi-rama C STYLE_GIAN; MRT E).
- `08`/`04`/`01`/`00`: nested ternary y comments apuntan a la style skill.

## 1.2.2 — 2026-08-13

- Ownership de contratos TS (`07`): `APP_OWNED` \| `LIBRARY_OWNED` \| `EXTERNAL_GENERATED` \| `UNION LEGÍTIMA` antes de enum/union/mapping. No duplica la regla de string enum; la acota.
- `LIBRARY_OWNED`: tipo oficial (`ChipProps['color']`, etc.); el shadow (`StatusTone`/`tone`) desaparece — no se reemplaza por enum shadow.
- `APP_OWNED` incluye modos/estados de UI nombrados; `null` de ausencia no es miembro del enum.
- Mappings: un `Record<Enum, Meta>`; `satisfies` en arrays runtime de la lib.
- Memoización React no ceremonial (`23`); `08` deja de exigir `useMemo` en todo display.

## 1.2.1 — 2026-08-13

- Queries SQL/Query Builder: alias de tabla `t1`/`t2` en el raíz; `st1`/`sst1` según profundidad de subquery. No `users u` / `orders o`.

## 1.2.0 — 2026-08-05

- Alcance **Auditar repositorio completo** (`24-full-repo-audit`): inventario, coverage ledger, categorías sin hallazgos con evidencia, gate de cobertura, disposición; prohibido muestreo como cierre.
- `18`/`21`/`SKILL` distinguen Auditar feature vs repo completo; Fase 0 ya no usa “≥2 features” como cierre de full-repo.
- PROP (`19`): costos/riesgos reales; no “garantiza CI” sin evidencia de lint + pipeline.

## 1.1.5 — 2026-08-05

- Auditoría: duplicación vs helper/util de área existente (p. ej. función local ≈ `DateHelper`) es Hallazgo Media; display duplicable (`08`) y “no extraer por una sola dup accidental” (`22`) quedan matizados.

## 1.1.4 — 2026-08-05

- Inventario FE en Fase 0 (`02`): dayjs módulo, apiFetcher, ErrorMapper/CustomError, QueryClient, query-keys; tooling Serena/ast-grep opcional.
- Contratos explícitos en `14` (HTTP/errores), `13` (QueryClient defaults), `23` (import dayjs del módulo del proyecto); canónicos en `19`; variantes profile/realtime en `20`.

## 1.1.3 — 2026-08-05

- Query/Mutation: `*QueryProps` y `Use*MutationOptions` con genéricos; hook de mutation solo `mutationFn` + `...options` (toast/invalidate en el caller).
- Input/DTO de form y mutación vía Zod `z.infer`; sin `interface Input` paralela.

## 1.1.2 — 2026-08-05

- Reference `23-ts-style-helpers`: arrows, expresión corta, `cn()`, renombres, dayjs como regla FE, utils pequeños vs helpers clase de área.
- Ajuste de `08`/`22`/`19`/`04` y severidades de auditoría alineadas.

## 1.1.1 — 2026-08-05

- Auditoría: un solo archivo `pattern-audit/YYYY-MM-DD-<alcance>-auditoria.md` (hallazgos, propuestas, lotes; checklist/registro si aplicar). Sin carpetas multi-archivo por feature.

## 1.1 — 2026-08-05 (ready)

- Cierre minor fixes: invalidación alineada (`list._def` / `detail(id).queryKey` / `detail._def`).
- AbortSignal punta a punta en service + docs; `EntityId` tipado (default `number`).
- PHP: backed Enum por default; State Machine string-based con `public const` como fuente única.
- Evaluación de mejoras de stack (gap u oportunidad) consolidada.
- Referencia `22-design-quality` (traits, SOLID operacional, Clean Code).
- Description semántica; evals de aprobación (aplicar vs revisar PROP).
- Terminología neutral; regla ADAPTAR solo en templates.

## 1.0 — 2026-08-05

- Creación del estándar canónico.
- Incorporación del molde frontend y backend.
- Definición de contratos API, forms, dialogs y display.
- Modos Implementar, Auditar, Aplicar y Consultar.
- String enums canónicos y mappings exhaustivos.
- Evals iniciales de activación y calidad.
