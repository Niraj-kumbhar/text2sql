import logging
import logging.config
import os
from pathlib import Path

# Create logs directory if it doesn't exist
logs_dir = Path(__file__).parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d] %(funcName)s(): %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'embedding': {
            'format': '%(asctime)s [%(levelname)s] EMBED-%(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detailed',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'encoding': 'utf-8'
        },
        'error_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detailed',
            'filename': 'logs/error.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 3,
            'encoding': 'utf-8'
        },
        'embed_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'embedding',
            'filename': 'logs/embedding_notebook.log',
            'maxBytes': 5242880,  # 5MB
            'backupCount': 3,
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file_handler', 'error_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'text2sql': {
            'handlers': ['console', 'file_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'embed_handler': {
            'handlers': ['console', 'file_handler', 'error_handler'],
            'level': 'INFO',
            'propagate': False
        } 
    }
}

def setup_logging(config_dict=None, log_level=None):
    """
    Setup logging configuration for Docesh
    
    Args:
        config_dict: Custom logging configuration dictionary
        log_level: Override log level from environment
    """
    # Use environment variable for log level if available
    env_log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    if log_level:
        env_log_level = log_level.upper()
    
    # Update log levels based on environment
    if config_dict is None:
        config_dict = LOGGING_CONFIG.copy()
    
    # Apply environment log level
    if env_log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        config_dict['loggers']['']['level'] = env_log_level
        config_dict['loggers']['text2sql']['level'] = env_log_level
        
        # Console handler level adjustment
        if env_log_level == 'DEBUG':
            config_dict['handlers']['console']['level'] = 'DEBUG'
    
    logging.config.dictConfig(config_dict)
    
    # Test log entry
    logger = logging.getLogger(__name__)
    logger.info("Text2SQL logging configuration initialized")
    logger.debug(f"Log level set to: {env_log_level}")

def get_logger(name):
    """
    Get a logger instance
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)

# Convenience function for RAG components
def get_embed_logger(module_name):
    """
    Get a RAG-specific logger
    
    Args:
        module_name: Name of the RAG module
    
    Returns:
        logging.Logger: RAG-specific logger
    """
    return logging.getLogger(f"embed.{module_name}")