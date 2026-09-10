# 15 — i18n y copy

Cargar cuando: textos UI, locales, tono, `t()` vs `i18n.t()`.

## i18n técnico (HARD)

```text
React component → t() from useTranslation
Anything else (helper, schema, util, config .ts) → i18n.t() from the repo i18n module
Do not inject TFunction
Do not wrap schemas as createXSchema(t)
```

- JSON **flat** dot-notation
- `useTranslation(['ns1', 'ns2'])` — namespace explícito; nunca `''`
- `t('ns:key', { var })` — 2º arg solo interpolación
- Helper / schema: `i18n.t('ns:key')` importado del módulo configurado (`@/lib/i18n` o el path del repo)
- Paridad es + en
- Prohibido `as any` / `as string` en i18n
- Prohibido `getXConfig(t: TFunction)` y `labelKey` + `t(key)` en render — `08`

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
