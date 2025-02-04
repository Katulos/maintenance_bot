from __future__ import annotations

from . import utils
from .bot import main

logger = utils.logging.setup_logger().bind(type="business")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
