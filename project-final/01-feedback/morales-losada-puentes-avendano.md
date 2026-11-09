# Retroalimentación · Revisión del 5 de noviembre

**Proyecto:** Nani Accesorios
**Estudiantes:** Danna Michelle Morales Losada y Alison Fernanda Puentes Avendaño
**Revisión:** jueves 5 de noviembre de 2026 · Docente Jesús Ariel González Bonilla
**Avance revisado:** fork `Dannamo34`, `15-week/proyecto-aula/` (commits «proyecto aula» y «model de proyecto»)

La base es buena: la ficha está completa, el modelo estrella está bien pensado, las claves de las cinco tablas cruzan sin errores y el generador se puede volver a ejecutar. No hay que empezar de nuevo.

**La prioridad para la entrega del jueves 12 de noviembre es tener el tablero listo en Power BI.** El tablero es lo que refleja el trabajo real. Hoy el repositorio tiene datos y documentación, pero todavía no hay un `.pbix`.

## 1. El tablero: lo más importante

Abran Power BI desde ya. Una propuesta de tres páginas, cada una con una sola pregunta:

| Página | Pregunta que responde | Qué debe tener |
|---|---|---|
| Resumen | ¿Cómo le fue al negocio en 2025? | Margen bruto % arriba a la izquierda, ventas netas, costo de ventas, unidades y la tendencia por mes |
| Productos | ¿Qué categorías y productos dejan más margen? | Ventas y margen por categoría, con drill-down de categoría a producto |
| Canales | ¿Qué canal conviene impulsar? | Ventas y margen por canal, y el efecto de los descuentos |

En el tablero se revisará:

- Modelo estrella con relaciones de uno a varios desde las dimensiones hacia `fact_ventas`.
- Al menos 5 medidas DAX, incluido el margen bruto %, cada una con su cifra de control.
- Al menos 2 segmentadores (por ejemplo mes y canal), una jerarquía con drill-down y las interacciones revisadas.
- Prueba del clic: 3 selecciones con sus cifras, comparadas contra las de control.
- Capturas del tablero y del modelo en la carpeta del proyecto, junto con el `.pbix`.

## 2. Los datos deben dar algo que mostrar

Este ajuste se hace antes de armar el tablero. Con los datos actuales el margen casi no cambia por canal (Instagram 50,2 %, WhatsApp 50,0 %, Venta directa 50,3 %) y las ventas de los meses no muestran temporadas claras. Un tablero así no tiene hallazgo ni recomendación. Ajusten `generar_datos.py`:

- **Temporadas:** más ventas en Día de la Madre, Amor y Amistad y Navidad.
- **Productos estrella:** unos pocos que vendan mucho más que el resto.
- **Un canal con trampa:** por ejemplo, uno que venda mucho pero deje menos margen por los descuentos.
- **Catálogo:** hoy Collares tiene 1 solo producto frente a 11 de Anillos; repártanlo mejor.
- **Ventas con varias líneas:** cada `id_venta` tiene hoy un solo producto, aunque el grano dice que una venta puede tener varios.

## 3. Pregunta y problema

La pregunta actual describe, pero no lleva a una decisión. Ejemplo: «¿Qué categorías y canales dejaron mayor margen en 2025, y dónde conviene concentrar los descuentos en las próximas temporadas?». El problema debe decir qué decisión toma mal hoy la empresa, por ejemplo a qué productos o canales les aplica descuentos sin saber si dejan ganancia.

## 4. Power Query

Hoy hay 1 fila duplicada, 1 fecha con otro formato y 1 producto con la categoría mal escrita. Siembren varios casos de cada problema para que la limpieza se note. Documenten cada paso aplicado con su motivo y dejen capturas de antes y después.

## 5. Para completar la entrega

- Diccionario de datos: agregar la columna de ejemplo y documentar `fecha_venta`, que está en el CSV y no en el diccionario.
- `nombre_mes` en español; hoy sale en inglés («January»).
- Explicar en el README cómo se generaron los datos y qué reglas se usaron.
- Recomendación concreta para la empresa: qué hacer, quién y cuándo.
- Sección «Overview & insights» en inglés, mínimo seis oraciones.
- FO-IV-159 solo en Moodle, nunca en GitHub.

## 6. Trabajo de las dos integrantes

Todos los commits del proyecto son de `Dannamo34`. Alison debe trabajar en el repositorio con sus propios commits, de modo que el aporte de cada una quede visible.
