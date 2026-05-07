import logging
import os

os.makedirs("logs", exist_ok=True)

class UpgradeHttpErrors(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        if "HTTP" in msg and any(f" {code} " in msg for code in ["429", "500", "502", "503", "504"]):
            record.levelno = logging.ERROR
            record.levelname = "ERROR"
        return True

file_handler = logging.FileHandler("logs/errors.log")
file_handler.setLevel(logging.ERROR)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[file_handler, stream_handler]
)

httpx_logger = logging.getLogger("httpx")
httpx_logger.addFilter(UpgradeHttpErrors())

logger = logging.getLogger("dalelk")
