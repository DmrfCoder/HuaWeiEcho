from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import json

from django.views.decorators.http import require_GET

from HuaWeiEcho import model

# Create your views here.
from HuaWeiEcho.model import *


def index(request):
    return render(request, "index.html")
    pass


@require_GET
def recogonize_music_of_tiktok_video(request):
    """
    识别抖音链接中视频的背景音乐
    请求格式：GET
    参数(json格式）：
        - maybeUrl：可能含有抖音视频链接的字符串，从中提取出抖音链接后进行识别
    返回值（json格式）：
        - resultCode：状态码，表示是否识别成功，0代表未识别出背景音乐，代表识别出了背景音乐
        - resultMusicList：识别结果
    :param request:
    :return:
    """
    print('接收到请求-------')

    # 从get请求的参数(params)中获取key为maybeUrl的参数
    maybeUrl = request.GET.get('maybeUrl', None)
    if maybeUrl is not None:
        print('收到url：'+maybeUrl)
        result = model_recogonize_music_of_tiktok_video(maybeUrl)
        if result is not None:
            resp = {'success': True, 'result': result}
            print('返回success')
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            resp = {'success': False, 'desc': '没有下载到正确的视频'}
            print('返回failed')
            return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        resp = {'success': False, 'desc': '没有找到合法的urlgi'}
        print('返回failed')
        return HttpResponse(json.dumps(resp), content_type="application/json")
        print('没有从maybeUrl中获取到url参数')



def recognize_music(request):
    result = []
    try:
        data = json.loads(request.body)
        raw_url = data.get("url", None)

        # url=model.model_recogonize_music_of_tiktok_video(raw_url)
        print(raw_url)
        # result=model.recognize_music(url)
    except:

        result = ['error']
    return HttpResponse(json.dumps(result))


def download_file(request):
    #download_name=recognize_music(request)
    # download_name = request.GET["file"]
    # the_file_name = str(download_name).split("/")[-1]  # 显示在弹出对话框中的默认的下载文件名
    download_name='狂浪'
    music_path=getMusicFile(download_name)
    #music_path='C:/Code/HuaWeiEcho/Server/tempfiles/Piano Sonata No.16 in C , K.545.mp3'

    print('1')
    response = StreamingHttpResponse(readFile(music_path))
    response['Content-Type'] = 'application/octet-stream'
    return response


def readFile(filename, chunk_size=512):
    """
    读取文件流方法
    """
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
