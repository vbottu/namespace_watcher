import logging
# Configures and returns a logger instance
def get_logger(name: str) -> logging.Logger:
  
    # Create a logger instance
    logger = logging.getLogger(name)
    
    # Set the logging level
    logger.setLevel(logging.INFO)
    
    # Define a log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Avoid adding duplicate handlers if the logger is already configured
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger
