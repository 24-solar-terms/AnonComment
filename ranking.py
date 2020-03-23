from acdb import select_for_ranking
import numpy as np
from functools import reduce

# 预设定的top30参评最少人数
m = 30
# 全局平均分
c = 0


def f(t):
    """
    计算每位老师的加权平均分
    :param t: 每位老师的信息列表
    :return: 计算完加权平均分后的老师信息列表
    """
    # 该老师评分人数
    v = float(t[4])
    # 该老师的算术平均分
    r = float(t[5])
    wr = v / (v + m) * r + m / (v + m) * c
    # 加权平均分保留2位小数
    t[6] = round(wr, 2)
    return list(t)


def ranking():
    """
    生成排行榜
    :return: 排行榜
    """
    global c
    # 获取每位老师信息
    teachers = select_for_ranking()
    rank = np.array(teachers)
    # 获取每位老师的总分数列表和评分人数列表
    tot_score_list = rank[:, 3]
    tot_num_list = rank[:, 4]
    # 计算全局平均分
    c = (reduce(lambda x, y: x + y, map(lambda x: float(x), tot_score_list)) /
         reduce(lambda x, y: x + y, map(lambda x: float(x), tot_num_list)))
    # 初始化加权平均分
    wr = np.zeros(rank.shape[0])
    # 将每位老师的信息和加权平均分合并
    rank = np.column_stack((rank, wr))
    # 按照公式计算加权平均分
    rank = list(map(f, rank))
    # 按照加权平均分排序
    rank = sorted(rank, key=lambda r: (-float(r[6]), -float(r[4]), float(r[0])))
    return list(enumerate(rank, start=1))

