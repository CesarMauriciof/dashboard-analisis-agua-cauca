"""Modelo predictivo simple para el IRCA municipal del Cauca.

Objetivo:
    Pronosticar el IRCA 2026 de cada municipio con datos 2025, usando
    únicamente información de años anteriores (sin fuga de información).

Decisión de modelado:
    Se comparan un pronóstico ingenuo, la media histórica, una regresión
    lineal simple (último valor + media móvil), una regresión completa y
    un Random Forest. Para el pronóstico final se elige la regresión
    simple por parsimonia y estabilidad: su MAE es prácticamente igual
    al de la regresión completa y produce escenarios menos agresivos.

Uso:
    python -m src.model

Salidas:
    reports/tablas/metricas_modelo.csv
    reports/tablas/coeficientes_modelo.csv
    reports/tablas/predicciones_2026.csv
    reports/tablas/predicciones_test.csv
    figures/fig_07_modelo.png
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import (  # noqa: E402
    CLEAN_CAUCA_MUNICIPAL,
    FIG_MODELO,
    RISK_COLORS,
    TABLA_METRICAS,
    TABLA_PREDICCIONES,
    TABLES,
)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": "--",
        "figure.dpi": 150,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
    }
)

FUENTE = "Fuente: SIVICAP - MinSalud/INS, datos.gov.co (nxt2-39c3). Consulta: 25/11/2026."

FEATURES_COMPLETO = [
    "irca_lag1",
    "irca_lag2",
    "irca_roll3",
    "irca_urbano_lag1",
    "anios_en_riesgo_prev",
    "irca_mean_prev",
    "tendencia_3",
    "reporta_rural_prev",
]
FEATURES_SIMPLE = ["irca_lag1", "irca_roll3"]

ETIQUETAS = {
    "irca_lag1": "IRCA del año anterior",
    "irca_lag2": "IRCA de hace 2 años",
    "irca_roll3": "Media móvil de 3 años",
    "irca_urbano_lag1": "IRCA urbano del año anterior",
    "anios_en_riesgo_prev": "Años históricos en riesgo",
    "irca_mean_prev": "IRCA promedio histórico",
    "tendencia_3": "Cambio en 3 años",
    "reporta_rural_prev": "Reporta dato rural",
}

RIESGO_MEDIO_ALTO = ["Riesgo medio", "Riesgo alto", "Inviable sanitariamente"]
MODELO_FINAL = "Regresión lineal simple"


# ---------------------------------------------------------------------------
# Preparación del panel
# ---------------------------------------------------------------------------
def preparar_panel(cauca: pd.DataFrame) -> pd.DataFrame:
    """Construye un panel anual completo (2007-2026) por municipio.

    Así los rezagos son temporales (año calendario) y no de fila. Si un
    municipio no reportó un año, el rezago queda nulo en lugar de tomar un
    dato antiguo como si fuera del año inmediatamente anterior.
    """
    municipios = cauca[
        ["codigo_departamento", "departamento", "codigo_municipio", "municipio"]
    ].drop_duplicates()
    anios = pd.DataFrame({"anio": range(2007, 2027)})
    grilla = municipios.merge(anios, how="cross")

    df = grilla.merge(
        cauca,
        on=[
            "codigo_departamento",
            "departamento",
            "codigo_municipio",
            "municipio",
            "anio",
        ],
        how="left",
    ).sort_values(["municipio", "anio"])
    grupo = df.groupby("municipio", group_keys=False)

    df["irca_lag1"] = grupo["irca"].shift(1)
    df["irca_lag2"] = grupo["irca"].shift(2)
    df["irca_lag3"] = grupo["irca"].shift(3)
    df["irca_roll3"] = grupo["irca"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=2).mean()
    )
    df["irca_urbano_lag1"] = grupo["irca_urbano"].shift(1)
    df["reporta_rural_prev"] = grupo["irca_rural"].shift(1).notna().astype(int)
    df["anios_en_riesgo_prev"] = grupo["nivel_riesgo"].transform(
        lambda s: s.isin(RIESGO_MEDIO_ALTO).cumsum().shift(1)
    ).fillna(0)
    df["irca_mean_prev"] = grupo["irca"].transform(
        lambda s: s.expanding().mean().shift(1)
    )
    df["tendencia_3"] = df["irca_lag1"] - df["irca_lag3"]
    return df


def construir_futuro(cauca: pd.DataFrame) -> pd.DataFrame:
    """Toma las filas 2026 del panel y rellena solo los casos incompletos."""
    panel = preparar_panel(cauca)
    futuro = panel[(panel["anio"] == 2026) & (panel["irca_lag1"].notna())].copy()

    # Rellenos transparentes para municipios con series incompletas.
    futuro["irca_lag2"] = futuro["irca_lag2"].fillna(futuro["irca_lag1"])
    futuro["irca_roll3"] = futuro["irca_roll3"].fillna(futuro["irca_lag1"])
    futuro["irca_urbano_lag1"] = futuro["irca_urbano_lag1"].fillna(futuro["irca_lag1"])
    futuro["tendencia_3"] = futuro["tendencia_3"].fillna(0)
    futuro["irca_mean_prev"] = futuro["irca_mean_prev"].fillna(futuro["irca_lag1"])
    futuro["anios_en_riesgo_prev"] = futuro["anios_en_riesgo_prev"].fillna(0)
    return futuro


# ---------------------------------------------------------------------------
# Métricas
# ---------------------------------------------------------------------------
def calcular_metricas(y_real: pd.Series, y_pred: np.ndarray) -> dict:
    y_real = np.asarray(y_real, dtype=float)
    y_pred = np.clip(np.asarray(y_pred, dtype=float), 0, 100)
    mascara = y_real != 0
    mape = (
        float(np.mean(np.abs((y_real[mascara] - y_pred[mascara]) / y_real[mascara])) * 100)
        if mascara.any()
        else np.nan
    )
    return {
        "n": int(len(y_real)),
        "mae": round(float(mean_absolute_error(y_real, y_pred)), 2),
        "rmse": round(float(root_mean_squared_error(y_real, y_pred)), 2),
        "r2": round(float(r2_score(y_real, y_pred)), 3),
        "mape": round(mape, 1) if not np.isnan(mape) else np.nan,
    }


def categoria(valor: float) -> str:
    if valor <= 5:
        return "Sin riesgo"
    if valor <= 14:
        return "Riesgo bajo"
    if valor <= 35:
        return "Riesgo medio"
    if valor <= 80:
        return "Riesgo alto"
    return "Inviable sanitariamente"


# ---------------------------------------------------------------------------
# Principal
# ---------------------------------------------------------------------------
def main() -> None:
    cauca = pd.read_csv(CLEAN_CAUCA_MUNICIPAL, encoding="utf-8-sig")
    cauca["anio"] = cauca["anio"].astype(int)

    print("Preparando panel...")
    panel = preparar_panel(cauca)
    datos = panel.dropna(subset=["irca"] + FEATURES_COMPLETO).copy()
    train = datos[datos["anio"] <= 2021]
    test = datos[datos["anio"] >= 2022]
    print(f"  Filas con variables completas: {len(datos)}")
    print(f"  Entrenamiento (<=2021): {len(train)} | Prueba (>=2022): {len(test)}")

    modelo_simple = Pipeline(
        [("escalador", StandardScaler()), ("modelo", LinearRegression())]
    )
    modelo_completo = Pipeline(
        [("escalador", StandardScaler()), ("modelo", LinearRegression())]
    )
    modelo_rf = RandomForestRegressor(
        n_estimators=500,
        max_depth=4,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    )

    candidatos = {
        "Naive (último valor)": (None, []),
        "Media histórica municipal": (None, []),
        MODELO_FINAL: (modelo_simple, FEATURES_SIMPLE),
        "Regresión lineal completa": (modelo_completo, FEATURES_COMPLETO),
        "Random Forest": (modelo_rf, FEATURES_COMPLETO),
    }

    metricas = []
    predicciones_test = {}

    for nombre, (modelo, features) in candidatos.items():
        if nombre == "Naive (último valor)":
            pred_test = test["irca_lag1"].to_numpy()
            pred_train = None
        elif nombre == "Media histórica municipal":
            pred_test = test["irca_mean_prev"].to_numpy()
            pred_train = None
        else:
            modelo.fit(train[features], train["irca"])
            pred_test = modelo.predict(test[features])
            pred_train = modelo.predict(train[features])

        predicciones_test[nombre] = np.clip(pred_test, 0, 100)
        fila = {"modelo": nombre, "conjunto": "Prueba (2022-2025)"}
        fila.update(calcular_metricas(test["irca"], pred_test))
        metricas.append(fila)

        if pred_train is not None:
            fila_train = {"modelo": nombre, "conjunto": "Entrenamiento (<=2021)"}
            fila_train.update(calcular_metricas(train["irca"], pred_train))
            metricas.append(fila_train)

    tabla_metricas = pd.DataFrame(metricas)
    prueba = tabla_metricas[tabla_metricas["conjunto"] == "Prueba (2022-2025)"]
    print("\nMétricas de prueba:")
    print(prueba[["modelo", "n", "mae", "rmse", "r2", "mape"]].to_string(index=False))

    # Predicciones de prueba en formato largo (para el dashboard y el informe)
    filas_test = []
    for nombre, pred in predicciones_test.items():
        for (_, fila), valor in zip(test.iterrows(), pred):
            filas_test.append(
                {
                    "modelo": nombre,
                    "municipio": fila["municipio"],
                    "anio": int(fila["anio"]),
                    "irca_real": round(float(fila["irca"]), 2),
                    "irca_predicho": round(float(valor), 2),
                }
            )
    pd.DataFrame(filas_test).to_csv(
        TABLES / "predicciones_test.csv", index=False, encoding="utf-8-sig"
    )

    fila_final = prueba[prueba["modelo"] == MODELO_FINAL].iloc[0]
    mae_final = float(fila_final["mae"])
    print(f"\nModelo final: {MODELO_FINAL} (MAE={mae_final:.2f})")
    print("Criterio: parsimonia y estabilidad; el modelo completo mejora el MAE solo marginalmente.")

    tabla_metricas.to_csv(TABLA_METRICAS, index=False, encoding="utf-8-sig")

    # Coeficientes del modelo final (sobre variables estandarizadas)
    modelo_simple.fit(datos[FEATURES_SIMPLE], datos["irca"])
    coeficientes = pd.DataFrame(
        {
            "variable": FEATURES_SIMPLE,
            "etiqueta": [ETIQUETAS[v] for v in FEATURES_SIMPLE],
            "coeficiente_estandarizado": np.round(
                modelo_simple.named_steps["modelo"].coef_, 4
            ),
        }
    )
    coeficientes.to_csv(
        TABLES / "coeficientes_modelo.csv", index=False, encoding="utf-8-sig"
    )
    print("\nCoeficientes del modelo final:")
    print(coeficientes.to_string(index=False))

    # Pronóstico 2026
    print("\nConstruyendo pronóstico 2026...")
    futuro = construir_futuro(cauca)
    futuro["irca_predicho"] = modelo_simple.predict(futuro[FEATURES_SIMPLE]).clip(0, 100)
    futuro["categoria_predicha"] = futuro["irca_predicho"].map(categoria)
    futuro["intervalo_inferior"] = (futuro["irca_predicho"] - mae_final).clip(0, 100)
    futuro["intervalo_superior"] = (futuro["irca_predicho"] + mae_final).clip(0, 100)
    futuro["cambio_esperado"] = (futuro["irca_predicho"] - futuro["irca_lag1"]).round(2)

    predicciones = futuro[
        [
            "municipio",
            "irca_lag1",
            "irca_roll3",
            "irca_predicho",
            "categoria_predicha",
            "intervalo_inferior",
            "intervalo_superior",
            "cambio_esperado",
        ]
    ].rename(
        columns={
            "irca_lag1": "irca_2025",
            "irca_roll3": "promedio_2023_2025",
            "irca_predicho": "irca_2026_predicho",
        }
    )
    predicciones["modelo_usado"] = MODELO_FINAL
    predicciones["mae_prueba"] = mae_final
    predicciones = predicciones.sort_values("irca_2026_predicho", ascending=False)
    for col in [
        "irca_2025",
        "promedio_2023_2025",
        "irca_2026_predicho",
        "intervalo_inferior",
        "intervalo_superior",
    ]:
        predicciones[col] = predicciones[col].round(2)
    predicciones.to_csv(TABLA_PREDICCIONES, index=False, encoding="utf-8-sig")

    # Figura
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1, 1.15]}
    )

    pred_final = predicciones_test[MODELO_FINAL]
    dispersion = ax1.scatter(
        test["irca"],
        pred_final,
        c=test["anio"].values,
        cmap="viridis",
        s=32,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.4,
    )
    ax1.plot([0, 100], [0, 100], color="#455A64", ls="--", lw=1.5, label="Predicción perfecta")
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 100)
    ax1.set_xlabel("IRCA observado")
    ax1.set_ylabel("IRCA predicho")
    ax1.set_title("Prueba 2022-2025: regresión lineal simple")
    ax1.text(
        0.04,
        0.94,
        f"MAE = {mae_final:.2f}\nn = {len(test)}",
        transform=ax1.transAxes,
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", edgecolor="#CFD8DC"),
    )
    ax1.legend(loc="lower right", fontsize=8)
    cbar = fig.colorbar(dispersion, ax=ax1, shrink=0.75, pad=0.02)
    cbar.set_label("Año")

    orden = predicciones.sort_values("irca_2026_predicho")
    colores = [RISK_COLORS[c] for c in orden["categoria_predicha"]]
    ax2.barh(orden["municipio"], orden["irca_2026_predicho"], color=colores, edgecolor="white")
    ax2.errorbar(
        orden["irca_2026_predicho"],
        orden["municipio"],
        xerr=mae_final,
        fmt="none",
        ecolor="#37474F",
        elinewidth=1,
        capsize=2,
    )
    ax2.axvline(14, color="#EF6C00", ls="--", lw=1, label="Umbral riesgo medio (14)")
    ax2.set_title("Pronóstico IRCA 2026 (escenario)")
    ax2.set_xlabel("IRCA (0-100)")
    ax2.set_xlim(0, max(45, orden["irca_2026_predicho"].max() + 10))
    ax2.tick_params(axis="y", labelsize=6.5)
    ax2.legend(loc="lower right", fontsize=8)

    fig.suptitle("Modelo predictivo del IRCA municipal", fontsize=14, fontweight="bold")
    fig.text(
        0.01,
        0.01,
        FUENTE + "  Las barras de error usan el MAE de prueba; no son intervalos de confianza.",
        fontsize=7,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.savefig(FIG_MODELO)
    plt.close(fig)

    print("\nPronóstico 2026 (primeros 10):")
    print(
        predicciones.head(10)[
            ["municipio", "irca_2025", "irca_2026_predicho", "categoria_predicha", "cambio_esperado"]
        ].to_string(index=False)
    )
    print("\nArchivos generados: metricas_modelo.csv, predicciones_2026.csv, fig_07_modelo.png")


if __name__ == "__main__":
    main()
