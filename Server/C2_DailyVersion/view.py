# -*- encoding:UTF-8 -*-
from django.shortcuts import render
import os
from Server.Utility import Path

PATH_DAILY = Path.C2_DailyBuild


def get_build_info(request):
    context = dict()
    context['builds'] = __get_daily_build_info()
    return render(request, 'C2_DailyVersion.html', context)


def __get_daily_build_info():
    lst = []
    builds = os.listdir(PATH_DAILY)
    for build in builds:
        dict_build = dict()
        build_path = os.path.join(PATH_DAILY, build)
        binary = os.path.join(build_path, 'Binary')
        debuginfo = os.path.join(build_path, 'DebugInfo')
        commit_history = os.path.join(build_path, 'CommitHistory.txt')
        version = os.path.join(build_path, 'VersionNumber.txt')
        dict_build['name'] = build
        dict_build['binaries'] = __get_binary(binary)
        dict_build['debug_infos'] = __get_debug_info(debuginfo)
        dict_build['commit_history'] = __get_commit_history(commit_history)
        dict_build['version'] = __get_version_number(version)
        lst.append(dict_build)
    return sorted(lst, key=lambda k: k['name'], reverse=True)


def __get_version_number(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read().strip('\r\n')
    else:
        return ''


def __get_binary(path):
    lst = list()
    if not os.path.exists(path):
        return lst
    for f in os.listdir(path):
        if f.endswith('.zip'):
            file_path = os.path.join(path, f).replace(PATH_DAILY, '')
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
            file_path = os.path.join(path, f).replace(PATH_DAILY, '')
            file_name = f.rstrip('.zip')
            _file = [file_name, file_path]
            lst.append(_file)
    return lst


def __get_commit_history(path):
    if os.path.exists(path):
        return path.replace(PATH_DAILY, '')
    return "None"
