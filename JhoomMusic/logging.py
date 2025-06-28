import logging

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)

LOGGER = logging.getLogger