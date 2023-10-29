# File: env_checker.py
#!/usr/bin/env python3  # Corrected shebang line
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_env(required_vars):
    missing_vars = [var for var in required_vars if var not in os.environ]
    if missing_vars:
        error_message = f"Missing environment variables: {', '.join(missing_vars)}"
        logger.error(error_message)  # Log the error
        raise EnvironmentError(error_message)  # Raise error with message

# # Example Usage:
# if __name__ == "__main__":
#     required_vars = ['REQUIRED_VAR', 'OTHER_REQUIRED_VAR']
#     check_env(required_vars)
