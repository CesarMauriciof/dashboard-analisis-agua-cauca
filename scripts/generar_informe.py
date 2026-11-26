"""Genera el informe final en PDF (máximo 3 páginas) y su versión Markdown.

Uso:
    python scripts/generar_informe.py

Salidas:
    reports/informe_final.pdf
    reports/informe_final.md
    reports/capturas/informe_pagina_1.png ... (para revisión visual)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.font_manager as fm
import pandas as pd
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image as RLImage,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE = Path(__file__).resolve().parents[1]
REPORTS = BASE / "reports"
CAPTURAS = REPORTS / "capturas"
CAPTURAS.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Fuentes y colores
# ---------------------------------------------------------------------------
fuente_regular = Path(fm.findfont("DejaVu Sans"))
carpeta_fuentes = fuente_regular.parent
pdfmetrics.registerFont(TTFont("DejaVu", str(carpeta_fuentes / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(carpeta_fuentes / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Oblique", str(carpeta_fuentes / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-BoldOblique", str(carpeta_fuentes / "DejaVuSans-BoldOblique.ttf")))
pdfmetrics.registerFontFamily(
    "DejaVu",
    normal="DejaVu",
    bold="DejaVu-Bold",
    italic="DejaVu-Oblique",
    boldItalic="DejaVu-BoldOblique",
)

AZUL_OSCURO = colors.HexColor("#0D2B45")
AZUL = colors.HexColor("#1565C0")
AZUL_CLARO = colors.HexColor("#90CAF9")
GRIS = colors.HexColor("#5A6B7B")
GRIS_CLARO = colors.HexColor("#D9E2EC")
FONDO = colors.HexColor("#F7F9FC")
BLANCO = colors.white
AMBAR = colors.HexColor("#FFB300")

# ---------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------
estilo_titulo = ParagraphStyle(
    "titulo", fontName="DejaVu-Bold", fontSize=17, leading=20, textColor=BLANCO
)
estilo_subtitulo = ParagraphStyle(
    "subtitulo",
    fontName="DejaVu",
    fontSize=10.5,
    leading=13,
    textColor=colors.HexColor("#D6E4F0"),
)
estilo_meta = ParagraphStyle(
    "meta", fontName="DejaVu", fontSize=8, leading=10, textColor=colors.HexColor("#B0C4D8")
)
estilo_h1 = ParagraphStyle(
    "h1",
    fontName="DejaVu-Bold",
    fontSize=11.5,
    leading=13.5,
    textColor=AZUL_OSCURO,
    spaceBefore=6,
    spaceAfter=3,
)
estilo_h2 = ParagraphStyle(
    "h2",
    fontName="DejaVu-Bold",
    fontSize=9.8,
    leading=11.8,
    textColor=AZUL,
    spaceBefore=5,
    spaceAfter=2,
)
estilo_body = ParagraphStyle(
    "body",
    fontName="DejaVu",
    fontSize=8.4,
    leading=10.5,
    textColor=colors.HexColor("#1F2933"),
    alignment=TA_JUSTIFY,
    spaceAfter=3,
)
estilo_caja = ParagraphStyle(
    "caja",
    parent=estilo_body,
    fontSize=8.2,
    leading=10.2,
    leftIndent=2,
)
estilo_caption = ParagraphStyle(
    "caption",
    fontName="DejaVu-Oblique",
    fontSize=7.1,
    leading=8.7,
    textColor=GRIS,
    alignment=TA_LEFT,
    spaceBefore=2,
    spaceAfter=4,
)
estilo_celda = ParagraphStyle(
    "celda", fontName="DejaVu", fontSize=7.0, leading=8.4, textColor=colors.HexColor("#1F2933")
)
estilo_celda_der = ParagraphStyle("celda_der", parent=estilo_celda, alignment=TA_RIGHT)
estilo_celda_cen = ParagraphStyle("celda_cen", parent=estilo_celda, alignment=TA_CENTER)
estilo_header = ParagraphStyle(
    "header", fontName="DejaVu-Bold", fontSize=7.0, leading=8.4, textColor=BLANCO
)
estilo_header_der = ParagraphStyle("header_der", parent=estilo_header, alignment=TA_RIGHT)
estilo_header_cen = ParagraphStyle("header_cen", parent=estilo_header, alignment=TA_CENTER)

# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------
cauca = pd.read_csv(BASE / "data/clean/irca_cauca_municipal.csv", encoding="utf-8-sig")
dep = pd.read_csv(BASE / "data/clean/irca_cauca_departamento.csv", encoding="utf-8-sig")
nac_mun = pd.read_csv(BASE / "data/clean/irca_nacional_municipal_2025.csv", encoding="utf-8-sig")
ranking = pd.read_csv(BASE / "reports/tablas/ranking_2025.csv", encoding="utf-8-sig")
contexto = pd.read_csv(BASE / "reports/tablas/contexto_nacional_2025.csv", encoding="utf-8-sig")
brecha_mun = pd.read_csv(BASE / "reports/tablas/brecha_urbano_rural.csv", encoding="utf-8-sig")
metricas = pd.read_csv(BASE / "reports/tablas/metricas_modelo.csv", encoding="utf-8-sig")
pred = pd.read_csv(BASE / "reports/tablas/predicciones_2026.csv", encoding="utf-8-sig")
for df in (cauca, dep, nac_mun, ranking, contexto, brecha_mun, pred):
    if "anio" in df.columns:
        df["anio"] = df["anio"].astype(int)

dep_2007 = dep[dep["anio"] == 2007].iloc[0]
dep_2015 = dep[dep["anio"] == 2015].iloc[0]
dep_2024 = dep[dep["anio"] == 2024].iloc[0]
dep_2025 = dep[dep["anio"] == 2025].iloc[0]
mun_2025 = cauca[cauca["anio"] == 2025]
ambos = cauca.dropna(subset=["irca_urbano", "irca_rural"])
gap_2025 = mun_2025["brecha_rural_urbano"].dropna()
n_2025 = len(ranking)
riesgo_2025 = int(ranking["nivel_riesgo"].isin(["Riesgo medio", "Riesgo alto"]).sum())
zeros_2025 = int((mun_2025["irca"] == 0).sum())
faltan_2025 = sorted(set(cauca["municipio"]) - set(mun_2025["municipio"]))
popayan_anios = cauca.loc[cauca["municipio"] == "Popayán", "anio"]
mediana_dep = float(contexto["irca"].median())
mediana_nac = float(nac_mun["irca"].median())
mediana_cauca = float(mun_2025["irca"].median())
percentil_mediana = float((nac_mun["irca"] <= mediana_cauca).mean() * 100)
cauca_ctx = contexto[contexto["es_cauca"]].iloc[0]
puesto_cauca = int(cauca_ctx["puesto"])
vecinos = contexto[
    contexto["departamento"].isin(
        ["Cauca", "Valle del Cauca", "Huila", "Caquetá", "Putumayo", "Nariño"]
    )
].sort_values("irca")
top4 = ranking.head(4)
metricas_test = metricas[metricas["conjunto"] == "Prueba (2022-2025)"].copy()
final = metricas_test[metricas_test["modelo"] == "Regresión lineal simple"].iloc[0]
naive = metricas_test[metricas_test["modelo"] == "Naive (último valor)"].iloc[0]
completa = metricas_test[metricas_test["modelo"] == "Regresión lineal completa"].iloc[0]
rf = metricas_test[metricas_test["modelo"] == "Random Forest"].iloc[0]
train_simple = metricas[
    (metricas["modelo"] == "Regresión lineal simple")
    & (metricas["conjunto"] == "Entrenamiento (<=2021)")
].iloc[0]
pred_top4 = pred.head(4)
conteo_pred = pred["categoria_predicha"].value_counts()
brecha_top = brecha_mun[brecha_mun["evidencia_suficiente"]].head(5)
caldono_brecha_prom = float(
    brecha_mun.loc[brecha_mun["municipio"] == "Caldono", "brecha_promedio"].iloc[0]
)


def f(valor, dec: int = 1) -> str:
    if pd.isna(valor):
        return "—"
    texto = f"{float(valor):,.{dec}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def img(path: Path, ancho: float, caption: str):
    with PILImage.open(path) as im:
        w, h = im.size
    return KeepTogether(
        [
            RLImage(str(path), width=ancho, height=ancho * h / w),
            Paragraph(caption, estilo_caption),
        ]
    )


def tabla(datos: list[list[str]], anchos: list[float], alineaciones: list[str] | None = None):
    filas = []
    for i, fila in enumerate(datos):
        celdas = []
        for j, valor in enumerate(fila):
            if i == 0:
                if alineaciones and alineaciones[j] == "R":
                    estilo = estilo_header_der
                elif alineaciones and alineaciones[j] == "C":
                    estilo = estilo_header_cen
                else:
                    estilo = estilo_header
            else:
                if alineaciones and alineaciones[j] == "R":
                    estilo = estilo_celda_der
                elif alineaciones and alineaciones[j] == "C":
                    estilo = estilo_celda_cen
                else:
                    estilo = estilo_celda
            celdas.append(Paragraph(str(valor), estilo))
        filas.append(celdas)
    t = Table(filas, colWidths=anchos, repeatRows=1, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), AZUL_OSCURO),
                ("BACKGROUND", (0, 1), (-1, -1), BLANCO),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLANCO, FONDO]),
                ("GRID", (0, 0), (-1, -1), 0.25, GRIS_CLARO),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, AMBAR),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def caja_hallazgos(items: list[str]):
    texto = "<br/>".join(f"• {item}" for item in items)
    t = Table([[Paragraph(texto, estilo_caja)]], colWidths=[7.0 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F6FB")),
                ("BOX", (0, 0), (-1, -1), 0.6, AZUL_CLARO),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def encabezado():
    t = Table(
        [
            [Paragraph("Calidad del agua para consumo humano en el Cauca", estilo_titulo)],
            [
                Paragraph(
                    "Análisis del IRCA 2007–2025, contexto nacional y pronóstico 2026",
                    estilo_subtitulo,
                )
            ],
            [
                Paragraph(
                    "Electiva II – Introducción a la Ciencia de Datos · Fundación Universitaria de "
                    "Popayán · Grupo 4 · 25 de noviembre de 2026",
                    estilo_meta,
                )
            ],
        ],
        colWidths=[7.0 * inch],
    )
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), AZUL_OSCURO),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, -1), (-1, -1), 3, AMBAR),
            ]
        )
    )
    return t


# ---------------------------------------------------------------------------
# Textos
# ---------------------------------------------------------------------------
resumen = (
    f"Se analizó el Índice de Riesgo de la Calidad del Agua (IRCA) en los 42 municipios del Cauca "
    f"entre 2007 y 2025, con datos abiertos del SIVICAP (MinSalud/INS). El IRCA departamental cayó "
    f"de <b>{f(dep_2007['irca'])}</b> en 2007 a <b>{f(dep_2024['irca'])}</b> en 2024, pero subió a "
    f"<b>{f(dep_2025['irca'])}</b> en 2025 (riesgo bajo). En 2025, <b>{riesgo_2025} de {n_2025}</b> "
    f"municipios con dato están en riesgo medio/alto: Timbiquí ({f(top4.iloc[0]['irca'])}), Caldono "
    f"({f(top4.iloc[1]['irca'])}), Guapi ({f(top4.iloc[2]['irca'])}) y Villa Rica "
    f"({f(top4.iloc[3]['irca'])}). La brecha rural promedia <b>{f(ambos['brecha_rural_urbano'].mean())} "
    f"puntos</b>, aunque <b>{f(cauca['irca_rural'].isna().mean() * 100)}%</b> de los registros no "
    f"tienen dato rural. El Cauca ocupa el puesto <b>{puesto_cauca} de 33</b> departamentos. Un modelo "
    f"lineal simple (IRCA del año anterior + media móvil de 3 años) obtiene un MAE de "
    f"<b>{f(final['mae'])} puntos</b> en prueba (2022–2025), solo {f(naive['mae'] - final['mae'], 2)} "
    f"mejor que el naive, con R² de {f(final['r2'], 2)}; los pronósticos 2026 son escenarios, no certezas."
)

introduccion = (
    "El acceso a agua segura es un determinante de la salud pública. En Colombia, el IRCA resume el "
    "riesgo de la calidad del agua para consumo humano en una escala de 0 a 100 (menor es mejor) y se "
    "clasifica en sin riesgo (0–5), riesgo bajo (5,1–14), medio (14,1–35), alto (35,1–80) e inviable "
    "(80,1–100), conforme al Decreto 1575 de 2007 y la Resolución 2115 de 2007. El Cauca combina alta "
    "ruralidad, dispersión territorial y brechas históricas de servicios públicos; sin embargo, los "
    "análisis suelen quedarse en promedios departamentales. Este trabajo responde cuatro preguntas: "
    "¿cómo evolucionó el IRCA?, ¿qué municipios concentran el riesgo?, ¿qué tan grande es la brecha "
    "urbano-rural?, ¿cómo se compara el Cauca con el país y qué se puede anticipar para 2026?"
)

metodologia = (
    f"Se usó el conjunto <b>nxt2-39c3</b> de datos.gov.co (SIVICAP, MinSalud/INS), actualizado el "
    f"04/11/2026 y consultado el 25/11/2026. La base contiene 20.212 registros nacionales; para el "
    f"Cauca se conservaron <b>736 registros municipales</b> (42 municipios, 2007–2025) y 19 filas "
    f"agregadas <b>#TODOS</b>, separadas para evitar doble conteo. El corte nacional 2025 incluye "
    f"1.019 municipios y 33 departamentos. Los valores <b>ND</b> se convirtieron en nulos y no se "
    f"imputaron; las variantes <i>Bajo riesgo</i>/<i>Alto riesgo</i> se unificaron; se validó el rango "
    f"0–100 y la categoría reportada contra la calculada. La auditoría no encontró duplicados exactos "
    f"ni duplicados municipio-año, pero sí 5 datos urbanos nulos, <b>489 rurales nulos (66,4%)</b>, 336 "
    f"etiquetas normalizadas, 52 ceros y 4 cienes. El análisis descriptivo usa la serie departamental, "
    f"el ranking municipal 2025, la brecha rural-urbano (solo casos completos) y el contexto nacional. "
    f"El modelo se entrenó con datos hasta 2021 (<b>463 observaciones</b>) y se evaluó en 2022–2025 "
    f"(<b>127</b>), sin fuga temporal. Se compararon naive, media histórica, regresión simple "
    f"(<b>irca_lag1</b> + <b>irca_roll3</b>), regresión completa (8 variables) y Random Forest; se eligió "
    f"la regresión simple por parsimonia y estabilidad. El pronóstico 2026 usa una banda ±MAE, que no "
    f"es un intervalo de confianza."
)

hallazgos = [
    f"<b>Mejora con rebote:</b> {f(dep_2007['irca'])} (2007) → {f(dep_2015['irca'])} (2015) → "
    f"{f(dep_2024['irca'])} (2024) → <b>{f(dep_2025['irca'])}</b> (2025). El aumento de 2025 es de "
    f"{f(dep_2025['irca'] - dep_2024['irca'])} puntos.",
    f"<b>Riesgo concentrado:</b> {riesgo_2025} de {n_2025} municipios en riesgo medio/alto "
    f"({f(riesgo_2025 / n_2025 * 100)}%): Timbiquí {f(top4.iloc[0]['irca'])}, Caldono "
    f"{f(top4.iloc[1]['irca'])}, Guapi {f(top4.iloc[2]['irca'])} y Villa Rica {f(top4.iloc[3]['irca'])}.",
    f"<b>Brecha rural subreportada:</b> promedio {f(ambos['brecha_rural_urbano'].mean())} puntos y "
    f"mediana {f(ambos['brecha_rural_urbano'].median())}; {f(cauca['irca_rural'].isna().mean() * 100)}% "
    f"de los registros no tienen IRCA rural.",
    f"<b>Contexto nacional:</b> puesto {puesto_cauca} de 33; mediana departamental {f(mediana_dep)}, "
    f"mediana municipal nacional {f(mediana_nac)} y mediana del Cauca {f(mediana_cauca)} "
    f"(percentil {f(percentil_mediana)}).",
]

evolucion = (
    f"El IRCA departamental pasó de <b>{f(dep_2007['irca'])}</b> en 2007 a <b>{f(dep_2015['irca'])}</b> "
    f"en 2015 y a <b>{f(dep_2024['irca'])}</b> en 2024; en 2025 subió a <b>{f(dep_2025['irca'])}</b> "
    f"(riesgo bajo), un aumento de {f(dep_2025['irca'] - dep_2024['irca'])} puntos. La serie urbana "
    f"({f(dep_2025['irca_urbano'])}) y rural ({f(dep_2025['irca_rural'])}) de 2025 muestra una brecha "
    f"de {f(dep_2025['irca_rural'] - dep_2025['irca_urbano'])} puntos, pero la rural tiene menos datos y "
    f"más volatilidad. La caída de 2024 y el rebote de 2025 coinciden con ceros y saltos abruptos en "
    f"varios municipios, lo que sugiere cambios de reporte además de cambios reales."
)

ranking_txt = (
    f"De los <b>{n_2025}</b> municipios con dato, 18 están sin riesgo, 16 en riesgo bajo, 2 en riesgo "
    f"medio y 2 en riesgo alto; <b>{riesgo_2025} ({f(riesgo_2025 / n_2025 * 100)}%)</b> concentran el "
    f"riesgo medio/alto. Timbiquí ({f(top4.iloc[0]['irca'])}) y Caldono ({f(top4.iloc[1]['irca'])}) "
    f"están en riesgo alto; Guapi ({f(top4.iloc[2]['irca'])}) y Villa Rica ({f(top4.iloc[3]['irca'])}) "
    f"en riesgo medio. Timbiquí, Guapi y Villa Rica solo reportan IRCA urbano; Caldono reporta urbano "
    f"{f(top4.iloc[1]['irca_urbano'])} y rural {f(top4.iloc[1]['irca_rural'])}, la brecha más alta de "
    f"2025 ({f(top4.iloc[1]['brecha_rural_urbano'])}). <b>{zeros_2025}</b> municipios reportan IRCA 0 y "
    f"<b>{len(faltan_2025)}</b> no tienen dato (Balboa, Florencia, López de Micay y Popayán), lo que "
    f"exige cautela."
)

contexto_txt = (
    f"El Cauca ocupa el puesto <b>{puesto_cauca} de 33</b> departamentos (1 = menor IRCA), con "
    f"<b>{f(dep_2025['irca'])}</b>; la mediana departamental es <b>{f(mediana_dep)}</b>. La mediana "
    f"municipal nacional es <b>{f(mediana_nac)}</b> y la del Cauca <b>{f(mediana_cauca)}</b>, que "
    f"corresponde al percentil <b>{f(percentil_mediana)}</b>: la mitad de los municipios del país tiene "
    f"un IRCA menor o igual. Entre los vecinos, el Cauca está mejor que Nariño (22,5) y Putumayo "
    f"(17,0), pero peor que Valle del Cauca (4,4), Huila (4,1) y Caquetá (6,7). Timbiquí está en el "
    f"percentil nacional 94,3: solo ~6% de los municipios del país tienen un IRCA peor."
)

brecha_txt = (
    f"En las <b>{len(ambos)}</b> observaciones con ambos datos, la brecha promedio es "
    f"<b>{f(ambos['brecha_rural_urbano'].mean())}</b> puntos, la mediana {f(ambos['brecha_rural_urbano'].median())} "
    f"y el {f((ambos['brecha_rural_urbano'] > 0).mean() * 100)}% son positivas; el máximo es "
    f"{f(ambos['brecha_rural_urbano'].max())} y el mínimo {f(ambos['brecha_rural_urbano'].min())}. La "
    f"diferencia entre media y mediana indica que el promedio está impulsado por casos extremos. Los "
    f"mayores promedios con al menos 3 años de datos son Popayán {f(brecha_top.iloc[0]['brecha_promedio'])} "
    f"(2009–2013), Santa Rosa {f(brecha_top.iloc[1]['brecha_promedio'])} (2010–2012), Caloto "
    f"{f(brecha_top.iloc[2]['brecha_promedio'])} (2010–2015), Páez {f(brecha_top.iloc[3]['brecha_promedio'])} "
    f"(2009–2013) y Rosas {f(brecha_top.iloc[4]['brecha_promedio'])} (2008–2011). En 2025 solo "
    f"<b>{len(gap_2025)} de {n_2025}</b> municipios tienen dato rural; la brecha promedio de ese año es "
    f"{f(gap_2025.mean())}. La falta de dato rural en <b>{f(cauca['irca_rural'].isna().mean() * 100)}%</b> "
    f"de los registros es una limitación central."
)

modelo_txt = (
    f"La regresión simple obtiene <b>MAE {f(final['mae'])}</b>, RMSE {f(final['rmse'])} y R² "
    f"{f(final['r2'], 2)} en prueba; el naive obtiene MAE {f(naive['mae'])}, la regresión completa "
    f"{f(completa['mae'])} (R² {f(completa['r2'], 2)}) y el Random Forest {f(rf['mae'])} (R² "
    f"{f(rf['r2'], 2)}). La mejora sobre el naive es de {f(naive['mae'] - final['mae'], 2)} puntos "
    f"({f((naive['mae'] - final['mae']) / naive['mae'] * 100)}%), modesta. El R² de entrenamiento de la "
    f"regresión simple es {f(train_simple['r2'], 2)}, frente a {f(final['r2'], 2)} en prueba: el modelo "
    f"no generaliza y suaviza los extremos. Para 2026, el escenario proyecta <b>4 municipios en riesgo "
    f"medio</b> (Timbiquí {f(pred_top4.iloc[0]['irca_2026_predicho'])}; Caldono "
    f"{f(pred_top4.iloc[1]['irca_2026_predicho'])}; Guapi {f(pred_top4.iloc[2]['irca_2026_predicho'])}; "
    f"Villa Rica {f(pred_top4.iloc[3]['irca_2026_predicho'])}), <b>{conteo_pred.get('Riesgo bajo', 0)} "
    f"en riesgo bajo</b> y <b>{conteo_pred.get('Sin riesgo', 0)} sin riesgo</b>; no proyecta riesgo alto, "
    f"pero Timbiquí y Caldono quedan cerca del umbral de 35 y la banda ±{f(final['mae'])} no descarta un "
    f"deterioro."
)

discusion = (
    "La mejora de largo plazo es consistente, pero el rebote de 2025 y los ceros de 2024 sugieren que la "
    "serie está afectada por cambios de reporte. La concentración del riesgo en cuatro municipios es el "
    "hallazgo más accionable; sin embargo, Timbiquí, Guapi y Villa Rica no reportan IRCA rural, por lo "
    "que el riesgo rural podría estar subestimado. Caldono es el caso más alarmante: su IRCA rural 2025 "
    f"({f(top4.iloc[1]['irca_rural'])}) es {f(top4.iloc[1]['brecha_rural_urbano'])} puntos mayor que el "
    f"urbano ({f(top4.iloc[1]['irca_urbano'])}), aunque el promedio 2020–2025 de la brecha es "
    f"{f(caldono_brecha_prom)}, lo que muestra que el dato de un año puede ser extremo. La brecha promedio de 12,2 puntos convive con una "
    "mediana de 1,9: la desigualdad no es generalizada, sino concentrada en casos específicos. En el "
    "contexto nacional, el Cauca está cerca de la mediana; el problema es territorial, no departamental. "
    "El modelo tiene un valor exploratorio, pero su R² negativo y la mejora modesta sobre el naive "
    "impiden usarlo como certeza o para asignar recursos sin validación."
)

conclusiones = [
    "El Cauca mejoró de forma sustancial desde 2007, pero el rebote de 2025 exige seguimiento y verificación del dato.",
    "Priorizar Timbiquí, Caldono, Guapi y Villa Rica, con énfasis en la zona rural de Caldono.",
    "Cerrar la brecha de reporte rural: 66,4% de los registros no tienen IRCA rural; sin ese dato, la política rural es a ciegas.",
    "Usar el dashboard para focalizar y el modelo como tamiz; validar con campo, infraestructura, clima e inversión.",
    "Publicar datos, código y resultados; repetir el ejercicio cada año para distinguir tendencia de artefacto.",
]

limitaciones = [
    "Datos agregados: no permiten inferencia causal ni identificación de hogares.",
    "66,4% de registros sin IRCA rural; en 2025 solo 8 de 38 municipios tienen dato rural.",
    "Popayán solo tiene 2008–2019; en 2025 faltan Balboa, Florencia y López de Micay.",
    "Ceros y saltos abruptos; posible cambio de reporte, no necesariamente deterioro real.",
    "Modelo simple con R² de prueba negativo; la banda ±MAE no es un intervalo de confianza.",
]

referencias = [
    "Ministerio de Salud y Protección Social, INS. <i>Calidad del Agua para Consumo Humano en Colombia (SIVICAP)</i>. datos.gov.co, nxt2-39c3, 2026.",
    "Colombia. <i>Decreto 1575 de 2007</i> y <i>Resolución 2115 de 2007</i>: sistema de protección y control de la calidad del agua para consumo humano.",
    "Fundación Universitaria de Popayán. <i>Guía del Proyecto Final, Electiva II – Introducción a la Ciencia de Datos</i>, 2026.",
    "Naciones Unidas. <i>Objetivo de Desarrollo Sostenible 6: Agua limpia y saneamiento</i>.",
]


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------
def construir_pdf() -> Path:
    ruta = REPORTS / "informe_final.pdf"
    doc = SimpleDocTemplate(
        str(ruta),
        pagesize=A4,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        title="Calidad del agua para consumo humano en el Cauca",
        author="Electiva II – Introducción a la Ciencia de Datos, FUP",
        subject="IRCA Cauca 2007–2025",
    )

    def pie(canvas, doc):
        canvas.saveState()
        canvas.setFont("DejaVu", 7)
        canvas.setFillColor(GRIS)
        canvas.drawString(
            0.65 * inch,
            0.32 * inch,
            "IRCA Cauca 2007–2025 · Electiva II – Introducción a la Ciencia de Datos · FUP",
        )
        canvas.drawRightString(A4[0] - 0.65 * inch, 0.32 * inch, f"Página {doc.page}")
        canvas.restoreState()

    historia = []
    historia.append(encabezado())
    historia.append(Spacer(1, 6))
    historia.append(Paragraph("Resumen", estilo_h1))
    historia.append(Paragraph(resumen, estilo_body))
    historia.append(Paragraph("1. Introducción", estilo_h1))
    historia.append(Paragraph(introduccion, estilo_body))
    historia.append(Paragraph("2. Datos y metodología", estilo_h1))
    historia.append(Paragraph(metodologia, estilo_body))

    ficha = [
        ["Elemento", "Detalle"],
        ["Fuente", "SIVICAP – MinSalud/INS, datos.gov.co, conjunto nxt2-39c3 (consulta 25/11/2026)"],
        ["Cobertura", "42 municipios del Cauca, 2007–2025; 1.019 municipios y 33 departamentos en 2025"],
        ["Unidad de análisis", "Municipio-año; IRCA en escala 0–100 (menor es mejor)"],
        ["Limpieza", "ND a nulo, sin imputación; #TODOS separado; etiquetas unificadas; auditoría documentada"],
        ["Modelo", "Regresión lineal simple (irca_lag1 + irca_roll3); train ≤2021, test 2022–2025"],
        ["Reproducibilidad", "src/, notebooks/, app.py, datos, tablas y figuras en el repositorio"],
    ]
    historia.append(tabla(ficha, [1.25 * inch, 5.75 * inch]))
    historia.append(Spacer(1, 5))
    historia.append(caja_hallazgos(hallazgos))
    historia.append(PageBreak())

    # Página 2
    historia.append(Paragraph("3. Resultados", estilo_h1))
    historia.append(Paragraph("3.1. Evolución departamental", estilo_h2))
    historia.append(Paragraph(evolucion, estilo_body))
    historia.append(
        img(
            BASE / "figures/fig_01_evolucion_cauca.png",
            4.75 * inch,
            "Figura 1. IRCA departamental del Cauca, 2007–2025. Bandas: umbrales oficiales. "
            "Fuente: SIVICAP, datos.gov.co (nxt2-39c3).",
        )
    )
    historia.append(Paragraph("3.2. Ranking municipal 2025", estilo_h2))
    historia.append(Paragraph(ranking_txt, estilo_body))

    filas_ranking = [["Municipio", "IRCA", "Categoría", "Urbano", "Rural", "Brecha"]]
    for fila in ranking.head(8).itertuples():
        filas_ranking.append(
            [
                fila.municipio,
                f(fila.irca),
                fila.nivel_riesgo,
                f(fila.irca_urbano),
                f(fila.irca_rural),
                f(fila.brecha_rural_urbano),
            ]
        )
    historia.append(
        tabla(
            filas_ranking,
            [1.55 * inch, 0.55 * inch, 1.15 * inch, 0.65 * inch, 0.65 * inch, 0.75 * inch],
            ["L", "R", "L", "R", "R", "R"],
        )
    )
    historia.append(
        Paragraph(
            "Tabla 1. Municipios con mayor IRCA en 2025. El ranking completo (38 municipios) está en los anexos. "
            "Los empates comparten puesto; Timbiquí, Guapi y Villa Rica no reportan IRCA rural.",
            estilo_caption,
        )
    )

    historia.append(Paragraph("3.3. Contexto nacional 2025", estilo_h2))
    historia.append(Paragraph(contexto_txt, estilo_body))
    filas_contexto = [["Departamento", "IRCA", "Puesto", "Dif. vs. mediana"]]
    vecinos = contexto[
        contexto["departamento"].isin(
            ["Cauca", "Valle del Cauca", "Huila", "Caquetá", "Putumayo", "Nariño"]
        )
    ].sort_values("irca")
    for fila in vecinos.itertuples():
        filas_contexto.append(
            [fila.departamento, f(fila.irca), str(int(fila.puesto)), f(fila.diferencia_vs_mediana)]
        )
    historia.append(
        tabla(
            filas_contexto,
            [1.65 * inch, 0.7 * inch, 0.65 * inch, 1.15 * inch],
            ["L", "R", "C", "R"],
        )
    )
    historia.append(
        Paragraph(
            "Tabla 2. Cauca y departamentos vecinos, 2025. Puesto: 1 = menor IRCA (mejor). "
            "Diferencia vs. mediana de los 33 departamentos (7,0).",
            estilo_caption,
        )
    )
    historia.append(PageBreak())

    # Página 3
    historia.append(Paragraph("3.4. Brecha urbano-rural", estilo_h2))
    historia.append(Paragraph(brecha_txt, estilo_body))
    historia.append(Paragraph("3.5. Modelo predictivo y pronóstico 2026", estilo_h2))
    historia.append(Paragraph(modelo_txt, estilo_body))

    filas_metricas = [["Modelo", "MAE", "RMSE", "R²", "MAPE (%)"]]
    for fila in metricas_test.itertuples():
        filas_metricas.append(
            [fila.modelo, f(fila.mae), f(fila.rmse), f(fila.r2, 2), f(fila.mape)]
        )
    historia.append(
        tabla(
            filas_metricas,
            [2.15 * inch, 0.6 * inch, 0.65 * inch, 0.6 * inch, 0.75 * inch],
            ["L", "R", "R", "R", "R"],
        )
    )
    historia.append(
        Paragraph(
            "Tabla 3. Métricas en prueba (2022–2025, n=127). El modelo final es la regresión simple; "
            "la regresión completa usa 8 variables y el Random Forest 500 árboles.",
            estilo_caption,
        )
    )
    filas_pred = [["Municipio", "IRCA 2025", "Pronóstico 2026", "Categoría", "Cambio"]]
    for fila in pred_top4.itertuples():
        filas_pred.append(
            [
                fila.municipio,
                f(fila.irca_2025),
                f(fila.irca_2026_predicho),
                fila.categoria_predicha,
                f(fila.cambio_esperado),
            ]
        )
    historia.append(
        tabla(
            filas_pred,
            [1.4 * inch, 0.8 * inch, 1.1 * inch, 1.15 * inch, 0.65 * inch],
            ["L", "R", "R", "L", "R"],
        )
    )
    historia.append(
        Paragraph(
            "Tabla 4. Primeros cuatro municipios del escenario 2026. El pronóstico completo (38 municipios) "
            "está en los anexos. La banda de error usa el MAE de prueba (±5,26), no un intervalo de confianza.",
            estilo_caption,
        )
    )

    historia.append(Paragraph("4. Discusión", estilo_h1))
    historia.append(Paragraph(discusion, estilo_body))
    historia.append(Paragraph("5. Conclusiones y recomendaciones", estilo_h1))
    for item in conclusiones:
        historia.append(Paragraph(f"• {item}", estilo_body))
    historia.append(Paragraph("6. Limitaciones", estilo_h1))
    historia.append(
        Paragraph(
            "Datos agregados, sin inferencia causal ni identificación de hogares; 66,4% de registros sin IRCA "
            "rural (en 2025 solo 8 de 38 municipios); Popayán solo 2008–2019 y en 2025 faltan Balboa, Florencia "
            "y López de Micay; ceros y saltos abruptos que sugieren cambios de reporte; modelo con R² de prueba "
            "negativo y banda ±MAE que no es un intervalo de confianza.",
            estilo_body,
        )
    )
    historia.append(Paragraph("7. Referencias", estilo_h1))
    for item in referencias:
        historia.append(Paragraph(item, estilo_caption))

    doc.build(historia, onFirstPage=pie, onLaterPages=pie)
    print(f"PDF generado: {ruta} ({doc.page} páginas)")
    return ruta


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------
def construir_markdown() -> Path:
    ruta = REPORTS / "informe_final.md"
    filas_ranking_md = "\n".join(
        f"| {fila.municipio} | {f(fila.irca)} | {fila.nivel_riesgo} | {f(fila.irca_urbano)} | "
        f"{f(fila.irca_rural)} | {f(fila.brecha_rural_urbano)} |"
        for fila in ranking.head(10).itertuples()
    )
    filas_contexto_md = "\n".join(
        f"| {fila.departamento} | {f(fila.irca)} | {int(fila.puesto)} | {f(fila.diferencia_vs_mediana)} |"
        for fila in vecinos.itertuples()
    )
    filas_metricas_md = "\n".join(
        f"| {fila.modelo} | {f(fila.mae)} | {f(fila.rmse)} | {f(fila.r2, 2)} | {f(fila.mape)} |"
        for fila in metricas_test.itertuples()
    )
    filas_pred_md = "\n".join(
        f"| {fila.municipio} | {f(fila.irca_2025)} | {f(fila.irca_2026_predicho)} | "
        f"{fila.categoria_predicha} | {f(fila.cambio_esperado)} |"
        for fila in pred_top4.itertuples()
    )
    conclusiones_md = "\n".join(f"- {item}" for item in conclusiones)
    limitaciones_md = "\n".join(f"- {item}" for item in limitaciones)
    referencias_md = "\n".join(f"- {item}" for item in referencias)

    contenido = f"""# Calidad del agua para consumo humano en el Cauca

**Análisis del IRCA 2007–2025, contexto nacional y pronóstico 2026**

Electiva II – Introducción a la Ciencia de Datos · Fundación Universitaria de Popayán · Grupo 4 · 25 de noviembre de 2026

> Versión Markdown del informe. El PDF de 3 páginas es `reports/informe_final.pdf`; los anexos están en `reports/anexos.md` y `reports/anexos.pdf`.

## Resumen

{resumen}

## 1. Introducción

{introduccion}

## 2. Datos y metodología

{metodologia}

| Elemento | Detalle |
|---|---|
| Fuente | SIVICAP – MinSalud/INS, datos.gov.co, conjunto nxt2-39c3 (consulta 25/11/2026) |
| Cobertura | 42 municipios del Cauca, 2007–2025; 1.019 municipios y 33 departamentos en 2025 |
| Unidad de análisis | Municipio-año; IRCA en escala 0–100 (menor es mejor) |
| Limpieza | ND a nulo, sin imputación; #TODOS separado; etiquetas unificadas; auditoría documentada |
| Modelo | Regresión lineal simple (irca_lag1 + irca_roll3); train ≤2021, test 2022–2025 |
| Reproducibilidad | `src/`, `notebooks/`, `app.py`, datos, tablas y figuras en el repositorio |

### Hallazgos clave

{chr(10).join(f"- {item}" for item in hallazgos)}

## 3. Resultados

### 3.1. Evolución departamental

{evolucion}

![Figura 1. IRCA departamental del Cauca, 2007–2025](../figures/fig_01_evolucion_cauca.png)

*Figura 1. IRCA departamental del Cauca, 2007–2025. Bandas: umbrales oficiales. Fuente: SIVICAP, datos.gov.co (nxt2-39c3).*

### 3.2. Ranking municipal 2025

{ranking_txt}

| Municipio | IRCA | Categoría | Urbano | Rural | Brecha |
|---|---:|---|---:|---:|---:|
{filas_ranking_md}

*Tabla 1. Municipios con mayor IRCA en 2025. El ranking completo (38 municipios) está en los anexos.*

### 3.3. Contexto nacional 2025

{contexto_txt}

| Departamento | IRCA | Puesto | Dif. vs. mediana |
|---|---:|---:|---:|
{filas_contexto_md}

*Tabla 2. Cauca y departamentos vecinos, 2025. Puesto: 1 = menor IRCA (mejor).*

### 3.4. Brecha urbano-rural

{brecha_txt}

### 3.5. Modelo predictivo y pronóstico 2026

{modelo_txt}

| Modelo | MAE | RMSE | R² | MAPE (%) |
|---|---:|---:|---:|---:|
{filas_metricas_md}

*Tabla 3. Métricas en prueba (2022–2025, n=127).*

![Figura 2. Modelo predictivo del IRCA municipal](../figures/fig_07_modelo.png)

*Figura 2. Izquierda: real vs. predicho en prueba. Derecha: escenario 2026 con barras de error ±MAE.*

| Municipio | IRCA 2025 | Pronóstico 2026 | Categoría | Cambio |
|---|---:|---:|---|---:|
{filas_pred_md}

*Tabla 4. Primeros cuatro municipios del escenario 2026. El pronóstico completo está en los anexos.*

## 4. Discusión

{discusion}

## 5. Conclusiones y recomendaciones

{conclusiones_md}

## 6. Limitaciones

{limitaciones_md}

## 7. Referencias

{referencias_md}

## Anexos

- `reports/anexos.pdf`: ranking completo, métricas, pronóstico 2026, diccionario y auditoría.
- `reports/anexos.md`: versión Markdown de los anexos.
- `app.py`: dashboard interactivo (Streamlit + Plotly).
- `notebooks/01_limpieza.ipynb`, `02_analisis.ipynb`, `03_modelo.ipynb`: flujo reproducible.
- `video/guion_video.md`: guion del video con los cuatro integrantes.
"""
    ruta.write_text(contenido, encoding="utf-8")
    print(f"Markdown generado: {ruta}")
    return ruta


# ---------------------------------------------------------------------------
# Render de páginas para revisión
# ---------------------------------------------------------------------------
def renderizar_paginas(pdf: Path) -> None:
    try:
        import pymupdf
    except ImportError:
        return
    documento = pymupdf.open(pdf)
    for i, pagina in enumerate(documento, start=1):
        pix = pagina.get_pixmap(dpi=110)
        salida = CAPTURAS / f"informe_pagina_{i}.png"
        pix.save(salida)
        print(f"  Página {i}: {salida}")
    documento.close()


if __name__ == "__main__":
    pdf = construir_pdf()
    construir_markdown()
    renderizar_paginas(pdf)
