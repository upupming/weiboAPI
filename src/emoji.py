# -*- coding: UTF-8 -*

from lxml import etree
import os, json
from util.Bmob import *
from util.table import *
import time

CUR_DIR = os.path.dirname(os.path.realpath('__file__')) + os.sep
BmobSDK.setup(config["bmob"]["APP_ID"], config["bmob"]["REST_API_KEY"])

def get_img_emojis():
    """
    返回两个数组，分别包含表情描述、表情图片网址
    """
    data = None
    with open(CUR_DIR + 'files/imgEmoji.html', 'r', encoding='UTF-8') as file:
        data = file.read()

    selector = etree.HTML(data)

    img_desc_arr = selector.xpath('//span/img/@alt')
    img_link_arr = selector.xpath('//span/img/@src')
    return (img_desc_arr, img_link_arr)

def get_unicode_emojis():
    """
    返回两个数组，分别包含表情英文描述、表情 Unicode 表示
    实测不太好用，只要是收集描述、表情的数据长度不匹配
    """
    data = None
    with open(CUR_DIR + 'files/unicodeEmoji.html', 'r', encoding='UTF-8') as file:
        data = file.read()

    selector = etree.HTML(data)

    unicode_emoji_arr = selector.xpath('//div[@class="emojis"]/text()')

    unicode_desc_arr = [[] for i in range(5)]
    index = 0
    started = False
    with open(CUR_DIR + 'files/unicodeDesc.html', 'r', encoding='UTF-8') as file:
        for data in file:
            if data == '\n':
                started = not started
                # 结束后将 index 加一
                if started == False and len(unicode_desc_arr[index]) > 0:
                    index += 1
            elif started and data.startswith(':'):
                # 去掉第一个冒号，最后一个冒号和换行符号
                unicode_desc_arr[index].append(data[1:len(data)-2])
            else:
                # 遇到 People 记得置为 False
                started = False
    lens = 0
    for i in range(5):
        print(f'len of desc {i}: {len(unicode_desc_arr[i])}')
        lens += len(unicode_desc_arr[i])
        print(f'len of emoji {i}: {len(unicode_emoji_arr[i])}')
    print(lens)
    return (unicode_desc_arr, unicode_emoji_arr)

def get_unicode_emojis_from_mdit():
    """
    返回 dict，以表情描述为 key、表情 Unicode 为 value
    """
    data = None
    # 此文件复制于 https://github.com/markdown-it/markdown-it-emoji/blob/master/lib/data/full.json
    with open(CUR_DIR + 'files/unicode.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
    return data

def insert_img_emojis():
    (img_desc_arr, img_link_arr) = get_img_emojis()
    for i in range(len(img_desc_arr)):
        emoji = Emoji(desc=img_desc_arr[i], content=img_link_arr[i])
        emoji.save()

def insert_unicode_emojis():
    data = get_unicode_emojis_from_mdit()
    for key in data.keys():
        emoji = Emoji(desc=key, content=data[key])
        emoji.save()


if __name__ == "__main__":
    insert_unicode_emojis()
    insert_img_emojis()