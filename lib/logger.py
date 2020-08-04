import logging

logger = logging.getLogger("ScanLog")

def log(name, log_level):
    f = open("./log/" + name + ".log", "a+")
    handler = logging.StreamHandler(f)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%m/%d/%Y-%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
