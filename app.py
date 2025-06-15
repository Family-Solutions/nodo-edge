"""Flask application entry point for the Smart Band Edge Service."""

from flask import Flask

import iam.application.services
from iam.interfaces.services import iam_api
from location.interfaces.services import location_api
from shared.infrastructure.database import init_db

app = Flask(__name__)
app.register_blueprint(iam_api)
app.register_blueprint(location_api)

first_request = True

@app.before_request
def setup():
    """Initialize the database and create a test device before the first request."""
    global first_request
    if first_request:
        first_request = False
        init_db()
        auth_application_service = iam.application.services.AuthApplicationService()
        auth_application_service.get_or_create_test_device()

@app.route("/")
def index():
    return "✅ Smart Band API funcionando. Usa /api/v1/location para enviar datos."


if __name__ == "__main__":
    app.run(debug=True)
