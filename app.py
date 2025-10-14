import secrets

from flask import Flask

from controllers import main_controller

# Gustavo de Souza
# Israel Victor
# Maria Eduarda Selhorst
# Yasmin Trembulack

app = Flask(__name__, template_folder="./views/templates", static_folder="./views/static")
app.secret_key = secrets.token_hex(32)


main_controller.configure_routes(app)


if __name__ == "__main__":
    app.run(debug=True)
