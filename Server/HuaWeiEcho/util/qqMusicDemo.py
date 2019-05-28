import requests
import json


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
    searchResult = requests.get(url).json()
    print(searchResult)


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
        return vkey
        print(vkey)


def getMusicFile(songmid):
    vkey = getVkey(songmid)
    url = 'http://dl.stream.qqmusic.qq.com/C400{songmid}.m4a?' \
          'vkey={vkey}&guid=3655047200&fromtag=66'.format(vkey=vkey, songmid=songmid)

    stream=requests.get(url,stream=True)
    f = open("qq-demo.mp3", "wb")
    for chunk in stream.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    f.close()
    print('success')


getMusicFile('003UMBTb2h2W3S')
