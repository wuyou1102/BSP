# -*- encoding:UTF-8 -*-
import os
import time


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
        for l in lines:
            if '    ' in l:
                l = l.replace('    ', '')
            if l:
                lines_with_out_empty.append(l)
        return lines_with_out_empty

    lines = remove_empty_lines()
    blocks = []
    block = []
    for line in lines:
        if line.startswith('commit '):
            if block:
                blocks.append(block)
                block = list()
        block.append(line)
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
    with open("D:\Profile\Desktop\ReleaseNotes.txt") as w:
        print format_commit_msg(w.readlines())
    print '1. \xe6\x95\xb4\xe5\x90\x88SIM 9/20 SDK'
    print '1. \xc3\xa6\xc2\x95\xc2\xb4\xc3\xa5\xc2\x90\xc2\x88SIM 9/20 SDK'