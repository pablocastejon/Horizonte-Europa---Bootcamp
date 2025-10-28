# 📊 Resumen del Preprocesado de Datos - Horizonte Europa PM9

> **Última actualización:** Octubre 2025  
> **Notebook:** `notebooks/01_preprocesado.ipynb`  
> **Dataset:** Proyectos administrativos del Programa Marco 9 (Horizonte Europa)

---

## 🎯 Objetivo del Preprocesado

Limpiar y preparar datos administrativos de proyectos europeos para su análisis y visualización en dashboard, **respetando la naturaleza administrativa de los datos** (preservando valores nulos que forman parte natural de la información).

---

## 📋 Dataset Original

| Característica | Detalle |
|---------------|---------|
| **Archivo** | `data/9PM_bootcamp1.xlsx` |
| **Formato** | Excel (carga con `pd.read_excel`) |
| **Registros iniciales** | ~730 proyectos |
| **Columnas** | 21 variables |
| **Período** | Proyectos de Horizonte Europa |
| **Clave primaria** | `Ref.CSIC` |

---

## 🔧 Transformaciones Realizadas

### 1️⃣ **Renombrado de Variables**

Cambio de nombres ambiguos por nombres descriptivos:

| Variable Original | Nuevo Nombre |
|------------------|--------------|
| `Concedido` | `Importe Concedido` |
| `CSIC` | `Participantes CSIC` |
| `España (no CSIC)` | `Participantes España (no CSIC)` |
| `Total (Csic, Esp. y otros)` | `Total Participantes` |

---

### 2️⃣ **Clasificación de Variables**

Las variables se clasificaron según su función administrativa:

#### 🔹 **Identificadores** (códigos únicos)
- `Ref.CSIC` ← Clave primaria
- `Ref.UE` 
- `Centro`
- `Acrónimo del proyecto`

#### 🔹 **Categóricas** (valores discretos)
- `Situación`
- `Programa`
- `Acción clave`
- `Convocatoria`
- `Cód.área`
- `Nombre Centro IP`

#### 🔹 **Descriptivas** (texto libre)
- `Título`
- `Resumen`
- `Keywords`

#### 🔹 **Numéricas** (medidas)
- `Importe Concedido` → float64
- `Duración (meses)` → Int64
- `Participantes CSIC` → Int64
- `Participantes España (no CSIC)` → Int64
- `Total Participantes` → Int64

#### 🔹 **Temporales** (fechas)
- `Comienzo` → datetime64
- `Final` → datetime64

---

### 3️⃣ **Conversión de Tipos de Datos**

**⚠️ Consideración crítica:** Variables como `Centro` y `Ref.UE` contienen números pero son **códigos identificadores**, NO variables numéricas.

```python
# Variables enteras (sin decimales)
df['Duración (meses)'] = df['Duración (meses)'].astype('Int64')
df['Participantes CSIC'] = df['Participantes CSIC'].astype('Int64')
df['Participantes España (no CSIC)'] = df['Participantes España (no CSIC)'].astype('Int64')
df['Total Participantes'] = df['Total Participantes'].astype('Int64')

# Códigos identificadores (cargados como string desde Excel)
# dtype={'Centro': str, 'Ref.UE': str} en pd.read_excel()

# Cód.área (código → string para mapeo posterior)
df['Cód.área'] = pd.to_numeric(df['Cód.área'], errors='coerce').astype('Int64')
df['Cód.área'] = df['Cód.área'].astype(str)

# Variables temporales
df['Comienzo'] = pd.to_datetime(df['Comienzo'], errors='coerce')
df['Final'] = pd.to_datetime(df['Final'], errors='coerce')
```

---

### 4️⃣ **Eliminación de Duplicados**

```python
# Eliminar filas con Ref.CSIC nulo (clave primaria)
df = df.dropna(subset=['Ref.CSIC'])

# Eliminar duplicados por Ref.CSIC (mantener primera ocurrencia)
df = df.drop_duplicates(subset=['Ref.CSIC'], keep='first')
```

**Resultado:**
- ✅ Nulos eliminados: Variable
- ✅ Duplicados eliminados: Variable
- ✅ **Dataset final: 719 proyectos únicos**

---

### 5️⃣ **Normalización de Nombres de Centros**

**Problema:** `Nombre Centro IP` contiene variaciones para el mismo centro (abreviaturas, espacios extra).

**Solución:** Normalizar usando el código `Centro` como referencia:

```python
# Crear mapeo: código centro → nombre más frecuente
for centro in df['Centro'].unique():
    nombres = df[df['Centro'] == centro]['Nombre Centro IP']
    nombre_frecuente = nombres.mode()[0]
    centro_nombre_map[centro] = nombre_frecuente

# Aplicar normalización
df['Nombre Centro IP Normalizado'] = df['Centro'].map(centro_nombre_map)
```

**Resultado:**
- ✅ Centros con múltiples nombres detectados y unificados
- ✅ Nueva columna: `Nombre Centro IP Normalizado`

---

### 6️⃣ **Limpieza de Texto**

Normalización de todas las columnas de texto:

```python
for col in text_columns:
    df[col] = df[col].str.strip()  # Eliminar espacios inicio/final
    df[col] = df[col].str.replace(r'\s+', ' ', regex=True)  # Espacios múltiples → uno solo
```

---

### 7️⃣ **Transformación de Áreas Científicas**

**Contexto:** `Cód.área` contiene códigos de las **antiguas áreas científicas del CSIC**. Se mapean a las **nuevas categorías globales**.

**Fuente:** Archivo `data/maestros.xlsx` con mapeo de códigos antiguos → nuevas áreas.

| Código Antiguo | Nueva Categoría |
|----------------|-----------------|
| `010101`, `010102`, ... | `Vida` |
| `020101`, `020102`, ... | `Materia` |
| `030101`, `030102`, ... | `Sociedad` |
| `040101`, `040102`, ... | `Central` |
| `<NA>` | `Desconocido` |

```python
# Cargar diccionario de áreas
areas_dict = pd.read_excel('../data/maestros.xlsx', sheet_name='Hoja1')
areas_dict['Cód.área'] = areas_dict['Cód.área'].astype(str)

# Crear mapeo
codigo_a_categoria = dict(zip(areas_dict['Cód.área'], areas_dict['Area']))

# Transformar
df['Area'] = df['Cód.área'].map(codigo_a_categoria)
```

**Resultado:**
- ✅ Nueva variable: `Area`
- ✅ Categorías: Vida, Materia, Sociedad, Central, Desconocido
- ✅ Distribución verificada (sin códigos sin mapear)

---

### 8️⃣ **Variables Derivadas**

Se crearon **5 variables derivadas** para facilitar análisis:

| Variable Derivada | Tipo | Descripción |
|------------------|------|-------------|
| **Año Inicio** | `string` | Año de inicio del proyecto (sin decimales) |
| **Año Fin** | `string` | Año de finalización del proyecto (sin decimales) |
| **Presupuesto Mensual** | `float64` | Importe Concedido / Duración (meses) |
| **Duración (categoría)** | `category` | Corto (≤12 meses), Medio (12-36), Largo (>36) |
| **Presupuesto (categoría)** | `category` | Pequeño (≤150k€), Mediano (150k-500k), Grande (>500k) |

```python
# Años como strings (sin decimales)
df['Año Inicio'] = df['Comienzo'].dt.year.astype('Int64').astype(str)
df['Año Fin'] = df['Final'].dt.year.astype('Int64').astype(str)

# Presupuesto mensual
df['Presupuesto Mensual'] = (df['Importe Concedido'] / df['Duración (meses)']).round(2)

# Categorías de duración
df['Duración (categoría)'] = pd.cut(df['Duración (meses)'], 
                                     bins=[0, 12, 36, float('inf')], 
                                     labels=['Corto', 'Medio', 'Largo'])

# Categorías de presupuesto
df['Presupuesto (categoría)'] = pd.cut(df['Importe Concedido'],
                                        bins=[0, 150000, 500000, float('inf')],
                                        labels=['Pequeño', 'Mediano', 'Grande'])
```

---

## 📤 Exportación de Datos Limpios

Los datos preprocesados se exportan en **dos formatos**:

```python
df.to_csv('../data/9PM_bootcamp_clean.csv', index=False, encoding='utf-8')
df.to_excel('../data/9PM_bootcamp_clean.xlsx', index=False)
```

**Archivos generados:**
- ✅ `data/9PM_bootcamp_clean.csv` (formato ligero para dashboard)
- ✅ `data/9PM_bootcamp_clean.xlsx` (con formato para Excel)

---

## 📊 Resumen Estadístico Final

Después del preprocesado completo:

| Métrica | Valor |
|---------|-------|
| **Total proyectos** | 719 |
| **Total variables** | 26 (21 originales + 5 derivadas) |
| **Duplicados eliminados** | Variable según ejecución |
| **Nulos en Ref.CSIC eliminados** | Variable según ejecución |
| **Rango temporal** | 2021 - 2027 |
| **Presupuesto total** | ~XXX millones € |
| **Presupuesto medio** | ~XXX k€ por proyecto |

### Distribución por Área Científica

| Área | Proyectos | % |
|------|-----------|---|
| Vida | ~XXX | XX% |
| Materia | ~XXX | XX% |
| Sociedad | ~XXX | XX% |
| Central | ~XXX | XX% |
| Desconocido | ~XXX | XX% |

---

## ⚠️ Consideraciones Importantes

### 🔹 **Datos Administrativos (No Experimentales)**

- ✅ Los valores nulos **NO se eliminan** (forman parte natural de los datos)
- ✅ Campos vacíos son válidos (no todos los proyectos tienen todos los datos)
- ✅ Se preserva la integridad administrativa del dataset

### 🔹 **Variables "Numéricas" que son Códigos**

Variables como `Centro`, `Ref.UE`, `Cód.área` contienen números pero:
- ❌ NO deben usarse para análisis estadísticos (correlaciones, promedios)
- ✅ Son identificadores categóricos
- ✅ Se cargan y mantienen como strings

### 🔹 **Clave Primaria**

- `Ref.CSIC` es la **clave primaria única**
- Cualquier duplicado se elimina (manteniendo primera ocurrencia)
- Es el identificador único de cada proyecto

### 🔹 **Normalización de Centros**

- Los nombres de centros pueden tener variaciones
- Se usa el código `Centro` como referencia única
- Variable normalizada: `Nombre Centro IP Normalizado`

---

## 🚀 Uso del Notebook

### **Ejecución:**

```bash
# Activar entorno virtual
source venv/bin/activate

# Abrir notebook
jupyter notebook notebooks/01_preprocesado.ipynb

# Ejecutar TODAS las celdas en orden
```

### **Salidas esperadas:**

1. ✅ Archivos generados en `data/`:
   - `9PM_bootcamp_clean.csv`
   - `9PM_bootcamp_clean.xlsx`

2. ✅ 719 proyectos únicos

3. ✅ 26 variables (21 originales + 5 derivadas)

4. ✅ Todos los tipos de datos correctos

---

## 📚 Próximos Pasos

Después del preprocesado:

1. ✅ **Análisis exploratorio** → `notebooks/02_EDA.ipynb`
2. ✅ **Dashboard interactivo** → `cd app && streamlit run dashboard.py`
3. ✅ **Análisis específicos** según necesidades

---

## 🛠️ Tecnologías Utilizadas

- **pandas 2.1.3** - Manipulación de datos
- **numpy 1.26.2** - Operaciones numéricas
- **openpyxl 3.1.2** - Lectura/escritura de Excel
- **Jupyter Notebook** - Entorno de ejecución

---

## 📝 Notas Técnicas

### **Preservación de Leading Zeros**

Variables como `Centro` pueden tener códigos como `"030102"`. Para preservar los ceros iniciales:

```python
df = pd.read_excel(
    '../data/9PM_bootcamp1.xlsx',
    dtype={'Centro': str, 'Ref.UE': str}  # ← Forzar como string desde la carga
)
```

### **Conversión de Años sin Decimales**

Para obtener años como strings sin el `.0`:

```python
# ❌ Incorrecto: produce "2021.0"
df['Año'] = df['Fecha'].dt.year.astype(str)

# ✅ Correcto: produce "2021"
df['Año'] = df['Fecha'].dt.year.astype('Int64').astype(str)
```

### **Manejo de Valores Nulos en Int64**

El tipo `Int64` (con I mayúscula) permite valores nulos en columnas enteras:

```python
df['Duración (meses)'] = df['Duración (meses)'].astype('Int64')  # Permite <NA>
```

---

**✅ Dataset preprocesado listo para análisis y visualización**

