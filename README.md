# Weibo API

广度优先搜索按照 following 关系爬取所有微博、评论和表情，利用 MySQL 存储爬取到的微博信息，可以在 `config.py` 中进行配置。

![20190709143726](https://i.loli.net/2019/07/09/5d24362c388ad33617.png)

## 使用

1. 安装 MySQL，无需操心建表过程，程序自动完成
2. 前往配置 [config.py](src/util/config.py) 填充配置信息
3. 运行 `python src/main.py` 开始爬取

## 参考资料

1. [Request sessions](https://2.python-requests.org//en/latest/user/advanced/#session-objects)
2. [一行代码将 cookie 字符串转换成字典对象](https://foofish.net/extract_cookie.html)
3. [如何在requests session中手动设置cookie](https://blog.csdn.net/mgxcool/article/details/52663382)
4. [Python + MySQL 编码问题](https://stackoverflow.com/a/20349552/8242705)
