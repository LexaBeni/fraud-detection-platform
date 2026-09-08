import logging
import sys

logger = logging.getLogger("fraud_api")
formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)