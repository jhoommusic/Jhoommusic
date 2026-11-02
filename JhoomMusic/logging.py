import logging

# Basic logging configuration
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)

# Suppress noisy libraries
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("tgcaller").setLevel(logging.WARNING)
logging.getLogger("yt_dlp").setLevel(logging.WARNING)

LOGGER = logging.getLogger
