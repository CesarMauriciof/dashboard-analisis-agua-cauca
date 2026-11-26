"""Ejecuta los notebooks y guarda sus salidas con nbclient.

Uso:
    python scripts/ejecutar_notebooks.py
"""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbclient import NotebookClient

BASE = Path(__file__).resolve().parents[1]
NOTEBOOKS = BASE / "notebooks"
NOMBRES = ["01_limpieza.ipynb", "02_analisis.ipynb", "03_modelo.ipynb"]


def main() -> None:
    for nombre in NOMBRES:
        ruta = NOTEBOOKS / nombre
        print(f"Ejecutando {ruta.name}...")
        nb = nbformat.read(ruta, as_version=4)
        cliente = NotebookClient(
            nb,
            timeout=300,
            kernel_name="python3",
            resources={"metadata": {"path": str(ruta.parent)}},
        )
        cliente.execute()
        nbformat.write(nb, ruta)
        print(f"  OK: {ruta}")


if __name__ == "__main__":
    main()
