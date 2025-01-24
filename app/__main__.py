from __future__ import annotations

import logging

from .bot import main

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
