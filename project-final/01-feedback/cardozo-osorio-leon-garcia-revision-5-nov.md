# Retroalimentación · Revisión del 5 de noviembre

**Proyecto:** Droguerías San Pedro
**Estudiantes:** Camilo Andrés Cardozo Osorio y Sergio Andrés León García
**Revisión:** jueves 5 de noviembre de 2026 · Docente Jesús Ariel González Bonilla
**Avance revisado:** fork `cacardozo2019-1-stack`, `14-week/01-session/proyecto-camilo-cardozo-sergion-leon.pbix` (commit `588ccc8`)

Ya hay un `.pbix` con datos cargados y cinco medidas DAX. Es un buen paso. **La prioridad para la entrega del jueves 12 de noviembre es mejorar los gráficos**, porque el tablero debe sumarle valor a la droguería: no se trata de colocar gráficas por colocarlas.

## 1. Mejorar los gráficos

Los cinco gráficos del tablero son de columnas y cada uno tiene solo una medida, sin eje ni categoría. Por eso cada uno muestra una sola barra, con un total que no deja ver dónde está el problema. Este es el cambio propuesto:

| Hoy | Mejor así | Decisión que apoya |
|---|---|---|
| Columna con Tasa Quiebre Stock | Barras por sede y otras por producto, de mayor a menor | Dónde reforzar el inventario |
| Columna con Total Ingresos | Tarjeta arriba, y línea por mes para ver la tendencia | Cómo va el negocio y en qué meses cae |
| Columna con Total Costo | Tarjeta o columna junto a ingresos, por categoría | Qué categorías cuestan más |
| Columna con Margen Bruto | Tarjeta arriba, y barras por categoría | Qué categorías dejan más ganancia |
| Columna con % Margen Bruto | KPI con su meta, y comparación por sede | Qué sede rinde menos |

Agreguen además:

- **Venta perdida:** (CantidadSolicitada − CantidadVendida) × precio de venta, por sede y por producto. Es el indicador más valioso, porque le pone plata al problema de quiebre de stock.
- **Segmentadores:** al menos sede, categoría y mes.
- **Jerarquía con drill-down:** de categoría a producto.
- **Títulos con el hallazgo:** por ejemplo, «Prado Alto pierde más ventas por falta de existencias», si los datos lo muestran. El título debe decir lo que se ve, no repetir el nombre de la medida.
- **Orden de lectura:** tarjetas arriba, tasa de quiebre y venta perdida primero, y detalle abajo.

Para cada gráfico pregúntense: **¿qué decisión toma la droguería con esto?** Si no hay respuesta, se quita. El tablero debe cerrar con una recomendación concreta: qué trasladar o pedir, a qué sede y cuándo.

## 2. Lo que necesitan los gráficos para funcionar

- **Relaciones.** Solo está la de `Fact_Ventas` con `Dim_Productos`. Sin las de fecha, sede y cliente, los gráficos por sede o por mes no van a filtrar bien.
- **`Dim_Sedes` y `Dim_Clientes`.** Quedaron con columnas `Column1`, `Column2` y la fila de títulos como dato. Usen «Usar la primera fila como encabezado».
- **Calendario.** Marquen `Dim_Calendario` como tabla de fechas y desactiven «Fecha y hora automáticas».

## 3. Para completar la entrega

- **Limpieza real en Power Query.** Hoy solo hay encabezados y tipos de dato. Documenten al menos tres problemas de calidad con su antes y después.
- **Carpeta del proyecto.** Muevan el `.pbix` a `15-week/proyecto-aula/` y suban el archivo de datos. Sin él no se pueden verificar las cifras.
- **Documentación.** Sigue pendiente lo de la Fase 0: `README.md` con la ficha, `empresa.md` (real o ficticia) y `kpi.md`. Agreguen el diccionario de datos, las cifras de control y la prueba del clic.
- **`13-week/proyecto.xlsx`.** Sigue en el repositorio. Retírenlo: el FO-IV-159 va solo en Moodle.
- **Trabajo de los dos.** Todos los commits son de Camilo. Sergio debe tener su propio acceso y sus commits, para que el aporte de cada uno quede visible.
- **Overview & insights.** Sección en inglés, mínimo seis oraciones.
