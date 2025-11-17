#!/bin/bash

# =============================================================================
# SCRIPT: apartado_despliegue_Bash.sh
# DESCRIPCIÓN: Script para desplegar automáticamente el proyecto Flask
# USO: Ejecutar como usuario alumnoimat después de apartado1.sh
# AUTOR: Claudia Maria Lopez Bombin Y Gonzalo Velasco Lucas
# FECHA: Noviembre 2025
# =============================================================================

echo "=== INICIANDO DESPLIEGUE AUTOMÁTICO DEL PROYECTO FLASK ==="
echo "Este script clona el repositorio, instala dependencias y ejecuta la aplicación"

# Configuración de variables
PROJECT_DIR="ProyectoFUSO"                    # Directorio del proyecto
REPO_URL="https://github.com/pablosanchezp/ProyectoFUSO.git"  # URL del repositorio
VENV_DIR="venv"                               # Directorio del entorno virtual

echo ""
echo "Paso 1: Obteniendo el código del proyecto..."

# Verificar si el directorio del proyecto ya existe
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Clonando repositorio desde: $REPO_URL"
    git clone $REPO_URL
    if [ $? -eq 0 ]; then
        echo "✓ Repositorio clonado correctamente"
    else
        echo "✗ Error al clonar el repositorio"
        exit 1
    fi
else
    echo "El directorio $PROJECT_DIR ya existe"
    echo "Actualizando código existente..."
    cd $PROJECT_DIR
    git pull
    cd ..
    echo "✓ Código actualizado"
fi

echo ""
echo "Paso 2: Configurando entorno virtual de Python..."

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
    echo "✓ Entorno virtual creado en: $VENV_DIR"
else
    echo "✓ Entorno virtual ya existe"
fi

# Activar el entorno virtual
source $VENV_DIR/bin/activate
echo "✓ Entorno virtual activado"

echo ""
echo "Paso 3: Instalando dependencias Python..."

# Actualizar pip primero
pip install --upgrade pip
echo "✓ Pip actualizado"

# Instalar dependencias desde requirements.txt o individualmente
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "Instalando desde requirements.txt..."
    pip install -r $PROJECT_DIR/requirements.txt
else
    echo "Requirements.txt no encontrado, instalando dependencias manualmente..."
    pip install flask scikit-learn pandas numpy matplotlib seaborn memory-profiler joblib requests
fi

# Verificar instalación
if [ $? -eq 0 ]; then
    echo "✓ Dependencias instaladas correctamente"
else
    echo "✗ Error instalando dependencias"
    exit 1
fi

echo ""
echo "Paso 4: Creando estructura de directorios..."

# Crear directorio para archivos estáticos (imágenes, CSS, etc.)
mkdir -p $PROJECT_DIR/static
echo "✓ Directorio static creado"

# Crear directorio para archivos HTML de mapas
mkdir -p $PROJECT_DIR/templates/html_files
echo "✓ Directorio templates/html_files creado"

echo ""
echo "Paso 5: Iniciando la aplicación Flask..."
echo "La aplicación estará disponible en: http://<ip_maquina>:5000"

# Cambiar al directorio del proyecto y ejecutar
cd $PROJECT_DIR
python main.py

# Si la aplicación se cierra, mostrar mensaje
echo ""
echo "La aplicación Flask se ha detenido"
echo "Para reiniciar, ejecuta: cd $PROJECT_DIR && python main.py"