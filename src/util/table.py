from .Bmob import BmobSDK, BmobModel

class Emoji(BmobModel):
    desc = ''
    content = ''

class Crawling(BmobModel):
    uid = 0
    uname = ''

class Crawled(BmobModel):
    uid = 0
    uname = ''

class Weibo(BmobModel):
    mid = ''
    text = ''
    img_emoji = []

class Comment(BmobModel):
    cid = ''
    mid = ''
    text = ''
    img_emoji = []
