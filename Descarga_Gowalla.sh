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


ciudades=("ElPaso" "Glasgow" "London" "Manchester" "New_YorkCity" "SanFrancisco" "WashingtonDC")
for ciudad in "${ciudades[@]}"; do
    cut -f3,4,5 "$PATH_GOWALLA_FILES""$ciudad""Gowalla.txt" >> "ALL_LOCATIONS.txt"
    cut -f1,2,5 ""$PATH_GOWALLA_FILES"""$ciudad""Gowalla.txt" > "$ciudad""filtered.txt"
    total_usuarios=$(cut -f1 "${PATH_GOWALLA_FILES}${ciudad}Gowalla.txt" | sort | uniq | wc -l)
    total_lugares=$(cut -f3 "$PATH_GOWALLA_FILES""$ciudad""Gowalla.txt" | sort -d | uniq | wc -l)
    total_interacciones=$(wc -l < "$PATH_GOWALLA_FILES""$ciudad""Gowalla.txt")
    echo "Ciudad: "$ciudad
    echo "Número total de usuarios "$total_usuarios
    echo "Número total de lugares "$total_lugares
    echo "Número de interacciones "$total_interacciones
done






