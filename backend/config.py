import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

class DevelopmentCfg(Config):
    DEBUG = True
    DEVELOPMENT = True