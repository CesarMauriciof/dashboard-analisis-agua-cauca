# Hoja de ruta de entrega

**Proyecto:** Calidad del agua para consumo humano en el Cauca — IRCA 2007–2025  
**Curso:** Electiva II – Introducción a la Ciencia de Datos  
**Grupo:** 4 integrantes  
**Fecha de referencia:** 25 de noviembre de 2026

---

## 1. Estado actual

| Componente | Estado | Evidencia |
|---|---|---|
| Datos crudos y limpios | Listo | `data/raw/`, `data/clean/`, `data/README.md` |
| Pipeline reproducible | Listo | `src/`, `scripts/run_all.py` |
| Notebooks ejecutados | Listo | `notebooks/01_limpieza.ipynb`, `02_analisis.ipynb`, `03_modelo.ipynb` |
| Dashboard Streamlit | Listo en local | `app.py`, capturas en `reports/capturas/` |
| Informe de 3 páginas | Listo | `reports/informe_final.pdf` |
| Anexos | Listo | `reports/anexos.pdf` (6 páginas) |
| Guion de video | Listo | `video/guion_video.md` |
| Publicación en Streamlit Cloud | Pendiente | Requiere cuenta de GitHub del grupo |
| Video final | Pendiente | Requiere grabación con los cuatro integrantes |

---

## 2. Cronograma propuesto

> Ajustar las fechas si el docente fijó una fecha límite distinta. La ruta crítica es: **desplegar → grabar → editar → revisar → entregar**.

| Fecha | Tarea | Responsable | Evidencia esperada |
|---|---|---|---|
| **25 nov** | Cierre técnico: correr `python scripts/run_all.py`, revisar PDF de 3 páginas y anexos, comprobar hashes. | Todos / [Nombre D] | Pipeline sin errores; PDF y anexos abiertos; `data/README.md` con hashes. |
| **26 nov** | Crear repositorio GitHub, subir el proyecto y desplegar en Streamlit Community Cloud. | [Nombre D] + [Nombre A] | URL pública del dashboard; captura de la app desplegada. |
| **27 nov** | Grabar el video con los cuatro integrantes hablando y en cámara. | Todos | Archivo de video en bruto; evidencia de las cuatro personas. |
| **28 nov** | Editar el video: cortes, subtítulos, inserción de dashboard, notebooks, informe y anexos. | [Nombre D] + [Nombre B] | Video final 1080p, 8–10 min. |
| **29 nov** | Revisión cruzada: cifras del informe vs. dashboard vs. video; nombres reales; URLs; checklist. | Todos | Lista de verificación firmada; correcciones aplicadas. |
| **30 nov** | Entrega final: video, PDF, URL del dashboard, URL del repositorio y datos. | [Nombre A] | Formulario/entrega completada; respaldo en Drive. |

### Ruta crítica

1. **URL del dashboard** → debe existir antes de grabar la demo del video.
2. **Video final** → es el entregable con más dependencias (cuatro personas, edición, evidencia).
3. **Revisión cruzada** → evita que el video muestre cifras que no coincidan con el informe.

### Plan B

- **Si Streamlit Cloud falla:** usar `python -m streamlit run app.py` en local, grabar la demo y adjuntar el repositorio con instrucciones. Dejar constancia en el video de que la versión local es equivalente.
- **Si un integrante no puede grabar:** reprogramar la grabación; no sustituir por una persona que no sea del grupo. El requisito es que los cuatro hablen y aparezcan.
- **Si el video se pasa de 10 minutos:** usar la versión corta de respaldo de 60 segundos del guion y dejar el corte largo como anexo.

---

## 3. Checklist de entrega

### Datos

- [ ] `data/raw/irca_colombia_raw.json` presente y con 20.212 registros.
- [ ] `data/clean/` contiene los seis CSV y el diccionario.
- [ ] `data/README.md` incluye fuente, descarga, hashes y decisiones de limpieza.
- [ ] `reports/tablas/calidad_datos.csv` declara faltantes, duplicados y ceros.

### Código y notebooks

- [ ] `python scripts/run_all.py` corre de principio a fin.
- [ ] `python scripts/run_all.py --sin-notebooks` corre sin errores.
- [ ] Los tres notebooks están ejecutados y sin celdas de error.
- [ ] `requirements.txt`, `requirements-dev.txt` y `runtime.txt` están completos.

### Dashboard

- [ ] `app.py` abre en local con `python -m streamlit run app.py`.
- [ ] Las cuatro pestañas cargan: Resumen, Municipios, Contexto nacional, Modelo.
- [ ] Los filtros de año, serie, municipio y categoría funcionan.
- [ ] Las descargas CSV funcionan.
- [ ] Capturas `dashboard_01_resumen.png` a `dashboard_04_modelo.png` actualizadas.
- [ ] URL pública de Streamlit Community Cloud registrada en `README.md`.

### Informe y anexos

- [ ] `reports/informe_final.pdf` tiene exactamente **3 páginas**.
- [ ] `reports/anexos.pdf` incluye ranking, serie anual, brecha, contexto, métricas, coeficientes, pronóstico, diccionario y auditoría.
- [ ] Las cifras del informe coinciden con el dashboard y el video.
- [ ] Las limitaciones están explícitas: R² de prueba negativo, MAE modesto, datos rurales faltantes, ceros y saltos de reporte.

### Video

- [ ] Duración 8–10 minutos.
- [ ] Los cuatro integrantes hablan y aparecen en cámara.
- [ ] Se muestra evidencia del dashboard, notebooks, informe y anexos.
- [ ] Se ven las URLs del dashboard y del repositorio.
- [ ] Audio audible, video 1080p, sin pantallas en blanco prolongadas.
- [ ] Preguntas del jurado practicadas (ver `video/guion_video.md`).

### Publicación

- [ ] Repositorio GitHub con `main` y último commit.
- [ ] `LICENSE`, `README.md`, `docs/` y `data/README.md` incluidos.
- [ ] Sin secretos, credenciales ni datos personales.
- [ ] URL del dashboard copiada en `README.md` y en el guion del video.

---

## 4. Criterios de aceptación

- El informe principal no supera **3 páginas** (los anexos van aparte).
- El dashboard permite explorar los 42 municipios y el contexto nacional.
- El modelo se presenta como **herramienta de tamizaje**, no como certeza.
- El video evidencia el trabajo de los cuatro integrantes.
- Todo es reproducible con los comandos del `README.md`.
- No se usan datos personales ni información sensible.

---

## 5. Registro de avances

| Fecha | Avance | Responsable | Observaciones |
|---|---|---|---|
| 25 nov | Proyecto técnico y documentación completos | Todos | Pendiente despliegue y video |
|  |  |  |  |
|  |  |  |  |