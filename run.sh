#!/bin/bash
set -x

# La primera vez poner: chmod +x run.sh
# Se ejecuta con: ./run.sh
# Si no instala bien poner en la terminal: rm -rf venv

# Ir al directorio donde está el script
cd "$(dirname "$0")"

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
  echo "🛠️  Creando entorno virtual 'venv'..."
  python3 -m venv venv || { echo "❌ Error al crear venv"; exit 1; }
fi

# Activar el entorno virtual
source venv/bin/activate

# Verificar si Flask está instalado, si no, instalar desde requirements.txt
if ! python3 -c "import flask" &>/dev/null; then
  echo "📦 Instalando dependencias desde requirements.txt..."
  pip install -r requirements.txt || { echo "❌ Error al instalar dependencias"; exit 1; }
fi

# Ejecutar la aplicación
echo "🚀 Ejecutando la app..."
python3 app.py
