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

- Sin siglas internas en visible
- Tono natural; mayúscula natural
- Título ↔ botón consistentes
- Toast: qué pasó y a dónde
- Key puede ser técnica; value humano
- `data-testid` en inglés técnico OK

Mensajes de validación user-facing (FormRequest `messages`/`attributes`, 422 por campo): autoridad `05`/`10`/`14`. Esta reference no define esa regla.

## Validación sugerida

Si el repo lo documenta: lint con `defaultLocale` es y en.
