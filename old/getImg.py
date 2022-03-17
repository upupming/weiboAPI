import re
import os,stat
import urllib.request
filename = "test.txt"
file = open(filename,encoding='UTF-8')
text = file.readlines()
img = {}
for line in text:
    pattern = '<img[^>]*/>'
    result = re.findall(pattern, line)
    for r in result:
        pattern_1 = 'alt=.*?.]'
        p1 = re.findall(pattern_1, r)
        x = p1[0].split("[")
        xx = x[1].replace("]", "")
        # print(xx)
        pattern_2 = 'h5.sinaimg.*?\.png'
        p2 = re.findall(pattern_2, r)
        # print(p2[0])
        img[xx] = p2[0]

print(img)
url_list = "http://h5.sinaimg.cn/m/emoticon/icon/default/d_tu-b5c18d9140.png"
save_path = 'weibo\\Images\\1.png'


for name in img.keys():
    save_path = 'weibo\\Images\\' + str(name) + '.png'
    url_list = img[name]
    pic_file = urllib.request.urlopen("http://" + url_list).read()
    f = open(save_path, "wb")
    f.write(pic_file)
    f.close()