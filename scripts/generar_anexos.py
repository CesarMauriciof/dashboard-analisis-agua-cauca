"""Genera los anexos del proyecto en PDF y Markdown.

Uso:
    python scripts/generar_anexos.py

Salidas:
    reports/anexos.pdf
    reports/anexos.md
    reports/capturas/anexos_pagina_*.png (revisión visual)
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    CondPageBreak,
    LongTable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

import scripts.generar_informe as rep  # noqa: E402

REPORTS = BASE / "reports"
CAPTURAS = REPORTS / "capturas"
CAPTURAS.mkdir(parents=True, exist_ok=True)

AZUL_OSCURO = rep.AZUL_OSCURO
AZUL = rep.AZUL
AMBAR = rep.AMBAR
BLANCO = rep.BLANCO
FONDO = rep.FONDO
GRIS = rep.GRIS
GRIS_CLARO = rep.GRIS_CLARO
f = rep.f

estilo_celda = ParagraphStyle(
    "celda_anexo", fontName="DejaVu", fontSize=6.4, leading=7.7, textColor=colors.HexColor("#1F2933")
)
estilo_celda_der = ParagraphStyle("celda_anexo_der", parent=estilo_celda, alignment=TA_RIGHT)
estilo_celda_cen = ParagraphStyle("celda_anexo_cen", parent=estilo_celda, alignment=TA_CENTER)
estilo_header = ParagraphStyle(
    "header_anexo", fontName="DejaVu-Bold", fontSize=6.4, leading=7.7, textColor=BLANCO
)
estilo_header_der = ParagraphStyle("header_anexo_der", parent=estilo_header, alignment=TA_RIGHT)
estilo_header_cen = ParagraphStyle("header_anexo_cen", parent=estilo_header, alignment=TA_CENTER)

# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------
ranking = pd.read_csv(REPORTS / "tablas/ranking_2025.csv", encoding="utf-8-sig")
resumen = pd.read_csv(REPORTS / "tablas/resumen_anual_cauca.csv", encoding="utf-8-sig")
brecha = pd.read_csv(REPORTS / "tablas/brecha_urbano_rural.csv", encoding="utf-8-sig")
contexto = pd.read_csv(REPORTS / "tablas/contexto_nacional_2025.csv", encoding="utf-8-sig")
metricas = pd.read_csv(REPORTS / "tablas/metricas_modelo.csv", encoding="utf-8-sig")
coeficientes = pd.read_csv(REPORTS / "tablas/coeficientes_modelo.csv", encoding="utf-8-sig")
pred = pd.read_csv(REPORTS / "tablas/predicciones_2026.csv", encoding="utf-8-sig")
diccionario = pd.read_csv(BASE / "data/clean/diccionario_datos.csv", encoding="utf-8-sig")
auditoria = pd.read_csv(REPORTS / "tablas/calidad_datos.csv", encoding="utf-8-sig")

brecha["periodo"] = (
    brecha["primer_anio"].astype(int).astype(str)
    + "–"
    + brecha["ultimo_anio"].astype(int).astype(str)
)
brecha = brecha.sort_values("brecha_promedio", ascending=False)
contexto = contexto.sort_values("puesto")
pred = pred.sort_values("irca_2026_predicho", ascending=False)


def fmt_int(valor) -> str:
    return "" if pd.isna(valor) else str(int(valor))


def fmt_dec(valor, dec: int = 1) -> str:
    return f(valor, dec)


# ---------------------------------------------------------------------------
# Filas formateadas (se reutilizan en PDF y Markdown)
# ---------------------------------------------------------------------------
def filas(
    df: pd.DataFrame,
    columnas: list[str],
    formatos: dict[str, callable] | None = None,
) -> list[list[str]]:
    salida = []
    for _, fila in df.iterrows():
        valores = []
        for col in columnas:
            valor = fila[col]
            if formatos and col in formatos:
                valores.append(formatos[col](valor))
            elif pd.isna(valor):
                valores.append("—")
            else:
                valores.append(str(valor))
        salida.append(valores)
    return salida


filas_ranking = filas(
    ranking,
    [
        "municipio",
        "irca",
        "nivel_riesgo",
        "irca_urbano",
        "irca_rural",
        "brecha_rural_urbano",
        "puesto_nacional",
        "percentil_nacional",
    ],
    {
        "irca": fmt_dec,
        "irca_urbano": fmt_dec,
        "irca_rural": fmt_dec,
        "brecha_rural_urbano": fmt_dec,
        "puesto_nacional": fmt_int,
        "percentil_nacional": fmt_dec,
    },
)

filas_anual = filas(
    resumen,
    [
        "anio",
        "irca_departamental",
        "nivel_riesgo_departamental",
        "irca_promedio",
        "irca_mediana",
        "municipios_con_dato",
        "pct_rural_sin_dato",
        "pct_riesgo_medio_alto",
    ],
    {
        "anio": fmt_int,
        "irca_departamental": fmt_dec,
        "irca_promedio": fmt_dec,
        "irca_mediana": fmt_dec,
        "municipios_con_dato": fmt_int,
        "pct_rural_sin_dato": fmt_dec,
        "pct_riesgo_medio_alto": fmt_dec,
    },
)

filas_brecha = filas(
    brecha,
    [
        "municipio",
        "anios_con_datos",
        "periodo",
        "irca_urbano_promedio",
        "irca_rural_promedio",
        "brecha_promedio",
        "brecha_maxima",
        "brecha_minima",
        "ultima_brecha",
    ],
    {
        "anios_con_datos": fmt_int,
        "irca_urbano_promedio": fmt_dec,
        "irca_rural_promedio": fmt_dec,
        "brecha_promedio": fmt_dec,
        "brecha_maxima": fmt_dec,
        "brecha_minima": fmt_dec,
        "ultima_brecha": fmt_dec,
    },
)

filas_contexto = filas(
    contexto,
    ["departamento", "irca", "nivel_riesgo", "puesto", "diferencia_vs_mediana"],
    {
        "irca": fmt_dec,
        "puesto": fmt_int,
        "diferencia_vs_mediana": fmt_dec,
    },
)

filas_metricas = filas(
    metricas,
    ["modelo", "conjunto", "n", "mae", "rmse", "r2", "mape"],
    {
        "n": fmt_int,
        "mae": lambda v: fmt_dec(v, 2),
        "rmse": lambda v: fmt_dec(v, 2),
        "r2": lambda v: fmt_dec(v, 3),
        "mape": fmt_dec,
    },
)

filas_coef = filas(
    coeficientes,
    ["variable", "etiqueta", "coeficiente_estandarizado"],
    {"coeficiente_estandarizado": lambda v: fmt_dec(v, 4)},
)

filas_pred = filas(
    pred,
    [
        "municipio",
        "irca_2025",
        "irca_2026_predicho",
        "categoria_predicha",
        "cambio_esperado",
        "intervalo_inferior",
        "intervalo_superior",
    ],
    {
        "irca_2025": fmt_dec,
        "irca_2026_predicho": fmt_dec,
        "cambio_esperado": fmt_dec,
        "intervalo_inferior": fmt_dec,
        "intervalo_superior": fmt_dec,
    },
)

filas_diccionario = filas(
    diccionario, ["variable", "tipo", "descripcion", "unidad", "fuente", "tratamiento"]
)

filas_auditoria = filas(auditoria, ["chequeo", "resultado", "detalle", "tratamiento"])

# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------
def tabla_larga(
    cabeceras: list[str],
    cuerpo: list[list[str]],
    anchos: list[float],
    alineaciones: list[str] | None = None,
) -> LongTable:
    datos = [cabeceras] + cuerpo
    celdas = []
    for i, fila in enumerate(datos):
        fila_celdas = []
        for j, valor in enumerate(fila):
            alineacion = alineaciones[j] if alineaciones else "L"
            if i == 0:
                estilo = (
                    estilo_header_der
                    if alineacion == "R"
                    else estilo_header_cen
                    if alineacion == "C"
                    else estilo_header
                )
            else:
                estilo = (
                    estilo_celda_der
                    if alineacion == "R"
                    else estilo_celda_cen
                    if alineacion == "C"
                    else estilo_celda
                )
            fila_celdas.append(Paragraph(str(valor), estilo))
        celdas.append(fila_celdas)
    t = LongTable(celdas, colWidths=anchos, repeatRows=1, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), AZUL_OSCURO),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLANCO, FONDO]),
                ("GRID", (0, 0), (-1, -1), 0.25, GRIS_CLARO),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, AMBAR),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.1),
                ("LEFTPADDING", (0, 0), (-1, -1), 2.6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2.6),
            ]
        )
    )
    return t


def seccion(titulo: str, nota: str | None = None):
    partes = [CondPageBreak(1.1 * inch), Paragraph(titulo, rep.estilo_h1)]
    if nota:
        partes.append(Paragraph(nota, rep.estilo_caption))
    return partes


def encabezado_anexos():
    t = Table(
        [
            [Paragraph("Anexos", rep.estilo_titulo)],
            [
                Paragraph(
                    "Calidad del agua para consumo humano en el Cauca · IRCA 2007–2025",
                    rep.estilo_subtitulo,
                )
            ],
            [
                Paragraph(
                    "Electiva II – Introducción a la Ciencia de Datos · Fundación Universitaria de "
                    "Popayán · Grupo 4 · 25 de noviembre de 2026",
                    rep.estilo_meta,
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
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LINEBELOW", (0, -1), (-1, -1), 3, AMBAR),
            ]
        )
    )
    return t


def construir_pdf() -> Path:
    ruta = REPORTS / "anexos.pdf"
    doc = SimpleDocTemplate(
        str(ruta),
        pagesize=A4,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        title="Anexos — IRCA Cauca 2007–2025",
        author="Electiva II – Introducción a la Ciencia de Datos, FUP",
    )

    def pie(canvas, doc):
        canvas.saveState()
        canvas.setFont("DejaVu", 7)
        canvas.setFillColor(GRIS)
        canvas.drawString(
            0.55 * inch,
            0.3 * inch,
            "Anexos · IRCA Cauca 2007–2025 · Electiva II – Introducción a la Ciencia de Datos · FUP",
        )
        canvas.drawRightString(A4[0] - 0.55 * inch, 0.3 * inch, f"Página {doc.page}")
        canvas.restoreState()

    historia = []
    historia.append(encabezado_anexos())
    historia.append(Spacer(1, 10))
    historia.append(Paragraph("Contenido", rep.estilo_h1))
    contenido = [
        "A1. Ranking municipal 2025 (38 municipios).",
        "A2. Serie anual del Cauca 2007–2025 (19 años).",
        "A3. Brecha urbano-rural por municipio (36 municipios con datos comparables).",
        "A4. Contexto nacional 2025 (33 departamentos).",
        "A5. Métricas de los modelos (entrenamiento y prueba).",
        "A6. Coeficientes del modelo final.",
        "A7. Pronóstico 2026 (38 municipios).",
        "A8. Diccionario de datos.",
        "A9. Auditoría de calidad.",
        "A10. Enlaces, reproducibilidad y notas metodológicas.",
    ]
    for item in contenido:
        historia.append(Paragraph(f"• {item}", rep.estilo_body))
    historia.append(Spacer(1, 6))
    historia.append(
        Paragraph(
            "Estos anexos complementan el informe principal de 3 páginas "
            "(<b>reports/informe_final.pdf</b>) y no cuentan para el límite de páginas. "
            "Las tablas completas también están en <b>reports/tablas/</b> y los datos limpios en "
            "<b>data/clean/</b>.",
            rep.estilo_body,
        )
    )
    historia.append(PageBreak())

    historia.extend(
        seccion(
            "A1. Ranking municipal 2025",
            "38 municipios con dato. IRCA de menor a mayor; puesto nacional entre 1.019 municipios. "
            "Los empates comparten puesto. Fuente: SIVICAP, datos.gov.co (nxt2-39c3).",
        )
    )
    historia.append(
        tabla_larga(
            ["Municipio", "IRCA", "Categoría", "Urbano", "Rural", "Brecha", "Puesto nac.", "Percentil"],
            filas_ranking,
            [1.35 * inch, 0.5 * inch, 0.95 * inch, 0.55 * inch, 0.55 * inch, 0.55 * inch, 0.5 * inch, 0.6 * inch],
            ["L", "R", "L", "R", "R", "R", "R", "R"],
        )
    )

    historia.extend(
        seccion(
            "A2. Serie anual del Cauca, 2007–2025",
            "IRCA departamental (fila #TODOS), promedio y mediana municipal, cobertura y porcentaje de "
            "registros sin IRCA rural. El porcentaje de riesgo medio/alto usa los municipios con dato.",
        )
    )
    historia.append(
        tabla_larga(
            [
                "Año",
                "IRCA dep.",
                "Categoría",
                "Prom. mun.",
                "Mediana mun.",
                "Municipios",
                "% rural sin dato",
                "% riesgo medio/alto",
            ],
            filas_anual,
            [0.45 * inch, 0.55 * inch, 0.95 * inch, 0.55 * inch, 0.55 * inch, 0.7 * inch, 0.8 * inch, 0.8 * inch],
            ["R", "R", "L", "R", "R", "R", "R", "R"],
        )
    )

    historia.extend(
        seccion(
            "A3. Brecha urbano-rural por municipio",
            "Brecha = IRCA rural − IRCA urbano. Solo se usan los registros con ambos datos; no se imputan "
            "faltantes. Un valor positivo indica peor situación rural. Se ordena por brecha promedio.",
        )
    )
    historia.append(
        tabla_larga(
            [
                "Municipio",
                "Años",
                "Periodo",
                "Urbano prom.",
                "Rural prom.",
                "Brecha prom.",
                "Brecha máx.",
                "Brecha mín.",
                "Última brecha",
            ],
            filas_brecha,
            [1.25 * inch, 0.45 * inch, 0.9 * inch, 0.6 * inch, 0.6 * inch, 0.6 * inch, 0.55 * inch, 0.55 * inch, 0.6 * inch],
            ["L", "R", "C", "R", "R", "R", "R", "R", "R"],
        )
    )

    historia.extend(
        seccion(
            "A4. Contexto nacional 2025",
            "33 departamentos (fila #TODOS). Puesto: 1 = menor IRCA (mejor). Diferencia vs. mediana "
            "departamental (7,0).",
        )
    )
    historia.append(
        tabla_larga(
            ["Departamento", "IRCA", "Categoría", "Puesto", "Dif. vs. mediana"],
            filas_contexto,
            [1.6 * inch, 0.5 * inch, 0.95 * inch, 0.5 * inch, 0.8 * inch],
            ["L", "R", "L", "R", "R"],
        )
    )

    historia.extend(
        seccion(
            "A5. Métricas de los modelos",
            "Entrenamiento ≤2021 (463 observaciones) y prueba 2022–2025 (127). MAE y RMSE en puntos de IRCA; "
            "MAPE en porcentaje. La regresión simple es el modelo final.",
        )
    )
    historia.append(
        tabla_larga(
            ["Modelo", "Conjunto", "n", "MAE", "RMSE", "R²", "MAPE (%)"],
            filas_metricas,
            [1.9 * inch, 1.4 * inch, 0.35 * inch, 0.5 * inch, 0.55 * inch, 0.5 * inch, 0.6 * inch],
            ["L", "L", "R", "R", "R", "R", "R"],
        )
    )

    historia.extend(
        seccion(
            "A6. Coeficientes del modelo final",
            "Coeficientes estandarizados de la regresión simple reentrenada con todos los datos completos. "
            "La etiqueta describe la variable.",
        )
    )
    historia.append(
        tabla_larga(
            ["Variable", "Etiqueta", "Coeficiente estandarizado"],
            filas_coef,
            [1.2 * inch, 2.2 * inch, 1.4 * inch],
            ["L", "L", "R"],
        )
    )

    historia.extend(
        seccion(
            "A7. Pronóstico 2026",
            "Escenario con el IRCA 2025 y la media móvil 2023–2025. La banda usa el MAE de prueba (±5,26) "
            "y no es un intervalo de confianza. Se ordena de mayor a menor pronóstico.",
        )
    )
    historia.append(
        tabla_larga(
            [
                "Municipio",
                "IRCA 2025",
                "Pronóstico 2026",
                "Categoría",
                "Cambio",
                "IC inferior",
                "IC superior",
            ],
            filas_pred,
            [1.25 * inch, 0.6 * inch, 0.7 * inch, 0.95 * inch, 0.6 * inch, 0.6 * inch, 0.6 * inch],
            ["L", "R", "R", "L", "R", "R", "R"],
        )
    )

    historia.extend(
        seccion(
            "A8. Diccionario de datos",
            "Variables de la base limpia. Los códigos DANE se conservan como texto para no perder ceros a la "
            "izquierda. ND se convierte en nulo y no se imputa.",
        )
    )
    historia.append(
        tabla_larga(
            ["Variable", "Tipo", "Descripción", "Unidad", "Fuente", "Tratamiento"],
            filas_diccionario,
            [0.9 * inch, 0.55 * inch, 2.4 * inch, 0.55 * inch, 0.55 * inch, 1.9 * inch],
            ["L", "L", "L", "L", "L", "L"],
        )
    )

    historia.extend(
        seccion(
            "A9. Auditoría de calidad",
            "Chequeos aplicados en src/cleaning.py. La auditoría se regenera con `python -m src.cleaning`.",
        )
    )
    historia.append(
        tabla_larga(
            ["Chequeo", "Resultado", "Detalle", "Tratamiento"],
            filas_auditoria,
            [1.35 * inch, 0.65 * inch, 2.6 * inch, 2.3 * inch],
            ["L", "R", "L", "L"],
        )
    )

    historia.extend(
        seccion(
            "A10. Enlaces, reproducibilidad y notas metodológicas",
        )
    )
    enlaces = [
        "<b>Fuente:</b> SIVICAP – Calidad del Agua para Consumo Humano en Colombia, datos.gov.co, "
        "conjunto nxt2-39c3: https://www.datos.gov.co/d/nxt2-39c3",
        "<b>API:</b> https://www.datos.gov.co/resource/nxt2-39c3.json",
        "<b>Dashboard local:</b> `python -m streamlit run app.py` (http://localhost:8501).",
        "<b>Repositorio:</b> completar con la URL de GitHub al publicar.",
        "<b>Streamlit Community Cloud:</b> completar con la URL de la app al desplegar.",
        "<b>Notebooks:</b> `notebooks/01_limpieza.ipynb`, `02_analisis.ipynb`, `03_modelo.ipynb`.",
        "<b>Reproducción:</b> `python -m src.cleaning`, `python -m src.analysis`, `python -m src.model`, "
        "`python scripts/generar_informe.py`, `python scripts/generar_anexos.py`.",
        "<b>Video:</b> `video/guion_video.md`.",
    ]
    for item in enlaces:
        historia.append(Paragraph(f"• {item}", rep.estilo_body))
    historia.append(Spacer(1, 6))
    historia.append(
        Paragraph(
            "<b>Nota metodológica.</b> El IRCA es un indicador agregado del reporte municipal; no identifica "
            "hogares, veredas ni causas. Los datos rurales están subreportados (66,4% de los registros sin "
            "IRCA rural) y varios municipios tienen series cortas o faltantes. Los resultados deben validarse "
            "con la autoridad sanitaria y con datos de campo. El pronóstico es un escenario, no una certeza.",
            rep.estilo_body,
        )
    )

    doc.build(historia, onFirstPage=pie, onLaterPages=pie)
    print(f"PDF de anexos generado: {ruta} ({doc.page} páginas)")
    return ruta


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------
def md_tabla(cabeceras: list[str], cuerpo: list[list[str]], alineaciones: list[str] | None = None) -> str:
    if alineaciones is None:
        alineaciones = ["L"] * len(cabeceras)
    separador = []
    for alineacion in alineaciones:
        separador.append("---:" if alineacion == "R" else ":---:" if alineacion == "C" else "---")
    lineas = [
        "| " + " | ".join(cabeceras) + " |",
        "|" + "|".join(separador) + "|",
    ]
    for fila in cuerpo:
        limpia = [str(valor).replace("|", "\\|") for valor in fila]
        lineas.append("| " + " | ".join(limpia) + " |")
    return "\n".join(lineas)


def construir_markdown() -> Path:
    ruta = REPORTS / "anexos.md"
    partes = [
        "# Anexos — Calidad del agua para consumo humano en el Cauca",
        "",
        "**IRCA 2007–2025, contexto nacional y pronóstico 2026**",
        "",
        "Electiva II – Introducción a la Ciencia de Datos · Fundación Universitaria de Popayán · Grupo 4 · 25 de noviembre de 2026",
        "",
        "> Versión Markdown de los anexos. El PDF es `reports/anexos.pdf`; el informe principal de 3 páginas es `reports/informe_final.pdf`.",
        "",
        "## Contenido",
        "",
        "- A1. Ranking municipal 2025.",
        "- A2. Serie anual del Cauca 2007–2025.",
        "- A3. Brecha urbano-rural por municipio.",
        "- A4. Contexto nacional 2025.",
        "- A5. Métricas de los modelos.",
        "- A6. Coeficientes del modelo final.",
        "- A7. Pronóstico 2026.",
        "- A8. Diccionario de datos.",
        "- A9. Auditoría de calidad.",
        "- A10. Enlaces, reproducibilidad y notas metodológicas.",
        "",
        "## A1. Ranking municipal 2025",
        "",
        "38 municipios con dato. IRCA de menor a mayor; puesto nacional entre 1.019 municipios. Los empates comparten puesto.",
        "",
        md_tabla(
            ["Municipio", "IRCA", "Categoría", "Urbano", "Rural", "Brecha", "Puesto nac.", "Percentil"],
            filas_ranking,
            ["L", "R", "L", "R", "R", "R", "R", "R"],
        ),
        "",
        "## A2. Serie anual del Cauca, 2007–2025",
        "",
        "IRCA departamental (fila #TODOS), promedio y mediana municipal, cobertura y porcentaje de registros sin IRCA rural.",
        "",
        md_tabla(
            ["Año", "IRCA dep.", "Categoría", "Prom. mun.", "Mediana mun.", "Municipios", "% rural sin dato", "% riesgo medio/alto"],
            filas_anual,
            ["R", "R", "L", "R", "R", "R", "R", "R"],
        ),
        "",
        "## A3. Brecha urbano-rural por municipio",
        "",
        "Brecha = IRCA rural − IRCA urbano. Solo se usan los registros con ambos datos; no se imputan faltantes. Un valor positivo indica peor situación rural. Se ordena por brecha promedio.",
        "",
        md_tabla(
            ["Municipio", "Años", "Periodo", "Urbano prom.", "Rural prom.", "Brecha prom.", "Brecha máx.", "Brecha mín.", "Última brecha"],
            filas_brecha,
            ["L", "R", "C", "R", "R", "R", "R", "R", "R"],
        ),
        "",
        "## A4. Contexto nacional 2025",
        "",
        "33 departamentos (fila #TODOS). Puesto: 1 = menor IRCA (mejor). Diferencia vs. mediana departamental (7,0).",
        "",
        md_tabla(
            ["Departamento", "IRCA", "Categoría", "Puesto", "Dif. vs. mediana"],
            filas_contexto,
            ["L", "R", "L", "R", "R"],
        ),
        "",
        "## A5. Métricas de los modelos",
        "",
        "Entrenamiento ≤2021 (463 observaciones) y prueba 2022–2025 (127). MAE y RMSE en puntos de IRCA; MAPE en porcentaje. La regresión simple es el modelo final.",
        "",
        md_tabla(
            ["Modelo", "Conjunto", "n", "MAE", "RMSE", "R²", "MAPE (%)"],
            filas_metricas,
            ["L", "L", "R", "R", "R", "R", "R"],
        ),
        "",
        "## A6. Coeficientes del modelo final",
        "",
        "Coeficientes estandarizados de la regresión simple reentrenada con todos los datos completos.",
        "",
        md_tabla(
            ["Variable", "Etiqueta", "Coeficiente estandarizado"],
            filas_coef,
            ["L", "L", "R"],
        ),
        "",
        "## A7. Pronóstico 2026",
        "",
        "Escenario con el IRCA 2025 y la media móvil 2023–2025. La banda usa el MAE de prueba (±5,26) y no es un intervalo de confianza. Se ordena de mayor a menor pronóstico.",
        "",
        md_tabla(
            ["Municipio", "IRCA 2025", "Pronóstico 2026", "Categoría", "Cambio", "IC inferior", "IC superior"],
            filas_pred,
            ["L", "R", "R", "L", "R", "R", "R"],
        ),
        "",
        "## A8. Diccionario de datos",
        "",
        "Variables de la base limpia. Los códigos DANE se conservan como texto para no perder ceros a la izquierda. ND se convierte en nulo y no se imputa.",
        "",
        md_tabla(
            ["Variable", "Tipo", "Descripción", "Unidad", "Fuente", "Tratamiento"],
            filas_diccionario,
            ["L", "L", "L", "L", "L", "L"],
        ),
        "",
        "## A9. Auditoría de calidad",
        "",
        "Chequeos aplicados en `src/cleaning.py`. La auditoría se regenera con `python -m src.cleaning`.",
        "",
        md_tabla(
            ["Chequeo", "Resultado", "Detalle", "Tratamiento"],
            filas_auditoria,
            ["L", "R", "L", "L"],
        ),
        "",
        "## A10. Enlaces, reproducibilidad y notas metodológicas",
        "",
        "- **Fuente:** SIVICAP – Calidad del Agua para Consumo Humano en Colombia, datos.gov.co, conjunto `nxt2-39c3`: https://www.datos.gov.co/d/nxt2-39c3",
        "- **API:** https://www.datos.gov.co/resource/nxt2-39c3.json",
        "- **Dashboard local:** `python -m streamlit run app.py` (http://localhost:8501).",
        "- **Repositorio:** completar con la URL de GitHub al publicar.",
        "- **Streamlit Community Cloud:** completar con la URL de la app al desplegar.",
        "- **Notebooks:** `notebooks/01_limpieza.ipynb`, `02_analisis.ipynb`, `03_modelo.ipynb`.",
        "- **Reproducción:** `python -m src.cleaning`, `python -m src.analysis`, `python -m src.model`, `python scripts/generar_informe.py`, `python scripts/generar_anexos.py`.",
        "- **Video:** `video/guion_video.md`.",
        "",
        "**Nota metodológica.** El IRCA es un indicador agregado del reporte municipal; no identifica hogares, veredas ni causas. Los datos rurales están subreportados (66,4% de los registros sin IRCA rural) y varios municipios tienen series cortas o faltantes. Los resultados deben validarse con la autoridad sanitaria y con datos de campo. El pronóstico es un escenario, no una certeza.",
        "",
    ]
    ruta.write_text("\n".join(partes), encoding="utf-8")
    print(f"Markdown de anexos generado: {ruta}")
    return ruta


def renderizar_paginas(pdf: Path) -> None:
    try:
        import pymupdf
    except ImportError:
        return
    documento = pymupdf.open(pdf)
    for i, pagina in enumerate(documento, start=1):
        pix = pagina.get_pixmap(dpi=90)
        salida = CAPTURAS / f"anexos_pagina_{i}.png"
        pix.save(salida)
        print(f"  Página {i}: {salida}")
    documento.close()


if __name__ == "__main__":
    pdf = construir_pdf()
    construir_markdown()
    renderizar_paginas(pdf)
