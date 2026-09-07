# Panel de Satisfacción · Hogar — Cardinal Assistance

## Qué incluye esta carpeta
- `index.html` → el panel en sí. Es lo único que abre el cliente. Tiene dos módulos
  navegables por pestañas: **KPIs** (tarjetas + 7 gráficos) y **Comentarios**
  (acordeón por mes, con la orden de servicio junto al prestador).
- `actualizar.html` → herramienta para generar el `data.json` nuevo cada mes,
  corre entera en tu navegador, no instala nada.
- `data.json` → los datos que alimentan el panel (se regenera cada mes).
- `build_data.py` → alternativa por Python para generar `data.json` (opcional,
  solo si tenés Python instalado — no hace falta si usás `actualizar.html`).
- `img/logo.png` → logo de Cardinal Assistance.

No usa Google, ni Looker Studio, ni librerías externas (Chart.js, SheetJS, etc.):
todo se procesa con JavaScript nativo, así que funciona aunque la red de la
empresa bloquee CDNs o no te dejen instalar programas.

## Cómo publicarlo (una sola vez)
1. Crear un repositorio nuevo en GitHub (por ejemplo `Encuestas-de-Calidad-Hogar-Cardinal`),
   en la misma cuenta/org que usaste para Ford, Segurcoop y Turismo (`ProyectoCalidad`).
2. Subir el contenido de esta carpeta completa (`index.html`, `actualizar.html`,
   `data.json`, `build_data.py`, `img/logo.png`) a la raíz del repositorio.
3. En el repositorio: **Settings → Pages → Branch: main / (root) → Save**.
4. GitHub te da un link tipo `https://proyectocalidad.github.io/Encuestas-de-Calidad-Hogar-Cardinal/`.
   Ese es el link que le compartís al cliente — no necesita iniciar sesión en nada.

## Cómo actualizarlo cada mes

**Opción A — vos sola, con `actualizar.html` (recomendada, no instala nada):**
1. Abrí tu `BBDD_Hogar.xlsx` de siempre, ya actualizado, parada en la hoja
   **"Histórico"**.
2. `Archivo → Guardar como` → elegí **CSV UTF-8 (delimitado por comas) (*.csv)**.
3. Abrí `actualizar.html` con doble clic (se abre en el navegador).
4. Subí ese `.csv` — la herramienta te muestra un resumen (casos totales,
   meses detectados, encuestas realizadas, comentarios) y te deja descargar
   el `data.json` nuevo.
5. Subí ese `data.json` a GitHub reemplazando el existente (mismo nombre, en
   la raíz del repo) → commit → esperá el check verde en la pestaña Actions →
   abrí el panel con Ctrl+Shift+R.

**Opción B — pedírmelo acá en el chat:**
Subí el Excel actualizado en esta conversación y pedime que regenere el panel
de Hogar. Te devuelvo el `data.json` nuevo listo para subir a GitHub.

**Opción C — vos misma, con Python instalado (si lo tenés disponible):**
```
pip install openpyxl
python build_data.py BBDD_Hogar.xlsx
```

## Estructura esperada del Excel / CSV
La herramienta lee la hoja **"Histórico"** y espera estas columnas en este orden:

| Columna | Contenido |
|---|---|
| A | Mes |
| B | Área |
| C | Cía |
| E | Provincia |
| F | Servicio |
| I | Orden de Servicio |
| P | Prestador |
| X | Gestión Telefónica (nivel de contacto) |
| Y | Estado de la encuesta |
| Z | Calificación de la atención telefónica (1-5) |
| AA | Calificación del trabajo realizado (1-5) |
| AB | Recomendación (Recomienda / No Recomienda / No Opina) |
| AC | Comentario del cliente |

Si el Excel cambia de estructura (columnas movidas, hoja renombrada), avisame y
ajusto tanto `actualizar.html` como `build_data.py`.

### Sobre `actualizar.html` y los formatos de fecha
La herramienta reconoce la columna Mes venga como fecha (`01/08/2026`), como
texto abreviado (`ago-26`, `agosto-26`) o como número de serie de Excel. Si
alguna fila tiene un formato raro que no puede interpretar, te lo avisa en
pantalla antes de descargar — igual procesa el resto del archivo sin problema.
También soporta que el CSV venga separado por coma o por punto y coma
(Excel en español suele usar punto y coma), y decimales con coma.

## Lógica de cálculo (por si necesitás explicarla)
- **Promedios de Atención / Trabajo Realizado**: solo se consideran encuestas con
  Estado de encuesta = "Encuesta Realizada" o "Parcial".
- **NPS**: % Promotor − % Detractor, sobre encuestas Realizada/Parcial con recomendación
  no vacía. "Recomienda" = Promotor, "No Recomienda" = Detractor, "No Opina" = Pasivo.
  La tarjeta muestra solo el %; el desglose Promotor/Pasivo/Detractor está en el
  gráfico de composición (para no repetir la misma info dos veces).
- **Comentarios**: en la pestaña "Comentarios", agrupados en acordeón por mes,
  se muestran los comentarios (columna AC) de casos Detractores, con el prestador
  (columna P) y la orden de servicio (columna I) asociados.
- **Nivel de Contacto / Nivel de Respuesta**: se calculan sobre la totalidad de los
  casos del período (no solo las encuestas válidas).

## Filtros
El panel tiene 3 segmentadores (Mes, Área, Cía) que recalculan todo en vivo:
KPIs, los 7 gráficos y los comentarios, en ambas pestañas. No hace falta tocar
nada del código para que funcionen con datos nuevos.
