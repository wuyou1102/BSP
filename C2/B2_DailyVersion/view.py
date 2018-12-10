# -*- encoding:UTF-8 -*-
from django.shortcuts import render
import os
from C2.Utility import Path

PATH_9A_DAILY = Path.B2_DailyBuild
PATH_9B_DAILY = Path.B2_DailyBuild


def get_9A_build_info(request):
    context = dict()
    context['builds'] = __get_daily_build_info(PATH_9A_DAILY)
    return render(request, 'B2_9A_DailyVersion.html', context)


def get_9B_build_info(request):
    context = dict()
    context['builds'] = __get_daily_build_info(PATH_9B_DAILY)
    return render(request, 'B2_9B_DailyVersion.html', context)


def __get_daily_build_info(path):
    PATH_DAILY = path
    lst = []
    builds = os.listdir(PATH_DAILY)
    for build in builds:
        dict_build = dict()
        build_path = os.path.join(PATH_DAILY, build)
        version = os.path.join(build_path, 'VersionNumber.txt')
        commit_history = os.path.join(build_path, 'CommitHistory.txt')
        dict_build['name'] = build
        dict_build['version'] = __get_version_number(version)
        dict_build['images'] = __get_images(build_path)
        dict_build['commit_history'] = __get_commit_history(commit_history)

        lst.append(dict_build)
    return sorted(lst, key=lambda k: k['name'], reverse=True)


def __get_version_number(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read().strip('\r\n')
    else:
        return ''


def __get_images(path):
    lst = list()
    if not os.path.exists(path):
        return lst
    for f in os.listdir(path):
        if f.endswith('.zip'):
            file_path = os.path.join(path, f).replace(PATH_DAILY, '')
            file_name = f.rstrip('.zip')
            _file = [file_name, file_path]
            lst.append(_file)
    return sorted(lst, key=lambda k: k[0], reverse=False)


def __get_commit_history(path):
    if os.path.exists(path):
        return path.replace(PATH_DAILY, '')
    return "None"
