"""
log.py
Simple script based on logging python lib ( https://docs.python.org/2/library/logging.html )
That print a specifiq loggin formatte

# Usage :
debug = True
log = getLogger('yourAppName', debug)
log.info("Starting app")
log.info("Debug level %s" % log.level)
log.warning("Wrong name")
log.error("Error while doing something")
log.critical("Critical error, stopping now")
getDeltaToStart(log) # return time elapsed since the log creation
"""

import logging
from datetime import datetime

def getLogger(name=None, debug=False):
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.addHandler(ch)
    logger.start = datetime.now()

    return logger

def getDeltaToStart(logger=None):
    return 'Delta to start: %s' % (datetime.now()-logger.start)
