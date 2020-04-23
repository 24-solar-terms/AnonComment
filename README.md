# AnonComment
### Flask+mysql+memcached
目前只能支持电脑端使用

## 项目结构
```
|-AnonComment/
  |-app/
    __init__.py
    |-main/            
      __init__.py
      errors.py         # 错误处理
      forms.py          # WTForms表单模块
      routes.py         # 视图函数
    |-static/           
    |-templates/
    |tools/
      __init__.py
      ac_database.py    # 数据库操作模块
      fuzzy_search.py   # 模糊搜索模块
      keywords          # 敏感词关键词
      qq_login_tool.py  # QQ登录辅助模块
      ranking.py        # 教师排行榜模块
      textfilter.py     # 敏感词过滤模块
      url_tools.py      # URL工具模块
  config.py
  run.py
  requirements.txt
  README.md
```

## 功能实现
1. 教师评分，是否点名，评论
2. 教师排行榜，TOP30 ——参考IMDb TOP250排名算法
3. 点赞，举报
4. QQ登录，防止刷分、刷评论、刷赞，数据库只记录用户openID
5. 敏感词过滤——基于DFA
6. （伪）模糊搜索

## 待改进
1. 移动端访问惨不忍睹
2. 功能优化，添加
3. 性能优化