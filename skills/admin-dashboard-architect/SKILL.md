---
name: admin-dashboard-architect
description: "Diseña y construye paneles administrativos, dashboards, tablas de datos, formularios y dialogs de alta densidad. Cargar al crear una superficie de administración nueva sin mundo visual previo. En un repo con tokens o librería de componentes solo aportan las reglas de estructura y de copy."
license: Apache-2.0
metadata:
  author: gian
  version: "1.0.0"
---

# Admin Dashboard & Backoffice UI

Al generar paneles administrativos, tablas, formularios o modales, aplica estas reglas.

## 0. Cuándo aplica

- **Sin identidad previa** (prototipo HTML de un solo archivo, o proyecto sin tokens ni librería de componentes): aplican todas las secciones, con los tokens concretos de abajo.
- **Con identidad previa** (el repo tiene tokens, shadcn, MUI o un tema): mandan los componentes y tokens del repo. No se introducen zinc, indigo, overlays a mano ni Tailwind por CDN. Del skill solo quedan las reglas de estructura (2, 3, 4) y de copy (6), expresadas con lo que el repo ya tiene.
- No es segunda dirección visual junto a otra skill de diseño. Acento propio: `indigo`. No se mezcla con el de `modern-ui-architect` en la misma superficie.

## 1. Layout del panel

- Sidebar fija (`w-60 border-r border-zinc-800/80 bg-zinc-950`), área principal `flex-1 bg-zinc-950` y cabecera `h-14 border-b border-zinc-800/80 px-6 flex items-center justify-between`.
- Contenido en `p-6 max-w-7xl mx-auto space-y-6`. Nada pegado a los bordes.
- El sidebar se oculta o colapsa en móvil (`hidden md:flex`).

## 2. Tablas

- Contenedor con borde fino, `rounded-xl overflow-hidden`.
- Encabezado `text-xs font-medium uppercase tracking-wider text-zinc-400`, padding `px-4 py-3`. Texto a la izquierda; cifras y acciones a la derecha.
- Filas con `divide-y`, hover sutil y celdas `px-4 py-3.5 text-sm`.
- Cifras y fechas con `tabular-nums`.
- Badges de estado: pills compactos con tinte translúcido y borde (`bg-emerald-500/10 text-emerald-400 border-emerald-500/20`; warning `amber`; error `rose`; neutro `zinc`). Nunca colores sólidos chillones.

## 3. Dialogs y drawers

- Prohibido `alert()`, `confirm()` y `prompt()` del navegador.
- Overlay `fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4`; caja `w-full max-w-md rounded-xl border`.
- Anatomía: header (título `text-base font-semibold` y subtítulo corto `text-xs`), body `p-6 space-y-4`, footer con borde superior y acciones a la derecha (cancelar en ghost, primaria sólida).

## 4. Formularios, inputs y microcopy de dialogs

- **Labels** siempre arriba del input. Nunca solo `placeholder` como etiqueta.
- **Grid:** desde 4 campos, `grid grid-cols-1 sm:grid-cols-2 gap-4`, solo para pares cortos y relacionados (plan y límite de usuarios). Un campo largo ocupa la fila completa.
- **Radio cards:** solo en un formulario nuevo, con 2 a 4 opciones, y solo si cada opción trae datos que hay que comparar (precio, límite). Dos opciones sin esos datos siguen siendo un radio. Un widget que ya existe no se convierte. Patrón: `border rounded-lg p-3 flex items-center justify-between cursor-pointer`.
- **Addons:** el prefijo o sufijo fijo (`https://`, dominio) vive en el control, como un `<span>` unido al `<input>` con borde compartido. No se escribe un párrafo que explique el formato. Con tokens del repo (`bg-muted`, `border-input`, `text-muted-foreground`); sin repo, los zinc de este skill.
- **Sin ayudas redundantes:** si el label ya es claro, no hay texto de ayuda. El `placeholder` lleva un ejemplo con `Ej. …` (`Ej. Grupo Solano S.A.`). Un formato que decide si el dato es válido (RFC, CLABE) no se esconde en el placeholder, porque desaparece al escribir: va en el addon o en una ayuda corta.
- **Inputs:** `w-full bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500`.
- **Tono:** ejecutivo B2B, directo y formal-moderno. Sin coloquialismos ni vaguedades («cupo de personas», «deja lista la cuenta»). Verbos precisos: «Registra una empresa y asigna su plan inicial». El sustantivo es el que ya usa el producto.

## 5. Tokens y anti-patrones

- Acento: `bg-indigo-500 hover:bg-indigo-400 text-white font-medium text-sm px-3.5 py-2 rounded-lg`.
- Iconos: SVG inline estilo Lucide (`16x16`, `stroke-width 1.75`). Cero emojis.
- Prohibido: `border="1"` en tablas, fondos blancos en inputs dentro de dark mode, sombras difusas en tarjetas, botones con textos largos.

## 6. Copy de producto

Nunca expongas nombres de arquitectura, infraestructura o patrones de código en textos visibles (títulos, menús, subtítulos, empty states, placeholders, etiquetas de grupo de la navegación).

- No se publican: `central`, `tenant`, `multitenant`, base de datos, CRUD, módulo, webhook, nombres de rol o de enum (`super_admin`).
- Las palabras del prompt no son copy. «Haz el dashboard de la db central» no produce el título «Panel central».
- No hay tabla fija de traducción. Usa el término que el producto ya tiene para esa entidad (navegación, breadcrumbs, locale). Si no existe, el sustantivo del dominio de quien lee, y se dice cuál se eligió. La misma entidad lleva la misma palabra en todas las pantallas.
- Sin meta-explicaciones: un subtítulo no describe el interior del sistema. Usa microcopy orientado a la tarea («Administra las empresas activas y sus planes»).
- Títulos cortos y directos (`Empresas`, `Facturación`, `Equipo`). Sin rellenos como «Panel de gestión de…» o «Módulo de…».
