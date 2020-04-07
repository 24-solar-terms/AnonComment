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

    cursor.execute(create_teachers_table_sql)
    cursor.execute(create_comments_table_sql)

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


def get_all_comments_num():
    """
    查询全站所有评论数
    :return: 返回字符串类型的评论数
    """
    sql = "SELECT COUNT(*) FROM comments"
    cursor.execute(sql)
    count = cursor.fetchone()
    return str(count[0])


def update_comment(t_id: int, score: int, whether: int, comment: str, submit_date: str):
    """
    更新老师信息，插入一条新的评论
    :param t_id: 教师id
    :param score: 评论的分数
    :param whether: 是否点名
    :param comment: 评论内容
    :param submit_date: 提交时间
    :return: None
    """
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
    db.commit()


def select_for_ranking():
    """
    获取所有老师的列表，为教师排行榜提供数据
    :return: 老师列表
    """
    select_sql = "SELECT t_id, name, pinyin, tot_score, num, score FROM teachers"
    cursor.execute(select_sql)
    teachers = cursor.fetchall()
    return teachers


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
