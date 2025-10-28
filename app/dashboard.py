"""
Dashboard Interactivo - Proyectos Horizonte Europa
===================================================
Dashboard de Streamlit para exploración, visualización y búsqueda de proyectos
europeos del Programa Marco 9 (Horizonte Europa)

Actualizado para trabajar con 9PM_bootcamp_clean.xlsx
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
        
        # Cargar datos preprocesados con dtypes específicos
        clean_xlsx = os.path.join(data_dir, '9PM_bootcamp_clean.xlsx')
        
        # Especificar tipos de datos para evitar que años se lean como numéricos
        df = pd.read_excel(
            clean_xlsx,
            dtype={
                'Año Inicio': str,
                'Año Fin': str,
                'Centro': str,
                'Ref.UE': str,
                'Cód.área': str
            }
        )
        
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        st.error(f"Ruta intentada: {clean_xlsx if 'clean_xlsx' in locals() else 'No definida'}")
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
    
    # Filtro por Situación
    if 'Situación' in df.columns:
        situaciones = ['Todos'] + sorted(df['Situación'].dropna().unique().tolist())
        filters['Situación'] = st.sidebar.selectbox(
            "📊 Situación del Proyecto",
            situaciones,
            index=0
        )
        if filters['Situación'] == 'Todos':
            filters['Situación'] = None
    
    # Filtro por Programa
    if 'Programa' in df.columns:
        programas = sorted(df['Programa'].dropna().unique().tolist())
        filters['Programa'] = st.sidebar.multiselect(
            "🎯 Programa",
            programas
        )
    
    # Filtro por Acción Clave
    if 'Acción clave' in df.columns:
        acciones = sorted(df['Acción clave'].dropna().unique().tolist())
        filters['Acción clave'] = st.sidebar.multiselect(
            "🔑 Acción Clave",
            acciones
        )
    
    # Filtro por Área Científica
    if 'Area' in df.columns:
        areas = sorted(df['Area'].dropna().unique().tolist())
        filters['Area'] = st.sidebar.multiselect(
            "🔬 Área Científica",
            areas
        )
    
    # Filtro por centro
    if 'Nombre Centro IP Normalizado' in df.columns:
        centros = sorted(df['Nombre Centro IP Normalizado'].dropna().unique().tolist())
        filters['Nombre Centro IP Normalizado'] = st.sidebar.multiselect(
            "🏢 Centro",
            centros
        )
    
    # Filtro por rango de años
    if 'Año Inicio' in df.columns:
        st.sidebar.markdown("---")
        st.sidebar.markdown("📅 **Rango de Años**")
        
        años_disponibles = sorted([año for año in df['Año Inicio'].dropna().unique() if año and año != 'nan'])
        
        if años_disponibles:
            año_min = años_disponibles[0]
            año_max = años_disponibles[-1]
            
            año_range = st.sidebar.select_slider(
                "Año de Inicio",
                options=años_disponibles,
                value=(año_min, año_max)
            )
            filters['año_inicio_min'] = año_range[0]
            filters['año_inicio_max'] = año_range[1]
    
    # Filtro por presupuesto
    if 'Importe Concedido' in df.columns:
        st.sidebar.markdown("---")
        st.sidebar.markdown("💰 **Rango de Presupuesto**")
        
        presupuestos_validos = df['Importe Concedido'].dropna()
        if len(presupuestos_validos) > 0:
            min_budget = float(presupuestos_validos.min())
            max_budget = float(presupuestos_validos.max())
            
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
        if 'Importe Concedido' in df.columns:
            total_budget = df['Importe Concedido'].sum()
            st.metric("💰 Presupuesto Total", f"{total_budget/1e6:.1f}M €")
    
    with col3:
        if 'Duración (meses)' in df.columns:
            avg_duration = df['Duración (meses)'].mean()
            st.metric("⏱️ Duración Media", f"{avg_duration:.1f} meses")
    
    with col4:
        if 'Participantes CSIC' in df.columns:
            total_csic = df['Participantes CSIC'].sum()
            st.metric("🏛️ Participación CSIC", f"{int(total_csic)}")
    
    st.divider()
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución por Situación
        if 'Situación' in df.columns:
            situacion_counts = df['Situación'].value_counts().reset_index()
            situacion_counts.columns = ['Situación', 'count']
            
            fig = px.pie(
                situacion_counts,
                values='count',
                names='Situación',
                title="📊 Distribución por Situación"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top 5 Programas
        if 'Programa' in df.columns:
            top_programas = df['Programa'].value_counts().head(5).reset_index()
            top_programas.columns = ['Programa', 'count']
            
            fig = px.bar(
                top_programas,
                x='count',
                y='Programa',
                orientation='h',
                title="🎯 Top 5 Programas",
                labels={'count': 'Número de Proyectos', 'Programa': 'Programa'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Evolución temporal
    if 'Año Inicio' in df.columns:
        st.subheader("📈 Evolución Temporal de Proyectos")
        
        evolucion = df['Año Inicio'].value_counts().sort_index().reset_index()
        evolucion.columns = ['Año', 'Número de Proyectos']
        
        fig = px.line(
            evolucion,
            x='Año',
            y='Número de Proyectos',
            markers=True,
            title="Proyectos por Año de Inicio"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Distribución por Área Científica
    if 'Area' in df.columns:
        st.subheader("🔬 Distribución por Área Científica")
        
        area_counts = df['Area'].value_counts().reset_index()
        area_counts.columns = ['Área', 'count']
        
        fig = px.bar(
            area_counts,
            x='count',
            y='Área',
            orientation='h',
            title="Proyectos por Área Científica",
            labels={'count': 'Número de Proyectos'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de datos
    st.subheader("👀 Vista Previa de Datos")
    
    # Seleccionar columnas más relevantes para mostrar
    display_cols = []
    for col in ['Ref.UE', 'Título', 'Programa', 'Situación', 'Importe Concedido', 'Año Inicio', 'Duración (meses)']:
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
        if 'Programa' in df.columns:
            programa_counts = df['Programa'].value_counts().reset_index()
            programa_counts.columns = ['Programa', 'Número de Proyectos']
            
            fig = px.bar(
                programa_counts,
                x='Número de Proyectos',
                y='Programa',
                orientation='h',
                title="Proyectos por Programa",
                color='Número de Proyectos',
                color_continuous_scale='viridis'
            )
            fig.update_layout(showlegend=False, height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Presupuesto por programa
        if 'Programa' in df.columns and 'Importe Concedido' in df.columns:
            programa_budget = df.groupby('Programa')['Importe Concedido'].sum().sort_values(ascending=True).reset_index()
            programa_budget['Importe Concedido (M€)'] = programa_budget['Importe Concedido'] / 1e6
            
            fig = px.bar(
                programa_budget,
                x='Importe Concedido (M€)',
                y='Programa',
                orientation='h',
                title="Presupuesto Total por Programa (M€)",
                color='Importe Concedido (M€)',
                color_continuous_scale='reds'
            )
            fig.update_layout(showlegend=False, height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    # Análisis por Acción Clave
    if 'Acción clave' in df.columns:
        st.subheader("🔑 Distribución por Acción Clave")
        
        accion_counts = df['Acción clave'].value_counts().head(10).reset_index()
        accion_counts.columns = ['Acción Clave', 'Número de Proyectos']
        
        fig = px.pie(
            accion_counts,
            values='Número de Proyectos',
            names='Acción Clave',
            title="Top 10 Acciones Clave"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Evolución temporal por programa
    if 'Programa' in df.columns and 'Año Inicio' in df.columns:
        st.subheader("📈 Evolución Temporal por Programa")
        
        evol_programa = df.groupby(['Año Inicio', 'Programa']).size().reset_index(name='Proyectos')
        
        fig = px.line(
            evol_programa,
            x='Año Inicio',
            y='Proyectos',
            color='Programa',
            title="Evolución de Proyectos por Programa y Año",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla resumen por programa
    if 'Programa' in df.columns:
        st.subheader("📊 Resumen Estadístico por Programa")
        
        summary_data = {'Proyectos': df.groupby('Programa').size()}
        
        if 'Importe Concedido' in df.columns:
            summary_data['Presupuesto Total (M€)'] = df.groupby('Programa')['Importe Concedido'].sum() / 1e6
            summary_data['Presupuesto Medio (€)'] = df.groupby('Programa')['Importe Concedido'].mean()
        
        if 'Duración (meses)' in df.columns:
            summary_data['Duración Media (meses)'] = df.groupby('Programa')['Duración (meses)'].mean()
        
        summary = pd.DataFrame(summary_data).round(2)
        summary = summary.sort_values('Proyectos', ascending=False)
        st.dataframe(summary, use_container_width=True)


# ==================== TAB 3: ANÁLISIS PRESUPUESTARIO ====================
def show_budget_analysis(df):
    """Análisis del presupuesto concedido"""
    st.header("💰 Análisis Presupuestario")
    
    if 'Importe Concedido' not in df.columns:
        st.warning("⚠️ No se encontró la columna 'Importe Concedido'")
        return
    
    # Filtrar datos válidos
    df_budget = df[df['Importe Concedido'].notna() & (df['Importe Concedido'] > 0)].copy()
    
    # KPIs presupuestarios
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = df_budget['Importe Concedido'].sum()
        st.metric("💰 Total", f"{total/1e6:.1f}M €")
    
    with col2:
        media = df_budget['Importe Concedido'].mean()
        st.metric("📊 Media", f"{media:,.0f} €")
    
    with col3:
        mediana = df_budget['Importe Concedido'].median()
        st.metric("📈 Mediana", f"{mediana:,.0f} €")
    
    with col4:
        maximo = df_budget['Importe Concedido'].max()
        st.metric("🔝 Máximo", f"{maximo/1e6:.2f}M €")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución del presupuesto
        fig = px.histogram(
            df_budget,
            x='Importe Concedido',
            nbins=50,
            title="Distribución del Presupuesto Concedido",
            labels={'Importe Concedido': 'Presupuesto (€)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Boxplot
        fig = px.box(
            df_budget,
            y='Importe Concedido',
            title="Análisis de Distribución (Boxplot)",
            labels={'Importe Concedido': 'Presupuesto (€)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Presupuesto por año
    if 'Año Inicio' in df_budget.columns:
        st.subheader("📅 Presupuesto por Año de Inicio")
        
        budget_year = df_budget.groupby('Año Inicio')['Importe Concedido'].sum().reset_index()
        budget_year['Importe Concedido (M€)'] = budget_year['Importe Concedido'] / 1e6
        
        fig = px.bar(
            budget_year,
            x='Año Inicio',
            y='Importe Concedido (M€)',
            title="Presupuesto Total por Año (M€)",
            labels={'Importe Concedido (M€)': 'Presupuesto (M€)', 'Año Inicio': 'Año'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Presupuesto por Área Científica
    if 'Area' in df_budget.columns:
        st.subheader("🔬 Presupuesto por Área Científica")
        
        budget_area = df_budget.groupby('Area')['Importe Concedido'].sum().sort_values(ascending=False).reset_index()
        budget_area['Importe Concedido (M€)'] = budget_area['Importe Concedido'] / 1e6
        
        fig = px.bar(
            budget_area,
            x='Importe Concedido (M€)',
            y='Area',
            orientation='h',
            title="Presupuesto Total por Área Científica (M€)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top proyectos por presupuesto
    st.subheader("🏆 Top 10 Proyectos por Presupuesto")
    
    cols_to_show = ['Ref.UE', 'Título', 'Programa', 'Importe Concedido']
    if 'Duración (meses)' in df_budget.columns:
        cols_to_show.append('Duración (meses)')
    if 'Nombre Centro IP Normalizado' in df_budget.columns:
        cols_to_show.append('Nombre Centro IP Normalizado')
    
    available_cols = [col for col in cols_to_show if col in df_budget.columns]
    
    if available_cols:
        top_projects = df_budget.nlargest(10, 'Importe Concedido')[available_cols]
        st.dataframe(top_projects, use_container_width=True, hide_index=True)


# ==================== TAB 4: ANÁLISIS POR CENTROS ====================
def show_center_analysis(df):
    """Análisis por centros de investigación"""
    st.header("🏛️ Análisis por Centros")
    
    # Seleccionar columna de centro a usar
    centro_col = 'Nombre Centro IP Normalizado' if 'Nombre Centro IP Normalizado' in df.columns else None
    
    if not centro_col or centro_col not in df.columns:
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
        if 'Importe Concedido' in df.columns:
            st.subheader("💰 Top 15 Centros por Presupuesto")
            
            centro_budget = df.groupby(centro_col)['Importe Concedido'].sum().sort_values(ascending=False).head(15).reset_index()
            centro_budget.columns = ['Centro', 'Presupuesto']
            centro_budget['Presupuesto (M€)'] = centro_budget['Presupuesto'] / 1e6
            
            fig = px.bar(
                centro_budget,
                x='Presupuesto (M€)',
                y='Centro',
                orientation='h',
                color='Presupuesto (M€)',
                color_continuous_scale='greens'
            )
            fig.update_layout(showlegend=False, height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    # Distribución temporal por centro (top 5)
    if 'Año Inicio' in df.columns:
        st.subheader("📈 Evolución Temporal - Top 5 Centros")
        
        top5_centers = df[centro_col].value_counts().head(5).index.tolist()
        df_top5 = df[df[centro_col].isin(top5_centers)]
        
        evol_centro = df_top5.groupby(['Año Inicio', centro_col]).size().reset_index(name='Proyectos')
        
        fig = px.line(
            evol_centro,
            x='Año Inicio',
            y='Proyectos',
            color=centro_col,
            title="Evolución de Proyectos - Top 5 Centros",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla resumen por centro
    st.subheader("📋 Resumen Estadístico por Centro (Top 20)")
    
    summary_data = {
        'Proyectos': df.groupby(centro_col).size(),
    }
    
    if 'Importe Concedido' in df.columns:
        summary_data['Presupuesto Total (M€)'] = df.groupby(centro_col)['Importe Concedido'].sum() / 1e6
        summary_data['Presupuesto Medio (€)'] = df.groupby(centro_col)['Importe Concedido'].mean()
    
    if 'Participantes CSIC' in df.columns:
        summary_data['Participantes CSIC'] = df.groupby(centro_col)['Participantes CSIC'].sum()
    
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
    
    # BÚSQUEDA INTELIGENTE (destacada al principio)
    st.subheader("🤖 Búsqueda Inteligente")
    st.markdown("**Busca en múltiples campos simultáneamente**: Título, Acrónimo, Resumen, Keywords y más")
    
    with st.form("smart_search_form"):
        busqueda_inteligente = st.text_input(
            "Introduce términos de búsqueda",
            placeholder="Ej: inteligencia artificial, sostenibilidad, energía renovable...",
            help="Busca en: Título, Acrónimo del proyecto, Resumen, Keywords, Nombre Centro IP Normalizado"
        )
        
        busqueda_inteligente_submitted = st.form_submit_button(
            "🚀 Buscar en Todos los Campos", 
            type="primary", 
            use_container_width=True
        )
    
    # Procesar búsqueda inteligente
    if busqueda_inteligente_submitted and busqueda_inteligente:
        df_result = df.copy()
        
        # Campos donde buscar
        search_fields = ['Título', 'Acrónimo del proyecto', 'Resumen', 'Keywords', 'Nombre Centro IP Normalizado']
        
        # Crear máscara de búsqueda (OR entre todos los campos)
        mask = pd.Series([False] * len(df_result), index=df_result.index)
        
        for field in search_fields:
            if field in df_result.columns:
                mask |= df_result[field].fillna('').astype(str).str.contains(
                    busqueda_inteligente, 
                    case=False, 
                    na=False
                )
        
        df_result = df_result[mask]
        
        # Mostrar resultados
        st.success(f"✅ Se encontraron {len(df_result)} proyectos con '{busqueda_inteligente}'")
        
        if len(df_result) > 0:
            # Mostrar en qué campos se encontró (información adicional)
            with st.expander("📊 Ver estadísticas de búsqueda"):
                matches_info = {}
                for field in search_fields:
                    if field in df_result.columns:
                        matches = df_result[field].fillna('').astype(str).str.contains(
                            busqueda_inteligente, 
                            case=False, 
                            na=False
                        ).sum()
                        if matches > 0:
                            matches_info[field] = matches
                
                if matches_info:
                    st.write("**Coincidencias por campo:**")
                    for field, count in matches_info.items():
                        st.write(f"- {field}: {count} proyectos")
            
            # Seleccionar columnas relevantes para mostrar
            display_cols = []
            for col in ['Ref.UE', 'Título', 'Acrónimo', 'Programa', 'Nombre Centro IP Normalizado', 
                       'Nombre IP', 'Importe Concedido', 'Año Inicio', 'Area']:
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
                file_name=f"busqueda_inteligente_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ No se encontraron proyectos con los términos especificados")
        
        st.markdown("---")
    
    # BÚSQUEDA AVANZADA (detallada, debajo)
    st.subheader("🔎 Búsqueda Detallada por Campos")
    st.markdown("Busca en campos específicos de forma individual")
    
    # Formulario de búsqueda
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Búsqueda por Ref.UE
            ref_ue = st.text_input("📌 Ref.UE", placeholder="Ej: 101012345")
            
            # Búsqueda por título
            titulo = st.text_input("📝 Título del Proyecto", placeholder="Palabras clave en el título")
            
            # Búsqueda por investigador
            if 'Nombre IP' in df.columns:
                investigador = st.text_input("👨‍🔬 Investigador Principal", placeholder="Nombre del IP")
            else:
                investigador = None
            
            # Búsqueda por acrónimo
            if 'Acrónimo' in df.columns:
                acronimo = st.text_input("🔤 Acrónimo", placeholder="Ej: HORIZON")
            else:
                acronimo = None
        
        with col2:
            # Búsqueda por programa
            if 'Programa' in df.columns:
                programas_busqueda = ['Todos'] + sorted(df['Programa'].dropna().unique().tolist())
                programa_busqueda = st.selectbox("🎯 Programa", programas_busqueda)
            else:
                programa_busqueda = None
            
            # Búsqueda por centro
            centro_col = 'Nombre Centro IP Normalizado'
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
            
            # Búsqueda por área científica
            if 'Area' in df.columns:
                areas_busqueda = ['Todos'] + sorted(df['Area'].dropna().unique().tolist())
                area_busqueda = st.selectbox("🔬 Área Científica", areas_busqueda)
            else:
                area_busqueda = None
        
        submitted = st.form_submit_button("🔍 Buscar", type="primary", use_container_width=True)
    
    # Aplicar búsqueda
    if submitted:
        df_result = df.copy()
        
        # Aplicar filtros de búsqueda
        if ref_ue and 'Ref.UE' in df_result.columns:
            df_result = df_result[df_result['Ref.UE'].astype(str).str.contains(ref_ue, case=False, na=False)]
        
        if titulo and 'Título' in df_result.columns:
            df_result = df_result[df_result['Título'].str.contains(titulo, case=False, na=False)]
        
        if investigador and 'Nombre IP' in df_result.columns:
            df_result = df_result[df_result['Nombre IP'].str.contains(investigador, case=False, na=False)]
        
        if acronimo and 'Acrónimo' in df_result.columns:
            df_result = df_result[df_result['Acrónimo'].str.contains(acronimo, case=False, na=False)]
        
        if programa_busqueda and programa_busqueda != 'Todos' and 'Programa' in df_result.columns:
            df_result = df_result[df_result['Programa'] == programa_busqueda]
        
        if centro_busqueda and centro_busqueda != 'Todos' and centro_col in df_result.columns:
            df_result = df_result[df_result[centro_col] == centro_busqueda]
        
        if keywords and 'Keywords' in df_result.columns:
            df_result = df_result[df_result['Keywords'].str.contains(keywords, case=False, na=False)]
        
        if area_busqueda and area_busqueda != 'Todos' and 'Area' in df_result.columns:
            df_result = df_result[df_result['Area'] == area_busqueda]
        
        # Mostrar resultados
        st.success(f"✅ Se encontraron {len(df_result)} proyectos")
        
        if len(df_result) > 0:
            # Seleccionar columnas relevantes para mostrar
            display_cols = []
            for col in ['Ref.UE', 'Título', 'Programa', 'Nombre Centro IP Normalizado', 'Nombre IP', 
                       'Importe Concedido', 'Año Inicio', 'Area']:
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
                        if k not in ['año_inicio_min', 'año_inicio_max', 'presupuesto_min', 'presupuesto_max']}
    
    df_filtered = apply_filters(df, filters_to_apply)
    
    # Aplicar filtros de año
    if 'año_inicio_min' in filters and 'año_inicio_max' in filters and 'Año Inicio' in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered['Año Inicio'] >= filters['año_inicio_min']) &
            (df_filtered['Año Inicio'] <= filters['año_inicio_max'])
        ]
    
    # Aplicar filtros de presupuesto
    if 'presupuesto_min' in filters and 'presupuesto_max' in filters and 'Importe Concedido' in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered['Importe Concedido'] >= filters['presupuesto_min']) &
            (df_filtered['Importe Concedido'] <= filters['presupuesto_max'])
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
