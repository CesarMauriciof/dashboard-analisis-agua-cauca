# Guion del video — IRCA Cauca 2007–2025

**Proyecto:** Calidad del agua para consumo humano en el Cauca  
**Curso:** Electiva II – Introducción a la Ciencia de Datos · Fundación Universitaria de Popayán  
**Grupo:** 4 integrantes  
**Duración objetivo:** 8–10 minutos  
**Formato:** video horizontal 1080p, con los cuatro integrantes hablando y evidencia en pantalla.

> **Cómo usar este guion:** reemplacen `[Nombre A]`, `[Nombre B]`, `[Nombre C]` y `[Nombre D]` por los nombres reales. Cada integrante debe aparecer en cámara al menos dos veces y hablar al menos 90 segundos. No lean el guion palabra por palabra: úsenlo como apoyo y conserven las cifras.

---

## 1. Reparto y responsabilidades

| Vocero | Rol en el proyecto | Tema en el video | Tiempo aproximado |
|---|---|---|---|
| **[Nombre A]** | Datos y limpieza | Problema, fuente, limpieza y auditoría | 2 min 10 s |
| **[Nombre B]** | Análisis descriptivo | Evolución, ranking y brecha urbano-rural | 1 min 40 s |
| **[Nombre C]** | Contexto y modelo | Comparación nacional, modelo y pronóstico 2026 | 2 min 10 s |
| **[Nombre D]** | Dashboard y cierre | Demo del dashboard, conclusiones y recomendaciones | 2 min 10 s |

**Regla de oro:** todos hablan, todos aparecen y todos pueden responder al menos una pregunta del jurado.

---

## 2. Storyboard y evidencia

| Tiempo | Vocero | Qué dice (resumen) | Qué se ve en pantalla |
|---|---|---|---|
| 0:00–0:25 | Todos | Saludo, curso, integrantes, tema | Cuadrícula con las cuatro cámaras y diapositiva de título |
| 0:25–0:50 | A | Problema: agua segura, IRCA y Cauca rural | Título del dashboard y escala del IRCA (0–100, umbrales) |
| 0:50–1:20 | A | Preguntas de investigación | Cuatro preguntas en pantalla |
| 1:20–2:10 | A | Fuente, 20.212 registros, 736 del Cauca, limpieza | `data/raw/irca_colombia_raw.json`, `src/cleaning.py`, `reports/tablas/calidad_datos.csv` |
| 2:10–2:40 | A | `ND` no se imputa; `#TODOS` separado; 66,4% sin rural | `data/clean/irca_cauca_municipal.csv` (736 filas) y tabla de nulos |
| 2:40–3:30 | B | Evolución: 30,7 → 3,3 → 7,3 | `figures/fig_01_evolucion_cauca.png` y tab Resumen |
| 3:30–4:20 | B | Ranking 2025: 4 de 38 en riesgo medio/alto | `figures/fig_03_ranking_2025.png` y tab Municipios |
| 4:20–4:50 | B | Brecha rural: 12,2 promedio, 1,9 mediana, 66,4% sin dato | `figures/fig_04_urbano_rural.png` |
| 4:50–5:35 | C | Contexto nacional: puesto 19/33, medianas y vecinos | `figures/fig_06_contexto_nacional.png` y tab Contexto nacional |
| 5:35–6:30 | C | Modelo: variables, train/test, MAE 5,26 vs 5,63, R² −0,06 | `notebooks/03_modelo.ipynb` y `figures/fig_07_modelo.png` |
| 6:30–7:10 | C | Pronóstico 2026: 4 medio, 14 bajo, 20 sin riesgo | Tab Modelo y `reports/tablas/predicciones_2026.csv` |
| 7:10–8:10 | D | Demo del dashboard: filtros, KPIs, descargas | Dashboard en vivo: Resumen, Municipios, Contexto, Modelo |
| 8:10–8:50 | D | Conclusiones y recomendaciones | Diapositiva de 5 recomendaciones |
| 8:50–9:20 | Todos | Limitaciones, informe de 3 páginas y anexos | `reports/informe_final.pdf` y `reports/anexos.pdf` |
| 9:20–9:40 | Todos | Cierre, gracias, enlaces | URL del dashboard y del repositorio |

---

## 3. Guion literal

### 0:00–0:25 · Apertura (todos en cámara)

**[Nombre A]:** Buenos días. Somos el grupo 4 de Electiva II, Introducción a la Ciencia de Datos, de la Fundación Universitaria de Popayán.

**[Nombre B]:** Hoy presentamos nuestro análisis de la calidad del agua para consumo humano en el Cauca entre 2007 y 2025.

**[Nombre C]:** Usamos el Índice de Riesgo de la Calidad del Agua, el IRCA, y datos abiertos del SIVICAP.

**[Nombre D]:** Al final mostramos el dashboard, el modelo simple y las recomendaciones. Todos los integrantes participamos en el análisis y en esta presentación.

*En pantalla: cuadrícula con las cuatro cámaras; diapositiva con el título “Calidad del agua para consumo humano en el Cauca · IRCA 2007–2025”.*

### 0:25–0:50 · Problema (A)

**[Nombre A]:** El acceso a agua segura es un determinante de la salud pública. En Colombia, el IRCA resume el riesgo de la calidad del agua en una escala de 0 a 100: menor es mejor. Se clasifica en sin riesgo, bajo, medio, alto e inviable, según el Decreto 1575 de 2007 y la Resolución 2115 de 2007.

*En pantalla: escala del IRCA con los umbrales 5, 14, 35 y 80. Resaltar “menor es mejor”.*

**[Nombre A]:** El Cauca combina alta ruralidad, municipios dispersos y brechas históricas de servicios públicos. Por eso nos preguntamos qué pasó con el IRCA, dónde se concentra el riesgo y qué tan grande es la diferencia entre la zona urbana y la rural.

### 0:50–1:20 · Preguntas (A)

**[Nombre A]:** Nuestro trabajo responde cuatro preguntas. Primera: ¿cómo evolucionó el IRCA del Cauca entre 2007 y 2025? Segunda: ¿qué municipios concentran el riesgo en 2025? Tercera: ¿qué tan grande es la brecha urbano-rural? Y cuarta: ¿cómo se compara el Cauca con el país y qué se puede anticipar para 2026?

*En pantalla: las cuatro preguntas, una por una, con un ícono. No saturar.*

### 1:20–2:10 · Fuente y limpieza (A)

**[Nombre A]:** Trabajamos con el conjunto `nxt2-39c3` de datos.gov.co, del SIVICAP, Ministerio de Salud y Protección Social e Instituto Nacional de Salud. La base tiene 20.212 registros nacionales. Para el Cauca conservamos 736 registros municipales, de 42 municipios, entre 2007 y 2025, y separamos 19 filas agregadas `#TODOS` para no contar dos veces.

*En pantalla: abrir `data/raw/irca_colombia_raw.json` y mostrar el tamaño; luego `data/clean/irca_cauca_municipal.csv` con 736 filas y 42 municipios.*

**[Nombre A]:** La limpieza está en `src/cleaning.py`. Convertimos `ND` en nulo y **no imputamos** los datos rurales; unificamos las etiquetas “Bajo riesgo” y “Alto riesgo”; validamos el rango 0–100; y revisamos duplicados y categorías. La auditoría no encontró duplicados exactos ni duplicados municipio-año, pero sí 489 registros rurales nulos, es decir, el 66,4% del total.

*En pantalla: `reports/tablas/calidad_datos.csv`, resaltar “IRCA rural nulo en el Cauca: 489” y “66,4%”.*

**[Nombre A]:** Esa decisión es importante: no inventamos el dato rural. Trabajamos con casos completos y declaramos el sesgo. Es una de las limitaciones centrales del proyecto.

### 2:10–2:40 · Cobertura y decisiones (A)

**[Nombre A]:** También revisamos la cobertura. Popayán solo tiene datos de 2008 a 2019; en 2025 faltan Balboa, Florencia, López de Micay y Popayán. Por eso los promedios y rankings no representan a los 42 municipios en todos los años. El dashboard muestra el año y el número de municipios con dato para que la lectura sea honesta.

*En pantalla: tabla de cobertura por año o el tab Resumen con el KPI “Municipios con dato”.*

### 2:40–3:30 · Evolución (B)

**[Nombre B]:** Pasemos a los resultados. El IRCA departamental cayó de 30,7 en 2007 a 14,7 en 2015 y a 3,3 en 2024. En 2025 subió a 7,3, que sigue siendo riesgo bajo, pero es un aumento de 4,0 puntos frente a 2024.

*En pantalla: `figures/fig_01_evolucion_cauca.png`. Señalar 2007, 2015, 2024 y 2025.*

**[Nombre B]:** La serie urbana de 2025 es 6,6 y la rural 9,9. La rural tiene menos datos y más volatilidad. Además, la caída de 2024 y el rebote de 2025 coinciden con ceros y saltos abruptos en varios municipios. Eso sugiere cambios de reporte, no necesariamente un deterioro real. Por eso hablamos de una mejora con rebote, no de una tendencia consolidada.

### 3:30–4:20 · Ranking 2025 (B)

**[Nombre B]:** En 2025 hay 38 municipios con dato. Dieciocho están sin riesgo, dieciséis en riesgo bajo, dos en riesgo medio y dos en riesgo alto. Es decir, 4 de 38, el 10,5%, concentran el riesgo medio o alto.

*En pantalla: `figures/fig_03_ranking_2025.png` o el tab Municipios, con la tabla ordenada.*

**[Nombre B]:** Los cuatro casos son Timbiquí, con 37,0; Caldono, con 36,6; Guapi, con 32,0; y Villa Rica, con 19,1. Timbiquí y Caldono están en riesgo alto. Timbiquí, Guapi y Villa Rica solo reportan IRCA urbano; Caldono reporta urbano 18,8 y rural 67,8, la brecha más alta de 2025: 49,0 puntos. Es el caso más alarmante.

**[Nombre B]:** También hay siete municipios con IRCA 0 y cuatro sin dato. Los ceros y los faltantes nos obligan a leer el ranking con cautela; no son una fotografía perfecta de la realidad.

### 4:20–4:50 · Brecha urbano-rural (B)

**[Nombre B]:** La brecha se calcula como IRCA rural menos IRCA urbano. En las 242 observaciones con ambos datos, el promedio es 12,2 puntos, la mediana 1,9 y el 55% son positivas. La diferencia entre media y mediana muestra que el promedio está impulsado por casos extremos, no por una desigualdad generalizada.

*En pantalla: `figures/fig_04_urbano_rural.png`. Señalar Popayán, Santa Rosa, Caloto, Páez y Rosas.*

**[Nombre B]:** Los mayores promedios con al menos tres años de datos son Popayán, 71,2, entre 2009 y 2013; Santa Rosa, 63,9; Caloto, 51,4; Páez, 44,5; y Rosas, 38,3. En 2025 solo 8 de 38 municipios tienen dato rural; la brecha promedio de ese año es 8,4. El 66,4% sin dato rural sigue siendo el gran hueco.

### 4:50–5:35 · Contexto nacional (C)

**[Nombre C]:** Ahora, el contexto nacional. En 2025 el Cauca ocupa el puesto 19 de 33 departamentos, con 7,3. La mediana departamental es 7,0; la mediana municipal nacional es 5,7 y la del Cauca es 6,1, que corresponde al percentil 51,6. En términos simples, el Cauca está cerca de la mitad del país.

*En pantalla: `figures/fig_06_contexto_nacional.png` y el tab Contexto nacional.*

**[Nombre C]:** Entre los vecinos, el Cauca está mejor que Nariño, con 22,5, y Putumayo, con 17,0; pero peor que Valle del Cauca, 4,4; Huila, 4,1; y Caquetá, 6,7. Timbiquí está en el percentil nacional 94,3: solo alrededor del 6% de los municipios del país tienen un IRCA peor. El problema no es todo el departamento; es territorial.

### 5:35–6:30 · Modelo (C)

**[Nombre C]:** Para el componente predictivo construimos un panel anual completo por municipio, de 2007 a 2026, para que los rezagos sean de año calendario y no de fila. Usamos dos variables: el IRCA del año anterior y la media móvil de tres años. Entrenamos hasta 2021, con 463 observaciones, y probamos en 2022–2025, con 127. No usamos información del futuro.

*En pantalla: `notebooks/03_modelo.ipynb`, celda del panel y del split; luego `figures/fig_07_modelo.png`.*

**[Nombre C]:** Comparamos un pronóstico ingenuo, la media histórica, una regresión simple, una regresión completa y un Random Forest. El modelo final es la regresión simple por parsimonia y estabilidad. Su MAE de prueba es 5,26 puntos; el naive, 5,63. La mejora es de 0,37 puntos, apenas un 6,6%. La regresión completa baja a 5,25 y el Random Forest sube a 5,88.

**[Nombre C]:** El R² de prueba es −0,06 y el de entrenamiento es 0,73. Eso significa que el modelo no generaliza bien y suaviza los extremos. Es una herramienta de tamizaje, no una certeza. Para 2026 proyectamos 4 municipios en riesgo medio: Timbiquí, 28,7; Caldono, 26,2; Guapi, 25,8; y Villa Rica, 14,4; 14 en riesgo bajo y 20 sin riesgo. No proyectamos riesgo alto, pero Timbiquí y Caldono quedan cerca del umbral de 35. La banda de error usa el MAE, no es un intervalo de confianza.

### 6:30–7:10 · Pronóstico y lectura (C)

**[Nombre C]:** El pronóstico asume persistencia: si no cambian las condiciones, el IRCA de 2026 se parecerá al de 2025. No incorpora inversiones, clima, infraestructura ni cambios de reporte. Por eso lo presentamos como escenario. La recomendación es usarlo para priorizar la vigilancia, no para asignar recursos sin validación de campo.

*En pantalla: `reports/tablas/predicciones_2026.csv` y el tab Modelo.*

### 7:10–8:10 · Dashboard (D)

**[Nombre D]:** Todo el análisis está en un dashboard interactivo hecho con Streamlit y Plotly. Tiene cuatro pestañas: Resumen, Municipios, Contexto nacional y Modelo. En la barra lateral se elige el año, la serie destacada —total, urbana o rural—, los municipios y la categoría de riesgo.

*En pantalla: dashboard en vivo. Cambiar el año y mostrar cómo se actualizan los KPIs.*

**[Nombre D]:** En Resumen están los indicadores clave y la evolución. En Municipios se puede seleccionar un municipio y ver su serie, su categoría, su brecha y descargar la tabla. En Contexto nacional se compara el Cauca con los 33 departamentos. En Modelo están las métricas, los coeficientes y el pronóstico 2026 con su banda de error.

*En pantalla: recorrer las cuatro pestañas; hacer clic en un municipio; mostrar el botón de descarga.*

**[Nombre D]:** El dashboard es reproducible: lee los CSV limpios del repositorio y se puede publicar en Streamlit Community Cloud. Las instrucciones están en el README y en `docs/despliegue.md`.

### 8:10–8:50 · Conclusiones (D)

**[Nombre D]:** Nuestras conclusiones son cinco. Primera: el Cauca mejoró de forma sustancial desde 2007, pero el rebote de 2025 exige seguimiento y verificación del dato. Segunda: hay que priorizar Timbiquí, Caldono, Guapi y Villa Rica, con énfasis en la zona rural de Caldono. Tercera: hay que cerrar la brecha de reporte rural; sin el 66,4% que falta, la política rural es a ciegas.

*En pantalla: diapositiva con las cinco recomendaciones; resaltar las tres primeras.*

**[Nombre D]:** Cuarta: usar el dashboard para focalizar y el modelo como tamiz, validando con campo, infraestructura, clima e inversión. Quinta: publicar datos, código y resultados, y repetir el ejercicio cada año para distinguir tendencia de artefacto.

### 8:50–9:20 · Limitaciones y entregables (todos)

**[Nombre A]:** Somos transparentes con las limitaciones: datos agregados, sin inferencia causal; 66,4% sin IRCA rural; Popayán solo 2008–2019; y ceros o saltos que pueden ser cambios de reporte.

**[Nombre B]:** El informe principal tiene tres páginas, como exige la guía. Los anexos tienen el ranking completo, la serie anual, la brecha, el contexto, las métricas, el pronóstico, el diccionario y la auditoría.

*En pantalla: `reports/informe_final.pdf` (3 páginas) y `reports/anexos.pdf` (6 páginas).*

**[Nombre C]:** El repositorio incluye los datos crudos y limpios, el código, los tres notebooks, el dashboard, las figuras y los informes. Todo se reproduce con los comandos del README.

### 9:20–9:40 · Cierre (todos)

**[Nombre D]:** Este es nuestro análisis de la calidad del agua en el Cauca. No es una verdad absoluta: es una herramienta para mirar el territorio, priorizar y seguir midiendo.

**[Nombre A]:** Gracias por su atención. Quedamos atentos a sus preguntas.

*En pantalla: nombres de los cuatro integrantes, curso, fecha, URL del dashboard y del repositorio. Mantener 5 segundos.*

---

## 4. Evidencia obligatoria en pantalla

Marquen cada evidencia antes de exportar el video:

- [ ] Los cuatro integrantes aparecen en cámara al inicio y al cierre.
- [ ] Cada integrante habla al menos 90 segundos.
- [ ] Se ve la fuente: `data/raw/irca_colombia_raw.json` o el enlace de datos.gov.co.
- [ ] Se ve la base limpia: `data/clean/irca_cauca_municipal.csv` con 736 filas y 42 municipios.
- [ ] Se ve la auditoría: `reports/tablas/calidad_datos.csv` con los 489 rurales nulos y el 66,4%.
- [ ] Se ven las figuras 01, 03, 04, 06 y 07.
- [ ] Se ve al menos un notebook ejecutado (`01_limpieza`, `02_analisis` o `03_modelo`).
- [ ] Se ve el dashboard en vivo con las cuatro pestañas y al menos un filtro.
- [ ] Se ve el informe de 3 páginas y los anexos.
- [ ] Se ve el README o el repositorio con los comandos de reproducción.
- [ ] Se muestran las limitaciones y no se exagera el poder del modelo.
- [ ] No aparece información personal ni datos sensibles.

---

## 5. Checklist de grabación y edición

**Antes de grabar**

- [ ] Ensayo general cronometrado (máximo 10 minutos).
- [ ] Guion impreso o en segunda pantalla; no leer la pantalla.
- [ ] Cámara a la altura de los ojos, luz de frente, fondo ordenado.
- [ ] Micrófono cerca (audífonos con micrófono o micrófono USB).
- [ ] Cerrar notificaciones, correo y pestañas personales.
- [ ] Abrir el dashboard, los notebooks, las figuras y los PDF antes de grabar.
- [ ] Resolución 1920×1080; 30 fps; audio a 48 kHz si es posible.

**Durante la grabación**

- [ ] Grabar la cámara y la pantalla por separado si es posible.
- [ ] Hacer pausas de 2 segundos entre secciones para facilitar la edición.
- [ ] Repetir una frase completa si hay un error; no cortar a mitad de palabra.
- [ ] Mover el cursor despacio y señalar las cifras clave.
- [ ] Evitar “eh”, “este”, “o sea”; si sale, cortar en edición.

**Después de grabar**

- [ ] Unir las cuatro cámaras en una cuadrícula al inicio y al cierre.
- [ ] Agregar rótulos con el nombre y el rol de cada integrante.
- [ ] Insertar las cifras clave como texto en pantalla (30,7; 3,3; 7,3; 4/38; 5,26; 5,63).
- [ ] Subtitular en español; revisar nombres propios y cifras.
- [ ] Normalizar el audio y eliminar ruidos.
- [ ] Exportar MP4 H.264, 1080p, audio AAC.
- [ ] Subir a YouTube como “no listado” o a Google Drive con permiso de lectura.
- [ ] Probar el enlace en una ventana de incógnito.
- [ ] Guardar una copia local y el enlace en `docs/hoja_de_ruta.md`.

---

## 6. Preguntas probable del jurado y respuestas sugeridas

**1. ¿Por qué no imputaron los datos rurales?**  
Porque el 66,4% de los registros no tienen IRCA rural. Imputar inventaría una realidad territorial que no observamos. Preferimos casos completos, declarar el sesgo y mostrar la cobertura en el dashboard.

**2. ¿Por qué un modelo con R² negativo?**  
Porque el objetivo no era maximizar el ajuste, sino construir un baseline transparente y compararlo. La regresión completa y el Random Forest no mejoran el MAE de forma relevante. El R² negativo es un resultado honesto: el modelo no explica bien la varianza y sirve solo como tamiz.

**3. ¿El IRCA subió en 2025?**  
El dato departamental subió de 3,3 a 7,3. No podemos afirmar que sea un deterioro real: en 2024 hay ceros y saltos abruptos que sugieren cambios de reporte. Recomendamos verificar con la autoridad sanitaria y monitorear 2026.

**4. ¿Por qué el Cauca está en el puesto 19 y no más arriba?**  
Porque el IRCA departamental es un agregado y el país tiene departamentos con mejor desempeño. Además, el promedio del Cauca esconde heterogeneidad municipal: cuatro municipios concentran el riesgo medio/alto.

**5. ¿Qué haría falta para mejorar el modelo?**  
Más predictores: infraestructura, inversión, clima, población, continuidad del servicio, calidad del reporte. También una serie más larga y datos rurales completos. Y validación externa con la autoridad sanitaria.

**6. ¿Cómo se reproduce el proyecto?**  
Con `requirements-dev.txt`, los comandos `python -m src.cleaning`, `src.analysis`, `src.model`, los notebooks y `python scripts/run_all.py`. El README y `docs/hoja_de_ruta.md` tienen el paso a paso.

**7. ¿Cómo se publica el dashboard?**  
En Streamlit Community Cloud, conectando el repositorio de GitHub y seleccionando `app.py`. Las instrucciones están en `docs/despliegue.md`.

**8. ¿Usaron inteligencia artificial?**  
Sí, como apoyo para código, revisión y redacción. Los autores verificaron los datos, ejecutaron el pipeline, revisaron las cifras y asumen la responsabilidad del contenido. La declaración está en `docs/equipo.md`.

**9. ¿Por qué el informe tiene 3 páginas?**  
Porque la guía fija ese límite. El informe principal es de 3 páginas; los anexos son un documento separado con las tablas completas, el diccionario y la auditoría.

**10. ¿Cuál es la recomendación más urgente?**  
Priorizar Timbiquí, Caldono, Guapi y Villa Rica, y cerrar la brecha de reporte rural. Sin datos rurales, cualquier política para el 66,4% del territorio es una política a ciegas.

---

## 7. Versión corta de respaldo (60 segundos)

Si el video completo no se puede subir, graben esta versión:

> “Analizamos el IRCA de los 42 municipios del Cauca entre 2007 y 2025 con datos del SIVICAP. El IRCA cayó de 30,7 en 2007 a 3,3 en 2024, pero subió a 7,3 en 2025. Cuatro de 38 municipios están en riesgo medio/alto: Timbiquí, Caldono, Guapi y Villa Rica. La brecha rural promedia 12,2 puntos, pero el 66,4% de los registros no tienen dato rural. El Cauca ocupa el puesto 19 de 33 departamentos. Un modelo lineal simple obtiene un MAE de 5,26, solo 0,37 mejor que el naive, con R² de −0,06; por eso el pronóstico 2026 es un escenario, no una certeza. El dashboard, los notebooks y el informe de 3 páginas están en el repositorio.”

---

## 8. Enlaces para el cierre

- **Dashboard local:** `http://localhost:8501`
- **Dashboard publicado:** completar después de desplegar en Streamlit Community Cloud.
- **Repositorio:** completar con la URL de GitHub.
- **Fuente:** https://www.datos.gov.co/d/nxt2-39c3
- **Informe:** `reports/informe_final.pdf` (3 páginas)
- **Anexos:** `reports/anexos.pdf` (6 páginas)
- **Notebooks:** `notebooks/01_limpieza.ipynb`, `02_analisis.ipynb`, `03_modelo.ipynb`

---

**Nota final:** el video debe demostrar que los cuatro integrantes entienden el proyecto, no solo que se turnan para leer. Si alguien no puede grabar, esa persona debe aparecer al menos en una llamada grabada o en una diapositiva con su aporte explícito; idealmente, todos hablan en vivo.
