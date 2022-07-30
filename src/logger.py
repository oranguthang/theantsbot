import logging
import sys

filename = "../the_ants_bot.log"
log_format = "%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s"
date_format = "%H:%M:%S"

logging.basicConfig(
    filename=filename,
    filemode="a",
    format=log_format,
    datefmt=date_format,
    level=logging.DEBUG
)

logger = logging.getLogger("TheAntsBot")

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(log_format, date_format)
handler.setFormatter(formatter)
logger.addHandler(handler)
