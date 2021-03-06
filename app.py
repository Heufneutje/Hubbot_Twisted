import argparse
import logging
import os
import sys
from hubbot.bothandler import BotHandler
from hubbot.config import Config, ConfigError
from newDB import createDB


def exceptionHandler(type, value, tb):
        logging.getLogger().exception("Uncaught exception: {}".format(str(value)))
        sys.__excepthook__(type, value, tb)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A derpy Twisted IRC bot.")
    parser.add_argument("-c", "--config", help="The configuration file to use", type=str, default="hubbot.yaml")
    parser.add_argument("-l", "--logfile", help="The file used for global error logging", type=str, default="hubbot.log")
    options = parser.parse_args()
    if not os.path.exists(os.path.join("hubbot", "data", "data.db")):
        createDB()
    # set up console output for general logging
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler(stream=sys.stdout)
    streamHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%H:%M:%S'))
    streamHandler.setLevel(logging.INFO)
    rootLogger.addHandler(streamHandler)
    # set up file for error logging
    fileHandler = logging.FileHandler(filename=options.logfile)
    fileHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y/%m/%d-%H:%M:%S'))
    fileHandler.setLevel(logging.WARNING)
    rootLogger.addHandler(fileHandler)
    # log all uncaught exceptions with the root logger
    sys.excepthook = exceptionHandler

    # actually start up the bot.
    config = Config(options.config)
    try:
        config.readConfig()
    except ConfigError:
        logging.exception("Failed to load config \"{}\".".format(options.config))
    else:
        bothandler = BotHandler(config)
