# -*- encoding:UTF-8 -*-
from django.shortcuts import render
import os
from C2.Utility import Path

PATH_DAILY = Path.B2_DailyBuild


def get_build_info(request):
    context = dict()
    context['builds'] = __get_daily_build_info()
    return render(request, 'B2_DailyVersion.html', context)


def __get_daily_build_info():
    lst = []
    builds = os.listdir(PATH_DAILY)
    for build in builds:
        dict_build = dict()
        build_path = os.path.join(PATH_DAILY, build)
        commit_history = os.path.join(build_path, 'CommitHistory.txt')
        dict_build['name'] = build
        dict_build['binaries'] = __get_binary(build_path)
        dict_build['commit_history'] = __get_commit_history(commit_history)
        lst.append(dict_build)
    return sorted(lst, key=lambda k: k['name'], reverse=True)


def __get_binary(path):
    lst = list()
    if not os.path.exists(path):
        return lst
    for f in os.listdir(path):
        if f.endswith('.img'):
            file_path = os.path.join(path, f).replace(PATH_DAILY, '')
            file_name = f.rstrip('.img')
            _file = [file_name, file_path]
            lst.append(_file)
    return lst


def __get_commit_history(path):
    if os.path.exists(path):
        return path.replace(PATH_DAILY, '')
    return "None"
