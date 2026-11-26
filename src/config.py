"""Configuración central del proyecto IRCA Cauca.

Rutas, constantes, umbrales oficiales y catálogos de municipios.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_CLEAN = BASE_DIR / "data" / "clean"
FIGURES = BASE_DIR / "figures"
REPORTS = BASE_DIR / "reports"
TABLES = REPORTS / "tablas"
NOTEBOOKS = BASE_DIR / "notebooks"
VIDEO = BASE_DIR / "video"
DOCS = BASE_DIR / "docs"

for _p in (DATA_RAW, DATA_CLEAN, FIGURES, REPORTS, TABLES, NOTEBOOKS, VIDEO, DOCS):
    _p.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Fuente de datos
# ---------------------------------------------------------------------------
DATASET_ID = "nxt2-39c3"
DATASET_NAME = "Calidad del Agua para Consumo Humano en Colombia (SIVICAP)"
DATASET_URL = f"https://www.datos.gov.co/d/{DATASET_ID}"
DATASET_API = f"https://www.datos.gov.co/resource/{DATASET_ID}.json?$limit=50000"
DATASET_ENTITY = "Ministerio de Salud y Protección Social / Instituto Nacional de Salud"
DATASET_UPDATED = "2026-11-04"
DATASET_CONSULTED = "2026-11-25"

RAW_JSON = DATA_RAW / "irca_colombia_raw.json"

# ---------------------------------------------------------------------------
# Catálogos
# ---------------------------------------------------------------------------
DEPARTAMENTO_CAUCA = "Cauca"

# Los 42 municipios del Cauca con su código DANE.
CAUCA_MUNICIPIOS = {
    "19001": "Popayán",
    "19022": "Almaguer",
    "19050": "Argelia",
    "19075": "Balboa",
    "19100": "Bolívar",
    "19110": "Buenos Aires",
    "19130": "Cajibío",
    "19137": "Caldono",
    "19142": "Caloto",
    "19212": "Corinto",
    "19256": "El Tambo",
    "19290": "Florencia",
    "19300": "Guachené",
    "19318": "Guapi",
    "19355": "Inzá",
    "19364": "Jambaló",
    "19392": "La Sierra",
    "19397": "La Vega",
    "19418": "López de Micay",
    "19450": "Mercaderes",
    "19455": "Miranda",
    "19473": "Morales",
    "19513": "Padilla",
    "19517": "Páez",
    "19532": "Patía",
    "19533": "Piamonte",
    "19548": "Piendamó - Tunía",
    "19573": "Puerto Tejada",
    "19585": "Puracé",
    "19622": "Rosas",
    "19693": "San Sebastián",
    "19698": "Santander de Quilichao",
    "19701": "Santa Rosa",
    "19743": "Silvia",
    "19760": "Sotará Paispamba",
    "19780": "Suárez",
    "19785": "Sucre",
    "19807": "Timbío",
    "19809": "Timbiquí",
    "19821": "Toribío",
    "19824": "Totoró",
    "19845": "Villa Rica",
}

DEPARTAMENTOS_VECINOS = [
    "Valle del Cauca",
    "Huila",
    "Caquetá",
    "Putumayo",
    "Nariño",
]

# ---------------------------------------------------------------------------
# Riesgo
# ---------------------------------------------------------------------------
RISK_ORDER = [
    "Sin riesgo",
    "Riesgo bajo",
    "Riesgo medio",
    "Riesgo alto",
    "Inviable sanitariamente",
]

RISK_COLORS = {
    "Sin riesgo": "#2E7D32",
    "Riesgo bajo": "#9CCC65",
    "Riesgo medio": "#FFC107",
    "Riesgo alto": "#EF6C00",
    "Inviable sanitariamente": "#C62828",
}

# Bandas oficiales (Decreto 1575 de 2007 / Resolución 2115 de 2007)
RISK_BANDS = [
    (0, 5, "Sin riesgo"),
    (5.1, 14, "Riesgo bajo"),
    (14.1, 35, "Riesgo medio"),
    (35.1, 80, "Riesgo alto"),
    (80.1, 100, "Inviable sanitariamente"),
]

# Colores generales
COLOR_CAUCA = "#1565C0"
COLOR_NEUTRO = "#90A4AE"
COLOR_URBANO = "#1565C0"
COLOR_RURAL = "#EF6C00"

# Años
ANIO_MIN = 2007
ANIO_MAX = 2025
ANIO_ULTIMO = 2025
ANIO_CONTEXTO = 2025
ANIO_ENTRENAMIENTO = 2021  # train <= 2021, test >= 2022

# ---------------------------------------------------------------------------
# Archivos limpios
# ---------------------------------------------------------------------------
CLEAN_CAUCA_MUNICIPAL = DATA_CLEAN / "irca_cauca_municipal.csv"
CLEAN_CAUCA_DEPARTAMENTO = DATA_CLEAN / "irca_cauca_departamento.csv"
CLEAN_NACIONAL_MUNICIPAL_2025 = DATA_CLEAN / "irca_nacional_municipal_2025.csv"
CLEAN_NACIONAL_DEPARTAMENTAL_2025 = DATA_CLEAN / "irca_nacional_departamental_2025.csv"
CLEAN_COLOMBIA = DATA_CLEAN / "irca_colombia_clean.csv"
DICCIONARIO = DATA_CLEAN / "diccionario_datos.csv"

# Tablas de resultados
TABLA_RESUMEN_ANUAL = TABLES / "resumen_anual_cauca.csv"
TABLA_RANKING_2025 = TABLES / "ranking_2025.csv"
TABLA_BRECHA = TABLES / "brecha_urbano_rural.csv"
TABLA_BRECHA_ANIO = TABLES / "brecha_urbano_rural_por_anio.csv"
TABLA_CONTEXTO = TABLES / "contexto_nacional_2025.csv"
TABLA_CONTEXTO_RESUMEN = TABLES / "contexto_nacional_resumen.csv"
TABLA_PERSISTENCIA = TABLES / "persistencia_riesgo.csv"
TABLA_CALIDAD = TABLES / "calidad_datos.csv"
TABLA_METRICAS = TABLES / "metricas_modelo.csv"
TABLA_PREDICCIONES = TABLES / "predicciones_2026.csv"

# Figuras
FIG_EVOLUCION = FIGURES / "fig_01_evolucion_cauca.png"
FIG_CATEGORIAS = FIGURES / "fig_02_categorias_riesgo.png"
FIG_RANKING = FIGURES / "fig_03_ranking_2025.png"
FIG_BRECHA = FIGURES / "fig_04_urbano_rural.png"
FIG_HEATMAP = FIGURES / "fig_05_heatmap.png"
FIG_CONTEXTO = FIGURES / "fig_06_contexto_nacional.png"
FIG_MODELO = FIGURES / "fig_07_modelo.png"
FIG_EVOLUCION_MUNICIPAL = FIGURES / "fig_08_evolucion_municipal.png"
