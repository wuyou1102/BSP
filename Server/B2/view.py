# -*- encoding:UTF-8 -*-
from django.shortcuts import render
import os
from Server.Utility import Path
from django.http import HttpResponse


def GetDailyBuildInfo(request):
    if request.method == 'GET':
        _type = request.GET["type"]
        path = __get_path(_type)
        context = dict()
        context['type'] = _type
        context['builds'] = __get_daily_build_info(path)
        return render(request, 'DailyBuild.html', context)
    else:
        return HttpResponse('method must be get')


def __get_daily_build_info(path):
    lst = []
    builds = os.listdir(path)
    for build in builds:
        dict_build = dict()
        build_path = os.path.join(path, build)
        version = os.path.join(build_path, 'VersionNumber.txt')
        commit_history = os.path.join(build_path, 'CommitHistory.txt')
        dict_build['name'] = build
        dict_build['version'] = __get_version_number(version)
        dict_build['images'] = __get_images(build_path, need_replace=path)
        dict_build['commit_history'] = __get_commit_history(commit_history, need_replace=path)

        lst.append(dict_build)
    return sorted(lst, key=lambda k: k['name'], reverse=True)


def __get_version_number(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read().strip('\r\n')
    else:
        return ''


def __get_images(path, need_replace):
    lst = list()
    if not os.path.exists(path):
        return lst
    for f in os.listdir(path):
        if f.endswith('.img'):
            file_path = os.path.join(path, f).replace(need_replace, '')
            file_name = f.rstrip('.img')
            _file = [file_name, file_path]
            lst.append(_file)
    return sorted(lst, key=lambda k: k[0], reverse=False)


def __get_commit_history(path, need_replace):
    if os.path.exists(path):
        return path.replace(need_replace, '')
    return "None"


def __get_path(_type):
    if _type == "9A":
        return Path.B2_9A_DailyBuild
    else:
        return Path.B2_9B_DailyBuild
