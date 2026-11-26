# Anexos — Calidad del agua para consumo humano en el Cauca

**IRCA 2007–2025, contexto nacional y pronóstico 2026**

Electiva II – Introducción a la Ciencia de Datos · Fundación Universitaria de Popayán · Grupo 4 · 25 de noviembre de 2026

> Versión Markdown de los anexos. El PDF es `reports/anexos.pdf`; el informe principal de 3 páginas es `reports/informe_final.pdf`.

## Contenido

- A1. Ranking municipal 2025.
- A2. Serie anual del Cauca 2007–2025.
- A3. Brecha urbano-rural por municipio.
- A4. Contexto nacional 2025.
- A5. Métricas de los modelos.
- A6. Coeficientes del modelo final.
- A7. Pronóstico 2026.
- A8. Diccionario de datos.
- A9. Auditoría de calidad.
- A10. Enlaces, reproducibilidad y notas metodológicas.

## A1. Ranking municipal 2025

38 municipios con dato. IRCA de menor a mayor; puesto nacional entre 1.019 municipios. Los empates comparten puesto.

| Municipio | IRCA | Categoría | Urbano | Rural | Brecha | Puesto nac. | Percentil |
|---|---:|---|---:|---:|---:|---:|---:|
| Timbiquí | 37,0 | Riesgo alto | 37,0 | — | — | 59 | 94,3 |
| Caldono | 36,6 | Riesgo alto | 18,8 | 67,8 | 49,0 | 60 | 94,2 |
| Guapi | 32,0 | Riesgo medio | 32,0 | — | — | 72 | 93,0 |
| Villa Rica | 19,1 | Riesgo medio | 19,1 | — | — | 168 | 83,6 |
| Padilla | 12,6 | Riesgo bajo | 12,6 | — | — | 276 | 73,0 |
| Jambaló | 12,5 | Riesgo bajo | 12,5 | — | — | 280 | 72,6 |
| Mercaderes | 12,4 | Riesgo bajo | 12,4 | — | — | 283 | 72,3 |
| Suárez | 11,5 | Riesgo bajo | 11,5 | — | — | 303 | 70,4 |
| Piamonte | 11,4 | Riesgo bajo | 11,4 | — | — | 306 | 70,1 |
| Cajibío | 11,1 | Riesgo bajo | 18,8 | 5,1 | -13,7 | 316 | 69,1 |
| Guachené | 9,5 | Riesgo bajo | 9,5 | — | — | 359 | 64,9 |
| Puerto Tejada | 8,6 | Riesgo bajo | 10,5 | 5,4 | -5,1 | 398 | 61,0 |
| Inzá | 8,4 | Riesgo bajo | 8,4 | — | — | 402 | 60,6 |
| Totoró | 7,8 | Riesgo bajo | 7,8 | — | — | 421 | 58,8 |
| Buenos Aires | 7,6 | Riesgo bajo | 7,6 | — | — | 430 | 57,9 |
| Patía | 6,3 | Riesgo bajo | 6,3 | — | — | 479 | 53,1 |
| San Sebastián | 6,3 | Riesgo bajo | 6,3 | — | — | 479 | 53,1 |
| Caloto | 6,3 | Riesgo bajo | 6,3 | — | — | 479 | 53,1 |
| Santander de Quilichao | 6,2 | Riesgo bajo | 2,1 | 8,4 | 6,3 | 488 | 52,2 |
| Puracé | 6,0 | Riesgo bajo | 0,0 | 13,2 | 13,2 | 497 | 51,3 |
| Rosas | 3,6 | Sin riesgo | 3,6 | — | — | 615 | 39,7 |
| El Tambo | 3,0 | Sin riesgo | 3,8 | 0,0 | -3,8 | 653 | 36,0 |
| Timbío | 2,6 | Sin riesgo | 1,0 | 3,2 | 2,2 | 678 | 33,6 |
| Silvia | 2,4 | Sin riesgo | 2,4 | — | — | 690 | 32,4 |
| Corinto | 1,7 | Sin riesgo | 1,7 | — | — | 746 | 26,9 |
| Bolívar | 1,6 | Sin riesgo | 0,0 | 19,0 | 19,0 | 755 | 26,0 |
| La Vega | 1,6 | Sin riesgo | 1,6 | — | — | 755 | 26,0 |
| Piendamó - Tunía | 1,5 | Sin riesgo | 1,5 | — | — | 765 | 25,0 |
| Morales | 1,5 | Sin riesgo | 1,5 | — | — | 765 | 25,0 |
| Miranda | 1,3 | Sin riesgo | 1,3 | — | — | 786 | 23,0 |
| Almaguer | 0,9 | Sin riesgo | 0,9 | — | — | 817 | 19,9 |
| Argelia | 0,0 | Sin riesgo | 0,0 | — | — | 913 | 10,5 |
| La Sierra | 0,0 | Sin riesgo | 0,0 | — | — | 913 | 10,5 |
| Páez | 0,0 | Sin riesgo | 0,0 | — | — | 913 | 10,5 |
| Santa Rosa | 0,0 | Sin riesgo | 0,0 | — | — | 913 | 10,5 |
| Sucre | 0,0 | Sin riesgo | 0,0 | — | — | 913 | 10,5 |
| Sotará Paispamba | 0,0 | Sin riesgo | 0,0 | — | — | 913 | 10,5 |
| Toribío | 0,0 | Sin riesgo | 0,0 | — | — | 913 | 10,5 |

## A2. Serie anual del Cauca, 2007–2025

IRCA departamental (fila #TODOS), promedio y mediana municipal, cobertura y porcentaje de registros sin IRCA rural.

| Año | IRCA dep. | Categoría | Prom. mun. | Mediana mun. | Municipios | % rural sin dato | % riesgo medio/alto |
|---:|---:|---|---:|---:|---:|---:|---:|
| 2007 | 30,7 | Riesgo medio | 33,6 | 19,1 | 32 | 84,4 | 59,5 |
| 2008 | 28,5 | Riesgo medio | 38,4 | 30,4 | 42 | 78,6 | 59,5 |
| 2009 | 27,1 | Riesgo medio | 34,8 | 28,2 | 42 | 69,0 | 57,2 |
| 2010 | 23,1 | Riesgo medio | 34,5 | 27,6 | 42 | 42,9 | 73,8 |
| 2011 | 25,0 | Riesgo medio | 31,2 | 23,8 | 41 | 56,1 | 75,6 |
| 2012 | 17,9 | Riesgo medio | 23,4 | 11,3 | 41 | 51,2 | 44,0 |
| 2013 | 16,5 | Riesgo medio | 20,4 | 9,3 | 41 | 58,5 | 31,8 |
| 2014 | 18,4 | Riesgo medio | 19,0 | 10,4 | 40 | 60,0 | 30,0 |
| 2015 | 14,7 | Riesgo medio | 17,5 | 7,5 | 40 | 67,5 | 32,5 |
| 2016 | 11,5 | Riesgo bajo | 15,6 | 6,8 | 40 | 85,0 | 20,0 |
| 2017 | 11,9 | Riesgo bajo | 15,1 | 10,1 | 41 | 80,5 | 29,3 |
| 2018 | 11,0 | Riesgo bajo | 14,8 | 7,0 | 42 | 83,3 | 19,1 |
| 2019 | 8,8 | Riesgo bajo | 12,3 | 5,6 | 42 | 78,6 | 14,3 |
| 2020 | 7,6 | Riesgo bajo | 9,0 | 3,5 | 36 | 63,9 | 8,4 |
| 2021 | 9,9 | Riesgo bajo | 11,4 | 6,7 | 36 | 55,6 | 19,4 |
| 2022 | 7,2 | Riesgo bajo | 7,8 | 5,3 | 34 | 52,9 | 8,8 |
| 2023 | 3,9 | Sin riesgo | 5,5 | 0,9 | 33 | 54,5 | 18,2 |
| 2024 | 3,3 | Sin riesgo | 3,8 | 1,3 | 33 | 57,6 | 9,1 |
| 2025 | 7,3 | Riesgo bajo | 7,7 | 6,1 | 38 | 78,9 | 10,6 |

## A3. Brecha urbano-rural por municipio

Brecha = IRCA rural − IRCA urbano. Solo se usan los registros con ambos datos; no se imputan faltantes. Un valor positivo indica peor situación rural. Se ordena por brecha promedio.

| Municipio | Años | Periodo | Urbano prom. | Rural prom. | Brecha prom. | Brecha máx. | Brecha mín. | Última brecha |
|---|---:|:---:|---:|---:|---:|---:|---:|---:|
| Totoró | 1 | 2012–2012 | 6,5 | 92,1 | 85,6 | 85,6 | 85,6 | 85,6 |
| Popayán | 5 | 2009–2013 | 9,2 | 80,4 | 71,2 | 81,4 | 61,6 | 81,4 |
| Santa Rosa | 3 | 2010–2012 | 24,1 | 88,0 | 63,9 | 74,5 | 51,0 | 66,3 |
| Toribío | 2 | 2010–2011 | 7,4 | 59,6 | 52,2 | 56,3 | 48,1 | 56,3 |
| Caloto | 6 | 2010–2015 | 12,7 | 64,1 | 51,4 | 70,1 | 25,0 | 63,5 |
| Sucre | 2 | 2011–2013 | 33,4 | 84,6 | 51,2 | 95,5 | 6,9 | 95,5 |
| Mercaderes | 2 | 2012–2014 | 9,6 | 60,3 | 50,7 | 67,4 | 34,0 | 34,0 |
| Jambaló | 1 | 2010–2010 | 26,9 | 76,7 | 49,8 | 49,8 | 49,8 | 49,8 |
| Páez | 5 | 2009–2013 | 16,6 | 61,1 | 44,5 | 68,9 | 15,0 | 15,0 |
| Rosas | 3 | 2008–2011 | 18,5 | 56,7 | 38,3 | 74,6 | 3,1 | 74,6 |
| Inzá | 10 | 2010–2024 | 5,7 | 36,0 | 30,4 | 95,3 | -4,7 | 24,8 |
| Bolívar | 2 | 2011–2025 | 14,9 | 44,7 | 29,8 | 40,6 | 19,0 | 19,0 |
| Piendamó - Tunía | 8 | 2013–2024 | 4,9 | 24,1 | 19,2 | 78,5 | -3,9 | 0,0 |
| Puracé | 7 | 2010–2025 | 19,5 | 36,4 | 16,9 | 35,0 | -1,1 | 13,2 |
| Sotará Paispamba | 3 | 2014–2017 | 13,1 | 26,7 | 13,6 | 31,6 | -8,4 | 17,5 |
| Caldono | 6 | 2020–2025 | 7,9 | 21,2 | 13,3 | 49,0 | -4,6 | 49,0 |
| Silvia | 5 | 2010–2015 | 8,0 | 21,3 | 13,2 | 61,2 | -5,5 | 0,0 |
| Timbío | 6 | 2012–2025 | 2,5 | 12,7 | 10,1 | 63,4 | -2,4 | 2,2 |
| Santander de Quilichao | 14 | 2007–2025 | 3,5 | 13,1 | 9,5 | 43,4 | -2,3 | 6,3 |
| Almaguer | 4 | 2008–2024 | 30,7 | 39,5 | 8,8 | 36,1 | -2,3 | 0,0 |
| Cajibío | 13 | 2008–2025 | 8,7 | 17,2 | 8,5 | 42,6 | -13,7 | -13,7 |
| Morales | 14 | 2007–2022 | 4,7 | 12,6 | 7,8 | 54,8 | -8,5 | -3,5 |
| Guapi | 5 | 2009–2024 | 28,9 | 34,9 | 6,0 | 42,3 | -18,6 | -18,6 |
| Patía | 10 | 2009–2019 | 6,0 | 11,8 | 5,9 | 56,8 | -5,1 | -4,9 |
| Puerto Tejada | 14 | 2007–2025 | 21,7 | 26,3 | 4,6 | 54,5 | -15,3 | -5,1 |
| Villa Rica | 7 | 2009–2024 | 21,8 | 25,9 | 4,1 | 17,5 | -11,0 | 0,4 |
| La Vega | 6 | 2010–2023 | 59,3 | 63,3 | 4,0 | 36,6 | -16,1 | 36,6 |
| La Sierra | 5 | 2014–2022 | 5,2 | 7,6 | 2,5 | 16,5 | -6,2 | 0,0 |
| Padilla | 18 | 2007–2024 | 13,8 | 14,8 | 1,0 | 24,8 | -16,7 | 24,8 |
| Argelia | 4 | 2013–2019 | 5,0 | 4,8 | -0,2 | 5,6 | -6,2 | 5,6 |
| Corinto | 14 | 2009–2023 | 2,5 | 1,5 | -1,1 | 5,8 | -4,5 | -0,1 |
| El Tambo | 9 | 2007–2025 | 7,1 | 3,5 | -3,6 | 10,2 | -18,3 | -3,8 |
| Buenos Aires | 7 | 2009–2023 | 11,9 | 8,0 | -3,9 | 39,8 | -33,4 | 0,0 |
| Miranda | 2 | 2010–2015 | 13,9 | 9,4 | -4,5 | -4,1 | -4,9 | -4,9 |
| Guachené | 17 | 2008–2024 | 24,7 | 18,9 | -5,8 | 19,3 | -22,4 | 0,0 |
| Piamonte | 2 | 2021–2022 | 32,2 | 26,0 | -6,2 | -0,6 | -11,8 | -0,6 |

## A4. Contexto nacional 2025

33 departamentos (fila #TODOS). Puesto: 1 = menor IRCA (mejor). Diferencia vs. mediana departamental (7,0).

| Departamento | IRCA | Categoría | Puesto | Dif. vs. mediana |
|---|---:|---|---:|---:|
| Quindío | 0,6 | Sin riesgo | 1 | -6,4 |
| Atlántico | 1,7 | Sin riesgo | 2 | -5,3 |
| Casanare | 2,3 | Sin riesgo | 3 | -4,7 |
| Archipiélago de San Andrés, Providencia y Santa Catalina | 2,3 | Sin riesgo | 3 | -4,7 |
| Caldas | 3,1 | Sin riesgo | 5 | -3,9 |
| Bogotá, D.C. | 3,9 | Sin riesgo | 6 | -3,1 |
| Huila | 4,1 | Sin riesgo | 7 | -2,9 |
| Norte de Santander | 4,1 | Sin riesgo | 7 | -2,9 |
| Valle del Cauca | 4,4 | Sin riesgo | 9 | -2,6 |
| Guaviare | 4,5 | Sin riesgo | 10 | -2,5 |
| Cundinamarca | 4,6 | Sin riesgo | 11 | -2,4 |
| La Guajira | 5,2 | Riesgo bajo | 12 | -1,8 |
| Antioquia | 5,2 | Riesgo bajo | 12 | -1,8 |
| Arauca | 6,5 | Riesgo bajo | 14 | -0,5 |
| Caquetá | 6,7 | Riesgo bajo | 15 | -0,3 |
| Santander | 6,9 | Riesgo bajo | 16 | -0,1 |
| Risaralda | 7,0 | Riesgo bajo | 17 | 0,0 |
| Boyacá | 7,2 | Riesgo bajo | 18 | 0,2 |
| Cauca | 7,3 | Riesgo bajo | 19 | 0,3 |
| Bolívar | 10,3 | Riesgo bajo | 20 | 3,3 |
| Meta | 11,2 | Riesgo bajo | 21 | 4,2 |
| Córdoba | 11,3 | Riesgo bajo | 22 | 4,3 |
| Cesar | 11,3 | Riesgo bajo | 22 | 4,3 |
| Magdalena | 12,0 | Riesgo bajo | 24 | 5,0 |
| Vichada | 12,0 | Riesgo bajo | 24 | 5,0 |
| Tolima | 12,8 | Riesgo bajo | 26 | 5,8 |
| Vaupés | 13,4 | Riesgo bajo | 27 | 6,4 |
| Amazonas | 14,1 | Riesgo medio | 28 | 7,1 |
| Sucre | 14,9 | Riesgo medio | 29 | 7,9 |
| Putumayo | 17,0 | Riesgo medio | 30 | 10,0 |
| Nariño | 22,5 | Riesgo medio | 31 | 15,5 |
| Guainía | 26,9 | Riesgo medio | 32 | 19,9 |
| Chocó | 42,0 | Riesgo alto | 33 | 35,0 |

## A5. Métricas de los modelos

Entrenamiento ≤2021 (463 observaciones) y prueba 2022–2025 (127). MAE y RMSE en puntos de IRCA; MAPE en porcentaje. La regresión simple es el modelo final.

| Modelo | Conjunto | n | MAE | RMSE | R² | MAPE (%) |
|---|---|---:|---:|---:|---:|---:|
| Naive (último valor) | Prueba (2022-2025) | 127 | 5,63 | 10,13 | -0,482 | 212,0 |
| Media histórica municipal | Prueba (2022-2025) | 127 | 14,26 | 20,23 | -4,912 | 660,1 |
| Regresión lineal simple | Prueba (2022-2025) | 127 | 5,26 | 8,57 | -0,060 | 215,9 |
| Regresión lineal simple | Entrenamiento (<=2021) | 463 | 7,98 | 12,34 | 0,734 | 154,6 |
| Regresión lineal completa | Prueba (2022-2025) | 127 | 5,25 | 8,29 | 0,007 | 202,4 |
| Regresión lineal completa | Entrenamiento (<=2021) | 463 | 7,86 | 12,23 | 0,738 | 157,3 |
| Random Forest | Prueba (2022-2025) | 127 | 5,88 | 8,07 | 0,060 | 305,3 |
| Random Forest | Entrenamiento (<=2021) | 463 | 6,58 | 9,87 | 0,830 | 146,3 |

## A6. Coeficientes del modelo final

Coeficientes estandarizados de la regresión simple reentrenada con todos los datos completos.

| Variable | Etiqueta | Coeficiente estandarizado |
|---|---|---:|
| irca_lag1 | IRCA del año anterior | 12,4180 |
| irca_roll3 | Media móvil de 3 años | 6,7312 |

## A7. Pronóstico 2026

Escenario con el IRCA 2025 y la media móvil 2023–2025. La banda usa el MAE de prueba (±5,26) y no es un intervalo de confianza. Se ordena de mayor a menor pronóstico.

| Municipio | IRCA 2025 | Pronóstico 2026 | Categoría | Cambio | IC inferior | IC superior |
|---|---:|---:|---|---:|---:|---:|
| Timbiquí | 37,0 | 28,7 | Riesgo medio | -8,3 | 23,4 | 33,9 |
| Caldono | 36,6 | 26,2 | Riesgo medio | -10,4 | 21,0 | 31,5 |
| Guapi | 32,0 | 25,8 | Riesgo medio | -6,2 | 20,5 | 31,1 |
| Villa Rica | 19,1 | 14,4 | Riesgo medio | -4,7 | 9,1 | 19,6 |
| Jambaló | 12,5 | 11,2 | Riesgo bajo | -1,3 | 6,0 | 16,5 |
| Piamonte | 11,4 | 10,7 | Riesgo bajo | -0,7 | 5,4 | 15,9 |
| Padilla | 12,6 | 10,7 | Riesgo bajo | -1,9 | 5,4 | 15,9 |
| Mercaderes | 12,4 | 10,4 | Riesgo bajo | -2,0 | 5,2 | 15,7 |
| Suárez | 11,5 | 8,9 | Riesgo bajo | -2,5 | 3,7 | 14,2 |
| Cajibío | 11,1 | 8,0 | Riesgo bajo | -3,1 | 2,8 | 13,3 |
| Guachené | 9,5 | 7,4 | Riesgo bajo | -2,1 | 2,2 | 12,7 |
| Inzá | 8,4 | 7,3 | Riesgo bajo | -1,1 | 2,0 | 12,6 |
| Puracé | 6,0 | 6,8 | Riesgo bajo | 0,8 | 1,6 | 12,1 |
| Puerto Tejada | 8,6 | 6,8 | Riesgo bajo | -1,8 | 1,6 | 12,1 |
| San Sebastián | 6,3 | 6,1 | Riesgo bajo | -0,2 | 0,9 | 11,4 |
| Totoró | 7,8 | 6,0 | Riesgo bajo | -1,9 | 0,7 | 11,2 |
| Buenos Aires | 7,6 | 5,7 | Riesgo bajo | -1,9 | 0,5 | 11,0 |
| Santander de Quilichao | 6,2 | 5,1 | Riesgo bajo | -1,1 | 0,0 | 10,3 |
| Patía | 6,3 | 4,9 | Sin riesgo | -1,4 | 0,0 | 10,2 |
| Caloto | 6,3 | 4,9 | Sin riesgo | -1,4 | 0,0 | 10,2 |
| La Vega | 1,6 | 4,2 | Sin riesgo | 2,6 | 0,0 | 9,5 |
| Rosas | 3,6 | 4,0 | Sin riesgo | 0,4 | 0,0 | 9,3 |
| El Tambo | 3,0 | 3,7 | Sin riesgo | 0,7 | 0,0 | 8,9 |
| Silvia | 2,4 | 3,4 | Sin riesgo | 1,0 | 0,0 | 8,6 |
| Timbío | 2,6 | 3,1 | Sin riesgo | 0,5 | 0,0 | 8,4 |
| Miranda | 1,3 | 2,4 | Sin riesgo | 1,1 | 0,0 | 7,7 |
| Bolívar | 1,6 | 2,3 | Sin riesgo | 0,7 | 0,0 | 7,5 |
| Morales | 1,5 | 2,1 | Sin riesgo | 0,6 | 0,0 | 7,4 |
| Corinto | 1,7 | 2,0 | Sin riesgo | 0,3 | 0,0 | 7,3 |
| Piendamó - Tunía | 1,5 | 2,0 | Sin riesgo | 0,5 | 0,0 | 7,2 |
| Sucre | 0,0 | 1,8 | Sin riesgo | 1,8 | 0,0 | 7,0 |
| Toribío | 0,0 | 1,6 | Sin riesgo | 1,6 | 0,0 | 6,8 |
| Almaguer | 0,9 | 1,5 | Sin riesgo | 0,6 | 0,0 | 6,8 |
| Sotará Paispamba | 0,0 | 1,3 | Sin riesgo | 1,3 | 0,0 | 6,5 |
| La Sierra | 0,0 | 1,1 | Sin riesgo | 1,1 | 0,0 | 6,4 |
| Santa Rosa | 0,0 | 1,0 | Sin riesgo | 1,0 | 0,0 | 6,3 |
| Argelia | 0,0 | 1,0 | Sin riesgo | 1,0 | 0,0 | 6,2 |
| Páez | 0,0 | 1,0 | Sin riesgo | 1,0 | 0,0 | 6,2 |

## A8. Diccionario de datos

Variables de la base limpia. Los códigos DANE se conservan como texto para no perder ceros a la izquierda. ND se convierte en nulo y no se imputa.

| Variable | Tipo | Descripción | Unidad | Fuente | Tratamiento |
|---|---|---|---|---|---|
| codigo_departamento | texto | Código DANE del departamento | código | SIVICAP | Se conserva como texto de 2 dígitos |
| departamento | texto | Nombre del departamento | nombre | SIVICAP | Se usa el nombre más frecuente por código |
| codigo_municipio | texto | Código DANE del municipio | código | SIVICAP | Texto de 5 dígitos; #TODOS identifica el agregado |
| municipio | texto | Nombre del municipio | nombre | SIVICAP | Se usa el catálogo DANE para el Cauca |
| anio | entero | Año de reporte | año | SIVICAP | Se convierte a entero |
| irca | decimal | Índice de Riesgo de la Calidad del Agua total | índice 0-100 | SIVICAP | ND se convierte en nulo |
| nivel_riesgo | texto | Categoría de riesgo total | categoría | SIVICAP | Se unifican variantes de escritura |
| irca_urbano | decimal | IRCA de la zona urbana | índice 0-100 | SIVICAP | ND se convierte en nulo |
| nivel_riesgo_urbano | texto | Categoría de riesgo urbana | categoría | SIVICAP | Se unifican variantes |
| irca_rural | decimal | IRCA de la zona rural | índice 0-100 | SIVICAP | ND se convierte en nulo; 66,4% sin dato en el Cauca (2007-2025) |
| nivel_riesgo_rural | texto | Categoría de riesgo rural | categoría | SIVICAP | Se unifican variantes; ND se conserva como nulo |
| categoria_calculada | texto | Categoría calculada con los umbrales oficiales | categoría | Cálculo propio | Sirve para validar la etiqueta reportada |
| coincide_categoria | booleano | Indica si la etiqueta reportada coincide con la calculada | verdadero/falso | Cálculo propio | Control de calidad |
| tiene_dato_rural | booleano | Indica si hay IRCA rural | verdadero/falso | Cálculo propio | Bandera de completitud |
| brecha_rural_urbano | decimal | IRCA rural menos IRCA urbano | puntos de índice | Cálculo propio | Positivo indica peor situación rural |
| es_agregado | booleano | Indica si la fila es el agregado departamental #TODOS | verdadero/falso | Cálculo propio | Evita doble conteo |

## A9. Auditoría de calidad

Chequeos aplicados en `src/cleaning.py`. La auditoría se regenera con `python -m src.cleaning`.

| Chequeo | Resultado | Detalle | Tratamiento |
|---|---:|---|---|
| Registros totales | 20212 | Base nacional descargada de datos.gov.co | Se conserva la base completa como referencia |
| Registros del Cauca | 736 | Municipios del Cauca, sin la fila agregada #TODOS | Base de análisis municipal |
| Filas agregadas del Cauca (#TODOS) | 19 | Una fila por año con el agregado departamental | Se separan para no duplicar el conteo municipal |
| Municipios del Cauca | 42 | Municipios distintos en la base municipal | Se validan contra el catálogo DANE de 42 municipios |
| Periodo | 2007-2025 | Años cubiertos por la base | Se usa 2007-2025 para la serie y 2025 para el corte transversal |
| Duplicados exactos (toda la base) | 0 | Filas idénticas en todas las columnas | No se eliminan si no hay evidencia de error; se documentan |
| Duplicados municipio-año en el Cauca | 0 | La llave municipio-año debería ser única | Se verificó que no hay duplicados |
| IRCA total nulo en el Cauca | 0 | Valores ND o vacíos después de convertir a número | Se excluyen del cálculo del indicador |
| IRCA urbano nulo en el Cauca | 5 | Valores ND o vacíos | Se mantiene como nulo; no se imputa |
| IRCA rural nulo en el Cauca | 489 | 66.4% de los registros municipales | No se imputa; el análisis rural se limita a casos completos |
| Etiquetas 'Bajo riesgo' / 'Alto riesgo' | 336 | Variantes de escritura de las categorías oficiales en la base original | Se unifican a 'Riesgo bajo' y 'Riesgo alto' |
| Categorías que no coinciden con el IRCA | 0 | Comparación entre la etiqueta reportada y la calculada con los umbrales | Se revisan; no se corrige la etiqueta original sin evidencia |
| IRCA = 0 en el Cauca | 52 | Puede ser un valor real o un problema de reporte | Se marca para revisión; no se elimina |
| IRCA = 100 en el Cauca | 4 | Categoría 'Inviable sanitariamente' | Se conserva: es un valor válido del índice |
| Municipios del Cauca con dato en 2025 | 38 | Cobertura del último año | El ranking 2025 cubre solo los municipios reportados |
| Años con dato de Popayán | 11 | La capital no aparece en los últimos cortes | Se advierte como limitación central |
| Filas agregadas departamentales (#TODOS) | 602 | Una fila por departamento y año; no existe un agregado nacional único | El contexto nacional se construye con los agregados departamentales |

## A10. Enlaces, reproducibilidad y notas metodológicas

- **Fuente:** SIVICAP – Calidad del Agua para Consumo Humano en Colombia, datos.gov.co, conjunto `nxt2-39c3`: https://www.datos.gov.co/d/nxt2-39c3
- **API:** https://www.datos.gov.co/resource/nxt2-39c3.json
- **Dashboard local:** `python -m streamlit run app.py` (http://localhost:8501).
- **Repositorio:** completar con la URL de GitHub al publicar.
- **Streamlit Community Cloud:** completar con la URL de la app al desplegar.
- **Notebooks:** `notebooks/01_limpieza.ipynb`, `02_analisis.ipynb`, `03_modelo.ipynb`.
- **Reproducción:** `python -m src.cleaning`, `python -m src.analysis`, `python -m src.model`, `python scripts/generar_informe.py`, `python scripts/generar_anexos.py`.
- **Video:** `video/guion_video.md`.

**Nota metodológica.** El IRCA es un indicador agregado del reporte municipal; no identifica hogares, veredas ni causas. Los datos rurales están subreportados (66,4% de los registros sin IRCA rural) y varios municipios tienen series cortas o faltantes. Los resultados deben validarse con la autoridad sanitaria y con datos de campo. El pronóstico es un escenario, no una certeza.
