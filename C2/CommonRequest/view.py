# -*- encoding:UTF-8 -*-
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
import os
from C2.Utility import Function, Path


def commit_history(request):
    if request.method == 'GET':
        context = dict()
        relative_path = request.GET["path"]
        _type = request.GET["type"]
        abs_path = os.path.join(Path.get_path(_type), relative_path)
        context['name'] = __get_commit_history_name(relative_path)
        context['commits'] = __parse_commits(abs_path)
        return render(request, 'CommitHistory.html', context)
    else:
        return HttpResponse('method must be get')


def download_file(request):
    if request.method == 'GET':
        relative_path = request.GET["path"]
        _type = request.GET["type"]
        file_path = os.path.join(Path.get_path(_type), relative_path)
        if os.path.exists(file_path):
            file_name = __format_file_name(relative_path)
            response = StreamingHttpResponse(Function.file_iterator(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename=%s' % file_name
            return response
        else:
            return HttpResponse(u"对不起，没有找到文件：%s" % relative_path)
    else:
        return HttpResponse('method must be get')


def __get_commit_history_name(path):
    name, text = os.path.split(path)
    return name


def __parse_commits(path):
    if os.path.exists(path):
        with open(path, 'r') as rfile:
            lines = rfile.readlines()
            return Function.format_commit_msg(lines)
    else:
        return []


def __format_file_name(path):
    _path = path.split(os.sep)
    for m in ["Binary", "DebugInfo"]:
        if m in _path:
            _path.remove(m)
    return "_".join(_path)
