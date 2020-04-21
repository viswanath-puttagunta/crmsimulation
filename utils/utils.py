from config import config
import time


def dprint(message=""):
    if config.debug is True:
        print("{}: {}".format(time.time(), message))
