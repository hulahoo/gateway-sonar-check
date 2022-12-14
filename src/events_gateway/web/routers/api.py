import time
import psutil

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from events_gateway.config.log_conf import logger

app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)


def execute():
    """
    Main function to start Flask application
    """
    app.run(host='0.0.0.0', port='8080')


@app.route('/health/readiness', methods=["GET"])
def readiness():
    """
    Текущее состояние готовности сервиса
    """
    logger.info("Readiness checking started")
    return app.response_class(
        response={"status": "UP"},
        status=200,
        mimetype='application/json'
    )


@app.route('/health/liveness', methods=["GET"])
def liveness():
    """
    Возвращает информацию о работоспособности сервиса
    """
    logger.info("Liveness checking started")
    return app.response_class(
        response={"status": "UP"},
        status=200,
        mimetype='application/json'
    )


@app.route('/metrics', methods=["GET"])
def metrics():
    """
    Возвращает метрики сервиса
    """
    service_cpu_load = psutil.cpu_percent()
    service_ram_used = psutil.virtual_memory().total - psutil.virtual_memory().available
    time_ = round(time.time() * 1000)
    metrics = "cpu_load={cpu_load}, ram_used={ram_used}".format(
        cpu_load=service_cpu_load, ram_used=service_ram_used
    )
    result_message = "service_metrics{" + metrics + "}"

    return app.response_class(
        response=f"{result_message} {time_}",
        status=200,
        mimetype='text/plain'
    )
