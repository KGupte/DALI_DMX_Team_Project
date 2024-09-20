import logging

class OLAFilter(logging.Filter):
    def filter(self, record):
        return "traceback.print_stack()" not in record.getMessage()

def configure_logging():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.addFilter(OLAFilter())
    return logger
