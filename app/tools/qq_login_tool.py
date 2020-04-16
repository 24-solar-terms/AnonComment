from flask import request
from .url_tools import generate_random_str
from urllib.parse import parse_qsl, urlsplit
import requests
import json


class QQLogin:
    """
    QQ第三方登录辅助工具类
    """

    def __init__(self):
        """
        初始化相关必要参数
        """
        self.authorize_url = 'https://graph.qq.com/oauth2.0/authorize'
        self.access_token_url = 'https://graph.qq.com/oauth2.0/token'
        self.openid_url = 'https://graph.qq.com/oauth2.0/me'
        self.user_info_url = 'https://graph.qq.com/user/get_user_info'
        self.client_id = ''
        self.client_secret = ''
        self.redirect_uri = ''

    def init_app(self, app):
        """
        通过应用实例配置该类
        :param app: 应用实例
        :return: None
        """
        self.client_id = app.config.get('QQ_CLIENT_ID')
        self.client_secret = app.config.get('QQ_CLIENT_SECRET')
        self.redirect_uri = app.config.get('REDIRECT_URI')

    def get_auth_code(self):
        """
        获取Authorization Code
        :return: 字符串类型，Authorization Code
        """
        auth_code = None
        # 请求参数
        data_dict = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': generate_random_str(24)
        }
        try:
            # 发起请求
            requests.get(url=self.authorize_url, params=data_dict)
            # 获取code
            auth_code = dict(parse_qsl(urlsplit(request.url).query))['code']
        except Exception as e:
            print('获取Authorization Code失败：\n{}'.format(e))

        return auth_code

    def get_access_token(self):
        """
        获取通过Authorization Code获取Access Token
        :return: 字符串类型，Access Token
        """
        access_token = None
        # 首先获取Authorization Code
        auth_code = self.get_auth_code()
        # 请求参数
        data_dict = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': auth_code
        }
        try:
            # 请求并获取Access Token
            response = requests.get(url=self.access_token_url, params=data_dict)
            access_token = dict(parse_qsl(response.text))['access_token']
        except Exception as e:
            print('获取Access Token失败：\n{}'.format(e))

        return access_token

    def get_openid(self):
        """
        通过Access Token获取openID
        :return: 字符串类型，openID
        """
        openid = None
        # 首先获取Access Token
        access_token = self.get_access_token()
        # 请求参数
        data_dict = {'access_token': access_token}
        try:
            # 发起请求，获得数据
            response = requests.get(url=self.openid_url, params=data_dict)
            openid = json.loads(response.text[10:-3])['openid']
        except Exception as e:
            print('获取openID失败：\n{}'.format(e))

        return openid, access_token

    def get_user_info(self):
        """
        获取用户信息
        :return: 字典类型，返回用户信息字典
        """
        # 获取openid，同时可以获得access token
        openid, access_token = self.get_openid()
        # 请求参数
        data_dict = {
            'access_token': access_token,
            'oauth_consumer_key': self.client_id,
            'openid': openid
        }
        try:
            response = requests.get(url=self.user_info_url, params=data_dict)
            user_data = json.loads(response.text)
        except Exception as e:
            print('获取用户信息失败：\n{}'.format(e))

        return user_data, openid
