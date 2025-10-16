import secrets

from flask import Flask, render_template

from controllers import auth_controller
from controllers import user_controller

# Gustavo de Souza
# Israel Victor
# Maria Eduarda Selhorst
# Yasmin Trembulack

app = Flask(__name__, template_folder="./views/templates", static_folder="./views/static")
app.secret_key = secrets.token_hex(32)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


auth_controller.configure_routes(app)
user_controller.configure_routes(app)


if __name__ == "__main__":
    app.run(debug=True)
