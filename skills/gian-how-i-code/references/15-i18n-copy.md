# 15 — i18n y copy

Cargar cuando: textos UI, locales, tono, `t()` vs `i18n.t()`.

## Alcance

- **Núcleo:** fuera de la vista, `i18n.t()` del módulo del repo; no inyectar `TFunction`; getters de `label`; paridad de locales; copy de este archivo.
- **Adaptador:** el helper de la vista según el bloque HARD de abajo. La vista no llama `i18n.t()` si el framework tiene helper de componente.

## i18n técnico (HARD)

```text
Vista React → t() de useTranslation
Vista Vue → t() de useI18n / $t
Vista Angular → $localize o TranslateService del repo
Fuera de la vista, en cualquier stack → i18n.t() del módulo del repo
Nunca inyectar el traductor
No envolver schemas como createXSchema(t)
```

Adaptador React (i18next):

- JSON **flat** dot-notation
- `useTranslation(['ns1', 'ns2'])` — namespace explícito; nunca `''`
- `t('ns:key', { var })` — 2º arg solo interpolación

Cualquier stack:

- Helper / schema: `i18n.t('ns:key')` importado del módulo configurado (`@/lib/i18n` o el path del repo)
- Metadata de enum en helper: propiedad pública `static readonly Record<Enum, Meta>` con getter `label` que ejecuta `i18n.t()` en cada lectura (`08`)
- Si existe `getXMeta(Enum | null | undefined)`, `unknownMeta.label` también usa getter para no congelar el locale; el resolver privado solo trata `null`/`undefined` como ausencia
- Paridad es + en
- Prohibido `as any` / `as string` en i18n
- Prohibido `getXConfig(t: TFunction)` y `labelKey` + `t(key)` en render — `08`
- Prohibido `label: i18n.t('…')` dentro de la inicialización estática: congela la traducción al cargar el módulo y no reacciona a un cambio de locale

```ts
static readonly statusMeta: Record<Status, StatusMeta> = {
  [Status.Active]: {
    get label() {
      return i18n.t('users:status.active');
    },
    tone: 'success',
  },
};
```

Los getters conservan un único Record sin congelar el locale. El componente usa `Helper.getStatusMeta(status).label` cuando el valor puede ser nullable; usa `Helper.statusMeta[status].label` para un enum garantizado o al iterar el catálogo. No vuelve a traducir ni usa `labelKey`.

## Copy (usuario final)

Todo texto visible se juzga por audiencia y función: título, descripción, vacío, error, toast, botón, placeholder y ayuda. La prueba no es una palabra prohibida.

Si quien lee no entiende la frase, o la frase le pide algo que no puede hacer, no se publica así. Un error dice qué pasó en su tarea y qué puede hacer esa persona. Un botón, un título o un placeholder cumplen su función. No se les impone la fórmula del error.

No se inventa la causa ni la recuperación. No se asume que el servidor está apagado, que los datos quedaron guardados, ni cuándo vuelve. “Más tarde” vale para un fallo temporal del servicio, no para cualquier error. Un dato inválido dice qué corregir. Una sesión vencida puede pedir iniciar sesión.

Si la pantalla ya tiene forma (tarjeta, lista, ficha, gráfica), la espera es un skeleton de esa forma, no un párrafo «Cargando…». El error y el vacío siguen en palabras. El nombre para el lector de pantalla, si hace falta, va en `sr-only`. El mecanismo (Tailwind o MUI) lo decide `04`.

Que el sistema compruebe, calcule o limite no se publica por eso. Prohibido anunciar el éxito o el estado normal: "Disponible", "Encontrado", "Solo presentación", "Guardar no convierte", y cualquier frase que explique qué no hace Guardar. Si hace falta señalar, es un icono (`10`). El icono no es obligatorio. El título de una sección no repite la etiqueta de su único campo. Al tocarlo, se quita ese adorno y no se sustituye por otro texto.

Un término del dominio de quien lee se conserva: `API key`, `PDF`, `URL`. “Revisa que la API esté en marcha” no: esa persona no opera el servidor. El verbo de la pantalla se conserva si es el de la operación. No se cambia “verificar” por “cargar” sin mirar qué hacía la pantalla.

```text
BAD:  No pudimos verificar la sucursal. Revisa que la API esté en marcha e inténtalo de nuevo.
GOOD: No pudimos verificar esta sucursal. Inténtalo más tarde.
```

Un `message` de `abort()`, excepción o JSON que el cliente puede mostrar es la misma copy. Un nombre interno de otra superficie no se publica: para quien lee no significa nada. Si hace falta la frase, nombra su tarea.

```text
BAD:  El laboratorio de chat ya no está disponible.
GOOD: El chat no está disponible.
```

Al detectar copy visible que habla al operador, contiene instrucciones que la audiencia no puede realizar, o atribuye causas y plazos sin evidencia, se corrige directo. Se revisa el contexto. Se conserva la operación real, el idioma del usuario y los términos del dominio, como `API key`. Los códigos y contratos quedan estables. Al terminar, se resume qué cambió.

Si el usuario pide explícitamente solo analizar, o no modificar archivos, se entrega la propuesta y no se edita.

- Sin siglas internas en visible
- Tono natural; mayúscula natural
- Título ↔ botón consistentes
- Toast: qué pasó y a dónde. «A dónde» es la pantalla o la tarea, no un valor fijo de prueba
- Key puede ser técnica; value humano
- `data-testid` en inglés técnico OK
- El entorno no cambia el copy. Prohibido "Test mode", "Testing mode" y equivalentes, y prohibido un mensaje distinto si `import.meta.env.DEV`, `NODE_ENV`, `APP_ENV` o el test runner
- Al tocar un archivo con ese copy, o con una validación cuyo texto depende del entorno: borrar el texto y la rama. No dejar un fallback. Si el archivo existe solo para ese aviso, borrarlo (`08`)

## Valor fijo de prueba

Cuando pidan un valor fijo para que la integración salga por ahí (teléfono, correo, id, URL) y ese valor no es el del registro, el valor va en el request, el dial o la config. La pantalla sigue mostrando el registro real.

No se publica el desvío ni el guion de la prueba. Prohibido el aviso, toast, helper o nota.

```text
BAD:  Llamada ordenada a +52…. Contesta y di bueno enseguida.
BAD:  Este registro se redirige a +52….
GOOD: El dial usa ese número. La ficha sigue mostrando el teléfono del registro.
```

Al tocar un archivo que lo tenga: quitar el texto y el estado que solo existe para mostrarlo. El cableado se queda. Excepción: en este hilo pidieron mostrar ese destino.

## Referencia, plan o mockup

Un HTML exportado, una captura, un Figma, una spec o un plan aportan composición, orden, tokens y datos de ejemplo. Su texto de andamiaje sirve a quien diseña, no a quien usa la pantalla, y no se publica:

- Nombre o estatus de la referencia: "oficial", "v2", "final", "exportado"
- Fase o alcance: "Próxima fase", "Próximamente", "Fase 2", "Fuera de este corte"
- Origen del dato: "Mock", "Muestra", "Periodo de muestra", "Datos de ejemplo", "Demo"
- Personas, dueños o fechas de entrega
- Notas de diseño para quien implementa

El título nombra la tarea de quien usa la pantalla.

Sección sin contrato de datos: se monta igual que las demás. Los valores viven en una sola constante de la feature, con `// TODO(datos): <endpoint, campo o contrato que falta>`. Ese prefijo fijo permite listarlos con `rg "TODO\(datos\)"`. El TODO no nombra personas. La pantalla no anuncia el hardcode: sin badge, leyenda, tooltip ni nota.

Lo que está fuera de alcance (export, PDF, una acción de otra fase) no se monta. Ni botón deshabilitado, ni "Próximamente", ni placeholder.

```text
BAD:  Dashboard oficial
GOOD: Inicio

BAD:  Facturas pendientes · Mock — aún no entregan el contrato
GOOD: Facturas pendientes
      (valores de PENDING_INVOICES_DATA con // TODO(datos): endpoint de facturas pendientes)

BAD:  [Reporte próxima fase] deshabilitado
GOOD: el control no existe

BAD:  Periodo de muestra: 1–31 oct
GOOD: el filtro muestra el periodo elegido
```

Un plan tampoco autoriza publicarlo. Al tocar un archivo que lo tenga, se quita el texto y el estado que solo existe para mostrarlo. Excepción: este hilo pide mostrarlo. Auditoría: hallazgo Alto, sin editar (`18`).

### Detectar y avisar

La falta de datos no bloquea y no se pregunta. Se detecta, se implementa igual y se avisa. El aviso va siempre, en el plan y en el cierre, aunque nadie lo haya pedido.

1. Detectar. Antes de escribir, recorrer la referencia y el plan sección por sección. Sin datos todavía: una cifra, lista o tarjeta que ningún endpoint, campo o tabla alimenta. Texto de andamiaje: lo de la lista de arriba.
2. Implementar. Sección sin datos: los datos de ejemplo de la referencia en una sola constante con `TODO(datos)`. Texto de andamiaje: título por la tarea, omitido, o no montado si es otra fase.
3. Revisar antes de cerrar. Strings visibles de los archivos tocados y de los JSON de locale:

```bash
rg -n -i "mock|muestra|ejemplo|demo|oficial|pr[oó]xima fase|pr[oó]ximamente|fase [0-9]|placeholder|sample|lorem" <archivos tocados>
rg -n "TODO\(datos\)" <archivos tocados>
```

Cada coincidencia visible se corrige, o se conserva si es término del dominio de quien lee. Un rótulo que ya estaba en un archivo tocado se quita y se lista.

4. Avisar. El plan lleva las dos listas, con lo que se hará. El cierre lleva el mismo bloque con `archivo:línea` sacado del `rg` (`21`). Si no hubo casos, no se agrega el bloque.

```text
Sin datos todavía
- Facturas pendientes: falta el endpoint de facturas pendientes. Constante en features/dashboard/constants/dashboard.constants.ts:14 (TODO(datos)).

Texto de la referencia que no publiqué
- "Dashboard oficial" → título "Inicio"
- Badge "Mock" y su leyenda → omitidos
- "Reporte próxima fase" → no montado (fuera de alcance)
```

Mensajes de validación user-facing (FormRequest `messages`/`attributes`, 422 por campo): autoridad `05`/`10`/`14`. Esta reference no define esa regla.

## Validación sugerida

Si el repo lo documenta: lint con `defaultLocale` es y en.
