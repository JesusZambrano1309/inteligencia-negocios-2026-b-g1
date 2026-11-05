# Retroalimentación · Revisión del 5 de noviembre

**Proyecto:** Andes Store
**Estudiantes:** Juan José Horta Vanegas, Andrés Felipe Gómez Anacona, Laura Sofía Vallejo Oviedo y María Paula Barrios Fajardo
**Revisión:** jueves 5 de noviembre de 2026 · Docente Jesús Ariel González Bonilla
**Avance revisado:** fork `Juan-Horta27`, `15-week/proyecto-aula/` (`Datos.pbix`, informe técnico y README, commit `1b5f937`)

El proyecto va muy adelantado. El tablero existe, el modelo funciona y las cifras de control cuadran contra un cálculo independiente desde los CSV: $87.729,89 en ventas, 2.523 transacciones, ticket de $34,77, 8.834 unidades y 326 clientes. Las pruebas del clic también cuadran; en marzo la cifra exacta es $8.837,72. Cada integrante tiene su commit en el proyecto.

**La prioridad para la entrega del jueves 12 de noviembre es que el tablero le sume valor a la empresa.** No se trata de colocar gráficas por colocarlas: cada visual debe ayudar a tomar una decisión.

## 1. Un tablero que le sirva a la empresa

Hoy el tablero muestra cuánto se vendió, pero no dice qué hacer con esa información. Antes de agregar o mover visuales, definan quién lo usa y qué decide con él. Para cada visual respondan: **¿qué decisión apoya?** Si no apoya ninguna, se quita o se reemplaza.

| Quién decide | Qué decide | Qué debería ver en el tablero |
|---|---|---|
| Compras e inventario | Cuánto pedir de cada categoría y en qué mes | Variación mensual por categoría y comparación del stock con las unidades vendidas |
| Mercadeo | Qué promocionar y en qué temporada | Categorías y productos que suben o caen en cada mes |
| Finanzas | Qué medios de pago impulsar y cuánto dinero falta por cerrar | Participación por método de pago y valor de las ventas pendientes |

Dos ideas que hoy los datos permiten y el tablero no aprovecha:

- **Dinero sin cerrar.** Las ventas pendientes y canceladas suman $15.373,30, frente a $87.729,89 completadas. Es información valiosa para la empresa y hoy no aparece.
- **Stock.** La columna `Stock` de `productos` no se usa. Con ella se puede mostrar qué productos corren riesgo de agotarse o tienen exceso.

Los títulos de los gráficos deben decir el hallazgo, no el nombre de la medida. Por ejemplo, «Carnicería explica la mayor parte del repunte de diciembre» en lugar de «Ventas por categoría». El tablero debe terminar en una recomendación concreta: qué hacer, quién y cuándo.

## 2. Responder la pregunta de negocio

- **KPI principal.** La pregunta habla de las variaciones mensuales, y la Fase 0 pidió la variación mensual de las ventas. Ventas Totales sigue como KPI principal y no existe esa medida. Créenla y muéstrenla por categoría y por método de pago.
- **Enero.** Tiene solo 7 ventas completadas ($256), todas del 31 de enero. Con ese mes, febrero daría una variación de +2.779 %. Exclúyanlo del análisis de variación y declárenlo en el informe.
- **Hallazgo disponible.** De noviembre a diciembre las ventas suben 27,3 %, y Carnicería aporta cerca de seis de cada diez pesos de ese aumento. Es un buen punto de partida para la historia del tablero.

## 3. Pendientes de la Fase 0

1. **Citar la fuente: no negociable.** El README solo dice «Kaggle». Escriban el nombre del dataset, el autor y el enlace, en formato APA. Sin la fuente citada, el proyecto no se acepta.
2. **Datos personales.** `clientes.csv` y el `.pbix` siguen con nombre, apellido y correo en un repositorio público. Quiten esas columnas de los dos archivos.
3. **Moneda y contexto.** Declaren la moneda y ambienten la empresa en el contexto de los datos, que son de Argentina.
4. **El plus de ser cuatro.** La segmentación RFM es una buena propuesta, pero aún no está construida. Debe aparecer en el tablero y aportar a una decisión: a qué clientes retener, por ejemplo, no ser una página más.

## 4. Ajustes técnicos

- **Regiones.** «Poner en mayúsculas cada palabra» convirtió «NEA» y «NOA» en «Nea» y «Noa», y «Bogota» sigue en la tabla. Corrijan esos valores y decidan qué hacer con el registro de Bogotá.
- **Fechas automáticas.** Siguen las tablas `LocalDateTable`. Desactiven «Fecha y hora automáticas» y marquen `Calendario` como tabla de fechas.
- **Ruta de los archivos.** Las consultas leen de una carpeta local de un computador. Usen un parámetro de ruta para que el `.pbix` abra en otro equipo.
- **Tabla auxiliar.** `Revision_duplicados` queda cargada en el modelo con 0 filas. Desactiven su carga.

## 5. Para completar la entrega

- Capturas de antes y después, del tablero, del modelo y de las tres pruebas del clic, con cifras exactas y no abreviadas.
- Diccionario con ejemplos reales: hoy hay textos como «Producto del catálogo» o «Dato del registro correspondiente».
- Historia del tablero y recomendación en el informe.
- Sección «Overview & insights» en inglés, mínimo seis oraciones.
- FO-IV-159 solo en Moodle, nunca en GitHub.
