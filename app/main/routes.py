from . import main
from .. import acdb
from .. import oauth
from .. import qq
from flask import render_template, redirect, request, session, url_for
from urllib.parse import urlparse, parse_qsl, unquote
from .forms import CommentForm
from ..tools.ranking import ranking
from ..tools.fuzzy_search import get_suggestions
from ..tools.url_tools import redirect_back
import re


# table字典的key值表示部门，value值是一个列表，每个元素是一位老师的信息
table = {}
# 模糊搜索时需要的老师数据信息
fuzzy_info = {}


@main.route('/')
@main.route('/index')
def index():
    """
    匿名评教首页
    :return: 渲染Jinja模板
    """
    # 查询数据库获得全站的总评论数
    tot_comments_num = acdb.get_all_comments_num()
    return render_template('index.html',
                           title='匿名评教',
                           tot_comments_num=tot_comments_num,
                           user_name=session.get('user_name'))


@main.route('/teachers')
def show_all_teachers():
    """
    显示所有老师界面
    1. 按照学院部门显示
    2. 按照排行榜显示
    :return: 渲染Jinja模板
    """
    # 使用全局教师table信息
    global table
    # 如果为空就调用数据库接口获取全部教师
    if not table:
        table = acdb.select_all_teachers()
    return render_template('teachers.html',
                           title='所有老师',
                           table=table,
                           user_name=session.get('user_name'))


@main.route('/<teacher>', methods=['GET', 'POST'])
def show_teacher(teacher: str):
    """
    显示每位老师具体信息的界面，包括老师信息和相关评价
    :param teacher: 字符串类型，组成为教师id+姓名拼音（没有+号，如1zhangsan）
                    用于数据库查找该老师的所有相关信息
    :return: 渲染Jinja模板
    """
    # 通过传入的参数查询获得数据库中该老师的信息
    info = acdb.select_teacher_info(teacher)
    # 获取该老师的所有评论和评论个数
    comments, count = acdb.select_comments(info[0])
    # 查询该用户是否对该老师有评价（包括评分，是否点名，评论）
    user_comment = acdb.is_commented(session.get('openid'), info[0])
    # 查询获取用户对该老师评论的点赞情况
    like_comments = acdb.get_like_list(session.get('openid'), info[0])
    # 实例化一个评价提交表单, 第一次评价该老师时使用
    submit_form = CommentForm()
    # 评论表单提交验证
    if submit_form.validate_on_submit():
        # 验证成功，获取表单数据，分数，是否点名，评论，提交日期
        score = submit_form.score.data
        whether_call_roll = submit_form.whether_call_roll.data
        comment = submit_form.comment.data
        submit_date = submit_form.submit_date.data
        # 更新老师信息，插入一条评价，同时获得评论id
        c_id = acdb.insert_comment(info[0], score, whether_call_roll, comment, submit_date)
        # 标记该用户评价了该老师，记录到数据库
        acdb.insert_user_comment(session.get('openid'), info[0], score, whether_call_roll, comment, c_id)
        # 重定向回该老师的页面
        return redirect('/'+teacher)

    return render_template('teacher.html',
                           title=info[1]+'-'+info[3]+info[4],
                           info=info,
                           form=submit_form,
                           count=count[0],
                           comments=comments,
                           user_comment=user_comment,
                           like_comments=like_comments,
                           user_name=session.get('user_name'))


@main.route('/update_user_comment', methods=['GET', 'POST'])
def update_user_comment():
    """
    用户修改对某位老师的评价
    :return: 如果直接请求，返回提交表单的Jinja模板片段
             如果使用提交表单提交，则重定向会该老师界面
    """
    # 实例化新的提交表单
    submit_form = CommentForm()
    if submit_form.validate_on_submit():
        # 验证成功，获取表单数据
        score = submit_form.score.data
        whether_call_roll = submit_form.whether_call_roll.data
        comment = submit_form.comment.data
        submit_date = submit_form.submit_date.data
        # 更新用户对该教师的评价，根据url获取老师id+姓名
        teacher = str(urlparse(request.referrer).path)
        # 更新用户的评价
        acdb.update_user_comment(teacher, session.get('openid'), score, whether_call_roll,
                                 comment, submit_date)
        return redirect_back('/')

    return render_template('comment_form.html', form=submit_form)


@main.route('/save_user_support')
def save_user_support():
    """
    传入点赞状态，并存入数据库
    :return: 字符串类型，成功状态字符串
    """
    # 通过GET方式从URL中获得传入的点赞状态数据字典，key为c_id，value为点赞1或取消点赞0
    like_state = dict(parse_qsl(unquote(urlparse(request.url).query)))
    # 获取必要信息
    openid = session.get('openid')
    teacher = str(urlparse(request.referrer).path)
    t_id = int(re.match(r'/([0-9]+)([a-z]+)', teacher).group(1))
    c_id = int(like_state['c_id'])
    click = int(like_state['click'])
    # 执行数据库操作
    acdb.update_user_support(openid, t_id, c_id, click)
    return "success"


@main.route('/rank')
def rank_by():
    """
    该函数处理每位老师评论的显示方式，按照最热评论和最新评论显示
    接收前端Ajax请求进行局部更新页面
    :return: 渲染Jinja模板片段
    """
    # 获取前端请求
    way = int(parse_qsl(urlparse(request.url).query)[0][1])
    # 这里必须重新请求数据库中的数据，防止数据不一致
    teacher = str(urlparse(request.referrer).path)
    t_id = int(re.match(r'/([0-9]+)([a-z]+)', teacher).group(1))
    # 获取该老师的评论，个数，以及该用户点赞评论的id列表
    comments, count = acdb.select_comments(t_id)
    like_comments = acdb.get_like_list(session.get('openid'), t_id)
    if not way:
        # 为0按照最热评论显示
        return render_template('show_comments.html',
                               count=count[0],
                               comments=comments,
                               like_comments=like_comments,
                               user_name=session.get('user_name'))
    else:
        # 为1按照最新评论显示，以c_id排序
        return render_template('show_comments.html',
                               count=count[0],
                               comments=sorted(comments, key=lambda t: t[0], reverse=True),
                               like_comments=like_comments,
                               user_name=session.get('user_name'))


@main.route('/ways')
def rank_or_departments():
    """
    显示所有老师界面，按照部门显示或按照排行榜显示
    接收Ajax请求，执行操作
    :return: 渲染Jinja模板片段
    """
    # 获取Ajax请求数据
    ways = int(parse_qsl(urlparse(request.url).query)[0][1])
    if not ways:
        # 为0按照部门显示
        return render_template('show_by_departments.html',
                               table=table)
    else:
        # 为1按照排行榜显示，获取最新排行榜，仅显示排名前30
        teachers = acdb.select_for_ranking()
        rank = ranking(teachers)
        return render_template('show_by_rank.html', rank=rank[:30])


@main.route('/search')
def search():
    """
    模糊搜索后端处理
    :return: 渲染Jinja模板
    """
    global fuzzy_info
    # 获取老师的数据，通过Ajax请求的关键词从中进行匹配
    if not fuzzy_info:
        fuzzy_info = acdb.select_all_teachers_for_search()
    # 从URL中获取GET请求数据
    request_data = dict(parse_qsl(urlparse(request.url).query))

    if 'tip' in request_data:
        # tip是request_data的key说明是为提示框提供数据发起的请求
        keyword = request_data['keyword']
        if keyword != '':
            # 当传入的keyword不为空才进行匹配
            suggestions, _ = get_suggestions(keyword, fuzzy_info)
            # 仅显示前八个匹配项
            return render_template('tip_list.html', suggestions=suggestions[:8])
    else:
        # 点击搜索框按钮
        # 如果没有输入任何东西直接搜索那么search_bar不是request_data的key
        # 此时直接返回首页
        if 'search_bar' not in request_data:
            return redirect('/')
        # 否则进行模糊匹配
        keyword = request_data['search_bar']
        session['keyword'] = keyword + ' '
        # flag=0表示直接匹配关键词获得的匹配结果
        # flag=1表示直接匹配汉字没有找到匹配项，得到的是换成拼音查找后的结果
        suggestions, flag = get_suggestions(keyword, fuzzy_info)
        # 返回搜索结果界面
        return render_template('search_results.html',
                               title=session.get('keyword') + '搜索结果',
                               keyword=session.get('keyword'),
                               results_num=len(suggestions),
                               suggestions=suggestions,
                               flag=flag,
                               user_name=session.get('user_name'))


# ------------------------以下是第三方登陆代码-------------------------------
@main.route('/login')
def login_page():
    """
    登录界面
    :return: 渲染Jinja模板
    """
    session['last_url'] = request.referrer
    return render_template('login.html')


@main.route('/logout')
def logout():
    """
    退出登录
    :return: 返回原地址
    """
    session.pop('user_name')
    return redirect_back('/')


@main.route('/qqlogin')
def login():
    """
    登录跳转
    :return: 重定向到QQ登陆授权
    """
    redirect_uri = url_for('.authorize', _external=True)
    return oauth.qq.authorize_redirect(redirect_uri)


@main.route('/authorize')
def authorize():
    """
    授权回调处理
    :return: 授权成功后返回登录之前的界面
    """
    # 获得用户信息和用户唯一标识openID
    user_data, openid = qq.get_user_info()
    # 保存用户信息到session
    session['user_name'] = user_data['nickname']
    session['openid'] = openid
    return redirect_back('/')
