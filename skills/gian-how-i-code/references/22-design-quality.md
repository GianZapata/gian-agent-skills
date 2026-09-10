# 22 — Calidad de diseño (Clean Code / SOLID operacional)

Cargar cuando: auditoría de calidad, refactor de límites, traits, abstracciones, Actions hinchadas.

No es permiso para sobrearquitectar. Preferir el cambio más pequeño que mejore cohesión y claridad.

## Traits

Usar traits solo para comportamiento **horizontal, cohesivo y reutilizado** por varias clases.

**Buenos casos:** auditoría técnica, integración con un paquete, scopes cohesivos, tenancy, metadata compartida, adaptación exigida por framework (p. ej. `HasStateMachines`).

**No usar traits para:** esconder reglas de negocio; evitar una Action; compartir código entre dos clases sin abstracción clara; service locator; side effects ocultos; simular herencia múltiple; cajones de métodos no relacionados.

**Señales de hallazgo:** muchas dependencias implícitas; varios dominios; queries/eventos no evidentes; conflictos de métodos; tests solo vía modelo consumidor.

Preferir **composición** cuando haya dependencias, configuración, estado propio o side effects relevantes.

## SOLID operacional

| Principio | Regla práctica |
|-----------|----------------|
| SRP | Controller HTTP; FormRequest valida; Action caso de uso; Query lectura; Resource serializa; SM transiciones; Service/Adapter externo |
| OCP | Sin abstracciones anticipadas; aplicar cuando haya variación real (proveedores, estrategias, central/tenant) |
| LSP | Evitar herencia que desactiva al padre; preferir composición |
| ISP | Interfaces pequeñas por capacidad; no contratos enormes |
| DIP | Inyectar contratos en límites externos (pagos, storage, notificaciones, HTTP externo). No interface por cada clase interna estable |

## Clean Code accionable

- Evitar boolean blindness en Actions (`bool $notify, bool $force…`).
- No mezclar lecturas y mutaciones complejas en el mismo método.
- No clases `Manager` / `Helper` / `Service` **cajón de sastre** (multi-dominio). Sí se permiten `*Helper` con **un solo eje cohesivo** (`DateHelper`, `NumberHelper`, `UserHelper`, etc.) — ver `23`.
- Nombres del dominio.
- Evitar herencia abstracta anticipada.
- Dependencias visibles (constructor); no `app()`/`Facade` si ocultan deps relevantes en dominio.
- Transacciones en la Action dueña del caso de uso; side effects post-commit cuando corresponda.
- Métodos privados para pasos legibles, no solo para acortar.
- Value Objects cuando haya invariantes reales.
- No extraer abstracción por una sola duplicación accidental.
- Si **ya existe** un `*Helper`/util de área y el código lo reimplementa → hallazgo (reutilizar/extender); distinto de “no extraer por una sola dup accidental” — ver `23`.
- Revisar N+1, cohesión, acoplamiento, side effects ocultos.

## Hallazgos típicos

| Observado | Severidad sugerida |
|-----------|-------------------|
| Trait de negocio con side effects | Alta/Media |
| Action que valida + serializa + notifica + cobra | Alta |
| Interface inútil de una sola implementación estable | Baja (sobreingeniería) |
| N+1 en listado | Alta |
| Reimplementar capacidad de `*Helper`/util ya existente | Media (`23`) |
