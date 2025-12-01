URL="https://drive.google.com/uc?export=download&id=1PHWBGuwDHw4ZEIlCbgMTiEUrG8FmlJK2"
PATH_MAIN_PYTHON="ProyectoFUSO/generate_maps.py"
PATH_GOWALLA_FILES="DatasetsGowalla/"
PATH_OUTPUT_GOWALLA_FILES="ProyectoFUSO/templates/html_files/"
ARCHIVO_ZIP="DatasetsGowalla.zip"

FILE_ID="1PHWBGuwDHw4ZEIlCbgMTiEUrG8FmlJK2"
if [ ! -f "$ARCHIVO_ZIP" ]; then
    wget --no-check-certificate "https://docs.google.com/uc?export=download&id=${FILE_ID}" -O "$ARCHIVO_ZIP"
    unzip $ARCHIVO_ZIP -d $PATH_GOWALLA_FILES
fi
> ALL_LOCATIONS.txt

ciudades=("ElPaso" "Glasgow"  "Manchester" "WashingtonDC")
for ciudad in "${ciudades[@]}"; do
    cut -f3,4,5 "${PATH_GOWALLA_FILES}${ciudad}Gowalla.txt" >> "ALL_LOCATIONS.txt"
    cut -f1,2,5 "${PATH_GOWALLA_FILES}${ciudad}Gowalla.txt" > "${ciudad}filtered.txt"
    total_usuarios=$(cut -f1 "${PATH_GOWALLA_FILES}${ciudad}Gowalla.txt" | sort | uniq | wc -l)
    total_lugares=$(cut -f3 "$PATH_GOWALLA_FILES""$ciudad""Gowalla.txt" | sort -d | uniq | wc -l)
    total_interacciones=$(wc -l < "$PATH_GOWALLA_FILES""$ciudad""Gowalla.txt")
    echo "Ciudad: "$ciudad
    echo "Número total de usuarios: "$total_usuarios
    echo "Número total de lugares: "$total_lugares
    echo "Número de interacciones: "$total_interacciones
    total_julio=$(cut -f2 "${PATH_GOWALLA_FILES}/${ciudad}Gowalla.txt" | grep -c '^2010-07')
    total_agosto=$(cut -f2 "${PATH_GOWALLA_FILES}/${ciudad}Gowalla.txt" | grep -c '^2010-08')
    echo "Número de interacciones en julio de 2010: "$total_julio
    echo "Número de interacciones en agosto de 2010: "$total_agosto
    py top_n.py "${ciudad}filtered.txt" 5 "top_5_${ciudad}.txt"
    while read -r user visits; do
        
        py generate_individual_maps.py \
            --user_id "$user" \
            --city_name "$ciudad" \
            --input_file "$PATH_GOWALLA_FILES""$ciudad""Gowalla.txt" \
            --output_html "ProyectoFUSO/templates/html_files/user_${user}_${ciudad}.html"
    done < "top_5_${ciudad}.txt"
done






