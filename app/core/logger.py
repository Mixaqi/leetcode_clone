import logging
from logging.handlers import RotatingFileHandler


FORMAT = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"


logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


file_handler = RotatingFileHandler(
    "app.log", maxBytes=500_000, backupCount=3, encoding="utf-8"
)
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter(FORMAT, "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
