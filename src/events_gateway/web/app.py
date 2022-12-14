from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)


def execute():
    """
    Main function to start Flask application
    """
    app.run(host='0.0.0.0', port='8080')
