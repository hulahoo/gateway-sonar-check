from src.web.app import app


@app.route('/hello_world', methods=["GET"])
def hello_world():
    return 'Hello, World!'
