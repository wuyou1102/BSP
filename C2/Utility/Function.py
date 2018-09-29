# -*- encoding:UTF-8 -*-
import os
import time
from urllib import quote

def file_iterator(file_name, chunk_size=1024):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


__dict_commit = {
    "commit ": "Commit Id :",
    "Author:": "Author :",
    "Date:   ": "Data :",
    "Change-Id: ": "Change Id :",
    "Signed-off-by: ": "Signed Off :",
    "BugID: ": "Bug Id :"
}


def get_commit_blocks(lines):
    def remove_empty_lines():
        lines_with_out_empty = list()
        for ln in lines:
            if '    ' in ln:
                ln = ln.replace('    ', '')
            if ln:
                lines_with_out_empty.append(ln)
        return lines_with_out_empty

    lines = remove_empty_lines()
    blocks = []
    block = []
    for line in lines:
        if line.startswith('commit '):
            if block:
                blocks.append(block)
                block = list()
        block.append(quote(line))
    if block:
        blocks.append(block)
    return blocks


def format_commit_msg(lines):
    blocks = get_commit_blocks(lines=lines)
    lst = list()
    for block in blocks:
        commit = dict()
        commit_attrs = list()
        for line in block[:]:
            for k, v in __dict_commit.items():
                if line.startswith(k):
                    commit_attrs.append([v, line.lstrip(k)])
                    block.remove(line)
                    break
        commit["msg"] = block
        commit["attr"] = commit_attrs
        lst.append(commit)
    return lst


def create_folder(path):
    if not os.path.exists(path):
        print "Create New Folder: %s " % path
        os.makedirs(path)
    return path


def get_timestamp(time_fmt='%Y_%m_%d-%H_%M_%S', t=None):
    t = t if t else time.time()
    return time.strftime(time_fmt, time.localtime(t))


def get_time():
    return time.time()

if __name__ == '__main__':
    with open('D:\Profile\Desktop\ReleaseNotes.txt') as r :
        print format_commit_msg(r.readlines())

    # s="萨达"
    # print s
    # print repr(s)
    # a =  '\xe8\x90\xa8\xe8\xbe\xbe'
    # print a
    # print repr(a)
    #
    # print '1. \xe6\x95\xb4\xe5\x90\x88SIM 9/20 SDK'