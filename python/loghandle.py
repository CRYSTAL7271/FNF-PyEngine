import os, sys, logging
from datetime import datetime
from python.settings import Properties


class LogHandler:
    logger = logging.getLogger(__name__)
    current_time = datetime.now()
    logname = f"errors/error{current_time.strftime('%d%m%Y_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.DEBUG,
    )
    logfile = logging.FileHandler(logname)
    logger.addHandler(logfile)

    def printLog(message):
        # print(f"[DEBUG] {message}")
        if Properties.Debug:
            LogHandler.logger.debug(message)

    def printWarning(message):
        # print(f"[WARNING] {message}")
        LogHandler.logger.warning(message)
