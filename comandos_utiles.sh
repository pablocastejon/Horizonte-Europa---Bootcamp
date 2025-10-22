#!/bin/bash

# ========================================
# Script de Comandos Útiles
# 9PM Bootcamp - Dashboard Project
# ========================================

echo "📊 Dashboard 9PM Bootcamp - Comandos Útiles"
echo "==========================================="
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐍 ENTORNO VIRTUAL${NC}"
echo "  Activar entorno:"
echo "    source venv/bin/activate"
echo ""
echo "  Desactivar entorno:"
echo "    deactivate"
echo ""

echo -e "${GREEN}📦 DEPENDENCIAS${NC}"
echo "  Instalar/Actualizar dependencias:"
echo "    pip install -r requirements.txt"
echo ""
echo "  Listar paquetes instalados:"
echo "    pip list"
echo ""
echo "  Añadir nueva dependencia:"
echo "    pip install <paquete>"
echo "    pip freeze > requirements.txt"
echo ""

echo -e "${GREEN}📓 JUPYTER NOTEBOOKS${NC}"
echo "  Iniciar Jupyter:"
echo "    jupyter notebook"
echo ""
echo "  Iniciar JupyterLab:"
echo "    jupyter lab"
echo ""
echo "  Ejecutar notebook específico:"
echo "    jupyter notebook notebooks/01_preprocesado.ipynb"
echo ""

echo -e "${GREEN}🚀 STREAMLIT DASHBOARD${NC}"
echo "  Ejecutar dashboard:"
echo "    cd app && streamlit run dashboard.py"
echo ""
echo "  Ejecutar con puerto específico:"
echo "    streamlit run dashboard.py --server.port 8502"
echo ""
echo "  Limpiar caché:"
echo "    streamlit cache clear"
echo ""

echo -e "${GREEN}📊 ANÁLISIS DE DATOS${NC}"
echo "  Ver estructura de datos con pandas:"
echo "    python -c \"import pandas as pd; df=pd.read_excel('data/9PM_bootcamp.xlsx'); print(df.info())\""
echo ""
echo "  Contar filas y columnas:"
echo "    python -c \"import pandas as pd; df=pd.read_excel('data/9PM_bootcamp.xlsx'); print(f'Filas: {len(df)}, Columnas: {len(df.columns)}')\"" 
echo ""

echo -e "${GREEN}🔧 GIT${NC}"
echo "  Ver estado:"
echo "    git status"
echo ""
echo "  Añadir cambios:"
echo "    git add ."
echo ""
echo "  Commit:"
echo "    git commit -m 'mensaje'"
echo ""
echo "  Push:"
echo "    git push origin main"
echo ""

echo -e "${GREEN}🧹 LIMPIEZA${NC}"
echo "  Limpiar archivos temporales:"
echo "    find . -type d -name '__pycache__' -exec rm -rf {} +"
echo "    find . -name '*.pyc' -delete"
echo "    find . -type d -name '.ipynb_checkpoints' -exec rm -rf {} +"
echo ""

echo "==========================================="
echo "💡 Para más información, consulta docs/README.md"
