# -*- encoding:UTF-8 -*-
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
import os
from C2 import Utility

DailyBuildPath = "/home/bspserver/sda/C2_DailyBuild/"


def view_release_notes(request):
    if request.method == 'GET':
        context = dict()
        relative_path = request.GET["path"]
        path = os.path.join(DailyBuildPath, relative_path)
        context['name'] = __get_build_name(relative_path)
        context['notes'] = __parse_release_notes(path)
        return render(request, 'ReleaseNotes.html', context)
    else:
        return HttpResponse('method must be get')


def download_file(request):
    if request.method == 'GET':
        relative_path = request.GET["path"]
        file_path = os.path.join(DailyBuildPath, relative_path)
        if os.path.exists(file_path):
            file_name = __format_file_name(relative_path)
            response = StreamingHttpResponse(Utility.file_iterator(file_path))
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


def __format_file_name(path):
    _path = path.split(os.sep)
    for m in ["Binary", "DebugInfo"]:
        if m in _path:
            _path.remove(m)
    return "_".join(_path)


def __get_build_name(path):
    name, text = os.path.split(path)
    return name


def __parse_release_notes(path):
    if os.path.exists(path):
        with open(path, 'r') as rfile:
            lines = rfile.readlines()
            return Utility.format_commit_msg(lines)
    else:
        return []


if __name__ == '__main__':
    commits = __parse_release_notes('D:\Profile\Desktop\ReleaseNotes.txt')
    print len(commits)
    print commits
