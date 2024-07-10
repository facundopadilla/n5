import logging

logger = logging.getLogger("n5-test")
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s: Line %(lineno)s | %(message)s"
    )
)
logger.addHandler(handler)
