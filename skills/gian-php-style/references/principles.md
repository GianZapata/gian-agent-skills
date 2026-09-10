# Principles

## Layers

1. **BASELINE / RECOMMENDED** — PHP moderno razonable cuando esta skill no especifica. No vender preferencias de Gian como "best practice universal".
2. **GIAN PREFERENCES** — estilo deliberado. Audit FAIL sólo si es objetivamente determinable; wrapping/legibilidad dudosa → GAP (no FAIL).
3. **GIAN DELIBERATE OVERRIDES** — contradicen PSR-12 / PER-CS: single-statement-if sin llaves **cuando el body es una línea física**; booleanos `&&`/`||` al **final** de línea; union/intersection `|`/`&` al final de línea; braces de clase/método/anonymous class same-line; empty class/method/ctor `{}` compacto; validation lists 2+ vertical.
4. **NEUTRAL / DO NOT AUDIT** — no añadir `declare(strict_types=1)`.

## Precedence

```text
explicit user instruction
  > HARD gian-php-style
  > project convention
  > recommended baseline
```

## Visual principle

```text
short + readable → inline
long/structured → multiline
multiline → geometrically aligned
```

Favor: poco ruido vertical, delimitadores alineados, diffs razonables, consistencia local. No verticalizar todo.

No usar 80/100/120 como umbral rígido salvo que el proyecto lo declare.

## Indent

HARD: 4 espacios. Nunca tabs para indentación.

## Trailing comma

`multiline-trailing-comma` (HARD, AUTOFIXABLE). En listas **multilínea** → trailing comma **obligatoria** (arrays, argument lists, parameter lists, `match`, array destructuring — alineado PER-CS 3.1).

```php
$data = [
    'name' => $name,
    'email' => $email,
];
```

Esta regla **no decide** trailing comma en expresiones **single-line**. No mezclar con `singleline-no-trailing-comma` (fuera de scope 1.2).

Audit FAIL si falta comma en una lista multilínea. FIX: añadir comma en multilínea es SAFE TEXTUAL.

## Enforcement metadata

Tags: `AUTOFIXABLE`, `AGENT-ENFORCED`, `DELIBERATE-OVERRIDE`. Registro completo: `references/overrides.md`. Pint overlay: `references/tooling.md`.

## FIX safety classes

- **SAFE TEXTUAL** — espacios, braces same-line, `elseif`, `} else {`, pad de `=>`, wrap de params, wrap de validation lists, trailing comma en listas multilínea sin cambiar strings.
- **AST-SENSITIVE** — `single-statement-if` FIX al **quitar** `{}`; unused imports; compound-type line breaks (no confundir `||` con `|`). Añadir `{}` a un body unbraced multilínea es SAFE TEXTUAL.
- **CONTENT-SENSITIVE** — heredoc/nowdoc; sintaxis alternativa PHP; comentarios intra-cuerpo; envelope Blade/HTML; contenido de regex/Rule.
- **NEVER AUTOFIX** — dangling-else; if/else chains; DNF wrap; grouped-import conversion; añadir `strict_types`; convertir `endif` o `@if` Blade; statements unspecified; cuerpo heredoc; inventar comentarios; regiones no-PHP de `.blade.php`; convertir `'required|string'` a array.

## PHP inside `.blade.php`

PHP real está in scope. Includes: Livewire 4 SFC `new class extends Component { ... }`; `<?php ... ?>`; `@php ... @endphp`.

Do NOT reformat: HTML; Blade markup; `wire:*`; Alpine; JavaScript; CSS; Blade directives/echo (`@if`, `{{ }}`) as if they were raw PHP.

Preserve template envelope and indent. Apply the rest of gian-php-style only to the PHP region.

## Heredoc / nowdoc (HARD SAFETY)

`heredoc-nowdoc-preserve`. El cuerpo, terminador y quoting se preservan EXACTAMENTE. Formatear PHP exterior si corresponde. Si una transformación podría tocar el contenido: DO NOT APPLY.

## `declare(strict_types=1)` (`strict-types-preserve`)

NEVER AUTOFIX add. Si ya existe, preservarlo y formatear solo layout/spacing alrededor.

## Alternative syntax (`alternative-syntax-preserve`)

PHP `if:` / `endif;` / `while:` / `endwhile;` / `for:` / `endfor;` / `foreach:` / `endforeach;` / `switch:` / `endswitch;` — preservar. NO convertir a braces.

Blade `@if` / `@endif` no es esta regla y no está in scope de formato.

## Comments and PHPDoc

Código autoexplicativo: nombres, no comentarios. WRITE no emite `//`, `/* */`, ni `/** */`. Si el usuario pide un comentario en el hilo, gana esa instrucción.

| Sitio | WRITE | FIX (hunk/archivo pedido) | AUDIT |
|---|---|---|---|
| PHPDoc `/** */` de archivo, clase, trait, enum, método, propiedad, parámetro | no emitir | borrar | FAIL `comments-phpdoc` |
| `//` y `/* */` **fuera** del cuerpo de función/método/closure (incl. entre métodos) | no emitir | borrar | FAIL |
| Comentario **dentro** del cuerpo, ruido (`check flag`, `return result`, narra el código) | no emitir | borrar | FAIL solo si es obvio |
| Comentario **dentro** del cuerpo que explica un porqué no obvio | no añadir uno nuevo | **conservar** | no FAIL |
| Relevancia intra-cuerpo dudosa | — | conservar | GAP, no FAIL |

`@var` / PHPDoc dentro de un cuerpo cuenta como PHPDoc → borrar.

No son comentarios: atributos `#[...]`, `declare(strict_types=1)`, `use`. Los `// BEFORE` / `// AFTER` de evals de esta skill son marcadores de fixture, no estilo de producción.
