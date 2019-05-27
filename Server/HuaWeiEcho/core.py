import json

from acrcloud.recognizer import ACRCloudRecognizer

from HuaWeiEcho.configure import *


def phase_json(resJson):
    try:
        print(resJson)
        metadata = resJson['metadata']
        musics = metadata['music']
        result_list = []
        if musics is not None:
            for music in musics:
                dic = {}
                dic['name'] = music['title']
                dic['score'] = music['score']
                result_list.append(dic)
        else:
            print('没有识别出来音乐')
            return None

        return result_list
    except:
        print('解析的时候出现了异常')
        return None


def recogonize_music_by_filepath(filepath):
    config = {
        # Replace "xxxxxxxx" below with your project's host, access_key and access_secret.
        'host': acr_host,
        'access_key': acr_access_key,
        'access_secret': acr_access_secret,
        'timeout': 10  # seconds
    }

    re = ACRCloudRecognizer(config)
    res = re.recognize_by_file(filepath, 0)
    resJson = json.loads(res)
    result = phase_json(resJson)

    return result


def recogonize_music_by_filebuf(filebuf):
    config = {
        # Replace "xxxxxxxx" below with your project's host, access_key and access_secret.
        'host': acr_host,
        'access_key': acr_access_key,
        'access_secret': acr_access_secret,
        'timeout': 10  # seconds
    }

    re = ACRCloudRecognizer(config)
    res = re.recognize_by_filebuffer(filebuf, 0)
    resJson = json.loads(res)
    result = phase_json(resJson)

    return result



