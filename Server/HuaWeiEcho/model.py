import re
import time
import urllib
from contextlib import closing

import requests
from bs4 import BeautifulSoup
import http.client
from urllib.request import urlretrieve
from HuaWeiEcho.core import recogonize_music_by_filepath
import requests

def model_recogonize_music_of_tiktok_video(maybeUrl):
    # 使用正则表达式匹配字符串中可能含有的链接
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    url = re.findall(pattern, maybeUrl)
    if url is not None and len(url) > 0 and 'http://v.douyin.com' in url[0]:
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
            f = open("tiktok-demo.mp4", "wb")
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
            result = recogonize_music_by_filepath('tiktok-demo.mp4')
            return result
        else:
            print('没有找到视频地址')
            return None

    else:
        print('maybeUrl中没有合法的url')
        return None

def search(key):
    """
    w：搜索关键字
    p：当前页
    n：每页歌曲数量
    format：数据格式
    :param key:
    """
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?g_tk=5381&p=1&n=10&' \
          'w=' + key + '&format=json&loginUin=0&hostUin=0&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&remoteplace=txt.yqq.song&t=0&aggr=1&cr=1&catZhida=1&flag_qc=0'
    session = requests.session()
    searchResult = session.get(url).json()
    return searchResult


def getSonginfo(key, num):
    """
    调用搜索显示歌曲列表
    :param key: 搜索的关键字
    :param num: 要显示的信息条数
    :return: resultlist每一条记录包括‘songmid’‘songname’‘singername’
    """
    jsonResult=search(key)
    result = []
    resultdict = {}
    data = jsonResult['data']
    song = data['song']
    songlist = song['list']
    for i in range(num):
        resultdict['songname'] = songlist[i]['songname']
        resultdict['songmid'] = songlist[i]['songmid']
        resultdict['singername']=songlist[i]['singer'][0]['name']
        result.append(resultdict)
        print(resultdict['singername'])
    return result


def getVkey(songmid):
    """
    songmid：歌曲mid。可从歌单、专辑、歌手、排行榜接口中获取
    filename：C400 + songmid + .m4a
    format：数据格式
    jsonpCallback：jsonp回调函数
    :param songmid:
    """
    url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=1278911659&hostUin=0&' \
          'format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747' \
          '&uin=0&songmid={songmid}&filename=C400{songmid}.m4a&guid=3655047200'.format(songmid=songmid)
    response = requests.get(url).json()
    data = response['data']
    items = data['items']
    for item in items:
        vkey = item['vkey']
        print(vkey)
        return vkey


def getMusicFile(key):
    songInfo = getSonginfo(key, 1)
    songmid=songInfo[0]['songmid']
    vkey = getVkey(songmid)

    url = urlretrieve('http://dl.stream.qqmusic.qq.com/C400{songmid}.m4a?' \
                      'vkey={vkey}&guid=3655047200&fromtag=66.mp3'.format(vkey=vkey, songmid=songmid),filename='tempfiles/'+songInfo[0]['songname']+'.mp3')

    filename =url[0]

    print(filename)
    print('2')
    return filename

#getMusicFile('狂浪')