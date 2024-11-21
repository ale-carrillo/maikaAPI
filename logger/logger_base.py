import logging as log

class Logger:
    def __init__(self, log_file='bookshelf_api.log', level=log.INFO):
        log.basicConfig(
            level=level,
            format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%I:%M:%S %p',
            handlers=[
                log.FileHandler(log_file),
                log.StreamHandler()
            ]
        )
        self.logger = log.getLogger()

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == '__main__':
    logger = Logger()
    logger.debug('Message level: DEBUG')
    logger.info('Message level: INFO')
    logger.warning('Message level: WARNING')
    logger.error('Message level: ERROR')
    logger.critical('Message level: CRITICAL')
 a