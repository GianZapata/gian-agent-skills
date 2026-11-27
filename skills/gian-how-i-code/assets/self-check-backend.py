#!/usr/bin/env python3
"""Structural self-check for a Laravel backend (gian-how-i-code `05`).

Usage: python3 self-check-backend.py <repo-root> [--glossary <file>] [<path-inside-app> ...]

`--glossary` takes a file with one `old_column new_column` pair per line
(`#` comments allowed). Any string literal in `app/` that still names an old
column is reported as `schema-column-drift` (`05` DoD, schema/code parity).

Without paths it scans all of `app/`. With paths (for example
`app/Http/Actions/Electoral app/Http/Controllers/Admin/ActController.php`)
it scans only those, which is how a migrated module is checked.

Exit 0: no findings. Exit 1: findings. Exit 2: nothing to scan (GAP).
"""

import re
import sys
from pathlib import Path

INTEGRATION_MARKERS = re.compile(
    r"Http::|Guzzle|curl_|Storage::disk|SimpleXML|XMLReader|DOMDocument|fopen\(|ZipArchive|"
    r"PhpSpreadsheet|OpenSpout|Process::|proc_open|socket_|Storage::|SplFileObject|fgetcsv\(|"
    r"new \\?\w*Client\(|\\Stripe\\|Gateway\b",
)

CHECKS = [
    (
        "legacy-core",
        re.compile(r"^use App\\Core\\", re.M),
        lambda rel: True,
        "pieza del framework legacy (`App\\Core\\*`); se reemplaza por lo nativo en el módulo (`05` §Migración)",
    ),
    (
        "inline-new",
        re.compile(r"\(?new [A-Z]\w*(Service|Store|Action|Query)\b"),
        lambda rel: True,
        "instancia inline; la dependencia se inyecta (`22` Inyección)",
    ),
    (
        "service-imports-action",
        re.compile(r"^use App\\Http\\Actions\\", re.M),
        lambda rel: rel.startswith("app/Services/"),
        "Service que importa Actions (dependencia invertida)",
    ),
    (
        "input-validation-in-code",
        re.compile(r"new (\\?[\w\\]*)?ValidationException\(|ValidationException::withMessages\("),
        lambda rel: rel.startswith(("app/Http/Actions/", "app/Http/Controllers/")),
        "validación de entrada fuera del FormRequest; va en `rules()` / `after()`",
    ),
    (
        "resource-resolve",
        re.compile(r"->resolve\(\)"),
        lambda rel: rel.startswith("app/Http/Controllers/"),
        "`->resolve()` en el Controller; se devuelve el Resource (`05` Respuesta del Controller)",
    ),
    (
        "resource-fields-map",
        re.compile(r"const FIELDS\s*="),
        lambda rel: rel.startswith("app/Http/Resources/"),
        "mapa mágico `FIELDS`; solo `toArray` explícito (`05` Claves del Resource)",
    ),
    (
        "resource-cast",
        re.compile(r"=>\s*\((int|bool|float|string|array)\)"),
        lambda rel: rel.startswith("app/Http/Resources/"),
        "cast en el Resource; va en `$casts` del Model",
    ),
    (
        "resource-route-branch",
        re.compile(r"\$request->(is|routeIs)\("),
        lambda rel: rel.startswith("app/Http/Resources/"),
        "el Resource ramifica por ruta",
    ),
    (
        "action-trait-writes-db",
        re.compile(r"->(?:create|update|delete|forceDelete|upsert|insert|save)\(|DB::(?:transaction|table)\("),
        lambda rel: rel.startswith("app/Traits/Actions/"),
        "trait en `app/Traits/Actions/` que escribe en BD (Service disfrazado; `22` §Traits / `05` §Migración)",
    ),
    (
        "legacy-runtime",
        re.compile(r"^use App\\(?:Runtime|Core|Legacy\w*)\\|\bsession_start\(|\$_SESSION\b", re.M),
        lambda rel: True,
        "runtime hecho a mano (sesión/CSRF/auth/validator/view); renombrarlo no lo vuelve nativo (`05` DoD)",
    ),
    (
        "raw-dompdf-new",
        re.compile(r"\bnew\s+\\?(?:Dompdf\\)?Dompdf\b"),
        lambda rel: rel.startswith("app/"),
        "instancia directa de `Dompdf`; usar `barryvdh/laravel-dompdf` + Blade en `resources/views/pdf/` (`32` §9)",
    ),
    (
        "legacy-auth-array",
        re.compile(r"toLegacyArray\(|\bActorHelper::|->attributes->get\('user'\)"),
        lambda rel: True,
        "usuario legacy como array; se lee `auth()->user()` (`User`) y sus métodos (`05` DoD)",
    ),
    (
        "parallel-exceptions",
        re.compile(r"^\s*\}?\s*catch \(", re.M),
        lambda rel: rel.startswith("app/Http/Controllers/"),
        "try/catch en el Controller; la excepción sube a `CustomException` / el handler (`05` Errores)",
    ),
    (
        "response-envelope",
        re.compile(r"'ok'\s*=>"),
        lambda rel: rel.startswith("app/Http/"),
        "sobre `'ok' =>` hecho a mano; el status HTTP y el Resource ya dicen si salió bien (`05` Respuesta del Controller)",
    ),
    (
        "hand-validator",
        re.compile(r"Validator::make\(|\$request->(?:merge|replace)\("),
        lambda rel: rel.startswith(("app/Http/Controllers/", "app/Http/Actions/", "app/Services/")),
        "validación o mutación del Request fuera del FormRequest; va en `rules()` / `prepareForValidation()`",
    ),
    (
        "redirect-literal",
        re.compile(r"redirect\(\s*['\"]/"),
        lambda rel: True,
        "redirect a URL literal; usar `to_route('<nombre>')` (`05` Rutas)",
    ),
]

PUBLIC_METHOD = re.compile(r"^\s*public (?:static )?function (\w+)\(", re.M)


STRING_LITERAL = re.compile(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"")
LEGACY_DIRS = ("app/Runtime/", "app/Core/", "app/Legacy")
WEBHOOK_DISPATCH = re.compile(r"::dispatch\(|dispatch\(|Bus::|->onQueue\(")


def load_glossary(path: Path) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        old, _, new = line.replace("=", " ").partition(" ")
        pairs.append((old.strip(), new.strip()))
    return pairs


DOMAIN_SERVICE_CONSUMERS = ("app/Http/Controllers/", "app/Console/", "app/Http/Resources/", "app/Jobs/", "app/Http/Middleware/")
DB_TOUCH = re.compile(
    r"\bDB::|::query\(|::where\w*\(|::find\w*\(|::first\w*\(|::all\(|::create\(|::updateOrCreate\(|"
    r"->save\(|->update\(|->insert\(|->upsert\(|->increment\(|->decrement\(|->refresh\(",
)
DB_WRITE = re.compile(r"->save\(|::create\(|->update\(|DB::transaction|->insert\(|->upsert\(|::updateOrCreate\(|->forceDelete\(|Model::destroy\(")


def is_domain_service(path: Path) -> bool:
    """A Service class that reads or writes the database: either it does no outside I/O, or it also writes rows.

    Pure builders/parsers with no database access and clients/stores that only talk to the outside are not domain.
    """
    if not path.exists():
        return False
    posix = path.as_posix()
    if any(part in posix for part in ("/Contracts/", "/DTO/", "/Exceptions/")):
        return False
    body = path.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"^(final\s+|abstract\s+|readonly\s+)*class\s", body, re.M):
        return False
    if not DB_TOUCH.search(body):
        return False
    return not INTEGRATION_MARKERS.search(body) or bool(DB_WRITE.search(body))


def delegates_dispatch(root: Path, text: str) -> bool:
    """True when an imported Action/Service of the webhook entry point dispatches a Job."""
    for match in re.finditer(r"^use (App\\(?:Http\\Actions|Services)\\[\w\\]+);", text, re.M):
        target = root / "app" / (match.group(1)[len("App\\"):].replace("\\", "/") + ".php")
        if target.exists() and WEBHOOK_DISPATCH.search(target.read_text(encoding="utf-8", errors="replace")):
            return True
    return False


def php_files(root: Path, targets: list[str]) -> list[Path]:
    bases = [root / t for t in targets] if targets else [root / "app"]
    files: list[Path] = []
    for base in bases:
        if base.is_file() and base.suffix == ".php":
            files.append(base)
        elif base.is_dir():
            files.extend(p for p in base.rglob("*.php") if "vendor" not in p.parts)
    return sorted(set(files))


def snake_plural(name: str) -> str:
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    if snake.endswith("y") and not snake.endswith(("ay", "ey", "oy", "uy")):
        return snake[:-1] + "ies"
    return snake if snake.endswith("s") else snake + "s"


def alias_model_findings(root: Path) -> list[str]:
    models = sorted((root / "app" / "Models").rglob("*.php")) if (root / "app" / "Models").exists() else []
    tables: dict[str, list[tuple[str, bool, int]]] = {}
    for path in models:
        text = path.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"extends\s+\\?[\w\\]*(Model|Authenticatable|Pivot)\b", text):
            continue
        match = re.search(r"protected \$table\s*=\s*['\"](\w+)['\"]", text)
        table = match.group(1) if match else snake_plural(path.stem)
        line = text.count("\n", 0, match.start()) + 1 if match else 1
        tables.setdefault(table, []).append((path.relative_to(root).as_posix(), bool(match), line))
    names = {path.stem for path in models}
    findings = []
    for path in models:
        text = path.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"class \w+ extends \\?(?:App\\Models\\)?(\w+)\b", text)
        if match and match.group(1) in names:
            line = text.count("\n", 0, match.start()) + 1
            findings.append(
                f"FAIL {path.relative_to(root).as_posix()}:{line} alias-model — alias de `{match.group(1)}`; "
                "los consumidores usan ese Model (`05` DoD)"
            )
    for table, owners in tables.items():
        if len(owners) < 2:
            continue
        for rel, explicit, line in owners:
            if explicit:
                others = ", ".join(o[0].rsplit("/", 1)[-1] for o in owners if o[0] != rel)
                findings.append(f"FAIL {rel}:{line} alias-model — tabla `{table}` ya es de {others}; un Model por tabla (`05` DoD)")
    return findings


def policy_findings(root: Path) -> list[str]:
    policies = sorted((root / "app" / "Policies").glob("*Policy.php")) if (root / "app" / "Policies").exists() else []
    if not policies:
        return []
    corpus = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for base in ("app", "routes")
        if (root / base).exists()
        for path in (root / base).rglob("*.php")
        if "/Policies/" not in path.as_posix()
    )
    uses = re.compile(r"(?:authorize\(|Gate::\w+\(|->can(?:not)?\(|can:|Gate::policy\()[^\n]*")
    used = " ".join(m.group(0) for m in uses.finditer(corpus))
    findings = []
    for path in policies:
        model = path.stem[: -len("Policy")]
        if not re.search(rf"\b{re.escape(model)}\b|\${model[:1].lower() + model[1:]}\b", used):
            findings.append(
                f"FAIL {path.relative_to(root).as_posix()}:1 policy-unused — ninguna ruta ni Controller autoriza `{model}`; "
                "se conecta (`authorize` / `can:`) o se borra (`05` Autorización)"
            )
    return findings


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 2
    args = sys.argv[2:]
    glossary: list[tuple[str, str]] = []
    if "--glossary" in args:
        index = args.index("--glossary")
        glossary = load_glossary(Path(args[index + 1]))
        args = args[:index] + args[index + 2:]
    root = Path(sys.argv[1]).resolve()
    files = php_files(root, args)
    if not files:
        print("GAP self-check backend: 0 archivos PHP en el alcance; pasa rutas dentro de app/")
        return 2

    findings: list[str] = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")

        for name, pattern, applies, message in CHECKS:
            if not applies(rel):
                continue
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"FAIL {rel}:{line} {name} — {message}")

        if rel.startswith("app/Http/Exceptions/"):
            findings.append(f"FAIL {rel}:1 parallel-exceptions — familia de excepciones paralela; se usa `CustomException` / `abort` / `ValidationException` (`05` Errores)")

        if rel.startswith(("app/", "app/Http/")) and re.search(r"/\w+Validator\.php$", rel) and "app/Rules/" not in rel:
            findings.append(f"FAIL {rel}:1 hand-validator — validador hecho a mano; las reglas viven en el FormRequest o en `app/Rules/`")

        if rel.startswith("app/Http/Actions/"):
            extra = [m for m in PUBLIC_METHOD.finditer(text) if m.group(1) not in ("__construct", "handle")]
            for match in extra:
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"FAIL {rel}:{line} action-mold — método público `{match.group(1)}`; una Action tiene solo `handle()` (`05` Action)")
            if re.match(r"(Get|List|Show|Find|Fetch)[A-Z]", parts_name := rel.rsplit("/", 1)[-1]):
                findings.append(f"FAIL {rel}:1 action-mold — `{parts_name}` es una lectura; va en `app/Queries/<Contexto>/` (`05` Query)")

        if rel.startswith(LEGACY_DIRS):
            findings.append(f"FAIL {rel}:1 legacy-runtime — carpeta del runtime legacy; se borra, no se renombra (`05` DoD)")

        if glossary:
            columns = {old: new for old, new in glossary}
            pattern = re.compile(r"\b(" + "|".join(map(re.escape, columns)) + r")\b")
            for literal in STRING_LITERAL.finditer(text):
                for match in pattern.finditer(literal.group(0)):
                    line = text.count("\n", 0, literal.start()) + 1
                    findings.append(
                        f"FAIL {rel}:{line} schema-column-drift — columna `{match.group(1)}` ya no existe; "
                        f"es `{columns[match.group(1)]}` (`05` DoD)"
                    )

        if "ZipArchive" in text and "xl/worksheets" in text:
            findings.append(f"FAIL {rel}:1 hand-rolled-xlsx — lector XLSX a mano; usar el Reader de openspout (`32` §9 Imports)")

        if re.search(r"Webhook", rel) and rel.startswith(("app/Http/Controllers/", "app/Services/")) \
                and not WEBHOOK_DISPATCH.search(text) and not delegates_dispatch(root, text):
            findings.append(f"FAIL {rel}:1 sync-webhook — webhook procesado en el request; responder y despachar un Job (`28` regla 12)")

        parts = rel.split("/")
        if rel.startswith("app/Actions/"):
            findings.append(f"FAIL {rel}:1 non-canonical-root — Actions solo en `app/Http/Actions/<Contexto>/`")
        if rel.startswith(("app/Http/Actions/", "app/Queries/")) and len(parts) == (4 if rel.startswith("app/Http") else 3) \
                and not parts[-1].startswith("Base"):
            findings.append(f"FAIL {rel}:1 loose-root — archivo suelto; va en `<raíz>/<Contexto>/`")

        if rel.startswith(DOMAIN_SERVICE_CONSUMERS):
            for match in re.finditer(r"^use (App\\Services\\[\w\\]+);", text, re.M):
                service = root / "app" / (match.group(1)[len("App\\"):].replace("\\", "/") + ".php")
                if is_domain_service(service):
                    line = text.count("\n", 0, match.start()) + 1
                    findings.append(
                        f"FAIL {rel}:{line} controller-uses-domain-service — `{match.group(1)}` es un Service de dominio; "
                        "se borra y el consumidor llama a la Action o Query (`05` §Migración)"
                    )

        if rel.startswith("app/Http/Actions/"):
            for match in re.finditer(r"^use (App\\Services\\[\w\\]+);", text, re.M):
                service = root / "app" / (match.group(1)[len("App\\"):].replace("\\", "/") + ".php")
                body = service.read_text(encoding="utf-8", errors="replace") if service.exists() else ""
                if not INTEGRATION_MARKERS.search(body):
                    line = text.count("\n", 0, match.start()) + 1
                    findings.append(
                        f"FAIL {rel}:{line} action-uses-domain-service — `{match.group(1)}` no llama fuera; "
                        "se disuelve en Actions/Queries (`05` §Migración)"
                    )

    if not args:
        findings.extend(policy_findings(root))
        findings.extend(alias_model_findings(root))

    bootstrap = root / "bootstrap" / "app.php"
    if not args and bootstrap.exists():
        text = bootstrap.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"Legacy\w*", text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"FAIL bootstrap/app.php:{line} legacy-runtime — middleware `{match.group(0)}` del runtime legacy")

    for finding in findings:
        print(finding)
    touched = len({f.split(":")[0] for f in findings})
    print(f"Self-check backend: {len(findings)} pendientes ({len(files)} archivos, {touched} con hallazgos)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
