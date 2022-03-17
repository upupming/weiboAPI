# -*- coding: UTF-8 -*

config = {
    # Bmob 配置
    'bmob': {
        'APP_ID': '366372322020724a39d8de5ccd61eeaa',
        'REST_API_KEY': '40de9f3e91287703e695fe1f6b94393a',
    },
    # 微博配置
    'weibo': {
        # Cookie 获取方法：前往 m.weibo.cn，打开一条评论较多的微博全文，往下翻几页
        # 这时 Chrome 的 Network 界面的 request headers 就会有 Cookie 信息了
        # 注意: m.weibo.cn 比较特殊，查看微博并不需要登录，而看评论确实是需要的
        # 比如直接进这个网址 https://m.weibo.cn/detail/4389138709375153，往后多翻几条评论在 Network 的 XHR 里面可以看到 request headers 的 Cookie
        'COOKIE': 'ALF=1564734503; SCF=AuUY2ywPv1KKDsxqBgngDXYn7XTsKn_5p4iBblRihSxO8mUlZ5DB13iaxpPOY50QQzi_qq8HXRkR0NEl6MjJ-Ts.; SUB=_2A25wGOOGDeRhGeFP4lcU9SfJzD-IHXVT4o3OrDV6PUJbktBeLW_RkW1NQO_UfEy6P_rwgaJHDE-0R3sOldFws7cD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5aERPgdESA6l4AaFTr3jGy5JpX5K-hUgL.FoMp1K-fSK.fS0e2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoM7SKnRe0eRe0z0; SUHB=0laVFNbqkGjoCM; _T_WM=68656738488; WEIBOCN_FROM=1110106030; MLOGIN=1; XSRF-TOKEN=aa01d1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076031669879400%26uicode%3D20000061%26fid%3D4389138709375153%26oid%3D4389138709375153'
    },
    'mysql': {
        'CONNECTION': {
            'host': "localhost",
            'user': 'upupming',
            'charset': 'utf8mb4'
        }
    },
    'crawl': {
        # 用来初始化爬取队列
        'START_USER': '2803301701',
        # 每两次请求之间等待 PERIOD 秒
        'PERIOD': 4,
        # 被封之后等待 5 分钟再次请求
        'FORBID_PAUSE': 300
    }
}
