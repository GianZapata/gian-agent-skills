# 22 — Calidad de diseño (Clean Code / SOLID operacional)

Cargar cuando: toda implementación (cada archivo tocado), auditoría de calidad, refactor de límites, traits, abstracciones, Actions hinchadas.

No es permiso para sobrearquitectar. Hacer el cambio más pequeño que mejore cohesión y claridad.

## Revisión en Implementar

En toda implementación se lee cada archivo tocado completo y se revisa contra esta reference.

- Un hallazgo dentro de lo escrito o tocado se corrige en el mismo cambio si es Alto. Media y Baja salen como pendiente con su propuesta.
- Un hallazgo fuera de las líneas tocadas no se edita. Sale con `archivo:línea` y su propuesta.
- No se abren archivos vecinos para buscar más. La revisión es del archivo tocado.
- Cada hallazgo lleva su severidad de las tablas de abajo. El resultado va en el cierre (`21` §Implementar, punto 13).

## Duplicación dentro del archivo

Dos apariciones ya son hallazgo.

- El mismo cálculo, validación o transformación, aunque cambien los nombres de las variables: Media. Propuesta: método privado, constante o helper local.
- Dos bloques de la misma forma (un guard repetido, dos `useState` iguales, dos handlers con el mismo cuerpo): Baja. Propuesta genérica.
- Las líneas triviales no cuentan.

Dentro de lo escrito o tocado, el duplicado se extrae. Fuera de lo tocado se reporta.

## Dirección de dependencias

Cada capa depende de la de abajo. Lo que la salta es hallazgo.

| Observado | Severidad |
|-----------|-----------|
| Controller que consulta o calcula | Alta |
| Action que lee `request()` o `auth()`, o devuelve una respuesta HTTP. Recibe el actor y el DTO | Alta |
| Resource que dispara queries (`06`) | Alta |
| Modelo que llama a un servicio externo | Media |
| Componente que llama a `fetch`, `axios` o al cliente HTTP. Pasa por service y query (`14`) | Media |
| Helper o util que importa React, router o un store | Media |

El flujo Laravel está en `05` y la estructura de feature en `03` y `04`. Esta reference no los repite.

## Traits

**Dónde vive el archivo:** `05`. `app/Traits/<anfitrión>/`, un solo nivel. Un trait de modelo es `app/Traits/Models/Nombre.php`, namespace `App\Traits\Models`.

Usar traits solo para comportamiento **horizontal, cohesivo y reutilizado** por varias clases.

**Buenos casos:** auditoría técnica, integración con un paquete, scopes cohesivos, tenancy, metadata compartida, adaptación exigida por framework (p. ej. `HasStateMachines`), bloque de validación de un eje reutilizado por requests de entidades distintas (`05`).

**No usar traits para:** esconder reglas de negocio; evitar una Action; compartir código entre dos clases sin abstracción clara; service locator; side effects ocultos; simular herencia múltiple; cajones de métodos no relacionados; compartir reglas entre el Store y el Update de una misma entidad (base abstracta, `05`).

**Señales de hallazgo:** muchas dependencias implícitas; varios dominios; queries/eventos no evidentes; conflictos de métodos; tests solo vía modelo consumidor.

Si el comportamiento tiene dependencias, configuración, estado propio o side effects, usar **composición** (MUST). Prohibido un trait o una herencia para eso.

## SOLID operacional

| Principio | Regla práctica |
|-----------|----------------|
| SRP | Controller HTTP; el schema del borde valida (FormRequest); el service es el caso de uso (Action en Laravel); Query lectura; el serializer serializa (Resource); SM transiciones; Adapter para lo externo (Service en Laravel) |
| OCP | Sin abstracciones anticipadas; aplicar cuando haya variación real (proveedores, estrategias, central/tenant) |
| LSP | Prohibida la herencia que desactiva al padre; usar composición |
| ISP | Interfaces pequeñas por capacidad; no contratos enormes |
| DIP | Inyectar contratos en límites externos (pagos, storage, notificaciones, HTTP externo). No interface por cada clase interna estable |

## Clean Code accionable

- Prohibido agregar parámetros `bool` de modo (`bool $notify, bool $force…`) a una Action nueva o tocada. Usar un enum o métodos separados.
- No mezclar lecturas y mutaciones complejas en el mismo método.
- No clases `Manager` / `Helper` / `Service` **cajón de sastre** (multi-dominio). Sí se permiten `*Helper` con **un solo eje cohesivo** (`DateHelper`, `NumberHelper`, `UserHelper`, etc.) — ver `23`.
- Nombres del dominio.
- Prohibida una clase abstracta con una sola implementación.
- En Actions y servicios de dominio, toda dependencia va por constructor. Prohibido resolver otra Action, un servicio de dominio o un adaptador con `app()` o con una Facade dentro de la clase. El constructor no autoriza una clase nueva.
- No crear `Support` ni agregar un archivo ahí porque la carpeta existe. El lugar lo decide `05`: config, modelo, enum, helper, adaptador, método privado o fixture.
- Transacciones en la Action dueña del caso de uso. Eventos, jobs, mails, notificaciones y llamadas externas disparados dentro de una transacción van `afterCommit` (`05`).
- Métodos privados para pasos legibles, no solo para acortar.
- Value Objects cuando haya invariantes reales.
- Una duplicación fuera de lo tocado no se extrae: se reporta con la severidad de «Duplicación dentro del archivo».
- Si **ya existe** un `*Helper`/util de área y el código lo reimplementa → hallazgo (reutilizar/extender) — ver `23`.
- Revisar N+1, cohesión, acoplamiento y side effects ocultos. El resultado de N+1 y de side effects ocultos se registra en el cierre o en el reporte.

## Hallazgos típicos

| Observado | Severidad |
|-----------|-----------|
| Trait de negocio que escribe o dispara efectos externos | Alta |
| Trait de negocio con efectos ocultos que solo leen (queries) | Media |
| Action que valida + serializa + notifica + cobra | Alta |
| Interface inútil de una sola implementación estable | Baja (sobreingeniería) |
| N+1 en listado | Alta |
| Reimplementar capacidad de `*Helper`/util ya existente | Media (`23`) |
| Mismo cálculo, validación o transformación dos veces en un archivo | Media |
| Dos bloques de la misma forma en un archivo | Baja |
| Controller que consulta o calcula; Action que lee `request()` / `auth()` | Alta |
| Componente que llama al cliente HTTP; helper que importa React o un store | Media |
