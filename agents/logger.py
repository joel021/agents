import logging
import os.path

from agents.config import WORK_DIR

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()  # Console handler

if not os.path.exists(WORK_DIR):
    os.makedirs(WORK_DIR, exist_ok=True)

f_handler = logging.FileHandler(f'{WORK_DIR}/logs.log')  # File handler

c_handler.setLevel(logging.WARNING)  # Set level for console
f_handler.setLevel(logging.DEBUG)    # Set level for file

# Create formatters and add them to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
