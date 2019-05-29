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
    from urllib.request import urlretrieve
    url = urlretrieve('http://dl.stream.qqmusic.qq.com/C400{songmid}.m4a?' \
                      'vkey={vkey}&guid=3655047200&fromtag=66.mp3'.format(vkey=vkey, songmid=songmid))
    filename = url[0] + '.mp3'
    print(filename)
    return filename
    # stream=requests.get(url)
    # print(stream.content)
    # f = open("qq-demo.m4a", "wb")
    # for chunk in stream.iter_content(chunk_size=512):
    #     if chunk:
    #         f.write(chunk)
    # f.close()
    # print('success')


# search("狂浪")
#getMusicFile('狂浪')
