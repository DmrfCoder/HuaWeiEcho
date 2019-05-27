import re


def model_recogonize_music_of_tiktok_video(maybeUrl):
    # 使用正则表达式匹配字符串中可能含有的链接
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    url = re.findall(pattern, maybeUrl)
    return url


