# -*- encoding:UTF-8 -*-
from django.shortcuts import render
import os
from C2.Utility import Path

PATH_9A_DAILY = Path.B2_9A_DailyBuild
PATH_9B_DAILY = Path.B2_9B_DailyBuild


def get_9A_build_info(request):
    context = dict()
    context['builds'] = __get_daily_build_info(PATH_9A_DAILY)
    return render(request, '9A_DailyVersion.html', context)


def get_9B_build_info(request):
    context = dict()
    context['builds'] = __get_daily_build_info(PATH_9B_DAILY)
    return render(request, '9B_DailyVersion.html', context)


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
        if f.endswith('.zip'):
            file_path = os.path.join(path, f).replace(need_replace, '')
            file_name = f.rstrip('.zip')
            _file = [file_name, file_path]
            lst.append(_file)
    return sorted(lst, key=lambda k: k[0], reverse=False)


def __get_commit_history(path, need_replace):
    if os.path.exists(path):
        return path.replace(need_replace, '')
    return "None"
