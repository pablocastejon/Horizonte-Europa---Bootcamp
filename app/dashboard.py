"""
Dashboard Interactivo - Proyectos Horizonte Europa
===================================================
Dashboard de Streamlit para exploración, visualización y búsqueda de proyectos
europeos del Programa Marco 9 (Horizonte Europa)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# ==================== CONFIGURACIÓN DE LA PÁGINA ====================
st.set_page_config(
    page_title="Dashboard Horizonte Europa",
    page_icon="🇪🇺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS PERSONALIZADOS ====================
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)


# ==================== FUNCIONES DE CARGA DE DATOS ====================
@st.cache_data
def load_data():
    """Carga los datos de proyectos europeos"""
    import os
    try:
        # Obtener la ruta base del proyecto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, 'data')
        
        # Intentar cargar datos preprocesados
        try:
            clean_csv = os.path.join(data_dir, '9PM_bootcamp_clean.csv')
            df = pd.read_csv(clean_csv)
        except:
            try:
                clean_xlsx = os.path.join(data_dir, '9PM_bootcamp_clean.xlsx')
                df = pd.read_excel(clean_xlsx)
            except:
                original_xlsx = os.path.join(data_dir, '9PM_bootcamp.xlsx')
                df = pd.read_excel(original_xlsx)
        
        # Asegurar conversión de fechas
        for col in ['Comienzo', 'Final']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Convertir Ref.UE y Centro a string
        for col in ['Ref.UE', 'Centro']:
            if col in df.columns:
                df[col] = df[col].astype(str)
        
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        return None


# ==================== FUNCIONES DE FILTRADO ====================
def apply_filters(df, filters):
    """Aplica filtros al dataframe"""
    df_filtered = df.copy()
    
    for key, value in filters.items():
        if value and key in df_filtered.columns:
            if isinstance(value, list) and len(value) > 0:
                df_filtered = df_filtered[df_filtered[key].isin(value)]
            elif not isinstance(value, list) and value != "Todos":
                df_filtered = df_filtered[df_filtered[key] == value]
    
    return df_filtered


# ==================== SIDEBAR CON FILTROS ====================
def render_sidebar(df):
    """Renderiza el sidebar con filtros interactivos"""
    st.sidebar.header("🎯 Filtros de Búsqueda")
    
    filters = {}
    
    # Filtro por situación
    if 'situación' in df.columns:
        situaciones = ['Todos'] + sorted(df['situación'].dropna().unique().tolist())
        filters['situación'] = st.sidebar.selectbox(
            "📊 Situación del Proyecto",
            situaciones,
            index=0
        )
        if filters['situación'] == 'Todos':
            filters['situación'] = None
    
    # Filtro por programa
    if 'programa' in df.columns:
        programas = sorted(df['programa'].dropna().unique().tolist())
        filters['programa'] = st.sidebar.multiselect(
            "🎯 Programa",
            programas
        )
    
    # Filtro por acción clave
    if 'Acción Clave' in df.columns:
        acciones = sorted(df['Acción Clave'].dropna().unique().tolist())
        filters['Acción Clave'] = st.sidebar.multiselect(
            "🔑 Acción Clave",
            acciones
        )
    
    # Filtro por coordinador CSIC
    if 'Coordinador CSIC' in df.columns:
        coordinador = ['Todos'] + sorted(df['Coordinador CSIC'].dropna().unique().tolist())
        filters['Coordinador CSIC'] = st.sidebar.selectbox(
            "🏛️ Coordinador CSIC",
            coordinador,
            index=0
        )
        if filters['Coordinador CSIC'] == 'Todos':
            filters['Coordinador CSIC'] = None
    
    # Filtro por centro
    if 'nombre centro IP normalizado' in df.columns:
        centros = sorted(df['nombre centro IP normalizado'].dropna().unique().tolist())
        filters['nombre centro IP normalizado'] = st.sidebar.multiselect(
            "🏢 Centro",
            centros
        )
    elif 'nombre centro IP' in df.columns:
        centros = sorted(df['nombre centro IP'].dropna().unique().tolist())
        filters['nombre centro IP'] = st.sidebar.multiselect(
            "🏢 Centro",
            centros
        )
    
    # Filtro por rango de fechas
    if 'Comienzo' in df.columns:
        st.sidebar.markdown("---")
        st.sidebar.markdown("📅 **Rango de Fechas**")
        
        min_date = df['Comienzo'].min()
        max_date = df['Comienzo'].max()
        
        if pd.notna(min_date) and pd.notna(max_date):
            date_range = st.sidebar.date_input(
                "Fecha de inicio",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            if len(date_range) == 2:
                filters['fecha_inicio'] = date_range[0]
                filters['fecha_fin'] = date_range[1]
    
    # Filtro por presupuesto
    if 'Concedido' in df.columns:
        st.sidebar.markdown("---")
        st.sidebar.markdown("💰 **Rango de Presupuesto**")
        
        min_budget = float(df['Concedido'].min())
        max_budget = float(df['Concedido'].max())
        
        budget_range = st.sidebar.slider(
            "Presupuesto (€)",
            min_value=min_budget,
            max_value=max_budget,
            value=(min_budget, max_budget),
            format="€%.0f"
        )
        filters['presupuesto_min'] = budget_range[0]
        filters['presupuesto_max'] = budget_range[1]
    
    # Información de registros
    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 **Total proyectos**: {len(df):,}")
    
    return filters


# ==================== TAB 1: RESUMEN GENERAL ====================
def show_overview(df):
    """Muestra resumen general con KPIs"""
    st.header("📋 Resumen General de Proyectos")
    
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Proyectos", f"{len(df):,}")
    
    with col2:
        if 'Concedido' in df.columns:
            total_budget = df['Concedido'].sum()
            st.metric("💰 Presupuesto Total", f"{total_budget:,.0f} €")
    
    with col3:
        if 'Duración(meses)' in df.columns:
            avg_duration = df['Duración(meses)'].mean()
            st.metric("⏱️ Duración Media", f"{avg_duration:.1f} meses")
    
    with col4:
        if 'CSIC' in df.columns:
            total_csic = df['CSIC'].sum()
            st.metric("🏛️ Participación CSIC", f"{int(total_csic)} centros")
    
    st.divider()
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución por situación
        if 'situación' in df.columns:
            fig = px.pie(
                df['situación'].value_counts().reset_index(),
                values='count',
                names='situación',
                title="📊 Distribución por Situación"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top 5 programas
        if 'programa' in df.columns:
            top_programas = df['programa'].value_counts().head(5).reset_index()
            fig = px.bar(
                top_programas,
                x='count',
                y='programa',
                orientation='h',
                title="🎯 Top 5 Programas",
                labels={'count': 'Número de Proyectos', 'programa': 'Programa'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Evolución temporal
    if 'Comienzo' in df.columns:
        st.subheader("📈 Evolución Temporal de Proyectos")
        
        df_temp = df.copy()
        df_temp['Año'] = df_temp['Comienzo'].dt.year
        evolucion = df_temp.groupby('Año').size().reset_index(name='Número de Proyectos')
        
        fig = px.line(
            evolucion,
            x='Año',
            y='Número de Proyectos',
            markers=True,
            title="Proyectos por Año de Inicio"
        )
        fig.update_xaxes(dtick=1)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de datos
    st.subheader("👀 Vista Previa de Datos")
    
    # Seleccionar columnas más relevantes para mostrar
    display_cols = []
    for col in ['Ref.CSIC', 'Título', 'programa', 'situación', 'Concedido', 'Comienzo', 'Duración(meses)']:
        if col in df.columns:
            display_cols.append(col)
    
    if display_cols:
        st.dataframe(df[display_cols].head(20), use_container_width=True, hide_index=True)
    else:
        st.dataframe(df.head(20), use_container_width=True, hide_index=True)


# ==================== TAB 2: ANÁLISIS POR PROGRAMA ====================
def show_program_analysis(df):
    """Análisis detallado por programa"""
    st.header("🎯 Análisis por Programa y Acción Clave")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución de proyectos por programa
        if 'programa' in df.columns:
            programa_counts = df['programa'].value_counts().reset_index()
            programa_counts.columns = ['programa', 'Número de Proyectos']
            
            fig = px.bar(
                programa_counts,
                x='Número de Proyectos',
                y='programa',
                orientation='h',
                title="Proyectos por Programa",
                color='Número de Proyectos',
                color_continuous_scale='viridis'
            )
            fig.update_layout(showlegend=False, height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Presupuesto por programa
        if 'programa' in df.columns and 'Concedido' in df.columns:
            programa_budget = df.groupby('programa')['Concedido'].sum().sort_values(ascending=True).reset_index()
            
            fig = px.bar(
                programa_budget,
                x='Concedido',
                y='programa',
                orientation='h',
                title="Presupuesto Total por Programa (€)",
                color='Concedido',
                color_continuous_scale='reds'
            )
            fig.update_layout(showlegend=False, height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    # Análisis por Acción Clave
    if 'Acción Clave' in df.columns:
        st.subheader("🔑 Distribución por Acción Clave")
        
        accion_counts = df['Acción Clave'].value_counts().head(10).reset_index()
        accion_counts.columns = ['Acción Clave', 'Número de Proyectos']
        
        fig = px.pie(
            accion_counts,
            values='Número de Proyectos',
            names='Acción Clave',
            title="Top 10 Acciones Clave"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla resumen por programa
    if 'programa' in df.columns:
        st.subheader("📊 Resumen Estadístico por Programa")
        
        summary_data = {'Proyectos': df.groupby('programa').size()}
        
        if 'Concedido' in df.columns:
            summary_data['Presupuesto Total'] = df.groupby('programa')['Concedido'].sum()
            summary_data['Presupuesto Medio'] = df.groupby('programa')['Concedido'].mean()
        
        if 'Duración(meses)' in df.columns:
            summary_data['Duración Media (meses)'] = df.groupby('programa')['Duración(meses)'].mean()
        
        summary = pd.DataFrame(summary_data).round(2)
        st.dataframe(summary, use_container_width=True)


# ==================== TAB 3: ANÁLISIS PRESUPUESTARIO ====================
def show_budget_analysis(df):
    """Análisis del presupuesto concedido"""
    st.header("💰 Análisis Presupuestario")
    
    if 'Concedido' not in df.columns:
        st.warning("⚠️ No se encontró la columna 'Concedido'")
        return
    
    # KPIs presupuestarios
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = df['Concedido'].sum()
        st.metric("💰 Total", f"{total:,.0f} €")
    
    with col2:
        media = df['Concedido'].mean()
        st.metric("📊 Media", f"{media:,.0f} €")
    
    with col3:
        mediana = df['Concedido'].median()
        st.metric("📈 Mediana", f"{mediana:,.0f} €")
    
    with col4:
        maximo = df['Concedido'].max()
        st.metric("🔝 Máximo", f"{maximo:,.0f} €")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución del presupuesto
        fig = px.histogram(
            df,
            x='Concedido',
            nbins=50,
            title="Distribución del Presupuesto Concedido",
            labels={'Concedido': 'Presupuesto (€)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Boxplot
        fig = px.box(
            df,
            y='Concedido',
            title="Análisis de Distribución (Boxplot)",
            labels={'Concedido': 'Presupuesto (€)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Presupuesto por año
    if 'Comienzo' in df.columns:
        st.subheader("📅 Presupuesto por Año de Inicio")
        
        df_temp = df.copy()
        df_temp['Año'] = df_temp['Comienzo'].dt.year
        budget_year = df_temp.groupby('Año')['Concedido'].sum().reset_index()
        
        fig = px.bar(
            budget_year,
            x='Año',
            y='Concedido',
            title="Presupuesto Total por Año",
            labels={'Concedido': 'Presupuesto (€)', 'Año': 'Año'}
        )
        fig.update_xaxes(dtick=1)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top proyectos por presupuesto
    st.subheader("🏆 Top 10 Proyectos por Presupuesto")
    
    cols_to_show = ['Ref.CSIC', 'Título', 'programa', 'Concedido']
    if 'Duración(meses)' in df.columns:
        cols_to_show.append('Duración(meses)')
    
    available_cols = [col for col in cols_to_show if col in df.columns]
    
    if available_cols:
        top_projects = df.nlargest(10, 'Concedido')[available_cols]
        st.dataframe(top_projects, use_container_width=True, hide_index=True)


# ==================== TAB 4: ANÁLISIS POR CENTROS ====================
def show_center_analysis(df):
    """Análisis por centros de investigación"""
    st.header("🏛️ Análisis por Centros")
    
    # Seleccionar columna de centro a usar
    centro_col = 'nombre centro IP normalizado' if 'nombre centro IP normalizado' in df.columns else 'nombre centro IP'
    
    if centro_col not in df.columns:
        st.warning("⚠️ No se encontró información de centros")
        return
    
    # Top centros por número de proyectos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Top 15 Centros por Número de Proyectos")
        
        top_centers = df[centro_col].value_counts().head(15).reset_index()
        top_centers.columns = ['Centro', 'Proyectos']
        
        fig = px.bar(
            top_centers,
            x='Proyectos',
            y='Centro',
            orientation='h',
            color='Proyectos',
            color_continuous_scale='blues'
        )
        fig.update_layout(showlegend=False, height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top centros por presupuesto
        if 'Concedido' in df.columns:
            st.subheader("💰 Top 15 Centros por Presupuesto")
            
            centro_budget = df.groupby(centro_col)['Concedido'].sum().sort_values(ascending=False).head(15).reset_index()
            centro_budget.columns = ['Centro', 'Presupuesto']
            
            fig = px.bar(
                centro_budget,
                x='Presupuesto',
                y='Centro',
                orientation='h',
                color='Presupuesto',
                color_continuous_scale='greens'
            )
            fig.update_layout(showlegend=False, height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    # Tabla resumen por centro
    st.subheader("📋 Resumen Estadístico por Centro")
    
    summary_data = {
        'Proyectos': df.groupby(centro_col).size(),
    }
    
    if 'Concedido' in df.columns:
        summary_data['Presupuesto Total'] = df.groupby(centro_col)['Concedido'].sum()
        summary_data['Presupuesto Medio'] = df.groupby(centro_col)['Concedido'].mean()
    
    if 'Coordinador CSIC' in df.columns:
        summary_data['Como Coordinador'] = df[df['Coordinador CSIC'] == 'Sí'].groupby(centro_col).size()
    
    summary = pd.DataFrame(summary_data).fillna(0)
    summary = summary.sort_values('Proyectos', ascending=False).head(20)
    
    st.dataframe(summary.round(2), use_container_width=True)


# ==================== TAB 5: BÚSQUEDA AVANZADA ====================
def show_search(df):
    """Motor de búsqueda avanzada"""
    st.header("🔍 Búsqueda Avanzada de Proyectos")
    
    st.markdown("""
    Busca proyectos específicos utilizando diferentes criterios.
    Los campos vacíos serán ignorados en la búsqueda.
    """)
    
    # Formulario de búsqueda
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Búsqueda por Ref.CSIC
            ref_csic = st.text_input("📌 Ref.CSIC", placeholder="Ej: 202212345")
            
            # Búsqueda por título
            titulo = st.text_input("📝 Título del Proyecto", placeholder="Palabras clave en el título")
            
            # Búsqueda por investigador
            if 'Nombre IP' in df.columns:
                investigador = st.text_input("👨‍🔬 Investigador Principal", placeholder="Nombre del IP")
            else:
                investigador = None
            
            # Búsqueda por acrónimo
            if 'Acrónimo del proyecto' in df.columns:
                acronimo = st.text_input("🔤 Acrónimo", placeholder="Ej: HORIZON")
            else:
                acronimo = None
        
        with col2:
            # Búsqueda por programa
            if 'programa' in df.columns:
                programas_busqueda = ['Todos'] + sorted(df['programa'].dropna().unique().tolist())
                programa_busqueda = st.selectbox("🎯 Programa", programas_busqueda)
            else:
                programa_busqueda = None
            
            # Búsqueda por centro
            centro_col = 'nombre centro IP normalizado' if 'nombre centro IP normalizado' in df.columns else 'nombre centro IP'
            if centro_col in df.columns:
                centros_busqueda = ['Todos'] + sorted(df[centro_col].dropna().unique().tolist())
                centro_busqueda = st.selectbox("🏢 Centro", centros_busqueda)
            else:
                centro_busqueda = None
            
            # Búsqueda por keywords
            if 'Keywords' in df.columns:
                keywords = st.text_input("🏷️ Palabras Clave", placeholder="Keywords del proyecto")
            else:
                keywords = None
            
            # Búsqueda por resumen
            if 'Resumen' in df.columns:
                resumen = st.text_input("📄 Resumen", placeholder="Palabras en el resumen")
            else:
                resumen = None
        
        submitted = st.form_submit_button("🔍 Buscar", type="primary", use_container_width=True)
    
    # Aplicar búsqueda
    if submitted:
        df_result = df.copy()
        
        # Aplicar filtros de búsqueda
        if ref_csic and 'Ref.CSIC' in df_result.columns:
            df_result = df_result[df_result['Ref.CSIC'].astype(str).str.contains(ref_csic, case=False, na=False)]
        
        if titulo and 'Título' in df_result.columns:
            df_result = df_result[df_result['Título'].str.contains(titulo, case=False, na=False)]
        
        if investigador and 'Nombre IP' in df_result.columns:
            df_result = df_result[df_result['Nombre IP'].str.contains(investigador, case=False, na=False)]
        
        if acronimo and 'Acrónimo del proyecto' in df_result.columns:
            df_result = df_result[df_result['Acrónimo del proyecto'].str.contains(acronimo, case=False, na=False)]
        
        if programa_busqueda and programa_busqueda != 'Todos' and 'programa' in df_result.columns:
            df_result = df_result[df_result['programa'] == programa_busqueda]
        
        if centro_busqueda and centro_busqueda != 'Todos' and centro_col in df_result.columns:
            df_result = df_result[df_result[centro_col] == centro_busqueda]
        
        if keywords and 'Keywords' in df_result.columns:
            df_result = df_result[df_result['Keywords'].str.contains(keywords, case=False, na=False)]
        
        if resumen and 'Resumen' in df_result.columns:
            df_result = df_result[df_result['Resumen'].str.contains(resumen, case=False, na=False)]
        
        # Mostrar resultados
        st.success(f"✅ Se encontraron {len(df_result)} proyectos")
        
        if len(df_result) > 0:
            # Seleccionar columnas relevantes para mostrar
            display_cols = []
            for col in ['Ref.CSIC', 'Título', 'programa', 'nombre centro IP', 'Nombre IP', 'Concedido', 'Comienzo']:
                if col in df_result.columns:
                    display_cols.append(col)
            
            if not display_cols:
                display_cols = df_result.columns.tolist()[:10]
            
            st.dataframe(df_result[display_cols], use_container_width=True, hide_index=True)
            
            # Opción de descarga
            csv = df_result.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar resultados (CSV)",
                data=csv,
                file_name=f"busqueda_proyectos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No se encontraron proyectos con los criterios especificados")


# ==================== APLICACIÓN PRINCIPAL ====================
def main():
    """Función principal de la aplicación"""
    
    # Título y descripción
    st.title("🇪🇺 Dashboard - Proyectos Horizonte Europa")
    st.markdown("**Programa Marco 9 (PM9)** - Gestión y Análisis de Proyectos de Investigación")
    st.markdown("---")
    
    # Cargar datos
    with st.spinner("Cargando datos..."):
        df = load_data()
    
    if df is None:
        st.stop()
    
    # Sidebar con filtros
    filters = render_sidebar(df)
    
    # Aplicar filtros (excluyendo filtros especiales)
    filters_to_apply = {k: v for k, v in filters.items() 
                        if k not in ['fecha_inicio', 'fecha_fin', 'presupuesto_min', 'presupuesto_max']}
    
    df_filtered = apply_filters(df, filters_to_apply)
    
    # Aplicar filtros de fecha
    if 'fecha_inicio' in filters and 'fecha_fin' in filters and 'Comienzo' in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered['Comienzo'].dt.date >= filters['fecha_inicio']) &
            (df_filtered['Comienzo'].dt.date <= filters['fecha_fin'])
        ]
    
    # Aplicar filtros de presupuesto
    if 'presupuesto_min' in filters and 'presupuesto_max' in filters and 'Concedido' in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered['Concedido'] >= filters['presupuesto_min']) &
            (df_filtered['Concedido'] <= filters['presupuesto_max'])
        ]
    
    # Mostrar número de proyectos filtrados
    if len(df_filtered) < len(df):
        st.info(f"🔍 Mostrando {len(df_filtered):,} de {len(df):,} proyectos")
    
    # Tabs principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Resumen General",
        "🎯 Por Programa",
        "💰 Análisis Presupuestario",
        "🏛️ Por Centros",
        "🔍 Búsqueda Avanzada"
    ])
    
    with tab1:
        show_overview(df_filtered)
    
    with tab2:
        show_program_analysis(df_filtered)
    
    with tab3:
        show_budget_analysis(df_filtered)
    
    with tab4:
        show_center_analysis(df_filtered)
    
    with tab5:
        show_search(df)  # Búsqueda siempre sobre dataset completo
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.9em;'>
            Dashboard de Proyectos Horizonte Europa | Programa Marco 9 (PM9)<br>
            Datos actualizados: {}
        </div>
        """.format(datetime.now().strftime("%d/%m/%Y")),
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
