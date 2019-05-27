from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import json
from HuaWeiEcho import model
# Create your views here.


def index(request):
    return render(request,"index.html")
    pass





def recognize_music(request):
    result = []
    try:
        data = json.loads(request.body)
        raw_url=data.get("url",None)

        url=model.model_recogonize_music_of_tiktok_video(raw_url)
        print(url)
        #result=model.recognize_music(url)
    except:
        result=['error']
    return HttpResponse(json.dumps(result))

def download_file(request):
    """
    下载文件
    """
    # download_name = request.GET["file"]
    # the_file_name = str(download_name).split("/")[-1]  # 显示在弹出对话框中的默认的下载文件名
    try:
        data = json.loads(request.body)
        url=data.get("url",None)
        print(url)
    except:
        print('url error')
    #music_path=model.extract_music(url)
    music_path='C:/Code/Echo/tempfiles/1.txt'
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