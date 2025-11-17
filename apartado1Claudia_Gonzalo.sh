#!/bin/bash

# =============================================================================
# SCRIPT: apartado1.sh
# DESCRIPCIÓN: Script de instalación de paquetes necesarios para Alpine Linux
# USO: Debe ejecutarse como usuario root
# AUTOR: Claudia Maria Lopez Bombin Y Gonzalo Velasco Lucas
# FECHA: Noviembre 2025
# =============================================================================

echo "=== SCRIPT DE INSTALACIÓN DE PAQUETES PARA ALPINE LINUX ==="
echo "Este script instala todos los paquetes necesarios para el proyecto"
echo "IMPORTANTE: Debe ejecutarse como usuario root"

# Lista de paquetes necesarios para el proyecto
PACKAGES=(
    "python3"           # Intérprete de Python 3
    "python3-dev"       # Librerías de desarrollo de Python
    "git"               # Sistema de control de versiones
    "nano"              # Editor de texto simple
    "sudo"              # Permisos de superusuario
    "bash"              # Shell Bash mejorado
    "gcc"               # Compilador C
    "g++"               # Compilador C++
    "musl-dev"          # Librerías de desarrollo musl
    "linux-headers"     # Headers del kernel Linux
    "wget"              # Utilidad para descargas web
    "curl"              # Cliente para transferencias URL
    "htop"              # Monitor de procesos interactivo
    "unzip"             # Utilidad para descomprimir archivos ZIP
)

echo ""
echo "Paso 1: Actualizando repositorios de Alpine..."
apk update

echo ""
echo "Paso 2: Verificando repositorio community..."
# El repositorio community debe estar habilitado para algunos paquetes
if ! grep -q "^[^#].*community" /etc/apk/repositories; then
    echo "ERROR: Repositorio community no está habilitado"
    echo "Para solucionar esto:"
    echo "1. Edita el archivo: nano /etc/apk/repositories"
    echo "2. Descomenta la línea que contiene 'community' (elimina el #)"
    echo "3. Guarda el archivo y ejecuta este script nuevamente"
    exit 1
else
    echo "✓ Repositorio community está habilitado"
fi

echo ""
echo "Paso 3: Instalando paquetes necesarios..."
for package in "${PACKAGES[@]}"; do
    # Verificar si el paquete ya está instalado
    if apk list --installed | grep -q "$package"; then
        echo "✓ Paquete $package ya está instalado"
    else
        echo "📦 Instalando $package..."
        apk add "$package"
        if [ $? -eq 0 ]; then
            echo "✓ $package instalado correctamente"
        else
            echo "✗ Error instalando $package"
        fi
    fi
done

echo ""
echo "Paso 4: Instalando librerías adicionales..."
# libc-dev es esencial para compilación de paquetes Python
apk add libc-dev
if [ $? -eq 0 ]; then
    echo "✓ libc-dev instalado correctamente"
else
    echo "✗ Error instalando libc-dev"
fi

echo ""
echo "=========================================="
echo "INSTALACIÓN COMPLETADA"
echo "Todos los paquetes necesarios han sido instalados"
echo "Ahora puedes configurar los permisos sudo para el usuario alumnoimat"
echo "=========================================="