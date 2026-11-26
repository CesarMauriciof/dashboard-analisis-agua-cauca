"""Dashboard interactivo del IRCA en el Cauca.

Ejecutar en local:
    streamlit run app.py

Publicar en Streamlit Community Cloud:
    subir el repositorio a GitHub y seleccionar app.py como entrypoint.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

from src.config import (  # noqa: E402
    COLOR_CAUCA,
    COLOR_NEUTRO,
    COLOR_RURAL,
    COLOR_URBANO,
    DEPARTAMENTOS_VECINOS,
    RISK_COLORS,
    RISK_ORDER,
)

# ---------------------------------------------------------------------------
# Configuración de página y estilo
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="IRCA Cauca | Calidad del agua",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.2rem; padding-bottom: 2.5rem; max-width: 1450px; }
    h1, h2, h3 { color: #0D2B45; letter-spacing: -0.02em; }
    h1 { font-size: 2.15rem; margin-bottom: 0.1rem; }
    .subtitulo { color: #4A5C6E; font-size: 1.02rem; margin-bottom: 0.9rem; }
    .hallazgo {
        background: #F8FAFC; border-left: 5px solid #1565C0;
        padding: 12px 16px; border-radius: 8px; margin-bottom: 10px;
        color: #243746; font-size: 0.93rem; line-height: 1.45;
    }
    .hallazgo b { color: #0D2B45; }
    .hallazgo .titulo { font-weight: 700; color: #1565C0; display: block; margin-bottom: 3px; }
    .nota { color: #607080; font-size: 0.82rem; line-height: 1.4; }
    .alerta {
        background: #FFF8E1; border-left: 5px solid #FFB300;
        padding: 12px 16px; border-radius: 8px; color: #4E3B00; font-size: 0.9rem;
    }
    [data-testid="stMetric"] {
        background: #FFFFFF; border: 1px solid #E3EAF1; border-radius: 12px;
        padding: 12px 16px; box-shadow: 0 1px 2px rgba(13, 43, 69, 0.04);
    }
    [data-testid="stMetricLabel"] { color: #5A6B7B; font-size: 0.82rem; }
    [data-testid="stMetricValue"] { color: #0D2B45; font-size: 1.55rem; }
    [data-testid="stSidebar"] { background: #F4F7FA; }
    .footer { color: #6B7C8F; font-size: 0.78rem; line-height: 1.5; }
    </style>
    """,
    unsafe_allow_html=True,
)

FUENTE = (
    "SIVICAP – Ministerio de Salud y Protección Social / Instituto Nacional de Salud. "
    "datos.gov.co, conjunto nxt2-39c3. Actualización: 04/11/2026. Consulta: 25/11/2026."
)


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def num(valor, decimales: int = 1) -> str:
    """Formato numérico colombiano: coma decimal y punto de miles."""
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    texto = f"{float(valor):,.{decimales}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def entero(valor) -> str:
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    return f"{int(valor):,}".replace(",", ".")


def corto(nombre: str, maximo: int = 28) -> str:
    return nombre if len(nombre) <= maximo else nombre[: maximo - 1] + "…"


@st.cache_data(show_spinner=False)
def cargar_datos() -> dict[str, pd.DataFrame]:
    def leer(ruta: str) -> pd.DataFrame:
        return pd.read_csv(BASE / ruta, encoding="utf-8-sig")

    cauca = leer("data/clean/irca_cauca_municipal.csv")
    dep = leer("data/clean/irca_cauca_departamento.csv")
    nac_mun = leer("data/clean/irca_nacional_municipal_2025.csv")
    nac_dep = leer("data/clean/irca_nacional_departamental_2025.csv")
    resumen = leer("reports/tablas/resumen_anual_cauca.csv")
    ranking = leer("reports/tablas/ranking_2025.csv")
    brecha = leer("reports/tablas/brecha_urbano_rural.csv")
    persistencia = leer("reports/tablas/persistencia_riesgo.csv")
    contexto = leer("reports/tablas/contexto_nacional_2025.csv")
    contexto_resumen = leer("reports/tablas/contexto_nacional_resumen.csv")
    metricas = leer("reports/tablas/metricas_modelo.csv")
    predicciones = leer("reports/tablas/predicciones_2026.csv")
    pred_test = leer("reports/tablas/predicciones_test.csv")
    calidad = leer("reports/tablas/calidad_datos.csv")
    coeficientes = leer("reports/tablas/coeficientes_modelo.csv")

    for df in (cauca, dep, nac_mun, nac_dep, resumen, ranking, brecha, persistencia, contexto, predicciones, pred_test):
        if "anio" in df.columns:
            df["anio"] = df["anio"].astype(int)

    return {
        "cauca": cauca,
        "dep": dep,
        "nac_mun": nac_mun,
        "nac_dep": nac_dep,
        "resumen": resumen,
        "ranking": ranking,
        "brecha": brecha,
        "persistencia": persistencia,
        "contexto": contexto,
        "contexto_resumen": contexto_resumen,
        "metricas": metricas,
        "predicciones": predicciones,
        "pred_test": pred_test,
        "calidad": calidad,
        "coeficientes": coeficientes,
    }


def ranking_para_anio(cauca: pd.DataFrame, ranking_2025: pd.DataFrame, anio: int) -> pd.DataFrame:
    if anio == 2025:
        return ranking_2025.copy()
    df = cauca[cauca["anio"] == anio].copy()
    df["puesto_departamental"] = df["irca"].rank(ascending=False, method="min").astype(int)
    for columna in [
        "puesto_nacional",
        "percentil_nacional",
        "mediana_nacional",
        "diferencia_vs_mediana_nacional",
        "anios_riesgo_medio_alto",
        "anios_con_dato",
        "pct_anios_riesgo",
    ]:
        df[columna] = np.nan
    return df


# ---------------------------------------------------------------------------
# Gráficos
# ---------------------------------------------------------------------------
BANDAS = [
    (0, 5, "rgba(46,125,50,0.08)", "Sin riesgo"),
    (5, 14, "rgba(156,204,101,0.10)", "Riesgo bajo"),
    (14, 35, "rgba(255,193,7,0.10)", "Riesgo medio"),
    (35, 80, "rgba(239,108,0,0.08)", "Riesgo alto"),
    (80, 100, "rgba(198,40,40,0.08)", "Inviable"),
]


def bandas_riesgo(fig: go.Figure) -> None:
    for y0, y1, color, etiqueta in BANDAS:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=color, line_width=0, layer="below")
        fig.add_annotation(
            x=2025.35,
            y=(y0 + y1) / 2,
            text=etiqueta,
            showarrow=False,
            xanchor="right",
            font=dict(size=9, color="#607080"),
            bgcolor="rgba(255,255,255,0.65)",
        )


def grafico_evolucion(dep: pd.DataFrame, anio: int, zona: str) -> go.Figure:
    fig = go.Figure()
    bandas_riesgo(fig)
    series = [
        ("irca", "Total", COLOR_CAUCA, "circle"),
        ("irca_urbano", "Urbano", COLOR_URBANO, "square"),
        ("irca_rural", "Rural", COLOR_RURAL, "triangle-up"),
    ]
    for columna, nombre, color, simbolo in series:
        destacada = (zona == nombre) or (zona == "Total" and nombre == "Total")
        fig.add_trace(
            go.Scatter(
                x=dep["anio"],
                y=dep[columna],
                mode="lines+markers",
                name=nombre,
                line=dict(color=color, width=3.2 if destacada else 1.3),
                marker=dict(size=7 if destacada else 4, symbol=simbolo, color=color),
                opacity=1.0 if destacada else 0.45,
                hovertemplate=f"{nombre}: %{{y:.1f}}<extra></extra>",
            )
        )
    fig.add_vline(
        x=anio,
        line_width=1.2,
        line_dash="dash",
        line_color="#37474F",
        annotation_text=str(anio),
        annotation_position="top",
    )
    fig.update_layout(
        title="Evolución del IRCA departamental",
        height=430,
        margin=dict(l=10, r=10, t=50, b=10),
        hovermode="x unified",
        legend=dict(orientation="h", y=1.08, x=0),
        yaxis=dict(title="IRCA (0-100)", range=[0, 100]),
        xaxis=dict(title="Año", dtick=2, range=[2006.5, 2025.8]),
        plot_bgcolor="white",
    )
    return fig


def grafico_categorias(resumen: pd.DataFrame, anio: int) -> go.Figure:
    mapa = {
        "Sin riesgo": "pct_sin_riesgo",
        "Riesgo bajo": "pct_riesgo_bajo",
        "Riesgo medio": "pct_riesgo_medio",
        "Riesgo alto": "pct_riesgo_alto",
        "Inviable sanitariamente": "pct_inviable",
    }
    fig = go.Figure()
    for categoria in RISK_ORDER:
        fig.add_trace(
            go.Bar(
                x=resumen["anio"],
                y=resumen[mapa[categoria]],
                name=categoria,
                marker_color=RISK_COLORS[categoria],
                hovertemplate=f"{categoria}: %{{y:.1f}}%<extra></extra>",
            )
        )
    fig.add_vline(
        x=anio,
        line_width=1.2,
        line_dash="dash",
        line_color="#37474F",
        annotation_text=str(anio),
        annotation_position="top",
    )
    fig.update_layout(
        title="Distribución de municipios por categoría de riesgo",
        height=410,
        margin=dict(l=10, r=10, t=50, b=80),
        barmode="stack",
        bargap=0.18,
        legend=dict(orientation="h", y=-0.22, x=0, traceorder="normal"),
        yaxis=dict(title="% de municipios", range=[0, 100]),
        xaxis=dict(title="Año", dtick=2, title_standoff=8),
        plot_bgcolor="white",
    )
    return fig


def grafico_ranking(ranking: pd.DataFrame, anio: int) -> go.Figure:
    datos = ranking.sort_values("irca", ascending=True)
    fig = go.Figure(
        go.Bar(
            x=datos["irca"],
            y=datos["municipio"],
            orientation="h",
            marker_color=[RISK_COLORS[c] for c in datos["nivel_riesgo"]],
            text=[num(v) for v in datos["irca"]],
            textposition="outside",
            cliponaxis=False,
            customdata=np.stack(
                [
                    datos["nivel_riesgo"],
                    datos["irca_urbano"],
                    datos["irca_rural"],
                ],
                axis=-1,
            ),
            hovertemplate=(
                "<b>%{y}</b><br>IRCA: %{x:.1f}<br>"
                "Categoría: %{customdata[0]}<br>"
                "Urbano: %{customdata[1]:.1f}<br>Rural: %{customdata[2]:.1f}<extra></extra>"
            ),
        )
    )
    fig.add_vline(
        x=14,
        line_dash="dot",
        line_color="#EF6C00",
        annotation_text="14",
        annotation_position="top",
    )
    fig.add_vline(
        x=35,
        line_dash="dot",
        line_color="#C62828",
        annotation_text="35",
        annotation_position="top",
    )
    fig.update_layout(
        title=f"IRCA municipal {anio} (arriba: mayor riesgo)",
        height=max(420, 21 * len(datos)),
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(title="IRCA (0-100)", range=[0, max(45, datos["irca"].max() + 8)]),
        yaxis=dict(title="", tickfont=dict(size=8)),
        plot_bgcolor="white",
    )
    return fig


def grafico_detalle(cauca: pd.DataFrame, municipio: str) -> go.Figure:
    datos = cauca[cauca["municipio"] == municipio].sort_values("anio")
    anios = list(range(2007, 2026))
    fig = go.Figure()
    bandas_riesgo(fig)
    for columna, nombre, color, simbolo in [
        ("irca", "Total", COLOR_CAUCA, "circle"),
        ("irca_urbano", "Urbano", COLOR_URBANO, "square"),
        ("irca_rural", "Rural", COLOR_RURAL, "triangle-up"),
    ]:
        serie = datos.set_index("anio")[columna].reindex(anios)
        fig.add_trace(
            go.Scatter(
                x=serie.index,
                y=serie.values,
                mode="lines+markers",
                name=nombre,
                line=dict(color=color, width=2.4 if nombre == "Total" else 1.5),
                marker=dict(size=6, symbol=simbolo, color=color),
                connectgaps=False,
                hovertemplate=f"{nombre}: %{{y:.1f}}<extra></extra>",
            )
        )
    fig.update_layout(
        title=f"{municipio}: serie histórica del IRCA",
        height=390,
        margin=dict(l=10, r=10, t=50, b=10),
        hovermode="x unified",
        legend=dict(orientation="h", y=1.08, x=0),
        yaxis=dict(title="IRCA (0-100)", range=[0, 100]),
        xaxis=dict(title="Año", dtick=2, range=[2006.5, 2025.8]),
        plot_bgcolor="white",
    )
    return fig


def grafico_heatmap(cauca: pd.DataFrame) -> go.Figure:
    tabla = cauca.pivot_table(index="municipio", columns="anio", values="irca", aggfunc="mean")
    orden = tabla.mean(axis=1).sort_values(ascending=False).index
    tabla = tabla.loc[orden]
    fig = go.Figure(
        go.Heatmap(
            z=tabla.values,
            x=[str(c) for c in tabla.columns],
            y=tabla.index,
            colorscale="RdYlGn_r",
            zmin=0,
            zmax=100,
            colorbar=dict(title="IRCA", thickness=14),
            hoverongaps=False,
            hovertemplate="<b>%{y}</b><br>Año: %{x}<br>IRCA: %{z:.1f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Mapa de calor: IRCA por municipio y año",
        height=860,
        margin=dict(l=10, r=10, t=50, b=10),
        plot_bgcolor="#E0E0E0",
        xaxis=dict(title="Año", tickangle=-45, tickfont=dict(size=9)),
        yaxis=dict(title="", autorange="reversed", tickfont=dict(size=8)),
    )
    return fig


def grafico_contexto(contexto: pd.DataFrame) -> go.Figure:
    datos = contexto.sort_values("irca", ascending=True)
    colores = [
        COLOR_CAUCA if c else ("#FFB74D" if v else COLOR_NEUTRO)
        for c, v in zip(datos["es_cauca"], datos["es_vecino"])
    ]
    fig = go.Figure(
        go.Bar(
            x=datos["irca"],
            y=[corto(d) for d in datos["departamento"]],
            orientation="h",
            marker_color=colores,
            text=[num(v) for v in datos["irca"]],
            textposition="outside",
            cliponaxis=False,
            customdata=np.stack([datos["departamento"], datos["puesto"], datos["nivel_riesgo"]], axis=-1),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>IRCA: %{x:.1f}<br>"
                "Puesto: %{customdata[1]} de 33<br>Categoría: %{customdata[2]}<extra></extra>"
            ),
        )
    )
    fig.add_vline(
        x=7.0,
        line_dash="dash",
        line_color="#455A64",
        annotation_text="Mediana 7,0",
        annotation_position="top",
    )
    fig.update_layout(
        title="Ranking departamental 2025 (arriba: mayor IRCA)",
        height=820,
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(title="IRCA (0-100)", range=[0, max(50, datos["irca"].max() + 8)]),
        yaxis=dict(title="", tickfont=dict(size=8), automargin=True),
        plot_bgcolor="white",
    )
    return fig


def grafico_distribucion(nac_mun: pd.DataFrame, cauca_2025: pd.DataFrame, dep_2025: float) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=nac_mun["irca"],
            nbinsx=40,
            marker_color="#CFD8DC",
            marker_line_color="white",
            marker_line_width=1,
            name="Municipios de Colombia",
            hovertemplate="IRCA %{x}<br>Municipios: %{y}<extra></extra>",
        )
    )
    mediana_nacional = float(nac_mun["irca"].median())
    mediana_cauca = float(cauca_2025["irca"].median())
    fig.add_vline(
        x=mediana_nacional,
        line_color="#455A64",
        line_dash="dash",
        annotation_text=f"Mediana nacional {num(mediana_nacional)}",
        annotation_position="top",
    )
    fig.add_vline(
        x=mediana_cauca,
        line_color=COLOR_CAUCA,
        annotation_text=f"Mediana Cauca {num(mediana_cauca)}",
        annotation_position="bottom",
    )
    max_count = int(np.histogram(nac_mun["irca"], bins=40, range=(0, 100))[0].max())
    fig.add_trace(
        go.Scatter(
            x=cauca_2025["irca"],
            y=[-max_count * 0.07] * len(cauca_2025),
            mode="markers",
            marker=dict(symbol="line-ns-open", size=14, color=COLOR_CAUCA, line=dict(width=2)),
            name="Municipios del Cauca",
            hovertemplate="IRCA: %{x:.1f}<extra></extra>",
        )
    )
    fig.add_hline(y=0, line_color="#B0BEC5", line_width=1)
    fig.update_layout(
        title="Distribución nacional municipal 2025",
        height=420,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=1.12, x=0),
        xaxis=dict(title="IRCA (0-100)", range=[0, 100]),
        yaxis=dict(title="Número de municipios", range=[-max_count * 0.14, max_count * 1.12]),
        plot_bgcolor="white",
        bargap=0.05,
    )
    fig.add_annotation(
        x=99,
        y=max_count * 0.55,
        text=f"Cauca departamental: {num(dep_2025)}",
        showarrow=False,
        xanchor="right",
        font=dict(size=10, color=COLOR_CAUCA),
        bgcolor="rgba(255,255,255,0.8)",
    )
    return fig


def grafico_modelo_scatter(pred_test: pd.DataFrame) -> go.Figure:
    datos = pred_test[pred_test["modelo"] == "Regresión lineal simple"].copy()
    fig = go.Figure(
        go.Scatter(
            x=datos["irca_real"],
            y=datos["irca_predicho"],
            mode="markers",
            marker=dict(
                color=datos["anio"],
                colorscale="Viridis",
                size=9,
                showscale=True,
                colorbar=dict(title="Año", thickness=14),
                line=dict(width=0.5, color="white"),
            ),
            customdata=np.stack([datos["municipio"], datos["anio"]], axis=-1),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>Año: %{customdata[1]}<br>"
                "Real: %{x:.1f}<br>Predicho: %{y:.1f}<extra></extra>"
            ),
            name="Observaciones",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0, 100],
            y=[0, 100],
            mode="lines",
            line=dict(color="#455A64", dash="dash", width=1.5),
            name="Predicción perfecta",
        )
    )
    fig.update_layout(
        title="Prueba 2022-2025: real vs. predicho",
        height=470,
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(title="IRCA observado", range=[0, 100]),
        yaxis=dict(title="IRCA predicho", range=[0, 100]),
        legend=dict(orientation="h", y=1.08, x=0),
        plot_bgcolor="white",
    )
    return fig


def grafico_pronostico(predicciones: pd.DataFrame) -> go.Figure:
    datos = predicciones.sort_values("irca_2026_predicho", ascending=True)
    fig = go.Figure(
        go.Bar(
            x=datos["irca_2026_predicho"],
            y=datos["municipio"],
            orientation="h",
            marker_color=[RISK_COLORS[c] for c in datos["categoria_predicha"]],
            text=[num(v) for v in datos["irca_2026_predicho"]],
            textposition="outside",
            cliponaxis=False,
            error_x=dict(
                type="data",
                array=datos["mae_prueba"],
                visible=True,
                color="#37474F",
                thickness=1,
                width=2,
            ),
            customdata=np.stack(
                [
                    datos["irca_2025"],
                    datos["intervalo_inferior"],
                    datos["intervalo_superior"],
                    datos["categoria_predicha"],
                ],
                axis=-1,
            ),
            hovertemplate=(
                "<b>%{y}</b><br>IRCA 2025: %{customdata[0]:.1f}<br>"
                "Pronóstico 2026: %{x:.1f}<br>"
                "Rango ±MAE: %{customdata[1]:.1f} – %{customdata[2]:.1f}<br>"
                "Categoría: %{customdata[3]}<extra></extra>"
            ),
        )
    )
    fig.add_vline(
        x=14,
        line_dash="dash",
        line_color="#EF6C00",
        annotation_text="Umbral 14",
        annotation_position="top",
    )
    fig.update_layout(
        title="Pronóstico 2026: escenario con el modelo simple",
        height=700,
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(title="IRCA (0-100)", range=[0, max(45, datos["irca_2026_predicho"].max() + 10)]),
        yaxis=dict(title="", tickfont=dict(size=7)),
        plot_bgcolor="white",
    )
    return fig


# ---------------------------------------------------------------------------
# Componentes de interfaz
# ---------------------------------------------------------------------------
def tarjeta_hallazgo(titulo: str, texto: str) -> None:
    st.markdown(
        f'<div class="hallazgo"><span class="titulo">{titulo}</span>{texto}</div>',
        unsafe_allow_html=True,
    )


def tabla_formateada(df: pd.DataFrame, columnas: dict[str, str]) -> pd.DataFrame:
    tabla = df[list(columnas)].rename(columns=columnas).copy()
    for columna in tabla.columns:
        if pd.api.types.is_float_dtype(tabla[columna]):
            tabla[columna] = tabla[columna].map(lambda v: num(v))
    return tabla


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
def main() -> None:
    datos = cargar_datos()
    cauca = datos["cauca"]
    dep = datos["dep"]
    nac_mun = datos["nac_mun"]
    ranking_2025 = datos["ranking"]
    resumen = datos["resumen"]
    contexto = datos["contexto"]

    anios = sorted(cauca["anio"].unique(), reverse=True)
    municipios = sorted(cauca["municipio"].unique())

    with st.sidebar:
        st.markdown("## 💧 IRCA Cauca")
        st.caption("Observatorio de calidad del agua para consumo humano")
        st.markdown("---")
        anio = st.selectbox("Año de análisis", anios, index=0)
        zona = st.radio("Serie destacada", ["Total", "Urbano", "Rural"], horizontal=True)
        st.markdown("---")
        st.markdown("**Filtros de municipios**")
        municipios_sel = st.multiselect(
            "Municipios",
            municipios,
            default=[],
            help="Sin selección se muestran todos los municipios.",
        )
        riesgos_sel = st.multiselect(
            "Categoría de riesgo",
            RISK_ORDER,
            default=RISK_ORDER,
        )
        st.markdown("---")
        st.caption("Fuente: SIVICAP – MinSalud/INS.")
        st.caption("Datos agregados; no contienen información personal.")
        st.caption("Corte nacional: 2025. Serie municipal: 2007-2025.")

    st.markdown("# Calidad del agua para consumo humano en el Cauca")
    st.markdown(
        '<div class="subtitulo">IRCA 2007–2025 · 42 municipios · contexto nacional 2025 · '
        "dashboard reproducible con datos abiertos</div>",
        unsafe_allow_html=True,
    )

    ranking_anio = ranking_para_anio(cauca, ranking_2025, anio)
    if municipios_sel:
        ranking_anio = ranking_anio[ranking_anio["municipio"].isin(municipios_sel)]
    if riesgos_sel:
        ranking_anio = ranking_anio[ranking_anio["nivel_riesgo"].isin(riesgos_sel)]

    tab_resumen, tab_municipios, tab_contexto, tab_modelo = st.tabs(
        ["📊 Resumen", "🏙️ Municipios", "🌎 Contexto nacional", "🤖 Modelo"]
    )

    # =======================================================================
    # TAB 1: RESUMEN
    # =======================================================================
    with tab_resumen:
        dep_anio = dep[dep["anio"] == anio].iloc[0]
        mun_anio = cauca[cauca["anio"] == anio]
        n_mun = mun_anio["municipio"].nunique()
        n_riesgo = int(
            mun_anio["nivel_riesgo"].isin(["Riesgo medio", "Riesgo alto", "Inviable sanitariamente"]).sum()
        )
        n_rural = int(mun_anio["irca_rural"].notna().sum())
        brecha = mun_anio["brecha_rural_urbano"].mean()

        previo = dep[dep["anio"] == anio - 1]
        delta = None
        if not previo.empty:
            delta = f"{num(dep_anio['irca'] - previo['irca'].iloc[0])} pts vs. {anio - 1}"

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.metric(
                f"IRCA Cauca {anio}",
                num(dep_anio["irca"]),
                delta=delta,
                delta_color="inverse",
                help="IRCA departamental (fila #TODOS). Menor es mejor.",
                border=True,
            )
        with c2:
            st.metric(
                "Municipios con dato",
                f"{n_mun} de 42",
                help="Cobertura municipal en el año seleccionado.",
                border=True,
            )
        with c3:
            st.metric(
                "Riesgo medio/alto",
                f"{n_riesgo} de {n_mun}",
                help=f"{num(n_riesgo / n_mun * 100)}% de los municipios con dato. "
                "Incluye riesgo medio, alto e inviable.",
                border=True,
            )
        with c4:
            st.metric(
                "Cobertura rural 2025",
                f"{num(n_rural / n_mun * 100, 0)}%",
                help=f"{n_rural} de {n_mun} municipios con IRCA rural reportado. "
                "En toda la serie 2007-2025, 66,4% de los registros municipales no tienen dato rural.",
                border=True,
            )
        with c5:
            st.metric(
                "Brecha rural-urbana",
                num(brecha) + " pts",
                help="2025. IRCA rural menos IRCA urbano, promedio simple del año seleccionado. "
                "Positivo = peor situación rural. En las 242 observaciones de toda la serie, "
                "la brecha promedio es 12,2 puntos.",
                border=True,
            )

        col_izq, col_der = st.columns([1.65, 1])
        with col_izq:
            st.plotly_chart(grafico_evolucion(dep, anio, zona), width="stretch")
            st.caption(
                "Bandas de color: umbrales oficiales del IRCA. La línea gruesa resalta la serie elegida en la barra lateral."
            )
        with col_der:
            st.markdown("### Hallazgos principales")
            dep_2007 = dep[dep["anio"] == 2007].iloc[0]
            dep_2024 = dep[dep["anio"] == 2024].iloc[0]
            top = ranking_2025.head(4)
            top_txt = ", ".join(
                f"{fila.municipio} ({num(fila.irca)})" for fila in top.itertuples()
            )
            tarjeta_hallazgo(
                "1. Mejora con rebote en 2025",
                f"El IRCA departamental pasó de <b>{num(dep_2007['irca'])}</b> en 2007 a "
                f"<b>{num(dep_2024['irca'])}</b> en 2024, pero subió a "
                f"<b>{num(dep_anio['irca'])}</b> en 2025 (riesgo bajo).",
            )
            tarjeta_hallazgo(
                "2. El riesgo se concentra",
                f"En 2025, <b>{n_riesgo} de {n_mun}</b> municipios están en riesgo medio/alto: "
                f"{top_txt}. Timbiquí y Caldono son los casos más críticos.",
            )
            ambos = cauca.dropna(subset=["irca_urbano", "irca_rural"])
            tarjeta_hallazgo(
                "3. La brecha rural es grande, pero está subreportada",
                f"En las <b>{len(ambos)}</b> observaciones con ambos datos, la brecha promedio es "
                f"<b>{num(ambos['brecha_rural_urbano'].mean())} puntos</b>. Sin embargo, "
                f"<b>{num(cauca['irca_rural'].isna().mean() * 100)}%</b> de los registros municipales "
                "no tienen IRCA rural.",
            )
            st.markdown(
                '<div class="nota">Los datos son agregados y no permiten identificar hogares, '
                "veredas ni causas específicas. Las cifras describen el reporte municipal, no una "
                "medición de campo independiente.</div>",
                unsafe_allow_html=True,
            )

        st.plotly_chart(grafico_categorias(resumen, anio), width="stretch")

        with st.expander("🔎 Fuente, limpieza y calidad del dato", expanded=False):
            st.markdown(
                f"**Fuente:** {FUENTE}\n\n"
                "**Universo:** 20.212 registros nacionales; 736 registros municipales del Cauca "
                "(42 municipios, 2007-2025) y 19 filas agregadas departamentales `#TODOS`.\n\n"
                "**Decisiones:** los valores `ND` se conservan como nulos (no se imputan); "
                "las variantes `Bajo riesgo`/`Alto riesgo` se unifican; los agregados `#TODOS` "
                "se separan para evitar doble conteo; el IRCA se calcula con los umbrales oficiales "
                "(5, 14, 35 y 80)."
            )
            calidad = datos["calidad"].rename(
                columns={
                    "chequeo": "Chequeo",
                    "resultado": "Resultado",
                    "detalle": "Detalle",
                    "tratamiento": "Tratamiento",
                }
            )
            st.dataframe(calidad, width="stretch", hide_index=True)
            cobertura = (
                cauca.groupby("anio")["municipio"].nunique().reset_index(name="municipios")
            )
            fig_cob = go.Figure(
                go.Bar(
                    x=cobertura["anio"],
                    y=cobertura["municipios"],
                    marker_color=COLOR_CAUCA,
                    hovertemplate="Año %{x}<br>Municipios: %{y}<extra></extra>",
                )
            )
            fig_cob.update_layout(
                title="Cobertura municipal del Cauca por año",
                height=300,
                margin=dict(l=10, r=10, t=45, b=10),
                xaxis=dict(dtick=2),
                yaxis=dict(range=[0, 45], title="Municipios"),
                plot_bgcolor="white",
            )
            st.plotly_chart(fig_cob, width="stretch")
            st.markdown(
                '<div class="alerta"><b>Limitación central:</b> Popayán solo tiene datos '
                "2008-2019 y no aparece en 2020-2025. En 2025 faltan Balboa, Florencia y "
                "López de Micay. El ranking y los promedios no representan a los 42 municipios "
                "en todos los años.</div>",
                unsafe_allow_html=True,
            )

    # =======================================================================
    # TAB 2: MUNICIPIOS
    # =======================================================================
    with tab_municipios:
        st.markdown(f"### Ranking municipal {anio}")
        if ranking_anio.empty:
            st.warning("No hay municipios que cumplan los filtros seleccionados.")
        else:
            st.plotly_chart(grafico_ranking(ranking_anio, anio), width="stretch")
            tabla = ranking_anio.copy()
            tabla["Puesto"] = tabla["puesto_departamental"].astype(int)
            tabla["Percentil nacional"] = tabla["percentil_nacional"].map(
                lambda v: num(v) + "%" if pd.notna(v) else "—"
            )
            tabla["Años en riesgo"] = tabla.apply(
                lambda f: f"{int(f['anios_riesgo_medio_alto'])} de {int(f['anios_con_dato'])}"
                if pd.notna(f["anios_riesgo_medio_alto"]) and pd.notna(f["anios_con_dato"])
                else "—",
                axis=1,
            )
            tabla_mostrar = tabla[
                [
                    "municipio",
                    "irca",
                    "nivel_riesgo",
                    "irca_urbano",
                    "irca_rural",
                    "brecha_rural_urbano",
                    "Puesto",
                    "Percentil nacional",
                    "Años en riesgo",
                ]
            ].rename(
                columns={
                    "municipio": "Municipio",
                    "irca": "IRCA",
                    "nivel_riesgo": "Categoría",
                    "irca_urbano": "Urbano",
                    "irca_rural": "Rural",
                    "brecha_rural_urbano": "Brecha rural-urbano",
                }
            )
            for columna in ["IRCA", "Urbano", "Rural", "Brecha rural-urbano"]:
                tabla_mostrar[columna] = tabla_mostrar[columna].map(lambda v: num(v))
            st.dataframe(tabla_mostrar, width="stretch", hide_index=True)
            st.caption(
                "Puesto departamental: 1 = mayor IRCA (peor). Los empates comparten puesto. "
                "El percentil nacional solo está disponible para 2025; indica el porcentaje de "
                "municipios del país con IRCA menor o igual."
            )
            st.download_button(
                "⬇️ Descargar ranking (CSV)",
                data=ranking_anio.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"ranking_irca_cauca_{anio}.csv",
                mime="text/csv",
            )

        st.markdown("---")
        st.markdown("### Detalle por municipio")
        opciones = sorted(cauca["municipio"].unique())
        indice = opciones.index("Timbiquí") if "Timbiquí" in opciones else 0
        municipio_detalle = st.selectbox("Selecciona un municipio", opciones, index=indice)
        detalle = cauca[cauca["municipio"] == municipio_detalle].sort_values("anio")
        ultimo = detalle.iloc[-1]
        n_anios = detalle["anio"].nunique()
        n_riesgo_mun = int(
            detalle["nivel_riesgo"].isin(["Riesgo medio", "Riesgo alto", "Inviable sanitariamente"]).sum()
        )
        ultima_brecha = detalle["brecha_rural_urbano"].dropna()
        ultima_brecha = ultima_brecha.iloc[-1] if not ultima_brecha.empty else np.nan

        k1, k2, k3, k4, k5 = st.columns(5)
        with k1:
            st.metric(
                f"Último IRCA ({int(ultimo['anio'])})",
                num(ultimo["irca"]),
                help=f"Categoría: {ultimo['nivel_riesgo']}.",
                border=True,
            )
        with k2:
            st.metric("Años con dato", f"{n_anios} de 19", border=True)
        with k3:
            st.metric(
                "Años en riesgo",
                f"{n_riesgo_mun}",
                help="Años con IRCA medio, alto o inviable sanitariamente.",
                border=True,
            )
        with k4:
            st.metric(
                "Brecha rural-urbano",
                num(ultima_brecha) + " pts" if pd.notna(ultima_brecha) else "—",
                help="IRCA rural menos IRCA urbano en el último año con ambos datos."
                if pd.notna(ultima_brecha)
                else "El último año no tiene dato rural.",
                border=True,
            )
        with k5:
            st.metric(
                "IRCA urbano / rural",
                f"{num(ultimo['irca_urbano'])} / {num(ultimo['irca_rural'])}",
                help=f"Valores de {int(ultimo['anio'])}.",
                border=True,
            )

        if int(ultimo["anio"]) < 2025:
            st.warning(
                f"{municipio_detalle} no tiene dato en 2025; su último registro es de "
                f"{int(ultimo['anio'])}. No se debe comparar directamente con el ranking 2025."
            )
        if municipio_detalle == "Popayán":
            st.info("Popayán solo reporta 2008-2019; no aparece en los cortes 2020-2025.")

        st.plotly_chart(grafico_detalle(cauca, municipio_detalle), width="stretch")
        tabla_detalle = detalle[
            ["anio", "irca", "nivel_riesgo", "irca_urbano", "irca_rural", "brecha_rural_urbano"]
        ].rename(
            columns={
                "anio": "Año",
                "irca": "IRCA",
                "nivel_riesgo": "Categoría",
                "irca_urbano": "Urbano",
                "irca_rural": "Rural",
                "brecha_rural_urbano": "Brecha",
            }
        )
        for columna in ["IRCA", "Urbano", "Rural", "Brecha"]:
            tabla_detalle[columna] = tabla_detalle[columna].map(lambda v: num(v))
        st.dataframe(tabla_detalle, width="stretch", hide_index=True)

        st.markdown("---")
        st.markdown("### Mapa de calor municipal")
        st.plotly_chart(grafico_heatmap(cauca), width="stretch")
        st.caption("Gris = año sin dato. Filas ordenadas por IRCA promedio histórico (mayor arriba).")

    # =======================================================================
    # TAB 3: CONTEXTO NACIONAL
    # =======================================================================
    with tab_contexto:
        st.markdown("### ¿Cómo está el Cauca frente al país?")
        cauca_dep_2025 = dep[dep["anio"] == 2025].iloc[0]
        cauca_mun_2025 = cauca[cauca["anio"] == 2025]
        mediana_nacional = float(nac_mun["irca"].median())
        mediana_departamental = float(contexto["irca"].median())
        mediana_cauca = float(cauca_mun_2025["irca"].median())
        puesto_cauca = int(contexto.loc[contexto["es_cauca"], "puesto"].iloc[0])
        percentil_mediana = float((nac_mun["irca"] <= mediana_cauca).mean() * 100)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric(
                "Puesto del Cauca",
                f"{puesto_cauca} de 33",
                help="Ranking de los 33 departamentos con dato en 2025. 1 = menor IRCA (mejor).",
                border=True,
            )
        with c2:
            st.metric(
                "Mediana departamental",
                num(mediana_departamental),
                help="Mediana de los 33 departamentos con dato en 2025.",
                border=True,
            )
        with c3:
            st.metric(
                "Mediana municipal nacional",
                num(mediana_nacional),
                help="Mediana de los 1.019 municipios con dato en 2025.",
                border=True,
            )
        with c4:
            st.metric(
                "Mediana municipal Cauca",
                num(mediana_cauca),
                help=f"Percentil {num(percentil_mediana)} de la distribución nacional municipal.",
                border=True,
            )

        col_izq, col_der = st.columns([1.35, 1])
        with col_izq:
            st.plotly_chart(grafico_contexto(contexto), width="stretch")
            st.caption("Azul: Cauca. Naranja: departamentos vecinos. Gris: resto del país.")
        with col_der:
            st.plotly_chart(
                grafico_distribucion(nac_mun, cauca_mun_2025, cauca_dep_2025["irca"]),
                width="stretch",
            )
            st.caption(
                f"La línea azul gruesa marca la mediana de los 38 municipios del Cauca con dato 2025 "
                f"({num(mediana_cauca)}); el IRCA departamental es {num(cauca_dep_2025['irca'])}. "
                "Las marcas azules inferiores son esos municipios."
            )

        vecinos = contexto[
            contexto["departamento"].isin(["Cauca"] + DEPARTAMENTOS_VECINOS)
        ].sort_values("irca")
        vecinos_mostrar = vecinos[
            ["departamento", "irca", "nivel_riesgo", "puesto", "diferencia_vs_mediana"]
        ].rename(
            columns={
                "departamento": "Departamento",
                "irca": "IRCA 2025",
                "nivel_riesgo": "Categoría",
                "puesto": "Puesto",
                "diferencia_vs_mediana": "Diferencia vs. mediana",
            }
        )
        for columna in ["IRCA 2025", "Diferencia vs. mediana"]:
            vecinos_mostrar[columna] = vecinos_mostrar[columna].map(lambda v: num(v))
        st.markdown("#### Cauca y departamentos vecinos")
        st.dataframe(vecinos_mostrar, width="stretch", hide_index=True)

        st.markdown(
            f'<div class="hallazgo"><span class="titulo">Lectura del contexto</span>'
            f"El Cauca ocupa el puesto <b>{puesto_cauca} de 33</b>, con un IRCA de "
            f"<b>{num(cauca_dep_2025['irca'])}</b>, ligeramente por encima de la mediana "
            f"departamental (<b>{num(mediana_departamental)}</b>). Está mejor que Nariño "
            f"(<b>22,5</b>) y Putumayo (<b>17,0</b>), pero peor que Valle del Cauca "
            f"(<b>4,4</b>), Huila (<b>4,1</b>) y Caquetá (<b>6,7</b>). El municipio mediano "
            f"del Cauca (<b>{num(mediana_cauca)}</b>) se sitúa en el percentil "
            f"<b>{num(percentil_mediana)}</b> de la distribución nacional: la mitad del país "
            "tiene un IRCA menor o igual.</div>",
            unsafe_allow_html=True,
        )

        st.markdown("#### Municipios del Cauca con mayor riesgo relativo nacional")
        top_nacional = ranking_2025.head(8)[
            ["municipio", "irca", "nivel_riesgo", "puesto_nacional", "percentil_nacional"]
        ].rename(
            columns={
                "municipio": "Municipio",
                "irca": "IRCA 2025",
                "nivel_riesgo": "Categoría",
                "puesto_nacional": "Puesto nacional",
                "percentil_nacional": "Percentil nacional",
            }
        )
        top_nacional["IRCA 2025"] = top_nacional["IRCA 2025"].map(lambda v: num(v))
        top_nacional["Percentil nacional"] = top_nacional["Percentil nacional"].map(
            lambda v: num(v) + "%"
        )
        st.dataframe(top_nacional, width="stretch", hide_index=True)
        st.caption(
            "Puesto nacional: 1 = mayor IRCA del país (peor). Percentil: porcentaje de municipios "
            "del país con IRCA menor o igual. Timbiquí está en el percentil 94,3: solo ~6% de los "
            "municipios del país tienen un IRCA peor."
        )

    # =======================================================================
    # TAB 4: MODELO
    # =======================================================================
    with tab_modelo:
        st.markdown("### Modelo predictivo simple del IRCA municipal")
        prueba = datos["metricas"][
            datos["metricas"]["conjunto"] == "Prueba (2022-2025)"
        ].copy()
        final = prueba[prueba["modelo"] == "Regresión lineal simple"].iloc[0]
        naive = prueba[prueba["modelo"] == "Naive (último valor)"].iloc[0]

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.metric(
                "Modelo final",
                "Lineal simple",
                help="Regresión lineal con dos predictores: IRCA del año anterior y media móvil de 3 años.",
                border=True,
            )
        with c2:
            st.metric(
                "MAE de prueba",
                num(final["mae"]) + " pts",
                help=f"Error absoluto medio en 2022-2025. Naive: {num(naive['mae'])}. Menor es mejor.",
                border=True,
            )
        with c3:
            st.metric(
                "RMSE de prueba",
                num(final["rmse"]) + " pts",
                help="Raíz del error cuadrático medio; penaliza más los errores grandes.",
                border=True,
            )
        with c4:
            st.metric(
                "R² de prueba",
                num(final["r2"], 2),
                help="Un R² negativo o cercano a cero indica que el modelo no explica la varianza.",
                border=True,
            )
        with c5:
            st.metric(
                "Observaciones de prueba",
                f"{int(final['n'])}",
                help="Municipio-año con datos completos en 2022-2025.",
                border=True,
            )

        st.markdown(
            '<div class="alerta"><b>Cómo leer el modelo:</b> se entrenó con datos hasta 2021 y se '
            "evaluó con 2022-2025. El MAE de 5,26 puntos mejora solo 0,37 puntos al pronóstico "
            "ingenuo (repetir el último valor). El R² de prueba es -0,06: el modelo <b>no</b> "
            "explica bien la varianza y no debe usarse como certeza. Los valores de 2026 son "
            "escenarios, no predicciones oficiales.</div>",
            unsafe_allow_html=True,
        )

        st.markdown("#### Comparación de modelos (conjunto de prueba)")
        metricas_mostrar = prueba[
            ["modelo", "n", "mae", "rmse", "r2", "mape"]
        ].rename(
            columns={
                "modelo": "Modelo",
                "n": "n",
                "mae": "MAE",
                "rmse": "RMSE",
                "r2": "R²",
                "mape": "MAPE (%)",
            }
        )
        for columna in ["MAE", "RMSE", "R²", "MAPE (%)"]:
            metricas_mostrar[columna] = metricas_mostrar[columna].map(lambda v: num(v, 2))
        st.dataframe(metricas_mostrar, width="stretch", hide_index=True)
        st.caption(
            "La regresión completa tiene un MAE apenas 0,01 puntos menor, pero usa 8 variables. "
            "Se prefirió la regresión simple por parsimonia y estabilidad. El Random Forest tiene "
            "mejor R², pero peor MAE."
        )

        col_izq, col_der = st.columns([1, 1.1])
        with col_izq:
            st.plotly_chart(grafico_modelo_scatter(datos["pred_test"]), width="stretch")
            st.caption(
                "Cada punto es un municipio-año de prueba. La diagonal es la predicción perfecta; "
                "la nube se comprime hacia el centro: el modelo suaviza los extremos."
            )
        with col_der:
            st.plotly_chart(grafico_pronostico(datos["predicciones"]), width="stretch")
            st.caption(
                "Las barras de error usan el MAE de prueba (±5,26 puntos); no son intervalos de confianza."
            )

        st.markdown("#### Pronóstico 2026")
        pred_mostrar = datos["predicciones"].copy()
        pred_mostrar["Cambio"] = pred_mostrar["cambio_esperado"].map(
            lambda v: ("+" if v > 0 else "") + num(v)
        )
        pred_mostrar = pred_mostrar[
            [
                "municipio",
                "irca_2025",
                "irca_2026_predicho",
                "categoria_predicha",
                "intervalo_inferior",
                "intervalo_superior",
                "Cambio",
            ]
        ].rename(
            columns={
                "municipio": "Municipio",
                "irca_2025": "IRCA 2025",
                "irca_2026_predicho": "IRCA 2026 (escenario)",
                "categoria_predicha": "Categoría pronosticada",
                "intervalo_inferior": "Límite inferior",
                "intervalo_superior": "Límite superior",
            }
        )
        for columna in ["IRCA 2025", "IRCA 2026 (escenario)", "Límite inferior", "Límite superior"]:
            pred_mostrar[columna] = pred_mostrar[columna].map(lambda v: num(v))
        st.dataframe(pred_mostrar, width="stretch", hide_index=True, height=420)
        st.download_button(
            "⬇️ Descargar pronóstico 2026 (CSV)",
            data=datos["predicciones"].to_csv(index=False).encode("utf-8-sig"),
            file_name="pronostico_irca_2026.csv",
            mime="text/csv",
        )

        st.markdown("#### Coeficientes del modelo final")
        coef = datos["coeficientes"].rename(
            columns={
                "variable": "Variable",
                "etiqueta": "Descripción",
                "coeficiente_estandarizado": "Coeficiente estandarizado",
            }
        )
        coef["Coeficiente estandarizado"] = coef["Coeficiente estandarizado"].map(lambda v: num(v, 2))
        st.dataframe(coef, width="stretch", hide_index=True)
        st.caption(
            "Coeficientes sobre variables estandarizadas. Ambos predictores son positivos: un IRCA "
            "alto el año anterior y una media móvil alta se asocian con un IRCA alto en 2026. "
            "La regresión no implica causalidad."
        )

        st.markdown(
            '<div class="hallazgo"><span class="titulo">Prioridades sugeridas</span>'
            "Timbiquí, Caldono, Guapi y Villa Rica concentran el riesgo medio/alto en 2025 y "
            "siguen siendo los primeros lugares del escenario 2026. Caldono es el caso más "
            "llamativo: su IRCA rural 2025 fue <b>67,8</b> frente a <b>18,8</b> urbano "
            "(brecha de <b>49,0</b> puntos). La priorización debe verificarse con datos de campo "
            "y con la autoridad sanitaria, no solo con este modelo.</div>",
            unsafe_allow_html=True,
        )

    # =======================================================================
    # PIE
    # =======================================================================
    st.markdown("---")
    st.markdown(
        f'<div class="footer"><b>Fuente:</b> {FUENTE}<br>'
        "<b>Elaboración:</b> Electiva II – Introducción a la Ciencia de Datos, Fundación "
        "Universitaria de Popayán. Grupo 4 (completar nombres).<br>"
        "<b>Reproducibilidad:</b> el repositorio incluye datos crudos, scripts de limpieza, "
        "análisis y modelo, tablas, figuras y este dashboard. Datos agregados; no contienen "
        "información personal. Las cifras de 2026 son escenarios de un modelo simple y no "
        "comprometen a las autoridades sanitarias.</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
