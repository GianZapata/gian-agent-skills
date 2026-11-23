<?php

const IGNORED = [T_WHITESPACE, T_COMMENT, T_DOC_COMMENT];

const MASKED = [T_CONSTANT_ENCAPSED_STRING, T_ENCAPSED_AND_WHITESPACE, T_COMMENT, T_DOC_COMMENT, T_INLINE_HTML];

const OPENERS = ['(', '[', '{', T_CURLY_OPEN, T_DOLLAR_OPEN_CURLY_BRACES, T_ATTRIBUTE];

const CLOSERS = [')', ']', '}'];

const CONTROL = [T_IF, T_ELSEIF, T_WHILE, T_FOR, T_FOREACH, T_SWITCH, T_CATCH];

const CONTINUATIONS = [T_ELSE, T_ELSEIF, T_CATCH, T_FINALLY];

const PROMOTION = [T_PUBLIC, T_PROTECTED, T_PRIVATE, T_READONLY];

const DECLARATIONS = [
    T_ABSTRACT,
    T_FINAL,
    T_READONLY,
    T_PUBLIC,
    T_PROTECTED,
    T_PRIVATE,
    T_STATIC,
    T_VAR,
    T_CONST,
    T_FUNCTION,
    T_CLASS,
    T_INTERFACE,
    T_TRAIT,
    T_ENUM,
    T_CASE,
    T_ATTRIBUTE,
];

const LIST_OWNERS = [
    T_STRING,
    T_NAME_QUALIFIED,
    T_NAME_FULLY_QUALIFIED,
    T_NAME_RELATIVE,
    T_VARIABLE,
    T_FUNCTION,
    T_FN,
    T_ARRAY,
    T_ISSET,
    T_UNSET,
    T_LIST,
    T_USE,
    T_STATIC,
    T_CLASS,
    ')',
    ']',
];

const RULES = [
    'indent-tabs'                    => 'indent con tabs; usar 4 espacios',
    'negation-space'                 => '`! $x`; escribir `!$x`',
    'else-if'                        => '`else if`; escribir `elseif`',
    'control-paren-spacing'          => '`keyword (` con un espacio y sin espacios internos en `()`',
    'concat-spacing'                 => 'concat sin espacios alrededor de `.`',
    'arrow-fn-space'                 => '`fn (`; escribir `fn(`',
    'continuation-same-line'         => '`}` y `else`/`elseif`/`catch`/`finally` van en la misma línea',
    'comments-phpdoc'                => 'PHPDoc sobre una declaración; no emitir PHPDoc',
    'single-statement-if'            => '`if` sin `{}` con body multilínea; agregar `{}`',
    'promoted-constructor-multiline' => 'constructor con promotion en una línea; un parámetro por línea',
    'multiline-trailing-comma'       => 'lista multilínea sin coma final',
    'boolean-operator-eol'           => '`&&`/`||` inicia la línea; debe terminar la anterior',
    'null-coalesce-break'            => '`??` inicia la línea; debe terminar la anterior',
    'attribute-empty-args'           => '`#[Foo()]`; escribir `#[Foo]`',
];

function git(array $gitArgs): ?string
{
    exec('git ' . implode(' ', array_map('escapeshellarg', $gitArgs)) . ' 2>/dev/null', $output, $code);

    if ($code !== 0) return null;

    return implode("\n", $output);
}

function isSource(string $file): bool
{
    return str_ends_with($file, '.php') &&
        !str_ends_with($file, '.blade.php') &&
        !preg_match('#(^|/)vendor/#', $file);
}

function lines(?string $output): array
{
    return array_values(array_filter(explode("\n", $output ?? ''), fn($line) => $line !== ''));
}

function changedRanges(string $file, bool $all, array $untracked): ?array
{
    if ($all || in_array(realpath($file), $untracked, true)) return null;

    $diff = git(['diff', '-U0', 'HEAD', '--', $file]);

    if ($diff === null) return null;

    preg_match_all('/^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@/m', $diff, $matches, PREG_SET_ORDER);

    $ranges = [];

    foreach ($matches as $match) {
        $start = (int) $match[1];
        $count = ($match[2] ?? '') === '' ? 1 : (int) $match[2];
        $ranges[] = [$start, $start + max($count, 1) - 1];
    }

    return $ranges;
}

function tokenize(string $source): array
{
    $tokens = [];
    $line = 1;

    foreach (token_get_all($source) as $token) {
        [$id, $text] = is_array($token) ? [$token[0], $token[1]] : [$token, $token];

        $tokens[] = [
            'id'   => $id,
            'text' => $text,
            'line' => $line,
        ];

        $line += substr_count($text, "\n");
    }

    return $tokens;
}

function significant(array $tokens, int $index, int $step): ?int
{
    for ($i = $index + $step; isset($tokens[$i]); $i += $step) {
        if (!in_array($tokens[$i]['id'], IGNORED, true)) return $i;
    }

    return null;
}

function closing(array $tokens, int $open): ?int
{
    $depth = 0;

    for ($i = $open; isset($tokens[$i]); $i++) {
        $id = $tokens[$i]['id'];

        if (in_array($id, OPENERS, true)) {
            $depth++;
        } elseif (in_array($id, CLOSERS, true)) {
            $depth--;
        }

        if ($depth === 0) return $i;
    }

    return null;
}

function statementEnd(array $tokens, int $start): ?int
{
    $depth = 0;

    for ($i = $start; isset($tokens[$i]); $i++) {
        $id = $tokens[$i]['id'];

        if (in_array($id, OPENERS, true)) {
            $depth++;
        } elseif (in_array($id, CLOSERS, true)) {
            $depth--;
        }

        if ($depth < 0) return null;

        if ($depth === 0 && $id === ';') return $i;
    }

    return null;
}

function isBreak(array $token): bool
{
    return $token['id'] === T_WHITESPACE && str_contains($token['text'], "\n");
}

function functionSpans(array $tokens): array
{
    $spans = [];

    foreach ($tokens as $index => $token) {
        if ($token['id'] !== T_FUNCTION) continue;

        $start = $index;

        while ($start > 0 && !in_array($tokens[$start - 1]['id'], [';', '{', '}'], true)) {
            $start--;
        }

        $open = $index;

        while (isset($tokens[$open]) && !in_array($tokens[$open]['id'], ['{', ';'], true)) {
            $open = $tokens[$open]['id'] === '(' ? closing($tokens, $open) + 1 : $open + 1;
        }

        $end = isset($tokens[$open]) && $tokens[$open]['id'] === '{' ? closing($tokens, $open) : $open;
        $first = significant($tokens, $start - 1, 1) ?? $index;

        $spans[] = [$tokens[$first]['line'], $tokens[$end ?? $index]['line'] ?? $token['line']];
    }

    return $spans;
}

function scope(?array $ranges, array $spans): ?array
{
    if ($ranges === null) return null;

    $scope = $ranges;

    foreach ($spans as [$start, $end]) {
        foreach ($ranges as [$from, $to]) {
            if ($from <= $end && $to >= $start) {
                $scope[] = [$start, $end];

                break;
            }
        }
    }

    return $scope;
}

function inScope(?array $scope, int $line): bool
{
    if ($scope === null) return true;

    foreach ($scope as [$from, $to]) {
        if ($line >= $from && $line <= $to) return true;
    }

    return false;
}

function tokenFindings(array $tokens): array
{
    $findings = [];
    $stack = [];

    foreach ($tokens as $i => $token) {
        $id = $token['id'];
        $line = $token['line'];
        $next = $tokens[$i + 1] ?? null;
        $previous = $tokens[$i - 1] ?? null;

        if ($id === '!' && $next !== null && $next['id'] === T_WHITESPACE) $findings[] = [$line, $line, 'negation-space'];

        if ($id === T_ELSE && $next !== null && $next['id'] === T_WHITESPACE && ($tokens[$i + 2]['id'] ?? null) === T_IF) {
            $findings[] = [$line, $line, 'else-if'];
        }

        if (in_array($id, CONTROL, true) && $next !== null) {
            $paren = $next['id'] === T_WHITESPACE ? $tokens[$i + 2] ?? null : $next;
            $inner = $tokens[$i + 3] ?? null;

            if ($next['id'] === '(' || ($paren['id'] ?? null) === '(' && $inner !== null && $inner['id'] === T_WHITESPACE && !isBreak($inner)) {
                $findings[] = [$line, $line, 'control-paren-spacing'];
            }
        }

        if ($id === '.' && ($previous['id'] ?? null) !== T_WHITESPACE || $id === '.' && ($next['id'] ?? null) !== T_WHITESPACE) {
            $findings[] = [$line, $line, 'concat-spacing'];
        }

        if ($id === T_FN && $next !== null && $next['id'] === T_WHITESPACE) $findings[] = [$line, $line, 'arrow-fn-space'];

        if (in_array($id, CONTINUATIONS, true) && $previous !== null && isBreak($previous) && ($tokens[$i - 2]['id'] ?? null) === '}') {
            $findings[] = [$line, $line, 'continuation-same-line'];
        }

        if ($id === T_DOC_COMMENT) {
            $declaration = significant($tokens, $i, 1);

            if ($declaration !== null && in_array($tokens[$declaration]['id'], DECLARATIONS, true)) {
                $findings[] = [$line, $tokens[$declaration]['line'], 'comments-phpdoc'];
            }
        }

        if (in_array($id, [T_IF, T_ELSEIF], true)) {
            $open = significant($tokens, $i, 1);
            $close = $open !== null ? closing($tokens, $open) : null;
            $body = $close !== null ? significant($tokens, $close, 1) : null;

            if ($body !== null && !in_array($tokens[$body]['id'], ['{', ':'], true)) {
                $end = statementEnd($tokens, $body);

                if ($end !== null && $tokens[$end]['line'] > $tokens[$body]['line']) $findings[] = [$line, $line, 'single-statement-if'];
            }
        }

        if ($id === T_STRING && $token['text'] === '__construct' && ($tokens[significant($tokens, $i, -1) ?? 0]['id'] ?? null) === T_FUNCTION) {
            $open = significant($tokens, $i, 1);
            $close = $open !== null ? closing($tokens, $open) : null;

            if ($close !== null && $tokens[$open]['line'] === $tokens[$close]['line']) {
                $promoted = array_filter(
                    array_slice($tokens, $open, $close - $open),
                    fn($param) => in_array($param['id'], PROMOTION, true),
                );

                if ($promoted !== []) $findings[] = [$line, $line, 'promoted-constructor-multiline'];
            }
        }

        if (in_array($id, OPENERS, true)) {
            $owner = significant($tokens, $i, -1);
            $multiline = $next !== null && isBreak($next);

            $eligible = match ($id) {
                '('     => $multiline && $owner !== null && in_array($tokens[$owner]['id'], LIST_OWNERS, true),
                '['     => $multiline,
                default => false,
            };

            $stack[] = [$i, $eligible];
        }

        if (in_array($id, CLOSERS, true) && $stack !== []) {
            [$open, $eligible] = array_pop($stack);
            $last = significant($tokens, $i, -1);

            if ($eligible && $last !== null && $last !== $open && $tokens[$last]['id'] !== ',' && $tokens[$last]['line'] < $line) {
                $findings[] = [$tokens[$last]['line'], $tokens[$last]['line'], 'multiline-trailing-comma'];
            }
        }
    }

    return $findings;
}

function lineFindings(array $tokens): array
{
    $masked = '';

    foreach ($tokens as $token) {
        $masked .= in_array($token['id'], MASKED, true) ? preg_replace('/[^\n]/', ' ', $token['text']) : $token['text'];
    }

    $findings = [];

    foreach (explode("\n", $masked) as $index => $text) {
        $line = $index + 1;

        $patterns = [
            'indent-tabs'          => '/^[ ]*\t/',
            'boolean-operator-eol' => '/^\s*(&&|\|\|)/',
            'null-coalesce-break'  => '/^\s*\?\?/',
            'attribute-empty-args' => '/#\[\s*[\w\\\\]+\(\s*\)/',
        ];

        foreach ($patterns as $rule => $pattern) {
            if (preg_match($pattern, $text)) $findings[] = [$line, $line, $rule];
        }
    }

    return $findings;
}

function check(string $file, ?array $ranges): array
{
    $tokens = tokenize(file_get_contents($file));
    $scope = scope($ranges, functionSpans($tokens));
    $results = [];

    foreach ([...tokenFindings($tokens), ...lineFindings($tokens)] as [$line, $anchor, $rule]) {
        if (inScope($scope, $anchor)) $results[] = sprintf('FAIL %s:%d %s — %s', $file, $line, $rule, RULES[$rule]);
    }

    return $results;
}

$args = array_slice($argv, 1);
$all = in_array('--all', $args, true);
$fileArgs = array_values(array_filter($args, fn($arg) => !str_starts_with($arg, '--')));
$untracked = array_map('realpath', lines(git(['ls-files', '--others', '--exclude-standard'])));

if ($fileArgs === []) {
    $changed = git(['diff', '--name-only', 'HEAD']);

    if ($changed === null) {
        echo "GAP self-check — no se pudo leer `git diff HEAD`; pasar los archivos explícitos.\n";

        exit(2);
    }

    $fileArgs = [...lines($changed), ...lines(git(['ls-files', '--others', '--exclude-standard']))];
}

$files = array_values(array_unique(array_filter($fileArgs, fn($file) => isSource($file) && is_file($file))));
$results = [];

foreach ($files as $file) {
    $results = [...$results, ...check($file, changedRanges($file, $all, $untracked))];
}

$results = array_values(array_unique($results));

natsort($results);

foreach ($results as $result) {
    echo $result . "\n";
}

printf("Self-check PHP: %d pendientes (%d archivos)\n", count($results), count($files));

exit($results === [] ? 0 : 1);
