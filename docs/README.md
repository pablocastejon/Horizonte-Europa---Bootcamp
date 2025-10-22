# 📊 Dashboard Interactivo - 9PM Bootcamp

Dashboard interactivo desarrollado con **Streamlit** para explorar y visualizar datos administrativos del Bootcamp 9PM Horizonte Europa.

## 🎯 Objetivos del Proyecto

Este proyecto tiene como objetivo proporcionar una herramienta interactiva para:
- Explorar datos administrativos del bootcamp
- Visualizar patrones y tendencias
- Facilitar la toma de decisiones basada en datos
- Realizar análisis exploratorio de datos (EDA)

## 📁 Estructura del Proyecto

```
Horizonte-Europa---Bootcamp/
│
├── 📂 data/                    # Archivos de datos
│   └── 9PM_bootcamp.xlsx       # Datos originales
│
├── 📂 notebooks/               # Notebooks de análisis
│   ├── 01_preprocesado.ipynb  # Limpieza y preparación de datos
│   └── 02_EDA.ipynb            # Análisis exploratorio de datos
│
├── 📂 app/                     # Aplicación Streamlit
│   └── dashboard.py            # Dashboard interactivo
│
├── 📂 docs/                    # Documentación
│   └── README.md               # Este archivo
│
├── requirements.txt            # Dependencias del proyecto
├── .gitignore                 # Archivos ignorados por Git
└── venv/                      # Entorno virtual (no versionado)
```

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/pablocastejon/Horizonte-Europa---Bootcamp.git
cd Horizonte-Europa---Bootcamp
```

### 2. Crear y activar entorno virtual

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 📊 Uso del Proyecto

### Notebooks de Análisis

#### 1. Notebook de Preprocesado (`01_preprocesado.ipynb`)

Este notebook se encarga de:
- ✅ Carga de datos desde Excel
- 🧹 Limpieza de datos (espacios, formatos, etc.)
- ❌ Manejo de valores nulos
- 🔁 Detección y tratamiento de duplicados
- ➕ Creación de nuevas columnas derivadas
- 💾 Exportación de datos limpios

**Para ejecutar:**
```bash
jupyter notebook notebooks/01_preprocesado.ipynb
```

#### 2. Notebook de EDA (`02_EDA.ipynb`)

Este notebook realiza:
- 📈 Estadísticas descriptivas
- 📊 Análisis univariado de variables
- 🔗 Análisis de correlaciones
- 📉 Visualizaciones estáticas e interactivas
- 🎯 Identificación de patrones y tendencias
- 💡 Generación de insights

**Para ejecutar:**
```bash
jupyter notebook notebooks/02_EDA.ipynb
```

### Dashboard de Streamlit

El dashboard proporciona una interfaz interactiva para:
- 📋 Ver resumen general de los datos
- 📊 Explorar variables categóricas
- 📈 Analizar variables numéricas
- 🔗 Examinar correlaciones entre variables
- 🎨 Visualizaciones interactivas con Plotly

**Para ejecutar el dashboard:**

```bash
cd app
streamlit run dashboard.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📦 Dependencias Principales

### Core
- `streamlit==1.29.0` - Framework para el dashboard
- `pandas==2.1.3` - Manipulación de datos
- `numpy==1.26.2` - Cálculos numéricos

### Visualización
- `plotly==5.18.0` - Gráficos interactivos
- `matplotlib==3.8.2` - Gráficos estáticos
- `seaborn==0.13.0` - Visualizaciones estadísticas

### Análisis
- `scipy==1.11.4` - Análisis estadístico

### Desarrollo
- `jupyter==1.0.0` - Notebooks interactivos
- `ipykernel==6.27.1` - Kernel de Python para Jupyter

### Utilidades
- `openpyxl==3.1.2` - Lectura de archivos Excel

## 📈 Características de los Datos

Los datos son de naturaleza **administrativa** con las siguientes características:
- 📝 Mayoría de campos **categóricos/varchar**
- 🔢 Pocas variables **numéricas**
- 📊 Enfoque en análisis de frecuencias y distribuciones
- 🎯 Análisis descriptivo y exploratorio

## 🛠️ Flujo de Trabajo Recomendado

1. **Exploración inicial**: Revisar datos originales en `data/9PM_bootcamp.xlsx`
2. **Preprocesado**: Ejecutar `01_preprocesado.ipynb` para limpiar datos
3. **Análisis exploratorio**: Ejecutar `02_EDA.ipynb` para obtener insights
4. **Visualización interactiva**: Usar el dashboard de Streamlit para exploración dinámica
5. **Documentación**: Registrar hallazgos y conclusiones

## 🎨 Personalización del Dashboard

Para personalizar el dashboard según tus necesidades:

1. Edita `app/dashboard.py`
2. Añade nuevas funciones de visualización
3. Modifica los filtros en el sidebar
4. Añade nuevas tabs o secciones
5. Personaliza los estilos CSS

## 📝 Notas Adicionales

- Los datos preprocesados se guardarán en `data/9PM_bootcamp_clean.csv` (si se exportan)
- Las visualizaciones generadas pueden exportarse desde el dashboard
- Los notebooks incluyen celdas comentadas para personalización

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Crea una rama nueva: `git checkout -b feature/nueva-funcionalidad`
2. Realiza tus cambios y commits
3. Push a la rama: `git push origin feature/nueva-funcionalidad`
4. Crea un Pull Request

## 📧 Contacto

**Autor**: Pablo Castejón
**Repositorio**: [Horizonte-Europa---Bootcamp](https://github.com/pablocastejon/Horizonte-Europa---Bootcamp)

---

**Fecha de creación**: Octubre 2025
**Última actualización**: Octubre 2025
