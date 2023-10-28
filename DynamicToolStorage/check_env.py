
# File: env_checker.py
#!/usr/local/bin
import os

def check_env(required_vars):
    missing_vars = [var for var in required_vars if var not in os.environ]
    if missing_vars:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")