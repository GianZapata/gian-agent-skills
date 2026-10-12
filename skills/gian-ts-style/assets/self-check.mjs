#!/usr/bin/env node
// gian-ts-style self-check. Run from the repo root of the project being edited:
//   node <skill>/assets/self-check.mjs              -> functions touched in `git diff HEAD` + untracked files
//   node <skill>/assets/self-check.mjs a.tsx b.ts   -> functions touched in those files (whole file if untracked)
//   node <skill>/assets/self-check.mjs --all a.tsx  -> every function in those files
// Exit 0: 0 pendientes. Exit 1: FAIL. Exit 2: could not run (report as GAP).

import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';

const args = process.argv.slice(2);
const all = args.includes('--all');
const fileArgs = args.filter((arg) => !arg.startsWith('--'));

const loadTypeScript = () => {
  const bases = [path.join(process.cwd(), 'package.json'), import.meta.url];

  for (const base of bases) {
    try {
      return createRequire(base)('typescript');
    } catch {}
  }

  return null;
};

const ts = loadTypeScript();

if (!ts) {
  console.log('GAP self-check — `typescript` no está instalado en este repo; no se pudo verificar.');
  process.exit(2);
}

const git = (gitArgs) => {
  try {
    return execFileSync('git', gitArgs, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
  } catch {
    return null;
  }
};

const isSource = (file) => /\.(ts|tsx|vue)$/.test(file) && !/\.d\.ts$/.test(file);

const untracked = new Set(
  (git(['ls-files', '--others', '--exclude-standard']) ?? '').split('\n').filter(Boolean).map((file) => path.resolve(file)),
);

const changedRanges = (file) => {
  if (all || untracked.has(path.resolve(file))) return null;

  const diff = git(['diff', '-U0', 'HEAD', '--', file]);

  if (diff === null) return null;

  const ranges = [];

  for (const match of diff.matchAll(/^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@/gm)) {
    const start = Number(match[1]);
    const count = match[2] === undefined ? 1 : Number(match[2]);

    ranges.push([start, Math.max(start, start + count - 1)]);
  }

  return ranges;
};

const filesToCheck = () => {
  if (fileArgs.length > 0) return fileArgs.filter(isSource);

  const tracked = (git(['diff', '--name-only', 'HEAD']) ?? '').split('\n').filter(Boolean);

  return [...new Set([...tracked, ...[...untracked].map((file) => path.relative(process.cwd(), file))])]
    .filter(isSource)
    .filter((file) => existsSync(file));
};

const findings = [];

const report = (level, file, line, rule, message) => {
  findings.push({ level, file, line, rule, message });
};

const DEPS = /^(useNavigate|useParams|useLocation|useSearch|useSearchParams|useMatch|useRouter|useRoute|useRouterState|useTranslation|useI18n|useQueryClient|useContext|useTheme|useMediaQuery|inject|storeToRefs|defineProps|defineEmits|defineModel|defineSlots|useSlots|useAttrs|use[A-Z]\w*Store|useStore)$/;
const STATE = /^(useState|useReducer|useRef|useForm|ref|shallowRef|reactive|shallowReactive|signal)$/;
const DERIVED_HOOK = /^(useMemo|computed)$/;
const FUNCTION_HOOK = /^(useCallback)$/;
const EFFECT = /^(useEffect|useLayoutEffect|useInsertionEffect|watch|watchEffect|watchPostEffect|onMounted|onBeforeMount|onUnmounted|onBeforeUnmount|onUpdated|onActivated|onDeactivated|effect)$/;
const QUERY = /^(useQuery|useSuspenseQuery|useInfiniteQuery|useQueries|use[A-Z]\w*Query)$/;
const WRITE_METHOD = /^(post|patch|put|delete|remove|save|create|update|store|destroy|mutate|mutateAsync|send|upload)/i;
const SECTION_COMMENT = /^\s*\/\/\s*(states?|effects?|handlers?|hooks?|queries|query|mutations?|derived|computed|refs?|functions?|callbacks?|variables?|estado|estados|efectos?|funciones|derivadas?|variables)\s*:?\s*$/i;

const UTILITY = /^(?:[a-z0-9-]+:)*-?(bg|text|border|ring|shadow|fill|stroke|from|to|via|p[xytrbl]?|m[xytrbl]?|gap|rounded|font|leading|tracking|w|h|size|min-w|min-h|max-w|max-h|flex|grid|inline-flex|items|justify|self|shrink|grow)(-|$)/;
const isClassList = (value) => {
  const tokens = value.trim().split(/\s+/).filter(Boolean);

  return tokens.length > 0 && tokens.every((token) => /^[!a-z0-9[:\-][\w:/[\]\-.#%(),!]*$/i.test(token)) && tokens.some((token) => UTILITY.test(token)) && !/^[A-ZÁÉÍÓÚÑ]/.test(value.trim());
};

const SLOT_NAMES = ['macros', 'dependencias', 'estado', 'hooks que leen estado', 'derivadas', 'funciones', 'efectos', 'return'];

const check = (file) => {
  const raw = readFileSync(file, 'utf8');
  let text = raw;
  let lineOffset = 0;
  const isVue = file.endsWith('.vue');

  if (isVue) {
    const match = raw.match(/<script\b[^>]*\bsetup\b[^>]*lang=["']ts["'][^>]*>([\s\S]*?)<\/script>|<script\b[^>]*lang=["']ts["'][^>]*\bsetup\b[^>]*>([\s\S]*?)<\/script>/);

    if (!match) return;

    const body = match[1] ?? match[2];

    lineOffset = raw.slice(0, raw.indexOf(body)).split('\n').length - 1;
    text = body;
  }

  const sf = ts.createSourceFile(file, text, ts.ScriptTarget.Latest, true, file.endsWith('.tsx') ? ts.ScriptKind.TSX : ts.ScriptKind.TS);
  const lines = text.split('\n');
  const startLine = (node) => sf.getLineAndCharacterOfPosition(node.getStart(sf)).line + 1;
  const endLine = (node) => sf.getLineAndCharacterOfPosition(node.getEnd()).line + 1;
  const at = (node) => startLine(node) + lineOffset;
  const isMultiline = (node) => startLine(node) !== endLine(node);
  const blankBetween = (a, b) => {
    for (let line = endLine(a) + 1; line < startLine(b); line += 1) {
      if (lines[line - 1].trim() === '') return true;
    }

    return false;
  };

  const ranges = changedRanges(file);
  const touched = (node) => {
    if (ranges === null) return true;

    const from = startLine(node) + lineOffset;
    const to = endLine(node) + lineOffset;

    return ranges.some(([start, end]) => start <= to && end >= from);
  };

  const calleeName = (expression) => {
    let node = expression;

    while (node && (ts.isAwaitExpression(node) || ts.isAsExpression(node) || ts.isNonNullExpression(node) || ts.isParenthesizedExpression(node) || ts.isSatisfiesExpression?.(node))) {
      node = node.expression;
    }

    if (!node || !ts.isCallExpression(node)) return null;

    const callee = node.expression;

    if (ts.isIdentifier(callee)) return callee.text;
    if (ts.isPropertyAccessExpression(callee)) return callee.name.text;

    return null;
  };

  const declaredNames = (statement) => {
    const names = new Set();
    const collect = (name) => {
      if (ts.isIdentifier(name)) names.add(name.text);
      else if (ts.isObjectBindingPattern(name) || ts.isArrayBindingPattern(name)) {
        for (const element of name.elements) {
          if (!ts.isOmittedExpression(element)) collect(element.name);
        }
      }
    };

    if (ts.isVariableStatement(statement)) {
      for (const declaration of statement.declarationList.declarations) collect(declaration.name);
    }

    if (ts.isFunctionDeclaration(statement) && statement.name) names.add(statement.name.text);

    return names;
  };

  const references = (node, names) => {
    if (names.size === 0) return false;

    let found = false;
    const visit = (child) => {
      if (found) return;
      if (ts.isIdentifier(child) && names.has(child.text)) {
        const parent = child.parent;
        const isDeclarationName = parent && (ts.isVariableDeclaration(parent) || ts.isBindingElement(parent)) && parent.name === child;

        if (!isDeclarationName) found = true;
      }

      ts.forEachChild(child, visit);
    };

    ts.forEachChild(node, visit);

    return found;
  };

  const initializer = (statement) => {
    if (!ts.isVariableStatement(statement)) return null;

    const declarations = statement.declarationList.declarations;

    return declarations.length === 1 ? declarations[0].initializer ?? null : null;
  };

  const isFunctionLike = (node) => node && (ts.isArrowFunction(node) || ts.isFunctionExpression(node));
  const hasBlockBody = (node) => isFunctionLike(node) && ts.isBlock(node.body);

  const isEarlyReturn = (statement) => ts.isIfStatement(statement) && !statement.elseStatement && (ts.isReturnStatement(statement.thenStatement) || ts.isThrowStatement(statement.thenStatement));

  const slotOf = (statement) => {
    if (ts.isReturnStatement(statement) || isEarlyReturn(statement)) return 7;
    if (ts.isFunctionDeclaration(statement)) return 5;

    if (ts.isExpressionStatement(statement)) {
      const name = calleeName(statement.expression);

      if (name && EFFECT.test(name)) return 6;
      if (name && DEPS.test(name)) return 1;
      if (name && /^use[A-Z]/.test(name)) return 3;

      return null;
    }

    const init = initializer(statement);

    if (!init) return null;
    if (isFunctionLike(init)) return 5;

    const name = calleeName(init);

    if (name && /^define(Props|Emits|Model|Slots)$/.test(name)) return 0;
    if (name && DEPS.test(name)) return 1;
    if (name && STATE.test(name)) return 2;
    if (name && DERIVED_HOOK.test(name)) return 4;
    if (name && FUNCTION_HOOK.test(name)) return 5;
    if (name && EFFECT.test(name)) return 6;
    if (name && /^use[A-Z]/.test(name)) return 3;

    return 4;
  };

  const isSectionBlock = (statement) => {
    if (ts.isFunctionDeclaration(statement)) return true;

    if (ts.isExpressionStatement(statement)) {
      const name = calleeName(statement.expression);

      return Boolean(name && EFFECT.test(name));
    }

    const init = initializer(statement);

    if (!init) return false;
    if (hasBlockBody(init)) return true;

    const name = calleeName(init);

    if (name && (DERIVED_HOOK.test(name) || FUNCTION_HOOK.test(name))) {
      const callback = ts.isCallExpression(init) ? init.arguments[0] : null;

      return Boolean(callback && hasBlockBody(callback));
    }

    return false;
  };

  const isQueryStatement = (statement) => {
    const init = initializer(statement);
    const name = init ? calleeName(init) : null;

    return Boolean(name && QUERY.test(name));
  };

  const isAwaitRead = (statement) => {
    const init = initializer(statement);

    if (!init) return false;

    let node = init;

    while (ts.isAsExpression(node) || ts.isNonNullExpression(node) || ts.isParenthesizedExpression(node)) node = node.expression;

    if (!ts.isAwaitExpression(node)) return false;

    const name = calleeName(node.expression);

    return Boolean(name && !WRITE_METHOD.test(name));
  };

  const isGuardOf = (previous, statement) => isEarlyReturn(statement) && !isMultiline(statement) && references(statement.expression, declaredNames(previous));

  // Body of a component, hook, composable or <script setup>: slots + section spacing.
  const checkSlotBody = (statements) => {
    const seenSlots = [];
    const culprits = new Set();
    let previousAccepted = null;

    statements.forEach((statement, index) => {
      const slot = slotOf(statement);

      if (slot !== null) {
        const higher = seenSlots.filter((entry) => entry.slot > slot && slot !== 7);
        const dependsOnHigher = references(statement, new Set(higher.flatMap((entry) => [...entry.names])));
        const continuesGroup = previousAccepted !== null && previousAccepted.slot === slot && previousAccepted.statement === statements[index - 1];
        let accepted = true;

        if (higher.length > 0 && !dependsOnHigher && !continuesGroup) {
          accepted = false;

          const fresh = higher.filter((entry) => !culprits.has(entry.statement));

          if (fresh.length > 0) {
            const culprit = fresh[0];

            report('FAIL', file, at(culprit.statement), 'slot-order', `${SLOT_NAMES[culprit.slot]} arriba de ${SLOT_NAMES[slot]} (línea ${at(statement)}): orden 04 — dependencias, estado, hooks, derivadas, funciones, efectos, return`);
            higher.forEach((entry) => culprits.add(entry.statement));
          }
        }

        if (slot === 3 && seenSlots.some((entry) => entry.slot === 7)) {
          report('FAIL', file, at(statement), 'slot-order', 'hook debajo de un return temprano (rules of hooks, 04)');
        }

        seenSlots.push({ slot, statement, names: declaredNames(statement) });
        previousAccepted = accepted ? { slot, statement } : null;
      }

      const previous = statements[index - 1];

      if (!previous || blankBetween(previous, statement)) return;

      const previousSlot = slotOf(previous);
      const sameEarlyReturns = previousSlot === 7 && slot === 7 && isEarlyReturn(previous) && isEarlyReturn(statement);

      if (sameEarlyReturns) return;

      if (previousSlot !== null && slot !== null && previousSlot !== slot) {
        report('FAIL', file, at(statement), 'vertical-spacing', `${SLOT_NAMES[slot]} pegado a ${SLOT_NAMES[previousSlot]}: falta línea en blanco entre secciones`);
      } else if (isSectionBlock(previous) || isSectionBlock(statement)) {
        report('FAIL', file, at(statement), 'vertical-spacing', 'función, efecto o useMemo/computed con cuerpo sin línea en blanco antes o después');
      } else if (isMultiline(previous)) {
        report('FAIL', file, at(statement), 'vertical-spacing', `la sentencia multilínea de la línea ${at(previous)} cierra con línea en blanco`);
      } else if (isQueryStatement(previous) && slot === 3 && !references(statement, declaredNames(previous))) {
        report('FAIL', file, at(statement), 'read-group', 'una query cierra su grupo: línea en blanco antes del siguiente hook');
      }
    });
  };

  // Any other block (plain function, handler, callback, effect body).
  const checkPlainBlock = (statements) => {
    statements.forEach((statement, index) => {
      const previous = statements[index - 1];

      if (!previous) return;

      const glued = !blankBetween(previous, statement);

      if (glued && isMultiline(previous) && !isGuardOf(previous, statement)) {
        report('FAIL', file, at(statement), 'vertical-spacing', `la sentencia multilínea de la línea ${at(previous)} cierra con línea en blanco`);
      } else if (glued && isAwaitRead(previous) && isAwaitRead(statement) && !references(statement, declaredNames(previous))) {
        report('FAIL', file, at(statement), 'read-group', 'dos lecturas pegadas: cada lectura abre su grupo');
      }

      if (!glued && ts.isVariableStatement(previous) && !isMultiline(previous) && isGuardOf(previous, statement)) {
        report('FAIL', file, at(statement), 'guard-glue', 'el guard que valida la lectura de arriba va pegado a ella (gian-how-i-code 26)');
      }
    });
  };

  const isComponentName = (name) => /^[A-Z]/.test(name);
  const isHookName = (name) => /^use[A-Z]/.test(name);

  const isFeatureDataFile = /\.(queries|mutations)\.ts$/.test(file) || /[\\/]hooks[\\/]use[A-Z]\w*\.ts$/.test(file);

  const checkNode = (node) => {
    if (ts.isCallExpression(node) && !isFeatureDataFile && /^(useMutation|useQuery|useSuspenseQuery|useInfiniteQuery)$/.test(calleeName(node) ?? '')) {
      report('FAIL', file, at(node), 'data-hook-location', `${calleeName(node)} directo en la UI: va en un hook de <entity>.queries.ts / <entity>.mutations.ts (gian-how-i-code 13)`);
    }

    if (ts.isVariableStatement(node) && ts.isSourceFile(node.parent)) {
      const init = initializer(node);
      const strings = [];
      const collect = (child) => {
        if (ts.isStringLiteral(child) || ts.isNoSubstitutionTemplateLiteral(child)) strings.push(child.text);

        ts.forEachChild(child, collect);
      };

      if (init && (ts.isArrayLiteralExpression(init) || ts.isObjectLiteralExpression(init))) {
        ts.forEachChild(init, collect);

        if (strings.some(isClassList)) {
          report('FAIL', file, at(node), 'no-local-style-constants', 'constante de clases Tailwind: clases inline con cn(); si se repite, extraer componente (gian-how-i-code 04/23)');
        }
      }
    }

    if (ts.isIfStatement(node) && !node.elseStatement && !ts.isBlock(node.thenStatement) && isMultiline(node)) {
      report('FAIL', file, at(node), 'single-statement-if', 'el if ocupa varias líneas: lleva {}');
    }

    if (ts.isArrowFunction(node) && ts.isBlock(node.body) && node.body.statements.length === 1) {
      const only = node.body.statements[0];
      const owner = ts.isVariableDeclaration(node.parent) && ts.isIdentifier(node.parent.name) ? node.parent.name.text : '';

      if (ts.isReturnStatement(only) && only.expression && !isComponentName(owner) && !isHookName(owner)) {
        report('FAIL', file, at(node), 'arrow-implicit-return', 'una sola expresión: sin {} ni return');
      }
    }

    if (ts.isJsxAttribute(node) && node.name.getText(sf) === 'className' && node.initializer && ts.isJsxExpression(node.initializer)) {
      const expression = node.initializer.expression;
      const composed = expression && (ts.isTemplateExpression(expression) || ts.isConditionalExpression(expression) || (ts.isBinaryExpression(expression) && expression.operatorToken.kind === ts.SyntaxKind.PlusToken) || calleeName(expression) === 'join');

      if (composed) report('FAIL', file, at(node), 'classname-cn', 'className compuesto: usar cn() del repo');
    }

    if (ts.isJsxAttribute(node) && node.initializer && ts.isJsxExpression(node.initializer) && node.initializer.expression?.kind === ts.SyntaxKind.TrueKeyword) {
      report('FAIL', file, at(node), 'boolean-prop-shorthand', `${node.name.getText(sf)}={true} → ${node.name.getText(sf)}`);
    }

    if (ts.isJsxElement(node)) {
      const tag = node.openingElement.tagName.getText(sf);
      const hasKey = node.openingElement.attributes.properties.some((attribute) => ts.isJsxAttribute(attribute) && attribute.name.getText(sf) === 'key');

      if (/^(React\.)?Fragment$/.test(tag) && !hasKey) report('FAIL', file, at(node), 'fragment-shorthand', `<${tag}> sin key → <>`);
      if (node.children.every((child) => ts.isJsxText(child) && child.containsOnlyTriviaWhiteSpaces)) {
        report('FAIL', file, at(node), 'self-closing-jsx', `<${tag}></${tag}> → <${tag} />`);
      }
    }

    if ((ts.isVariableDeclaration(node) || ts.isFunctionDeclaration(node)) && node.name && ts.isIdentifier(node.name) && /^handle[A-Z]/.test(node.name.text) && node.name.text !== 'handleSubmit') {
      report('FAIL', file, at(node), 'handler-naming', `${node.name.text}: handle* prohibido en handlers (gian-how-i-code 04); usar on*/verbo`);
    }

    if (ts.isTypeAliasDeclaration(node) && ts.isUnionTypeNode(node.type) && node.type.types.length > 1 && node.type.types.every((type) => ts.isLiteralTypeNode(type) && ts.isStringLiteral(type.literal))) {
      report('GAP', file, at(node), 'enum-ownership', `type ${node.name.text} es unión de strings: si es APP_OWNED va string enum (gian-how-i-code 07)`);
    }

    if (ts.isBlock(node) || ts.isSourceFile(node) || ts.isModuleBlock(node) || ts.isCaseClause(node) || ts.isDefaultClause(node)) {
      const parent = node.parent;
      const owner = parent && (ts.isArrowFunction(parent) || ts.isFunctionExpression(parent) || ts.isFunctionDeclaration(parent)) ? unitName(parent) : null;
      const isSlotBody = (owner && (isComponentName(owner) || isHookName(owner)) && ts.isBlock(node)) || (isVue && ts.isSourceFile(node));

      if (isSlotBody) checkSlotBody([...node.statements]);
      else if (!ts.isSourceFile(node)) checkPlainBlock([...node.statements]);
    }

    ts.forEachChild(node, checkNode);
  };

  const unitName = (fn) => {
    if (ts.isFunctionDeclaration(fn)) return fn.name?.text ?? null;

    const parent = fn.parent;

    if (parent && ts.isVariableDeclaration(parent) && ts.isIdentifier(parent.name)) return parent.name.text;

    return null;
  };

  const checkRange = (fromLine, toLine) => {
    let previousBlank = false;

    for (let line = fromLine; line <= toLine; line += 1) {
      const content = lines[line - 1] ?? '';
      const blank = content.trim() === '';

      if (blank && previousBlank) report('FAIL', file, line + lineOffset, 'vertical-spacing', 'dos líneas en blanco seguidas');
      if (SECTION_COMMENT.test(content)) report('FAIL', file, line + lineOffset, 'comments-noise', 'comentario de sección: el espacio marca la sección');

      previousBlank = blank;
    }
  };

  if (isVue) {
    if (touched(sf)) {
      checkNode(sf);
      checkRange(1, lines.length);
    }

    return;
  }

  let anyTouched = false;

  for (const statement of sf.statements) {
    if (!touched(statement)) continue;

    anyTouched = true;
    checkNode(statement);
    checkRange(startLine(statement), endLine(statement));
  }

  if (!anyTouched || !file.endsWith('.tsx')) return;

  const classNames = new Map();
  const collectClassNames = (node) => {
    if (ts.isJsxAttribute(node) && node.name.getText(sf) === 'className' && node.initializer && ts.isStringLiteral(node.initializer) && node.initializer.text.length >= 40) {
      const entries = classNames.get(node.initializer.text) ?? [];

      entries.push(at(node));
      classNames.set(node.initializer.text, entries);
    }

    ts.forEachChild(node, collectClassNames);
  };

  collectClassNames(sf);

  for (const [, linesFound] of classNames) {
    const inScope = ranges === null || linesFound.some((line) => ranges.some(([start, end]) => line >= start && line <= end));

    if (linesFound.length >= 3 && inScope) {
      report('GAP', file, linesFound[0], 'repeated-block', `mismo className en ${linesFound.length} lugares (líneas ${linesFound.join(', ')}): si es el mismo bloque, extraer componente (gian-how-i-code 04)`);
    }
  }
};

const files = filesToCheck();

for (const file of files) {
  try {
    check(file);
  } catch (error) {
    report('GAP', file, 1, 'self-check', `no se pudo analizar: ${error.message}`);
  }
}

const seen = new Set();
const unique = findings.filter((finding) => {
  const key = `${finding.level}|${finding.file}|${finding.line}|${finding.rule}`;

  if (seen.has(key)) return false;

  seen.add(key);

  return true;
});

unique.sort((a, b) => a.file.localeCompare(b.file) || a.line - b.line);

for (const finding of unique) {
  console.log(`${finding.level.padEnd(4)} ${finding.file}:${finding.line} ${finding.rule} — ${finding.message}`);
}

const fails = unique.filter((finding) => finding.level === 'FAIL').length;
const gaps = unique.filter((finding) => finding.level === 'GAP').length;

console.log(`Self-check TS: ${fails} pendientes${gaps ? `, ${gaps} GAP` : ''} (${files.length} archivos)`);
process.exit(fails > 0 ? 1 : 0);
