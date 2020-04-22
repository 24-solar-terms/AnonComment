from flask import Flask
from config import config
from .tools.ac_database import AnonCommentDatabase
from .tools.qq_login_tool import QQLogin
from authlib.integrations.flask_client import OAuth
import memcache

# 创建数据库操作类实例
acdb = AnonCommentDatabase()
# 创建OAuth实例
oauth = OAuth()
# 创建QQ登录辅助类
qq = QQLogin()
# 创建memcached实例
mc = memcache.Client(["127.0.0.1:11211"])


def create_app(config_name):
    """
    工厂函数，创建应用实例
    :param config_name: 配置名
    :return: 应用实例
    """
    # 创建应用
    app = Flask(__name__)
    # 配置应用
    app.config.from_object(config[config_name])

    # 配置并初始化数据库操作类实例
    acdb.init_app(app)
    acdb.init_database()

    # 配置初始化OAuth
    oauth.init_app(app)
    oauth.register(
        name='qq',
        access_token_url='https://graph.qq.com/oauth2.0/token',
        authorize_url='https://graph.qq.com/oauth2.0/authorize',
        api_base_url='https://graph.qq.com'
    )

    # 配置初始化QQ登录辅助类
    qq.init_app(app)

    # 注册主蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
