import json
import time
import logging
from collections import OrderedDict
import os
import ConfigParser
import StringIO
import splunk
from splunk.clilib import cli_common as cli
from splunk.appserver.mrsparkle.lib.util import make_url
import splunk.appserver.mrsparkle.lib.util as util
from splunk.appserver.mrsparkle.lib.util import make_splunkhome_path
from xml.dom import minidom
import traceback
import sys
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET


def setup_rotating_log_file():
    try:
        SPLUNK_HOME_LOG_PATH = make_splunkhome_path(["var", "log", "splunk"])
        LOG_FILENAME = ''
        # check to see if the SPLUNK_HOME based log path exists
        if not os.path.exists(SPLUNK_HOME_LOG_PATH):
            # check to see if the relative path based log path exists
            SPLUNK_BASE = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', '..', '..'))
            SPLUNK_BASE_LOG_PATH = os.path.join(SPLUNK_BASE, 'var', 'log', 'splunk')
            if not os.path.exists(SPLUNK_BASE_LOG_PATH):
                # disable logging with noop handler
                logger.addHandler(logging.NullHandler())
                return logger
            else:
                LOG_FILENAME = os.path.join(SPLUNK_BASE_LOG_PATH, 'document_builder.log')
        else:
            LOG_FILENAME = os.path.join(SPLUNK_HOME_LOG_PATH, 'document_builder.log')

        # valid log file path exists and rotate at 10 MB
        file_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10240000, backupCount=10)
        LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(name)s:%(lineno)d - %(message)s"
        file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
        return file_handler
    except:
        # disable logging with noop handler
        return logging.NullHandler()

def setup_logger(modulename):
    logger = logging.getLogger(modulename)
    logger.propagate = False # Prevent the log messages from being duplicated in the python.log file
    logger.setLevel(logging.INFO)
    logger.addHandler(rotating_log_file)
    return logger


# Initialize the rotating log file which we will use for multiple loggers.
rotating_log_file = setup_rotating_log_file()

# Initialize the first such logger.
logger = setup_logger('cloner_utils')
