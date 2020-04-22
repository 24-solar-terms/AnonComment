import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or '****'
    QQ_CLIENT_ID = os.environ.get('QQ_CLIENT_ID') or '****'
    QQ_CLIENT_SECRET = os.environ.get('QQ_CLIENT_SECRET') or '****'
    MANAGER_OPENID = os.environ.get('MANAGER_OPENID') or '****'


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = {
                'host': 'localhost',
                'user': 'root',
                'passwd': os.environ.get('MYSQL_PASSWORD') or '****',
                'database': 'acdb',
                'charset': 'utf8'
               }
    REDIRECT_URI = 'http://127.0.0.1:5000/authorize'


class ProductionConfig(Config):
    DATABASE = {
                'host': 'localhost',
                'user': 'root',
                'passwd': os.environ.get('MYSQL_PASSWORD') or '****',
                'database': 'acdb',
                'charset': 'utf8'
               }
    REDIRECT_URI = 'https://anoncomment.cn/authorize'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
