import os
from logging.config import dictConfig

# TODO: configure logging based on config
# https://flask.palletsprojects.com/en/2.3.x/logging/
# dictConfig({
# 'version': 1,
# 'formatters': {'default': {
#     'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
# }},
# 'handlers': {'wsgi': {
#     'class': 'logging.StreamHandler',
#     'stream': 'ext://flask.logging.wsgi_errors_stream',
#     'formatter': 'default'
# }},
# 'root': {
#     'level': 'INFO',
#     'handlers': ['wsgi']
# }
# })

class Config:
    DEBUG = False
    DEVELOPMENT = False
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

class DevelopmentCfg(Config):
    DEBUG = True
    DEVELOPMENT = True