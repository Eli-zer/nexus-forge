import logging
import sys
from typing import Dict, Any, Optional

def configure_logging(
    level: int = logging.INFO,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None
) -> None:
    """
    Configure basic logging for the application.
    
    Args:
        level: The logging level (default: INFO)
        log_format: Custom log format string (optional)
        date_format: Custom date format string (optional)
    """
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S"
    
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        stream=sys.stdout,
    )
    
    # Set to warning to reduce "noise" in logs
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    
    logging.info(f"Logging configured with level: {logging.getLevelName(level)}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: The name for the logger
        
    Returns:
        A configured logger instance
    """
    return logging.getLogger(name)