import os
import secrets
from datetime import timedelta

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

app.permanent_session_lifetime = timedelta(days=3)

app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'True') == 'True',
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL', 'False') == 'True',
)

auth_controller.configure_routes(app)
user_controller.configure_routes(app)
book_controller.configure_routes(app)
review_controller.configure_routes(app)
public_controller.configure_routes(app)


if __name__ == "__main__":
    app.run(debug=False)
