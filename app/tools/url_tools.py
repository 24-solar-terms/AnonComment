from flask import request, redirect, session
from urllib.parse import urlparse, urljoin
import random
import string


def generate_random_str(length=16):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    :param length: 整型，生成随机字符串的长度
    :return: 字符串类型，随机生成的字符串
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for _ in range(length)]
    return ''.join(str_list)


def redirect_back(back_url):
    """
    返回触发当前URL的上一个URL
    :param back_url: 字符串类型，指定的返回URL
    :return:
    """
    for target in request.args.get('next'), request.referrer, session['last_url']:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(back_url)


def is_safe_url(target):
    """
    判断是否是安全的URL
    :param target: 字符串类型，要检测的URL
    :return: 安全返回True，否则返回False
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
