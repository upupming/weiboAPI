# -*- coding: UTF-8 -*-
import settings, requests, sys, traceback, json, os, time, random, csv, tqdm, threading
import logging, datetime
from lxml import etree
import progress
from selenium import webdriver, common

INFO_URL = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'
WEIBO_URL = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid={}&page={}'
LONG_WEIBO_URL = 'https://m.weibo.cn/statuses/extend?id={}'
COMMENT_URL = 'https://m.weibo.cn/api/comments/show?id={}&page={}'
COMMENT_URL1 = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type={}'
COMMENT_URL2 = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type={}&max_id={}'

# 现在爬取第几次
num_requested = 0
# 正在爬取的用户
crawling_user_ids = []
# 等待爬取的用户
waiting_user_ids = []
# 已经爬取完毕的用户
crawled_user_ids = progress.crawled

current_user_index = 0


# http://nladuo.github.io/2018/12/08/那些年，我爬过的北科-六-——反反爬虫之js渲染
# 微博评论貌似有反爬机制，因此使用『无头浏览器』，模仿 Chrome 浏览器
# 比如这个请求在 Chrome 就 okay，但是用普通的 request 就会返回登陆的 html：
# https://m.weibo.cn/comments/hotflow?id=1669879400&mid=4384122253963002&max_id_type=0&max_id=261294286701954
# 最后发现其实是需要 Cookie，我在 Chrome Driver 里面登录来获取 Cookie（第二页以及以后的均需要 Cookie）
# selenium 的使用参考文档 https://selenium-python.readthedocs.io
driver = webdriver.Chrome(settings.CHROME_DRIVER_PATH)
logged = False

def login():
    driver.get('https://passport.weibo.cn/signin/login')
    print('请进入 https://passport.weibo.cn/signin/login 后按 Enter 键继续')
    os.system("pause")
    driver.find_element_by_id('loginName').send_keys(settings.USER_PASSWORD[current_user_index]['user'])
    driver.find_element_by_id('loginPassword').send_keys(settings.USER_PASSWORD[current_user_index]['password'])
    # https://stackoverflow.com/questions/21350605/python-selenium-click-on-button
    # driver.find_element_by_id('loginAction').click()
    print(f'密码已经填好，请完成登录之后按 Enter 继续（可能需要人工拖动滑块验证）')
    os.system("pause")
    logged = True

# See https://osf.io/upav8/
# Line by line https://github.com/rkern/line_profiler
import cProfile, pstats, io
def profile(fnc):
    
    """A decorator that uses cProfile to profile a function"""
    
    def inner(*args, **kwargs):
        
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        logging.info(s.getvalue())
        return retval

    return inner

class WBSpider():
    @staticmethod
    def spide(user_id=1669879400):
        """
        user_id 可以改成任意合法的用户id
        """
        # 使用实例,输入一个用户id，所有信息都会存储在wb实例中
        pic_download = 0  # 值为0代表不下载微博原始图片,1代表下载微博原始图片
        wb = WBSpider(user_id, pic_download)  # 调用Weibo类，创建微博实例wb
        t1 = threading.Thread(target=wb.start)
        t1.start()
        # try:
        #     _thread.start_new_thread(wb.start, ("ssssss",))
        # except Exception as e:
        #     logging.error(str(e))
        #     logging.error("Error: unable to start thread")

    def __init__(self, user_id, pic_download=0):
        """Weibo类初始化"""
        if not isinstance(user_id, int):
            sys.exit(u"user_id值应为一串数字形式,请重新输入")
        if pic_download != 0 and pic_download != 1:
            sys.exit(u"pic_download值应为0或1,请重新输入")
        self.user_id = user_id  # 用户id,即需要我们输入的数字,如昵称为"Dear-迪丽热巴"的id为1669879400
        self.pic_download = pic_download  # 取值范围为0、1,程序默认值为0,代表不下载微博原始图片,1代表下载
        # 根据抓取信息赋值
        self.userInfo = None
        self.weobo_containerid = None
        self.total_pages = 0
        self.all_cards = []
        self.all_comments = []
        self.got_num = 0
        self.comments_got_num = 0
        self.got_comments_mids = []

    def request_data(self, url):
        logging.info(f'Requesting {url}...')
        driver.get(url)
        # driver.save_screenshot("screenshot.png")  # 截个图
        # print(driver.page_source)  # 打印源码
        try:
            json_str = driver.find_element_by_css_selector("pre").text
        except:
            logging.info(f'{url} 的请求结果无法转为 json：{driver.page_source}')
            try:
                driver.find_element_by_xpath("//body/div/p[@class='h5-4con']")
                print('请求过于频繁，将切换当前使用的用户重新登录...')
                global current_user_index
                current_user_index = (current_user_index + 1) % len(settings.USER_PASSWORD)
                login()
            except common.exceptions.NoSuchElementException:
                # 不是请求过于频繁的话，目前默认是没有正确登录
                login()
            return self.request_data(url)
        # print(text)
        res_obj = json.loads(json_str, encoding='UTF-8')

        global num_requested
        num_requested += 1
        if num_requested % settings.WAITING_FOR_REQUESTS == 0:
            logging.info(f'当前已经请求 {num_requested} 次，等待 {settings.DELAY} 秒')
            time.sleep(settings.DELAY)

        # response = requests.get(url, headers=settings.DEFAULT_REQUEST_HEADERS)
        # if response.status_code >= 400:
        #     rand = random.randint(6, 10)
        #     logging.info(f"出现错误状态码 {response.status_code}，等待 {rand} 秒")
        #     time.sleep(rand)
        #     return self.request_data(url)
        # try:
        #     data = response.json()
        # except Exception as e:
        #     rand = random.randint(6, 10)
        #     logging.info(f"出现 HTML {response.content}，等待 {rand} 秒")
        #     time.sleep(rand)
        #     return self.request_data(url)
        # if res_obj == None:
        #     rand = random.randint(6, 10)
        #     logging.info(f"出现状态码 {res_obj.status_code}，空返回结果，等待 {rand} 秒")
        #     time.sleep(rand)
        #     return self.request_data(url)
        # if data["ok"] == 0:
        #     if data["msg"] == "请求过于频繁,歇歇吧":
        #         rand = random.randint(6, 10)
        #         logging.info(f"访问被限制，等待 {rand} 秒")
        #         time.sleep(rand)
        #         return self.request_data(url)
        # assert data["ok"] == 1
        # 有时候会得到：
        # {'ok': 0, 'msg': '这里还没有内容', 'data': {'cards': []}}
        return res_obj["data"]

    def save_json(self, data, type='userinfo.json'):
        json_path = self.get_filepath(type)
        with open(json_path, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=2)

    def start(self):
        """运行爬虫"""
        try:
            if crawling_user_ids.count(self.user_id):
                logging.warning(f'uid {self.user_id} 正在爬取，拒绝加入到爬取池')
                return
            elif crawled_user_ids.count(self.user_id):
                logging.warning(f'uid {self.user_id} 已经爬取完毕，拒绝加入到爬取池')
                return
            elif waiting_user_ids.count(self.user_id):
                logging.warning(f'uid {self.user_id} 正在等待被抓取，拒绝加入到爬取池')
                return
            elif len(crawling_user_ids) < settings.MAX_CRAWING_USERS:
                crawling_user_ids.append(self.user_id)
                logging.info(f'uid {self.user_id} 加入到爬取池')
            else:
                waiting_user_ids.append(self.user_id)
                logging.info(f'uid {self.user_id} 加入到等待池')
                return
            if not self.get_user_info():
                logging.error('获取用户信息中断')
                return
            if not self.get_all_weibo():
                logging.error('获取所有微博中断')
                return
            crawling_user_ids.remove(self.user_id)
            crawled_user_ids.append(self.user_id)
            # 存成文件避免下次启动时重复爬取
            with open('./progress.py', 'w', encoding='UTF-8') as crawled_py:
                crawled_py.write(f'crawled = {crawled_user_ids}\n')
                crawled_py.write(f'crawling = {crawling_user_ids}\n')
            logging.info(f"【uid: {self.user_id}, 昵称: {self.userInfo['screen_name']}】爬取完毕，已经从爬取池中删除")
            if len(waiting_user_ids) > 0:
                wuid = waiting_user_ids.pop()
                logging.info(f"uid {self.user_id}  被取出等待池中")
                WBSpider.spide(wuid)
            logging.info("*" * 100)
            if self.pic_download == 1:
                self.download_pictures()
        except Exception as e:
            logging.error(str(e))
            traceback.print_exc()

    def get_user_info(self):
        """获取用户信息"""
        try:
            url = INFO_URL.format(self.user_id)
            data = self.request_data(url)
            self.userInfo = data["userInfo"]
            self.weobo_containerid = data["tabsInfo"]["tabs"][1]["containerid"]
            self.save_json(data)
            return True
        except Exception as e:
            logging.error(str(e))
            traceback.print_exc()

    def get_comments(self, mid, max_num=200):
        """
        max_num: 因为很多重复评论没有意义，所以最多抓取 200 条即可
        """
        if self.got_comments_mids.count(mid):
            logging.info(f'mid={mid} 的评论已经收集好了，不再收集')
            return
        url = COMMENT_URL1.format(self.user_id, mid, 0)
        data = self.request_data(url)
        max_id = data["max_id"]
        max_id_type = data["max_id_type"]
        wrote_num = 0
        page = 0
        while True:
            page += 1
            url = COMMENT_URL2.format(self.user_id, mid, max_id_type, max_id)
            data = self.request_data(url)
            if data == None:
                break
            max_id = data["max_id"]
            max_id_type = data["max_id_type"]
            for comment in data["data"]:
                # print(comment)
                # exit()
                selector = etree.HTML(comment["text"])
                self.all_comments.append({'mid': mid, 'id': comment["id"], 'created_at': comment["created_at"], 'user_id': comment["user"]["id"], 'text': etree.tostring(selector, method="text", encoding="UTF-8").decode('utf-8'), 'img_emoji': selector.xpath("//span/img/@alt")})
                self.comments_got_num += 1

                # 把评论用户也加入爬取池
                uid = comment["user"]["id"]
                uname = comment["user"]["screen_name"]
                logging.info(f'尝试抓取评论者 {uid}, {uname}')
                WBSpider.spide

            if page % 20 == 0:  # 每爬20页写入一次文件
                    # 写文件
                    if self.comments_got_num > wrote_num:
                        self.write_comment_csv(wrote_num, type=f"{mid}.comments.csv")
                    wrote_num = self.comments_got_num
            
            # 评论已经够用了
            if self.comments_got_num >= max_num:
                break
            # 经测试，这是评论终止条件
            if max_id == 0 and max_id_type == 0:
                break

        self.write_comment_csv(wrote_num, type=f"{mid}.comments.csv")  # 将剩余不足20页的评论写入文件
        logging.info(f"用户 {self.user_id} 的微博 {mid} 共爬取" + str(self.comments_got_num) + u"条评论")
        self.all_comments = []
        self.comments_got_num = 0

    def get_all_weibo(self):
        """获取用户信息"""
        try:
            url = WEIBO_URL.format(self.user_id, self.weobo_containerid, 1)
            data = self.request_data(url)
            self.total_pages = int(self.userInfo["statuses_count"]/10)+1
            self.save_json(data, type='cards1.json')

            page1  = 0
            wrote_num = 0
            for i in tqdm.tqdm(range(self.total_pages), desc=f"【uid: {self.user_id}, 昵称: {self.userInfo['screen_name']}】爬取进度"):
                logging.info(f"【uid: {self.user_id}, 昵称: {self.userInfo['screen_name']}】爬取进度：{i+1}/{self.total_pages}")
                page = i+1
                url = WEIBO_URL.format(self.user_id, self.weobo_containerid, page)
                data = self.request_data(url)
                for card in data['cards']:
                    # 忽略广告等其他卡片
                    if card["card_type"] != 9:
                        continue
                    mblog = card["mblog"]
                    # 如果是转发微博的话，就抓取被转发者
                    if "retweeted_status" in mblog:
                        uid = mblog["retweeted_status"]["user"]["id"]
                        uname = mblog["retweeted_status"]["user"]["screen_name"]
                        logging.info(f'尝试抓取被转发者 {uid}, {uname}')
                        WBSpider.spide(user_id=uid)
                        continue
                    selector = etree.HTML(mblog["text"])
                    a_text = selector.xpath("//a/text()")
                    if u"全文" in a_text:
                        if None == self.get_long_weibo(mblog["mid"]):
                            logging.error(f'无法获取全文，uid: {self.user_id}，页数: {page}，微博：{mblog["mid"]}')
                            logging.error(f'其短文为 {mblog["text"]}')
                        else:
                            mblog["text"] = self.get_long_weibo(mblog["mid"])
                            selector = etree.HTML(mblog["text"])
                    # 将 HTML 转换为 txt
                    # 参考 https://www.zybuluo.com/Alston/note/778377
                    mblog["img_emoji"] = selector.xpath("//span/img/@alt")
                    mblog["text"] = etree.tostring(selector, method="text", encoding="UTF-8").decode('utf-8')
                    self.all_cards.append(card)
                    self.got_num += 1
                    # 抓取评论
                    self.get_comments(mblog["mid"])

                if page % 20 == 0:  # 每爬20页写入一次文件
                    # 写文件
                    if self.got_num > wrote_num:
                        self.write_csv(wrote_num)
                    wrote_num = self.got_num

            self.write_csv(wrote_num)  # 将剩余不足20页的微博写入文件
            logging.info(f"用户 {user_id} 共爬取" + str(self.got_num) + u"条原创微博")
            return True
        except Exception as e:
            logging.error(str(e))
            traceback.print_exc()

    def get_long_weibo(self, mid):
        """获取长微博"""
        try:
            url = LONG_WEIBO_URL.format(mid)
            data = self.request_data(url)
            long_content = data["longTextContent"]
            return long_content
        except Exception as e:
            logging.error(str(e))
            traceback.print_exc()

    def write_comment_csv(self, wrote_num, type):
        """将爬取的评论写入txt文件"""
        try:
            result_headers = [
                "mid",
                "评论 id",
                "评论人 id",
                "评论时间",
                "评论内容",
                "包含图片表情"
            ]
            result_data = [ [ comment["mid"], comment["id"], comment["user_id"], comment["created_at"], comment["text"], comment['img_emoji'] ] for comment in self.all_comments][wrote_num:]
            with open(self.get_filepath(type),
                          "a",
                          encoding="utf-8",
                          newline="") as f:
                    writer = csv.writer(f)
                    if wrote_num == 0:
                        writer.writerows([result_headers])
                    writer.writerows(result_data)
            assert self.comments_got_num == len(self.all_comments)
            print(u"%d条评论写入csv文件完毕,保存路径:" % self.comments_got_num)
            print(self.get_filepath(type))
        except Exception as e:
            logging.error(str(e))
            traceback.print_exc()

    def write_csv(self, wrote_num):
        """将爬取的信息写入txt文件"""
        try:
            result_headers = [
                "mid",
                "发布时间",
                "微博内容",
                "包含图片表情"
            ]
            result_data = [ [card["mblog"]["mid"], card["mblog"]["created_at"], card["mblog"]["text"], card["mblog"]['img_emoji'] ] for card in self.all_cards][wrote_num:]
            with open(self.get_filepath("csv"),
                          "a",
                          encoding="utf-8",
                          newline="") as f:
                    writer = csv.writer(f)
                    if wrote_num == 0:
                        writer.writerows([result_headers])
                    writer.writerows(result_data)
            assert self.got_num == len(self.all_cards)
            print(u"%d条微博写入csv文件完毕,保存路径:" % self.got_num)
            print(self.get_filepath("csv"))
        except Exception as e:
            logging.error(str(e))
            traceback.print_exc()

    def download_pictures(self):
        pass

    def get_filepath(self, type):
        """获取结果文件路径"""
        try:
            file_dir = os.path.dirname(os.path.realpath('__file__')) + os.sep + "weibo" + os.sep + self.userInfo["screen_name"]
            # 图片的话就是 'img' 目录
            if type == "img":
                file_dir = file_dir + os.sep + "img"
            # 没有目录的时候自动创建
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            if type == "img":
                return file_dir
            # 其他类型的话，直接返回 user_id.csv
            file_path = file_dir + os.sep + "%d" % self.user_id + "." + type
            return file_path
        except Exception as e:
            logging.error(str(e))
            traceback.print_exc()

def init_logging(name='testname', log_level=logging.INFO):
        file_dir = os.path.dirname(os.path.realpath('__file__')) + "/log"
        # 没有目录的时候自动创建
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        fileh = logging.FileHandler(file_dir+f'/{name}-{logging.getLevelName(log_level)}.log', 'w', encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")
        fileh.setFormatter(formatter)

        log = logging.getLogger()  # root logger
        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)
        log.addHandler(fileh)      # set the new handler
        log.setLevel(log_level)

        return fileh

if __name__ == "__main__":
    init_logging(name=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    login()
    for user_id in progress.crawling:
        WBSpider.spide(user_id)
