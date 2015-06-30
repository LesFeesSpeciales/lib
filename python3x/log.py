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
