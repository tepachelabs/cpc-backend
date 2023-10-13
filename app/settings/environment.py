import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

PRODUCTION = ENVIRONMENT in ["PROD", "prod", "production", "PRODUCTION"]
