# 🚀 Guía de Inicio Rápido

## ✅ Checklist de Configuración

- [x] Entorno virtual creado (`venv/`)
- [x] Dependencias instaladas
- [x] Estructura de carpetas organizada
- [x] Datos en carpeta `data/`
- [x] Notebooks creados
- [x] Dashboard de Streamlit configurado

## 📋 Pasos Siguientes

### 1️⃣ Explorar los Datos (AHORA)

```bash
# Activar el entorno virtual (si no está activo)
source venv/bin/activate

# Abrir el notebook de preprocesado
jupyter notebook notebooks/01_preprocesado.ipynb
```

**¿Qué hacer en este notebook?**
- Ejecutar todas las celdas
- Revisar la estructura de los datos
- Identificar valores nulos y duplicados
- Limpiar datos según necesidades específicas
- Crear nuevas columnas si es necesario

### 2️⃣ Análisis Exploratorio

```bash
# Abrir el notebook de EDA
jupyter notebook notebooks/02_EDA.ipynb
```

**¿Qué hacer en este notebook?**
- Analizar distribuciones de variables
- Crear visualizaciones
- Identificar patrones y tendencias
- Generar insights para el dashboard

### 3️⃣ Probar el Dashboard

```bash
# Desde la carpeta del proyecto
cd app
streamlit run dashboard.py
```

**El dashboard se abrirá en:** `http://localhost:8501`

### 4️⃣ Personalizar el Dashboard

Según los insights del EDA, personaliza:

1. **Filtros en el sidebar** (`app/dashboard.py`, línea ~50)
   - Añade filtros específicos para tus datos
   
2. **Nuevas visualizaciones**
   - Crea funciones adicionales en `app/utils.py`
   - Añade nuevas tabs en el dashboard

3. **Métricas importantes**
   - Identifica KPIs relevantes
   - Añádelos en la sección de resumen

## 🎯 Flujo de Trabajo Recomendado

```
1. Preprocesado → 2. EDA → 3. Dashboard → 4. Iteración
     ↑                                          |
     └──────────────────────────────────────────┘
```

## 💡 Comandos Útiles

### Ver ayuda completa de comandos
```bash
./comandos_utiles.sh
```

### Activar entorno virtual
```bash
source venv/bin/activate
```

### Desactivar entorno virtual
```bash
deactivate
```

### Ejecutar Jupyter
```bash
jupyter notebook
```

### Ejecutar Dashboard
```bash
cd app && streamlit run dashboard.py
```

### Ver estructura del proyecto
```bash
tree -L 2 -I 'venv|__pycache__|.git'
```

## 🔧 Personalización de Variables

### En el Notebook de Preprocesado

Ajusta las siguientes secciones según tus datos:

```python
# 4.2 Tratamiento de Valores Nulos
# Personalizar estrategia para cada columna

# 6. Creación de Nuevas Columnas
# Añadir columnas derivadas según necesidades
```

### En el Dashboard

Personaliza los filtros en `dashboard.py`:

```python
def render_sidebar(df):
    # Añadir filtros específicos aquí
    if 'tu_columna' in df.columns:
        valores = st.sidebar.multiselect(
            "Filtrar por...",
            options=df['tu_columna'].unique()
        )
```

## 📊 Estructura de Datos

**Recuerda**: Los datos son principalmente **categóricos/administrativos**

- ✅ Enfocarse en **frecuencias y distribuciones**
- ✅ Usar gráficos de barras, pasteles, tablas
- ✅ Análisis de categorías y cruces
- ⚠️ Pocas variables numéricas para correlaciones

## 🐛 Solución de Problemas

### Problema: "ModuleNotFoundError"
```bash
# Asegúrate de tener el entorno virtual activo
source venv/bin/activate
pip install -r requirements.txt
```

### Problema: "FileNotFoundError" al cargar datos
```bash
# Verifica que el archivo esté en la carpeta correcta
ls -la data/9PM_bootcamp.xlsx
```

### Problema: Streamlit no se abre
```bash
# Especifica el puerto manualmente
streamlit run dashboard.py --server.port 8502
```

## 📚 Recursos Adicionales

- **Documentación completa**: `docs/README.md`
- **Streamlit Docs**: https://docs.streamlit.io/
- **Plotly Docs**: https://plotly.com/python/
- **Pandas Docs**: https://pandas.pydata.org/docs/

## 🎓 Próximos Pasos

1. ✅ Completar preprocesado de datos
2. ✅ Realizar EDA exhaustivo
3. ✅ Personalizar dashboard
4. 📝 Documentar insights encontrados
5. 🚀 Compartir dashboard con stakeholders

---

**¡Éxito con tu análisis! 🚀**
