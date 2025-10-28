# 🇪🇺 Horizonte Europa - Análisis de Proyectos del 9PM

## 📋 Descripción del Proyecto

Este proyecto realiza un **análisis exhaustivo de los proyectos del programa Horizonte Europa del 9º Programa Marco (9PM)** obtenidos del CSIC. Incluye preprocesamiento de datos, análisis exploratorio (EDA) y un dashboard interactivo para visualización y búsqueda de proyectos.

El objetivo es proporcionar insights sobre:
- Distribución temporal de proyectos
- Análisis presupuestario
- Participación por centros de investigación
- Áreas científicas más activas
- Palabras clave y temáticas principales

---

## 🗂️ Estructura del Proyecto

```
Horizonte-Europa---Bootcamp/
├── github_repository/
│   ├── app/
│   │   └── dashboard.py              # Dashboard interactivo con Streamlit
│   ├── data/
│   │   └── 9PM_bootcamp_clean.xlsx   # Dataset limpio (694 proyectos, 27 variables)
│   ├── notebooks/
│   │   ├── 01_preprocesado.ipynb     # Limpieza y preprocesamiento de datos
│   │   └── 02_EDA.ipynb              # Análisis Exploratorio de Datos
│   ├── docs/                         # Documentación adicional
│   ├── .streamlit/                   # Configuración de Streamlit
│   ├── requirements.txt              # Dependencias del proyecto
│   ├── PREPROCESADO_RESUMEN.md      # Resumen del preprocesamiento
│   └── README.md                     # Este archivo
└── entorno/
    └── venv/                         # Entorno virtual Python
```

---

## 📊 Dataset

**Archivo:** `9PM_bootcamp_clean.xlsx`

**Características:**
- **694 proyectos** del programa Horizonte Europa
- **27 variables** por proyecto

**Variables principales:**
- `Ref.CSIC`, `Ref.UE`: Referencias del proyecto
- `Situación`: Estado del proyecto
- `Programa`, `Acción clave`: Clasificación del proyecto
- `Título`, `Acrónimo del proyecto`: Identificadores
- `Comienzo`, `Final`, `Duración (meses)`: Temporalidad
- `Importe Concedido`, `Presupuesto Mensual`: Información financiera
- `Centro`, `Nombre Centro IP`, `Nombre Centro IP Normalizado`: Institución responsable
- `Participantes CSIC`, `Participantes España (no CSIC)`, `Total Participantes`: Colaboradores
- `Cód.área`, `Area`: Área científica
- `Resumen`, `Keywords`: Descripción temática
- `Año Inicio`, `Año Fin`: Variables derivadas para análisis temporal
- `Duración (categoría)`, `Presupuesto (categoría)`: Variables categorizadas

---

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.12+
- pip

### 1. Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd Horizonte-Europa---Bootcamp/github_repository
```

### 2. Crear y Activar Entorno Virtual
```bash
# Crear entorno virtual
python3 -m venv ../entorno/venv

# Activar entorno virtual
source ../entorno/venv/bin/activate  # Linux/Mac
# o
..\entorno\venv\Scripts\activate     # Windows
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

**Librerías principales:**
- `streamlit==1.29.0` - Framework del dashboard
- `pandas==2.1.3` - Manipulación de datos
- `plotly==5.18.0` - Visualizaciones interactivas
- `matplotlib==3.8.2`, `seaborn==0.13.0` - Visualizaciones estáticas
- `openpyxl==3.1.2` - Lectura de archivos Excel
- `jupyter==1.0.0` - Notebooks interactivos

---

## 📓 Notebooks

### 1. **01_preprocesado.ipynb**
Limpieza y preprocesamiento de datos raw del CSIC.

**Tareas realizadas:**
- Carga de datos crudos
- Limpieza de valores nulos y duplicados
- Normalización de nombres de centros
- Creación de variables derivadas (`Año Inicio`, `Año Fin`, categorías)
- Conversión de tipos de datos
- Exportación a `9PM_bootcamp_clean.xlsx`

### 2. **02_EDA.ipynb**
Análisis Exploratorio de Datos completo.

**Secciones:**
1. **Análisis Temporal:** Evolución de proyectos por año
2. **Análisis Presupuestario:** Distribución de presupuestos y estadísticas
3. **Análisis por Áreas Científicas:** Top áreas y distribución
4. **Análisis de Keywords:** WordCloud y términos más frecuentes
5. **Análisis por Centros:** Top centros por proyectos y presupuesto

**Visualizaciones:**
- Gráficos de líneas temporales
- Histogramas y boxplots
- Gráficos de barras
- WordClouds
- Tablas estadísticas

---

## 🎨 Dashboard Interactivo

### Ejecutar el Dashboard

```bash
# Activar entorno virtual
source ../entorno/venv/bin/activate

# Navegar a la carpeta app
cd app

# Ejecutar dashboard
streamlit run dashboard.py
```

El dashboard se abrirá automáticamente en **http://localhost:8501**

### Características del Dashboard

#### 🎯 **Barra Lateral de Filtros**
Filtra datos en tiempo real por:
- Situación del proyecto
- Programa
- Acción clave
- Área Científica
- Centro de investigación
- Rango de años (Inicio)
- Rango de presupuesto

#### 📑 **5 Pestañas Principales**

##### 1️⃣ **Resumen General**
- KPIs principales (total proyectos, presupuesto total, promedio, duración)
- Distribución por situación (gráfico de pastel)
- Evolución temporal de proyectos
- Top 10 áreas científicas
- Top 10 centros por número de proyectos

##### 2️⃣ **Por Programa**
- Distribución de proyectos por programa
- Distribución por acción clave
- Tabla resumen con estadísticas por programa

##### 3️⃣ **Análisis Presupuestario**
- Distribución de presupuestos (histograma)
- Estadísticas descriptivas
- Boxplot de presupuestos por programa
- Relación presupuesto vs duración (scatter plot)

##### 4️⃣ **Por Centros**
- Top 15 centros por número de proyectos
- Top 15 centros por presupuesto total
- Tabla detallada con estadísticas por centro

##### 5️⃣ **Búsqueda Avanzada**

**🔍 Búsqueda Inteligente:**
- Búsqueda simultánea en múltiples campos de texto
- Campos incluidos:
  - Título
  - Acrónimo del proyecto
  - Resumen
  - Keywords
  - Nombre Centro IP Normalizado
- Estadísticas de coincidencias por campo
- Descarga de resultados en CSV

**🔎 Búsqueda Detallada:**
- Filtros individuales por campo específico:
  - Ref.UE
  - Título del Proyecto
  - Investigador Principal
  - Acrónimo
  - Programa
  - Centro
  - Keywords
  - Área Científica
- Visualización de resultados en tabla interactiva
- Descarga de resultados filtrados

#### 📥 **Funcionalidades Adicionales**
- Todos los gráficos son **interactivos** (zoom, hover, descarga)
- **Descarga de datos filtrados** en formato CSV con timestamp
- **Tablas interactivas** con ordenamiento
- **Responsive design** adaptable a diferentes pantallas

---

## 🛠️ Tecnologías Utilizadas

### Lenguajes
- Python 3.12

### Librerías de Datos
- **pandas** - Manipulación y análisis de datos
- **numpy** - Operaciones numéricas
- **openpyxl** - Lectura de archivos Excel

### Visualización
- **Plotly** - Gráficos interactivos (dashboard)
- **Matplotlib** - Gráficos estáticos (notebooks)
- **Seaborn** - Visualizaciones estadísticas
- **WordCloud** - Nubes de palabras

### Desarrollo Web
- **Streamlit** - Framework para dashboard interactivo

### Análisis Estadístico
- **scipy** - Análisis estadístico avanzado

### Entorno de Desarrollo
- **Jupyter** - Notebooks interactivos
- **VS Code** - Editor de código

---

## 📈 Resultados Clave

### Estadísticas Generales
- **694 proyectos** analizados del Horizonte Europa 9PM
- Presupuesto total gestionado: **Millones de euros**
- Duración promedio: **Variable según categoría**
- **Múltiples centros CSIC** participantes

### Insights Principales
- Identificación de áreas científicas más activas
- Distribución de presupuestos por programa y centro
- Evolución temporal de la participación
- Palabras clave y temáticas predominantes
- Centros líderes en número de proyectos y financiación

---

## 🤝 Contribuciones

Este proyecto es parte del **Bootcamp de Horizonte Europa del CSIC**.

---

## 📝 Notas Técnicas

### Convenciones de Datos
- **Tipos de datos críticos:** Algunas columnas requieren tipo `str` para evitar problemas de visualización (años, códigos, referencias)
- **Valores nulos:** Gestionados con `fillna()` en visualizaciones
- **Normalización:** Los nombres de centros están normalizados en `Nombre Centro IP Normalizado`

### Configuración de Streamlit
La configuración del dashboard se encuentra en `.streamlit/config.toml` (si existe).

---

## 📧 Contacto

Para más información sobre el proyecto o colaboraciones, contacta a través del repositorio.

---

## 📄 Licencia

Este proyecto es de uso interno del CSIC para análisis de datos del programa Horizonte Europa.

---

**Última actualización:** Octubre 2025
