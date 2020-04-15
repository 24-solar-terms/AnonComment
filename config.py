import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'UAEecJL6HlmG7xRgrphWhQkJuSVaywxz'
    QQ_CLIENT_ID = '101860705'
    QQ_CLIENT_SECRET = '78e232c1b0cb6ca59b84b3173a2869e5'


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = {
                'host': 'localhost',
                'user': 'root',
                'passwd': 'guyu980324',
                'database': 'acdb',
                'charset': 'utf8'
               }
    REDIRECT_URI = 'http://127.0.0.1:5000/authorize'


class ProductionConfig(Config):
    DATABASE = {}
    REDIRECT_URI = ''


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
