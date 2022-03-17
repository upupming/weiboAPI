import unittest
from spider import WBSpider

# 使用实例,输入一个用户id，所有信息都会存储在wb实例中
user_id = 1669879400  # 可以改成任意合法的用户id（爬虫的微博id除外）
filter = 0  # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
pic_download = 0  # 值为0代表不下载微博原始图片,1代表下载微博原始图片
wb = WBSpider(user_id, filter, pic_download)  # 调用Weibo类，创建微博实例wb
wb.start()  # 爬取微博信息

class TestStringMethods(unittest.TestCase):

    # def test_get_user_info(self):
    #     wb.get_user_info()
    #     assert wb.userInfo["screen_name"] == 'Dear-迪丽热巴'
    #     assert wb.weobo_containerid == "1076031669879400"
    def test_start(self):
        assert wb.total_pages > 0
        wb.start()

if __name__ == '__main__':
    unittest.main()