#!/bin/bash
set -x

# La primera vez: chmod +x run.sh
# Se ejecuta con: ./run.sh

# Ir al directorio donde está el script
cd "$(dirname "$0")"

# 1) Borra viejo venv para refrescar
echo "🗑️  Borrando entorno virtual 'venv' anterior (si existía)..."
rm -rf venv

# 2) Crea un nuevo entorno virtual
echo "🛠️  Creando entorno virtual 'venv'..."
python3 -m venv venv || { echo "❌ Error al crear venv"; exit 1; }

# 3) Activa el entorno virtual
source venv/bin/activate

# 4) Instala todas las dependencias
echo "📦 Instalando dependencias desde requirements.txt..."
pip install --upgrade pip          || { echo "❌ Error al actualizar pip"; exit 1; }
pip install -r requirements.txt    || { echo "❌ Error al instalar dependencias"; exit 1; }

# 5) Prepara carpeta de logs
mkdir -p logs

# 6) Ejecuta connector.py: logs a pantalla y a logs/connector.log
echo "🚀 Ejecutando connector.py (logs en logs/connector.log)…"
python3 connector.py 2>&1 | tee logs/connector.log &
echo $! > logs/connector.pid
echo "   → PID connector: $(cat logs/connector.pid)"

# 7) Ejecuta app.py: logs a pantalla y a logs/app.log
echo "🚀 Ejecutando app.py (logs en logs/app.log)…"
python3 app.py 2>&1 | tee logs/app.log &
echo $! > logs/app.pid
echo "   → PID app: $(cat logs/app.pid)"

# 8) Instrucciones y espera
echo
echo "🔍 Ahora verás en vivo los logs de ambos procesos en pantalla"
echo "   • connector.py → logs/connector.log"
echo "   • app.py       → logs/app.log"
wait
