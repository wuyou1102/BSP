# -*- encoding:UTF-8 -*-
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
import os
from C2.Utility import Function, Path
import sys
from django.utils.encoding import escape_uri_path

reload(sys)
sys.setdefaultencoding('utf-8')


def release_notes(request):
    if request.method == 'GET':
        context = dict()
        relative_path = request.GET["path"]
        _type = request.GET["type"]
        abs_path = os.path.join(Path.get_path(_type), relative_path)
        context['name'] = __get_name_from_path(relative_path)
        context['release_notes'] = __parse_release_note(abs_path)
        return render(request, 'ReleaseNotes.html', context)
    else:
        return HttpResponse('method must be get')


def view_history(request):
    if request.method == 'GET':
        context = dict()
        relative_path = request.GET["path"]
        _type = request.GET["type"]
        abs_path = os.path.join(Path.get_path(_type), relative_path)
        context['name'] = __get_name_from_path(relative_path)
        context['history'] = __parse_history(abs_path)
        return render(request, 'History.html', context)
    else:
        return HttpResponse('method must be get')


def commit_history(request):
    if request.method == 'GET':
        context = dict()
        relative_path = request.GET["path"]
        _type = request.GET["type"]
        abs_path = os.path.join(Path.get_path(_type), relative_path)
        context['name'] = __get_name_from_path(relative_path)
        context['commits'] = __parse_commits(abs_path)
        return render(request, 'CommitHistory.html', context)
    else:
        return HttpResponse('method must be get')


def download_file(request):
    if request.method == 'GET':
        relative_path = request.GET["path"]
        print relative_path
        _type = request.GET["type"]
        file_path = os.path.join(Path.get_path(_type), relative_path)
        if os.path.exists(file_path):
            file_name = __format_file_name(relative_path)
            response = StreamingHttpResponse(Function.file_iterator(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(file_name))
            return response
        else:
            return HttpResponse(u"对不起，没有找到文件：%s" % relative_path)
    else:
        return HttpResponse('method must be get')


def upload_file(request):
    if request.method == 'POST':
        uploadfile = request.FILES.get('file')
        _data = request.POST["version"]
        _type = request.POST["type"]
        _class = request.GET["cls"]
        backup_folder = Function.create_folder(os.path.join(Path.get_path(_type), _data, "Backup"))
        history_text = os.path.join(backup_folder, "History.txt")
        if uploadfile is None:
            return HttpResponse("Nothing Upload")
        else:
            if _class == "ReleaseNotes":
                store_path = Function.create_folder(os.path.join(Path.get_path(_type), _data))
                result = store_release_notes(store_path=store_path, uploadfile=uploadfile, history=history_text,
                                             backup=backup_folder)
                return HttpResponse(result)
            elif _class == "Report":
                store_path = Function.create_folder(os.path.join(Path.get_path(_type), _data, "Reports"))
                result = store_report(store_path=store_path, uploadfile=uploadfile, history=history_text,
                                      backup=backup_folder)
                return HttpResponse(result)
            return HttpResponse('Error')
    else:
        return HttpResponse('method must be post')


def store_release_notes(store_path, uploadfile, history, backup):
    file_name = uploadfile.name
    Function.create_folder(path=store_path)
    __write_history(history=history, msg="Upload %s" % file_name)
    if not file_name.endswith(".txt"):
        __write_history(history=history, msg="Upload Fail %s" % file_name)
        return u"版本说明文件格式不正确"
    file_path = os.path.join(store_path, "ReleaseNotes.txt")
    if os.path.exists(file_path):
        __write_history(history=history, msg="Find duplicate release notes")
        backup_file = "ReleaseNotes.txt.%s" % Function.get_time()
        os.rename(file_path, os.path.join(backup, backup_file))
        __write_history(history=history, msg="{src}  --->  {dst}".format(src="ReleaseNotes.txt", dst=backup_file))
    with open(file_path, 'wb+') as f:
        for chunk in uploadfile.chunks():
            f.write(chunk)
    __write_history(history=history, msg="Upload %s Success" % file_name)
    return u"上传成功"


def store_report(store_path, uploadfile, history, backup):
    file_name = uploadfile.name
    file_name = file_name.replace('&', '_')
    Function.create_folder(path=store_path)
    __write_history(history=history, msg="Upload %s" % file_name)
    file_path = os.path.join(store_path, file_name)
    if os.path.exists(file_path):
        __write_history(history=history, msg="Find duplicate %s" % file_name)
        backup_file = "%s.%s" % (file_name, Function.get_time())
        os.rename(file_path, os.path.join(backup, backup_file))
        __write_history(history=history, msg="{src}  --->  {dst}".format(src=file_name, dst=backup_file))
    with open(file_path, 'wb+') as f:
        for chunk in uploadfile.chunks():
            f.write(chunk)
    __write_history(history=history, msg="Upload %s Success" % file_name)
    return u"上传成功"


def __write_history(history, msg):
    with open(history, 'a') as f:
        f.write("{time} : {msg}\n".format(time=Function.get_timestamp(), msg=msg))


def __get_name_from_path(path):
    name, text = os.path.split(path)
    return name


def __parse_commits(path):
    if os.path.exists(path):
        with open(path, 'r') as rfile:
            lines = rfile.readlines()
            return Function.format_commit_msg(lines)
    else:
        return []


def __parse_release_note(path):
    if os.path.exists(path):
        with open(path, 'r') as rfile:
            lst = []
            for line in rfile.readlines():
                line = line.strip('\r\n')
                if line:
                    lst.append(line)
            return lst
    else:
        return []


def __parse_history(path):
    if os.path.exists(path):
        with open(path, 'r') as rfile:
            lst = []
            for line in rfile.readlines():
                line = line.strip('\r\n')
                if line:
                    lst.append(line)
            return lst
    else:
        return []


def __format_file_name(path):
    _path = path.split(os.sep)
    # for m in ["Binary", "DebugInfo"]:
    #     if m in _path:
    #         _path.remove(m)
    return "_".join(_path)
