import logging
import sys

def get_logger(name):
    logger = logging.getLogger(name)
    stdout = logging.StreamHandler(stream=sys.stdout)
    fmt = logging.Formatter(
    fmt=(
            '%(asctime)s '
            '[%(levelname)-8s] '
            '[%(processName)s (%(process)d)] '
            '[%(threadName)s] '
            '%(module)s:%(lineno)d - %(message)s'
        ),
        datefmt='%d-%m-%Y %I:%M:%S %p IST'
    )
    stdout.setFormatter(fmt)
    logger.addHandler(stdout)
    logger.setLevel(level=logging.DEBUG)
    return logger
