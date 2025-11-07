from flask import Flask, render_template, session

def configure_routes(app: Flask):
    
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html', logged_user=session.get('user'))

    @app.route('/contact', methods=['GET'])
    def contact():
        return render_template('contact.html', logged_user=session.get('user'))
