# -*- encoding:UTF-8 -*-
from django.http import HttpResponse

from django.shortcuts import render
import os

DailyBuildPath = "/home/bspserver/sda/C2_DailyBuild/"


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
            file_path = os.path.join(path, f)
            file_name = f.rstrip('.zip')
            lst.append((file_name, file_path))
    return lst


def __get_debug_info(path):
    lst = list()
    for f in os.listdir(path):
        if f.endswith('.zip'):
            file_path = os.path.join(path, f)
            file_name = f.rstrip('.zip')
            lst.append((file_name, file_path))
    return lst


def __get_release_notes(path):
    if os.path.exists(path):
        file_path, file_name = os.path.split(path)
        return file_name, path
    return None, None
