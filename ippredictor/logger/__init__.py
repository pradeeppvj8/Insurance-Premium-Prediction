import logging
from datetime import datetime
import os, sys

LOG_DIR = "application_logs"
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)

# Create logs directory
os.makedirs(LOG_DIR,exist_ok=True)

# Creating logging config
logging.basicConfig(
    level=logging.INFO,
    format= "[%(asctime)s : %(levelname)s : %(module)s : %(lineno)s : %(message)s]",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)
