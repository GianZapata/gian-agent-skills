# Evals 1.4.16 — caso de uso backend

Local only. Do not commit.

El agente no recibe la columna Esperado. Se mira el diff y, si hubo ejecución, el estado de la base. Una explicación no demuestra rollback.

| ID | Entrada | Esperado |
|---|---|---|
| UC-1 | Borrado simple ya protegido por policy, modelo y constraint | Lo justifica y lo deja |
| UC-2 | La Action hija falla y la principal captura | Mira qué queda confirmado |
| UC-3 | Dos solicitudes compiten por un cupo | Protege la escritura, no solo el chequeo previo |
| UC-4 | No hay una regla extra y eso no cambia el caso | Lo deja. No lo marca pendiente |
| UC-5 | Hay que crear o corregir un flujo autorizado | El diff cumple el contrato conocido |
| UC-6 | Se afirma rollback o protección de concurrencia | Se comprueba el estado resultante |
