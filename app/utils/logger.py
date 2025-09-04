# Logger setup
import logging

logger = logging.getLogger(__name__)

def setup_logger():
    """
    Sets up basic logging to stdout.
    - Level: INFO
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logger.info("Logger setup complete.")