"""Análisis descriptivo del IRCA en el Cauca y contexto nacional.

Uso:
    python -m src.analysis

Genera:
    reports/tablas/*.csv
    figures/fig_01 ... fig_06, fig_08
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import (  # noqa: E402
    ANIO_ULTIMO,
    CAUCA_MUNICIPIOS,
    CLEAN_CAUCA_DEPARTAMENTO,
    CLEAN_CAUCA_MUNICIPAL,
    CLEAN_NACIONAL_DEPARTAMENTAL_2025,
    CLEAN_NACIONAL_MUNICIPAL_2025,
    COLOR_CAUCA,
    COLOR_NEUTRO,
    COLOR_RURAL,
    COLOR_URBANO,
    DEPARTAMENTOS_VECINOS,
    FIG_BRECHA,
    FIG_CATEGORIAS,
    FIG_CONTEXTO,
    FIG_EVOLUCION,
    FIG_EVOLUCION_MUNICIPAL,
    FIG_HEATMAP,
    FIG_RANKING,
    RISK_COLORS,
    RISK_ORDER,
    TABLA_BRECHA,
    TABLA_BRECHA_ANIO,
    TABLA_CONTEXTO,
    TABLA_CONTEXTO_RESUMEN,
    TABLA_PERSISTENCIA,
    TABLA_RANKING_2025,
    TABLA_RESUMEN_ANUAL,
)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": "--",
        "figure.dpi": 150,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
    }
)

FUENTE = "Fuente: SIVICAP - MinSalud/INS, datos.gov.co (nxt2-39c3). Consulta: 25/11/2026."


# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------
def cargar() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    cauca = pd.read_csv(CLEAN_CAUCA_MUNICIPAL, encoding="utf-8-sig")
    dep = pd.read_csv(CLEAN_CAUCA_DEPARTAMENTO, encoding="utf-8-sig")
    nac_mun = pd.read_csv(CLEAN_NACIONAL_MUNICIPAL_2025, encoding="utf-8-sig")
    nac_dep = pd.read_csv(CLEAN_NACIONAL_DEPARTAMENTAL_2025, encoding="utf-8-sig")
    for df in (cauca, dep, nac_mun, nac_dep):
        df["anio"] = df["anio"].astype(int)
    return cauca, dep, nac_mun, nac_dep


# ---------------------------------------------------------------------------
# Tablas
# ---------------------------------------------------------------------------
def resumen_anual(cauca: pd.DataFrame, dep: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for anio, grupo in cauca.groupby("anio"):
        total = len(grupo)
        conteos = grupo["nivel_riesgo"].value_counts()
        fila = {
            "anio": int(anio),
            "municipios_con_dato": grupo["municipio"].nunique(),
            "irca_promedio": round(grupo["irca"].mean(), 2),
            "irca_mediana": round(grupo["irca"].median(), 2),
            "irca_minimo": round(grupo["irca"].min(), 2),
            "irca_maximo": round(grupo["irca"].max(), 2),
            "pct_sin_riesgo": round(conteos.get("Sin riesgo", 0) / total * 100, 1),
            "pct_riesgo_bajo": round(conteos.get("Riesgo bajo", 0) / total * 100, 1),
            "pct_riesgo_medio": round(conteos.get("Riesgo medio", 0) / total * 100, 1),
            "pct_riesgo_alto": round(conteos.get("Riesgo alto", 0) / total * 100, 1),
            "pct_inviable": round(conteos.get("Inviable sanitariamente", 0) / total * 100, 1),
            "pct_rural_sin_dato": round(grupo["irca_rural"].isna().mean() * 100, 1),
            "municipios_con_brecha": int(grupo["brecha_rural_urbano"].notna().sum()),
            "brecha_promedio": round(grupo["brecha_rural_urbano"].mean(), 2)
            if grupo["brecha_rural_urbano"].notna().any()
            else np.nan,
        }
        fila["pct_riesgo_medio_alto"] = round(
            fila["pct_riesgo_medio"] + fila["pct_riesgo_alto"] + fila["pct_inviable"], 1
        )
        filas.append(fila)

    resumen = pd.DataFrame(filas)
    dep_serie = dep[["anio", "irca", "nivel_riesgo"]].rename(
        columns={"irca": "irca_departamental", "nivel_riesgo": "nivel_riesgo_departamental"}
    )
    dep_serie["anio"] = dep_serie["anio"].astype(int)
    resumen = resumen.merge(dep_serie, on="anio", how="left")
    resumen.to_csv(TABLA_RESUMEN_ANUAL, index=False, encoding="utf-8-sig")
    return resumen


def tabla_brecha(cauca: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ambos = cauca.dropna(subset=["irca_urbano", "irca_rural"]).copy()

    por_municipio = (
        ambos.groupby("municipio")
        .agg(
            anios_con_datos=("anio", "nunique"),
            primer_anio=("anio", "min"),
            ultimo_anio=("anio", "max"),
            irca_urbano_promedio=("irca_urbano", "mean"),
            irca_rural_promedio=("irca_rural", "mean"),
            brecha_promedio=("brecha_rural_urbano", "mean"),
            brecha_maxima=("brecha_rural_urbano", "max"),
            brecha_minima=("brecha_rural_urbano", "min"),
        )
        .reset_index()
    )
    ultimo = (
        ambos.sort_values("anio")
        .groupby("municipio")
        .tail(1)[["municipio", "brecha_rural_urbano"]]
        .rename(columns={"brecha_rural_urbano": "ultima_brecha"})
    )
    por_municipio = por_municipio.merge(ultimo, on="municipio", how="left")
    por_municipio["evidencia_suficiente"] = por_municipio["anios_con_datos"] >= 3
    for col in [
        "irca_urbano_promedio",
        "irca_rural_promedio",
        "brecha_promedio",
        "brecha_maxima",
        "brecha_minima",
        "ultima_brecha",
    ]:
        por_municipio[col] = por_municipio[col].round(2)
    por_municipio = por_municipio.sort_values(
        ["evidencia_suficiente", "brecha_promedio"], ascending=[False, False]
    )
    por_municipio.to_csv(TABLA_BRECHA, index=False, encoding="utf-8-sig")

    por_anio = (
        ambos.groupby("anio")
        .agg(
            observaciones=("municipio", "size"),
            irca_urbano_promedio=("irca_urbano", "mean"),
            irca_rural_promedio=("irca_rural", "mean"),
            brecha_promedio=("brecha_rural_urbano", "mean"),
            brecha_mediana=("brecha_rural_urbano", "median"),
            pct_brecha_positiva=("brecha_rural_urbano", lambda s: (s > 0).mean() * 100),
        )
        .reset_index()
    )
    for col in [
        "irca_urbano_promedio",
        "irca_rural_promedio",
        "brecha_promedio",
        "brecha_mediana",
        "pct_brecha_positiva",
    ]:
        por_anio[col] = por_anio[col].round(2)
    por_anio.to_csv(TABLA_BRECHA_ANIO, index=False, encoding="utf-8-sig")
    return por_municipio, por_anio


def persistencia(cauca: pd.DataFrame) -> pd.DataFrame:
    def racha_maxima(serie: pd.Series) -> int:
        mejor = actual = 0
        for bandera in serie:
            actual = actual + 1 if bandera else 0
            mejor = max(mejor, actual)
        return mejor

    filas = []
    for municipio, grupo in cauca.groupby("municipio"):
        grupo = grupo.sort_values("anio")
        en_riesgo = grupo["nivel_riesgo"].isin(
            ["Riesgo medio", "Riesgo alto", "Inviable sanitariamente"]
        )
        ultimo = grupo.iloc[-1]
        filas.append(
            {
                "municipio": municipio,
                "anios_con_dato": int(grupo["anio"].nunique()),
                "anios_riesgo_medio_alto": int(en_riesgo.sum()),
                "pct_anios_riesgo": round(en_riesgo.mean() * 100, 1),
                "racha_maxima_riesgo": racha_maxima(en_riesgo),
                "primer_anio": int(grupo["anio"].min()),
                "ultimo_anio": int(grupo["anio"].max()),
                "irca_ultimo": round(float(ultimo["irca"]), 2),
                "categoria_ultimo": ultimo["nivel_riesgo"],
            }
        )
    tabla = pd.DataFrame(filas).sort_values(
        ["anios_riesgo_medio_alto", "pct_anios_riesgo"], ascending=False
    )
    tabla.to_csv(TABLA_PERSISTENCIA, index=False, encoding="utf-8-sig")
    return tabla


def ranking_2025(cauca: pd.DataFrame, nac_mun: pd.DataFrame, persist: pd.DataFrame) -> pd.DataFrame:
    actual = cauca[cauca["anio"] == ANIO_ULTIMO].copy()
    valores_nacionales = np.sort(nac_mun["irca"].dropna().values)
    mediana_nacional = float(np.median(valores_nacionales))

    actual["puesto_departamental"] = actual["irca"].rank(
        ascending=False, method="min"
    ).astype(int)
    actual["percentil_nacional"] = actual["irca"].map(
        lambda v: round(float((valores_nacionales <= v).mean() * 100), 1)
    )
    actual["puesto_nacional"] = actual["irca"].map(
        lambda v: int((valores_nacionales > v).sum() + 1)
    )
    actual["mediana_nacional"] = mediana_nacional
    actual["diferencia_vs_mediana_nacional"] = (
        actual["irca"] - mediana_nacional
    ).round(2)
    actual = actual.merge(
        persist[["municipio", "anios_riesgo_medio_alto", "anios_con_dato", "pct_anios_riesgo"]],
        on="municipio",
        how="left",
    )
    columnas = [
        "municipio",
        "codigo_municipio",
        "irca",
        "nivel_riesgo",
        "puesto_departamental",
        "puesto_nacional",
        "percentil_nacional",
        "mediana_nacional",
        "diferencia_vs_mediana_nacional",
        "irca_urbano",
        "irca_rural",
        "brecha_rural_urbano",
        "anios_riesgo_medio_alto",
        "anios_con_dato",
        "pct_anios_riesgo",
    ]
    actual = actual[columnas].sort_values("irca", ascending=False)
    actual.to_csv(TABLA_RANKING_2025, index=False, encoding="utf-8-sig")
    return actual


def contexto_nacional(nac_dep: pd.DataFrame, nac_mun: pd.DataFrame, dep: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    tabla = nac_dep.copy()
    tabla["puesto"] = tabla["irca"].rank(ascending=True, method="min").astype(int)
    tabla["es_cauca"] = tabla["departamento"].eq("Cauca")
    tabla["es_vecino"] = tabla["departamento"].isin(DEPARTAMENTOS_VECINOS)
    tabla["grupo"] = np.select(
        [tabla["es_cauca"], tabla["es_vecino"]],
        ["Cauca", "Vecino"],
        default="Otro",
    )
    mediana_nacional = float(nac_dep["irca"].median())
    tabla["diferencia_vs_mediana"] = (tabla["irca"] - mediana_nacional).round(2)
    tabla = tabla.sort_values("irca")
    tabla.to_csv(TABLA_CONTEXTO, index=False, encoding="utf-8-sig")

    cauca_dep = dep[dep["anio"] == ANIO_ULTIMO].iloc[0]
    cauca_mun = nac_mun[nac_mun["departamento"] == "Cauca"]
    filas = [
        ("Departamentos con dato 2025", str(len(tabla)), "Agregados departamentales #TODOS"),
        ("Municipios con dato 2025", f"{len(nac_mun):,}".replace(",", "."), "Base municipal nacional, sin #TODOS"),
        ("IRCA Cauca 2025", f"{cauca_dep['irca']:.1f}", "Agregado departamental oficial"),
        ("Puesto del Cauca", str(int(tabla.loc[tabla["es_cauca"], "puesto"].iloc[0])), "1 = menor IRCA (mejor)"),
        ("Mediana departamental 2025", f"{mediana_nacional:.1f}", "Mediana de los 33 departamentos"),
        ("IRCA mediano municipal nacional", f"{nac_mun['irca'].median():.1f}", "1.019 municipios"),
        ("IRCA mediano municipal Cauca", f"{cauca_mun['irca'].median():.1f}", f"{len(cauca_mun)} municipios"),
        ("Percentil del municipio mediano del Cauca", f"{(nac_mun['irca'] <= cauca_mun['irca'].median()).mean() * 100:.1f}", "Porcentaje de municipios nacionales con IRCA menor o igual"),
        ("Municipios del Cauca en riesgo medio/alto", str(int(cauca_mun["nivel_riesgo"].isin(["Riesgo medio", "Riesgo alto", "Inviable sanitariamente"]).sum())), "Corte 2025"),
    ]
    resumen = pd.DataFrame(filas, columns=["indicador", "valor", "detalle"])
    resumen.to_csv(TABLA_CONTEXTO_RESUMEN, index=False, encoding="utf-8-sig")
    return tabla, resumen


# ---------------------------------------------------------------------------
# Figuras
# ---------------------------------------------------------------------------
def fig_evolucion(dep: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.2))
    bandas = [
        (0, 5, "#E8F5E9", "Sin riesgo"),
        (5, 14, "#F1F8E9", "Riesgo bajo"),
        (14, 35, "#FFF8E1", "Riesgo medio"),
        (35, 80, "#FBE9E7", "Riesgo alto"),
        (80, 100, "#FFEBEE", "Inviable"),
    ]
    for inicio, fin, color, etiqueta in bandas:
        ax.axhspan(inicio, fin, color=color, zorder=0)
        ax.text(
            2006.7,
            (inicio + fin) / 2,
            etiqueta,
            fontsize=7,
            color="#616161",
            va="center",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.7),
        )

    ax.plot(dep["anio"], dep["irca"], marker="o", color=COLOR_CAUCA, lw=2.4, label="IRCA total")
    ax.plot(dep["anio"], dep["irca_urbano"], marker="s", ms=4, color=COLOR_URBANO, lw=1.4, ls="--", label="Urbano")
    ax.plot(dep["anio"], dep["irca_rural"], marker="^", ms=4, color=COLOR_RURAL, lw=1.4, ls="--", label="Rural")

    for anio in (2007, 2015, 2024, 2025):
        fila = dep[dep["anio"] == anio].iloc[0]
        desplazamiento = -14 if anio in (2024, 2025) else 9
        ax.annotate(
            f"{fila['irca']:.1f}",
            (anio, fila["irca"]),
            textcoords="offset points",
            xytext=(0, desplazamiento),
            ha="center",
            fontsize=8,
            color=COLOR_CAUCA,
            fontweight="bold",
        )

    ax.set_title("Cauca: evolución del IRCA, 2007-2025")
    ax.set_xlabel("Año")
    ax.set_ylabel("IRCA (0-100)")
    ax.set_xlim(2006.5, 2025.5)
    ax.set_ylim(0, 100)
    ax.set_xticks(range(2007, 2026, 2))
    ax.legend(loc="upper right", frameon=True, ncol=3, fontsize=8)
    ax.text(0.01, -0.16, FUENTE, transform=ax.transAxes, fontsize=7, color="#555555")
    fig.savefig(FIG_EVOLUCION)
    plt.close(fig)


def fig_categorias(resumen: pd.DataFrame) -> None:
    columnas = [
        "pct_sin_riesgo",
        "pct_riesgo_bajo",
        "pct_riesgo_medio",
        "pct_riesgo_alto",
        "pct_inviable",
    ]
    datos = resumen.set_index("anio")[columnas]
    datos.columns = RISK_ORDER

    fig, ax = plt.subplots(figsize=(10, 5.2))
    fondo = np.zeros(len(datos))
    for categoria in RISK_ORDER:
        valores = datos[categoria].values
        ax.bar(
            datos.index,
            valores,
            bottom=fondo,
            color=RISK_COLORS[categoria],
            label=categoria,
            width=0.8,
        )
        fondo += valores

    ax.set_title("Cauca: distribución de municipios por categoría de riesgo")
    ax.set_xlabel("Año")
    ax.set_ylabel("Porcentaje de municipios (%)")
    ax.set_ylim(0, 100)
    ax.set_xticks(datos.index[::2])
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=5, fontsize=8, frameon=False)
    ax.text(0.01, -0.24, FUENTE, transform=ax.transAxes, fontsize=7, color="#555555")
    fig.savefig(FIG_CATEGORIAS)
    plt.close(fig)


def fig_ranking(ranking: pd.DataFrame) -> None:
    datos = ranking.sort_values("irca", ascending=True)
    colores = [RISK_COLORS[c] for c in datos["nivel_riesgo"]]
    fig, ax = plt.subplots(figsize=(9, 9.5))
    barras = ax.barh(datos["municipio"], datos["irca"], color=colores, edgecolor="white")
    for barra, valor in zip(barras, datos["irca"]):
        ax.text(valor + 0.6, barra.get_y() + barra.get_height() / 2, f"{valor:.1f}", va="center", fontsize=7)
    ax.set_title("Cauca: IRCA municipal 2025 (38 municipios con dato)")
    ax.set_xlabel("IRCA (0-100)")
    ax.set_xlim(0, max(45, datos["irca"].max() + 6))
    ax.text(0.01, -0.08, FUENTE + "  El ranking no incluye a Popayán, Balboa, Florencia ni López de Micay.", transform=ax.transAxes, fontsize=7, color="#555555")
    fig.savefig(FIG_RANKING)
    plt.close(fig)


def fig_brecha(brecha_municipio: pd.DataFrame) -> None:
    datos = brecha_municipio[brecha_municipio["anios_con_datos"] >= 3].head(15)
    datos = datos.sort_values("brecha_promedio")
    fig, ax = plt.subplots(figsize=(9.5, 6.4))
    y = np.arange(len(datos))
    ax.hlines(y, datos["irca_urbano_promedio"], datos["irca_rural_promedio"], color="#B0BEC5", lw=2)
    ax.scatter(datos["irca_urbano_promedio"], y, color=COLOR_URBANO, s=55, label="Urbano (promedio)", zorder=3)
    ax.scatter(datos["irca_rural_promedio"], y, color=COLOR_RURAL, s=55, label="Rural (promedio)", zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(
        [f"{fila.municipio} ({fila.primer_anio}-{fila.ultimo_anio})" for fila in datos.itertuples()],
        fontsize=7.5,
    )
    ax.set_title("Brecha urbano-rural: municipios con mayor diferencia promedio")
    ax.set_xlabel("IRCA promedio (0-100)")
    ax.legend(loc="lower right", frameon=True)
    ax.text(0.01, -0.12, FUENTE + "  Solo municipios con al menos 3 años de datos urbanos y rurales; los promedios cubren periodos distintos.", transform=ax.transAxes, fontsize=7, color="#555555")
    fig.savefig(FIG_BRECHA)
    plt.close(fig)


def fig_heatmap(cauca: pd.DataFrame) -> None:
    tabla = cauca.pivot_table(index="municipio", columns="anio", values="irca", aggfunc="mean")
    orden = tabla.mean(axis=1).sort_values(ascending=False).index
    tabla = tabla.loc[orden]
    matriz = np.ma.masked_invalid(tabla.values)
    cmap = plt.cm.RdYlGn_r.copy()
    cmap.set_bad("#E0E0E0")

    fig, ax = plt.subplots(figsize=(11, 10))
    imagen = ax.imshow(matriz, aspect="auto", cmap=cmap, vmin=0, vmax=100)
    ax.set_xticks(range(len(tabla.columns)))
    ax.set_xticklabels(tabla.columns, rotation=45, ha="right", fontsize=7)
    ax.set_yticks(range(len(tabla.index)))
    ax.set_yticklabels(tabla.index, fontsize=7)
    ax.set_title("Cauca: IRCA por municipio y año (gris = sin dato)")
    ax.set_xlabel("Año")
    cbar = fig.colorbar(imagen, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("IRCA (0-100)")
    ax.text(0.01, -0.08, FUENTE, transform=ax.transAxes, fontsize=7, color="#555555")
    fig.savefig(FIG_HEATMAP)
    plt.close(fig)


def fig_contexto(contexto: pd.DataFrame, nac_mun: pd.DataFrame) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={"width_ratios": [1.25, 1]})

    datos = contexto.sort_values("irca", ascending=True)
    colores = [
        COLOR_CAUCA if es_cauca else ("#FFB74D" if es_vecino else COLOR_NEUTRO)
        for es_cauca, es_vecino in zip(datos["es_cauca"], datos["es_vecino"])
    ]
    barras = ax1.barh(datos["departamento"], datos["irca"], color=colores, edgecolor="white")
    for barra, valor in zip(barras, datos["irca"]):
        ax1.text(valor + 0.5, barra.get_y() + barra.get_height() / 2, f"{valor:.1f}", va="center", fontsize=7)
    ax1.set_title("Ranking departamental del IRCA, 2025")
    ax1.set_xlabel("IRCA (0-100)")
    ax1.set_xlim(0, max(50, datos["irca"].max() + 8))
    ax1.tick_params(axis="y", labelsize=7)

    ax2.hist(nac_mun["irca"], bins=np.arange(0, 102.5, 2.5), color="#CFD8DC", edgecolor="white")
    mediana_nacional = float(nac_mun["irca"].median())
    mediana_cauca = float(nac_mun.loc[nac_mun["departamento"] == "Cauca", "irca"].median())
    ax2.axvline(mediana_nacional, color="#455A64", lw=2, ls="--", label=f"Mediana nacional: {mediana_nacional:.1f}")
    ax2.axvline(mediana_cauca, color=COLOR_CAUCA, lw=2, label=f"Mediana Cauca: {mediana_cauca:.1f}")
    ax2.set_title("Distribución nacional municipal, 2025")
    ax2.set_xlabel("IRCA (0-100)")
    ax2.set_ylabel("Número de municipios")
    ax2.legend(loc="upper right", fontsize=8, frameon=True)
    ax2.text(
        0.98,
        0.72,
        f"n = {len(nac_mun):,} municipios\nCauca: {int((nac_mun['departamento'] == 'Cauca').sum())} municipios",
        transform=ax2.transAxes,
        ha="right",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", edgecolor="#CFD8DC"),
    )
    fig.suptitle("Contexto nacional del IRCA en 2025", fontsize=14, fontweight="bold")
    fig.text(0.01, 0.01, FUENTE, fontsize=7, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 0.96))
    fig.savefig(FIG_CONTEXTO)
    plt.close(fig)


def fig_evolucion_municipal(cauca: pd.DataFrame, ranking: pd.DataFrame) -> None:
    anios = list(range(2007, 2026))
    fig, ax = plt.subplots(figsize=(10, 5.4))
    for _, grupo in cauca.groupby("municipio"):
        serie = grupo.set_index("anio")["irca"].reindex(anios)
        ax.plot(serie.index, serie.values, color="#B0BEC5", lw=0.8, alpha=0.45)
    destacados = ranking.head(4)["municipio"].tolist()
    colores = ["#C62828", "#EF6C00", "#6A1B9A", "#00695C"]
    for municipio, color in zip(destacados, colores):
        grupo = cauca[cauca["municipio"] == municipio]
        serie = grupo.set_index("anio")["irca"].reindex(anios)
        ax.plot(serie.index, serie.values, color=color, lw=2, label=municipio)
    dep = cauca.groupby("anio")["irca"].mean().reindex(anios)
    ax.plot(dep.index, dep.values, color=COLOR_CAUCA, lw=2.6, label="Promedio municipal")
    ax.set_title("Cauca: trayectorias municipales del IRCA")
    ax.set_xlabel("Año")
    ax.set_ylabel("IRCA (0-100)")
    ax.set_ylim(0, 100)
    ax.set_xticks(range(2007, 2026, 2))
    ax.legend(loc="upper right", fontsize=8, frameon=True)
    ax.text(0.01, -0.14, FUENTE + "  Cada línea gris es un municipio; los huecos indican años sin dato.", transform=ax.transAxes, fontsize=7, color="#555555")
    fig.savefig(FIG_EVOLUCION_MUNICIPAL)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Principal
# ---------------------------------------------------------------------------
def main() -> None:
    print("Cargando datos limpios...")
    cauca, dep, nac_mun, nac_dep = cargar()

    print("Calculando tablas...")
    resumen = resumen_anual(cauca, dep)
    brecha_municipio, brecha_anio = tabla_brecha(cauca)
    persist = persistencia(cauca)
    ranking = ranking_2025(cauca, nac_mun, persist)
    contexto, contexto_resumen = contexto_nacional(nac_dep, nac_mun, dep)

    print("Generando figuras...")
    fig_evolucion(dep)
    fig_categorias(resumen)
    fig_ranking(ranking)
    fig_brecha(brecha_municipio)
    fig_heatmap(cauca)
    fig_contexto(contexto, nac_mun)
    fig_evolucion_municipal(cauca, ranking)

    print("\nResumen de indicadores:")
    fila_2025 = dep[dep["anio"] == 2025].iloc[0]
    print(f"  Cauca 2025: {fila_2025['irca']} ({fila_2025['nivel_riesgo']})")
    print(f"  Municipios con dato 2025: {len(ranking)}")
    en_riesgo = int(ranking["nivel_riesgo"].isin(["Riesgo medio", "Riesgo alto"]).sum())
    print(f"  En riesgo medio/alto 2025: {en_riesgo}")
    ambos = cauca.dropna(subset=["irca_urbano", "irca_rural"])
    print(f"  Brecha promedio (n={len(ambos)}): {ambos['brecha_rural_urbano'].mean():.1f} puntos")
    print(f"  Registros con dato rural: {len(cauca) - cauca['irca_rural'].isna().sum()} de {len(cauca)}")
    print(f"  Puesto del Cauca: {contexto.loc[contexto['es_cauca'], 'puesto'].iloc[0]} de {len(contexto)}")
    print("\nTablas y figuras generadas.")


if __name__ == "__main__":
    main()
