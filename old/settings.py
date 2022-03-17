# -*- coding: utf-8 -*-

# 访问 m.weibo.cn 的 request headers
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0'
}

# info for https://passport.weibo.cn/signin/login
USER_PASSWORD = [
    {
        'user': 'xxxxx',
        'password': 'xxxxx'
    }
]

# Chrome driver 的路径，前往 http://chromedriver.chromium.org/downloads 下载
CHROME_DRIVER_PATH = "D:\\software\\chromedriver.exe"

# 请求次数，每次请求返回的数据大约10条，因具体 API 而异
WAITING_FOR_REQUESTS = 1
# 停多少秒
DELAY = 2
# 允许同时爬取的最多用户数量
MAX_CRAWING_USERS = 1
