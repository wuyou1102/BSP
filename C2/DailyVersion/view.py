# -*- encoding:UTF-8 -*-

from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
import os

DailyBuildPath = "/home/bspserver/sda/C2_DailyBuild/"


def file_iterator(file_name, chunk_size=1024):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def format_file_name(path):
    _path = path.split(os.sep)
    for m in ["Binary", "DebugInfo"]:
        if m in _path:
            _path.remove(m)
    return "_".join(_path)


def download_file(request):
    if request.method == 'GET':
        relative_path = request.GET["path"]
        file_path = os.path.join(DailyBuildPath, relative_path)
        if os.path.exists(file_path):
            file_name = format_file_name(relative_path)
            response = StreamingHttpResponse(file_iterator(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename=%s' % file_name
            return response
        else:
            return HttpResponse(u"对不起，没有找到文件：%s" % relative_path)
            return response
    else:
        return HttpResponse('method must be get')


def get_daily_build_info(request):
    context = dict()
    context['builds'] = __get_daily_build_info()
    return render(request, 'DailyVersion.html', context)


def __get_daily_build_info():
    lst = []
    builds = os.listdir(DailyBuildPath)
    for build in builds:
        dict_build = dict()
        build_path = os.path.join(DailyBuildPath, build)
        binary = os.path.join(build_path, 'Binary')
        debuginfo = os.path.join(build_path, 'DebugInfo')
        release_notes = os.path.join(build_path, 'ReleaseNotes.txt')
        dict_build['name'] = build
        dict_build['binary'] = __get_binary(binary)
        dict_build['debug_info'] = __get_debug_info(debuginfo)
        dict_build['release_notes'] = __get_release_notes(release_notes)
        lst.append(dict_build)
    return sorted(lst, key=lambda k: k['name'], reverse=True)


def __get_binary(path):
    lst = list()
    if not os.path.exists(path):
        return lst
    for f in os.listdir(path):
        if f.endswith('.zip'):
            file_path = os.path.join(path, f).replace(DailyBuildPath, '')
            file_name = f.rstrip('.zip')
            _file = [file_name, file_path]
            lst.append(_file)
    return lst


def __get_debug_info(path):
    lst = list()
    if not os.path.exists(path):
        return lst
    for f in os.listdir(path):
        if f.endswith('.zip'):
            file_path = os.path.join(path, f).replace(DailyBuildPath, '')
            file_name = f.rstrip('.zip')
            _file = [file_name, file_path]
            lst.append(_file)
    return lst


def __get_release_notes(path):
    if os.path.exists(path):
        return path.replace(DailyBuildPath, '')
    return None
