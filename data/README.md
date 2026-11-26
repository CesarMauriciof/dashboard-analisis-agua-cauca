# Datos del proyecto IRCA Cauca

## Fuente

- **Conjunto:** `nxt2-39c3` — *Calidad del Agua para Consumo Humano en Colombia (SIVICAP)*.
- **Entidad:** Ministerio de Salud y Protección Social / Instituto Nacional de Salud.
- **Portal:** https://www.datos.gov.co/d/nxt2-39c3
- **API JSON:** https://www.datos.gov.co/resource/nxt2-39c3.json
- **Actualización del conjunto:** 04/11/2026.
- **Consulta:** 25/11/2026.
- **Cobertura:** 20.212 registros nacionales; 736 registros municipales del Cauca (42 municipios, 2007–2025); 19 agregados departamentales del Cauca (`#TODOS`); 1.019 municipios y 33 departamentos en el corte nacional 2025.
- **Datos personales:** no contiene información personal. El IRCA es un indicador agregado por municipio y año.
- **Licencia de uso:** datos abiertos de datos.gov.co; se conserva la atribución a MinSalud/INS.

## Archivos

### Crudos (`data/raw/`)

| Archivo | Registros | Tamaño | SHA-256 | Descripción |
|---|---:|---:|---|---|
| `irca_colombia_raw.json` | 20.212 | 5.535.783 B | `5fa165a7292aaa87c7e8d27a5dffb352f9da8dcdfaa82737fa73b2691cf1972c` | Respuesta original de la API. **Fuente canónica del pipeline.** |
| `irca_colombia_raw.csv` | 20.212 | 2.019.065 B | `9b163bef9a52d129997b51009de50342248fae23e0b2edf268b2a0a421316102` | Exportación CSV alternativa descargada en la misma consulta. No se usa en el pipeline. |

> El endpoint CSV de exportación presentó problemas al momento de la consulta. El JSON es la fuente reproducible; el CSV incluido es una exportación alternativa y se conserva como respaldo legible.

### Limpios (`data/clean/`)

| Archivo | Filas | Columnas | SHA-256 | Descripción |
|---|---:|---:|---|---|
| `irca_colombia_clean.csv` | 20.212 | 16 | `e05b331a7a998f25f44b784d94a7e7f3ecdb7de3592b9a7d271f6b95a9d5c0c0` | Base nacional limpia y normalizada. |
| `irca_cauca_municipal.csv` | 736 | 16 | `41fa85e44f6784e830c3031ce6e6ba9f2c492ee15b14e78d6f47dac791d45e6a` | 42 municipios del Cauca, 2007–2025. Base principal del análisis. |
| `irca_cauca_departamento.csv` | 19 | 16 | `55ba4905e97a643f26add2dfba0795c21d153e295b14c9af98aa0240a4aa796f` | Agregados `#TODOS` del Cauca, un registro por año. |
| `irca_nacional_municipal_2025.csv` | 1.019 | 16 | `dc142fea73d8da13652393f103413c19170311eaa02442b3f992893e5b0de159` | Municipios del país en el corte 2025. |
| `irca_nacional_departamental_2025.csv` | 33 | 16 | `9c17cc2e0a596558e3d40063dfe5ea20c50c8f123b2e9c12f5d98e06b29a0d35` | Agregados departamentales en el corte 2025. |
| `diccionario_datos.csv` | 16 | 6 | `e3b000d45dd10b398660633f00fa114748ac814667fe7d099947fae1f322ec25` | Diccionario de variables y tratamientos. |

## Descarga reproducible

En Linux/macOS o Git Bash:

```bash
curl -L 'https://www.datos.gov.co/resource/nxt2-39c3.json?$limit=50000' \
  -o data/raw/irca_colombia_raw.json
```

En PowerShell:

```powershell
Invoke-WebRequest `
  -Uri 'https://www.datos.gov.co/resource/nxt2-39c3.json?%24limit=50000' `
  -OutFile 'data/raw/irca_colombia_raw.json'
```

La API devuelve como máximo 50.000 registros por petición; el conjunto consultado tiene 20.212, por lo que una sola petición alcanza.

## Diccionario de variables

| Variable | Tipo | Descripción | Tratamiento |
|---|---|---|---|
| `codigo_departamento` | texto | Código DANE del departamento (2 dígitos). | Se conserva como texto. |
| `departamento` | texto | Nombre del departamento. | Se usa el nombre más frecuente por código. |
| `codigo_municipio` | texto | Código DANE del municipio (5 dígitos). | Texto; `#TODOS` identifica el agregado. |
| `municipio` | texto | Nombre del municipio. | Se usa el catálogo DANE para el Cauca. |
| `anio` | entero | Año de reporte. | Convertido a entero. |
| `irca` | decimal | Índice de Riesgo de la Calidad del Agua total (0–100). | `ND` se convierte en nulo. |
| `nivel_riesgo` | texto | Categoría de riesgo total. | Se unifican variantes de escritura. |
| `irca_urbano` | decimal | IRCA de la zona urbana (0–100). | `ND` se convierte en nulo. |
| `nivel_riesgo_urbano` | texto | Categoría de riesgo urbana. | Se unifican variantes. |
| `irca_rural` | decimal | IRCA de la zona rural (0–100). | `ND` se convierte en nulo; 66,4% sin dato en el Cauca. |
| `nivel_riesgo_rural` | texto | Categoría de riesgo rural. | Se unifican variantes; `ND` se conserva como nulo. |
| `categoria_calculada` | texto | Categoría calculada con los umbrales oficiales. | Cálculo propio. |
| `coincide_categoria` | booleano | Indica si la etiqueta reportada coincide con la calculada. | Control de calidad. |
| `tiene_dato_rural` | booleano | Indica si hay IRCA rural. | Bandera de completitud. |
| `brecha_rural_urbano` | decimal | IRCA rural menos IRCA urbano. | Positivo indica peor situación rural. |
| `es_agregado` | booleano | Indica si la fila es el agregado departamental `#TODOS`. | Evita doble conteo. |

## Decisiones de limpieza

1. **Nombres de columnas:** se traducen a español sin tildes y con snake_case (`a_o` → `anio`, `ircaurbano` → `irca_urbano`, etc.).
2. **Valores faltantes:** `ND`, `N/D`, `Sin dato` y vacíos se convierten en nulos. **No se imputan** los datos rurales faltantes.
3. **Categorías de riesgo:** se unifican variantes como `Bajo riesgo` → `Riesgo bajo` y `Alto riesgo` → `Riesgo alto`. Se conserva la categoría original y se calcula una categoría con los umbrales oficiales.
4. **Agregados:** las filas `#TODOS` se separan del análisis municipal para no duplicar conteos. El Cauca tiene 19 agregados departamentales (uno por año).
5. **Catálogo municipal:** se validan los 42 municipios del Cauca contra el catálogo DANE incluido en `src/config.py`.
6. **Duplicados:** se verifican duplicados exactos y duplicados municipio-año. En la base consultada no hay duplicados.
7. **Ceros y valores extremos:** se conservan. Los 52 ceros del Cauca y los 4 valores de 100 se marcan para revisión, pero no se eliminan sin evidencia de error.
8. **Cobertura 2025:** 38 de 42 municipios tienen dato. Faltan Balboa, Florencia, López de Micay y Popayán.
9. **Popayán:** solo tiene datos de 2008 a 2019; se declara como limitación central.
10. **Codificación:** los CSV se guardan en UTF-8 con BOM para que Excel abra correctamente las tildes.

## Auditoría de calidad

El archivo `reports/tablas/calidad_datos.csv` resume los chequeos. Resultados clave:

- 20.212 registros nacionales; 736 registros municipales del Cauca; 19 agregados departamentales.
- 0 duplicados exactos y 0 duplicados municipio-año en el Cauca.
- 489 de 736 registros municipales sin IRCA rural (**66,4%**); 5 sin IRCA urbano.
- 336 filas con variantes `Bajo riesgo` / `Alto riesgo` unificadas.
- 0 categorías que no coincidan con el IRCA calculado.
- 52 ceros y 4 valores de 100 en el Cauca, conservados y marcados.
- 38 municipios con dato en 2025; 11 años con dato de Popayán.
- 602 agregados departamentales (`#TODOS`) en la base nacional; no existe un agregado nacional único.

## Reproducibilidad

Para regenerar los archivos limpios y la auditoría:

```bash
python -m src.cleaning
```

El script lee `data/raw/irca_colombia_raw.json`, aplica las reglas anteriores y reescribe `data/clean/` y `reports/tablas/calidad_datos.csv`. Los hashes SHA-256 permiten verificar que los archivos no cambiaron respecto a la versión entregada.