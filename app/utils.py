"""
Funciones Auxiliares para el Dashboard
========================================
Funciones de utilidad para procesamiento de datos y visualizaciones
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def format_number(num):
    """
    Formatea números con separadores de miles
    
    Args:
        num: Número a formatear
        
    Returns:
        str: Número formateado
    """
    if pd.isna(num):
        return "N/A"
    return f"{num:,.0f}".replace(",", ".")


def calculate_percentage(part, total):
    """
    Calcula porcentaje
    
    Args:
        part: Parte del total
        total: Total
        
    Returns:
        float: Porcentaje calculado
    """
    if total == 0:
        return 0
    return (part / total) * 100


def get_column_types(df):
    """
    Clasifica columnas por tipo de dato
    
    Args:
        df: DataFrame de pandas
        
    Returns:
        dict: Diccionario con columnas categóricas y numéricas
    """
    return {
        'categorical': df.select_dtypes(include=['object']).columns.tolist(),
        'numeric': df.select_dtypes(include=[np.number]).columns.tolist(),
        'datetime': df.select_dtypes(include=['datetime64']).columns.tolist()
    }


def detect_outliers(df, column):
    """
    Detecta outliers usando el método IQR
    
    Args:
        df: DataFrame de pandas
        column: Nombre de la columna
        
    Returns:
        tuple: (outliers_df, lower_bound, upper_bound)
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    
    return outliers, lower_bound, upper_bound


def create_frequency_table(df, column, top_n=None):
    """
    Crea tabla de frecuencias para una columna
    
    Args:
        df: DataFrame de pandas
        column: Nombre de la columna
        top_n: Número máximo de valores a mostrar
        
    Returns:
        DataFrame: Tabla de frecuencias
    """
    freq = df[column].value_counts().reset_index()
    freq.columns = [column, 'Frecuencia']
    freq['Porcentaje'] = (freq['Frecuencia'] / len(df) * 100).round(2)
    freq['Porcentaje_str'] = freq['Porcentaje'].apply(lambda x: f"{x}%")
    
    if top_n:
        return freq.head(top_n)
    return freq


def create_cross_table(df, col1, col2):
    """
    Crea tabla cruzada entre dos columnas categóricas
    
    Args:
        df: DataFrame de pandas
        col1: Primera columna
        col2: Segunda columna
        
    Returns:
        DataFrame: Tabla cruzada
    """
    return pd.crosstab(df[col1], df[col2], margins=True)


def filter_dataframe(df, filters):
    """
    Aplica filtros múltiples a un DataFrame
    
    Args:
        df: DataFrame de pandas
        filters: Diccionario con filtros {columna: valores}
        
    Returns:
        DataFrame: DataFrame filtrado
    """
    df_filtered = df.copy()
    
    for column, values in filters.items():
        if values and column in df_filtered.columns:
            if isinstance(values, list):
                df_filtered = df_filtered[df_filtered[column].isin(values)]
            else:
                df_filtered = df_filtered[df_filtered[column] == values]
    
    return df_filtered


def get_missing_values_summary(df):
    """
    Genera resumen de valores faltantes
    
    Args:
        df: DataFrame de pandas
        
    Returns:
        DataFrame: Resumen de valores nulos
    """
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    summary = pd.DataFrame({
        'Columna': df.columns,
        'Valores_Nulos': missing.values,
        'Porcentaje': missing_pct.values
    })
    
    return summary[summary['Valores_Nulos'] > 0].sort_values('Valores_Nulos', ascending=False)


def create_summary_stats(df, column):
    """
    Crea estadísticas resumidas para una columna numérica
    
    Args:
        df: DataFrame de pandas
        column: Nombre de la columna
        
    Returns:
        dict: Diccionario con estadísticas
    """
    return {
        'Media': df[column].mean(),
        'Mediana': df[column].median(),
        'Desv. Estándar': df[column].std(),
        'Mínimo': df[column].min(),
        'Máximo': df[column].max(),
        'Q1 (25%)': df[column].quantile(0.25),
        'Q3 (75%)': df[column].quantile(0.75),
        'Rango': df[column].max() - df[column].min(),
        'Coef. Variación': (df[column].std() / df[column].mean()) * 100 if df[column].mean() != 0 else 0
    }


def export_to_excel(df, filename):
    """
    Exporta DataFrame a Excel
    
    Args:
        df: DataFrame de pandas
        filename: Nombre del archivo
        
    Returns:
        bool: True si se exportó correctamente
    """
    try:
        df.to_excel(filename, index=False)
        return True
    except Exception as e:
        print(f"Error al exportar: {str(e)}")
        return False


def create_color_palette(n_colors):
    """
    Crea una paleta de colores para visualizaciones
    
    Args:
        n_colors: Número de colores necesarios
        
    Returns:
        list: Lista de colores en formato hex
    """
    if n_colors <= 10:
        return px.colors.qualitative.Plotly[:n_colors]
    else:
        return px.colors.sample_colorscale("viridis", [i/(n_colors-1) for i in range(n_colors)])


def clean_text_column(series):
    """
    Limpia una columna de texto
    
    Args:
        series: Serie de pandas
        
    Returns:
        Series: Serie limpia
    """
    return series.str.strip().str.replace(r'\s+', ' ', regex=True)


def calculate_mode(series):
    """
    Calcula la moda de una serie
    
    Args:
        series: Serie de pandas
        
    Returns:
        Valor más frecuente
    """
    mode = series.mode()
    return mode[0] if len(mode) > 0 else None
