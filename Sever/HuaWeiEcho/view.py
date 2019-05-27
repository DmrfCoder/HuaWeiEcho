from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST

from HuaWeiEcho.model import model_recogonize_music_of_tiktok_video


@require_GET
def hello(request):
    return HttpResponse("Hello world ! ")


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

    maybeUrl = request.GET.get('maybeUrl', None)
    url = "error"
    if maybeUrl is not None:
        print(maybeUrl)
        url = model_recogonize_music_of_tiktok_video(maybeUrl)
        print(url)

    return HttpResponse(url)


@require_POST
def recogonize_music_of_upload_video(request):
    """
    识别上传的本地视频中的背景音乐
    :param request:
    :return:
    """
    return HttpResponse("demo")


@require_POST
def extract_music_of_upload_video(request):
    """
    提取上传视频中的背景音乐
    :param request:
    :return:
    """
    return HttpResponse("demo")
