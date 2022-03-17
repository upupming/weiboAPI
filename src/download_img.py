from emoji import *
import requests

(img_desc_arr, img_link_arr) = get_img_emojis()

CUR_DIR = os.path.dirname(os.path.realpath('__file__')) + os.sep

print(img_desc_arr)

def download_pic(name, url):
    p = requests.get(url)
    with open(CUR_DIR + '/imgs/' + name + '.png', "wb") as f:
        f.write(p.content)

for i in range(len(img_desc_arr)):
    download_pic(f'img_{i}', img_link_arr[i])