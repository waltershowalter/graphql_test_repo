###TestLogging.py###
__author__ = "Andrew.Fernandez"

import os
import sys
import constants
import logging
import logging.config

class TestLoggingMixin:

    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.logger = self.get_logger(os.path.join(self.script_dir, constants.LOG_FILE_LOCATION), logging.INFO, True)

    def get_logger(self, filename, level, stdout=False):
        format_str = constants.LOGGING_FORMAT_STR_COMPACT
        if stdout:
            logging.basicConfig(level=level, format=format_str)
        formatter = logging.Formatter(format_str)

        file_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=1048576, backupCount=5)
        file_handler.setFormatter(formatter)
        logging.getLogger('').addHandler(file_handler)

        logging.getLogger('').setLevel(level)


