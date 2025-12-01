#!/bin/bash

URL="https://drive.google.com/uc?export=download&id=1PHWBGuwDHw4ZEIlCbgMTiEUrG8FmlJK2"
PATH_GOWALLA_FILES="DatasetsGowalla/"
ARCHIVO_ZIP="DatasetsGowalla.zip"

# Crear directorios necesarios
mkdir -p "$PATH_GOWALLA_FILES"
mkdir -p "ProyectoFUSO/templates/html_files/"

# Descargar dataset si no existe
if [ ! -f "$ARCHIVO_ZIP" ]; then
    echo "Descargando dataset..."
    wget --no-check-certificate "$URL" -O "$ARCHIVO_ZIP"
    
    if [ -f "$ARCHIVO_ZIP" ]; then
        echo "Descomprimiendo..."
        unzip -o "$ARCHIVO_ZIP" -d "$PATH_GOWALLA_FILES"
    else
        echo "Error al descargar el dataset"
        exit 1
    fi
fi

> ALL_LOCATIONS.txt

ciudades=("ElPaso" "Glasgow" "Manchester" "WashingtonDC")

for ciudad in "${ciudades[@]}"; do
    echo ""
    echo "========================================"
    echo "Procesando ciudad: $ciudad"
    echo "========================================"
    
    archivo_ciudad="${PATH_GOWALLA_FILES}${ciudad}Gowalla.txt"
    
    if [ ! -f "$archivo_ciudad" ]; then
        echo "Archivo no encontrado: $archivo_ciudad"
        continue
    fi
    
    # Extraer datos
    cut -f3,4,5 "$archivo_ciudad" >> "ALL_LOCATIONS.txt"
    cut -f1,2,5 "$archivo_ciudad" > "${ciudad}filtered.txt"
    
    # Estadísticas
    total_usuarios=$(cut -f1 "$archivo_ciudad" | sort | uniq | wc -l)
    total_lugares=$(cut -f5 "$archivo_ciudad" | sort | uniq | wc -l)
    total_interacciones=$(wc -l < "$archivo_ciudad")
    
    echo "Número total de usuarios: $total_usuarios"
    echo "Número total de lugares: $total_lugares"
    echo "Número de interacciones: $total_interacciones"
    
    total_julio=$(cut -f2 "$archivo_ciudad" | grep -c '^2010-07')
    total_agosto=$(cut -f2 "$archivo_ciudad" | grep -c '^2010-08')
    echo "Check-ins julio 2010: $total_julio"
    echo "Check-ins agosto 2010: $total_agosto"
    
    # Top 5 usuarios
    echo "Generando top 5 usuarios..."
    python3 top_n.py "${ciudad}filtered.txt" 5 "top_5_${ciudad}.txt"
    
    # Generar mapas para top 5
    echo "Generando mapas para top 5 usuarios..."
    while read -r user visits; do
        if [[ ! -z "$user" ]]; then
            python3 generate_individual_maps.py \
                --user_id "$user" \
                --city_name "$ciudad" \
                --input_file "$archivo_ciudad" \
                --output_html "ProyectoFUSO/templates/html_files/user_${user}_${ciudad}.html"
        fi
    done < "top_5_${ciudad}.txt"
done

echo ""
echo "Análisis completado!"