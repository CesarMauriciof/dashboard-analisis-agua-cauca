"""Genera los tres notebooks del proyecto con nbformat.

Uso:
    python scripts/crear_notebooks.py
    jupyter nbconvert --to notebook --execute --inplace notebooks/01_limpieza.ipynb
    jupyter nbconvert --to notebook --execute --inplace notebooks/02_analisis.ipynb
    jupyter nbconvert --to notebook --execute --inplace notebooks/03_modelo.ipynb
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

BASE = Path(__file__).resolve().parents[1]
NOTEBOOKS = BASE / "notebooks"
NOTEBOOKS.mkdir(parents=True, exist_ok=True)

SETUP = """import os
import sys
from pathlib import Path

BASE = Path.cwd()
if BASE.name == "notebooks":
    BASE = BASE.parent
    os.chdir(BASE)
sys.path.insert(0, str(BASE))

import pandas as pd

pd.set_option("display.max_columns", 30)
pd.set_option("display.width", 170)
print("Directorio de trabajo:", Path.cwd())"""


def md(texto: str):
    return nbf.v4.new_markdown_cell(texto)


def code(texto: str):
    return nbf.v4.new_code_cell(texto)


def guardar(nombre: str, celdas: list) -> None:
    nb = nbf.v4.new_notebook(cells=celdas)
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python"}
    ruta = NOTEBOOKS / nombre
    nbf.write(nb, ruta)
    print(f"Notebook creado: {ruta}")


# ---------------------------------------------------------------------------
# 01. Limpieza
# ---------------------------------------------------------------------------
limpieza = [
    md(
        """# 01 · Limpieza y auditoría de la base IRCA (SIVICAP)

**Proyecto:** Calidad del agua para consumo humano en el Cauca, 2007–2025.
**Fuente:** SIVICAP – Ministerio de Salud y Protección Social / INS, conjunto `nxt2-39c3` de datos.gov.co.
**Consulta:** 25/11/2026.

Este notebook documenta la descarga, la normalización, la auditoría y la exportación de las tablas limpias. La lógica vive en `src/cleaning.py` para que el proceso sea reproducible desde la terminal con `python -m src.cleaning`."""
    ),
    md(
        """## 1. Preparación del entorno

El notebook se puede ejecutar desde la raíz del proyecto o desde `notebooks/`. El bloque siguiente ajusta el directorio de trabajo y el `sys.path`."""
    ),
    code(SETUP),
    md(
        """## 2. Carga de la base cruda

La descarga original se hizo con la API de datos.gov.co:

```bash
curl -L "https://www.datos.gov.co/resource/nxt2-39c3.json?$limit=50000" \\
  -o data/raw/irca_colombia_raw.json
```

Se usa JSON porque el endpoint CSV de exportación estaba deprecado al momento de la consulta. El archivo tiene 20.212 registros."""
    ),
    code(
        """from src.cleaning import cargar_crudo

crudo = cargar_crudo()
print("Filas:", crudo.shape[0], "| Columnas:", crudo.shape[1])
crudo.head(3)"""
    ),
    md("""### 2.1. Columnas, tipos y nulos de la base original"""),
    code(
        """resumen_crudo = pd.DataFrame(
    {
        "tipo": crudo.dtypes.astype(str),
        "nulos": crudo.isna().sum(),
        "ejemplo": [
            crudo[c].dropna().iloc[0] if crudo[c].notna().any() else None
            for c in crudo.columns
        ],
    }
)
resumen_crudo"""
    ),
    md(
        """## 3. Limpieza

Decisiones principales:

- `ND`, `N/D`, `Sin dato` y cadenas vacías se convierten en nulos. **No se imputan** valores rurales.
- Las variantes `Bajo riesgo` y `Alto riesgo` se unifican con las categorías oficiales.
- Los códigos DANE se conservan como texto para no perder ceros a la izquierda.
- La fila `#TODOS` se separa de la base municipal para evitar doble conteo.
- Se valida la categoría reportada contra la calculada con los umbrales oficiales (5, 14, 35 y 80)."""
    ),
    code(
        """from src.cleaning import limpiar

limpio = limpiar(crudo)
print("Filas:", limpio.shape[0], "| Columnas:", limpio.shape[1])
limpio.head(3)"""
    ),
    md("""## 4. Auditoría de calidad"""),
    code(
        """from src.cleaning import auditar

auditoria = auditar(limpio, crudo)
auditoria"""
    ),
    md(
        """## 5. Base municipal del Cauca

La base municipal excluye la fila agregada `#TODOS`. La serie departamental se conserva aparte."""
    ),
    code(
        """cauca = limpio[(limpio["departamento"] == "Cauca") & (~limpio["es_agregado"])].copy()
cauca_dep = limpio[(limpio["departamento"] == "Cauca") & (limpio["es_agregado"])].copy()

print("Cauca municipal:", cauca.shape)
print("Municipios:", cauca["municipio"].nunique())
print("Años:", int(cauca["anio"].min()), "-", int(cauca["anio"].max()))
print("Cauca #TODOS:", cauca_dep.shape)
cauca.head(3)"""
    ),
    md("""### 5.1. Completitud de las variables principales"""),
    code(
        """faltantes = pd.DataFrame(
    {
        "nulos": cauca[["irca", "irca_urbano", "irca_rural"]].isna().sum(),
        "porcentaje": (
            cauca[["irca", "irca_urbano", "irca_rural"]].isna().mean() * 100
        ).round(1),
    }
)
faltantes"""
    ),
    md(
        """La variable rural es la más incompleta: 489 de 736 registros (66,4%) no tienen IRCA rural. Por eso el análisis de brecha se limita a los casos completos y se declara el sesgo."""
    ),
    md("""### 5.2. Cobertura municipal por año"""),
    code(
        """cobertura = (
    cauca.groupby("anio")
    .agg(municipios=("municipio", "nunique"), con_rural=("irca_rural", "count"))
    .reset_index()
)
cobertura"""
    ),
    md("""### 5.3. Validación de categorías"""),
    code(
        """print("Registros con categoría inconsistente:", int((~limpio["coincide_categoria"]).sum()))
print("\\nDistribución de categorías en el Cauca:")
print(cauca["nivel_riesgo"].value_counts(dropna=False).to_string())"""
    ),
    md(
        """## 6. Exportación

Se ejecuta el flujo oficial para guardar todas las tablas limpias, el diccionario y la auditoría. Los archivos quedan en `data/clean/` y `reports/tablas/`."""
    ),
    code(
        """from src.cleaning import main

main()"""
    ),
    md(
        """## 7. Archivos generados

| Archivo | Contenido |
|---|---|
| `data/clean/irca_colombia_clean.csv` | Base nacional limpia (20.212 registros) |
| `data/clean/irca_cauca_municipal.csv` | Base municipal del Cauca (736 registros, 42 municipios) |
| `data/clean/irca_cauca_departamento.csv` | Serie agregada `#TODOS` del Cauca (19 años) |
| `data/clean/irca_nacional_municipal_2025.csv` | Contexto nacional municipal 2025 (1.019 municipios) |
| `data/clean/irca_nacional_departamental_2025.csv` | Contexto nacional departamental 2025 (33 departamentos) |
| `data/clean/diccionario_datos.csv` | Diccionario de variables |
| `reports/tablas/calidad_datos.csv` | Auditoría de calidad |

**Limitación central:** Popayán solo tiene datos 2008–2019; en 2025 faltan Balboa, Florencia y López de Micay. Los promedios y rankings no representan a los 42 municipios en todos los años."""
    ),
]

# ---------------------------------------------------------------------------
# 02. Análisis
# ---------------------------------------------------------------------------
analisis = [
    md(
        """# 02 · Análisis descriptivo y contexto nacional

**Objetivo:** describir la evolución del IRCA en el Cauca, identificar los municipios con mayor riesgo, medir la brecha urbano-rural y comparar al departamento con el resto del país en 2025.

La lógica vive en `src/analysis.py`; este notebook la ejecuta paso a paso y muestra las tablas y figuras."""
    ),
    code(SETUP),
    md("""## 1. Carga de las tablas limpias"""),
    code(
        """from src.analysis import cargar

cauca, dep, nac_mun, nac_dep = cargar()
print("Cauca municipal:", cauca.shape)
print("Cauca departamento:", dep.shape)
print("Nacional municipal 2025:", nac_mun.shape)
print("Nacional departamental 2025:", nac_dep.shape)"""
    ),
    md("""## 2. Evolución departamental

El IRCA departamental pasó de 30,7 en 2007 a 3,3 en 2024 y subió a 7,3 en 2025. La serie urbana y rural permite ver que la rural es más volátil y tiene más años sin dato."""),
    code(
        """from src.analysis import resumen_anual

resumen = resumen_anual(cauca, dep)
resumen.tail(5)[
    [
        "anio",
        "municipios_con_dato",
        "irca_departamental",
        "nivel_riesgo_departamental",
        "irca_promedio",
        "irca_mediana",
        "pct_riesgo_medio_alto",
        "pct_rural_sin_dato",
    ]
]"""
    ),
    code(
        """dep[dep["anio"].isin([2007, 2010, 2015, 2020, 2023, 2024, 2025])][
    ["anio", "irca", "nivel_riesgo", "irca_urbano", "irca_rural"]
]"""
    ),
    code(
        """from IPython.display import Image, display
from src.analysis import fig_evolucion, fig_categorias

fig_evolucion(dep)
fig_categorias(resumen)
display(Image(filename="figures/fig_01_evolucion_cauca.png", width=900))
display(Image(filename="figures/fig_02_categorias_riesgo.png", width=900))"""
    ),
    md("""## 3. Ranking municipal 2025

En 2025 hay 38 municipios con dato: 18 sin riesgo, 16 en riesgo bajo, 2 en riesgo medio y 2 en riesgo alto. Cuatro municipios concentran el riesgo medio/alto."""),
    code(
        """from src.analysis import persistencia, ranking_2025, fig_ranking

persist = persistencia(cauca)
ranking = ranking_2025(cauca, nac_mun, persist)
ranking.head(10)[
    [
        "municipio",
        "irca",
        "nivel_riesgo",
        "irca_urbano",
        "irca_rural",
        "brecha_rural_urbano",
        "puesto_departamental",
        "puesto_nacional",
        "percentil_nacional",
    ]
]"""
    ),
    code(
        """print("Distribución 2025:")
print(ranking["nivel_riesgo"].value_counts().to_string())
print("\\nMunicipios sin dato en 2025:")
print(sorted(set(cauca["municipio"]) - set(ranking["municipio"])))"""
    ),
    code(
        """fig_ranking(ranking)
display(Image(filename="figures/fig_03_ranking_2025.png", width=720))"""
    ),
    md("""## 4. Brecha urbano-rural

La brecha se calcula como `IRCA rural - IRCA urbano`. Solo se usan los 242 registros con ambos datos; no se imputan los faltantes. Un valor positivo indica peor situación rural."""),
    code(
        """from src.analysis import tabla_brecha, fig_brecha

brecha_municipio, brecha_anio = tabla_brecha(cauca)
ambos = cauca.dropna(subset=["irca_urbano", "irca_rural"])

print("Observaciones con ambos datos:", len(ambos))
print("Brecha promedio:", round(ambos["brecha_rural_urbano"].mean(), 2))
print("Brecha mediana:", round(ambos["brecha_rural_urbano"].median(), 2))
print("Porcentaje con brecha positiva:", round((ambos["brecha_rural_urbano"] > 0).mean() * 100, 1))
print("Registros sin IRCA rural:", int(cauca["irca_rural"].isna().sum()), "de", len(cauca))"""
    ),
    code(
        """brecha_municipio[brecha_municipio["evidencia_suficiente"]].head(10)[
    [
        "municipio",
        "anios_con_datos",
        "primer_anio",
        "ultimo_anio",
        "irca_urbano_promedio",
        "irca_rural_promedio",
        "brecha_promedio",
    ]
]"""
    ),
    code(
        """fig_brecha(brecha_municipio)
display(Image(filename="figures/fig_04_urbano_rural.png", width=820))"""
    ),
    md("""## 5. Contexto nacional 2025

El Cauca ocupa el puesto 19 de 33 departamentos (1 = menor IRCA). Su IRCA de 7,3 está 0,3 puntos por encima de la mediana departamental (7,0). La mediana municipal nacional es 5,7 y la del Cauca es 6,1 (percentil 51,6)."""),
    code(
        """from src.analysis import contexto_nacional, fig_contexto

contexto, contexto_resumen = contexto_nacional(nac_dep, nac_mun, dep)
contexto_resumen"""
    ),
    code(
        """contexto[
    contexto["departamento"].isin(
        ["Cauca", "Valle del Cauca", "Huila", "Caquetá", "Putumayo", "Nariño"]
    )
][["departamento", "irca", "nivel_riesgo", "puesto", "diferencia_vs_mediana"]]"""
    ),
    code(
        """fig_contexto(contexto, nac_mun)
display(Image(filename="figures/fig_06_contexto_nacional.png", width=1000))"""
    ),
    md("""## 6. Mapa de calor y trayectorias municipales

El mapa de calor muestra los 42 municipios y los 19 años; el gris indica ausencia de dato. Las trayectorias resaltan los cuatro municipios con mayor IRCA en 2025."""),
    code(
        """from src.analysis import fig_evolucion_municipal, fig_heatmap

fig_heatmap(cauca)
fig_evolucion_municipal(cauca, ranking)
display(Image(filename="figures/fig_05_heatmap.png", width=820))
display(Image(filename="figures/fig_08_evolucion_municipal.png", width=900))"""
    ),
    md(
        """## 7. Hallazgos para el informe

1. **Mejora con rebote:** 30,7 (2007) → 3,3 (2024) → 7,3 (2025). El aumento de 2025 es de 4,0 puntos y debe monitorearse; los ceros de 2024 y los saltos abruptos sugieren posibles cambios de reporte.
2. **Riesgo concentrado:** 4 de 38 municipios en riesgo medio/alto (10,5%): Timbiquí 37,0, Caldono 36,6, Guapi 32,0 y Villa Rica 19,1. Timbiquí y Caldono son los casos más críticos.
3. **Brecha rural subreportada:** 242 observaciones con ambos datos, brecha promedio 12,2 puntos y mediana 1,9; 66,4% de los registros municipales no tienen IRCA rural. En 2025 solo 8 de 38 municipios tienen dato rural.
4. **Contexto nacional:** Cauca 19/33, cerca de la mediana departamental (7,0) y por encima de la mediana municipal nacional (5,7). Es mejor que Nariño (22,5) y Putumayo (17,0), pero peor que Valle (4,4), Huila (4,1) y Caquetá (6,7).
5. **Datos faltantes:** Popayán solo tiene 2008–2019; en 2025 faltan Balboa, Florencia y López de Micay. Los promedios no representan a los 42 municipios en todos los años.

> **Advertencia:** el IRCA es un indicador agregado del reporte municipal. No identifica hogares, veredas ni causas. Las cifras deben validarse con la autoridad sanitaria y con datos de campo."""
    ),
]

# ---------------------------------------------------------------------------
# 03. Modelo
# ---------------------------------------------------------------------------
modelo = [
    md(
        """# 03 · Modelo predictivo simple del IRCA municipal

**Objetivo:** pronosticar el IRCA 2026 de cada municipio con datos 2025, usando solo información de años anteriores.

**Decisión:** se compara un pronóstico ingenuo, la media histórica, una regresión lineal simple (IRCA del año anterior + media móvil de 3 años), una regresión completa y un Random Forest. El modelo final es la regresión simple por parsimonia y estabilidad: su MAE es prácticamente igual al de la regresión completa y produce escenarios menos agresivos.

**Corte temporal:** entrenamiento ≤ 2021 (463 observaciones), prueba 2022–2025 (127). No se usa información del futuro para entrenar."""
    ),
    code(SETUP),
    md(
        """## 1. Panel anual completo

Se construye una grilla 2007–2026 por municipio. Así los rezagos son de año calendario y no de fila: si un municipio no reportó un año, el rezago queda nulo en lugar de tomar un dato antiguo como si fuera del año anterior."""
    ),
    code(
        """from src.model import FEATURES_COMPLETO, FEATURES_SIMPLE, preparar_panel

cauca = pd.read_csv("data/clean/irca_cauca_municipal.csv", encoding="utf-8-sig")
cauca["anio"] = cauca["anio"].astype(int)
panel = preparar_panel(cauca)

print("Panel:", panel.shape)
print("Variables simples:", FEATURES_SIMPLE)
print("Variables completas:", FEATURES_COMPLETO)
panel[panel["municipio"] == "Timbiquí"][
    ["anio", "irca", "irca_lag1", "irca_lag2", "irca_roll3", "tendencia_3"]
].tail(10)"""
    ),
    md("""## 2. Conjunto de entrenamiento y prueba"""),
    code(
        """datos = panel.dropna(subset=["irca"] + FEATURES_COMPLETO).copy()
train = datos[datos["anio"] <= 2021]
test = datos[datos["anio"] >= 2022]

print("Observaciones completas:", len(datos))
print("Entrenamiento:", len(train), "| años:", int(train["anio"].min()), "-", int(train["anio"].max()))
print("Prueba:", len(test), "| años:", int(test["anio"].min()), "-", int(test["anio"].max()))"""
    ),
    md("""## 3. Modelo simple y métricas de prueba"""),
    code(
        """from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from src.model import calcular_metricas

modelo_simple = Pipeline(
    [("escalador", StandardScaler()), ("modelo", LinearRegression())]
)
modelo_simple.fit(train[FEATURES_SIMPLE], train["irca"])
pred_simple = modelo_simple.predict(test[FEATURES_SIMPLE])

print("Regresión lineal simple:")
print(calcular_metricas(test["irca"], pred_simple))"""
    ),
    md("""## 4. Comparación con los modelos alternativos"""),
    code(
        """from sklearn.ensemble import RandomForestRegressor

modelo_completo = Pipeline(
    [("escalador", StandardScaler()), ("modelo", LinearRegression())]
)
modelo_completo.fit(train[FEATURES_COMPLETO], train["irca"])
pred_completo = modelo_completo.predict(test[FEATURES_COMPLETO])

modelo_rf = RandomForestRegressor(
    n_estimators=500,
    max_depth=4,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1,
)
modelo_rf.fit(train[FEATURES_COMPLETO], train["irca"])
pred_rf = modelo_rf.predict(test[FEATURES_COMPLETO])

comparacion = pd.DataFrame(
    [
        {"modelo": "Naive (último valor)", **calcular_metricas(test["irca"], test["irca_lag1"])},
        {"modelo": "Media histórica", **calcular_metricas(test["irca"], test["irca_mean_prev"])},
        {"modelo": "Regresión simple", **calcular_metricas(test["irca"], pred_simple)},
        {"modelo": "Regresión completa", **calcular_metricas(test["irca"], pred_completo)},
        {"modelo": "Random Forest", **calcular_metricas(test["irca"], pred_rf)},
    ]
)
comparacion"""
    ),
    md(
        """**Lectura:** el MAE de la regresión simple (5,26) mejora en 0,37 puntos al naive (5,63). La regresión completa baja apenas 0,01 puntos más, pero usa 8 variables. El R² de prueba es negativo o casi nulo: el modelo no explica bien la varianza. El R² de entrenamiento es 0,73, lo que evidencia sobreajuste y cambios estructurales entre periodos."""
    ),
    md("""## 5. Coeficientes del modelo final

El modelo de prueba se entrena solo con ≤2021. Para el pronóstico 2026 se reentrena con todos los datos completos (práctica estándar de pronóstico). Los coeficientes que se reportan son los del modelo reentrenado."""
    ),
    code(
        """modelo_final = Pipeline(
    [("escalador", StandardScaler()), ("modelo", LinearRegression())]
)
modelo_final.fit(datos[FEATURES_SIMPLE], datos["irca"])

coeficientes = pd.DataFrame(
    {
        "variable": FEATURES_SIMPLE,
        "coeficiente_estandarizado": modelo_final.named_steps["modelo"].coef_.round(4),
    }
)
coeficientes"""
    ),
    md("""## 6. Pronóstico 2026

El escenario usa el IRCA 2025 y la media móvil 2023–2025. La banda de error usa el MAE de prueba (±5,26 puntos); **no es un intervalo de confianza**."""),
    code(
        """from src.model import categoria, construir_futuro

futuro = construir_futuro(cauca)
futuro["irca_2026_predicho"] = modelo_final.predict(futuro[FEATURES_SIMPLE]).clip(0, 100)
futuro["categoria_predicha"] = futuro["irca_2026_predicho"].map(categoria)
futuro["intervalo_inferior"] = (futuro["irca_2026_predicho"] - 5.26).clip(0, 100)
futuro["intervalo_superior"] = (futuro["irca_2026_predicho"] + 5.26).clip(0, 100)

futuro[
    [
        "municipio",
        "irca_lag1",
        "irca_roll3",
        "irca_2026_predicho",
        "categoria_predicha",
        "intervalo_inferior",
        "intervalo_superior",
    ]
].sort_values("irca_2026_predicho", ascending=False).head(10)"""
    ),
    code(
        """print("Categorías pronosticadas 2026:")
print(futuro["categoria_predicha"].value_counts().to_string())"""
    ),
    md("""## 7. Figura oficial del modelo

Se ejecuta el flujo oficial para regenerar la figura y las tablas del modelo."""),
    code(
        """from IPython.display import Image, display
from src.model import main

main()
display(Image(filename="figures/fig_07_modelo.png", width=1000))"""
    ),
    md(
        """## 8. Conclusiones del modelo

- **MAE de prueba:** 5,26 puntos; naive: 5,63. La mejora es modesta.
- **R² de prueba:** -0,06; R² de entrenamiento: 0,73. El modelo no generaliza bien y suaviza los extremos.
- **Pronóstico 2026:** 4 municipios en riesgo medio (Timbiquí 28,7; Caldono 26,2; Guapi 25,8; Villa Rica 14,4), 14 en riesgo bajo y 20 sin riesgo. No se pronostica riesgo alto, pero Timbiquí y Caldono quedan cerca del umbral de 35.
- **Uso responsable:** es una herramienta de tamizaje y exploración, no una predicción oficial ni una relación causal. La priorización debe validarse con datos de campo, infraestructura, clima e inversión.

> **Nota metodológica:** la banda ±MAE no es un intervalo de confianza. Para intervalos formales se necesitaría un bootstrap o un modelo probabilístico, que excede el alcance de este trabajo."""
    ),
]

guardar("01_limpieza.ipynb", limpieza)
guardar("02_analisis.ipynb", analisis)
guardar("03_modelo.ipynb", modelo)
