"""Limpieza reproducible de la base IRCA (SIVICAP).

Uso:
    python -m src.cleaning

Entrada:
    data/raw/irca_colombia_raw.json

Salidas:
    data/clean/irca_colombia_clean.csv
    data/clean/irca_cauca_municipal.csv
    data/clean/irca_cauca_departamento.csv
    data/clean/irca_nacional_municipal_2025.csv
    data/clean/irca_nacional_departamental_2025.csv
    data/clean/diccionario_datos.csv
    reports/tablas/calidad_datos.csv
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import (  # noqa: E402
    ANIO_ULTIMO,
    CAUCA_MUNICIPIOS,
    CLEAN_CAUCA_DEPARTAMENTO,
    CLEAN_CAUCA_MUNICIPAL,
    CLEAN_COLOMBIA,
    CLEAN_NACIONAL_DEPARTAMENTAL_2025,
    CLEAN_NACIONAL_MUNICIPAL_2025,
    DATA_CLEAN,
    DICCIONARIO,
    RAW_JSON,
    RISK_ORDER,
    TABLA_CALIDAD,
)

RENOMBRES = {
    "departamentocodigo": "codigo_departamento",
    "departamento": "departamento",
    "municipiocodigo": "codigo_municipio",
    "municipio": "municipio",
    "a_o": "anio",
    "irca": "irca",
    "nivel_de_riesgo": "nivel_riesgo",
    "ircaurbano": "irca_urbano",
    "nivel_de_riesgo_urbano": "nivel_riesgo_urbano",
    "ircarural": "irca_rural",
    "nivel_de_riesgo_rural": "nivel_riesgo_rural",
}

ETIQUETAS_RIESGO = {
    "sin riesgo": "Sin riesgo",
    "riesgo bajo": "Riesgo bajo",
    "bajo riesgo": "Riesgo bajo",
    "riesgo medio": "Riesgo medio",
    "riesgo alto": "Riesgo alto",
    "alto riesgo": "Riesgo alto",
    "inviable sanitariamente": "Inviable sanitariamente",
    "nd": None,
    "n/d": None,
    "sin dato": None,
    "": None,
}


# ---------------------------------------------------------------------------
# Utilidades de normalización
# ---------------------------------------------------------------------------
def normalizar_texto(valor: object) -> str:
    """Mayúsculas, sin tildes y con espacios simples."""
    if pd.isna(valor):
        return ""
    texto = str(valor).strip()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"\s+", " ", texto)
    return texto.upper()


def normalizar_etiqueta_riesgo(valor: object) -> str | None:
    if pd.isna(valor):
        return None
    clave = normalizar_texto(valor).lower()
    if clave in ETIQUETAS_RIESGO:
        return ETIQUETAS_RIESGO[clave]
    return str(valor).strip() or None


def categoria_por_irca(valor: object) -> str | None:
    """Categoría oficial según el IRCA (Decreto 1575 de 2007)."""
    if pd.isna(valor):
        return None
    valor = float(valor)
    if valor <= 5:
        return "Sin riesgo"
    if valor <= 14:
        return "Riesgo bajo"
    if valor <= 35:
        return "Riesgo medio"
    if valor <= 80:
        return "Riesgo alto"
    return "Inviable sanitariamente"


def a_numero(serie: pd.Series) -> pd.Series:
    """Convierte texto a número, tratando ND y cadenas vacías como nulos."""
    limpia = (
        serie.astype("string")
        .str.strip()
        .replace({"ND": pd.NA, "N/D": pd.NA, "": pd.NA, "nan": pd.NA})
    )
    return pd.to_numeric(limpia, errors="coerce")


def normalizar_codigo(valor: object, ancho: int) -> str:
    texto = str(valor).strip()
    if texto.startswith("#"):
        return texto
    texto = texto.replace(".0", "")
    return texto.zfill(ancho)


# ---------------------------------------------------------------------------
# Carga y limpieza
# ---------------------------------------------------------------------------
def cargar_crudo() -> pd.DataFrame:
    if not RAW_JSON.exists():
        raise FileNotFoundError(
            f"No existe {RAW_JSON}. Descárguelo con:\n"
            "  curl -L \"https://www.datos.gov.co/resource/nxt2-39c3.json?$limit=50000\" "
            "-o data/raw/irca_colombia_raw.json"
        )
    with open(RAW_JSON, encoding="utf-8") as archivo:
        registros = json.load(archivo)
    return pd.DataFrame(registros)


def limpiar(df_crudo: pd.DataFrame) -> pd.DataFrame:
    df = df_crudo.rename(columns=RENOMBRES).copy()

    # Códigos como texto, conservando ceros a la izquierda.
    df["codigo_departamento"] = df["codigo_departamento"].map(
        lambda x: normalizar_codigo(x, 2)
    )
    df["codigo_municipio"] = df["codigo_municipio"].map(
        lambda x: normalizar_codigo(x, 5)
    )

    # Tipos numéricos.
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce").astype("Int64")
    for columna in ("irca", "irca_urbano", "irca_rural"):
        df[columna] = a_numero(df[columna])

    # Etiquetas de riesgo.
    for columna in ("nivel_riesgo", "nivel_riesgo_urbano", "nivel_riesgo_rural"):
        df[columna] = df[columna].map(normalizar_etiqueta_riesgo)

    # Nombres canónicos: el nombre más frecuente por código.
    df["departamento"] = df["departamento"].astype("string").str.strip()
    df["municipio"] = df["municipio"].astype("string").str.strip()

    dep_map = (
        df.loc[~df["codigo_departamento"].str.startswith("#")]
        .groupby("codigo_departamento")["departamento"]
        .agg(lambda s: s.mode().iloc[0])
    )
    df["departamento"] = (
        df["codigo_departamento"].map(dep_map).fillna(df["departamento"])
    )

    mun_map = (
        df.loc[~df["codigo_municipio"].str.startswith("#")]
        .groupby("codigo_municipio")["municipio"]
        .agg(lambda s: s.mode().iloc[0])
    )
    df["municipio"] = df["codigo_municipio"].map(mun_map).fillna(df["municipio"])

    # El Cauca tiene un catálogo oficial propio: evita variantes de tilde.
    mask_cauca = df["departamento"] == "Cauca"
    df.loc[mask_cauca, "municipio"] = (
        df.loc[mask_cauca, "codigo_municipio"]
        .map(CAUCA_MUNICIPIOS)
        .fillna(df.loc[mask_cauca, "municipio"])
    )

    # La fila agregada departamental se identifica sin ambigüedad.
    df.loc[df["codigo_municipio"] == "#TODOS", "municipio"] = "#TODOS"
    df.loc[df["codigo_departamento"] == "#TODOS", "departamento"] = "#TODOS"

    # Variables derivadas.
    df["es_agregado"] = df["codigo_municipio"] == "#TODOS"
    df["categoria_calculada"] = df["irca"].map(categoria_por_irca)
    df["coincide_categoria"] = (
        df["nivel_riesgo"].isna()
        | df["categoria_calculada"].isna()
        | (df["nivel_riesgo"] == df["categoria_calculada"])
    )
    df["tiene_dato_rural"] = df["irca_rural"].notna()
    df["brecha_rural_urbano"] = df["irca_rural"] - df["irca_urbano"]

    # Orden de columnas.
    columnas = [
        "codigo_departamento",
        "departamento",
        "codigo_municipio",
        "municipio",
        "anio",
        "irca",
        "nivel_riesgo",
        "irca_urbano",
        "nivel_riesgo_urbano",
        "irca_rural",
        "nivel_riesgo_rural",
        "categoria_calculada",
        "coincide_categoria",
        "tiene_dato_rural",
        "brecha_rural_urbano",
        "es_agregado",
    ]
    df = df[columnas].sort_values(
        ["departamento", "municipio", "anio"], ignore_index=True
    )
    return df


# ---------------------------------------------------------------------------
# Auditoría de calidad
# ---------------------------------------------------------------------------
def auditar(df: pd.DataFrame, crudo: pd.DataFrame | None = None) -> pd.DataFrame:
    cauca = df[(df["departamento"] == "Cauca") & (~df["es_agregado"])]
    cauca_dep = df[(df["departamento"] == "Cauca") & (df["es_agregado"])]
    filas = []

    def agregar(chequeo, resultado, detalle, tratamiento):
        filas.append(
            {
                "chequeo": chequeo,
                "resultado": resultado,
                "detalle": detalle,
                "tratamiento": tratamiento,
            }
        )

    agregar(
        "Registros totales",
        len(df),
        "Base nacional descargada de datos.gov.co",
        "Se conserva la base completa como referencia",
    )
    agregar(
        "Registros del Cauca",
        len(cauca),
        "Municipios del Cauca, sin la fila agregada #TODOS",
        "Base de análisis municipal",
    )
    agregar(
        "Filas agregadas del Cauca (#TODOS)",
        len(cauca_dep),
        "Una fila por año con el agregado departamental",
        "Se separan para no duplicar el conteo municipal",
    )
    agregar(
        "Municipios del Cauca",
        cauca["municipio"].nunique(),
        "Municipios distintos en la base municipal",
        "Se validan contra el catálogo DANE de 42 municipios",
    )
    agregar(
        "Periodo",
        f"{int(df['anio'].min())}-{int(df['anio'].max())}",
        "Años cubiertos por la base",
        "Se usa 2007-2025 para la serie y 2025 para el corte transversal",
    )
    duplicados_exactos = int(df.duplicated().sum())
    agregar(
        "Duplicados exactos (toda la base)",
        duplicados_exactos,
        "Filas idénticas en todas las columnas",
        "No se eliminan si no hay evidencia de error; se documentan",
    )
    duplicados_cauca = int(cauca.duplicated(subset=["codigo_municipio", "anio"]).sum())
    agregar(
        "Duplicados municipio-año en el Cauca",
        duplicados_cauca,
        "La llave municipio-año debería ser única",
        "Se verificó que no hay duplicados",
    )
    agregar(
        "IRCA total nulo en el Cauca",
        int(cauca["irca"].isna().sum()),
        "Valores ND o vacíos después de convertir a número",
        "Se excluyen del cálculo del indicador",
    )
    agregar(
        "IRCA urbano nulo en el Cauca",
        int(cauca["irca_urbano"].isna().sum()),
        "Valores ND o vacíos",
        "Se mantiene como nulo; no se imputa",
    )
    rural_nulos = int(cauca["irca_rural"].isna().sum())
    agregar(
        "IRCA rural nulo en el Cauca",
        rural_nulos,
        f"{rural_nulos / len(cauca):.1%} de los registros municipales",
        "No se imputa; el análisis rural se limita a casos completos",
    )
    variantes_etiquetas = 0
    if crudo is not None:
        variantes_etiquetas = int(
            crudo["nivel_de_riesgo"].isin(["Bajo riesgo", "Alto riesgo"]).sum()
        )
    agregar(
        "Etiquetas 'Bajo riesgo' / 'Alto riesgo'",
        variantes_etiquetas,
        "Variantes de escritura de las categorías oficiales en la base original",
        "Se unifican a 'Riesgo bajo' y 'Riesgo alto'",
    )
    agregar(
        "Categorías que no coinciden con el IRCA",
        int((~df["coincide_categoria"]).sum()),
        "Comparación entre la etiqueta reportada y la calculada con los umbrales",
        "Se revisan; no se corrige la etiqueta original sin evidencia",
    )
    agregar(
        "IRCA = 0 en el Cauca",
        int((cauca["irca"] == 0).sum()),
        "Puede ser un valor real o un problema de reporte",
        "Se marca para revisión; no se elimina",
    )
    agregar(
        "IRCA = 100 en el Cauca",
        int((cauca["irca"] == 100).sum()),
        "Categoría 'Inviable sanitariamente'",
        "Se conserva: es un valor válido del índice",
    )
    agregar(
        "Municipios del Cauca con dato en 2025",
        int(cauca.loc[cauca["anio"] == ANIO_ULTIMO, "municipio"].nunique()),
        "Cobertura del último año",
        "El ranking 2025 cubre solo los municipios reportados",
    )
    agregar(
        "Años con dato de Popayán",
        int(cauca.loc[cauca["municipio"] == "Popayán", "anio"].nunique()),
        "La capital no aparece en los últimos cortes",
        "Se advierte como limitación central",
    )
    agregar(
        "Filas agregadas departamentales (#TODOS)",
        int(df["es_agregado"].sum()),
        "Una fila por departamento y año; no existe un agregado nacional único",
        "El contexto nacional se construye con los agregados departamentales",
    )

    return pd.DataFrame(filas)


# ---------------------------------------------------------------------------
# Diccionario
# ---------------------------------------------------------------------------
def construir_diccionario() -> pd.DataFrame:
    filas = [
        ("codigo_departamento", "texto", "Código DANE del departamento", "código", "SIVICAP", "Se conserva como texto de 2 dígitos"),
        ("departamento", "texto", "Nombre del departamento", "nombre", "SIVICAP", "Se usa el nombre más frecuente por código"),
        ("codigo_municipio", "texto", "Código DANE del municipio", "código", "SIVICAP", "Texto de 5 dígitos; #TODOS identifica el agregado"),
        ("municipio", "texto", "Nombre del municipio", "nombre", "SIVICAP", "Se usa el catálogo DANE para el Cauca"),
        ("anio", "entero", "Año de reporte", "año", "SIVICAP", "Se convierte a entero"),
        ("irca", "decimal", "Índice de Riesgo de la Calidad del Agua total", "índice 0-100", "SIVICAP", "ND se convierte en nulo"),
        ("nivel_riesgo", "texto", "Categoría de riesgo total", "categoría", "SIVICAP", "Se unifican variantes de escritura"),
        ("irca_urbano", "decimal", "IRCA de la zona urbana", "índice 0-100", "SIVICAP", "ND se convierte en nulo"),
        ("nivel_riesgo_urbano", "texto", "Categoría de riesgo urbana", "categoría", "SIVICAP", "Se unifican variantes"),
        ("irca_rural", "decimal", "IRCA de la zona rural", "índice 0-100", "SIVICAP", "ND se convierte en nulo; 66,4% sin dato en el Cauca (2007-2025)"),
        ("nivel_riesgo_rural", "texto", "Categoría de riesgo rural", "categoría", "SIVICAP", "Se unifican variantes; ND se conserva como nulo"),
        ("categoria_calculada", "texto", "Categoría calculada con los umbrales oficiales", "categoría", "Cálculo propio", "Sirve para validar la etiqueta reportada"),
        ("coincide_categoria", "booleano", "Indica si la etiqueta reportada coincide con la calculada", "verdadero/falso", "Cálculo propio", "Control de calidad"),
        ("tiene_dato_rural", "booleano", "Indica si hay IRCA rural", "verdadero/falso", "Cálculo propio", "Bandera de completitud"),
        ("brecha_rural_urbano", "decimal", "IRCA rural menos IRCA urbano", "puntos de índice", "Cálculo propio", "Positivo indica peor situación rural"),
        ("es_agregado", "booleano", "Indica si la fila es el agregado departamental #TODOS", "verdadero/falso", "Cálculo propio", "Evita doble conteo"),
    ]
    return pd.DataFrame(
        filas,
        columns=["variable", "tipo", "descripcion", "unidad", "fuente", "tratamiento"],
    )


# ---------------------------------------------------------------------------
# Principal
# ---------------------------------------------------------------------------
def main() -> None:
    print("Cargando base cruda...")
    crudo = cargar_crudo()
    print(f"  Registros: {len(crudo):,}")

    print("Limpiando...")
    limpio = limpiar(crudo)

    print("Auditando calidad...")
    auditoria = auditar(limpio, crudo)

    print("Separando tablas...")
    cauca = limpio[(limpio["departamento"] == "Cauca") & (~limpio["es_agregado"])].copy()
    cauca_dep = limpio[(limpio["departamento"] == "Cauca") & (limpio["es_agregado"])].copy()
    nacional_mun_2025 = limpio[
        (~limpio["es_agregado"]) & (limpio["anio"] == ANIO_ULTIMO)
    ].copy()
    nacional_dep_2025 = limpio[
        (limpio["es_agregado"]) & (limpio["anio"] == ANIO_ULTIMO)
    ].copy()

    print("Guardando archivos...")
    limpio.to_csv(CLEAN_COLOMBIA, index=False, encoding="utf-8-sig")
    cauca.to_csv(CLEAN_CAUCA_MUNICIPAL, index=False, encoding="utf-8-sig")
    cauca_dep.to_csv(CLEAN_CAUCA_DEPARTAMENTO, index=False, encoding="utf-8-sig")
    nacional_mun_2025.to_csv(
        CLEAN_NACIONAL_MUNICIPAL_2025, index=False, encoding="utf-8-sig"
    )
    nacional_dep_2025.to_csv(
        CLEAN_NACIONAL_DEPARTAMENTAL_2025, index=False, encoding="utf-8-sig"
    )
    construir_diccionario().to_csv(DICCIONARIO, index=False, encoding="utf-8-sig")
    auditoria.to_csv(TABLA_CALIDAD, index=False, encoding="utf-8-sig")

    print("\nResumen:")
    print(f"  Base limpia completa: {len(limpio):,} registros")
    print(f"  Cauca municipal:      {len(cauca):,} registros")
    print(f"  Cauca departamento:   {len(cauca_dep):,} registros")
    print(f"  Nacional municipal 2025: {len(nacional_mun_2025):,} registros")
    print(f"  Nacional departamental 2025: {len(nacional_dep_2025):,} registros")
    print(f"  Municipios del Cauca: {cauca['municipio'].nunique()}")
    print(f"  Años: {int(cauca['anio'].min())}-{int(cauca['anio'].max())}")
    print("\nArchivos generados en data/clean y reports/tablas.")


if __name__ == "__main__":
    main()
