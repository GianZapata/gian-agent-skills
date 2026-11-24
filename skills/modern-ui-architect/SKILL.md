---
name: modern-ui-architect
description: "Genera interfaces web modernas y minimalistas (estilo Linear/Vercel) para prototipos y pantallas nuevas sin identidad previa, bloqueando patrones genéricos o anticuados. En un repo con tokens o librería de componentes solo aplican las reglas de estructura."
license: Apache-2.0
metadata:
  author: gian
  version: "1.0.0"
---

# Modern UI/UX Architect

Al crear o modificar una interfaz web, componente o app frontend, aplica estas reglas antes y durante la generación de código.

## 0. Cuándo aplica

- **Sin identidad previa** (prototipo HTML de un solo archivo, o proyecto sin tokens ni librería de componentes): aplican todas las secciones.
- **Con identidad previa** (el repo tiene tokens, shadcn, MUI o un tema): mandan los componentes y tokens del repo. No se introducen emerald, zinc, Inter ni Tailwind por CDN. Del skill solo quedan el flujo spec-first (1) y los anti-patrones de estructura (4).
- No es segunda dirección visual junto a otra skill de diseño. Acento propio: `emerald`. No se mezcla con el de `admin-dashboard-architect` en la misma superficie. Para paneles administrativos, usa esa skill.

## 1. Spec-first

Antes de escribir código, un bloque de máximo 4 líneas:

- **Layout:** estructura y contenedor principal (`max-w-4xl` o `max-w-5xl`).
- **Jerarquía:** qué elemento pesa más y cuál es el flujo de lectura.
- **Interacción:** cómo se comportan hover, filtros y modales.

## 2. Base técnica (solo sin identidad previa)

- Tailwind CSS. En un HTML único, `<script src="https://cdn.tailwindcss.com"></script>`. Sin bloques `<style>` con CSS manual innecesario.
- Tipografía Inter (400, 500, 600) como `font-sans`.
- Iconos SVG inline estilo Lucide (`18x18`, `stroke-width 1.75`). Cero emojis como elementos de interfaz.

## 3. Tokens (solo sin identidad previa)

- Fondo `bg-zinc-950`, texto `text-zinc-100`. Superficies `bg-zinc-900/50 border border-zinc-800/80 rounded-xl`.
- Títulos `text-zinc-50 font-semibold tracking-tight`; subtítulos y labels `text-zinc-400 text-sm`; cifras y fechas con `tabular-nums font-medium`.
- Acento único `emerald-500` (`bg-emerald-500 hover:bg-emerald-400 text-zinc-950 font-medium`), solo para el CTA principal y las pestañas activas.
- Inputs: `bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm text-zinc-100 focus:outline-none focus:border-emerald-500`. Nunca con el estilo por defecto del navegador.

## 4. Anti-patrones

- Sin degradados de fondo.
- Sin sombras difusas pesadas (`shadow-lg`, `shadow-xl`, `shadow-2xl`): la profundidad sale del borde de 1px.
- Sin colores saturados múltiples ni badges arcoíris: neutros o tintes sutiles (`bg-emerald-500/10 text-emerald-400 border border-emerald-500/20`).
- Sin amontonar: mínimo `p-5` en tarjetas y `gap-4` o `gap-6` entre bloques.
- Sin `alert()`, `confirm()` ni `prompt()`: un modal estilizado.

## 5. Copy

El texto visible nombra la tarea de quien usa la pantalla. No publica `central`, `tenant`, base de datos, CRUD ni módulo, ni palabras copiadas del prompt. Usa el término que el producto ya tiene para cada entidad.
