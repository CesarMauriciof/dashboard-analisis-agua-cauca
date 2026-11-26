"""Pipeline completo del proyecto IRCA Cauca.

Uso:
    python scripts/run_all.py
    python scripts/run_all.py --sin-notebooks

Ejecuta, en orden:
    1. Limpieza y auditoría (src.cleaning)
    2. Tablas y figuras descriptivas (src.analysis)
    3. Modelo y pronóstico 2026 (src.model)
    4. Generación y ejecución de notebooks (opcional)
    5. Informe final de 3 páginas (scripts.generar_informe)
    6. Anexos (scripts.generar_anexos)

El script usa el mismo intérprete de Python con el que se invoca y fuerza
UTF-8 para evitar problemas de acentos en consolas Windows.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def paso(numero: int, total: int, titulo: str) -> None:
    print(f"\n[{numero}/{total}] {titulo}", flush=True)


def correr(comando: list[str], descripcion: str) -> None:
    print(f"  $ {' '.join(comando)}", flush=True)
    subprocess.run(comando, cwd=BASE, check=True)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Ejecuta el pipeline completo del proyecto IRCA Cauca."
    )
    parser.add_argument(
        "--sin-notebooks",
        action="store_true",
        help="Omite la generación y ejecución de los notebooks.",
    )
    args = parser.parse_args()

    raw_json = BASE / "data" / "raw" / "irca_colombia_raw.json"
    if not raw_json.exists():
        raise SystemExit(
            "No se encontró data/raw/irca_colombia_raw.json. "
            "Descargue la fuente antes de ejecutar el pipeline (ver data/README.md)."
        )

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    os.environ.update(env)

    total = 6
    inicio = time.perf_counter()

    paso(1, total, "Limpieza y auditoría de datos")
    correr([sys.executable, "-m", "src.cleaning"], "limpieza")

    paso(2, total, "Tablas y figuras descriptivas")
    correr([sys.executable, "-m", "src.analysis"], "análisis")

    paso(3, total, "Modelo predictivo y pronóstico 2026")
    correr([sys.executable, "-m", "src.model"], "modelo")

    if args.sin_notebooks:
        paso(4, total, "Notebooks omitidos (--sin-notebooks)")
    else:
        paso(4, total, "Generación y ejecución de notebooks")
        correr([sys.executable, "scripts/crear_notebooks.py"], "crear notebooks")
        correr([sys.executable, "scripts/ejecutar_notebooks.py"], "ejecutar notebooks")

    paso(5, total, "Informe final de 3 páginas")
    correr([sys.executable, "scripts/generar_informe.py"], "informe")

    paso(6, total, "Anexos")
    correr([sys.executable, "scripts/generar_anexos.py"], "anexos")

    transcurrido = time.perf_counter() - inicio
    print(f"\nPipeline completado en {transcurrido:.1f} s.")
    print("Salidas principales:")
    print("  - data/clean/")
    print("  - reports/tablas/")
    print("  - figures/")
    print("  - reports/informe_final.pdf")
    print("  - reports/anexos.pdf")


if __name__ == "__main__":
    main()