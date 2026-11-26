"""Captura evidencias visuales del dashboard con Playwright.

Uso:
    1. Tener el dashboard corriendo: python -m streamlit run app.py
    2. python scripts/capturar_dashboard.py

Salida:
    reports/capturas/dashboard_01_resumen.png
    reports/capturas/dashboard_02_municipios.png
    reports/capturas/dashboard_03_contexto.png
    reports/capturas/dashboard_04_modelo.png
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parents[1]
SALIDA = BASE / "reports" / "capturas"
SALIDA.mkdir(parents=True, exist_ok=True)

URL = "http://localhost:8501"
TABS = [
    (0, "dashboard_01_resumen.png", 2100),
    (1, "dashboard_02_municipios.png", 2800),
    (2, "dashboard_03_contexto.png", 2400),
    (3, "dashboard_04_modelo.png", 2800),
]


def main() -> None:
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page(viewport={"width": 1600, "height": 2200})
        pagina.goto(URL, wait_until="domcontentloaded", timeout=60_000)
        pagina.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=60_000)
        pagina.wait_for_selector('[data-testid="stMetric"]', timeout=90_000)
        pagina.wait_for_selector(".js-plotly-plot", timeout=90_000)
        pagina.wait_for_timeout(5_000)

        for indice, archivo, alto in TABS:
            tabs = pagina.locator('[role="tab"]')
            if tabs.count() > indice:
                tabs.nth(indice).click()
                pagina.wait_for_timeout(4_000)
            pagina.set_viewport_size({"width": 1600, "height": alto})
            pagina.wait_for_timeout(2_000)
            ruta = SALIDA / archivo
            pagina.screenshot(path=str(ruta), full_page=False)
            print(f"Guardado: {ruta}")

        navegador.close()


if __name__ == "__main__":
    sys.exit(main())
