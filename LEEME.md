# Panel de Satisfacción · Hogar — Cardinal Assistance

## Qué incluye esta carpeta
- `index.html` → el panel en sí. Es lo único que abre el cliente.
- `data.json` → los datos que alimentan el panel (se regenera cada mes).
- `build_data.py` → script que convierte el Excel mensual (`BBDD_Hogar.xlsx`) en `data.json`.
- `img/logo.png` → logo de Cardinal Assistance.

No usa Google, ni Looker Studio, ni librerías externas (Chart.js, etc.): todos los gráficos
se dibujan con JavaScript nativo, así que funciona aunque la red de la empresa bloquee CDNs.

## Cómo publicarlo (una sola vez)
1. Crear un repositorio nuevo en GitHub (por ejemplo `Encuestas-de-Calidad-Hogar`), en la
   misma cuenta/org que usaste para Ford y Segurcoop (`ProyectoCalidad`).
2. Subir el contenido de esta carpeta completa (`index.html`, `data.json`, `build_data.py`,
   `img/logo.png`) a la raíz del repositorio.
3. En el repositorio: **Settings → Pages → Branch: main / (root) → Save**.
4. GitHub te da un link tipo `https://proyectocalidad.github.io/Encuestas-de-Calidad-Hogar/`.
   Ese es el link que le compartís al cliente — no necesita iniciar sesión en nada.

## Cómo actualizarlo cada mes
Necesitás reemplazar `data.json` con los datos nuevos. Dos formas:

**Opción A — pedírmelo acá en el chat (más simple):**
Subí el Excel actualizado (`BBDD_Hogar.xlsx`) en esta conversación y pedime que regenere
el panel de Hogar. Te devuelvo el `data.json` nuevo listo para subir a GitHub.

**Opción B — vos misma, con Python instalado:**
```
pip install openpyxl
python build_data.py BBDD_Hogar.xlsx
```
Esto genera un `data.json` nuevo en la misma carpeta. Subilo a GitHub (reemplazando el
archivo existente) y listo — no hace falta tocar `index.html`.

## Estructura esperada del Excel
El script lee la hoja **"Histórico"** y espera estas columnas en este orden:

| Columna | Contenido |
|---|---|
| A | Mes |
| E | Provincia |
| F | Servicio |
| P | Prestador |
| X | Gestión Telefónica (nivel de contacto) |
| Y | Estado de la encuesta |
| Z | Calificación de la atención telefónica (1-5) |
| AA | Calificación del trabajo realizado (1-5) |
| AB | Recomendación (Recomienda / No Recomienda / No Opina) |
| AC | Comentario del cliente |

Si el Excel cambia de estructura (columnas movidas, hoja renombrada), avisame y ajusto
el script.

## Lógica de cálculo (por si necesitás explicarla)
- **Promedios de Atención / Trabajo Realizado**: solo se consideran encuestas con
  Estado de encuesta = "Encuesta Realizada" o "Parcial".
- **NPS**: % Promotor − % Detractor, sobre encuestas Realizada/Parcial con recomendación
  no vacía. "Recomienda" = Promotor, "No Recomienda" = Detractor, "No Opina" = Pasivo.
- **Comentarios**: se muestran los comentarios (columna AC) de casos Detractores, con
  el nombre del prestador (columna P) asociado.
- **Nivel de Contacto / Nivel de Respuesta**: se calculan sobre la totalidad de los
  casos del período (no solo las encuestas válidas).

## Filtros
El panel tiene 3 segmentadores (Mes, Provincia, Servicio) que recalculan todo en
vivo: KPIs, los 7 gráficos y los comentarios. No hace falta tocar nada del código
para que funcionen con datos nuevos.
