class InvalidUsage(Exception):

    def __init__(self, message, logger):
        Exception.__init__(self)
        logger.error(message)
        exit(1)
