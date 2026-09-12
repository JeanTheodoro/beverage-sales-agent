import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    # Suprime logs excessivos de bibliotecas de terceiros se necessário
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

setup_logging()
logger = logging.getLogger("bar_do_jaum")
