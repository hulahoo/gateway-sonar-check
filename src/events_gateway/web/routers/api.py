import time
import psutil

from events_gateway.web.app import app
from events_gateway.config.log_conf import logger


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
