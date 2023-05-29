import logging

main_logger = logging.getLogger('main_log')
main_logger.level = logging.INFO
file_handler = logging.FileHandler('logs/main.log', 'a', 'utf-8')
formatter_main = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter_main)
main_logger.addHandler(file_handler)