import logging
import sys

def setup_logging():
    log_format = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    

    logging.basicConfig(
        level=logging.INFO,    
        format=log_format,         
        datefmt="%H:%M:%S",         
        handlers=[
            logging.StreamHandler(sys.stdout)  
        ]
    )