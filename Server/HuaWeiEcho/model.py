import re
import urllib
from contextlib import closing

import requests
from bs4 import BeautifulSoup
import http.client

from HuaWeiEcho.core import recogonize_music_by_filepath


def model_recogonize_music_of_tiktok_video(maybeUrl):
    # 使用正则表达式匹配字符串中可能含有的链接
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    url = re.findall(pattern, maybeUrl)
    if url is not None and 'http://v.douyin.com' in url[0]:
        print(url[0])
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'Keep-Alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        response = requests.get(url[0], headers=headers)
        response.encoding = 'utf-8'
        result = response.text
        index1 = result.index('playAddr')
        index2 = result.index('cover')
        result = result[index1:index2]
        videoAddress = re.findall(pattern, result)
        if videoAddress is not None:
            print(videoAddress[0])
            r = requests.get(videoAddress[0], headers=headers, stream=True)
            f = open("./cache/tiktok-demo.mp4", "wb")
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
            result = recogonize_music_by_filepath('./cache/tiktok-demo.mp4')
            print(result)
            print('success')

def recognize_music(url):
    """
    通过url识别音乐
    返回结果list
    :param url: 解析得到的url
    """
def extract_music(url):
    """
    通过url获取音频文件并下载到服务器
    返回暂存地址
    :param url: 解析得到的url
    """
    pass



model_recogonize_music_of_tiktok_video(
    '#在抖音，记录美好生活#眼前这一幕，你愿意给这群为迎战跳绳世界杯进行赛前魔鬼训练，为中国🇨🇳争光的孩子们点赞吗？ http://v.douyin.com/Mq6VSc/ 复制此链接，打开【抖音短视频】，直接观看视频！！')
