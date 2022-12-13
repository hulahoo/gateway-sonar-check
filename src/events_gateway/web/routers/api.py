from events_gateway.web.app import app
from events_gateway.config.log_conf import logger


@app.route('/health/readiness', methods=["GET"])
@logger.catch
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
@logger.catch
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
