#!/bin/bash

# =============================================================================
# SCRIPT: apartado_despliegue_Bash.sh
# DESCRIPCIÓN: Script para desplegar automáticamente el proyecto Flask
# USO: Ejecutar como usuario alumnoimat después de apartado1.sh
# AUTOR: Claudia Maria Lopez Bombin Y Gonzalo Velasco Lucas
# FECHA: Noviembre 2025
# =============================================================================


echo "=== DESPLIEGUE AUTOMÁTICO DEL PROYECTO FLASK ==="
echo "Ejecutar como usuario alumnoimat"

# Verificar que estamos en Alpine
if ! command -v apk &> /dev/null; then
    echo "Este script está diseñado para Alpine Linux"
    exit 1
fi

# Configuración
PROJECT_DIR="ProyectoFUSO"
REPO_URL="https://github.com/pablosanchezp/ProyectoFUSO.git"
VENV_DIR="venv"

echo ""
echo "Paso 1: Instalando dependencias del sistema..."
sudo apk add python3 py3-pip git

echo ""
echo "Paso 2: Clonando repositorio..."
if [ ! -d "$PROJECT_DIR" ]; then
    git clone "$REPO_URL"
else
    echo "El proyecto ya existe, actualizando..."
    cd "$PROJECT_DIR"
    git pull
    cd ..
fi

echo ""
echo "Paso 3: Creando entorno virtual..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo ""
echo "Paso 4: Instalando dependencias Python..."
pip install --upgrade pip

# Instalar dependencias mínimas primero
pip install flask==2.3.3 Werkzeug==2.3.7

# Luego las demás
pip install scikit-learn pandas numpy matplotlib seaborn requests

echo ""
echo "Paso 5: Configurando directorios..."
mkdir -p "$PROJECT_DIR/static"
mkdir -p "$PROJECT_DIR/templates/html_files"

echo ""
echo "Paso 6: Iniciando aplicación..."
cd "$PROJECT_DIR"

echo "La aplicación se iniciará en: http://localhost:5000"
echo "Para acceder desde otra máquina: http://<ip_maquina>:5000"
echo ""
echo "Presiona Ctrl+C para detener la aplicación"
echo ""

python main.py