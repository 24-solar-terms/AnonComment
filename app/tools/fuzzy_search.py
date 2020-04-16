import re
import pypinyin


def fuzzy_finder(user_input: str, collection: dict):
    """
    模糊搜索功能函数
    :param user_input: 字符串类型，用户输入的关键词
    :param collection: 字典类型，key为姓名+拼音+id如张三zhagnsan1，value为一个列表，包含了该老师的必要信息
    :return: 列表类型，符合条件的key列表
    """
    suggestions = []
    user_input = user_input.replace("'", '').lower()
    # 将 'djm' 转换为 'd.*?j.*?m'
    pattern = '.*?'.join(user_input)
    regex = re.compile(pattern)
    for item in collection:
        match = regex.search(item)
        if match:
            suggestions.append((len(match.group()), match.start(), item))

    return [x for _, _, x in sorted(suggestions)]


def get_suggestions(keyword: str, info: dict):
    """
    获取最终匹配的结果
    :param keyword: 字符串类型，用户输入的关键词
    :param info: 字典类型，key为姓名+拼音如张三zhagnsan，value为一个列表，包含了该老师的必要信息
    :return: 列表类型，每个元素也是一个列表包含了一位教师的信息
    """
    flag = 0
    suggestions = fuzzy_finder(keyword, info)
    suggestions = [info[x] for x in suggestions]
    # 如果直接匹配传入的关键词无匹配项，则把关键词转换成拼音再匹配一次
    if not suggestions:
        flag = 1
        pinyin = ''
        # 将关键词转成拼音
        for i in pypinyin.pinyin(keyword, style=pypinyin.NORMAL):
            pinyin += ''.join(i)
        suggestions = fuzzy_finder(pinyin, info)
        suggestions = [info[x] for x in suggestions]

    return suggestions, flag
