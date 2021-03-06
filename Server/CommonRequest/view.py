# -*- encoding:UTF-8 -*-
import os
import sys

from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.utils.encoding import escape_uri_path
from Server.Utility import Function, Path
import chardet

reload(sys)
sys.setdefaultencoding('utf-8')

VersionConfig_Path = '/home/bspserver/sda/VersionConfig/'
sep = ' *|* '


def version_number_config(request):
    if request.method == 'GET':
        return render(request, 'BuildNumberConfig.html', __get_version_config_context())
    elif request.method == 'POST':
        data = request.POST
        form = data['Form']
        if form == "C2":
            __writer_version_config(os.path.join(VersionConfig_Path, "C2.txt"), data=data)
        return render(request, 'BuildNumberConfig.html', __get_version_config_context())


def __get_version_config_context():
    context = dict()
    context['C2'] = __parse_version_config(os.path.join(VersionConfig_Path, "C2.txt"))
    return context


def __writer_version_config(path, data):
    with open(path, 'w') as w_file:
        for attr_name in ['Project', 'HW', 'Market', 'Reserved', 'Edition', 'Release', 'Internal']:
            w_file.write('{name}{sep}{value}\n'.format(name=attr_name, value=data[attr_name], sep=sep))


def __parse_version_config(path):
    if os.path.exists(path):
        config = dict()
        with open(path) as r_file:
            for line in r_file.readlines():
                attrs = line.split(sep)
                config[attrs[0]] = attrs[1]
            return config
    else:
        return {}


def release_notes(request):
    if request.method == 'GET':
        context = dict()
        relative_path = get_relative_path(request)
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
        relative_path = get_relative_path(request)
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
        relative_path = get_relative_path(request)
        _type = request.GET["type"]
        abs_path = os.path.join(Path.get_path(_type), relative_path)
        print abs_path
        context['name'] = __get_name_from_path(relative_path)
        context['commits'] = __parse_commits(abs_path)
        return render(request, 'CommitHistory.html', context)
    else:
        return HttpResponse('method must be get')


def download_file(request):
    if request.method == 'GET':
        relative_path = get_relative_path(request)
        _type = request.GET["type"]
        version = __get_version(Path.get_path(_type), relative_path)
        file_path = os.path.join(Path.get_path(_type), relative_path)
        if os.path.exists(file_path):
            if _type.lower() in ['b29adaily', 'b29bdaily', 'b29aweekly', 'b29bweekly']:
                file_name = os.path.basename(file_path)
            else:
                file_name = __format_file_name(relative_path, version)
            response = StreamingHttpResponse(Function.file_iterator(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(file_name))
            return response
        else:
            return HttpResponse(u"对不起，没有找到文件：%s" % relative_path)
    else:
        return HttpResponse('method must be get')


def __get_version(path, relative_path):
    data = relative_path.split(os.sep)[0]
    version_txt = os.path.join(path, data, 'VersionNumber.txt')
    if os.path.exists(version_txt):
        with open(version_txt, 'r') as f:
            return f.read()
    return ''


def upload_file(request):
    if request.method == 'POST':
        uploadfile = request.FILES.get('file')
        _data = request.POST["version"]
        _type = request.POST["type"]
        _class = request.POST["cls"]
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
    file_name = file_name.replace('&', '_').replace('+', '_')
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
        encoding = get_encoding(file=path)
        with open(path, 'r') as rfile:
            lst = []
            for line in rfile.readlines():
                line = line.strip('\r\n')
                if line:
                    if encoding == "GB2312":
                        line = line.decode("gb2312").encode("utf-8")
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


def __format_file_name(path, version):
    _path = path.split(os.sep)
    if version:
        _path[0] = version
    # for m in ["Binary", "DebugInfo"]:
    #     if m in _path:
    #         _path.remove(m)
    return "_".join(_path)


def get_relative_path(request):
    path = request.GET["path"]
    if path[0] == '/':
        path = path.lstrip('/')
    return path


def get_encoding(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']
