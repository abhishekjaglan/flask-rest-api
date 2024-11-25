import logging

def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler('YouTubeAPI.log'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger('youTube API')
    logger.setLevel(logging.DEBUG)
    return logger

logger = setup_logger()