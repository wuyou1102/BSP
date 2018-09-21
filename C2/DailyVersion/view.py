# -*- encoding:UTF-8 -*-

from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
import os

DailyBuildPath = "/home/bspserver/sda/C2_DailyBuild/"


def download_file(request):
    def file_iterator(file_name, chunk_size=1024):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    relative_path = request.GET["path"]
    print relative_path
    file_path = os.path.join(DailyBuildPath, relative_path)
    if os.path.exists(file_path):
        response = StreamingHttpResponse(file_iterator(file_path))
        return response
    else:
        return HttpResponse("错误，没有找到文件：%s" % relative_path)


def get_daily_build_info(request):
    context = dict()
    context['builds'] = __get_daily_build_info()
    print context
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
    return lst


def __get_binary(path):
    lst = list()
    for f in os.listdir(path):
        if f.endswith('.zip'):
            file_path = os.path.join(path, f).replace(DailyBuildPath, '')
            file_name = f.rstrip('.zip')
            _file = [file_name, file_path]
            lst.append(_file)
    return lst


def __get_debug_info(path):
    lst = list()
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
