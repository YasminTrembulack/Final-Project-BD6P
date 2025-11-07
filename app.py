import secrets

from flask import Flask

from controllers import auth_controller
from controllers import user_controller
from controllers import book_controller
from controllers import review_controller
from controllers import public_controller

# Gustavo de Souza
# Israel Victor
# Maria Eduarda Selhorst
# Yasmin Trembulack

app = Flask(__name__, template_folder="./views/templates", static_folder="./views/static")
app.secret_key = secrets.token_hex(32)


auth_controller.configure_routes(app)
user_controller.configure_routes(app)
book_controller.configure_routes(app)
review_controller.configure_routes(app)
public_controller.configure_routes(app)


if __name__ == "__main__":
    app.run(debug=True)
