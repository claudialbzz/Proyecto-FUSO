#!/bin/bash

ENV_NAME="venv"

python3 -m venv "$ENV_NAME"

source "$ENV_NAME/bin/activate"

pip install -r requirements.txt



REPO_URL=https://github.com/pablosanchezp/ProyectoFUSO.git


PROJECT_DIR="ProyectoFUSO"


MAIN_FILE="main.py"



if [ -d "$PROJECT_DIR/.git" ]; then
  echo "El directorio $PROJECT_DIR ya existe. Haciendo git pull..."
  cd "$PROJECT_DIR"
  git pull
else
  echo "Clonando repositorio en $PROJECT_DIR..."
  git clone "$REPO_URL" "$PROJECT_DIR"
  cd "$PROJECT_DIR"
fi

export FLASK_APP="$MAIN_FILE"
export FLASK_ENV="production"



if command -v flask >/dev/null 2>&1; then
  echo "http://<ip_maquina_alpine>:5000/"
  flask run --host=0.0.0.0 --port=5000
else
  echo "No se ha encontrado el comando 'flask'."
  echo "Intentando ejecutar directamente con python3 ${MAIN_FILE}..."
  echo "Si la app no se expone fuera de 127.0.0.1, revisa que en main.py se use host='0.0.0.0'."
  python3 "$MAIN_FILE"
fi

deactivate