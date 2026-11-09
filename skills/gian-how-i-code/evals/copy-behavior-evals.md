# Evals 1.4.15 — copy, idioma, convención

Local only. Do not commit.

## Cómo se corre

Dos registros separados.

Comprobación textual: las frases acordadas están en `SKILL.md`, `05`, `14`, `15` y `18`, y las frases viejas no. No prueba comportamiento.

Evaluación de comportamiento: contexto limpio, skill candidata cargada. El agente no recibe la respuesta esperada. Copy de operador se corrige salvo instrucción explícita de solo lectura. Se guarda la respuesta y el diff. Lo que afirma no cuenta si el entorno no cambió, o cambió de más.

| ID | Entrada | Éxito | Evidencia |
|---|---|---|---|
| COPY-1 | Durante el trabajo aparece copy de operador. No hay instrucción de solo lectura. | Lo corrige directo y resume el cambio. | Diff de ese texto. |
| COPY-2 | Instrucción explícita de solo analizar o no modificar archivos. | Propone sin editar. | Diff vacío. |
| COPY-3 | El producto administra integraciones. El texto dice “API key”. | Conserva “API key”. | El término sigue en el texto. |
| COPY-4 | El mensaje atribuye una causa que no está en la evidencia, o promete “en unos minutos”. | Propone una redacción sin inventar causa ni plazo. “Más tarde” solo si el fallo es temporal del servicio. | La propuesta no afirma servidor apagado ni datos guardados. |
| I18N-1 | El repo localiza por usuario. | Traduce mensajes y errores por campo. Conserva `code`, status y claves. | Recorre el locale existente. No inventa otro sistema. |
| I18N-2 | No existe ese recorrido. | Identifica la carencia y propone cómo cubrirla. No la implementa en el mismo corte. | Diff sin sistema de i18n nuevo. |
| TX-1 | B termina y después A falla, misma conexión. | Se revierten B y A. | Decisión, no solo la frase “savepoint”. |
| TX-2 | B falla y A continúa. | Solo si B ya revirtió y el parcial está autorizado. Opcional no conserva escrituras de B. | |
| TX-3 | A y B terminan bien, misma conexión. | Se confirma todo junto. | |
| TX-4 | Dos solicitudes compiten por el mismo slug. | La comprobación puede existir. No publica "Disponible". Guardar usa índice, atómico o bloqueo. | |
| SURFACE-1 | El campo ya consulta disponibilidad al salir. El valor guardado sigue libre. | No agrega "Disponible", check gris, ni botón Comprobar. Silencio, o un icono solo si señalar aporta. | Diff sin ese texto ni ese botón. |
| SURFACE-2 | El formulario ya tiene Guardar. Nadie pidió una acción aparte. | No agrega un segundo envío junto al campo. | Diff sin ese botón. |
| SURFACE-3 | Un grupo tiene un solo campo. | El título de la sección no repite la etiqueta. | |
| SURFACE-4 | El sistema no convierte importes, o un ejemplo es solo presentación. | No publica ese descargo. | Diff sin "Solo presentación" ni "Guardar no convierte". |
