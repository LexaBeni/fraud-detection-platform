import logging

logger = logging.getLogger(__name__)
formater = logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
file_handler = logging.FileHandler("app.log")
stream_handler = logging.StreamHandler()
file_handler.setFormatter(formater)
stream_handler.setFormatter(formater)
logger.handlers = [stream_handler, file_handler]
logger.setLevel(logging.INFO)