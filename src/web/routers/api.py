from loguru import logger

from src.web.app import app


@app.route('/health/readiness', methods=["GET"])
@logger.catch
def healthcheck():
    """
    Текущее состояние готовности сервиса
    """
    logger.info("Health checking started")
    return 200


@app.route('/health/liveness', methods=["GET"])
@logger.catch
def liveness():
    """
    Возвращает информацию о работоспособности сервиса
    """
    logger.info("Health checking started")
    return 200
