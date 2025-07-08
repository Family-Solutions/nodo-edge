"""Flask application entry point for the Smart Band Edge Service."""

from flask import Flask, jsonify

from iam.interfaces.services import iam_api
from location.interfaces.services import location_api
from shared.infrastructure.database import init_db

app = Flask(__name__)

# Configure Flask to handle JSON requests properly
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# Force Flask to always try to parse JSON, regardless of Content-Type
app.config['FORCE_PARSING_JSON'] = True

app.register_blueprint(iam_api)
app.register_blueprint(location_api)

@app.after_request
def after_request(response):
    """Add headers to every response to make the API more permissive."""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/v1/location', methods=['OPTIONS'])
@app.route('/api/v1/locations', methods=['OPTIONS'])
@app.route('/api/v1/sync-external', methods=['OPTIONS'])
@app.route('/api/v1/sync-to-collar', methods=['OPTIONS'])
def options():
    """Handle preflight requests."""
    return jsonify({'status': 'ok'}), 200

first_request = True

@app.before_request
def setup():
    """Initialize the database before the first request."""
    global first_request
    if first_request:
        first_request = False
        init_db()

@app.route("/")
def index():
    return "✅ Smart Band API funcionando. Endpoints disponibles:\n- POST /api/v1/location (crear ubicación)\n- GET /api/v1/locations (obtener todas las ubicaciones)\n- POST /api/v1/sync-external (sincronizar desde API externa)\n- POST /api/v1/sync-to-collar (enviar ubicaciones a collar API)\n\nNota: No se requiere autenticación"


if __name__ == "__main__":
    # 🌐 Iniciar túnel ngrok
    #public_url = ngrok.connect('127.0.0.1:5000', bind_tls=True)  # HTTPS -> Flask
    #print(f"🌍 URL pública ngrok: {public_url}")

    # Ejecutar la app Flask
    #app.run(port=5000)
    app.run(host="0.0.0.0", port=5000, debug=True)
