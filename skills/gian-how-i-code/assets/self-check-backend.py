#!/usr/bin/env python3
"""Structural self-check for a Laravel backend (gian-how-i-code `05`).

Usage: python3 self-check-backend.py <repo-root> [<path-inside-app> ...]

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
    r"PhpSpreadsheet|OpenSpout|Process::|proc_open|socket_",
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
        "raw-dompdf-new",
        re.compile(r"\bnew\s+\\?(?:Dompdf\\)?Dompdf\b"),
        lambda rel: rel.startswith("app/"),
        "instancia directa de `Dompdf`; usar `barryvdh/laravel-dompdf` + Blade en `resources/views/pdf/` (`32` §9)",
    ),
]


def php_files(root: Path, targets: list[str]) -> list[Path]:
    bases = [root / t for t in targets] if targets else [root / "app"]
    files: list[Path] = []
    for base in bases:
        if base.is_file() and base.suffix == ".php":
            files.append(base)
        elif base.is_dir():
            files.extend(p for p in base.rglob("*.php") if "vendor" not in p.parts)
    return sorted(set(files))


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 2
    root = Path(sys.argv[1]).resolve()
    files = php_files(root, sys.argv[2:])
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

        parts = rel.split("/")
        if rel.startswith("app/Actions/"):
            findings.append(f"FAIL {rel}:1 non-canonical-root — Actions solo en `app/Http/Actions/<Contexto>/`")
        if rel.startswith(("app/Http/Actions/", "app/Queries/")) and len(parts) == (4 if rel.startswith("app/Http") else 3) \
                and not parts[-1].startswith("Base"):
            findings.append(f"FAIL {rel}:1 loose-root — archivo suelto; va en `<raíz>/<Contexto>/`")

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

    for finding in findings:
        print(finding)
    touched = len({f.split(":")[0] for f in findings})
    print(f"Self-check backend: {len(findings)} pendientes ({len(files)} archivos, {touched} con hallazgos)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
