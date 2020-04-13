import mysql.connector
import pandas as pd
import numpy as np
import re
from textfilter import DFAFilter


def init():
    """
    初始化数据库，建表操作
    :return: None
    """
    # 建表SQL语句
    create_teachers_table_sql = "CREATE TABLE teachers (" \
                                "t_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                                "name VARCHAR(10) NOT NULL," \
                                "pinyin VARCHAR(50) NOT NULL," \
                                "college VARCHAR(20) NOT NULL," \
                                "institute VARCHAR(30) NOT NULL," \
                                "department VARCHAR(20) NOT NULL," \
                                "degree VARCHAR(15)," \
                                "title VARCHAR(10)," \
                                "courses VARCHAR(255) NOT NULL," \
                                "tot_score BIGINT NOT NULL DEFAULT 0," \
                                "num BIGINT NOT NULL DEFAULT 0," \
                                "score FLOAT NOT NULL DEFAULT 0," \
                                "yes BIGINT NOT NULL DEFAULT 0," \
                                "percent FLOAT DEFAULT NULL);"

    insert_teachers_table_sql = "INSERT INTO teachers (name, pinyin, degree, title, courses, " \
                                "college, institute, department) " \
                                "VALUES " \
                                "(%s, %s, %s, %s, %s, %s, %s, %s);"

    create_comments_table_sql = "CREATE TABLE comments (" \
                                "c_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                                "t_id INT NOT NULL," \
                                "content VARCHAR(300) NOT NULL," \
                                "support INT NOT NULL DEFAULT 0," \
                                "post_time DATE NOT NULL);"

    create_user_comments_table_sql = "CREATE TABLE user_comments (" \
                                     "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                                     "openid VARCHAR(50) NOT NULL," \
                                     "t_id INT NOT NULL," \
                                     "score INT NOT NULL," \
                                     "yes INT NOT NULL," \
                                     "content VARCHAR(300) NOT NULL," \
                                     "c_id INT DEFAULT NULL);"

    create_user_supports_table_sql = "CREATE TABLE user_supports (" \
                                     "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                                     "openid VARCHAR(50) NOT NULL," \
                                     "c_id INT NOT NULL," \
                                     "t_id INT NOT NULL);"

    cursor.execute(create_teachers_table_sql)
    cursor.execute(create_comments_table_sql)
    cursor.execute(create_user_comments_table_sql)
    cursor.execute(create_user_supports_table_sql)

    # 获取老师信息并插入表
    with open('./app/static/data/data.csv', 'rb') as f:
        pd_data = pd.read_csv(f, header=None, encoding='gb18030', keep_default_na=False)

    data = np.array(pd_data)
    insert_data = list((tuple(i) for i in data))
    cursor.execute('USE acdb')
    cursor.executemany(insert_teachers_table_sql, insert_data)
    db.commit()


def select_all_teachers():
    """
    查询所有老师
    :return: 字典类型，key值表示部门，value值是一个列表，每个元素是一位老师的信息
    """
    table = {}
    select_sql = "SELECT t_id, name, pinyin, department FROM teachers;"
    cursor.execute(select_sql)
    teachers = cursor.fetchall()
    for teacher in teachers:
        if teacher[3] not in table.keys():
            table[teacher[3]] = []
        table[teacher[3]].append(str(teacher[0]) + ' ' + teacher[1] + ' ' + teacher[2])
    return table


def select_all_teachers_for_search():
    """
    查询所有老师信息，为模糊搜索提供数据
    :return: 字典类型，key：中文姓名+拼音，如'张三zhangsan'
                      value: 列表信息，[t_id, name, pinyin, score, department, degree, title]
    """
    info = {}
    select_sql = "SELECT t_id, name, pinyin, score, department, degree, title  FROM teachers;"
    cursor.execute(select_sql)
    teachers = cursor.fetchall()
    for teacher in teachers:
        key = teacher[1] + teacher[2] + str(teacher[0])
        teacher = list(teacher)
        # 分数保留两位小数
        teacher[3] = round(teacher[3], 2)
        info[key] = teacher
    return info


def select_teacher_info(teacher: str):
    """
    查询某位老师的信息和评论
    :param teacher: 字符串类型，组成为教师id+姓名拼音（没有+号），用于数据库查找该老师的评论
    :return: 返回列表信息
    """
    # 将teacher中的t_id利用正则表达式分离出来，以便进行查询
    t_id = int(re.match(r'([0-9]+)([a-z]+)', teacher).group(1))
    select_sql = "SELECT * FROM teachers WHERE t_id={}".format(t_id)
    cursor.execute(select_sql)
    # 将教师的信息列表化
    info = list(cursor.fetchone())
    if info[11]:
        # 将教师得分和点名率保留两位小数
        info[11] = round(info[11], 2)
        info[13] = round(info[13] * 100.0, 2)
    return info


def select_comments(t_id: int):
    """
    根据教师id查询对该老师的评论
    :param t_id: 整型，教师id
    :return: 返回comments和count
             comments：列表类型，每个元素为一条评论的所有信息，包括内容，时间，点赞数等
             count：元组类型，只有一个元素，为某位老师的所有评论数
    """
    # 默认按照点赞数排序获取评论
    select_sql = "SELECT * FROM comments WHERE t_id={} ORDER BY support DESC, c_id DESC".format(t_id)
    cursor.execute(select_sql)
    comments = cursor.fetchall()
    select_sql = "SELECT COUNT(*) FROM comments WHERE t_id={}".format(t_id)
    cursor.execute(select_sql)
    count = cursor.fetchone()
    return comments, count


def select_for_ranking():
    """
    获取所有老师的列表，为教师排行榜提供数据
    :return: 老师列表
    """
    select_sql = "SELECT t_id, name, pinyin, tot_score, num, score FROM teachers"
    cursor.execute(select_sql)
    teachers = cursor.fetchall()
    return teachers


def get_all_comments_num():
    """
    查询全站所有评论数
    :return: 返回字符串类型的评论数
    """
    sql = "SELECT COUNT(*) FROM comments"
    cursor.execute(sql)
    count = cursor.fetchone()
    return str(count[0])


def is_commented(openid: str, t_id: int):
    """
    根据openid和t_id查询用户评论表中是否有记录，没有则说明该用户未对该老师评论，
    否则评论过了，返回评论
    :param openid: 用户标识
    :param t_id: 老师id
    :return: 如果存在评论则返回评论列表，否则返回None
    """
    select_sql = "SELECT * FROM user_comments WHERE openid='{}' AND t_id={};".format(openid, t_id)
    cursor.execute(select_sql)
    res = cursor.fetchone()
    if res:
        return list(res)
    else:
        return None


def insert_comment(t_id: int, score: int, whether: int, comment: str, submit_date: str):
    """
    更新老师信息，插入一条新的评论到评论表
    :param t_id: 教师id
    :param score: 评论的分数
    :param whether: 是否点名
    :param comment: 评论内容
    :param submit_date: 提交时间
    :return: c_id
    """
    c_id = None
    # 更新老师信息
    update_sql = "UPDATE teachers SET tot_score=tot_score+{}, num=num+1, yes=yes+{}," \
                 "score=tot_score/num, percent=yes/num WHERE t_id={};".format(score, whether, t_id)
    cursor.execute(update_sql)
    if comment != "":
        # 如果评论内容不为空插入一条评论
        # 创建一个DFA敏感词过滤器
        dfa_filter = DFAFilter()
        dfa_filter.parse('keywords')
        comment = dfa_filter.filter(comment)
        insert_sql = "INSERT INTO comments (t_id, content, post_time) VALUES (%s, %s, %s);"
        val = (t_id, comment, submit_date)
        cursor.execute(insert_sql, val)
        # 获取c_id
        cursor.execute("SELECT LAST_INSERT_ID();")
        c_id = cursor.fetchone()[0]
    db.commit()
    return c_id


def insert_user_comment(openid: str, t_id: int, score: int, whether: int,
                        comment: str, c_id: int):
    """
    插入新纪录到用户评论表，即标记用户评论了该老师
    :param openid: 用户唯一标识
    :param t_id: 评论教师的id
    :param score: 评分
    :param whether: 是否点名
    :param comment: 评论内容
    :param c_id: 评论id
    :return: None
    """
    insert_sql = "INSERT INTO user_comments (openid, t_id, score, yes, content, c_id) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (openid, t_id, score, whether, comment, c_id)
    cursor.execute(insert_sql, val)
    db.commit()


def update_user_comment(teacher: str, openid: str, score: int, whether: int,
                        comment: str, submit_date: str):
    """
    用户更新自己对某位老师的评论
    :param teacher: 字符串类型，为评论老师的URL路径，如/1zhangsan
    :param openid: 字符串类型，当前用户的唯一标识
    :param score: int，更新后的评分
    :param whether: int，更新后的点名情况
    :param comment: str，更新后的评论
    :param submit_date: str，更新后的提交日期
    :return: None
    """
    t_id = int(re.match(r'/([0-9]+)([a-z]+)', teacher).group(1))
    old_comment = is_commented(openid, t_id)
    old_score = old_comment[3]
    old_whether = old_comment[4]
    c_id = old_comment[6]
    # 更新教师信息
    sql = "UPDATE teachers SET tot_score=tot_score-{}+{}, yes=yes-{}+{}," \
          "score=tot_score/num, percent=yes/num WHERE t_id={};".format(old_score, score,
                                                                       old_whether, whether,
                                                                       t_id)
    cursor.execute(sql)
    # 更新用户评论表
    sql = "UPDATE user_comments SET score={}, yes={}, content='{}'" \
          "WHERE openid='{}' AND t_id={};".format(score, whether, comment, openid, t_id)
    cursor.execute(sql)
    # 更新评论表
    # 原来没评论，现在有评论
    if not c_id and comment != "":
        sql = "INSERT INTO comments (t_id, content, post_time) VALUES (%s, %s, %s);"
        val = (t_id, comment, submit_date)
        cursor.execute(sql, val)
        # 获取c_id
        cursor.execute("SELECT LAST_INSERT_ID();")
        c_id = cursor.fetchone()[0]
        # 更新用户评论表的c_id
        sql = "UPDATE user_comments SET c_id={} WHERE openid='{}' AND t_id={};".format(c_id,
                                                                                       openid,
                                                                                       t_id)
        cursor.execute(sql)
    # 原来有评论，现在也有评论
    elif c_id and comment != "":
        sql = "UPDATE comments SET content='{}' WHERE c_id={};".format(comment, c_id)
        cursor.execute(sql)
    # 原来有评论，现在无评论
    elif c_id and comment == "":
        sql = "DELETE FROM comments WHERE c_id={}".format(c_id)
        cursor.execute(sql)
        sql = "DELETE FROM user_supports WHERE c_id={}".format(c_id)
        cursor.execute(sql)
        sql = "UPDATE user_comments SET c_id=NULL WHERE openid='{}' AND t_id={};".format(openid,
                                                                                         t_id)
        cursor.execute(sql)

    db.commit()


def update_user_support(openid: str, t_id: int, c_id: int, click: int):
    """
    单条修改点赞记录
    :param openid: 用户唯一标识字符串
    :param t_id: 用户点赞评论对应的老师id
    :param c_id: 点赞的评论id
    :param click: 点赞1或取消点赞0
    :return: None
    """
    if click:
        # 更新用户点赞表
        sql = "INSERT INTO user_supports (openid, c_id, t_id) VALUES (%s, %s, %s)"
        val = (openid, c_id, t_id)
        cursor.execute(sql, val)
        # 更新评论表中support字段
        sql = "UPDATE comments SET support=support+1 WHERE c_id={}".format(c_id)
        cursor.execute(sql)
    else:
        # 更新用户点赞表
        sql = "DELETE FROM user_supports WHERE openid='{}' AND c_id={}".format(openid, c_id)
        cursor.execute(sql)
        # 更新评论表中support字段
        sql = "UPDATE comments SET support=support-1 WHERE c_id={}".format(c_id)
        cursor.execute(sql)
    db.commit()


def get_like_list(openid: str, t_id: int):
    """
    根据openid和t_id查询用户对该老师的点赞评论，返回c_id列表
    :param openid: 字符串类型，用户的唯一标识
    :param t_id: int，老师id
    :return: 列表类型，每个元素是一个c_id
    """
    sql = "SELECT c_id FROM user_supports WHERE openid='{}' AND t_id={}".format(openid,
                                                                                t_id)
    cursor.execute(sql)
    like_list = cursor.fetchall()
    like_list = list(map(lambda x: x[0], like_list))
    return like_list


config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'guyu980324',
    'database': 'acdb',
    'charset': 'utf8'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

# 初始化数据库
cursor.execute('SHOW TABLES')
if not cursor.fetchall():
    init()
