import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
LOG_FILE = PROJECT_ROOT / "app.log"

logger = logging.getLogger()
formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.setLevel(logging.INFO)

print(f"[Logger] Logging to: {LOG_FILE}")