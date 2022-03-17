# weiboAPI

m.weibo.cn API 收集，利用这些 API 可以轻松获取用户微博、评论、转发信息。

## 用法

1. 首先前往 http://chromedriver.chromium.org/downloads 下载 Chrome driver。如果没有安装 Chrome 的话也需要安装上对应的版本。
2. 前往 [`progress.py`](progress.py) 配置开始爬取的种子用户，在 `crawling` 数组中加入一个用户 id。用户 id 获取的方法可以参考[这里](https://github.com/dataabc/weiboSpider/blob/b4172051adeba8d2f699c3209bafda63d8a12b1d/README.md#%E5%A6%82%E4%BD%95%E8%8E%B7%E5%8F%96user_id)。
3. 前往 [`settings.py`](settings.py) 配置账户、Chrome driver 路径、并行程度等其他信息。（目前并行没有做得很好，因为开多个 Chrome driver 的话需要重复地进行手动登录，建议 `MAX_CRAWING_USERS` 设为 1）
4. 执行 `make` 或者 `python spider.py` 开始运行爬虫。

## 注意事项

注意运行过程中可能需要手动进行登录操作，这是可以根据命令行提示进行操作。

因为一条微博的评论可以达到 20 万条甚至更多，为了节省资源（微博有爬取频次限制）、减少重复信息，对于一条微博只抓取前 200 条评论。

同时为了抓取到更广泛的信息，采用并行抓取方式，用户可自行在 `settings.py` 中设置最多并行爬取用户数。

## API

我整理成了网页，参见 https://upupming.site/weiboAPI/index.html

## 可能会遇到的问题

修复[输出重定向错误](http://blog.mathieu-leplatre.info/python-utf-8-print-fails-when-redirecting-stdout.html)：

```pwsh
$env:PYTHONIOENCODING = "utf_8"
```

运行（无需 Cookie）：

```pwsh
python.exe .\spider.py
```
