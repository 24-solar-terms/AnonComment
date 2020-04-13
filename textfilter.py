class DFAFilter(object):
    """
    基于DFA的敏感词过滤器
    """

    def __init__(self):
        """
        self.keyword_chains: DFA查询表，多层嵌套字典，本质上可以看成字典树，例如:
                             添加关键词‘傻瓜蛋’，‘傻瓜’，字典是下面的样子
                             {
                              '傻': {
                                     '瓜': {'蛋': {self.delimit: 0},
                                            self.delimit: 0
                                           }
                                    }
                             }
                             即‘傻瓜’后存在结束标志表示傻瓜是个敏感词，‘傻瓜蛋’同理
        self.delimit: 一个完整的敏感词的结束标志
        """
        self.keyword_chains = {}
        self.delimit = '\x00'

    def add(self, keyword):
        """
        添加一个新的敏感词
        :param keyword: 字符串类型，敏感词
        :return: None
        """
        # 预处理
        # 判断是否是Unicode编码，统一转换成utf-8
        if not isinstance(keyword, str):
            keyword = keyword.decode('utf-8')
        # 统一转换成小写处理
        keyword = keyword.lower()
        # 去掉首尾空白符
        chars = keyword.strip()
        # 关键词为空则返回，函数执行结束
        if not chars:
            return
        level = self.keyword_chains
        # 遍历关键词每个字符
        for i in range(len(chars)):
            # 如果该字符可以在当前层的字典中找到，说明已经存在公共前缀，则进入下一层字典
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                # 否则直接将当前位置到关键词结束添加到字典中
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                # 最后加上结束标志
                last_level[last_char] = {self.delimit: 0}
                break
        # 如果添加的某个关键词是已存在的字典中的某个公共前缀，则在结尾直接加上一个结束标志
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path):
        """
        添加某个敏感词词库
        :param path: 字符串类型，敏感词词库所在路径
        :return: None
        """
        with open(path, encoding='utf-8') as f:
            # 打开文件并对词库中的每个敏感词次逐一添加到DFA中
            for keyword in f:
                self.add(keyword.strip())

    def filter(self, message, repl="*"):
        """
        敏感词过滤
        :param message: 字符串类型，将要进行过滤的信息
        :param repl: 字符类型，用来替换敏感词的符号，默认为'*'
        :return: 字符串类型，过滤后的字符串
        """
        # 首先将字符串转成utf-8
        if not isinstance(message, str):
            message = message.decode('utf-8')
        # 作为小写字符处理
        message = message.lower()
        # 存放结果字符串的数组，最后会把所有元素连接返回
        ret = []
        # 起始位置
        start = 0
        while start < len(message):
            # 每次字典都要从最外层开始查找
            level = self.keyword_chains
            # 敏感词长度
            step_ins = 0
            # 从当前的起始位置往后遍历查找字典看是否存在敏感词
            for char in message[start:]:
                # 如果当前字符是当前层字典的一个key，说明有公共前缀
                if char in level:
                    # 敏感词长度+1
                    step_ins += 1
                    if self.delimit not in level[char]:
                        # 如果当前字符后面在字典中没有结束标志，说明不是完整敏感词，进入下一层继续查找
                        level = level[char]
                    else:
                        # 如果当前字符后面在字典中有结束标志，说明找到了一个完整的敏感词
                        # 将敏感词替换成等长'*'号放入结果数组
                        ret.append(repl * step_ins)
                        # 下次查询的位置从该敏感词后面一个字符开始
                        # 这里-1的原因是外层while循环每次固定+1
                        start += step_ins - 1
                        break
                else:
                    # 如果字符不是当前层字典的key，也就不可能作为敏感词的前缀
                    # 直接将该字符加入结果数组，从下一个位置查找
                    ret.append(message[start])
                    break
            else:
                # 当上面的for循环非break结束，而是正常迭代结束则执行此句
                # 此时说明从查询的起始位置start到字符串结束，只找到了敏感词前缀而没有找到完整敏感词
                # 此时仅将起始字符加入结果数组，然后再将下一个字符作为起始字符查找
                ret.append(message[start])
            start += 1
        # 将结果数组连接返回
        return ''.join(ret)
