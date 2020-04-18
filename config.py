import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or '****'
    QQ_CLIENT_ID = '****'
    QQ_CLIENT_SECRET = '****'


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = {
                'host': 'localhost',
                'user': '****',
                'passwd': '****',
                'database': 'acdb',
                'charset': 'utf8'
               }
    REDIRECT_URI = 'http://127.0.0.1:5000/authorize'
    MEMCACHED_SERVER = ["127.0.0.1:11211"]


class ProductionConfig(Config):
    DATABASE = {}
    REDIRECT_URI = ''
    MEMCACHED_SERVER = []


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
