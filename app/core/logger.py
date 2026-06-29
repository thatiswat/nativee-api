import logging
import sys

# --------------------------------------------------
# Logger Configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("nativeee")