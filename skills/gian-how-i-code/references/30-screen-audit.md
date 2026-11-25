# 30 — Auditoría de pantalla

El código puede estar bien y la pantalla no servir. Esta reference audita lo que el usuario **ve y hace**: qué dice, a dónde lleva y cómo se presenta la información. Aplica a toda pantalla o sección con UI visible, en Auditar e Implementar.

No reemplaza `visual-quality.md`: este capítulo detecta y clasifica; la propuesta visual sale de la skill principal que esa guía elige para la superficie.

## Procedimiento (en orden, por pantalla o sección)

### 1. Quién y para qué

Escribir en una frase quién lee la pantalla y qué pregunta viene a responder.

```text
Torres (dashboard central): el operador central quiere saber qué torre necesita atención hoy.
```

Si no se puede escribir esa frase, la pantalla no tiene foco: primer hallazgo.

### 2. Cada elemento contra la pregunta

Cada métrica, columna, tarjeta o bloque ayuda a responder la pregunta del punto 1, o no. Lo que no ayuda se mueve a la vista de detalle o se quita. Se juzga con datos reales (o seed realista), no con el mock. Un control que no encaja con el dato o el contexto, o una ayuda ágil que falta (slug, dominio, dinero, default visible, fecha con atajos), es hallazgo según `31`.

### 3. Lenguaje

Cada texto nombra lo que significa para quien lee, no el mecanismo que lo produce.

- BAD: "Webhooks Stripe fallidos — últimos 30 días"
- GOOD: "Pagos sin confirmar — últimos 30 días"

El nombre de un proveedor o de una pieza técnica se conserva solo si quien lee la pantalla la opera. Reglas de copy: `15` §Copy.

### 4. Acciones coherentes

Cada botón, link, CTA, tarjeta o fila clicable promete un resultado. Al hacer click, el usuario ve:

- la pantalla que nombra el texto;
- el filtro que nombra el texto, ya aplicado y visible;
- la misma cantidad que anunciaba el aviso ("3 torres con alertas" → 3 filas).

Si el destino no puede mostrar eso, se cambia el texto o se cambia la acción. Nunca quedan desalineados.

Cómo se comprueba:

1. Recorrer cada `onClick`, `navigate`, `<Link>`, `href` o setter de scope/filtro con texto visible (`rg -n "onClick|navigate\(|<Link|to=|href=" <pantalla>`).
2. Comparar el texto contra la ruta, el search param o el scope de destino, y contra lo que el destino renderiza con ese estado.
3. Abrirlo en el navegador (punto 7). En Implementar, el test verifica el destino o el filtro aplicado.

Ejemplo: "Ver con alertas →" llama a `onScopeChange(CentralDashboardScope.Attention)`. Si la vista resultante no muestra solo las torres con alertas, con el filtro visible, es incoherente.

### 5. Densidad y jerarquía

Una tabla o lista resumen (dashboard, overview) responde «¿cuál necesita atención?»; el detalle vive en la vista de detalle.

- Máximo 5–6 columnas: identidad (nombre + un dato secundario), estado, 2–4 métricas clave, acción.
- Máximo 2 líneas por celda. Un dato que necesita una tercera línea no es de resumen.
- Una celda no junta varias métricas ("N contratos · clientes · usuarios").
- Dato principal visible primero; secundario en tono atenuado.
- Métricas alineadas a la derecha con `tabular-nums`.
- Lo que pide atención (vencido, pendiente, error) se resalta con un token semántico; el resto queda neutro. Si todo está resaltado, nada lo está.
- Fila clicable: indicador visible (chevron, hover) y su destino cumple el punto 4.

Tarjetas, KPIs y bloques siguen la misma lógica: un dato principal por tarjeta, sin apilar métricas que no responden la pregunta.

### 6. Estados

Vacío, cargando (skeleton con forma, Hard Rule «Carga con forma»), error, y el caso extremo: nombres largos, valores en 0, muchísimos registros. Cada uno se ve bien y dice algo útil.

### 7. Visto en vivo

Abrir la pantalla real a 375, 768 y 1440 px (`visual-quality.md`). Densidad, jerarquía, truncado y coherencia de acciones no se dan por cubiertos leyendo solo el código: si no se abrió, el reporte lo dice («leído, no visto»).

## Severidad

| Severidad | Caso |
|-----------|------|
| Alta | Acción que lleva a otro lado o no aplica el filtro que nombra; término técnico en navegación o título principal |
| Media | Término técnico en el contenido; tabla resumen con más de 6 columnas o celdas de 3+ líneas; varias métricas en una celda; elemento que no responde la pregunta del punto 1; estado vacío/error sin mensaje útil |
| Baja | Jerarquía (principal/secundario), alineación numérica, resaltado excesivo o ausente |

## Formato del hallazgo

```text
### H-NNN — <título>
Pantalla: <ruta> — <sección>   Archivo: <ruta:línea>
Qué ve el usuario: …
Por qué estorba: … (punto N de 30)
Propuesta: … (tras cargar visual-quality.md; skill principal: …)
Visto en vivo: sí (375/768/1440) | no (leído, no visto)
```

En Auditar no se edita. En Implementar, lo que está dentro de la unidad tocada se corrige; lo de fuera se reporta.
